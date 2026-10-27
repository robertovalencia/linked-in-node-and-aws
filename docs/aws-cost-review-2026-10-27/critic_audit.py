#!/usr/bin/env python3
"""Independent, credential-free audit of the saved cost packet; no AWS calls.

Reads the builders' exported quantities without importing or executing model.py.
Checks ledger integrity, independent topology counts, paired-network deltas,
replicated Kafka capacity, a closed-form baseline and displayed table totals.
Prints JSON evidence; does not change any source or model artifact.
"""
import hashlib
import json
import re
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rates = json.loads((ROOT / 'rates.json').read_text())
packet = json.loads((ROOT / 'comparison.json').read_text())
cases = packet['cases']
tol = D('1e-22')


def equal(actual, expected, context):
    assert abs(D(actual) - D(expected)) < tol, (context, actual, expected)


def price(key):
    return D(rates[key]['rate'])


def item(case, key):
    found = [x for x in case['items'] if x['rate_key'] == key]
    assert len(found) == 1, (case['option'], key, len(found))
    return found[0]


assert len(cases) == 42
assert len(packet['streaming']) == 6
assert set(x['hours'] for x in cases) == {'24', '720'}
index = {(x['option'], x['hours'], x['profile']): x for x in cases}
assert len(index) == 42

for c in cases:
    h = D(c['hours'])
    for x in c['items']:
        equal(x['usd'], D(x['quantity']) * price(x['rate_key']), (c['option'], x['meter']))
    equal(c['total_usd'], sum(D(x['usd']) for x in c['items']), c['option'])
    managed = c['option'].startswith('3')
    replicas = 2 if c['option'].startswith(('3r ', '3re ')) else 1
    nat = 'NAT' in c['option']
    endpoints = 'endpoints' in c['option']
    ips = (2 + (replicas if nat else 0)) if managed else 3 if c['option'].startswith('2 ') else 1
    equal(item(c, 'ipv4')['quantity'], ips * h, 'IPv4 topology')
    if managed:
        equal(item(c, 'fargate_cpu')['quantity'], D(5) * replicas * D('.25') * h, 'five distinct tasks CPU')
        equal(item(c, 'fargate_memory')['quantity'], D(5) * replicas * D('.5') * h, 'five distinct tasks RAM')
        equal(item(c, 'cloudmap_resource')['quantity'], D(5) * replicas * h / D(730), 'DNS task registrations')
        equal(item(c, 'route53_zone')['quantity'], 1 if h == 24 else 2, 'nonprorated DNS zone months')
        assert 'CloudMap' not in c['zero_scope']
        if nat:
            equal(item(c, 'nat_hour')['quantity'], replicas * h, 'NAT AZ multiplication')
        if endpoints:
            equal(item(c, 'endpoint_hour')['quantity'], 6 * replicas * h, 'endpoint AZ multiplication')
    p = {k: D(v) for k, v in packet['profiles'][c['profile']].items()}
    equal(c['lcu'], max(p['new_connections_s']/25, p['active_connections']/3000,
                        p['alb_gb_h'], p['rules_evaluated_s']/1000), 'largest LCU dimension')

# Closed-form baseline, independently using declared Ohio tariffs and quantities.
for h in (D(24), D(720)):
    baseline = h * (D('.09576') + D('.005') + D('.05') * D('.09')
                    + D(10) * D('.000005') + D(10) * D('.000005') + D(100) * D('.0000004'))
    baseline += h / D(730) * (D(40)*D('.08') + D('.4') + D(2)*D('.1') + D(2)*D('.023'))
    equal(index[('0 Current SSM baseline', str(h), 'expected')]['total_usd'], baseline, 'closed-form baseline')

# Pairwise network deltas cancel common compute/data/DNS costs.
break_even = []
for replicas, nat_name, ep_name in [
    (1, '3 Private ECS/RDS + one NAT', '3e Private ECS/RDS + six endpoints'),
    (2, '3r Two-AZ tasks/RDS + two NATs', '3re Two-AZ tasks/RDS + twelve endpoints')]:
    fixed = D(replicas) * (6 * price('endpoint_hour') - price('nat_hour') - price('ipv4'))
    break_even.append({'active_azs': replicas, 'equivalent_api_gb_per_hour': str(fixed/(price('nat_gb')-price('endpoint_gb')))})
    for h in (D(24), D(720)):
        for p, values in packet['profiles'].items():
            expected_delta = h * (fixed + D(values['network_gb_h']) * (price('endpoint_gb')-price('nat_gb')))
            equal(D(index[(ep_name,str(h),p)]['total_usd']) - D(index[(nat_name,str(h),p)]['total_usd']), expected_delta, 'paired NAT/endpoint delta')

