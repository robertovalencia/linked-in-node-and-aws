#!/usr/bin/env python3
"""Failure-path tests using fake AWS/Terraform/curl executables, never AWS."""
import contextlib
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('operator_commands', Path(__file__).with_name('aws-ecs-operator.py'))
op = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(op)

FAKE_CLI = r'''#!PYTHON
import json, os, pathlib, sys
args = sys.argv[1:]
name = pathlib.Path(sys.argv[0]).name
scenario = json.loads(pathlib.Path(os.environ['OP_TEST_SCENARIO']).read_text())
keys = ['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','AWS_SESSION_TOKEN','AWS_ROLE_ARN','AWS_WEB_IDENTITY_TOKEN_FILE','AWS_CONTAINER_CREDENTIALS_FULL_URI','AWS_DEFAULT_PROFILE','TF_CLI_ARGS_plan','TF_VAR_project','TF_DATA_DIR','TF_WORKSPACE','TF_LOG','AWS_CONFIG_FILE','AWS_SHARED_CREDENTIALS_FILE','PYTHONOPTIMIZE']
with open(os.environ['OP_TEST_LOG'],'a') as f:
 f.write(json.dumps({'name':name,'args':args,'forbiddenEnvPresent':[k for k in keys if k in os.environ],'profile':os.getenv('AWS_PROFILE'),'region':os.getenv('AWS_REGION')})+'\n')
def emit(x): print(json.dumps(x))
if name == 'curl': print(scenario.get('ip','203.0.113.7'))
elif name == 'terraform':
 if args[:2] == ['workspace','show']: print(scenario.get('workspace','default'))
 elif args[0] == 'plan':
  if scenario.get('plan_fails'): print('intentional plan failure',file=sys.stderr);sys.exit(1)
  target=pathlib.Path(next(a.split('=',1)[1] for a in args if a.startswith('-out=')));target.write_bytes(b'fake-saved-plan')
 elif args[:2] == ['show','-json']: emit({'format_version':'1.2','private_payload':'not-for-transcript'})
 else: raise SystemExit('Unexpected Terraform command')
elif name == 'aws':
 pair=args[:2]
 if pair == ['sts','get-caller-identity']: emit({'Account':scenario.get('account','772641336063')})
 elif pair == ['freetier','get-account-plan-state']: emit({'accountPlanType':'FREE','accountPlanStatus':'ACTIVE','accountPlanRemainingCredits':{'amount':100,'unit':'USD'}})
 elif pair == ['s3api','head-object']:
  mode=scenario.get('state','absent')
  if mode=='present':emit({'ContentLength':500})
  else:print('An error occurred ('+('403' if mode=='denied' else '404')+')',file=sys.stderr);sys.exit(254)
 elif pair == ['acm','describe-certificate']:emit({'Status':scenario.get('cert','ISSUED'),'DomainName':'app.linked-in-node-rv.dynv6.net','Export':'DISABLED'})
 elif pair == ['ecs','describe-clusters']:
  emit({'clusters':[{'clusterName':'existing'}],'failures':[]} if scenario.get('existing_cluster') else {'clusters':[],'failures':[{'reason':'MISSING'}]})
 elif pair == ['rds','describe-db-instances']: print('An error occurred (DBInstanceNotFound)',file=sys.stderr);sys.exit(254)
 elif pair == ['elbv2','describe-load-balancers']: print('An error occurred (LoadBalancerNotFound)',file=sys.stderr);sys.exit(254)
 elif pair == ['ec2','describe-vpcs']:emit(scenario.get('vpcs',[]))
 else:raise SystemExit('Unexpected AWS command')
else:raise SystemExit('Unexpected fake executable')
'''
FAKE_REVIEW = r'''import hashlib,json,pathlib,sys,os
args=sys.argv[1:]
report=pathlib.Path(args[args.index('--report')+1]);binary=pathlib.Path(args[args.index('--plan-binary')+1])
mode=json.loads(pathlib.Path(os.environ['OP_TEST_SCENARIO']).read_text())
if mode.get('review_fails'): raise SystemExit('intentional reviewer failure')
report.write_text(json.dumps({'status':'WRONG' if mode.get('bad_review') else 'S3_BACKED_HTTPS_INFRASTRUCTURE_PLAN_REVIEWED_NOT_APPROVED','planBinarySha256':hashlib.sha256(binary.read_bytes()).hexdigest()}));report.chmod(0o600)
print('Strict reviewer fixture complete')
'''


