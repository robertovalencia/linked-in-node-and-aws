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
from zipfile import ZipFile
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
    parser.add_argument('--s3-backend-context', type=Path)
    args = parser.parse_args()
    original = json.loads(args.plan_json.read_text())
    def review_fixture(*pos):
        return reviewer.review(*pos,s3_backend_context=args.s3_backend_context.resolve() if args.s3_backend_context else None)
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
            review_fixture(args.plan_json.resolve(),args.plan_binary.resolve(),report,args.https_context.resolve() if args.https_context else None)

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
                    review_fixture(fixture, args.plan_binary.resolve(), report,args.https_context.resolve() if args.https_context else None)
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
                        review_fixture(fixture,args.plan_binary.resolve(),report,args.https_context.resolve())
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
                    review_fixture(fixture,args.plan_binary.resolve(),report,args.https_context.resolve())
                except AssertionError as error:
                    assert 'CIDR ingress must be HTTPS443 only' in str(error), str(error)
                else:
                    raise AssertionError('Approved /32 permitted SSH')
            checks.append({'name':'approved_cidr_cannot_open_ssh','status':'PASS'})
        if args.s3_backend_context:
            # Mutate actual saved tfplan backend bytes while retaining source ZIP.
            # This proves rejection is independent of mutable init-cache metadata
            # and of terraform-show JSON (which never exposes the backend).
            def varint(number):
                result = bytearray()
                while number >= 128:
                    result.append((number & 127) | 128)
                    number >>= 7
                result.append(number)
                return bytes(result)
            def protobuf(fields):
                result = bytearray()
                for number, wire, value in fields:
                    result.extend(varint((number << 3) | wire))
                    if wire == 0: result.extend(varint(value))
                    elif wire == 2: result.extend(varint(len(value))); result.extend(value)
                    else: result.extend(value)
                return bytes(result)
            def msgpack(value):
                if value is None: return b'\xc0'
                if value is False: return b'\xc2'
                if value is True: return b'\xc3'
                if isinstance(value, str):
                    text = value.encode()
                    return (bytes([160 + len(text)]) if len(text)<32 else b'\xda'+len(text).to_bytes(2,'big'))+text
                if isinstance(value, list):
                    return (bytes([144+len(value)]) if len(value)<16 else b'\xdc'+len(value).to_bytes(2,'big'))+b''.join(msgpack(x) for x in value)
                if isinstance(value, dict):
                    return (bytes([128+len(value)]) if len(value)<16 else b'\xde'+len(value).to_bytes(2,'big'))+b''.join(msgpack(k)+msgpack(v) for k,v in value.items())
                if isinstance(value, int) and 0<=value<128: return bytes([value])
                raise AssertionError('Unsupported test MessagePack value')
            with ZipFile(args.plan_binary) as saved:
                members = {name:saved.read(name) for name in saved.namelist()}
            original_fields = reviewer._protobuf_fields(members['tfplan'])
            backend = reviewer._protobuf_fields(reviewer._one_field(original_fields,13,2))
            dynamic = reviewer._protobuf_fields(reviewer._one_field(backend,2,2))
            original_config = reviewer._msgpack_value(reviewer._one_field(dynamic,1,2))
            backend_controls = [
                ('reject_saved_wrong_bucket','bucket','another-state-bucket'),
                ('reject_saved_legacy_ec2_key','key','linked-in-node/dev/terraform.tfstate'),
                ('reject_saved_wrong_region','region','us-east-1'),
                ('reject_saved_unencrypted_state','encrypt',False),
                ('reject_saved_unlocked_state','use_lockfile',False),
                ('reject_saved_missing_account_allowlist','allowed_account_ids',None),
                ('reject_saved_wrong_account_allowlist','allowed_account_ids',['000000000000']),
                ('reject_saved_other_workspace_prefix','workspace_key_prefix','env:'),
                ('reject_saved_static_credentials','access_key','AKIA_FAKE_TEST_ONLY'),
                ('reject_saved_profile_override','profile','another-account'),
                ('reject_saved_endpoint_override','endpoint','https://example.invalid'),
                ('reject_saved_skip_account_lookup','skip_requesting_account_id',True),
                ('reject_saved_alternate_locking','dynamodb_table','unreviewed-lock-table'),
            ]
            for name,key,bad in backend_controls:
                config = copy.deepcopy(original_config)
                config[key] = bad
                changed_backend = [(1,2,b's3'),(2,2,protobuf([(1,2,msgpack(config))])),(3,2,b'default')]
                fields = [(n,w,protobuf(changed_backend) if n==13 else v) for n,w,v in original_fields]
                altered = Path(tmp)/(name+'.tfplan')
                with ZipFile(altered,'w') as output_zip:
                    for member,data in members.items(): output_zip.writestr(member,protobuf(fields) if member=='tfplan' else data)
                altered.chmod(0o600)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        review_fixture(args.plan_json.resolve(),altered,report,args.https_context.resolve())
                except AssertionError as error:
                    assert 'Unreviewed saved S3 backend' in str(error),(name,str(error))
                else:
                    raise AssertionError('Reviewer accepted saved backend mutation: '+name)
                checks.append({'name':name,'status':'PASS'})
            structural_controls = [
                ('reject_saved_local_backend',13,protobuf([(1,2,b'local'),(2,2,protobuf([(1,2,msgpack(original_config))])),(3,2,b'default')]),'Actual saved backend must be S3'),
                ('reject_saved_other_workspace',13,protobuf([(1,2,b's3'),(2,2,protobuf([(1,2,msgpack(original_config))])),(3,2,b'other')]),'Actual saved S3 workspace must be default'),
                ('reject_unsupported_plan_producer',14,b'1.18.0','Unsupported Terraform saved-backend producer'),
                ('reject_unknown_backend_value',13,protobuf([(1,2,b's3'),(2,2,protobuf([(1,2,b'\xc1')])),(3,2,b'default')]),'Unsupported saved backend MessagePack'),
                ('reject_trailing_backend_value',13,protobuf([(1,2,b's3'),(2,2,protobuf([(1,2,msgpack(original_config)+b'\xc0')])),(3,2,b'default')]),'Trailing saved backend MessagePack'),
                ('reject_duplicate_backend_map_key',13,protobuf([(1,2,b's3'),(2,2,protobuf([(1,2,b'\x82'+msgpack('key')+msgpack('one')+msgpack('key')+msgpack('two'))])),(3,2,b'default')]),'Duplicate or invalid saved backend config key'),
                ('reject_duplicate_backend_message',None,None,'Missing, duplicate or invalid saved backend field'),
                ('reject_unknown_state_store',29,b'not-reviewed','Unreviewed Terraform state_store'),
                ('reject_partial_saved_plan',26,0,'Saved S3 plan must be complete and applyable'),
                ('reject_unapplyable_saved_plan',25,0,'Saved S3 plan must be complete and applyable'),
                ('reject_errored_saved_plan',20,1,'Saved S3 plan must be normal and not errored'),
                ('reject_targeted_saved_plan',5,b'aws_instance.kafka','Targeted or forced saved S3 plans require separate review'),
            ]
            for name,number,bad,expected_error in structural_controls:
                fields = [(n,w,bad if n==number else v) for n,w,v in original_fields]
                if number is None: fields.append((13,2,reviewer._one_field(original_fields,13,2)))
                if number in (5,20,29) and not any(n==number for n,_,_ in original_fields): fields.append((number,0 if number==20 else 2,bad))
                altered = Path(tmp)/(name+'.tfplan')
                with ZipFile(altered,'w') as output_zip:
                    for member,data in members.items(): output_zip.writestr(member,protobuf(fields) if member=='tfplan' else data)
                altered.chmod(0o600)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        review_fixture(args.plan_json.resolve(),altered,report,args.https_context.resolve())
                except AssertionError as error:
                    assert expected_error in str(error),(name,str(error))
                else:
                    raise AssertionError('Reviewer accepted saved backend structural mutation: '+name)
                checks.append({'name':name,'status':'PASS'})
            for name,member,data,expected_error in [
                ('reject_saved_backend_override','tfconfig/m-/backend_override.tf',b'terraform { backend "local" {} }','Actual S3 plan must have no backend override'),
                ('reject_saved_source_tamper','tfconfig/m-/versions.tf',b'terraform { backend "local" {} }','Saved plan source differs'),
                ('reject_extra_json_configuration','tfconfig/m-/unreviewed.tf.json',b'{}','Actual S3 plan must have no backend override'),
                ('reject_nested_module_configuration','tfconfig/m-child/main.tf',b'','Actual S3 plan must have no backend override'),
                ('reject_unreviewed_module_manifest','tfconfig/modules.json',b'[]','Unreviewed saved Terraform modules'),
                ('reject_saved_provider_lock_tamper','.terraform.lock.hcl',b'','Saved provider lock differs'),
            ]:
                altered = Path(tmp)/(name+'.tfplan')
                with ZipFile(altered,'w') as output_zip:
                    for original_member,original_data in members.items():
                        if original_member!=member: output_zip.writestr(original_member,original_data)
                    output_zip.writestr(member,data)
                altered.chmod(0o600)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        review_fixture(args.plan_json.resolve(),altered,report,args.https_context.resolve())
                except AssertionError as error:
                    assert expected_error in str(error),(name,str(error))
                else:
                    raise AssertionError('Reviewer accepted source mutation: '+name)
                checks.append({'name':name,'status':'PASS'})
        fixture.write_text(json.dumps(original)); fixture.chmod(0o644)
        try:
            review_fixture(fixture,args.plan_binary.resolve(),report,args.https_context.resolve() if args.https_context else None)
        except AssertionError as error:
            assert 'owner-only' in str(error),str(error)
        else:
            raise AssertionError('Publicly readable plan JSON accepted')
        checks.append({'name':'reject_non_private_plan_input','status':'PASS'})
        result = subprocess.run(['python3','-O',str(ROOT/'scripts/aws-ecs-review-plan.py'),'--help'], capture_output=True,text=True)
        assert result.returncode != 0 and 'refuses Python optimization' in result.stderr
        checks.append({'name':'reject_optimized_python_validation_bypass','status':'PASS'})
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({'passed':len(checks),'failed':0,'validFixtureAccepted':True,'fixtureScope':'Private saved-plan fixture; rule mutations stub only terraform show, backend controls mutate actual saved bytes; never AWS','checks':checks},indent=2)+'\n')
    args.report.chmod(0o600)
    print(f'{len(checks)} negative controls passed')

if __name__ == '__main__':
    main()
