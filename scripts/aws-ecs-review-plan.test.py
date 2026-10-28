#!/usr/bin/env python3
"""Negative controls for the offline reviewer, using an ignored private plan fixture.

Only `terraform show` is stubbed for rule-mutation controls; source ZIP checks stay
real. A separate control deliberately leaves show real to detect mismatched JSON.
No AWS API, provisioning or plan mutation occurs.
"""
import argparse
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reviewer', ROOT/'scripts/aws-ecs-review-plan.py')
reviewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewer)
real_output = subprocess.check_output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan-json', required=True, type=Path)
    parser.add_argument('--plan-binary', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--https-context', type=Path)
    args = parser.parse_args()
    original = json.loads(args.plan_json.read_text())
    def resource(plan, kind):
        return next(r['change']['after'] for r in plan['resource_changes'] if r['type'] == kind)
    controls = [
        ('public_database', 'aws_db_instance', 'publicly_accessible', True, 'source-bound JSON mismatch', False),
        ('public_broker', 'aws_instance', 'associate_public_ip_address', True, '', True),
        ('unprotected_database', 'aws_db_instance', 'deletion_protection', False, '', True),
        ('unencrypted_database', 'aws_db_instance', 'storage_encrypted', False, '', True),
        ('inline_public_ssh', 'aws_security_group', 'ingress', [{'from_port':22,'to_port':22,'protocol':'tcp','cidr_blocks':['0.0.0.0/0']}], 'Inline security-group', True),
        ('inline_wide_egress', 'aws_security_group', 'egress', [{'from_port':0,'to_port':0,'protocol':'-1','cidr_blocks':['0.0.0.0/0']}], 'Inline security-group', True),
        ('unknown_sg_reference_ssh', 'aws_vpc_security_group_ingress_rule', 'from_port', 22, 'Unexpected ingress', True),
        ('public_cidr_ingress', 'aws_vpc_security_group_ingress_rule', 'cidr_ipv4', '0.0.0.0/0', 'no CIDR', True),
        ('wide_ingress_protocol', 'aws_vpc_security_group_ingress_rule', 'ip_protocol', '-1', 'Unexpected ingress', True),
    ]
    if args.https_context:
        controls = [(name,kind,key,bad,'Unapproved HTTPS' if name == 'public_cidr_ingress' else expected,stub) for name,kind,key,bad,expected,stub in controls]
        wrong_condition = copy.deepcopy(resource(original,'aws_lb_listener_rule')['condition'])
        wrong_condition[0]['host_header'][0]['values'] = ['unapproved.example.invalid']
        wrong_default = copy.deepcopy(resource(original,'aws_lb_listener')['default_action'])
        wrong_default[0]['fixed_response'][0]['status_code'] = '200'
        controls += [
            ('reject_http_listener','aws_lb_listener','protocol','HTTP','Only HTTPS443',True),
            ('reject_other_listener_port','aws_lb_listener','port',80,'Only HTTPS443',True),
            ('reject_other_certificate','aws_lb_listener','certificate_arn','arn:aws:acm:us-east-2:772641336063:certificate/00000000-0000-0000-0000-000000000000','Unreviewed listener certificate',True),
            ('reject_weaker_tls_policy','aws_lb_listener','ssl_policy','ELBSecurityPolicy-2016-08','Unreviewed TLS policy',True),
            ('reject_other_hostname','aws_lb_listener_rule','condition',wrong_condition,'Unreviewed host-header',True),
            ('reject_default_success','aws_lb_listener','default_action',wrong_default,'Default hostname rejection',True),
        ]
    checks = []
    with tempfile.TemporaryDirectory(prefix='ecs-plan-review-') as tmp:
        fixture, report = Path(tmp)/'mutated.json', Path(tmp)/'report.json'
        with contextlib.redirect_stdout(io.StringIO()):
            reviewer.review(args.plan_json.resolve(),args.plan_binary.resolve(),report,args.https_context.resolve() if args.https_context else None)

        for name, kind, key, bad, expected, stub in controls:
            plan = copy.deepcopy(original)
            resource(plan, kind)[key] = bad
            fixture.write_text(json.dumps(plan)); fixture.chmod(0o600)
            def output(command, *pos, **kw):
                if command[:3] == ['terraform','show','-json'] and stub:
                    return json.dumps(plan)
                return real_output(command, *pos, **kw)
            try:
                with patch.object(reviewer.subprocess, 'check_output', output), contextlib.redirect_stdout(io.StringIO()):
                    reviewer.review(fixture, args.plan_binary.resolve(), report,args.https_context.resolve() if args.https_context else None)
            except AssertionError as error:
                if name == 'public_database':
                    assert 'does not match saved binary' in str(error), str(error)
                elif expected:
                    assert expected in str(error), (name, str(error))
            else:
                raise AssertionError('Reviewer accepted negative control: '+name)
            checks.append({'name':name,'status':'PASS'})
        if args.https_context:
            graph_controls = [
                ('reject_https_wrong_owner_sg','aws_vpc_security_group_ingress_rule','https','security_group_id','sg-unapproved'),
                ('reject_db_wrong_source_sg','aws_vpc_security_group_ingress_rule','database','referenced_security_group_id','sg-unapproved'),
                ('reject_forward_wrong_target','aws_lb_listener_rule','application','action',None),
                ('reject_listener_wrong_alb','aws_lb_listener','https','load_balancer_arn','arn:aws:elasticloadbalancing:us-east-2:772641336063:loadbalancer/app/unapproved/0000000000000000'),
                ('reject_rule_wrong_listener','aws_lb_listener_rule','application','listener_arn','arn:aws:elasticloadbalancing:us-east-2:772641336063:listener/app/unapproved/0000000000000000/0000000000000000'),
            ]
            for name,kind,resource_name,field,bad in graph_controls:
                plan = copy.deepcopy(original)
                item = next(r for r in plan['resource_changes'] if r['type']==kind and r['name']==resource_name)
                if name == 'reject_forward_wrong_target':
                    item['change']['after']['action'][0]['target_group_arn'] = 'arn:aws:elasticloadbalancing:us-east-2:772641336063:targetgroup/unapproved/0000000000000000'
                    expected_error = 'Unreviewed frontend target group'
                else:
                    item['change']['after'][field] = bad
                    expected_error = 'Unreviewed HTTPS routing owner' if kind in ['aws_lb_listener','aws_lb_listener_rule'] else 'Unreviewed SG owner/peer'
                fixture.write_text(json.dumps(plan)); fixture.chmod(0o600)
                with patch.object(reviewer.subprocess, 'check_output', output), contextlib.redirect_stdout(io.StringIO()):
                    try:
                        reviewer.review(fixture,args.plan_binary.resolve(),report,args.https_context.resolve())
                    except AssertionError as error:
                        assert expected_error in str(error),(name,str(error))
                    else:
                        raise AssertionError('Reviewer accepted graph mutation: '+name)
                checks.append({'name':name,'status':'PASS'})
            plan = copy.deepcopy(original)
            cidr_rule = next(r for r in plan['resource_changes'] if r['type']=='aws_vpc_security_group_ingress_rule' and r['change']['after'].get('cidr_ipv4'))
            cidr_rule['change']['after']['from_port'] = 22
            cidr_rule['change']['after']['to_port'] = 22
            fixture.write_text(json.dumps(plan)); fixture.chmod(0o600)
            with patch.object(reviewer.subprocess, 'check_output', output), contextlib.redirect_stdout(io.StringIO()):
                try:
                    reviewer.review(fixture,args.plan_binary.resolve(),report,args.https_context.resolve())
                except AssertionError as error:
                    assert 'CIDR ingress must be HTTPS443 only' in str(error), str(error)
                else:
                    raise AssertionError('Approved /32 permitted SSH')
            checks.append({'name':'approved_cidr_cannot_open_ssh','status':'PASS'})
        fixture.write_text(json.dumps(original)); fixture.chmod(0o644)
        try:
            reviewer.review(fixture,args.plan_binary.resolve(),report,args.https_context.resolve() if args.https_context else None)
        except AssertionError as error:
            assert 'owner-only' in str(error),str(error)
        else:
            raise AssertionError('Publicly readable plan JSON accepted')
        checks.append({'name':'reject_non_private_plan_input','status':'PASS'})
        result = subprocess.run(['python3','-O',str(ROOT/'scripts/aws-ecs-review-plan.py'),'--help'], capture_output=True,text=True)
        assert result.returncode != 0 and 'refuses Python optimization' in result.stderr
        checks.append({'name':'reject_optimized_python_validation_bypass','status':'PASS'})
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({'passed':len(checks),'failed':0,'validFixtureAccepted':True,'fixtureScope':'Private saved-plan fixture; rule mutations stub only terraform show, never AWS','checks':checks},indent=2)+'\n')
    print(f'{len(checks)} negative controls passed')

if __name__ == '__main__':
    main()
