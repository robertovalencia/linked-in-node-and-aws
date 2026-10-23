// Executable AWS CLI contract tests; no network or AWS account is used.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmod, copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { gzipSync } from 'node:zlib';

const commandId = '12345678-1234-1234-1234-123456789abc';
const instanceId = 'i-0123456789abcdef0';
const sourceSha = 'a'.repeat(40);
const report = () => ({ expected: 48, passed: 48, failed: 0, results: Array.from({length:48}, (_, i) => ({name:`Acceptance ${i}`,status:'PASS'})) });
function invocation(output = report()) {
  return { CommandId: commandId, InstanceId: instanceId, Status: 'Success', ResponseCode: 0,
    StandardOutputContent: `MARKETPLACE_ACCEPTANCE_GZIP_BASE64=${gzipSync(JSON.stringify(output)).toString('base64')}\n`, StandardErrorContent: '' };
}
async function run(invocationResult) {
  const root = await mkdtemp(join(tmpdir(), 'marketplace-aws-contract-'));
  try {
    for (const path of ['scripts','infra/aws-dev','infra/postgres','bin']) await mkdir(join(root,path), {recursive:true});
    await copyFile('scripts/aws-deploy.sh', join(root,'scripts/aws-deploy.sh'));
    for (const path of ['scripts/aws-remote-deploy.sh','scripts/aws-smoke.sh','scripts/acceptance.mjs','infra/aws-dev/compose.yaml','infra/postgres/init-databases.sh']) await writeFile(join(root,path), 'test fixture\n');
    await writeFile(join(root,'invocation.json'), JSON.stringify(invocationResult));
    const cli = join(root, 'bin/aws');
    await writeFile(cli, `#!/usr/bin/env python3
import json,os,sys
args=sys.argv[1:]
if args[:2]==['s3','cp']: sys.exit(0)
if args[:2]==['ssm','send-command']:
    print(json.dumps({'Command':{'CommandId':'${commandId}'}})); sys.exit(0)
if args[:2]==['ssm','get-command-invocation']:
    assert args[args.index('--command-id')+1]=='${commandId}'
    assert args[args.index('--instance-id')+1]=='${instanceId}'
    print(open(os.environ['MOCK_INVOCATION']).read()); sys.exit(0)
raise SystemExit('Unexpected AWS operation '+str(args))
`);
    await chmod(cli, 0o755);
    const execution = spawnSync('bash',[join(root,'scripts/aws-deploy.sh')],{encoding:'utf8',env:{...process.env,PATH:`${join(root,'bin')}:${process.env.PATH}`,MOCK_INVOCATION:join(root,'invocation.json'),AWS_REGION:'us-east-2',AWS_INSTANCE_ID:instanceId,AWS_RELEASE_BUCKET:'marketplace-test-release',AWS_SECRET_ARN:'arn:aws:secretsmanager:us-east-2:123456789012:secret:test',BACKEND_IMAGE:'example-backend@sha256:'+'b'.repeat(64),FRONTEND_IMAGE:'example-frontend@sha256:'+'c'.repeat(64),GITHUB_SHA:sourceSha}});
    const saved = async name => JSON.parse(await readFile(join(root,'work',name),'utf8'));
    return { ...execution, command:await saved('aws-ssm-command.json'), invocation:await saved('aws-ssm-invocation.json'), acceptance:await saved('aws-acceptance.json').catch(()=>undefined) };
  } finally { await rm(root,{recursive:true,force:true}); }
}

test('preserves exact SSM command, invocation, and all 48 acceptance results', async () => {
  const result = await run(invocation());
  assert.equal(result.status,0,result.stderr);
  assert.equal(result.command.Command.CommandId,commandId);
  assert.equal(result.invocation.CommandId,commandId);
  assert.equal(result.acceptance.ssmCommandId,commandId);
  assert.equal(result.acceptance.ssmInstanceId,instanceId);
  assert.equal(result.acceptance.sourceSha,sourceSha);
  assert.equal(result.acceptance.results.length,48);
});
for (const [name, mutate] of [
  ['missing or truncated evidence', value => { value.StandardOutputContent='Release verified'; }],
  ['partial acceptance suite', value => { value.StandardOutputContent=`MARKETPLACE_ACCEPTANCE_GZIP_BASE64=${gzipSync(JSON.stringify({...report(),passed:47,results:report().results.slice(0,47)})).toString('base64')}`; }],
  ['failed check hidden by summary', value => { const r=report();r.results[0].status='FAIL';value.StandardOutputContent=`MARKETPLACE_ACCEPTANCE_GZIP_BASE64=${gzipSync(JSON.stringify(r)).toString('base64')}`; }],
  ['different command identity', value => { value.CommandId='different-command'; }],
  ['nonzero response despite Success', value => { value.ResponseCode=1; }],
  ['terminal SSM failure', value => { value.Status='Failed';value.ResponseCode=1; }],
]) test(`rejects ${name}`,async()=>{const value=invocation();mutate(value);const result=await run(value);assert.notEqual(result.status,0);assert.equal(result.invocation.Status,value.Status);});

test('preserves failed remote acceptance evidence without approving the release', async () => {
  const failed = report();
  failed.passed = 47; failed.failed = 1; failed.results[0].status = 'FAIL';
  const value = invocation(failed); value.Status = 'Failed'; value.ResponseCode = 1;
  const result = await run(value);
  assert.notEqual(result.status, 0);
  assert.equal(result.acceptance.failed, 1);
  assert.equal(result.acceptance.ssmStatus, 'Failed');
});
