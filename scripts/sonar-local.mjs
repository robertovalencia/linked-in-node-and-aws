import { randomBytes } from 'node:crypto';
import { mkdir, readFile, unlink, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
const base='http://127.0.0.1:9191';
const scannerImage='sonarsource/sonar-scanner-cli@sha256:a3f4215076706c95a17a68c19322ee916e40a3acd081a8c1a1e839e0194afa57';
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
await writeFile('work/sonar-scanner.env','',{mode:0o600});
let tokenIssued=false;
try{
 const tokenResponse=await post('/api/user_tokens/generate',{name:tokenName});
 tokenIssued=true;
 const token=await tokenResponse.json();
 await writeFile('work/sonar-scanner.env',`SONAR_TOKEN=${token.token}\n`,{mode:0o600});
 await mkdir('work/sonar-scanner',{recursive:true});
 await unlink('work/sonar-scanner/report-task.txt').catch(error=>{if(error.code!=='ENOENT')throw error;});
 const run=spawnSync('docker',['run','--rm','--network','linked-in-node-local_default','-e','SONAR_HOST_URL=http://sonarqube:9000','--env-file','work/sonar-scanner.env','-v',`${process.cwd()}:/usr/src`,scannerImage,'-Dsonar.working.directory=/usr/src/work/sonar-scanner'],{encoding:'utf8',maxBuffer:10_000_000});
 const scanLog=`${run.stdout??''}${run.stderr??''}`;
 process.stdout.write(scanLog);
 await writeFile('docs/evidence/sonar-scan.txt',scanLog);
 const task=Object.fromEntries((await readFile('work/sonar-scanner/report-task.txt','utf8')).trim().split('\n').map(line=>line.split('=',2)));
 if(!task.ceTaskId)throw new Error('Fresh scanner did not report a CE task ID');
 let ce;
 const ceDeadline=Date.now()+300000;
 do{
  ce=await fetch(`${base}/api/ce/task?id=${encodeURIComponent(task.ceTaskId)}`,{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
  if(ce.task?.status==='SUCCESS'||ce.task?.status==='FAILED'||ce.task?.status==='CANCELED')break;
  if(Date.now()>ceDeadline)throw new Error('Fresh CE task did not finish within 300 seconds');
  await new Promise(r=>setTimeout(r,2000));
 }while(true);
 if(ce.task?.status!=='SUCCESS'||!ce.task.analysisId)throw new Error(`Fresh CE task did not succeed: ${ce.task?.status??'missing'}`);
 const gate=await fetch(`${base}/api/qualitygates/project_status?analysisId=${encodeURIComponent(ce.task.analysisId)}`,{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
 const issues=await fetch(`${base}/api/issues/search?componentKeys=linked-in-node-and-aws&ps=100`,{headers:{Connection:'close',Authorization:auth(password)}}).then(r=>r.json());
 await writeFile('docs/evidence/sonar-gate.json',JSON.stringify({ceTaskId:task.ceTaskId,analysisId:ce.task.analysisId,...gate},null,2)+'\n');
 await writeFile('docs/evidence/sonar-issues.json',JSON.stringify(issues,null,2)+'\n');
 if(run.status!==0||gate.projectStatus?.status!=='OK')process.exitCode=1;
}finally{
 try{if(tokenIssued)await post('/api/user_tokens/revoke',{name:tokenName});}
 finally{await writeFile('work/sonar-scanner.env','',{mode:0o600});}
}
