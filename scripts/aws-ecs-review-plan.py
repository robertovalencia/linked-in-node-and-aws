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
from pathlib import Path
import subprocess
from zipfile import ZipFile

if not __debug__:
    raise SystemExit("Plan review refuses Python optimization because validation checks must run")

ROOT = Path(__file__).resolve().parents[1]


def review(plan_file, plan_binary, output):
    # JSON alone cannot establish which source was actually saved by Terraform.
    with ZipFile(plan_binary) as saved:
        expected = {f'tfconfig/m-/{p.name}': p for p in (ROOT/'infra/aws-ecs-dev').glob('*.tf')}
        for name, path in expected.items():
            assert saved.read(name) == path.read_bytes(), f'Saved plan source differs: {path.name}'
        assert saved.read('.terraform.lock.hcl') == (ROOT/'infra/aws-ecs-dev/.terraform.lock.hcl').read_bytes(), 'Saved provider lock differs'
        saved_tf = {n for n in saved.namelist() if n.startswith('tfconfig/m-/') and n.endswith('.tf')}
        assert saved_tf == set(expected) | {'tfconfig/m-/backend_override.tf'}, 'Unexpected saved Terraform configuration'
        assert ''.join(saved.read('tfconfig/m-/backend_override.tf').decode().split()) == 'terraform{backend"local"{}}', 'Preview must use local backend only'
    template = ROOT/'infra/aws-ecs-dev/kafka-user-data.sh.tftpl'
    assert (plan_binary.parent/template.name).read_bytes() == template.read_bytes(), 'Scratch broker template differs from reviewed source'
    plan = json.loads(plan_file.read_text())
    shown = json.loads(subprocess.check_output(['terraform','show','-json',str(plan_binary)], cwd=plan_binary.parent, text=True))
    assert plan == shown, 'Plan JSON does not match saved binary'

    outputs = plan['planned_values']['outputs']
    value = lambda name: outputs[name]['value']
    assert value('deployment_account_id') == '772641336063', 'Unexpected AWS account'
    assert value('deployment_region') == 'us-east-2', 'Unexpected AWS region'
    resources = [r for r in plan.get('resource_changes', []) if r['mode'] == 'managed']
    assert all(r['change']['actions'] == ['create'] for r in resources), 'This first staging review requires create-only changes'
    def by_type(kind):
        return [r['change']['after'] for r in resources if r['type'] == kind]
    assert not any(by_type(k) for k in ['aws_secretsmanager_secret_version', 'tls_private_key', 'random_password', 'aws_iam_openid_connect_provider', 'aws_msk_cluster', 'aws_wafv2_web_acl']), 'Unreviewed secret material or service'
    broker = by_type('aws_instance')
    db = by_type('aws_db_instance')
    assert len(broker) == len(db) == 1
    assert broker[0]['associate_public_ip_address'] is False
    assert all(b['encrypted'] for b in broker[0]['root_block_device'])
    assert db[0]['publicly_accessible'] is False and db[0]['multi_az'] is False
    assert db[0]['storage_encrypted'] and db[0]['manage_master_user_password']
    assert db[0]['deletion_protection'] and not db[0]['skip_final_snapshot']
    assert db[0].get('password') is None
    assert len(by_type('aws_nat_gateway')) == 1
    assert by_type('aws_nat_gateway')[0]['availability_mode'] == 'zonal'
    assert len(by_type('aws_lb_listener')) == 0, 'Hostname-free staging must have no listener'
    assert len(by_type('aws_ecs_service')) == len(by_type('aws_ecs_task_definition')) == 0
    assert value('access_mode') == 'no_listener_no_client_ingress_staging'
    assert not by_type('aws_security_group_rule'), 'Legacy SG rules are outside this reviewed design'
    for group in by_type('aws_security_group'):
        assert not group.get('ingress') and not group.get('egress'), 'Inline security-group rules are forbidden; use reviewed standalone rules'
    allowed_ports = {8180,8181,8182,8183,8184,5432,9093}
    for rule in by_type('aws_vpc_security_group_ingress_rule'):
        assert not rule.get('cidr_ipv4') and not rule.get('cidr_ipv6'), 'Staging permits no CIDR-based ingress'
        assert rule['ip_protocol'] == 'tcp' and rule['from_port'] == rule['to_port'] and rule['from_port'] in allowed_ports, 'Unexpected ingress protocol or port'
    for rule in by_type('aws_vpc_security_group_egress_rule'):
        assert not rule.get('cidr_ipv6'), 'IPv6 egress is outside this design'
        assert rule['ip_protocol'] == 'tcp' and rule['from_port'] == rule['to_port'], 'Unexpected egress protocol or range'
        if rule.get('cidr_ipv4'):
            assert rule['cidr_ipv4'] == '0.0.0.0/0' and rule['from_port'] in {80,443}, 'Unexpected CIDR egress'
        else:
            assert rule['from_port'] in allowed_ports, 'Unexpected SG egress port'
    q = value('cost_quantities')
    assert q['zonal_nat'] == 1 and q['interface_endpoints'] == 0 and q['s3_gateway_endpoints'] == 1
    assert q['runtime_secret_resources'] + q['rds_managed_master_secrets'] == 7
    assert q['standard_alarms'] == 7 and q['custom_host_metrics'] == 3
    assert len(by_type('aws_secretsmanager_secret')) == 6
    assert len(by_type('aws_cloudwatch_metric_alarm')) == 7
    assert len(by_type('aws_lb')) == len(by_type('aws_eip')) == 1
    assert len(by_type('aws_service_discovery_private_dns_namespace')) == 1
    assert broker[0]['instance_type'] == 'm7i-flex.large'
    assert broker[0]['root_block_device'][0]['volume_size'] == 40
    assert db[0]['instance_class'] == 'db.t4g.small' and db[0]['allocated_storage'] == 20
    model_spec = importlib.util.spec_from_file_location('reviewed_cost_model', ROOT/'docs/aws-cost-review-2026-10-27/model.py')
    model = importlib.util.module_from_spec(model_spec)
    model_spec.loader.exec_module(model)
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
                    if not active and key in ['fargate_cpu','fargate_memory','cloudmap_resource','alb_lcu','internet_out']:
                        item['quantity'] = '0'
                    if key == 'secrets_store': item['note'] = 'Six runtime secret resources plus the RDS-managed master secret; conservative full storage pricing.'
                    if key == 'secrets_api': item['note'] = 'Modeled runtime/bootstrap/broker API reads; actual calls vary with retries and rotation.'
                    if key == 'cloudwatch_metric': item['note'] = 'Three agent host metrics: memory, disk, Kafka Java process.'
                    if key == 'cloudwatch_alarm_standard': item['note'] = 'Seven standard alarms; no notification topic provisioned.'
                    if key == 'cross_az': item['note'] = 'Backend tasks, broker and RDS primary in one AZ; user ingress/other-AZ traffic remains usage-dependent.'
                    item['usd'] = str(D(item['quantity']) * model.rate(key))
                kms_requests = D(70 if active else 150)*h + D(100)*h/D(24)
                c['items'].append({'meter':'KMS symmetric API allowance (AWS-managed keys)', 'rate_key':'kms_api', 'quantity':str(kms_requests), 'units':'requests', 'usd':str(kms_requests*model.rate('kms_api')), 'note':'Conservative unmeasured allowance: one KMS call per modeled Secrets read plus 100 storage/lifecycle calls per 24h; no customer key, no shared free allowance deducted. Empty-secret failures may not decrypt.'})
                c['mode'] = 'future_five_task_activation_NOT_PLANNED' if active else 'actual_infrastructure_staging'
                c['total_usd'] = str(sum(D(x['usd']) for x in c['items']))
                cases.append(c)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    source = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'infra/aws-ecs-dev').iterdir()) if p.is_file() and (p.suffix=='.tf' or p.name.endswith('.tftpl') or p.name=='.terraform.lock.hcl')}
    result = {'checkedAt':datetime.now(timezone.utc).isoformat(), 'status':'STAGING_PREVIEW_ONLY_NOT_APPROVED', 'sourceCommit':commit, 'sourceDirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()), 'sourceFilesSha256':source, 'planJsonSha256':hashlib.sha256(plan_file.read_bytes()).hexdigest(), 'planBinarySha256':hashlib.sha256(plan_binary.read_bytes()).hexdigest(), 'savedTfConfigMatchesCurrentSource':True, 'templateBinding':'External broker template matches private planning scratch; not embedded as a separate file in Terraform ZIP', 'changes':dict(Counter('/'.join(r['change']['actions']) for r in resources)), 'resourceTypes':dict(Counter(r['type'] for r in resources)), 'account':value('deployment_account_id'), 'region':value('deployment_region'), 'accessMode':value('access_mode'), 'quantities':q, 'costCases':cases, 'limits':['Local-backend preview; no remote state or apply', 'All seven secrets priced conservatively even before values are populated', 'Zero running app tasks and no visitor path in actual staging plan', 'Future five-task scenario is an estimate, not an activation plan', 'Exact-SHA verified images, secrets, bootstrap, owned hostname/issued certificate/CIDRs and new final plan required before activation', 'No cloud health, recovery, notification or deployment evidence']}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    for c in cases:
        if c['profile']=='expected': print(c['mode'], c['hours']+'h', f"${D(c['total_usd']):.2f}")
    print('Saved sanitized staging/cost review:',output)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan-json',required=True,type=Path)
    parser.add_argument('--plan-binary',required=True,type=Path)
    parser.add_argument('--report',required=True,type=Path)
    args=parser.parse_args()
    review(args.plan_json.resolve(),args.plan_binary.resolve(),args.report.resolve())
