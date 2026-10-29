#!/usr/bin/env python3
"""Visible, private AWS preparation commands. Never applies, destroys or logs in."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('Operator preparation refuses Python optimization')

ROOT = Path(__file__).resolve().parents[1]
ACCOUNT = '772641336063'
REGION = 'us-east-2'
PROFILE = 'marketplace-dev'
BUCKET = ACCOUNT + '-linked-in-node-terraform-state'
STATE_KEY = 'linked-in-node/ecs-dev/terraform.tfstate'
NAME = 'linked-in-node-ecs-dev'
BACKEND = {
    'account': ACCOUNT, 'region': REGION, 'bucket': BUCKET, 'key': STATE_KEY,
    'workspace': 'default', 'encrypt': True, 'useLockfile': True,
    'allowedAccountIds': [ACCOUNT],
    'workspaceKeyPrefix': 'linked-in-node/ecs-dev/workspaces',
}


class Stop(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Stop(message)


def private_file(value):
    path = Path(value).resolve()
    require(path.is_file(), 'Required private file is missing: ' + str(path))
    try:
        path.relative_to(ROOT / 'work')
    except ValueError:
        raise Stop('Private inputs and plans must remain under this repository work directory')
    info = path.stat()
    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) & 0o077 == 0,
            'Private input must be owner-only: ' + str(path))
    return path


def cleaned_environment():
    result = dict(os.environ)
    names = {
        'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN',
        'AWS_SECURITY_TOKEN', 'AWS_ROLE_ARN', 'AWS_WEB_IDENTITY_TOKEN_FILE',
        'AWS_ROLE_SESSION_NAME', 'AWS_CONTAINER_CREDENTIALS_FULL_URI',
        'AWS_CONTAINER_CREDENTIALS_RELATIVE_URI', 'AWS_CONTAINER_AUTHORIZATION_TOKEN',
        'AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE', 'AWS_DEFAULT_PROFILE',
        'AWS_CONFIG_FILE', 'AWS_SHARED_CREDENTIALS_FILE', 'PYTHONOPTIMIZE',
        'TF_WORKSPACE', 'TF_DATA_DIR', 'TF_CLI_CONFIG_FILE', 'TF_LOG', 'TF_LOG_PATH', 'TF_LOG_CORE', 'TF_LOG_PROVIDER',
    }
    for name in list(result):
        if name in names or name.startswith(('TF_CLI_ARGS', 'TF_VAR_', 'AWS_ENDPOINT_URL')):
            result.pop(name)
    result.update(AWS_PROFILE=PROFILE, AWS_REGION=REGION, AWS_DEFAULT_REGION=REGION,
                  AWS_PAGER='', TF_IN_AUTOMATION='1', TF_INPUT='0')
    return result


def contexts(args):
    s3 = private_file(args.s3_backend_context)
    https = private_file(args.https_context)
    require(json.dumps(json.loads(s3.read_text()), sort_keys=True) == json.dumps(BACKEND, sort_keys=True),
            'Unreviewed S3 backend context')
    context = json.loads(https.read_text())
    require(context.get('account') == ACCOUNT and context.get('region') == REGION,
            'Unexpected HTTPS account or region')
    require(context.get('certificateStatus') == 'ISSUED', 'Certificate context is not issued')
    require(context.get('applicationHostname') == 'app.linked-in-node-rv.dynv6.net',
            'Unexpected application hostname')
    require(re.fullmatch(r'arn:aws:acm:us-east-2:' + ACCOUNT + r':certificate/[a-f0-9-]+',
                         context.get('certificateArn', '')) is not None,
            'Unexpected certificate identity')
    cidrs = context.get('approvedClientCidrs', [])
    require(len(cidrs) == 1, 'Exactly one approved client is required')
    network = ipaddress.ip_network(cidrs[0], strict=True)
    require(network.version == 4 and network.prefixlen == 32, 'An approved IPv4 /32 is required')
    return https, s3, context


def check_backend():
    cache = ROOT / 'infra/aws-ecs-dev/.terraform/terraform.tfstate'
    require(cache.is_file(), 'Actual S3 backend must already be initialized; bootstrap/init are not automated here')
    value = json.loads(cache.read_text()).get('backend', {})
    expected = {'bucket': BUCKET, 'key': STATE_KEY, 'region': REGION, 'encrypt': True,
                'use_lockfile': True, 'allowed_account_ids': [ACCOUNT],
                'workspace_key_prefix': BACKEND['workspaceKeyPrefix']}
    require(value.get('type') == 's3', 'Initialized backend must be S3')
    config = value.get('config', {})
    for key, setting in expected.items():
        require(key in config and type(config[key]) is type(setting) and config[key] == setting,
                'Initialized backend differs: ' + key)
    require(all(setting is None for key, setting in config.items() if key not in expected),
            'Unreviewed initialized backend option or cached credentials')
    require(not list((ROOT / 'infra/aws-ecs-dev').glob('*.tfstate*')),
            'Unexpected local application state; reconcile before continuing')
    require(not (ROOT / 'infra/aws-ecs-dev/backend_override.tf').exists(),
            'A backend override cannot be used by the actual S3 operator')


class Session:
    def __init__(self, directory):
        path = Path(directory).absolute()
        base = ROOT / 'work/aws-operator-preparation-2026-10-29'
        try:
            path.resolve().relative_to(base.resolve())
        except ValueError:
            raise Stop('Transcript directory must be under work/aws-operator-preparation-2026-10-29')
        require(path.resolve() != base.resolve(), 'Use a new named run directory beneath the private base')
        require(not path.exists(), 'Refusing to overwrite an existing transcript/run directory')
        require(not any(p.is_symlink() for p in [path, *path.parents]), 'Transcript paths cannot contain symlinks')
        os.umask(0o077)
        path.mkdir(mode=0o700, parents=True)
        path.chmod(0o700)
        self.directory = path.resolve()
        self.transcript = self.directory / 'transcript.txt'
        self.steps = []
        self.env = cleaned_environment()
        self.say('PREPARATION ONLY: no apply, destroy, login, secret reads or application provisioning.')
        self.say('Runtime AWS_PROFILE=' + PROFILE + ' AWS_REGION=' + REGION + '; conflicting credential/Terraform override variables cleared.')

    def say(self, text):
        print(text, flush=True)
        with self.transcript.open('a') as stream:
            stream.write(text + '\n')
        self.transcript.chmod(0o600)

    def save(self, status, detail=''):
        result = {'status': status, 'detail': detail,
                  'recordedAt': datetime.now(timezone.utc).isoformat(),
                  'scope': 'PREPARATION_ONLY_NOT_APPLY_APPROVAL', 'steps': self.steps}
        target = self.directory / 'steps.json'
        target.write_text(json.dumps(result, indent=2) + '\n')
        target.chmod(0o600)

    def run(self, command, purpose, cwd=None, redact=False, accepted=(0,)):
        command = [str(x) for x in command]
        working_directory = Path(cwd or ROOT).resolve()
        self.say('\n' + purpose)
        self.say('Working directory: ' + str(working_directory))
        self.say('$ ' + shlex.join(command))
        started = time.monotonic()
        try:
            result = subprocess.run(command, cwd=working_directory, env=self.env,
                                    text=True, capture_output=True, timeout=600)
        except (OSError, subprocess.TimeoutExpired) as error:
            self.steps.append({'purpose': purpose, 'command': command, 'workingDirectory': str(working_directory), 'status': 'EXECUTION_FAILED'})
            raise Stop('Command could not complete: ' + type(error).__name__)
        if redact:
            self.say('[response suppressed; private result processed without echoing]')
        else:
            if result.stdout.strip(): self.say(result.stdout.rstrip())
            if result.stderr.strip(): self.say(result.stderr.rstrip())
        self.steps.append({'purpose': purpose, 'command': command, 'workingDirectory': str(working_directory), 'expectedExitCodes': list(accepted), 'exitCode': result.returncode,
                           'seconds': round(time.monotonic() - started, 3),
                           'responseRedacted': redact})
        self.save('RUNNING')
        require(result.returncode in accepted, 'Command failed; no subsequent commands ran: ' + shlex.join(command))
        return result

    def aws(self, arguments, purpose, accepted=(0,)):
        endpoint_region = 'us-east-1' if arguments[0] == 'freetier' else REGION
        return self.run(['aws', *arguments, '--region', endpoint_region, '--output', 'json'],
                        purpose, accepted=accepted)


def preflight(session, context):
    check_backend()
    result = session.aws(['sts', 'get-caller-identity', '--query', '{Account:Account}'],
                         '1. Confirm the actual AWS account with the same environment used by Terraform.')
    require(json.loads(result.stdout).get('Account') == ACCOUNT, 'Wrong AWS account; stopped before planning')
    session.aws(['freetier', 'get-account-plan-state'],
                '2. Read current plan/credits; the result is not a spending cap or service eligibility guarantee.')
    workspace = session.run(['terraform', 'workspace', 'show'],
                            '3. Verify the initialized default ECS workspace.', ROOT / 'infra/aws-ecs-dev')
    require(workspace.stdout.strip() == 'default', 'Only the default reviewed workspace is allowed')
    result = session.aws(['s3api', 'head-object', '--bucket', BUCKET, '--key', STATE_KEY,
                          '--expected-bucket-owner', ACCOUNT],
                         '4. Require no existing application state before first provisioning.', accepted=(0, 254, 255))
    require(result.returncode != 0 and '(404)' in result.stderr,
            'Application state is present or unreadable; reconcile it instead of creating a duplicate stack')
    result = session.aws(['acm', 'describe-certificate', '--certificate-arn', context['certificateArn'],
                          '--query', 'Certificate.{Status:Status,DomainName:DomainName,Export:Options.Export}'],
                         '5. Verify the real certificate identity, issued status and nonexportable setting.')
    certificate = json.loads(result.stdout)
    require(certificate.get('Status') == 'ISSUED' and certificate.get('DomainName') == context['applicationHostname']
            and certificate.get('Export') == 'DISABLED', 'Real certificate does not match the reviewed context')
    result = session.aws(['ecs', 'describe-clusters', '--clusters', NAME],
                         '6. Check the exact proposed ECS cluster is absent (not a complete account inventory).')
    clusters = json.loads(result.stdout)
    require(not clusters.get('clusters') and len(clusters.get('failures', [])) == 1
            and clusters['failures'][0].get('reason') == 'MISSING', 'Named ECS cluster exists or absence is unproved')
    for service, operation, key, error, purpose in [
        ('rds', 'describe-db-instances', '--db-instance-identifier', 'DBInstanceNotFound', 'RDS instance'),
        ('elbv2', 'describe-load-balancers', '--names', 'LoadBalancerNotFound', 'ALB'),
    ]:
        result = session.aws([service, operation, key, NAME],
                             'Check the exact proposed ' + purpose + ' is absent.', accepted=(0, 254, 255))
        require(result.returncode != 0 and error in result.stderr, purpose + ' exists or absence is unproved')
    result = session.aws(['ec2', 'describe-vpcs', '--filters', 'Name=tag:Project,Values=linked-in-node',
                          'Name=tag:Environment,Values=ecs-dev', '--query', 'Vpcs[].VpcId'],
                         'Check the project-tagged VPC scope is empty; the unrelated default VPC is preserved.')
    require(json.loads(result.stdout) == [], 'Project VPC already exists; reconcile before initial planning')
    result = session.run(['curl', '--fail', '--silent', '--show-error', '--max-time', '15',
                          'https://checkip.amazonaws.com'],
                         '7. Compare current client egress to the approved /32 without displaying the address.', redact=True)
    require(ipaddress.ip_address(result.stdout.strip()) in ipaddress.ip_network(context['approvedClientCidrs'][0]),
            'Current client differs from the approved /32. Ask for a new explicitly approved CIDR; do not broaden access.')
    session.say('PASS: current client matches the existing approved /32; address omitted from transcript.')
    session.say('PASS: scoped first-deployment preflight. This does not prove create permissions, capacity or application health.')


def initial_inputs(path, context):
    value = json.loads(private_file(path).read_text())
    required = {'region': REGION, 'project': 'linked-in-node', 'owner': 'robertovalencia',
                'approved_client_cidrs': context['approvedClientCidrs'],
                'application_hostname': context['applicationHostname'], 'certificate_arn': context['certificateArn'],
                'deploy_application': False, 'image_digests': None, 'seed_demo': False, 'protect_database': True}
    for key, expected in required.items():
        require(key in value and type(value[key]) is type(expected) and value[key] == expected,
                'Unreviewed first-stage input: ' + key)
    require(value.get('teardown_discard_demo_data', False) is False,
            'Cleanup mode is forbidden in the initial infrastructure plan')
    allowed = set(required) | {'expires_at', 'kafka_image', 'postgres_engine_version',
                               'recovery_snapshot_suffix', 'notification_topic_arn', 'teardown_discard_demo_data'}
    require(not (set(value) - allowed), 'Unexpected input fields; credentials or unreviewed variables are forbidden')
    require(value.get('notification_topic_arn') is None, 'Alarm destination requires its own reviewed change')
    require(re.fullmatch(r'apache/kafka:[0-9.]+@sha256:[a-f0-9]{64}', value.get('kafka_image', '')) is not None,
            'Broker image must be digest pinned')
    require(value.get('postgres_engine_version') == '17.6', 'This command set reviews the tested/orderable PostgreSQL17.6 pin')
    deadline = datetime.fromisoformat(value.get('expires_at', '').replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    require(deadline.tzinfo is not None and deadline.utcoffset() == timedelta(0)
            and now < deadline <= now + timedelta(hours=48), 'Expiry proposal must be future UTC within48hours; it is not a shutdown scheduler')
    return value


def review(session, args, binary, plan_json, expected_sha, https, s3):
    binary, plan_json = private_file(binary), private_file(plan_json)
    require(hashlib.sha256(binary.read_bytes()).hexdigest() == expected_sha, 'Saved plan SHA256 differs')
    rates = Path(args.rates_file).resolve()
    require(rates.is_file(), 'Current official rates file is required')
    report = session.directory / 'review.json'
    session.run([sys.executable, ROOT / 'scripts/aws-ecs-review-plan.py',
                 '--plan-json', plan_json, '--plan-binary', binary, '--https-context', https,
                 '--s3-backend-context', s3, '--rates-file', rates, '--report', report],
                'Run the existing strict actual saved-backend/source/security/cost reviewer; this is not approval.')
    result = json.loads(report.read_text())
    require(result.get('planBinarySha256') == expected_sha
            and result.get('status') == 'S3_BACKED_HTTPS_INFRASTRUCTURE_PLAN_REVIEWED_NOT_APPROVED',
            'Reviewer receipt does not describe this exact actual S3 plan')
    session.say('Plan SHA256: ' + expected_sha)
    session.say('STOP before apply: separate exact-plan/current-cost/lifetime/cleanup approval is required.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest='command', required=True)
    for command in ['preflight', 'review', 'plan']:
        item = subcommands.add_parser(command)
        item.add_argument('--run-directory', required=True, type=Path,
                          help='NEW private directory below work/aws-operator-preparation-2026-10-29')
        item.add_argument('--https-context', required=True, type=Path)
        item.add_argument('--s3-backend-context', required=True, type=Path)
        if command != 'preflight': item.add_argument('--rates-file', required=True, type=Path)
        if command == 'review':
            item.add_argument('--plan-binary', required=True, type=Path)
            item.add_argument('--plan-json', required=True, type=Path)
            item.add_argument('--expected-sha256', required=True)
        if command == 'plan': item.add_argument('--inputs', required=True, type=Path)
    args = parser.parse_args(argv)
    session = None
    try:
        https, s3, context = contexts(args)
        check_backend()
        if args.command == 'plan': initial_inputs(args.inputs, context)
        session = Session(args.run_directory)
        if args.command in ['preflight', 'plan']: preflight(session, context)
        if args.command == 'review':
            require(re.fullmatch(r'[a-f0-9]{64}', args.expected_sha256) is not None, 'Expected SHA256 is invalid')
            review(session, args, args.plan_binary, args.plan_json, args.expected_sha256, https, s3)
        elif args.command == 'plan':
            inputs = session.directory / 'inputs.tfvars.json'
            shutil.copyfile(private_file(args.inputs), inputs)
            inputs.chmod(0o600)
            binary, plan_json = session.directory / 'application.tfplan', session.directory / 'plan.json'
            require(not binary.exists() and not plan_json.exists(), 'Refusing to overwrite plan evidence')
            shutil.copyfile(ROOT / 'infra/aws-ecs-dev/kafka-user-data.sh.tftpl',
                            session.directory / 'kafka-user-data.sh.tftpl')
            session.run(['terraform', 'plan', '-input=false', '-no-color', '-lock-timeout=60s',
                         '-var-file=' + str(inputs), '-out=' + str(binary)],
                        '8. Generate a NEW saved S3-backed plan only. S3 lock-object writes/deletes are normal.',
                        ROOT / 'infra/aws-ecs-dev')
            require(binary.is_file(), 'Terraform did not create the saved plan')
            binary.chmod(0o600)
            result = session.run(['terraform', 'show', '-json', str(binary)],
                                 '9. Preserve the exact private saved-plan JSON; output is suppressed.',
                                 ROOT / 'infra/aws-ecs-dev', redact=True)
            plan_json.write_text(result.stdout)
            plan_json.chmod(0o600)
            review(session, args, binary, plan_json, hashlib.sha256(binary.read_bytes()).hexdigest(), https, s3)
        session.save('PREPARATION_COMPLETE_NOT_APPROVED')
        session.say('Private transcript: ' + str(session.transcript))
        return 0
    except (Stop, ValueError, KeyError, json.JSONDecodeError) as error:
        message = str(error)
        if session is not None:
            session.say('STOP: ' + message)
            session.save('STOPPED_NO_APPLY', message)
        else:
            print('STOP: ' + message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
