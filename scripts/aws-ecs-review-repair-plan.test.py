#!/usr/bin/env python3
"""Adversarial controls for the real mixed-action repair fixture; never AWS/apply."""
import argparse
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import shutil
import tempfile
from unittest.mock import patch
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('repair_reviewer',ROOT/'scripts/aws-ecs-review-repair-plan.py')
reviewer=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)
REAL_OUTPUT=subprocess.check_output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['plan-json','plan-binary','baseline-state','repair-context','https-context','s3-backend-context','rates-file','cost-proposal','cloudmap-instances','report']:
        parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args()
    values={key:value.resolve() for key,value in vars(args).items()}
    original=json.loads(values['plan_json'].read_text())
    baseline=reviewer.state_resources(json.loads(values['baseline_state'].read_text()))
    checks=[]
    def call(overrides=None):
        supplied={**values,**(overrides or {})}
        with contextlib.redirect_stdout(io.StringIO()):
            return reviewer.review(supplied['plan_json'],supplied['plan_binary'],supplied['baseline_state'],supplied['repair_context'],supplied['https_context'],supplied['s3_backend_context'],supplied['rates_file'],supplied['cost_proposal'],supplied['cloudmap_instances'],supplied['report'])
    def resource(plan,address):return next(r for r in plan['resource_changes'] if r['address']==address)
    def expect(name,operation,message=None):
        try:operation()
        except AssertionError as error:
            if message:assert message in str(error),(name,str(error))
        else:raise AssertionError('Repair reviewer accepted negative control: '+name)
        checks.append({'name':name,'status':'PASS'})
    with tempfile.TemporaryDirectory(prefix='repair-review-controls-') as temporary:
        folder=Path(temporary);report=folder/'review.json'
        # Prevent an always-rejecting implementation from passing its negatives.
        accepted=call({'report':report})
        assert accepted['status']=='PARTIAL_APPLY_REPAIR_PLAN_REVIEWED_NOT_APPROVED'
        def mutation(name,mutate,message=None,stub=True):
            plan=copy.deepcopy(original);mutate(plan)
            fixture=folder/'mutated-plan.json';fixture.write_text(json.dumps(plan));fixture.chmod(0o600)
            def output(command,*pos,**kw):
                if stub and command[:3]==['terraform','show','-json']:return json.dumps(plan)
                return REAL_OUTPUT(command,*pos,**kw)
            with patch.object(reviewer.subprocess,'check_output',output):
                expect(name,lambda:call({'plan_json':fixture,'report':report}),message)
        mutation('reject_json_not_bound_to_actual_binary',lambda p:p['variables']['region'].update(value='us-east-1'),'does not match actual saved binary',False)
        mutation('reject_wrong_output_account',lambda p:p['planned_values']['outputs']['deployment_account_id'].update(value='000000000000'),'Wrong deployment identity')
        mutation('reject_extended_clock_input',lambda p:p['variables']['expires_at'].update(value='2026-10-31T21:51:25Z'),'original shutdown deadline')
        mutation('reject_zero_backup_input',lambda p:p['variables']['rds_backup_retention_days'].update(value=0),'backup/discard/protection')
        mutation('reject_discard_mode_input',lambda p:p['variables']['teardown_discard_demo_data'].update(value=True),'backup/discard/protection')
        mutation('reject_application_activation',lambda p:p['variables']['deploy_application'].update(value=True),'activation is outside')
        mutation('reject_broker_replacement',lambda p:resource(p,'aws_instance.broker')['change'].update(actions=['delete','create']),'Unexpected deletion or replacement')
        mutation('reject_unreviewed_deletion',lambda p:resource(p,'aws_ecs_cluster.dev')['change'].update(actions=['delete']),'Unexpected deletion or replacement')
        mutation('reject_create_before_delete_alb',lambda p:resource(p,'aws_lb.dev')['change'].update(actions=['create','delete']),'delete-before-create ALB')
        mutation('reject_untaint_shortcut',lambda p:resource(p,'aws_lb.dev')['change'].update(actions=['no-op']),'delete-before-create ALB')
        mutation('reject_cloudmap_create_before_delete',lambda p:resource(p,'aws_service_discovery_service.app["frontend"]')['change'].update(actions=['create','delete']),'delete-before-create empty discovery')
        mutation('reject_extra_replacement_path',lambda p:resource(p,'aws_service_discovery_service.app["frontend"]')['change'].update(replace_paths=[['dns_config']]),'discovery replacement path')
        mutation('reject_changed_cloudmap_name',lambda p:resource(p,'aws_service_discovery_service.app["frontend"]')['change']['after'].update(name='other'),'beyond custom health')
        mutation('reject_changed_cloudmap_health_threshold',lambda p:resource(p,'aws_service_discovery_service.app["frontend"]')['change']['after'].update(health_check_custom_config=[{'failure_threshold':2}]),'custom health transition')
        mutation('reject_broker_type_update',lambda p:resource(p,'aws_instance.broker')['change']['after'].update(instance_type='m7i-flex.xlarge'),'nonmetadata update')
        mutation('reject_changed_existing_identity',lambda p:resource(p,'aws_instance.broker')['change']['after'].update(id='i-unreviewed'),'Existing resource identity')
        mutation('reject_changed_embedded_before_projection',lambda p:resource(p,'aws_instance.broker')['change']['before'].update(instance_type='m7i-flex.xlarge'),'before values differ')
        mutation('reject_tag_deadline_reset',lambda p:resource(p,'aws_instance.broker')['change']['after']['tags_all'].update(ExpiresAt='2026-10-31T21:51:25Z'),'Expiry tag resets')
        mutation('reject_empty_new_resource_as_noop',lambda p:resource(p,'aws_db_instance.dev')['change'].update(actions=['no-op']),'must be create-only')
        mutation('reject_extra_resource',lambda p:p['resource_changes'].append({**copy.deepcopy(resource(p,'aws_ecs_cluster.dev')),'address':'aws_ecs_cluster.unreviewed'}),'resource address')
        mutation('reject_missing_final_resource',lambda p:p['resource_changes'].remove(resource(p,'aws_vpc.dev')),'resource count')
        mutation('reject_public_new_database',lambda p:resource(p,'aws_db_instance.dev')['change']['after'].update(publicly_accessible=True))
        mutation('reject_zero_new_database_backups',lambda p:resource(p,'aws_db_instance.dev')['change']['after'].update(backup_retention_period=0),'one-day RDS backups')
        mutation('reject_rds_protection_removed',lambda p:resource(p,'aws_db_instance.dev')['change']['after'].update(deletion_protection=False))
        mutation('reject_broker_discovery_wrong_peer',lambda p:resource(p,'aws_service_discovery_instance.broker')['change']['after']['attributes'].update(AWS_INSTANCE_IPV4='10.85.9.9'),'discovery identity/peer')
        mutation('reject_broker_discovery_wrong_port',lambda p:resource(p,'aws_service_discovery_instance.broker')['change']['after']['attributes'].update(AWS_INSTANCE_PORT='9092'),'discovery identity/peer')
        mutation('reject_broker_discovery_other_service',lambda p:resource(p,'aws_service_discovery_instance.broker')['change']['after'].update(service_id='srv-unreviewed'),'reference its new service')
        mutation('reject_wrong_certificate',lambda p:resource(p,'aws_lb_listener.https[0]')['change']['after'].update(certificate_arn='arn:aws:acm:us-east-2:772641336063:certificate/unreviewed'),'Unreviewed listener certificate')
        def bad_policy(plan):
            r=resource(plan,'aws_s3_bucket_policy.operations')['change']['after'];policy=json.loads(r['policy'])
            policy['Statement'][1]['Condition']['ArnLike']['aws:SourceArn']='*';r['policy']=json.dumps(policy)
        mutation('reject_broad_alb_logging_policy',bad_policy,'Unreviewed ALB logging bucket policy')
        # Direct final-topology probes retain genuine mixed actions. These reach
        # graph checks without weakening the real embedded-before binding.
        topology_controls=[
            ('reject_world_https','aws_vpc_security_group_ingress_rule.https['+json.dumps(json.loads(values['https_context'].read_text())['approvedClientCidrs'][0])+']','cidr_ipv4','0.0.0.0/0'),
            ('reject_db_wrong_sg','aws_vpc_security_group_ingress_rule.database["identity"]','referenced_security_group_id','sg-unreviewed'),
            ('reject_public_broker','aws_instance.broker','associate_public_ip_address',True),
            ('reject_ssh_port','aws_vpc_security_group_ingress_rule.frontend','from_port',22),
            ('reject_weaker_listener_tls','aws_lb_listener.https[0]','ssl_policy','ELBSecurityPolicy-2016-08'),
        ]
        https=json.loads(values['https_context'].read_text())
        for name,address,key,bad in topology_controls:
            plan=copy.deepcopy(original);resource(plan,address)['change']['after'][key]=bad
            expect(name,lambda p=plan:reviewer.validate_topology(p,https))
        plan=copy.deepcopy(original)
        resource(plan,'aws_security_group.alb')['change']['after']['ingress'].append({'cidr_blocks':['0.0.0.0/0'],'description':'','from_port':22,'ipv6_cidr_blocks':[],'prefix_list_ids':[],'protocol':'tcp','security_groups':[],'self':False,'to_port':22})
        expect('reject_extra_computed_sg_mirror_atom',lambda:reviewer.validate_topology(plan,https),'Computed SG mirrors differ')
        plan=copy.deepcopy(original)
        next(r for r in plan['configuration']['root_module']['resources'] if r['address']=='aws_security_group.alb')['expressions']['ingress']={'constant_value':[]}
        expect('reject_configured_inline_sg_even_when_empty',lambda:reviewer.validate_topology(plan,https),'Configured inline SG')
        mutation('reject_missing_explicit_volume_expiry',lambda p:resource(p,'aws_instance.broker')['change']['after']['root_block_device'][0].update(tags={}), 'Explicit canonical root-volume expiry')
        mutation('reject_changed_computed_volume_ownership',lambda p:resource(p,'aws_instance.broker')['change']['after']['root_block_device'][0]['tags_all'].update(Owner='unreviewed'),'nonmetadata update')
        for name,key,bad in [
            ('reject_wrong_repair_account','account','000000000000'),
            ('reject_wrong_consumed_approval','approvedPlanSha256','0'*64),
            ('reject_wrong_baseline_context','baselineStateSha256','0'*64),
            ('reject_changed_context_deadline','shutdownDeadlineUtc','2026-10-31T21:51:25Z'),
        ]:
            context=json.loads(values['repair_context'].read_text());context[key]=bad
            fixture=folder/(name+'.json');fixture.write_text(json.dumps(context));fixture.chmod(0o600)
            expect(name,lambda f=fixture:call({'repair_context':f,'report':report}),'Unreviewed repair context')
        altered_state=folder/'state.json';state=json.loads(values['baseline_state'].read_text());state['serial']=5
        altered_state.write_text(json.dumps(state));altered_state.chmod(0o600)
        expect('reject_changed_baseline_file',lambda:call({'baseline_file':altered_state,'baseline_state':altered_state,'report':report}),'baseline state hash differs')
        cm=json.loads(values['cloudmap_instances'].read_text());cm['instancesByServiceId'][next(iter(cm['instancesByServiceId']))]=[{'Id':'active'}]
        fixture=folder/'nonempty-cloudmap.json';fixture.write_text(json.dumps(cm));fixture.chmod(0o600)
        context=json.loads(values['repair_context'].read_text());context['cloudMapInstancesSha256']=reviewer.sha(fixture)
        context_file=folder/'nonempty-context.json';context_file.write_text(json.dumps(context));context_file.chmod(0o600)
        expect('reject_nonempty_discovery_replacement',lambda:call({'cloudmap_instances':fixture,'repair_context':context_file,'report':report}),'empty discovery definitions')
        cost=json.loads(values['cost_proposal'].read_text());cost['costCases'][0]['total_usd']='0'
        fixture=folder/'wrong-cost.json';fixture.write_text(json.dumps(cost));fixture.chmod(0o600)
        expect('reject_undercosted_proposal',lambda:call({'cost_proposal':fixture,'report':report}),'cost total differs')
        with ZipFile(values['plan_binary']) as saved:members={name:saved.read(name) for name in saved.namelist()}
        shutil.copyfile(values['plan_binary'].parent/'kafka-user-data.sh.tftpl',folder/'kafka-user-data.sh.tftpl')
        for name,field,bad in [
            ('reject_refreshed_broker_ami','ami','ami-unreviewed'),
            ('reject_refreshed_volume_identity','volume_id','vol-unreviewed'),
            ('reject_refreshed_volume_encryption','encrypted',False),
            ('reject_refreshed_volume_deletion_flag','delete_on_termination',False),
            ('reject_refreshed_broker_profile','iam_instance_profile','unreviewed-profile'),
        ]:
            prior=json.loads(members['tfstate'])
            frozen=next(r['instances'][0]['attributes'] for r in prior['resources'] if r['type']=='aws_instance' and r['name']=='broker')
            plan=copy.deepcopy(original)
            broker=resource(plan,'aws_instance.broker')['change']
            if field in ['ami','iam_instance_profile']:
                frozen[field]=bad;broker['before'][field]=bad;broker['after'][field]=bad
            else:
                frozen['root_block_device'][0][field]=bad
                broker['before']['root_block_device'][0][field]=bad
                broker['after']['root_block_device'][0][field]=bad
            binary=folder/(name+'.tfplan')
            with ZipFile(binary,'w') as target:
                for key,data in members.items():target.writestr(key,json.dumps(prior).encode() if key=='tfstate' else data)
            binary.chmod(0o600)
            fixture=folder/'embedded-mutant-plan.json';fixture.write_text(json.dumps(plan));fixture.chmod(0o600)
            def output(command,*pos,**kw):
                if command[:3]==['terraform','show','-json']:return json.dumps(plan)
                return REAL_OUTPUT(command,*pos,**kw)
            with patch.object(reviewer.subprocess,'check_output',output):
                expect(name,lambda b=binary:call({'plan_binary':b,'plan_json':fixture,'report':report}),'Frozen broker')
        for name,member,content,message in [
            ('reject_saved_source_tamper','tfconfig/m-/versions.tf',b'terraform {}','repair source differs'),
            ('reject_saved_extra_source','tfconfig/m-/bad.tf',b'','Extra source'),
            ('reject_saved_lock_tamper','.terraform.lock.hcl',b'','Provider lock differs'),
        ]:
            binary=folder/(name+'.tfplan')
            with ZipFile(binary,'w') as target:
                for key,data in members.items():target.writestr(key,content if key==member else data)
                if member not in members:target.writestr(member,content)
            binary.chmod(0o600)
            expect(name,lambda b=binary:call({'plan_binary':b,'report':report}),message)
        # Mutate actual saved backend bytes, not only a mutable init cache.
        def varint(value):
            result=bytearray()
            while value>127:result.append((value&127)|128);value>>=7
            result.append(value);return bytes(result)
        def protobuf(fields):
            result=bytearray()
            for number,wire,value in fields:
                result.extend(varint((number<<3)|wire))
                if wire==0:result.extend(varint(value))
                elif wire==2:result.extend(varint(len(value)));result.extend(value)
                else:result.extend(value)
            return bytes(result)
        fields=reviewer.initial._protobuf_fields(members['tfplan'])
        backend=reviewer.initial._protobuf_fields(reviewer.initial._one_field(fields,13,2))
        wrong_backend=protobuf([(number,wire,b'local' if number==1 else value) for number,wire,value in backend])
        changed=protobuf([(number,wire,wrong_backend if number==13 else value) for number,wire,value in fields])
        binary=folder/'wrong-backend.tfplan'
        with ZipFile(binary,'w') as target:
            for key,data in members.items():target.writestr(key,changed if key=='tfplan' else data)
        binary.chmod(0o600)
        expect('reject_saved_local_backend',lambda:call({'plan_binary':binary,'report':report}),'Actual saved backend must be S3')
        public_fixture=folder/'public-plan.json';public_fixture.write_text(values['plan_json'].read_text());public_fixture.chmod(0o644)
        expect('reject_public_repair_input',lambda:call({'plan_json':public_fixture,'report':report}),'owner-only')
        optimized=subprocess.run(['python3','-O',str(ROOT/'scripts/aws-ecs-review-repair-plan.py'),'--help'],capture_output=True,text=True)
        assert optimized.returncode!=0 and 'refuses Python optimization' in optimized.stderr
        checks.append({'name':'reject_python_optimization','status':'PASS'})
    result={'passed':len(checks),'failed':0,'validMixedActionFixtureAccepted':True,
            'fixtureScope':'Real saved repair fixture; JSON mutation probes stub only terraform show, source/backend bytes remain bound. Direct topology probes retain real mixed actions. No AWS/apply.', 'checks':checks}
    values['report'].parent.mkdir(parents=True,exist_ok=True)
    values['report'].write_text(json.dumps(result,indent=2)+'\n');values['report'].chmod(0o600)
    print(str(len(checks))+' repair negative controls passed after accepted real mixed-action fixture')


if __name__=='__main__':main()
