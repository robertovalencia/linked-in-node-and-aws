#!/usr/bin/env python3
"""Read-only saved-plan checks and deterministic cost ledger. Never calls AWS/apply."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D
import hashlib
import importlib.util
import ipaddress
import json
import os
import stat
from pathlib import Path
import subprocess
from zipfile import ZipFile

if not __debug__:
    raise SystemExit("Plan review refuses Python optimization because validation checks must run")

ROOT = Path(__file__).resolve().parents[1]


# Terraform show JSON omits the saved backend. Read only the pinned internal
# message envelope needed to bind the actual artifact, not mutable init metadata.
# Official schema: Terraform v1.17.0 internal/plans/planproto/planfile.proto
# Plan.version=1, terraform_version=14, backend=13; Backend type/config/workspace.
# This intentionally fails closed on another producer/format until reviewed.
def _protobuf_fields(data):
    fields = []
    offset = 0
    def varint():
        nonlocal offset
        result = 0
        for shift in range(0, 70, 7):
            assert offset < len(data), 'Truncated saved backend protobuf'
            byte = data[offset]
            offset += 1
            result |= (byte & 127) << shift
            if byte < 128:
                return result
        raise AssertionError('Invalid saved backend protobuf varint')
    while offset < len(data):
        tag = varint()
        number, wire = tag >> 3, tag & 7
        assert number > 0, 'Invalid saved backend protobuf field'
        if wire == 0:
            value = varint()
        else:
            assert wire in (1, 2, 5), 'Unsupported saved backend protobuf wire'
            length = varint() if wire == 2 else (8 if wire == 1 else 4)
            assert length <= len(data) - offset, 'Truncated saved backend protobuf value'
            value = data[offset:offset + length]
            offset += length
        fields.append((number, wire, value))
    return fields


def _one_field(fields, number, wire):
    matches = [(kind, value) for key, kind, value in fields if key == number]
    assert len(matches) == 1 and matches[0][0] == wire, 'Missing, duplicate or invalid saved backend field'
    return matches[0][1]


def _msgpack_value(data):
    # S3 backend config uses only known primitive objects/arrays. Reject unknown
    # values, extensions, binary payloads, floats, duplicate keys and trailing data.
    offset = 0
    def take(count):
        nonlocal offset
        assert count <= len(data) - offset, 'Truncated saved backend MessagePack'
        value = data[offset:offset + count]
        offset += count
        return value
    def integer(count, signed=False):
        return int.from_bytes(take(count), 'big', signed=signed)
    def value(depth=0):
        assert depth < 30, 'Saved backend MessagePack nesting exceeds limit'
        marker = integer(1)
        if marker <= 127: return marker
        if marker >= 224: return marker - 256
        if marker == 192: return None
        if marker in (194, 195): return marker == 195
        if 160 <= marker <= 191:
            return take(marker & 31).decode('utf-8')
        if marker in (217, 218, 219):
            return take(integer({217:1, 218:2, 219:4}[marker])).decode('utf-8')
        if 144 <= marker <= 159:
            return [value(depth + 1) for _ in range(marker & 15)]
        if marker in (220, 221):
            count = integer(2 if marker == 220 else 4)
            assert count <= len(data), 'Invalid saved backend array size'
            return [value(depth + 1) for _ in range(count)]
        if 128 <= marker <= 143 or marker in (222, 223):
            count = marker & 15 if marker <= 143 else integer(2 if marker == 222 else 4)
            assert count <= len(data), 'Invalid saved backend map size'
            result = {}
            for _ in range(count):
                key = value(depth + 1)
                assert isinstance(key, str) and key not in result, 'Duplicate or invalid saved backend config key'
                result[key] = value(depth + 1)
            return result
        if marker in (204, 205, 206, 207):
            return integer({204:1, 205:2, 206:4, 207:8}[marker])
        if marker in (208, 209, 210, 211):
            return integer({208:1, 209:2, 210:4, 211:8}[marker], signed=True)
        raise AssertionError('Unsupported saved backend MessagePack value')
    result = value()
    assert offset == len(data), 'Trailing saved backend MessagePack data'
    return result


def _saved_s3_backend(saved, context):
    expected_context = {
        'account':'772641336063', 'region':'us-east-2',
        'bucket':'772641336063-linked-in-node-terraform-state',
        'key':'linked-in-node/ecs-dev/terraform.tfstate',
        'workspace':'default', 'encrypt':True, 'useLockfile':True,
        'allowedAccountIds':['772641336063'],
        'workspaceKeyPrefix':'linked-in-node/ecs-dev/workspaces',
    }
    assert json.dumps(context,sort_keys=True) == json.dumps(expected_context,sort_keys=True), 'Unreviewed S3 backend context'
    fields = _protobuf_fields(saved.read('tfplan'))
    assert _one_field(fields, 1, 0) == 3, 'Unsupported Terraform saved-plan format'
    assert _one_field(fields, 14, 2) == b'1.17.0', 'Unsupported Terraform saved-backend producer; review schema before changing version'
    assert _one_field(fields, 25, 0) == 1 and _one_field(fields, 26, 0) == 1, 'Saved S3 plan must be complete and applyable'
    assert all(value == 0 for key, _, value in fields if key in (17,20)), 'Saved S3 plan must be normal and not errored'
    assert not any(key in (5,16,32) for key, _, _ in fields), 'Targeted or forced saved S3 plans require separate review'
    assert not any(key == 29 for key, _, _ in fields), 'Unreviewed Terraform state_store'
    backend = _protobuf_fields(_one_field(fields, 13, 2))
    assert {key for key, _, _ in backend} == {1, 2, 3}, 'Unexpected saved backend fields'
    assert _one_field(backend, 1, 2) == b's3', 'Actual saved backend must be S3'
    assert _one_field(backend, 3, 2) == b'default', 'Actual saved S3 workspace must be default'
    dynamic = _protobuf_fields(_one_field(backend, 2, 2))
    assert len(dynamic) == 1, 'Unsupported saved backend encoding'
    config = _msgpack_value(_one_field(dynamic, 1, 2))
    assert isinstance(config, dict), 'Saved S3 backend config must be an object'
    required = {
        'bucket':context['bucket'], 'key':context['key'], 'region':context['region'],
        'encrypt':True, 'use_lockfile':True,
        'allowed_account_ids':context['allowedAccountIds'],
        'workspace_key_prefix':context['workspaceKeyPrefix'],
    }
    for key, expected in required.items():
        assert key in config and type(config[key]) is type(expected) and config[key] == expected, 'Unreviewed saved S3 backend setting: ' + key
    # All authentication is temporary runtime environment configuration. Do not
    # accept cached access keys, profiles, assume-role hops, custom endpoints,
    # skip-validation flags, alternate locking or other unreviewed nonnull options.
    for key, setting in config.items():
        if key not in required:
            assert setting is None, 'Unreviewed saved S3 backend override: ' + key
    return {
        'type':'s3', 'bucket':context['bucket'], 'key':context['key'],
        'region':context['region'], 'workspace':'default', 'encrypt':True,
        'useLockfile':True, 'allowedAccountIds':context['allowedAccountIds'],
        'workspaceKeyPrefix':context['workspaceKeyPrefix'],
        'binding':'Decoded actual saved tfplan backend, not mutable initialization cache',
        'producer':'Terraform1.17.0 / planformat3',
    }


def review(plan_file, plan_binary, output, https_context=None, rates_file=None, s3_backend_context=None):
    private_inputs = [plan_file,plan_binary] + ([https_context] if https_context is not None else []) + ([s3_backend_context] if s3_backend_context is not None else [])
    for private_input in private_inputs:
        info = private_input.stat()
        assert info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) & 0o077 == 0, 'Plan/context inputs must be owner-only files'
    assert s3_backend_context is None or https_context is not None, 'Final S3-backed review requires the issued-certificate HTTPS context'
    backend_review = None
    # JSON alone cannot establish which source was actually saved by Terraform.
    with ZipFile(plan_binary) as saved:
        expected = {f'tfconfig/m-/{p.name}': p for p in (ROOT/'infra/aws-ecs-dev').glob('*.tf')}
        for name, path in expected.items():
            assert saved.read(name) == path.read_bytes(), f'Saved plan source differs: {path.name}'
        assert saved.read('.terraform.lock.hcl') == (ROOT/'infra/aws-ecs-dev/.terraform.lock.hcl').read_bytes(), 'Saved provider lock differs'
        saved_tf = {n for n in saved.namelist() if n.startswith('tfconfig/m-/') and n.endswith('.tf')}
        if s3_backend_context is None:
            assert saved_tf == set(expected) | {'tfconfig/m-/backend_override.tf'}, 'Unexpected saved Terraform configuration'
            assert ''.join(saved.read('tfconfig/m-/backend_override.tf').decode().split()) == 'terraform{backend"local"{}}', 'Preview must use local backend only'
        else:
            assert len(saved.namelist()) == len(set(saved.namelist())), 'Duplicate saved ZIP members are forbidden'
            saved_config = {name for name in saved.namelist() if name.startswith('tfconfig/')}
            assert saved_config == set(expected) | {'tfconfig/modules.json'}, 'Actual S3 plan must have no backend override or extra Terraform source'
            assert json.loads(saved.read('tfconfig/modules.json')) == [{'Key':'', 'Dir':'.'}], 'Unreviewed saved Terraform modules'
            backend_review = _saved_s3_backend(saved, json.loads(s3_backend_context.read_text()))
    template = ROOT/'infra/aws-ecs-dev/kafka-user-data.sh.tftpl'
    assert (plan_binary.parent/template.name).read_bytes() == template.read_bytes(), 'Scratch broker template differs from reviewed source'
    plan = json.loads(plan_file.read_text())
    # Actual S3 plans are saved outside the source root to keep artifacts private;
    # use the initialized root only for provider schemas, never as backend proof.
    schema_directory = ROOT/'infra/aws-ecs-dev' if backend_review is not None else plan_binary.parent
    shown = json.loads(subprocess.check_output(['terraform','show','-json',str(plan_binary)], cwd=schema_directory, text=True))
    assert plan == shown, 'Plan JSON does not match saved binary'

    context = json.loads(https_context.read_text()) if https_context is not None else None
    if context is not None:
        assert context['account'] == '772641336063' and context['region'] == 'us-east-2', 'Unexpected HTTPS context account/region'
        assert context['certificateStatus'] == 'ISSUED', 'HTTPS certificate must be verified issued'
        approved = context['approvedClientCidrs']
        assert len(approved) == 1 and ipaddress.ip_network(approved[0], strict=True).version == 4 and ipaddress.ip_network(approved[0], strict=True).prefixlen == 32, 'This review requires the one approved IPv4 /32'
        assert context['certificateArn'].startswith('arn:aws:acm:us-east-2:772641336063:certificate/'), 'Wrong certificate account/region'
    outputs = plan['planned_values']['outputs']
    value = lambda name: outputs[name]['value']
    assert value('deployment_account_id') == '772641336063', 'Unexpected AWS account'
    assert value('deployment_region') == 'us-east-2', 'Unexpected AWS region'
    resources = [r for r in plan.get('resource_changes', []) if r['mode'] == 'managed']
    assert all(r['change']['actions'] == ['create'] for r in resources), 'This first staging review requires create-only changes'
    def by_type(kind):
        return [r['change']['after'] for r in resources if r['type'] == kind]
    assert not any(by_type(k) for k in ['aws_secretsmanager_secret_version', 'tls_private_key', 'random_password', 'aws_iam_openid_connect_provider', 'aws_msk_cluster', 'aws_wafv2_web_acl']), 'Unreviewed secret material or service'
    broker_instances = by_type('aws_instance')
    db = by_type('aws_db_instance')
    assert len(broker_instances) == len(db) == 1
    assert broker_instances[0]['associate_public_ip_address'] is False
    assert all(b['encrypted'] for b in broker_instances[0]['root_block_device'])
    assert db[0]['publicly_accessible'] is False and db[0]['multi_az'] is False
    assert db[0]['storage_encrypted'] and db[0]['manage_master_user_password']
    assert db[0]['deletion_protection'] and not db[0]['skip_final_snapshot']
    assert db[0].get('password') is None
    assert len(by_type('aws_nat_gateway')) == 1
    assert by_type('aws_nat_gateway')[0]['availability_mode'] == 'zonal'
    listeners, host_rules = by_type('aws_lb_listener'), by_type('aws_lb_listener_rule')
    if context is None:
        assert len(listeners) == len(host_rules) == 0, 'Hostname-free staging must have no listener'
    else:
        assert len(listeners) == len(host_rules) == 1, 'HTTPS infrastructure requires exactly one listener and hostname rule'
        listener, host_rule = listeners[0], host_rules[0]
        assert listener['port'] == 443 and listener['protocol'] == 'HTTPS', 'Only HTTPS443 listener is reviewed'
        assert listener['ssl_policy'] == 'ELBSecurityPolicy-TLS13-1-2-2021-06', 'Unreviewed TLS policy'
        assert listener['certificate_arn'] == context['certificateArn'], 'Unreviewed listener certificate'
        action = listener['default_action']
        assert len(action) == 1 and action[0]['type'] == 'fixed-response' and action[0]['fixed_response'][0]['status_code'] == '403', 'Default hostname rejection must remain403'
        assert host_rule['priority'] == 10 and len(host_rule['condition']) == 1 and host_rule['condition'][0]['host_header'][0]['values'] == [context['applicationHostname']], 'Unreviewed host-header rule'
        assert len(host_rule['action']) == 1 and host_rule['action'][0]['type'] == 'forward', 'Hostname must forward only to the frontend target group'
        assert value('application_url') == 'https://' + context['applicationHostname'], 'Unreviewed application URL'

    assert len(by_type('aws_ecs_service')) == len(by_type('aws_ecs_task_definition')) == 0
    assert value('access_mode') == ('https_configured' if context is not None else 'no_listener_no_client_ingress_staging')
    assert not by_type('aws_security_group_rule'), 'Legacy SG rules are outside this reviewed design'
    for group in by_type('aws_security_group'):
        assert not group.get('ingress') and not group.get('egress'), 'Inline security-group rules are forbidden; use reviewed standalone rules'
    allowed_ports = {8180,8181,8182,8183,8184,5432,9093}
    cidr_ingress = []
    for rule in by_type('aws_vpc_security_group_ingress_rule'):
        assert not rule.get('cidr_ipv6'), 'IPv6 ingress is outside this design'
        if rule.get('cidr_ipv4'):
            assert context is not None, 'Staging permits no CIDR-based ingress'
            assert rule['cidr_ipv4'] in context['approvedClientCidrs'], 'Unapproved HTTPS client CIDR'
            assert rule['ip_protocol'] == 'tcp' and rule['from_port'] == rule['to_port'] == 443, 'CIDR ingress must be HTTPS443 only'
            cidr_ingress.append(rule['cidr_ipv4'])
        else:
            assert rule['ip_protocol'] == 'tcp' and rule['from_port'] == rule['to_port'] and rule['from_port'] in allowed_ports, 'Unexpected ingress protocol or port'
    assert sorted(cidr_ingress) == (sorted(context['approvedClientCidrs']) if context else []), 'Expected exactly the approved HTTPS client rule'
    for rule in by_type('aws_vpc_security_group_egress_rule'):
        assert not rule.get('cidr_ipv6'), 'IPv6 egress is outside this design'
        assert rule['ip_protocol'] == 'tcp' and rule['from_port'] == rule['to_port'], 'Unexpected egress protocol or range'
        if rule.get('cidr_ipv4'):
            assert rule['cidr_ipv4'] == '0.0.0.0/0' and rule['from_port'] in {80,443}, 'Unexpected CIDR egress'
        else:
            assert rule['from_port'] in allowed_ports, 'Unexpected SG egress port'
    # Bind the trust graph even while first-create IDs/ARNs are unknown.
    # A port allowlist alone cannot establish which SG owns or receives a rule.
    configuration = {r['address']:r for r in plan['configuration']['root_module']['resources']}
    planned = {r['address']:r for r in resources}
    capabilities = {'identity':8181,'catalog':8182,'inquiries':8183,'notifications':8184}
    def service_sg(name):
        return 'aws_security_group.service[' + json.dumps(name) + ']'
    def static_refs(address):
        refs = [address+'.id', address]
        return refs + (['aws_security_group.service'] if address.startswith('aws_security_group.service[') else [])
    def expression_refs(address, field):
        return set(configuration[address]['expressions'][field].get('references',[]))
    graph = {}
    def edge(direction, name, owner, peer, port, index=None):
        address = 'aws_vpc_security_group_' + direction + '_rule.' + name
        if index is not None:
            address += '[' + json.dumps(index) + ']'
        graph[address] = (owner,peer,port)
    alb, database, broker, bootstrap = ['aws_security_group.'+name for name in ['alb','database','broker','bootstrap']]
    front = service_sg('frontend')
    edge('ingress','frontend',front,alb,8180)
    edge('egress','alb_frontend',alb,front,8180)
    edge('ingress','catalog_lookup',service_sg('catalog'),service_sg('inquiries'),8182)
    edge('egress','catalog_lookup',service_sg('inquiries'),service_sg('catalog'),8182)
    for capability,port in capabilities.items():
        edge('ingress','api',service_sg(capability),front,port,capability)
        edge('egress','frontend_api',front,service_sg(capability),port,capability)
    for capability in [*capabilities,'bootstrap']:
        owner = bootstrap if capability == 'bootstrap' else service_sg(capability)
        edge('ingress','database',database,owner,5432,capability)
        edge('egress','database',owner,database,5432,capability)
    for capability in ['inquiries','notifications']:
        edge('ingress','broker',broker,service_sg(capability),9093,capability)
        edge('egress','broker',service_sg(capability),broker,9093,capability)
    for name in [*capabilities,'frontend','bootstrap','broker']:
        owner = bootstrap if name == 'bootstrap' else broker if name == 'broker' else service_sg(name)
        edge('egress','aws_https',owner,'cidr:0.0.0.0/0',443,name)
    edge('egress','broker_packages',broker,'cidr:0.0.0.0/0',80)
    if context is not None:
        for cidr in approved:
            edge('ingress','https',alb,'cidr:'+cidr,443,cidr)
    rule_addresses = {r['address'] for r in resources if r['type'] in ['aws_vpc_security_group_ingress_rule','aws_vpc_security_group_egress_rule']}
    assert rule_addresses == set(graph), 'Unreviewed security-group rule topology'
    dynamic_refs = {
        ('ingress','api','security_group_id'):['aws_security_group.service','each.key'],
        ('ingress','broker','referenced_security_group_id'):['aws_security_group.service','each.key'],
        ('ingress','database','referenced_security_group_id'):['each.value'],
        ('egress','frontend_api','referenced_security_group_id'):['aws_security_group.service','each.key'],
        ('egress','broker','security_group_id'):['aws_security_group.service','each.key'],
        ('egress','database','security_group_id'):['each.value'],
        ('egress','aws_https','security_group_id'):['each.value'],
    }
    mapped_db_refs = ['local.capabilities','aws_security_group.service','aws_security_group.bootstrap.id','aws_security_group.bootstrap']
    each_refs = {'api':['local.capabilities'],'frontend_api':['local.capabilities'],'broker':['local.brokers_clients'],'database':mapped_db_refs,'aws_https':['aws_security_group.service','aws_security_group.bootstrap.id','aws_security_group.bootstrap','aws_security_group.broker.id','aws_security_group.broker'],'https':['local.https_configured','var.approved_client_cidrs']}
    for address,(owner,peer,port) in graph.items():
        resource = planned[address]
        after,unknown = resource['change']['after'],resource['change']['after_unknown']
        base = address.split('[',1)[0]
        direction = 'ingress' if resource['type'].endswith('ingress_rule') else 'egress'
        name = base.split('.')[-1]
        assert after['from_port'] == after['to_port'] == port, 'Unreviewed SG graph port'
        fields = [('security_group_id',owner)]
        if peer.startswith('cidr:'):
            assert after.get('cidr_ipv4') == peer[5:] and not after.get('referenced_security_group_id'), 'Unreviewed CIDR graph edge'
        else:
            assert not after.get('cidr_ipv4'), 'SG graph edge replaced with CIDR'
            fields.append(('referenced_security_group_id',peer))
        for field,expected_sg in fields:
            expected_id = planned[expected_sg]['change']['after'].get('id')
            assert after.get(field) == expected_id, 'Unreviewed SG owner/peer ID'
            if expected_id is None:
                assert unknown.get(field) is True, 'Unknown SG ID must retain Terraform reference'
            refs = dynamic_refs.get((direction,name,field),static_refs(expected_sg))
            assert expression_refs(base,field) == set(refs), 'Unreviewed SG configuration reference'
        expected_each = set(each_refs.get(name,[]))
        assert set(configuration[base].get('for_each_expression',{}).get('references',[])) == expected_each, 'Unreviewed SG for_each mapping'
    assert expression_refs('aws_lb.dev','security_groups') == set(static_refs(alb)), 'ALB must use its reviewed SG'
    if context is not None:
        links = [
            ('aws_lb_listener.https[0]','load_balancer_arn','aws_lb.dev',{'aws_lb.dev.arn','aws_lb.dev'}),
            ('aws_lb_listener_rule.application[0]','listener_arn','aws_lb_listener.https[0]',{'aws_lb_listener.https[0].arn','aws_lb_listener.https[0]','aws_lb_listener.https'}),
        ]
        for owner,field,parent,refs in links:
            link = planned[owner]['change']
            parent_arn = planned[parent]['change']['after'].get('arn')
            assert link['after'].get(field) == parent_arn, 'Unreviewed HTTPS routing owner ARN'
            if parent_arn is None:
                assert link['after_unknown'].get(field) is True, 'Unknown HTTPS routing owner must retain Terraform reference'
            assert expression_refs(owner.split('[',1)[0],field) == refs, 'Unreviewed HTTPS routing configuration'
        target = planned['aws_lb_target_group.frontend']['change']['after'].get('arn')
        rule = planned['aws_lb_listener_rule.application[0]']['change']
        assert rule['after']['action'][0].get('target_group_arn') == target, 'Unreviewed frontend target group ARN'
        if target is None:
            assert rule['after_unknown']['action'][0]['target_group_arn'] is True, 'Unknown target group must retain Terraform reference'
        action = configuration['aws_lb_listener_rule.application']['expressions']['action'][0]
        assert set(action['target_group_arn']['references']) == {'aws_lb_target_group.frontend.arn','aws_lb_target_group.frontend'}, 'Unreviewed frontend target group configuration'
    q = value('cost_quantities')
    assert q['zonal_nat'] == 1 and q['interface_endpoints'] == 0 and q['s3_gateway_endpoints'] == 1
    assert q['runtime_secret_resources'] + q['rds_managed_master_secrets'] == 7
    assert q['standard_alarms'] == 7 and q['custom_host_metrics'] == 3
    assert len(by_type('aws_secretsmanager_secret')) == 6
    assert len(by_type('aws_cloudwatch_metric_alarm')) == 7
    assert len(by_type('aws_lb')) == len(by_type('aws_eip')) == 1
    assert len(by_type('aws_service_discovery_private_dns_namespace')) == 1
    assert broker_instances[0]['instance_type'] == 'm7i-flex.large'
    assert broker_instances[0]['root_block_device'][0]['volume_size'] == 40
    assert db[0]['instance_class'] == 'db.t4g.small' and db[0]['allocated_storage'] == 20
    model_spec = importlib.util.spec_from_file_location('reviewed_cost_model', ROOT/'docs/aws-cost-review-2026-10-27/model.py')
    model = importlib.util.module_from_spec(model_spec)
    model_spec.loader.exec_module(model)
    if rates_file is not None:
        model.RATES = json.loads(rates_file.read_text())
    cases = []
    for active in [False, True]:
        for hours in [24,720]:
            for profile in model.PROFILES:
                c = model.scenario('3 Private ECS/RDS + one NAT', hours, profile)
                h = D(hours)
                for item in c['items']:
                    key = item['rate_key']
                    if key == 'secrets_store': item['quantity'] = str(D(7)*h/D(730))
                    if key == 'secrets_api': item['quantity'] = str(D(70 if active else 150)*h)
                    if key == 'cloudwatch_metric': item['quantity'] = str(D(3)*h/D(730))
                    if key == 'cloudwatch_alarm_standard': item['quantity'] = str(D(7)*h/D(730))
                    # All backend tasks, RDS primary and broker are pinned in the same AZ.
                    if key == 'cross_az': item['quantity'] = '0'
                    if not active and key in ['fargate_cpu','fargate_memory']:
                        item['quantity'] = '0'
                    if key == 'cloudmap_resource':
                        item['quantity'] = str((D(q.get('broker_registered_resources', 0)) + D(5 if active else 0))*h/D(730))
                    if not active and context is None and key in ['alb_lcu','internet_out']:
                        item['quantity'] = '0'
                    if not active and context is not None and key in ['alb_lcu','internet_out']:
                        item['note'] = 'Conservative TLS/403/503 probe envelope from the selected usage profile; no running app tasks or marketplace traffic claimed.'
                    if key == 'secrets_store': item['note'] = 'Six runtime secret resources plus the RDS-managed master secret; conservative full storage pricing.'
                    if key == 'secrets_api': item['note'] = 'Modeled runtime/bootstrap/broker API reads; actual calls vary with retries and rotation.'
                    if key == 'cloudwatch_metric': item['note'] = 'Three agent host metrics: memory, disk, Kafka Java process.'
                    if key == 'cloudwatch_alarm_standard': item['note'] = 'Seven standard alarms; no notification topic provisioned.'
                    if key == 'cross_az': item['note'] = 'Backend tasks, broker and RDS primary in one AZ; user ingress/other-AZ traffic remains usage-dependent.'
                    item['usd'] = str(D(item['quantity']) * model.rate(key))
                kms_requests = D(70 if active else 150)*h + D(100)*h/D(24)
                c['items'].append({'meter':'KMS symmetric API allowance (AWS-managed keys)', 'rate_key':'kms_api', 'quantity':str(kms_requests), 'units':'requests', 'usd':str(kms_requests*model.rate('kms_api')), 'note':'Conservative unmeasured allowance: one KMS call per modeled Secrets read plus 100 storage/lifecycle calls per 24h; no customer key, no shared free allowance deducted. Empty-secret failures may not decrypt.'})
                c['mode'] = 'future_five_task_activation_NOT_PLANNED' if active else ('https_probe_infrastructure_NO_APP_TASKS' if context is not None else 'actual_infrastructure_staging')
                c['total_usd'] = str(sum(D(x['usd']) for x in c['items']))
                cases.append(c)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    source = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'infra/aws-ecs-dev').iterdir()) if p.is_file() and (p.suffix=='.tf' or p.name.endswith('.tftpl') or p.name=='.terraform.lock.hcl')}
    result = {'checkedAt':datetime.now(timezone.utc).isoformat(), 'status':'HTTPS_INFRASTRUCTURE_PREVIEW_ONLY_NOT_APPROVED' if context is not None else 'STAGING_PREVIEW_ONLY_NOT_APPROVED', 'sourceCommit':commit, 'sourceDirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()), 'sourceFilesSha256':source, 'planJsonSha256':hashlib.sha256(plan_file.read_bytes()).hexdigest(), 'planBinarySha256':hashlib.sha256(plan_binary.read_bytes()).hexdigest(), 'savedTfConfigMatchesCurrentSource':True, 'templateBinding':'External broker template matches private planning scratch; not embedded as a separate file in Terraform ZIP', 'changes':dict(Counter('/'.join(r['change']['actions']) for r in resources)), 'resourceTypes':dict(Counter(r['type'] for r in resources)), 'account':value('deployment_account_id'), 'region':value('deployment_region'), 'accessMode':value('access_mode'), 'quantities':q, 'costCases':cases, 'limits':['Local-backend preview; no remote state or apply', 'All seven secrets priced conservatively even before values are populated', 'Zero running app tasks and no visitor path in actual staging plan', 'Future five-task scenario is an estimate, not an activation plan', 'Exact-SHA verified images, secrets, bootstrap, owned hostname/issued certificate/CIDRs and new final plan required before activation', 'No cloud health, recovery, notification or deployment evidence']}
    if context is not None:
        result['httpsReview'] = {'hostname':context['applicationHostname'], 'certificateArn':context['certificateArn'], 'certificateStatusAtPreflight':context['certificateStatus'], 'approvedClientRuleCount':len(approved), 'approvedClientPrefixLength':32, 'exactCidrLocation':'Private review context and saved plan; omitted from published receipt', 'privateContextSha256':hashlib.sha256(https_context.read_bytes()).hexdigest()}
        result['limits'][2] = 'HTTPS listener and approved CIDR proposed; zero running app tasks. ALB may return403/503 and cannot serve marketplace until separate activation.'
    if backend_review is not None:
        result['status'] = 'S3_BACKED_HTTPS_INFRASTRUCTURE_PLAN_REVIEWED_NOT_APPROVED'
        result['backendReview'] = backend_review
        result['backendReview']['privateContextSha256'] = hashlib.sha256(s3_backend_context.read_bytes()).hexdigest()
        result['limits'][0] = 'Actual saved S3 backend bound to the isolated ECS state key; no application apply or activation'
        result['limits'].append('Offline backend binding does not establish live bucket controls, empty state, current identity or application health; verify those separately before any approved apply')
    if rates_file is not None:
        result['ratesFileSha256'] = hashlib.sha256(rates_file.read_bytes()).hexdigest()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    output.chmod(0o600)
    for c in cases:
        if c['profile']=='expected': print(c['mode'], c['hours']+'h', f"${D(c['total_usd']):.2f}")
    print('Saved sanitized staging/cost review:',output)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan-json',required=True,type=Path)
    parser.add_argument('--plan-binary',required=True,type=Path)
    parser.add_argument('--report',required=True,type=Path)
    parser.add_argument('--https-context',type=Path,help='Private owner-approved CIDR and actual issued-certificate context; omit to retain strict hostname-free review')
    parser.add_argument('--s3-backend-context',type=Path,help='Private exact S3 state isolation context; bind the actual saved backend instead of accepting a local preview')
    parser.add_argument('--rates-file',type=Path,help='Refreshed official rate receipt; original historical rates remain unchanged')
    args=parser.parse_args()
    review(args.plan_json.resolve(),args.plan_binary.resolve(),args.report.resolve(),args.https_context.resolve() if args.https_context else None,args.rates_file.resolve() if args.rates_file else None,args.s3_backend_context.resolve() if args.s3_backend_context else None)
