#!/usr/bin/env python3
"""Gross Ohio list-price scenarios, not a quote, invoice, or provisioning tool.

python3 model.py writes comparison.json and tables.md alongside this file.
All money arithmetic is Decimal; quantities are explicit and freely editable.
"""
import json
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RATES = json.loads((ROOT / 'rates.json').read_text())
MONTH_HOURS = D('730')  # GB/month and metric/month normalization only
PROFILES = {
    'idle': dict(log_gb_h='0.001', network_gb_h='0.01', out_gb_h='0.001',
                 cross_az_gb_h='0', new_connections_s='0.01', active_connections='5',
                 alb_gb_h='0.001', rules_evaluated_s='0', requests_h='10',
                 excess_backup_gb='0', cpu_surplus_vcpu_h='0'),
    'expected': dict(log_gb_h='0.04', network_gb_h='0.25', out_gb_h='0.05',
                     cross_az_gb_h='0.05', new_connections_s='1', active_connections='100',
                     alb_gb_h='0.1', rules_evaluated_s='0', requests_h='3600',
                     excess_backup_gb='5', cpu_surplus_vcpu_h='0'),
    'higher': dict(log_gb_h='0.5', network_gb_h='5', out_gb_h='1',
                   cross_az_gb_h='1', new_connections_s='50', active_connections='1000',
                   alb_gb_h='2', rules_evaluated_s='0', requests_h='180000',
                   excess_backup_gb='20', cpu_surplus_vcpu_h='0.5'),
}
# This is scenario comparison, NOT desired Terraform configuration.
OPTIONS = {
    '0 Current SSM baseline': dict(edge=False, harden=False, managed=False, network=None),
    '1 Hardened SSM host': dict(edge=False, harden=True, managed=False, network=None),
    '2 ALB HTTPS + same host': dict(edge=True, harden=True, managed=False, network=None),
    '3 Private ECS/RDS + one NAT': dict(edge=True, harden=True, managed=True, network='nat'),
    '3e Private ECS/RDS + six endpoints': dict(edge=True, harden=True, managed=True, network='endpoints'),
    '3r Two-AZ tasks/RDS + two NATs': dict(edge=True, harden=True, managed=True, network='nat', replicas=2),
    '3re Two-AZ tasks/RDS + twelve endpoints': dict(edge=True, harden=True, managed=True, network='endpoints', replicas=2),
}

def rate(key):
    return D(RATES[key]['rate'])

