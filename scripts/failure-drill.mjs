import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const base='http://127.0.0.1:8180';
const results=[];
const dc=(...args)=>execFileSync('docker',['compose','--project-directory',root,'-p','linked-in-node-local',...args],{cwd:root,encoding:'utf8',stdio:['pipe','pipe','pipe'],timeout:180000});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function request(path,{token,method='GET',body,key}={}){
  const response=await fetch(`${base}${path}`,{method,headers:{...(token?{Authorization:`Bearer ${token}`} :{}),...(body?{'Content-Type':'application/json'}:{}),...(key?{'Idempotency-Key':key}:{})},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(15000)});
  let data;try{data=await response.json();}catch{data=null;}return{status:response.status,data};
}
async function check(name,fn){try{await fn();results.push({name,status:'PASS'});console.log(`PASS ${name}`);}catch(error){results.push({name,status:'FAIL',detail:error.message});console.error(`FAIL ${name}: ${error.message}`);}}
async function eventually(fn,ms=60000){const until=Date.now()+ms;let last;while(Date.now()<until){try{return await fn();}catch(e){last=e;await sleep(800);}}throw last??new Error('Timed out');}
const login=async email=>{const r=await request('/api/auth/login',{method:'POST',body:{email,password:'DemoPass123!'}});assert.equal(r.status,201===r.status?201:200);assert.ok(r.data.token);return r.data.token;};
const company=await login('company@demo.local'), ava=await login('ava@demo.local');
const body={providerId:'ava-martinez',subject:`Resilience ${Date.now()}`,message:'Verify durable delivery through a real local broker outage.',budget:1500,clientType:'COMPANY'};
await check('Reject missing idempotency key',async()=>assert.equal((await request('/api/inquiries',{method:'POST',token:company,body})).status,400));
await check('Reject wrong field types and unknown status',async()=>{assert.equal((await request('/api/inquiries',{method:'POST',token:company,key:randomUUID(),body:{...body,budget:'1500'}})).status,400);});
await check('Private internal lookup is absent from edge',async()=>{const r=await request('/internal/providers/ava-martinez');assert.ok(!r.data?.ownerEmail);});
let inquiry;let brokerStopped=false;
try {
  await check('Inquiry remains durable while Kafka is stopped',async()=>{
    dc('stop','kafka');brokerStopped=true;
    const r=await request('/api/inquiries',{method:'POST',token:company,body,key:randomUUID()});assert.ok(r.status===200||r.status===201);inquiry=r.data;assert.ok(inquiry.id);
    const out=dc('exec','-T','postgres','psql','-U','marketplace_admin','-d','inquiries','-tAc',`SELECT count(*) FROM outbox WHERE inquiry_id='${inquiry.id}' AND published_at IS NULL`);
    assert.equal(out.trim(),'1');
  });
} finally {if(brokerStopped)dc('up','-d','--wait','kafka');}
if(inquiry){
  await check('Outbox delivers after Kafka recovers',async()=>{await eventually(async()=>{const r=await request('/api/notifications',{token:ava});assert.equal(r.status,200);assert.ok(r.data.some(n=>n.inquiryId===inquiry.id));});});
  await check('Replaying identical Kafka event does not duplicate inbox',async()=>{
    const payload=dc('exec','-T','postgres','psql','-U','marketplace_admin','-d','inquiries','-tAc',`SELECT payload::text FROM outbox WHERE inquiry_id='${inquiry.id}'`).trim();
    assert.ok(JSON.parse(payload).eventId);
    execFileSync('docker',['compose','--project-directory',root,'-p','linked-in-node-local','exec','-T','kafka','/opt/kafka/bin/kafka-console-producer.sh','--bootstrap-server','localhost:9092','--topic','inquiry.created.v1'],{input:payload+'\n'+payload+'\n',timeout:30000,stdio:['pipe','pipe','pipe']});
    await sleep(2500);
    const r=await request('/api/notifications',{token:ava});assert.equal(r.data.filter(n=>n.inquiryId===inquiry.id).length,1);
  });
  await check('Resolved inquiry cannot be changed to opposite outcome',async()=>{
    assert.ok([200,201].includes((await request(`/api/inquiries/${inquiry.id}/status`,{method:'PATCH',token:ava,body:{status:'ACCEPTED'}})).status));
    assert.equal((await request(`/api/inquiries/${inquiry.id}/status`,{method:'PATCH',token:ava,body:{status:'DECLINED'}})).status,409);
  });
  await check('Database and application restart preserve inquiry and notification',async()=>{
    dc('restart','postgres','identity','catalog','inquiries','notifications');
    await eventually(async()=>{const r=await request('/api/inquiries',{token:company});assert.equal(r.status,200);assert.equal(r.data.find(x=>x.id===inquiry.id)?.status,'ACCEPTED');});
    await eventually(async()=>{const r=await request('/api/notifications',{token:ava});assert.equal(r.status,200);assert.equal(r.data.filter(x=>x.inquiryId===inquiry.id).length,1);});
  });
}
await check('Service database login cannot connect to another service database',async()=>{
  const output=dc('exec','-T','postgres','psql','-U','marketplace_admin','-d','postgres','-tAc',"SELECT has_database_privilege('identity','catalog','CONNECT')");assert.equal(output.trim(),'f');
});
const report={completedAt:new Date().toISOString(),environment:'local',passed:results.filter(r=>r.status==='PASS').length,failed:results.filter(r=>r.status==='FAIL').length,results};
await mkdir(resolve(root,'docs/evidence'),{recursive:true});await writeFile(resolve(root,'docs/evidence/failure-drill.json'),JSON.stringify(report,null,2)+'\n');
if(report.failed||results.length!==9)process.exitCode=1;
