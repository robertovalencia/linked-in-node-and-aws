#!/usr/bin/env python3
"""Credential-free contracts/identity exercise. Only built-in terraform_data is used."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parent
COMMANDS = 0
ASSERTIONS = 0

def main():
    global COMMANDS, ASSERTIONS
    # Ignore ambient CLI arguments, backend data directories, workspaces and tokens.
    env = {k: v for k, v in os.environ.items() if not k.startswith(('TF_', 'TFE_', 'AWS_', 'ARM_', 'GOOGLE_', 'CLOUDSDK_'))}
    env.update(TF_IN_AUTOMATION='1', CHECKPOINT_DISABLE='1')
    with tempfile.TemporaryDirectory(prefix='terraform-advanced-') as directory:
        root = Path(directory)
        for name in ('main.tf', 'modules', 'tests'):
            source = SOURCE / name
            if source.is_dir():
                shutil.copytree(source, root / name)
            else:
                shutil.copy2(source, root / name)
        cli = root / 'terraform.rc'
        cli.write_text('disable_checkpoint = true\n')
        env['TF_CLI_CONFIG_FILE'] = str(cli)

        def tf(*args, expected=0, capture_json=False):
            global COMMANDS
            COMMANDS += 1
            result = subprocess.run(['terraform', *args], cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(f'COMMAND {COMMANDS}: terraform {" ".join(args)} -> {result.returncode} (expected {expected})', flush=True)
            if result.returncode != expected:
                print(result.stdout)
                raise RuntimeError('Unexpected Terraform exit status')
            if capture_json:
                return json.loads(result.stdout)
            print(result.stdout, end='')
            return result.stdout

        def require(condition, message):
            global ASSERTIONS
            if not condition:
                raise AssertionError(message)
            ASSERTIONS += 1
            print(f'ASSERT {ASSERTIONS} PASS: {message}', flush=True)

        tf('version')
        tf('fmt', '-check', '-recursive')
        tf('init', '-input=false', '-no-color')
        tf('validate', '-no-color')
        tf('plan', '-input=false', '-no-color', '-detailed-exitcode', '-out=initial.tfplan', expected=2)
        initial_plan = tf('show', '-json', 'initial.tfplan', capture_json=True)
        changes = initial_plan['resource_changes']
        require(len(changes) == 2 and all(c['change']['actions'] == ['create'] for c in changes), 'exactly two child resources are created')
        tf('apply', '-input=false', '-no-color', 'initial.tfplan')
        initial = tf('output', '-json', capture_json=True)
        require(set(initial['contracts']['value']) == {'catalog', 'identity'}, 'disabled preview has no module instance')
        require(initial['contracts']['value']['catalog']['tier'] == 'standard', 'optional tier defaults in the child contract')
        old_ids = initial['identities']['value']
        tf('plan', '-input=false', '-no-color', '-detailed-exitcode')

        changed = {'services': {'catalog': {'owner': 'team-catalog-v2'}, 'identity': {'owner': 'team-identity', 'tier': 'critical'}, 'search': {'owner': 'team-search'}}}
        (root / 'scenario.auto.tfvars.json').write_text(json.dumps(changed))
        tf('plan', '-input=false', '-no-color', '-detailed-exitcode', '-out=change.tfplan', expected=2)
        changed_plan = tf('show', '-json', 'change.tfplan', capture_json=True)
        actions = {c['address']: c['change']['actions'] for c in changed_plan['resource_changes']}
        require(actions['module.service["catalog"].terraform_data.record'] == ['update'], 'owner change updates the catalog instance')
        require(actions['module.service["identity"].terraform_data.record'] == ['no-op'], 'unrelated identity instance remains unchanged')
        require(actions['module.service["search"].terraform_data.record'] == ['create'], 'new stable search key creates only its own instance')
        tf('apply', '-input=false', '-no-color', 'change.tfplan')
        after = tf('output', '-json', capture_json=True)
        require(all(after['identities']['value'][key] == value for key, value in old_ids.items()), 'existing IDs survive value change and key addition')

        child = root / 'modules' / 'service' / 'main.tf'
        child.write_text(child.read_text().replace('"terraform_data" "record"', '"terraform_data" "entry"').replace('terraform_data.record.', 'terraform_data.entry.') + '\nmoved {\n  from = terraform_data.record\n  to   = terraform_data.entry\n}\n')
        tf('fmt', '-recursive')
        tf('validate', '-no-color')
        tf('plan', '-input=false', '-no-color', '-detailed-exitcode', '-out=move.tfplan', expected=2)
        moved = tf('show', '-json', 'move.tfplan', capture_json=True)
        require(len(moved['resource_changes']) == 3 and all(c['change']['actions'] == ['no-op'] and c.get('previous_address', '').endswith('.terraform_data.record') for c in moved['resource_changes']), 'child moved block maps all three instances without replacement')
        tf('apply', '-input=false', '-no-color', 'move.tfplan')
        moved_outputs = tf('output', '-json', capture_json=True)
        require(moved_outputs['identities']['value'] == after['identities']['value'], 'every ID survives the child-module address migration')
        backup = tf('state', 'pull', capture_json=True)
        require(backup['serial'] > 0 and bool(backup['lineage']), 'state snapshot includes serial and lineage')
        backup_file = root / 'private-state-backup.json'
        backup_file.write_text(json.dumps(backup))
        backup_file.chmod(0o600)
        tf('plan', '-input=false', '-no-color', '-refresh-only', '-detailed-exitcode')
        tf('test', '-no-color')
        tf('destroy', '-input=false', '-no-color', '-auto-approve')
        require(not tf('state', 'list').strip(), 'normal local state is empty after cleanup')
        print(f'PASS: {COMMANDS} Terraform commands; {ASSERTIONS} runner assertions; five Terraform test runs. No cloud provider, backend or credentials.', flush=True)

if __name__ == '__main__':
    main()
