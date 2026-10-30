#!/usr/bin/env python3
"""Strict review of the single recorded partial-apply repair; never AWS/apply."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import stat
import subprocess
from zipfile import ZipFile

if not __debug__:
    raise SystemExit('Repair review refuses Python optimization')
ROOT = Path(__file__).resolve().parents[1]
ACCOUNT, REGION = '772641336063', 'us-east-2'
BASELINE_SHA = '5ec48dbf15cb268b42fc937dae8ffa3b537948302ac4e8ce7a6e6939da901ac5'
APPROVED_PLAN_SHA = '2fd776a529ab587759500bf71e43c5f461a528034db2942d5af2f664fe222b56'
DEADLINE = '2026-10-30T21:51:25Z'
LINEAGE = 'e92e5f80-f163-7df0-69db-022df56db002'
INITIAL_SPEC = importlib.util.spec_from_file_location('initial_reviewer', ROOT/'scripts/aws-ecs-review-plan.py')
initial = importlib.util.module_from_spec(INITIAL_SPEC)
INITIAL_SPEC.loader.exec_module(initial)
ALARMS = {'broker_disk','broker_process','alb_unhealthy','alb_5xx','database_storage','database_cpu','broker_status'}
EMPTY_DEFINITIONS = {'aws_service_discovery_service.app['+json.dumps(name)+']' for name in ['identity','catalog','inquiries','notifications','frontend']}
CREATES = {'aws_db_instance.dev','aws_lb_listener.https[0]','aws_lb_listener_rule.application[0]',
           'aws_service_discovery_service.broker','aws_service_discovery_instance.broker'} | {
           'aws_cloudwatch_metric_alarm.dev['+json.dumps(name)+']' for name in ALARMS}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private(path):
    info=path.stat()
    assert info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) & 0o077 == 0, 'Repair inputs must be owner-only files'


def state_resources(state):
    result={}
    for resource in state['resources']:
        if resource['mode'] != 'managed': continue
        for instance in resource['instances']:
            assert not instance.get('deposed'), 'Deposed baseline state is outside this repair'
            address=(resource.get('module','')+'.' if resource.get('module') else '')+resource['type']+'.'+resource['name']
            if 'index_key' in instance: address+='['+json.dumps(instance['index_key'])+']'
            assert address not in result, 'Duplicate baseline resource address'
            result[address]=instance
    return result


def without_expiry(value, path=()):
    if isinstance(value,dict):
        result={key:without_expiry(item,path+(key,)) for key,item in value.items()
                if not (path and path[-1] in ('tags','tags_all') and key=='ExpiresAt')}
        # Removing the sole explicit expiry tag yields no tags in provider state;
        # None and an empty tag map have identical semantics, not other fields.
        return None if path and path[-1] in ('tags','tags_all') and not result else result
    if isinstance(value,list): return [without_expiry(item,path+(str(i),)) for i,item in enumerate(value)]
    return value


def contains_true(value):
    if isinstance(value,dict):return any(contains_true(x) for x in value.values())
    if isinstance(value,list):return any(contains_true(x) for x in value)
    return value is True


def final_tags(value,path=(),root_mirror=None):
    if isinstance(value,dict):
        if root_mirror is not None and path==('root_block_device','0','tags_all'):
            assert value==root_mirror, 'Unreviewed computed root-volume tag mirror'
            return
        if path and path[-1] in ('tags','tags_all') and 'ExpiresAt' in value:
            assert value['ExpiresAt']==DEADLINE, 'Expiry tag resets or changes the actual deadline'
        for key,item in value.items():final_tags(item,path+(key,),root_mirror)
    elif isinstance(value,list):
        for i,item in enumerate(value):final_tags(item,path+(str(i),),root_mirror)


def validate_changes(plan,baseline):
    resources=[r for r in plan['resource_changes'] if r['mode']=='managed']
    mapping={r['address']:r for r in resources}
    assert len(mapping)==len(resources)==112, 'Unexpected final repaired resource count'
    assert set(mapping)==set(baseline)|CREATES, 'Unreviewed resource additions/removals'
    actual_creates=set()
    updates=[]
    for address,resource in mapping.items():
        change=resource['change']; actions=change['actions']
        if address in CREATES:
            assert actions==['create'] and change['before'] is None, 'Missing resource must be create-only'
            actual_creates.add(address)
        else:
            before=change['before'];old=baseline[address]['attributes']
            assert before is not None and before.get('id')==old.get('id'), 'Repair before identity differs from frozen baseline'
            if address in EMPTY_DEFINITIONS:
                assert actions==['delete','create'] and resource.get('action_reason')=='replace_because_cannot_update', 'Only delete-before-create empty discovery definitions are reviewed'
                assert change.get('replace_paths')==[['health_check_custom_config',0,'failure_threshold'],['health_check_custom_config']], 'Unreviewed discovery replacement path'
                after=change['after']
                assert before['health_check_custom_config']==[] and after['health_check_custom_config']==[{'failure_threshold':1}], 'Discovery custom health transition differs'
                for field in ['name','dns_config','force_destroy','health_check_config','region']:
                    assert after[field]==before[field], 'Discovery definition changed beyond custom health'
                assert after.get('description') in ('',None) and before.get('description') in ('',None)
                assert after.get('id') is None and change['after_unknown'].get('id') is True, 'Replaced discovery identity must be unknown'
                assert set(after)=={'description','dns_config','force_destroy','health_check_config','health_check_custom_config','name','region','tags','tags_all'}, 'Unreviewed discovery definition setting'
                assert after['tags'] is None and set(before['tags'])=={'ExpiresAt'}, 'Unreviewed discovery explicit tags'
                assert without_expiry({'tags_all':after['tags_all']})==without_expiry({'tags_all':before['tags_all']}), 'Discovery ownership tags differ'
            elif address=='aws_lb.dev':
                assert actions==['delete','create'], 'Only delete-before-create ALB replacement is reviewed'
                assert resource.get('action_reason')=='replace_because_tainted', 'ALB replacement must retain recorded taint'
                assert baseline[address].get('status')=='tainted', 'Baseline ALB taint missing'
                assert change['after'].get('id') is None and change['after_unknown'].get('id') is True, 'New ALB identity must be unknown'
            else:
                assert actions in (['no-op'],['update']), 'Unexpected deletion or replacement'
                assert change['after'].get('id')==old.get('id'), 'Existing resource identity changed'
                if actions==['no-op']:
                    assert change['after']==before, 'No-op values differ'
                else:
                    clean_before=without_expiry(before);clean_after=without_expiry(change['after'])
                    if address=='aws_s3_bucket_policy.operations':
                        clean_before.pop('policy',None);clean_after.pop('policy',None)
                    assert clean_before==clean_after, 'Unreviewed nonmetadata update: '+address
                    assert not contains_true(change['after_unknown']), 'Existing update introduces unknown values'
                    updates.append(address)
        mirror=None
        if address=='aws_instance.broker':
            frozen=baseline[address]['attributes']
            for side in ['before','after']:
                observed=change[side]
                for key in ['ami','id','arn','availability_zone','private_ip','subnet_id','vpc_security_group_ids','iam_instance_profile','user_data','user_data_base64','user_data_replace_on_change','instance_type','associate_public_ip_address','metadata_options']:
                    assert observed.get(key)==frozen.get(key), 'Frozen broker control changed: '+key
                assert len(observed['root_block_device'])==len(frozen['root_block_device'])==1
                for key in ['volume_id','device_name','encrypted','delete_on_termination','iops','kms_key_id','throughput','volume_size','volume_type']:
                    assert observed['root_block_device'][0][key]==frozen['root_block_device'][0][key], 'Frozen broker volume control changed: '+key
            root=change['after']['root_block_device'][0]
            assert root['tags']=={'ExpiresAt':DEADLINE}, 'Explicit canonical root-volume expiry is required'
            prior_mirror=frozen['root_block_device'][0]['tags_all']
            if root['tags_all'].get('ExpiresAt')!=DEADLINE:
                assert prior_mirror['ExpiresAt']=='2026-10-30T22:00:00Z' and root['tags_all']==prior_mirror, 'Only the exact prior computed root tag mirror may remain stale'
                mirror=prior_mirror
        final_tags(change['after'],root_mirror=mirror)
    assert actual_creates==CREATES, 'Expected exact missing-resource creates'
    assert 'aws_s3_bucket_policy.operations' in updates, 'ALB log-bucket policy repair must be explicit'
    return resources,updates


def validate_sg_mirrors(resources):
    """AWS read-back may coalesce peers; expand atoms and bind to standalone rules."""
    groups={r['change']['after']['id']:r['change']['after'] for r in resources if r['type']=='aws_security_group'}
    assert None not in groups and len(groups)==9, 'Repair requires the nine existing SG identities'
    expected={(identity,direction):set() for identity in groups for direction in ['ingress','egress']}
    for resource in resources:
        if resource['type'] not in ['aws_vpc_security_group_ingress_rule','aws_vpc_security_group_egress_rule']:continue
        value=resource['change']['after'];direction='ingress' if resource['type'].endswith('ingress_rule') else 'egress'
        assert value['security_group_id'] in groups, 'Unknown SG mirror owner'
        peer=('cidr',value['cidr_ipv4']) if value.get('cidr_ipv4') else ('sg',value['referenced_security_group_id'])
        atom=(value['ip_protocol'],value['from_port'],value['to_port'],*peer)
        assert atom not in expected[value['security_group_id'],direction], 'Duplicate standalone SG atom'
        expected[value['security_group_id'],direction].add(atom)
    for identity,group in groups.items():
        for direction in ['ingress','egress']:
            observed=set()
            for permission in group.get(direction,[]):
                assert not permission['ipv6_cidr_blocks'] and not permission['prefix_list_ids'] and permission['self'] is False, 'Unreviewed computed SG mirror peer kind'
                assert permission.get('description','')=='', 'Unreviewed computed SG mirror description'
                peers=[('cidr',x) for x in permission['cidr_blocks']]+[('sg',x) for x in permission['security_groups']]
                assert peers, 'Computed SG mirror rule has no peer'
                for kind,peer in peers:
                    atom=(permission['protocol'],permission['from_port'],permission['to_port'],kind,peer)
                    assert atom not in observed, 'Duplicate computed SG mirror atom'
                    observed.add(atom)
            assert observed==expected[identity,direction], 'Computed SG mirrors differ from exact standalone graph'


def validate_topology(plan,context):
    resources=[r for r in plan['resource_changes'] if r['mode']=='managed']
    outputs=plan['planned_values']['outputs']
    value=lambda name:outputs[name]['value']
    approved=context['approvedClientCidrs']
    def by_type(kind):return [r['change']['after'] for r in resources if r['type']==kind]
    assert value('deployment_account_id')==ACCOUNT and value('deployment_region')==REGION, 'Wrong deployment identity'
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
    for group_resource in [r for r in resources if r['type']=='aws_security_group']:
        base=group_resource['address'].split('[',1)[0]
        declared=next(r for r in plan['configuration']['root_module']['resources'] if r['address']==base)
        assert 'ingress' not in declared['expressions'] and 'egress' not in declared['expressions'], 'Configured inline SG rules are forbidden'
    validate_sg_mirrors(resources)
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
    assert not by_type('aws_route53_record'), 'Manual records in the Cloud Map hosted zone are forbidden'
    assert type(db[0]['backup_retention_period']) is int and db[0]['backup_retention_period']==1, 'Repair requires explicit nonzero one-day RDS backups'
    assert db[0]['engine']=='postgres' and db[0]['engine_version']=='17.6' and db[0]['storage_type']=='gp3'
    assert db[0]['max_allocated_storage']==20 and db[0]['availability_zone']=='us-east-2a'
    assert db[0]['port']==5432 and db[0]['delete_automated_backups'] is False
    parameters=by_type('aws_db_parameter_group')[0]
    assert {x['name']:x['value'] for x in parameters['parameter']}=={'rds.force_ssl':'1','log_statement':'none','log_min_error_statement':'panic'}, 'RDS SSL/password-log controls differ'
    assert db[0]['parameter_group_name']==parameters['name']
    subnet_values={r['address']:r['change']['after'] for r in resources if r['type']=='aws_subnet'}
    public_ids={subnet_values['aws_subnet.public['+str(i)+']']['id'] for i in [0,1]}
    private_ids={subnet_values['aws_subnet.private['+str(i)+']']['id'] for i in [0,1]}
    assert set(by_type('aws_lb')[0]['subnets'])==public_ids, 'ALB subnet boundaries differ'
    assert set(by_type('aws_db_subnet_group')[0]['subnet_ids'])==private_ids, 'Database subnet boundaries differ'
    assert db[0]['db_subnet_group_name']==by_type('aws_db_subnet_group')[0]['name']
    assert db[0]['vpc_security_group_ids']==[next(r['change']['after']['id'] for r in resources if r['address']=='aws_security_group.database')]
    assert broker_instances[0]['subnet_id']==subnet_values['aws_subnet.private[0]']['id']
    assert db[0]['engine_lifecycle_support']=='open-source-rds-extended-support-disabled'
    assert broker_instances[0]['metadata_options'][0]['http_tokens']=='required'
    assert broker_instances[0]['id']=='i-06a5a2da57b60f70a', 'Broker replacement is forbidden'
    assert all(x['retention_in_days']==7 for x in by_type('aws_cloudwatch_log_group')) and len(by_type('aws_cloudwatch_log_group'))==8
    assert all(x['recovery_window_in_days']==7 for x in by_type('aws_secretsmanager_secret'))
    assert all(x['alarm_actions'] in (None,[]) and x['ok_actions'] in (None,[]) for x in by_type('aws_cloudwatch_metric_alarm')), 'Unreviewed alarm notification actions'
    assert all(x['image_tag_mutability']=='IMMUTABLE' and x['image_scanning_configuration'][0]['scan_on_push'] for x in by_type('aws_ecr_repository'))
    lb=by_type('aws_lb')[0]
    assert lb['internal'] is False and lb['load_balancer_type']=='application' and lb['ip_address_type']=='ipv4'
    assert lb['access_logs'][0]['enabled'] and lb['access_logs'][0]['prefix']=='alb'
    operation=next(r['change']['after'] for r in resources if r['address']=='aws_s3_bucket.operations')
    assert operation['force_destroy'] is False and lb['access_logs'][0]['bucket']==operation['id']
    policy=next(r['change']['after'] for r in resources if r['address']=='aws_s3_bucket_policy.operations')
    expected_policy={'Version':'2012-10-17','Statement':[
        {'Sid':'DenyInsecureTransport','Effect':'Deny','Principal':'*','Action':'s3:*',
         'Resource':[operation['arn'],operation['arn']+'/*'],'Condition':{'Bool':{'aws:SecureTransport':'false'}}},
        {'Sid':'ALBAccessLogs','Effect':'Allow','Principal':{'Service':'logdelivery.elasticloadbalancing.amazonaws.com'},
         'Action':'s3:PutObject','Resource':operation['arn']+'/alb/AWSLogs/'+ACCOUNT+'/*',
         'Condition':{'ArnLike':{'aws:SourceArn':'arn:aws:elasticloadbalancing:'+REGION+':'+ACCOUNT+':loadbalancer/*'}}}]}
    assert json.loads(policy['policy'])==expected_policy, 'Unreviewed ALB logging bucket policy'
    namespace=by_type('aws_service_discovery_private_dns_namespace')[0]
    broker_service=next(r['change'] for r in resources if r['address']=='aws_service_discovery_service.broker')
    service=broker_service['after']
    assert service['name']=='kafka' and service['dns_config']==[{'namespace_id':namespace['id'],'routing_policy':'MULTIVALUE','dns_records':[{'ttl':10,'type':'A'}]}], 'Unreviewed broker discovery DNS'
    assert not service.get('health_check_config') and not service.get('health_check_custom_config'), 'No broker health controller is provisioned'
    instance=next(r['change'] for r in resources if r['address']=='aws_service_discovery_instance.broker')
    assert instance['after']['instance_id']=='broker' and instance['after']['attributes']=={'AWS_INSTANCE_IPV4':broker_instances[0]['private_ip'],'AWS_INSTANCE_PORT':'9093'}, 'Broker discovery identity/peer differs'
    assert instance['after'].get('service_id')==service.get('id') and instance['after_unknown'].get('service_id') is True, 'Broker discovery must reference its new service'
    config={r['address']:r for r in plan['configuration']['root_module']['resources']}
    assert set(config['aws_service_discovery_service.broker']['expressions']['dns_config'][0]['namespace_id']['references'])=={'aws_service_discovery_private_dns_namespace.dev.id','aws_service_discovery_private_dns_namespace.dev'}
    assert set(config['aws_service_discovery_instance.broker']['expressions']['service_id']['references'])=={'aws_service_discovery_service.broker.id','aws_service_discovery_service.broker'}
    assert set(config['aws_service_discovery_instance.broker']['expressions']['attributes']['references'])=={'aws_instance.broker.private_ip','aws_instance.broker'}
    assert q['rds_backup_days']==1 and q['broker_registered_resources']==1 and q['fargate_tasks']==0, 'Cost quantities must describe repaired topology'
    return q


def calculate_costs(q,rates_file,proposal):
    context=True
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
    expected={('future' if 'future' in c['mode'] else 'stage',c['hours'],c['profile']):c for c in proposal['costCases']}
    assert len(cases)==len(expected)==12, 'Expected all twelve cost cases'
    for case in cases:
        key=('future' if 'future' in case['mode'] else 'stage',case['hours'],case['profile'])
        proposed=expected[key]
        assert D(case['total_usd'])==D(proposed['total_usd']), 'Repair cost total differs from current proposal'
        assert [(i['rate_key'],D(i['quantity']),D(i['usd'])) for i in case['items']]==[(i['rate_key'],D(i['quantity']),D(i['usd'])) for i in proposed['items']], 'Repair cost item quantities/rates differ'
        case['mode']=proposed['mode']
    return cases


def review(plan_file,plan_binary,baseline_file,repair_context,https_context,s3_context,rates_file,cost_proposal,cloudmap_instances,output):
    for path in [plan_file,plan_binary,baseline_file,repair_context,https_context,s3_context,cost_proposal,cloudmap_instances]:private(path)
    context=json.loads(repair_context.read_text())
    assert context=={'account':ACCOUNT,'region':REGION,'baselineStateSha256':BASELINE_SHA,'approvedPlanSha256':APPROVED_PLAN_SHA,'shutdownDeadlineUtc':DEADLINE,'originalExactShutdownDeadlineUtc':'2026-10-30T21:51:25.219221Z','baselineLineage':LINEAGE,'baselineSerial':4,'scope':'PREPARATION_ONLY_REPAIR_NOT_APPROVED_NO_APPLICATION_ACTIVATION','cloudMapInstancesSha256':sha(cloudmap_instances)}, 'Unreviewed repair context'
    assert sha(baseline_file)==BASELINE_SHA, 'Frozen baseline state hash differs'
    baseline_state=json.loads(baseline_file.read_text())
    assert baseline_state['lineage']==LINEAGE and baseline_state['serial']==4, 'Baseline lineage/serial differs'
    baseline=state_resources(baseline_state)
    assert len(baseline)==100 and [a for a,i in baseline.items() if i.get('status')=='tainted']==['aws_lb.dev'], 'Unexpected partial baseline or taints'
    cm=json.loads(cloudmap_instances.read_text())
    assert cm['account']==ACCOUNT and cm['region']==REGION, 'Wrong discovery instance evidence identity'
    checked=datetime.fromisoformat(cm['checkedAt'].replace('Z','+00:00'))
    assert checked.tzinfo is not None and 0 <= (datetime.now(timezone.utc)-checked).total_seconds() <= 7200, 'Discovery emptiness evidence is not fresh'
    expected_services={baseline[address]['attributes']['id']:[] for address in EMPTY_DEFINITIONS}
    assert cm['instancesByServiceId']==expected_services, 'Only independently checked empty discovery definitions may be replaced'
    assert datetime.now(timezone.utc)<datetime.fromisoformat(DEADLINE.replace('Z','+00:00')), 'The original shutdown deadline has passed; no repair lifetime extension'
    with ZipFile(plan_binary) as saved:
        assert len(saved.namelist())==len(set(saved.namelist())), 'Duplicate saved ZIP names'
        source={f'tfconfig/m-/{p.name}':p for p in (ROOT/'infra/aws-ecs-dev').glob('*.tf')}
        assert {n for n in saved.namelist() if n.startswith('tfconfig/')}==set(source)|{'tfconfig/modules.json'}, 'Extra source/module/backend override'
        for name,path in source.items():assert saved.read(name)==path.read_bytes(), 'Saved repair source differs: '+path.name
        assert json.loads(saved.read('tfconfig/modules.json'))==[{'Key':'','Dir':'.'}], 'Unreviewed modules'
        assert saved.read('.terraform.lock.hcl')==(ROOT/'infra/aws-ecs-dev/.terraform.lock.hcl').read_bytes(), 'Provider lock differs'
        backend=initial._saved_s3_backend(saved,json.loads(s3_context.read_text()))
        prior=json.loads(saved.read('tfstate'))
        assert prior['lineage']==LINEAGE and prior['serial']==4, 'Saved plan prior-state lineage/serial differs'
        prior_resources=state_resources(prior)
        assert set(prior_resources)==set(baseline), 'Saved plan prior resource scope differs'
        for address,instance in baseline.items():
            assert prior_resources[address]['attributes'].get('id')==instance['attributes'].get('id'), 'Saved plan prior identity differs'
            assert prior_resources[address].get('status')==instance.get('status'), 'Saved plan prior taint differs'
    assert (plan_binary.parent/'kafka-user-data.sh.tftpl').read_bytes()==(ROOT/'infra/aws-ecs-dev/kafka-user-data.sh.tftpl').read_bytes(), 'External broker template differs'
    plan=json.loads(plan_file.read_text())
    shown=json.loads(subprocess.check_output(['terraform','show','-json',str(plan_binary)],cwd=ROOT/'infra/aws-ecs-dev',text=True))
    assert plan==shown, 'Repair JSON does not match actual saved binary'
    for resource in plan['resource_changes']:
        if resource['mode']=='managed' and resource['change']['before'] is not None:
            assert resource['address'] in prior_resources, 'Repair before resource address absent from frozen prior state'
            assert resource['change']['before']==prior_resources[resource['address']]['attributes'], 'Plan before values differ from actual embedded prior state'
    https=json.loads(https_context.read_text())
    assert https['account']==ACCOUNT and https['region']==REGION and https['certificateStatus']=='ISSUED', 'Wrong HTTPS account/region/status'
    assert len(https['approvedClientCidrs'])==1 and ipaddress.ip_network(https['approvedClientCidrs'][0],strict=True).version==4 and ipaddress.ip_network(https['approvedClientCidrs'][0],strict=True).prefixlen==32, 'One approved IPv4 /32 required'
    variables={key:item['value'] for key,item in plan['variables'].items()}
    assert variables['region']==REGION and variables['expires_at']==DEADLINE, 'Repair must preserve the original shutdown deadline'
    assert type(variables['rds_backup_retention_days']) is int and variables['rds_backup_retention_days']==1 and variables['teardown_discard_demo_data'] is False and variables['protect_database'] is True, 'Unreviewed backup/discard/protection input'
    assert variables['deploy_application'] is False and variables['image_digests'] is None and variables['seed_demo'] is False, 'Application activation is outside repair scope'
    assert variables['notification_topic_arn'] is None, 'Unreviewed alarm notification destination'
    assert variables['approved_client_cidrs']==https['approvedClientCidrs'] and variables['application_hostname']==https['applicationHostname'] and variables['certificate_arn']==https['certificateArn'], 'HTTPS inputs differ from reviewed context'
    resources,updates=validate_changes(plan,baseline)
    q=validate_topology(plan,https)
    proposal=json.loads(cost_proposal.read_text())
    assert sha(rates_file)==proposal['priceRatesSha256'], 'Rates differ from fresh proposal'
    pq=proposal['quantities']
    expected_pq={key:value for key,value in q.items() if key!='broker_registered_resources'}
    expected_pq.update(broker_registered_cloudmap_resources=q['broker_registered_resources'],cloudmap_registered_resources_infrastructure=1,cloudmap_registered_resources_future_five_app_tasks=6)
    assert pq==expected_pq, 'Actual quantities differ from the complete current cost proposal'
    cases=calculate_costs(q,rates_file,proposal)
    result={'checkedAt':datetime.now(timezone.utc).isoformat(),'status':'PARTIAL_APPLY_REPAIR_PLAN_REVIEWED_NOT_APPROVED',
        'account':ACCOUNT,'region':REGION,'approvedConsumedInitialPlanSha256':APPROVED_PLAN_SHA,
        'baselineStateSha256':BASELINE_SHA,'cloudMapInstancesEvidenceSha256':sha(cloudmap_instances),'baselineSerial':4,'baselineManagedResources':100,
        'planBinarySha256':sha(plan_binary),'planJsonSha256':sha(plan_file),'repairContextSha256':sha(repair_context),
        'sourceFilesSha256':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'infra/aws-ecs-dev').iterdir() if p.suffix=='.tf' or p.name.endswith('.tftpl') or p.name=='.terraform.lock.hcl'},
        'changes':dict(Counter('/'.join(r['change']['actions']) for r in resources)), 'updates':[address if not address.startswith('aws_vpc_security_group_ingress_rule.https[') else 'aws_vpc_security_group_ingress_rule.https[APPROVED_CLIENT_REDACTED]' for address in updates],
        'finalManagedResources':len(resources),'backendReview':backend,'quantities':q,'costCases':cases,
        'deadlineUtc':DEADLINE,'clockReset':False,'httpsReview':{'hostname':https['applicationHostname'],'certificateArn':https['certificateArn'],'approvedClientRuleCount':1,'clientPrefixLength':32,'exactCidrLocation':'Private context and plan only'},
        'limits':['No repair apply authorization or execution','Only the tainted ALB and five independently verified empty discovery definitions are replaced; no untaint/import/target shortcuts','RDS one-day account eligibility remains unproven until an approved create succeeds','Zero app tasks; no marketplace runtime/TLS/discovery/health/metric/recovery success inferred','Original24-hour clock remains unchanged; partial resources continue costing','Replacement rounding/transition reserve and sunk timing remain in the separate current cost proposal','Provider6.70 computed EBS tags_all may retain the exact old22:00 mirror while explicit root tags set canonical21:51:25; verify actual EBS tag after any approved apply']}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n');output.chmod(0o600)
    for case in cases:
        if case['profile']=='expected':print(case['mode'],case['hours']+'h',str(D(case['total_usd']).quantize(D('0.01'))))
    print('Saved sanitized strict repair review:',output)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['plan-json','plan-binary','baseline-state','repair-context','https-context','s3-backend-context','rates-file','cost-proposal','cloudmap-instances','report']:
        parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args()
    review(args.plan_json.resolve(),args.plan_binary.resolve(),args.baseline_state.resolve(),args.repair_context.resolve(),args.https_context.resolve(),args.s3_backend_context.resolve(),args.rates_file.resolve(),args.cost_proposal.resolve(),args.cloudmap_instances.resolve(),args.report.resolve())
