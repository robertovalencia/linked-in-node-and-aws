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
    checks = []
    with tempfile.TemporaryDirectory(prefix='ecs-plan-review-') as tmp:
        fixture, report = Path(tmp)/'mutated.json', Path(tmp)/'report.json'
        for name, kind, key, bad, expected, stub in controls:
            plan = copy.deepcopy(original)
            resource(plan, kind)[key] = bad
            fixture.write_text(json.dumps(plan))
            def output(command, *pos, **kw):
                if command[:3] == ['terraform','show','-json'] and stub:
                    return json.dumps(plan)
                return real_output(command, *pos, **kw)
            try:
                with patch.object(reviewer.subprocess, 'check_output', output), contextlib.redirect_stdout(io.StringIO()):
                    reviewer.review(fixture, args.plan_binary.resolve(), report)
            except AssertionError as error:
                if name == 'public_database':
                    assert 'does not match saved binary' in str(error), str(error)
                elif expected:
                    assert expected in str(error), (name, str(error))
            else:
                raise AssertionError('Reviewer accepted negative control: '+name)
            checks.append({'name':name,'status':'PASS'})
        result = subprocess.run(['python3','-O',str(ROOT/'scripts/aws-ecs-review-plan.py'),'--help'], capture_output=True,text=True)
        assert result.returncode != 0 and 'refuses Python optimization' in result.stderr
        checks.append({'name':'reject_optimized_python_validation_bypass','status':'PASS'})
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({'passed':len(checks),'failed':0,'fixtureScope':'Private saved-plan fixture; rule mutations stub only terraform show, never AWS','checks':checks},indent=2)+'\n')
    print(f'{len(checks)} negative controls passed')

if __name__ == '__main__':
    main()
