#!/usr/bin/env python3
"""Local SG reasoning model: synthetic TCP flows, explicit route/NACL assumptions; no AWS."""
from copy import deepcopy
from ipaddress import ip_address, ip_network
import json
from pathlib import Path

RULES = Path(__file__).with_name('rules.json')
original = RULES.read_bytes()
config = json.loads(original)


class NetworkModel:
    """A deliberately partial teaching model; not an AWS SG/NACL engine."""

    def __init__(self, groups):
        self.groups = deepcopy(groups)
        self.established = set()

    @staticmethod
    def matches(rule, peer, direction, port):
        if rule['protocol'] != 'tcp' or rule['port'] != port:
            return False
        group_key = 'source_group' if direction == 'ingress' else 'destination_group'
        cidr_key = 'source_cidr' if direction == 'ingress' else 'destination_cidr'
        if group_key in rule:
            return peer == rule[group_key]
        if cidr_key in rule:
            try:
                return ip_address(peer) in ip_network(rule[cidr_key])
            except ValueError:
                return False
        return False

    def connect(self, source, target, port, source_port=55000,
                route_available=True, nacl_permits=True):
        # These flags are supplied assumptions: the lab does not discover routes or evaluate NACLs.
        if not route_available or not nacl_permits:
            return False
        incoming = any(self.matches(rule, source, 'ingress', port)
                       for rule in self.groups[target]['ingress'])
        outgoing = source not in self.groups or any(
            self.matches(rule, target, 'egress', port)
            for rule in self.groups[source]['egress'])
        if incoming and outgoing:
            self.established.add((source, source_port, target, port))
            return True
        return False

    def reply(self, source, source_port, target, target_port):
        return (target, target_port, source, source_port) in self.established


results = []
def check(name, actual, expected):
    assert actual is expected, f'{name}: expected {expected}, got {actual}'
    results.append({'name': name, 'status': 'PASS'})
    print('PASS', name)

model = NetworkModel(config['groups'])
check('approved documentation-range client reaches ALB HTTPS', model.connect('203.0.113.5','alb',443), True)
check('unapproved client is denied ALB HTTPS', model.connect('198.51.100.8','alb',443), False)
check('public SSH is denied', model.connect('203.0.113.5','alb',22), False)
check('internet database access is denied', model.connect('203.0.113.5','db',5432), False)
check('ALB group reaches application listener', model.connect('alb','app',8180), True)
check('external client cannot bypass ALB to application', model.connect('203.0.113.5','app',8180), False)
check('application reaches database', model.connect('app','db',5432), True)
check('SG references are not transitive: ALB cannot access database', model.connect('alb','db',5432), False)
check('established database reply needs no separate database outbound permission', model.reply('db',5432,'app',55000), True)
check('unsolicited database-to-app connection is denied', model.connect('db','app',55000), False)
check('SG permission does not create a missing route', model.connect('app','db',5432,route_available=False), False)
check('an explicit NACL veto still denies a new connection', model.connect('app','db',5432,nacl_permits=False), False)
no_egress = NetworkModel(config['groups']); no_egress.groups['app']['egress'] = []
check('source egress is required for a new application database connection', no_egress.connect('app','db',5432), False)
no_ingress = NetworkModel(config['groups']); no_ingress.groups['alb']['ingress'] = []
check('no ingress remains deny-by-default, not a reason to add public access', no_ingress.connect('203.0.113.5','alb',443), False)
assert RULES.read_bytes() == original, 'Lab must not mutate its rule source'
print(json.dumps({'passed':len(results),'failed':0,'aws_calls':0,'source_unchanged':True,
                  'limits':'Partial TCP permission model; no AWS attachment, actual routing/NACL evaluation, listeners, TLS, IAM, or application authorization tested.'}))