def scenario(name, hours, profile):
    h = D(hours)
    p = {k: D(v) for k, v in PROFILES[profile].items()}
    o = OPTIONS[name]
    multi = o.get('replicas', 1)
    managed, edge, harden = o['managed'], o['edge'], o['harden']
    items = []

    def add(label, key, quantity, units, note=''):
        q = D(quantity)
        items.append(dict(meter=label, rate_key=key, quantity=str(q), units=units,
                          usd=str(q * rate(key)), note=note))

    # Current one host; for managed variants, retain the SAME conservative size
    # as a dedicated private Kafka host. Do not silently remove Kafka's cost.
    add('EC2 application host' if not managed else 'EC2 Kafka host (single point of failure)',
        'ec2_host', h, 'host-hours', 'm7i-flex.large, Linux x86; retained size is conservative, not benchmarked')
    add('EC2 root gp3', 'ebs_gp3', D(40) * h / MONTH_HOURS, 'GB-month')
    if managed:
        add('Cloud Map registered task resources', 'cloudmap_resource', D(5)*multi*h/MONTH_HOURS, 'resource-month', 'ECS service discovery in one private DNS namespace; no proxy sidecars')
        add('Private DNS hosted zone', 'route53_zone', D(1 if h <= 24 else 2), 'zone-month-charges', 'Nonprorated: one charge for 24h, conservatively two calendar-month charges for a 30-day run starting near month end')
        add('Cloud Map API discovery requests', 'cloudmap_lookup', 0, 'requests', 'Clients use DNS instead; private Route53 queries have no additional charge under current Route53 tariff')
        add('Fargate CPU: five tasks per replica', 'fargate_cpu', D('1.25') * multi * h, 'vCPU-hours')
        add('Fargate RAM: five tasks per replica', 'fargate_memory', D('2.5') * multi * h, 'GB-hours')
        add('Fargate additional ephemeral storage', 'fargate_extra_disk', 0, 'GB-hours', '20 GiB included per task; no durable DB/Kafka on ephemeral disks')
        add('RDS PostgreSQL db.t4g.small', 'rds_small_multi' if multi == 2 else 'rds_small_single', h, 'instance-hours', 'Four databases/roles on one physical primary; Multi-AZ standby when replicas=2')
        add('RDS 20 GiB gp3', 'rds_gp3_multi' if multi == 2 else 'rds_gp3_single', D(20) * h / MONTH_HOURS, 'GB-month', 'Multi-AZ rate already includes both copies; do not double count')
        add('RDS excess backups', 'rds_backup', p['excess_backup_gb'] * h / MONTH_HOURS, 'GB-month', 'Explicit chargeable GB above regional running-DB allowance, not total snapshot size')
        add('RDS burst CPU surplus', 'rds_cpu_surplus', p['cpu_surplus_vcpu_h'] * h * multi, 'vCPU-hours', 'Higher case surcharge assumption; observe credits, not a performance prediction')
        if o['network'] == 'nat':
            add('NAT gateway AZ-hours', 'nat_hour', h * multi, 'AZ-hours')
            add('NAT data processed', 'nat_gb', p['network_gb_h'] * h, 'GB', 'Excludes S3 gateway traffic and inbound ALB path')
        else:
            add('Six interface endpoints per active AZ', 'endpoint_hour', D(6) * multi * h, 'endpoint-AZ-hours', 'ECR api/dkr, Logs, Secrets, SSM, ssmmessages; S3 gateway free')
            add('Interface endpoint data processed', 'endpoint_gb', p['network_gb_h'] * h, 'GB', 'Only equivalent AWS API traffic; no general internet access')
        add('Billable cross-AZ data (two charged sides)', 'cross_az', D(2) * p['cross_az_gb_h'] * h, 'side-GB', 'Conservative app/DB/Kafka traffic allowance; excludes exempt ALB-to-target and RDS standby replication')
    ips = (2 + (multi if o['network'] == 'nat' else 0)) if managed else (3 if edge else 1)
    add('Public IPv4', 'ipv4', D(ips) * h, 'address-hours', 'ALB minimum two; NAT one/AZ; private tasks/DB/Kafka no public IP; existing host one')
    lcu = max(p['new_connections_s'] / D(25), p['active_connections'] / D(3000),
              p['alb_gb_h'], p['rules_evaluated_s'] / D(1000))
    if edge:
        add('ALB hourly', 'alb_hour', h, 'ALB-hours')
        add('ALB maximum LCU dimension', 'alb_lcu', lcu * h, 'LCU-hours', 'No reserved LCUs; <=10 rules, ordinary certificate sizes, no mTLS trust store')
    secrets = 5 if managed else 1
    add('Secrets Manager storage', 'secrets_store', D(secrets) * h / MONTH_HOURS, 'secret-month', 'Managed: one credential secret/capability plus shared signing/event configuration')
    add('Secrets Manager API', 'secrets_api', D(10) * secrets * h, 'requests', 'Conservative 10 requests/secret/hour; applications should cache and never log values')
    add('ECR images', 'ecr_storage', D(2) * h / MONTH_HOURS, 'GB-month', 'Two GB combined repos including rollback images; basic scanning, not paid Inspector')
    add('S3 releases/state/backups', 's3_storage', D(10 if harden else 2) * h / MONTH_HOURS, 'GB-month', 'Versions count; hardened includes logical backups; no archive minimum-storage class')
    add('S3 PUT/LIST', 's3_put', D(10) * h, 'requests')
    add('S3 GET', 's3_get', D(100) * h, 'requests')
    if harden:
        ingest = p['log_gb_h'] * h
        # Upper bound: charge retention window's full occupied size throughout.
        stored = p['log_gb_h'] * min(h, D(168))
        add('CloudWatch standard logs ingest', 'cloudwatch_logs_ingest', ingest, 'GB', 'App/system/audit/flow log total; no payloads/tokens; Free allowance not deducted')
        add('CloudWatch logs seven-day retention', 'cloudwatch_logs_store', stored * h / MONTH_HOURS, 'GB-month', 'Uncompressed upper bound with immediate-full-window storage; real billed compressed volume varies')
        add('Logs Insights queries', 'cloudwatch_logs_query', D(5) * ingest, 'GB scanned', 'Five times ingest volume queried during period')
        add('CloudWatch custom metrics', 'cloudwatch_metric', D(8 if managed else 3) * h / MONTH_HOURS, 'metric-month', 'Low-cardinality agent memory/disk + outbox/consumer metrics; detailed/container insights off')
        add('CloudWatch standard alarms', 'cloudwatch_alarm_standard', D(10 if managed else 5) * h / MONTH_HOURS, 'alarm-metric-month', 'No composite/high-resolution alarms; notification delivery extra')
    add('Internet egress, first paid tier', 'internet_out', p['out_gb_h'] * h, 'GB', 'Gross before any shared 100GB/month allowance; transfer in free; not NAT processing')
    # These explicitly unused services have no cost in the selected comparisons.
    total = sum(D(x['usd']) for x in items)
    return dict(option=name, hours=str(h), profile=profile, lcu=str(lcu),
                total_usd=str(total), items=items,
                zero_scope=['WAF', 'customer-managed KMS keys', 'GuardDuty/Inspector/Security Hub/Config',
                            'MSK', 'new public DNS zone/domain (managed private zone included)', 'EFS', 'RDS Proxy',
                            'CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces',
                            'EBS snapshots (logical backups modeled in S3 instead)', 'extra gp3 IOPS/throughput'])