class OperatorSafety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='aws-operator-tests-')
        self.repo = (Path(self.tmp.name) / 'repo').resolve()
        self.work = self.repo / 'work'
        self.base = self.work / 'aws-operator-preparation-2026-10-29'
        self.source = self.repo / 'infra/aws-ecs-dev'
        (self.source / '.terraform').mkdir(parents=True)
        self.base.mkdir(parents=True)
        (self.repo / 'scripts').mkdir()
        self.bin = Path(self.tmp.name) / 'bin'
        self.bin.mkdir()
        self.scenario = Path(self.tmp.name) / 'scenario.json'
        self.log = Path(self.tmp.name) / 'commands.jsonl'
        self.scenario.write_text('{}')
        for command in ['aws','terraform','curl']:
            target=self.bin/command
            target.write_text(FAKE_CLI.replace('PYTHON',sys.executable));target.chmod(0o700)
        (self.repo/'scripts/aws-ecs-review-plan.py').write_text(FAKE_REVIEW)
        (self.source/'kafka-user-data.sh.tftpl').write_text('broker-template')
        self.backend = {'type':'s3','config':{'bucket':op.BUCKET,'key':op.STATE_KEY,'region':op.REGION,
            'encrypt':True,'use_lockfile':True,'allowed_account_ids':[op.ACCOUNT],
            'workspace_key_prefix':op.BACKEND['workspaceKeyPrefix'],'profile':None}}
        self.cache=self.source/'.terraform/terraform.tfstate'
        self.cache.write_text(json.dumps({'backend':self.backend}))
        self.https = self.write('https-context.json',{'account':op.ACCOUNT,'region':op.REGION,
            'certificateStatus':'ISSUED','certificateArn':'arn:aws:acm:us-east-2:'+op.ACCOUNT+':certificate/ae18667c-47ac-4fda-8039-e877bafe9705',
            'applicationHostname':'app.linked-in-node-rv.dynv6.net','approvedClientCidrs':['203.0.113.7/32']})
        self.s3 = self.write('s3-context.json',op.BACKEND)
        self.inputs_value={'region':op.REGION,'project':'linked-in-node','owner':'robertovalencia',
            'approved_client_cidrs':['203.0.113.7/32'],'application_hostname':'app.linked-in-node-rv.dynv6.net',
            'certificate_arn':json.loads(self.https.read_text())['certificateArn'],'deploy_application':False,
            'image_digests':None,'seed_demo':False,'protect_database':True,'teardown_discard_demo_data':False,
            'kafka_image':'apache/kafka:4.0.1@sha256:'+'a'*64,'postgres_engine_version':'17.6',
            'recovery_snapshot_suffix':'test-20261029',
            'expires_at':(datetime.now(timezone.utc)+timedelta(hours=24)).isoformat()}
        self.inputs=self.write('inputs.json',self.inputs_value)
        self.rates=self.write('rates.json',{})
        self.env=patch.dict(os.environ,{'PATH':str(self.bin)+os.pathsep+os.environ['PATH'],
            'OP_TEST_SCENARIO':str(self.scenario),'OP_TEST_LOG':str(self.log),
            'AWS_ACCESS_KEY_ID':'never-print-this','AWS_SECRET_ACCESS_KEY':'never-print-this',
            'AWS_SESSION_TOKEN':'never-print-this','AWS_ROLE_ARN':'unexpected','AWS_WEB_IDENTITY_TOKEN_FILE':'unexpected',
            'AWS_CONTAINER_CREDENTIALS_FULL_URI':'unexpected','AWS_DEFAULT_PROFILE':'unexpected',
            'AWS_CONFIG_FILE':'unexpected','AWS_SHARED_CREDENTIALS_FILE':'unexpected','PYTHONOPTIMIZE':'1',
            'TF_CLI_ARGS_plan':'-destroy','TF_VAR_project':'wrong','TF_DATA_DIR':'wrong','TF_WORKSPACE':'wrong','TF_LOG':'TRACE'})
        self.env.start();self.root_patch=patch.object(op,'ROOT',self.repo);self.root_patch.start()
        self.run_dir=self.base/'run'

    def tearDown(self):
        self.root_patch.stop();self.env.stop();self.tmp.cleanup()

    def write(self,name,value):
        target=self.base/name;target.write_text(json.dumps(value));target.chmod(0o600);return target

    def scenario_set(self,**settings): self.scenario.write_text(json.dumps(settings))

    def call(self,command='preflight',extra=None,directory=None):
        args=[command,'--run-directory',str(directory or self.run_dir),'--https-context',str(self.https),
              '--s3-backend-context',str(self.s3)]
        if command!='preflight':args+=['--rates-file',str(self.rates)]
        if command=='plan':args+=['--inputs',str(self.inputs)]
        args+=extra or []
        output=io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output): result=op.main(args)
        self.output=output.getvalue();return result

    def commands(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_preflight_logs_only_private_safe_commands(self):
        self.assertEqual(self.call(),0)
        self.assertEqual(stat.S_IMODE(self.run_dir.stat().st_mode),0o700)
        for path in self.run_dir.iterdir():self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
        transcript=(self.run_dir/'transcript.txt').read_text()
        self.assertNotIn('203.0.113.7',transcript);self.assertNotIn('never-print-this',transcript)
        for call in self.commands():
            self.assertFalse(call['forbiddenEnvPresent']);self.assertEqual(call['profile'],op.PROFILE)
        freetier=next(x for x in self.commands() if x['args'][:2]==['freetier','get-account-plan-state'])
        self.assertEqual(freetier['args'][freetier['args'].index('--region')+1],'us-east-1')
        self.assertEqual(json.loads((self.run_dir/'steps.json').read_text())['status'],'PREPARATION_COMPLETE_NOT_APPROVED')
        recorded = json.loads((self.run_dir/'steps.json').read_text())['steps']
        self.assertTrue(all(Path(step['workingDirectory']).is_absolute() for step in recorded))
        self.assertTrue(all(step['exitCode'] in step['expectedExitCodes'] for step in recorded))

    def test_wrong_account_stops_before_other_calls(self):
        self.scenario_set(account='000000000000');self.assertEqual(self.call(),1)
        self.assertEqual(len(self.commands()),1)

    def test_wrong_backend_stops_before_any_cli(self):
        self.backend['config']['key']='other/state';self.cache.write_text(json.dumps({'backend':self.backend}))
        self.assertEqual(self.call(),1);self.assertFalse(self.commands())

    def test_cached_profile_is_rejected(self):
        self.backend['config']['profile']='other';self.cache.write_text(json.dumps({'backend':self.backend}))
        self.assertEqual(self.call(),1);self.assertFalse(self.commands())

    def test_nondefault_workspace_stops(self):
        self.scenario_set(workspace='prod');self.assertEqual(self.call(),1)
        self.assertFalse(any(c['args'][:2]==['s3api','head-object'] for c in self.commands()))

    def test_denied_state_is_not_absent(self):
        self.scenario_set(state='denied');self.assertEqual(self.call(),1)
        self.assertIn('present or unreadable',self.output)

    def test_existing_state_stops_initial_plan(self):
        self.scenario_set(state='present');self.assertEqual(self.call('plan'),1)
        self.assertFalse(any(c['args'][0]=='plan' for c in self.commands()))

    def test_unissued_certificate_stops(self):
        self.scenario_set(cert='PENDING_VALIDATION');self.assertEqual(self.call(),1)

    def test_existing_named_cluster_stops(self):
        self.scenario_set(existing_cluster=True);self.assertEqual(self.call(),1)

    def test_existing_project_vpc_stops(self):
        self.scenario_set(vpcs=['vpc-existing']);self.assertEqual(self.call(),1)

    def test_wrong_client_is_not_broadened_or_echoed(self):
        self.scenario_set(ip='203.0.113.8');self.assertEqual(self.call(),1)
        self.assertIn('differs from the approved',self.output)
        self.assertNotIn('203.0.113.8',self.output)
        self.assertNotIn('203.0.113.8',(self.run_dir/'transcript.txt').read_text())

    def test_cleanup_inputs_stop_before_any_cli(self):
        self.inputs_value['teardown_discard_demo_data']=True;self.inputs.write_text(json.dumps(self.inputs_value))
        self.assertEqual(self.call('plan'),1);self.assertFalse(self.commands())

    def test_active_application_inputs_stop(self):
        self.inputs_value['deploy_application']=True;self.inputs.write_text(json.dumps(self.inputs_value))
        self.assertEqual(self.call('plan'),1);self.assertFalse(self.commands())

    def test_credentials_cannot_be_added_to_inputs(self):
        self.inputs_value['password']='never-print-this';self.inputs.write_text(json.dumps(self.inputs_value))
        self.assertEqual(self.call('plan'),1);self.assertNotIn('never-print-this',self.output)

    def test_expired_deadline_stops(self):
        self.inputs_value['expires_at']='2020-01-01T00:00:00Z';self.inputs.write_text(json.dumps(self.inputs_value))
        self.assertEqual(self.call('plan'),1);self.assertFalse(self.commands())

    def test_unpinned_image_stops(self):
        self.inputs_value['kafka_image']='apache/kafka:latest';self.inputs.write_text(json.dumps(self.inputs_value))
        self.assertEqual(self.call('plan'),1);self.assertFalse(self.commands())

    def test_public_transcript_path_is_rejected(self):
        self.assertEqual(self.call(directory=self.repo/'docs/transcript'),1);self.assertFalse(self.commands())

    def test_existing_run_is_never_overwritten(self):
        self.run_dir.mkdir();(self.run_dir/'keep').write_text('keep')
        self.assertEqual(self.call(),1);self.assertEqual((self.run_dir/'keep').read_text(),'keep')

    def test_symlink_run_is_rejected(self):
        other=self.base/'other';other.mkdir();self.run_dir.symlink_to(other,target_is_directory=True)
        self.assertEqual(self.call(),1);self.assertFalse(self.commands())

    def test_public_context_is_rejected(self):
        self.https.chmod(0o644);self.assertEqual(self.call(),1);self.assertFalse(self.commands())

    def test_plan_produces_private_artifact_and_strict_review(self):
        self.assertEqual(self.call('plan'),0)
        for name in ['application.tfplan','plan.json','inputs.tfvars.json','review.json','steps.json','transcript.txt']:
            self.assertEqual(stat.S_IMODE((self.run_dir/name).stat().st_mode),0o600)
        self.assertNotIn('not-for-transcript',(self.run_dir/'transcript.txt').read_text())
        pairs=[c['args'][:2] for c in self.commands()]
        self.assertFalse(any('apply' in p or 'destroy' in p or 'login' in p for p in pairs))
        self.assertEqual(json.loads((self.run_dir/'review.json').read_text())['planBinarySha256'],hashlib.sha256(b'fake-saved-plan').hexdigest())

    def test_failed_plan_does_not_continue_to_show_or_review(self):
        self.scenario_set(plan_fails=True);self.assertEqual(self.call('plan'),1)
        self.assertFalse(any(c['args'][:2]==['show','-json'] for c in self.commands()))
        self.assertFalse((self.run_dir/'review.json').exists())

    def test_wrong_review_hash_never_runs_cli(self):
        binary=self.base/'saved.tfplan';binary.write_bytes(b'plan');binary.chmod(0o600)
        plan_json=self.write('plan.json',{})
        self.assertEqual(self.call('review',['--plan-binary',str(binary),'--plan-json',str(plan_json),
                                           '--expected-sha256','0'*64]),1)
        self.assertFalse(self.commands())

    def test_wrong_reviewer_receipt_is_not_success(self):
        self.scenario_set(bad_review=True);self.assertEqual(self.call('plan'),1)
        self.assertEqual(json.loads((self.run_dir/'steps.json').read_text())['status'],'STOPPED_NO_APPLY')

    def test_numeric_boolean_context_is_rejected(self):
        bad=dict(op.BACKEND);bad['encrypt']=1;self.s3.write_text(json.dumps(bad))
        self.assertEqual(self.call(),1);self.assertFalse(self.commands())

    def test_failed_reviewer_never_claims_success(self):
        self.scenario_set(review_fails=True)
        self.assertEqual(self.call('plan'),1)
        self.assertEqual(json.loads((self.run_dir/'steps.json').read_text())['status'],'STOPPED_NO_APPLY')
        self.assertNotIn('PREPARATION_COMPLETE_NOT_APPROVED',self.output)

    def test_optimized_operator_refuses_before_any_command(self):
        script=Path(__file__).with_name('aws-ecs-operator.py')
        result=subprocess.run([sys.executable,'-O',str(script),'--help'],text=True,capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('refuses Python optimization',result.stderr)
        self.assertFalse(self.commands())

    def test_no_apply_destroy_or_login_subcommands(self):
        for command in ['apply','destroy','login']:
            with self.subTest(command=command),contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:op.main([command])
                self.assertEqual(error.exception.code,2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
