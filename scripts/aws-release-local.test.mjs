// Contract tests replace every external service/tool. They never contact AWS or GitHub.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmod, copyFile, mkdir, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const sha = 'a'.repeat(40);
async function release(scenario = 'success') {
  const fixture = await mkdtemp(join(tmpdir(), 'marketplace-local-release-'));
  try {
    for (const dir of ['scripts','bin','infra/aws-dev/.terraform','archive/backend','archive/frontend']) await mkdir(join(fixture, dir), {recursive:true});
    await copyFile('scripts/aws-release-local.mjs',join(fixture,'scripts/aws-release-local.mjs'));
    await writeFile(join(fixture,'infra/aws-dev/.terraform/terraform.tfstate'),JSON.stringify({backend:{type:scenario==='local-state'?'local':'s3',config:{bucket:'marketplace-state',key:'linked-in-node/dev/terraform.tfstate'}}}));
    await writeFile(join(fixture,'archive/backend/Dockerfile'),'test source');
    await writeFile(join(fixture,'archive/frontend/Dockerfile'),'test source');
    const fake = `#!/usr/bin/env node
import { basename,join } from 'node:path';
import { readFileSync,writeFileSync,mkdirSync,existsSync,appendFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
const tool=basename(process.argv[1]);const args=process.argv.slice(2);const root=process.env.MOCK_ROOT;const scenario=process.env.MOCK_SCENARIO;
appendFileSync(join(root,'calls.log'),JSON.stringify({tool,args})+'\\n');
const sha='${sha}';const registry='111111111111.dkr.ecr.us-east-2.amazonaws.com';const prefix='linked-in-node-dev';
const pass=()=>({expected:48,passed:48,failed:0,results:Array.from({length:48},(_,i)=>({name:'Check'+i,status:'PASS'}))});
const output=value=>{console.log(typeof value==='string'?value:JSON.stringify(value));process.exit(0);};
if(tool==='git'){
 if(args[0]==='rev-parse')output(sha);
 if(args[0]==='branch')output('main');
 if(args[0]==='remote')output('https://github.com/robertovalencia/linked-in-node-and-aws.git');
 if(args[0]==='status')output(scenario==='dirty'?' M backend/src/main.ts':'');
 if(args[0]==='archive'){const archive=spawnSync('tar',['-cf','-','-C',join(root,'archive'),'backend','frontend']);process.stdout.write(archive.stdout);process.exit(archive.status);}
}
if(tool==='gh'){
 if(args[0]==='api'&&args[1].includes('/jobs?'))output({jobs:[{name:'verify',conclusion:scenario==='verify-failed'?'failure':'success'},{name:'deploy',conclusion:scenario==='ci-deployed'?'success':'skipped'}]});
 if(args[0]==='api')output({id:123,path:scenario==='wrong-workflow'?'.github/workflows/quality.yml':'.github/workflows/deploy-dev.yml',head_repository:{full_name:'robertovalencia/linked-in-node-and-aws'},head_sha:scenario==='wrong-sha'?'b'.repeat(40):sha,head_branch:'main',event:'workflow_dispatch',status:'completed',conclusion:'success'});
 if(args[0]==='run'&&args[1]==='download'){
  const dir=args[args.indexOf('--dir')+1];mkdirSync(join(dir,'work/ci-sonar'),{recursive:true});
  const acceptance=pass();if(scenario==='partial-suite'){acceptance.passed=47;acceptance.results.pop();}
  writeFileSync(join(dir,'work/release-acceptance.json'),JSON.stringify(acceptance));
  const conditions=[{metricKey:'coverage',status:'OK',comparator:'LT',errorThreshold:'80',actualValue:scenario==='low-coverage'?'79.9':'82.3'},{metricKey:'violations',status:'OK',comparator:'GT',errorThreshold:'0',actualValue:'0'},{metricKey:'duplicated_lines_density',status:'OK',comparator:'GT',errorThreshold:'3',actualValue:'0'}];
  if(scenario==='missing-sonar-condition')conditions.pop();
  writeFileSync(join(dir,'work/ci-sonar/gate.json'),JSON.stringify({sourceSha:scenario==='wrong-analysis-sha'?'b'.repeat(40):sha,ceTaskId:'task123',analysisId:'analysis123',projectStatus:{status:'OK',conditions}}));output('downloaded');
 }
}
if(tool==='terraform'){
 if(args.includes('workspace'))output('default');
 if(args.includes('output')){
  const values={deployment_account_id:'111111111111',deployment_region:scenario==='wrong-region'?'us-east-1':'us-east-2',instance_id:'i-0123456789abcdef0',release_bucket:prefix+'-releases-test',secret_arn:'arn:aws:secretsmanager:us-east-2:111111111111:secret:'+prefix+'/runtime-AbCdEf',backend_repository:registry+'/'+prefix+'/backend',frontend_repository:registry+'/'+prefix+'/frontend'};
  output(Object.fromEntries(Object.entries(values).map(([key,value])=>[key,{value}])));
 }
}
if(tool==='aws'){
 if(args[0]==='sts')output({Account:scenario==='wrong-account'?'222222222222':'111111111111'});
 if(args[0]==='ecr'&&args[1]==='get-login-password')output('FAKE_ECR_PASSWORD_NEVER_LOG');
 if(args[0]==='ecr'&&args[1]==='describe-repositories')output(scenario==='mutable-tags'?'MUTABLE':'IMMUTABLE');
 if(args[0]==='ecr'&&args[1]==='batch-get-image'){
  const app=args[args.indexOf('--repository-name')+1].split('/').at(-1);
  if(scenario==='new-images'&&!existsSync(join(root,'built-'+app)))output({images:[],failures:[{failureCode:'ImageNotFound'}]});
  output({images:[{imageId:{imageDigest:'sha256:'+(app==='backend'?'b':'c').repeat(64)}}]});
 }
}
if(tool==='docker'){
 if(args[0]==='info'||args[0]==='login'||args[0]==='pull')output('ok');
 if(args[0]==='buildx'&&args[1]==='version')output('buildx test');
 if(args[0]==='buildx'&&args[1]==='build'){
  if(args[args.indexOf('--platform')+1]!=='linux/amd64')throw Error('wrong build platform');
  const app=args[args.indexOf('--tag')+1].split('/').at(-1).split(':')[0];writeFileSync(join(root,'built-'+app),'built');output('pushed');
 }
 if(args[0]==='image'&&args[1]==='inspect')output([{Architecture:scenario==='wrong-architecture'?'arm64':'amd64',Os:'linux',Config:{Labels:{'org.opencontainers.image.revision':scenario==='wrong-image-label'?'b'.repeat(40):sha}}}]);
}
if(tool==='trivy'){
 if(args[0]==='--version')output('Version: 0.76.1');
 if(args[0]==='image'){
  if(!args.includes('--ignore-unfixed=false')||args[args.indexOf('--severity')+1]!=='HIGH,CRITICAL')throw Error('weakened Trivy gate');
  writeFileSync(args[args.indexOf('--output')+1],JSON.stringify({ArtifactName:args.at(-1),Results:[{Vulnerabilities:scenario==='vulnerable-image'?[{VulnerabilityID:'TEST',Severity:'HIGH'}]:[]}]}));
  if(scenario==='scan-failure')process.exit(1);output('scan done');
 }
}
throw Error('Unexpected external operation '+tool+' '+args.join(' '));
`;
    for (const tool of ['git','gh','terraform','aws','docker','trivy']) {const path=join(fixture,'bin',tool);await writeFile(path,fake);await chmod(path,0o755);}
    await writeFile(join(fixture,'scripts/aws-deploy.sh'),`#!/usr/bin/env bash\nset -euo pipefail\nnode "$MOCK_ROOT/capture.mjs"\n`);
    await writeFile(join(fixture,'capture.mjs'),`import{writeFileSync,mkdirSync}from'node:fs';import{join}from'node:path';const root=process.env.MOCK_ROOT;writeFileSync(join(root,'deployed.json'),JSON.stringify({sha:process.env.GITHUB_SHA,backend:process.env.BACKEND_IMAGE,frontend:process.env.FRONTEND_IMAGE,instance:process.env.AWS_INSTANCE_ID,region:process.env.AWS_REGION}));mkdirSync(join(root,'work'),{recursive:true});writeFileSync(join(root,'work/aws-acceptance.json'),JSON.stringify({passed:48,failed:0}));console.log('fake release verified');if(process.env.MOCK_SCENARIO==='deployment-failed'){console.error('Fake remote failure');process.exit(1);}`);
    const execution=spawnSync(process.execPath,[join(fixture,'scripts/aws-release-local.mjs'),'123'],{encoding:'utf8',env:{...process.env,PATH:`${join(fixture,'bin')}:${process.env.PATH}`,AWS_PROFILE:'marketplace-dev',AWS_REGION:'us-east-2',MOCK_ROOT:fixture,MOCK_SCENARIO:scenario}});
    const calls=(await readFile(join(fixture,'calls.log'),'utf8')).trim().split('\n').map(line=>JSON.parse(line));
    const deployed=await readFile(join(fixture,'deployed.json'),'utf8').then(JSON.parse).catch(()=>undefined);
    const directories=await readdir(join(fixture,'work/local-release')).catch(()=>[]);
    const deploymentLog=directories.length?await readFile(join(fixture,'work/local-release',directories[0],'deployment.log'),'utf8').catch(()=>undefined):undefined;
    return {...execution,calls,deployed,deploymentLog};
  }finally{await rm(fixture,{recursive:true,force:true});}
}