def streaming(hours, profile):
    h = D(hours)
    p = {k: D(v) for k, v in PROFILES[profile].items()}
    # One topic with six OPEN partitions for learning, not a measured requirement.
    # Serverless stores logical bytes; provisioned capacity is per broker.
    retained_gb = p['network_gb_h'] * min(h, D(24))
    # RF equals broker count in these teaching alternatives, so each broker
    # holds one complete logical copy. Reserve 30% headroom, rounded to 10GiB.
    per_broker_gb = max(D(20), (retained_gb*D('1.3')/D(10)).to_integral_value(rounding=ROUND_CEILING)*D(10))
    provisioned2 = D(2)*rate('msk_broker_t3_small')*h + D(2)*per_broker_gb*rate('msk_gp2_storage')*h/MONTH_HOURS
    provisioned3 = D(3)*rate('msk_broker_t3_small')*h + D(3)*per_broker_gb*rate('msk_gp2_storage')*h/MONTH_HOURS
    serverless = (rate('msk_serverless_cluster')*h + D(6)*rate('msk_serverless_partition')*h
                  + p['network_gb_h']*h*rate('msk_serverless_in')
                  + D(2)*p['network_gb_h']*h*rate('msk_serverless_out')
                  + retained_gb*rate('msk_serverless_storage')*h/MONTH_HOURS)
    removed_host = rate('ec2_host')*h + D(40)*rate('ebs_gp3')*h/MONTH_HOURS
    return dict(hours=str(h), profile=profile, per_broker_gb=str(per_broker_gb), retained_logical_gb=str(retained_gb), provisioned_2_brokers_usd=str(provisioned2),
                provisioned_3_brokers_usd=str(provisioned3), serverless_usd=str(serverless),
                removed_private_kafka_host_usd=str(removed_host),
                phase3_provisioned_2_broker_delta_usd=str(provisioned2-removed_host),
                note='MSK Paid-plan-only in current project experience; excluded from platform totals. Logs/network extra. No provisioned throughput surcharge on small brokers. t3 burst limits not throughput guarantee.')

def money(x):
    return f'${D(x):.2f}'

def main():
    cases=[scenario(n,h,p) for n in OPTIONS for h in [24,720] for p in PROFILES]
    stream=[streaming(h,p) for h in [24,720] for p in PROFILES]
    output=dict(date='2026-10-27', region='us-east-2', currency='USD',
                monthly_rate_normalization_hours=str(MONTH_HOURS),
                profiles=PROFILES, options=OPTIONS, cases=cases, streaming=stream)
    (ROOT/'comparison.json').write_text(json.dumps(output,indent=2)+'\n')
    lines=['# Calculated comparison','',
           'Gross list-price estimates; workload assumptions, not capacity or invoice predictions.',
           '30 days = 720 running hours; monthly storage/metric rates normalized over 730 hours.', '',
           '| Option | 24h idle | 24h expected | 24h higher | 30d idle | 30d expected | 30d higher |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for n in OPTIONS:
        row=[money(c['total_usd']) for c in cases if c['option']==n]
        lines.append('| '+n+' | '+' | '.join(row)+' |')
    lines += ['', '## Optional streaming service only', '',
              '| Duration/profile | GiB per broker | Two small brokers + storage | Three small brokers + storage | Serverless six partitions + bytes |',
              '|---|---:|---:|---:|---:|---:|']
    for s in stream:
        lines.append('| '+s['hours']+'h '+s['profile']+' | '+s['per_broker_gb']+' | '+money(s['provisioned_2_brokers_usd'])+' | '+money(s['provisioned_3_brokers_usd'])+' | '+money(s['serverless_usd'])+' |')
    (ROOT/'tables.md').write_text('\n'.join(lines)+'\n')
    detail=['# Itemized expected-use estimates', '',
            'Generated from the exact ledger. USD gross; no credits/shared free allowances deducted.',
            '24h and 720h runtime; 730h normalization for proratable monthly meters. Zone fees are nonprorated.']
    for n in OPTIONS:
        a=next(c for c in cases if c['option']==n and c['hours']=='24' and c['profile']=='expected')
        b=next(c for c in cases if c['option']==n and c['hours']=='720' and c['profile']=='expected')
        detail += ['', '## '+n, '', '| Meter | 24h quantity | 24h USD | 30d USD |', '|---|---:|---:|---:|']
        for x,y in zip(a['items'],b['items']):
            detail.append(f"| {x['meter']} | {D(x['quantity']):.4f} {x['units']} | {D(x['usd']):.5f} | {D(y['usd']):.5f} |")
        detail.append(f"| **Total** | | **{money(a['total_usd'])}** | **{money(b['total_usd'])}** |")
        detail += ['', 'Unused paid categories: '+', '.join(a['zero_scope'])+'.']
    (ROOT/'line-items.md').write_text('\n'.join(detail)+'\n')
    print('\n'.join(lines))

if __name__=='__main__':
    main()
