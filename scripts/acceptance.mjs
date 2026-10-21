#!/usr/bin/env node
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';
const base=(process.argv[2]||'http://localhost:8080').replace(/\/$/,'');
const output=process.argv[3];
const runId=`acceptance-${Date.now()}`;
const results=[];
async function request(path,{method='GET',token,body,key}={}){
 const r=await fetch(`${base}${path}`,{method,headers:{...(body?{'Content-Type':'application/json'}:{}),...(token?{Authorization:`Bearer ${token}`} :{}),...(key?{'Idempotency-Key':key}:{})},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(15000)});
 const text=await r.text(); let data;try{data=JSON.parse(text);}catch{data=text;}
 return {status:r.status,data};
}
async function check(name,fn){try{await fn();results.push({name,status:'PASS'});console.log(`PASS ${name}`);}catch(e){results.push({name,status:'FAIL',detail:String(e.message).slice(0,600)});console.error(`FAIL ${name}: ${e.message}`);}}
function status(r,n){assert.equal(r.status,n,`Expected HTTP ${n}; got ${r.status}: ${JSON.stringify(r.data).slice(0,350)}`);}
function ok(r){assert.ok(r.status>=200&&r.status<300,`Expected success; got ${r.status}: ${JSON.stringify(r.data).slice(0,350)}`);}
const tokens={};
for(const [who,email] of Object.entries({company:'company@demo.local',individual:'individual@demo.local',ava:'ava@demo.local',leo:'leo@demo.local'})){
 await check(`Login ${who}`,async()=>{const r=await request('/api/auth/login',{method:'POST',body:{email,password:'DemoPass123!'}});ok(r);assert.equal(r.data.email,email);assert.ok(r.data.token);tokens[who]=r.data.token;});
}
await check('Invalid password rejected',async()=>status(await request('/api/auth/login',{method:'POST',body:{email:'company@demo.local',password:'not-the-password'}}),401));
await check('Anonymous identity denied',async()=>status(await request('/api/auth/me'),401));
await check('Tampered bearer denied',async()=>status(await request('/api/auth/me',{token:'invalid.token.invalid'}),401));
await check('Verified identity returns correct role',async()=>{const r=await request('/api/auth/me',{token:tokens.company});ok(r);assert.equal(r.data.role,'CLIENT');});
let providers=[];let ava;
await check('Anonymous provider discovery uses persistent seed data',async()=>{const r=await request('/api/providers');ok(r);providers=r.data.items;assert.ok(providers.length>=6);assert.ok(r.data.total>=6);ava=providers.find(p=>p.id==='ava-martinez');assert.ok(ava);});
await check('Public provider fields cover service showcase without private identity',async()=>{const r=await request('/api/providers/ava-martinez');ok(r);ava=r.data;for(const f of ['name','headline','location','category','about','skills','tools','services','experience','portfolio','hourlyRate','available'])assert.ok(Object.hasOwn(ava,f),f);assert.ok(ava.experience.length);assert.ok(ava.portfolio.length);assert.ok(!Object.hasOwn(ava,'ownerEmail'));});
await check('Name search narrows providers',async()=>{const r=await request('/api/providers?q=Ava');ok(r);assert.ok(r.data.items.length);assert.ok(r.data.items.every(x=>JSON.stringify(x).toLowerCase().includes('ava')));});
await check('Category filter',async()=>{const r=await request('/api/providers?category=IT%20Consulting');ok(r);assert.ok(r.data.items.length);assert.ok(r.data.items.every(x=>x.category==='IT Consulting'));});
await check('Skill filter',async()=>{const r=await request('/api/providers?skill=Java');ok(r);assert.ok(r.data.items.length);assert.ok(r.data.items.every(x=>x.skills.some(s=>s.toLowerCase().includes('java'))));});
await check('Maximum rate filter',async()=>{const r=await request('/api/providers?maxRate=100');ok(r);assert.ok(r.data.items.length);assert.ok(r.data.items.every(x=>x.hourlyRate<=100));});
await check('Availability filter',async()=>{const r=await request('/api/providers?available=true');ok(r);assert.ok(r.data.items.length);assert.ok(r.data.items.every(x=>x.available));});
await check('Rate sort and deterministic pagination',async()=>{const a=await request('/api/providers?sort=rate-asc&size=2&page=0');const b=await request('/api/providers?sort=rate-asc&size=2&page=1');ok(a);ok(b);assert.equal(a.data.items.length,2);assert.equal(b.data.items.length,2);assert.equal(a.data.total,b.data.total);const all=[...a.data.items,...b.data.items];assert.equal(new Set(all.map(x=>x.id)).size,4);assert.deepEqual(all.map(x=>x.hourlyRate),all.map(x=>x.hourlyRate).sort((x,y)=>x-y));});
await check('No-match query has empty items and zero total',async()=>{const r=await request('/api/providers?q=no-match-zzzz-999');ok(r);assert.equal(r.data.total,0);assert.deepEqual(r.data.items,[]);});
await check('Missing provider 404',async()=>status(await request('/api/providers/no-such-provider'),404));
await check('Anonymous provider editor denied',async()=>status(await request('/api/providers/me'),401));
await check('Client provider editor denied',async()=>status(await request('/api/providers/me',{token:tokens.company}),403));
let original;
await check('Provider reads own editor profile',async()=>{const r=await request('/api/providers/me',{token:tokens.ava});ok(r);assert.equal(r.data.id,'ava-martinez');original=r.data;});
if(original){
 await check('Cross-owner provider update rejected',async()=>{const r=await request('/api/providers/me',{method:'PUT',token:tokens.leo,body:{...original,id:'ava-martinez'}});assert.ok([403,409].includes(r.status),`Expected ownership denial, got ${r.status}`);});
 await check('Client provider update denied',async()=>status(await request('/api/providers/me',{method:'PUT',token:tokens.company,body:original}),403));
 await check('Negative provider price rejected',async()=>status(await request('/api/providers/me',{method:'PUT',token:tokens.ava,body:{...original,hourlyRate:-1}}),400));
 await check('Provider update survives subsequent independent read',async()=>{const headline=`Full-stack engineering · ${runId}`;const r=await request('/api/providers/me',{method:'PUT',token:tokens.ava,body:{...original,headline}});ok(r);const read=await request('/api/providers/ava-martinez');ok(read);assert.equal(read.data.headline,headline);});
 await check('Restore provider demonstration data',async()=>ok(await request('/api/providers/me',{method:'PUT',token:tokens.ava,body:original})));
}
const body={providerId:'ava-martinez',subject:`Java platform ${runId}`,message:'Please help build a secure Java platform and demonstrate deployment and delivery reliability.',budget:5000,clientType:'COMPANY'};
await check('Anonymous inquiry submission denied',async()=>status(await request('/api/inquiries',{method:'POST',body,key:randomUUID()}),401));
await check('Provider cannot submit client inquiry',async()=>status(await request('/api/inquiries',{method:'POST',token:tokens.leo,body,key:randomUUID()}),403));
await check('Invalid inquiry budget rejected',async()=>status(await request('/api/inquiries',{method:'POST',token:tokens.company,body:{...body,budget:-1},key:randomUUID()}),400));
await check('Missing target provider rejected',async()=>status(await request('/api/inquiries',{method:'POST',token:tokens.company,body:{...body,providerId:'no-such-provider'},key:randomUUID()}),404));
let companyInquiry;const companyKey=randomUUID();
await check('Company creates a durable inquiry',async()=>{const r=await request('/api/inquiries',{method:'POST',token:tokens.company,body,key:companyKey});ok(r);companyInquiry=r.data;assert.ok(companyInquiry.id);assert.equal(companyInquiry.providerId,'ava-martinez');});
if(companyInquiry){
 await check('Repeated submission returns same inquiry',async()=>{const r=await request('/api/inquiries',{method:'POST',token:tokens.company,body,key:companyKey});ok(r);assert.equal(r.data.id,companyInquiry.id);});
 await check('Changed payload with same key conflicts',async()=>status(await request('/api/inquiries',{method:'POST',token:tokens.company,body:{...body,subject:'Changed subject'},key:companyKey}),409));
 await check('Concurrent duplicate submissions converge',async()=>{const key=randomUUID();const rs=await Promise.all(Array.from({length:4},()=>request('/api/inquiries',{method:'POST',token:tokens.company,body:{...body,subject:`Concurrent ${runId}`},key})));rs.forEach(ok);assert.equal(new Set(rs.map(r=>r.data.id)).size,1);});
 await check('Sender can list persisted inquiry',async()=>{const r=await request('/api/inquiries',{token:tokens.company});ok(r);assert.ok(r.data.some(x=>x.id===companyInquiry.id));});
 await check('Other client cannot list inquiry',async()=>{const r=await request('/api/inquiries',{token:tokens.individual});ok(r);assert.ok(!r.data.some(x=>x.id===companyInquiry.id));});
 await check('Other provider cannot list inquiry',async()=>{const r=await request('/api/inquiries',{token:tokens.leo});ok(r);assert.ok(!r.data.some(x=>x.id===companyInquiry.id));});
 await check('Other provider cannot change inquiry',async()=>{const r=await request(`/api/inquiries/${companyInquiry.id}/status`,{method:'PATCH',token:tokens.leo,body:{status:'ACCEPTED'}});assert.ok([403,404].includes(r.status));});
 await check('Sender cannot accept own inquiry',async()=>status(await request(`/api/inquiries/${companyInquiry.id}/status`,{method:'PATCH',token:tokens.company,body:{status:'ACCEPTED'}}),403));
 await check('Target provider accepts inquiry',async()=>{const r=await request(`/api/inquiries/${companyInquiry.id}/status`,{method:'PATCH',token:tokens.ava,body:{status:'ACCEPTED'}});ok(r);assert.equal(r.data.status,'ACCEPTED');});
 await check('Client sees persisted acceptance',async()=>{const r=await request('/api/inquiries',{token:tokens.company});ok(r);assert.equal(r.data.find(x=>x.id===companyInquiry.id)?.status,'ACCEPTED');});
 await check('Invalid status rejected',async()=>status(await request(`/api/inquiries/${companyInquiry.id}/status`,{method:'PATCH',token:tokens.ava,body:{status:'HACKED'}}),400));
 let notification;
 await check('Kafka eventually delivers provider notification',async()=>{for(let i=0;i<25;i++){const r=await request('/api/notifications',{token:tokens.ava});ok(r);notification=r.data.find(x=>x.inquiryId===companyInquiry.id);if(notification)return;await new Promise(r=>setTimeout(r,800));}assert.ok(notification,'Notification not delivered within 20s');});
 if(notification){
  await check('Other provider cannot mark notification read',async()=>{const r=await request(`/api/notifications/${notification.id}/read`,{method:'PATCH',token:tokens.leo});assert.ok([403,404].includes(r.status));});
  await check('Recipient marks notification read durably',async()=>{ok(await request(`/api/notifications/${notification.id}/read`,{method:'PATCH',token:tokens.ava}));const r=await request('/api/notifications',{token:tokens.ava});ok(r);assert.equal(r.data.find(x=>x.id===notification.id)?.read,true);});
 }
}
let individualInquiry;
await check('Individual creates inquiry',async()=>{const r=await request('/api/inquiries',{method:'POST',token:tokens.individual,body:{...body,subject:`Individual ${runId}`,clientType:'INDIVIDUAL'},key:randomUUID()});ok(r);individualInquiry=r.data;assert.equal(r.data.clientType,'INDIVIDUAL');});
if(individualInquiry)await check('Target provider declines individual inquiry',async()=>{const r=await request(`/api/inquiries/${individualInquiry.id}/status`,{method:'PATCH',token:tokens.ava,body:{status:'DECLINED'}});ok(r);assert.equal(r.data.status,'DECLINED');});
await check('Anonymous inquiries and notifications denied',async()=>{status(await request('/api/inquiries'),401);status(await request('/api/notifications'),401);});
const report={runId,base,expected:48,completedAt:new Date().toISOString(),passed:results.filter(x=>x.status==='PASS').length,failed:results.filter(x=>x.status==='FAIL').length,createdInquiryIds:[companyInquiry?.id,individualInquiry?.id].filter(Boolean),results};
if(output){await mkdir(dirname(output),{recursive:true});await writeFile(output,JSON.stringify(report,null,2)+'\n');}
console.log(JSON.stringify({runId,passed:report.passed,failed:report.failed,createdInquiryIds:report.createdInquiryIds}));
if(report.failed || report.passed!==48 || results.length!==48){console.error(`Acceptance gate requires exactly48 passes; observed ${report.passed} passes / ${report.failed} failures / ${results.length} executed`);process.exitCode=1;}