test('deploys exact verified digests after matching account/region, architecture and clean scans',async()=>{
 const result=await release();assert.equal(result.status,0,result.stderr);assert.equal(result.deployed.sha,sha);assert.equal(result.deployed.region,'us-east-2');assert.match(result.deployed.backend,/@sha256:b{64}$/);assert.match(result.deployed.frontend,/@sha256:c{64}$/);assert.ok(!result.stdout.includes('FAKE_ECR_PASSWORD_NEVER_LOG'));assert.ok(!result.stderr.includes('FAKE_ECR_PASSWORD_NEVER_LOG'));
});
test('builds missing immutable SHA tags from Git archive for linux/amd64 before scanning',async()=>{
 const result=await release('new-images');assert.equal(result.status,0,result.stderr);const builds=result.calls.filter(call=>call.tool==='docker'&&call.args[0]==='buildx'&&call.args[1]==='build');assert.equal(builds.length,2);assert.ok(builds.every(call=>call.args.includes('--push')&&call.args.includes(`org.opencontainers.image.revision=${sha}`)));
});
for(const scenario of ['dirty','wrong-sha','wrong-workflow','verify-failed','ci-deployed','partial-suite','wrong-analysis-sha','low-coverage','missing-sonar-condition','local-state','wrong-account','wrong-region'])test(`rejects ${scenario} before registry publication or SSM`,async()=>{
 const result=await release(scenario);assert.notEqual(result.status,0,scenario);assert.equal(result.deployed,undefined);assert.ok(!result.calls.some(call=>call.tool==='docker'&&call.args[0]==='login'));assert.ok(!result.calls.some(call=>call.tool==='docker'&&call.args[0]==='buildx'&&call.args[1]==='build'));
});
for(const scenario of ['mutable-tags','wrong-image-label','wrong-architecture','vulnerable-image','scan-failure'])test(`rejects ${scenario} before deployment`,async()=>{
 const result=await release(scenario);assert.notEqual(result.status,0,scenario);assert.equal(result.deployed,undefined);
});

test('preserves remote failure output and fails the local release',async()=>{
 const result=await release('deployment-failed');assert.notEqual(result.status,0);assert.match(result.deploymentLog,/Fake remote failure/);
});
