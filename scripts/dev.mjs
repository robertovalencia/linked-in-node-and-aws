import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const secrets=Object.fromEntries(readFileSync(resolve(root,'.env'),'utf8').split('\n').filter(l=>l&&!l.startsWith('#')).map(l=>{const i=l.indexOf('=');return [l.slice(0,i),l.slice(i+1)];}));
const children=[];
for (const [index,service] of ['identity','catalog','inquiries','notifications'].entries()) {
  const env={...process.env,...secrets,SEED_DEMO:'true',INSPECT_PORT:String(9229+index),SERVICE:service,PORT:String(8181+index),DB_URL:`postgresql://${service}:${secrets[`${service.toUpperCase()}_DB_PASSWORD`]}@127.0.0.1:55432/${service}`,CATALOG_URL:'http://127.0.0.1:8182',KAFKA_BROKERS:'127.0.0.1:19092'};
  children.push(spawn('npm',['run',`dev:${service}`],{cwd:resolve(root,'backend'),env,stdio:'inherit',detached:process.platform!=='win32'}));
}
children.push(spawn('npm',['run','dev'],{cwd:resolve(root,'frontend'),env:process.env,stdio:'inherit',detached:process.platform!=='win32',detached:process.platform!=='win32'}));
let stopping=false;
function stop(code=0){if(stopping)return;stopping=true;for(const child of children){try{if(process.platform!=='win32')process.kill(-child.pid,'SIGTERM');else child.kill('SIGTERM');}catch{}}setTimeout(()=>process.exit(code),600).unref();}
for (const child of children) child.on('exit',code=>{if(!stopping&&code!==0)stop(code??1);});
process.on('SIGINT',()=>stop());process.on('SIGTERM',()=>stop());
