#!/usr/bin/env python3
"""Disposable Docker discovery drill. No AWS calls or marketplace data changes."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time
import urllib.request
import os


def main(image, output):
    prefix = f'marketplace-dns-drill-{os.getpid()}'
    network, backend, edge, blocker = [prefix + suffix for suffix in ('-net', '-api', '-edge', '-block')]
    checks = []
    def run(*args, check=True):
        return subprocess.run(['docker', *args], capture_output=True, text=True, check=check, timeout=60)
    def api(marker):
        code = "require('http').createServer((q,s)=>{s.setHeader('content-type','application/json');s.end(JSON.stringify({marker:process.env.MARKER,host:q.headers.host}))}).listen(8182,'0.0.0.0')"
        run('run', '-d', '--name', backend, '--network', network, '--network-alias', 'catalog.lab.internal', '-e', f'MARKER={marker}', '--entrypoint', 'node', 'linked-in-node/backend:local', '-e', code)
    def fetch(port):
        req = urllib.request.Request(f'http://127.0.0.1:{port}/api/providers', headers={'Host': 'demo.invalid'})
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.load(response)
    def wait(port, marker):
        deadline = time.monotonic() + 35
        while time.monotonic() < deadline:
            try:
                body = fetch(port)
                if body == {'marker': marker, 'host': 'demo.invalid'}:
                    return
            except (OSError, ValueError):
                pass
            time.sleep(1)
        raise RuntimeError('DNS proxy did not return the expected replacement backend and Host header')
    try:
        run('network', 'create', '--subnet', f'198.19.{os.getpid() % 250}.0/24', '--label', 'purpose=marketplace-local-dns-drill', network)
        api('before')
        env = []
        for name in ('IDENTITY', 'CATALOG', 'INQUIRIES', 'NOTIFICATIONS'):
            env += ['-e', f'{name}_UPSTREAM=catalog.lab.internal']
        run('run', '-d', '--name', edge, '--network', network, '-p', '127.0.0.1::8180', *env, image)
        port = run('port', edge, '8180/tcp').stdout.strip().rsplit(':', 1)[1]
        wait(port, 'before')
        checks.append({'name': 'configured_private_dns_and_preserved_nginx_host_variable', 'status': 'PASS'})
        old_ip = json.loads(run('inspect', backend).stdout)[0]['NetworkSettings']['Networks'][network]['IPAddress']
        run('rm', '-f', backend)
        # Occupy the previous address to prove recovery follows DNS, not IP reuse.
        run('run', '-d', '--name', blocker, '--network', network, '--ip', old_ip, '--entrypoint', 'sleep', 'linked-in-node/backend:local', '120')
        api('after')
        new_ip = json.loads(run('inspect', backend).stdout)[0]['NetworkSettings']['Networks'][network]['IPAddress']
        assert new_ip != old_ip
        wait(port, 'after')
        checks.append({'name': 'proxy_recovers_when_backend_ip_changes', 'status': 'PASS'})
        for label, key, value in [('upstream_config_injection', 'CATALOG_UPSTREAM', 'catalog; return 200 injected;'), ('resolver_config_injection', 'DNS_RESOLVER', '127.0.0.11;'), ('invalid_resolver_octet', 'DNS_RESOLVER', '300.0.0.1')]:
            result = run('run', '--rm', '--network', network, '-e', f'{key}={value}', image, check=False)
            assert result.returncode != 0 and ('Invalid' in result.stderr or 'DNS_RESOLVER' in result.stderr), label
            checks.append({'name': label, 'status': 'PASS'})
    finally:
        for name in (edge, backend, blocker):
            run('rm', '-f', name, check=False)
        run('network', 'rm', network, check=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {'timestamp': datetime.now(timezone.utc).isoformat(), 'scope': 'Local disposable Docker DNS; no AWS execution', 'frontendImage': image, 'passed': len(checks), 'failed': 0, 'checks': checks}
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'Frontend private DNS drill: {len(checks)} passed, 0 failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend-image', required=True, help='Image built from the source being verified')
    parser.add_argument('--report', type=Path, default=Path('work/aws-ecs-preparation/frontend-dns.json'))
    args = parser.parse_args()
    main(args.frontend_image, args.report)