for s in packet['streaming']:
    h = D(s['hours'])
    ingress = D(packet['profiles'][s['profile']]['network_gb_h'])
    logical = ingress * min(h, D(24))
    capacity = max(D(20), (logical * D('1.3') / 10).to_integral_value(rounding=ROUND_CEILING) * 10)
    equal(s['per_broker_gb'], capacity, 'full replica plus 30% headroom')
    for n in (2,3):
        total = D(n) * (h * price('msk_broker_t3_small') + capacity * h / D(730) * price('msk_gp2_storage'))
        equal(s[f'provisioned_{n}_brokers_usd'], total, 'replicated provisioned MSK')
    serverless = h*(D('.75')+6*D('.0015')) + ingress*h*(D('.1')+2*D('.05')) + logical*h/D(730)*D('.1')
    equal(s['serverless_usd'], serverless, 'independent Serverless formula')

for name in packet['options']:
    row = next(line for line in (ROOT/'tables.md').read_text().splitlines() if line.startswith('| '+name+' |'))
    displayed = [x.strip().lstrip('$') for x in row.split('|')[2:-1]]
    expected = [f"{D(index[(name,str(h),p)]['total_usd']):.2f}" for h in (24,720) for p in packet['profiles']]
    assert displayed == expected, (name, displayed, expected)

account = json.loads((ROOT/'account-summary.json').read_text())
assert account['plan']['accountPlanType'] == 'FREE'
assert account['plan']['accountPlanStatus'] == 'ACTIVE'
assert account['plan']['accountPlanRemainingCredits']['amount'] == 100
for denied in ('msk','oidc'):
    assert account['checks'][denied]['result'] == 'denied'
    assert 'SCP denial' in account['checks'][denied]['reason']
assert account['checks']['logs_ohio']['result'] == 'success'

plans = json.loads((ROOT/'baseline-plan-summary.json').read_text())
assert plans['approvalStatus'] == 'NOT APPROVED; NO APPLY'
assert plans['plans']['bootstrap']['changes'] == {'create':5}
dev = plans['plans']['aws-dev']
assert dev['changes'] == {'create':21}
assert dev['sgIngress'] == []
assert dev['mode'] == 'LOCAL BACKEND BASELINE PREVIEW ONLY'
assert dev['sourceFilesMatchRepository'] is True
assert dev['region'] == 'us-east-2' and dev['oidcCreated'] is False
# Only verify private binary hashes when the local-only files are available;
# this portable packet must not require those plans or ever apply them.
binary_hashes_checked = []
for name, plan in plans['plans'].items():
    private = Path(plan['path'])
    if private.exists():
        assert hashlib.sha256(private.read_bytes()).hexdigest() == plan['sha256']
        binary_hashes_checked.append(name)

sections = (ROOT/'line-items.md').read_text().split('\n## ')[1:]
assert len(sections) == 7
for section in sections:
    name = section.splitlines()[0]
    totals = re.search(r'\| \*\*Total\*\* \| \| \*\*\$(.*?)\*\* \| \*\*\$(.*?)\*\* \|', section)
    assert totals, name
    for h, shown in zip((24,720), totals.groups()):
        assert shown == f"{D(index[(name,str(h),'expected')]['total_usd']):.2f}"
for filename in ('README.md','critic.md'):
    for link in re.findall(r'\]\(([^)]+)\)', (ROOT/filename).read_text()):
        if '://' not in link:
            assert (ROOT/link.split('#')[0]).exists(), (filename,link)

hashed = ['model.py','rates.json','comparison.json','tables.md','line-items.md',
          'account-summary.json','baseline-plan-summary.json','architecture.md','README.md','critic.md']
print(json.dumps({
    'status': 'PASS', 'platform_cases': len(cases), 'streaming_cases': len(packet['streaming']),
    'checks': ['all item products and ledger sums', 'closed-form expected baseline',
               'IPv4/task/NAT/endpoint/DNS topology quantities', 'maximum ALB LCU dimension',
               'paired equivalent-traffic NAT/endpoint deltas', 'replicated MSK capacity and service cost',
               'displayed comparison/itemized totals and local links', 'current Free-plan and explicit-denial evidence',
               'baseline preview scope/zero ingress and available private plan hashes'],
    'decimal_tolerance_usd': str(tol), 'network_break_even': break_even,
    'private_plan_binary_hashes_checked': binary_hashes_checked,
    'limits': ['No cloud provisioning or runtime test', 'No capacity/throughput proof',
               'Account reads do not verify create grants', 'Totals exclude explicitly named optional add-ons'],
    'sha256': {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in hashed}
}, indent=2))
