import { randomBytes } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
const base='http://127.0.0.1:9191';
await mkdir('work',{recursive:true});
let password;
try{password=(await readFile('work/sonar-admin-password','utf8')).trim();}catch{password='N!'+randomBytes(24).toString('hex');}
const auth=value=>`Basic ${Buffer.from(`admin:${value}`).toString('base64')}`;
async function post(path,body,pass=password){const r=await fetch(base+path,{method:'POST',headers:{Connection:'close',Authorization:auth(pass),'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(body),signal:AbortSignal.timeout(15000)});if(!r.ok)throw new Error(`${path} returned HTTP${r.status}`);return r;}
const until=Date.now()+180000;
while(true){try{const r=await fetch(base+'/api/system/status');const s=await r.json();if(s.status==='UP')break;}catch{}if(Date.now()>until)throw new Error('SonarQube not ready after180s; inspect logs');await new Promise(r=>setTimeout(r,2000));}
const current=await fetch(base+'/api/authentication/validate',{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
if(!current.valid){await post('/api/users/change_password',{login:'admin',previousPassword:'admin',password},'admin');await writeFile('work/sonar-admin-password',password+'\n',{mode:0o600});}
const tokenName=`local-${Date.now()}`;
const token=await post('/api/user_tokens/generate',{name:tokenName}).then(r=>r.json());
await writeFile('work/sonar-scanner.env',`SONAR_TOKEN=${token.token}\n`,{mode:0o600});
try{
 const run=spawnSync('docker',['run','--rm','--network','linked-in-node-local_default','-e','SONAR_HOST_URL=http://sonarqube:9000','--env-file','work/sonar-scanner.env','-v',`${process.cwd()}:/usr/src`,'sonarsource/sonar-scanner-cli:latest'],{stdio:'inherit'});
 const gate=await fetch(`${base}/api/qualitygates/project_status?projectKey=linked-in-node-and-aws`,{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
 const issues=await fetch(`${base}/api/issues/search?componentKeys=linked-in-node-and-aws&ps=100`,{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
 await writeFile('docs/evidence/sonar-gate.json',JSON.stringify(gate,null,2)+'\n');
 await writeFile('docs/evidence/sonar-issues.json',JSON.stringify(issues,null,2)+'\n');
 if(run.status!==0||gate.projectStatus?.status!=='OK')process.exitCode=1;
}finally{await post('/api/user_tokens/revoke',{name:tokenName});await writeFile('work/sonar-scanner.env','',{mode:0o600});}
