import assert from 'node:assert/strict';
import { mkdir, writeFile } from 'node:fs/promises';
import { chromium } from 'playwright';
const base=process.argv[2]||'http://127.0.0.1:8180';
const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
const results=[];
await mkdir('docs/evidence/browser',{recursive:true});
try {
 for(const [name,width,height]of[['desktop',1440,1000],['mobile',390,844]]){
  const context=await browser.newContext({viewport:{width,height}});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('.provider-card').first().waitFor();
  assert.ok(await page.locator('.provider-card').count()>=6);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:`docs/evidence/browser/${name}-discovery.png`,fullPage:true});
  await page.getByRole('button',{name:'Add Ava Martinez to comparison',exact:true}).click();
  await page.getByRole('button',{name:/Add Leo Chen to comparison/}).click();
  await page.locator('.compare-bar').getByRole('button',{name:'Compare',exact:true}).click();
  await page.getByRole('dialog').getByText('Ava Martinez',{exact:true}).waitFor();
  await page.screenshot({path:`docs/evidence/browser/${name}-compare.png`,fullPage:true});
  await page.getByRole('dialog').getByRole('button',{name:/Close/}).click();
  await page.getByRole('button',{name:'View Ava Martinez profile',exact:true}).click();
  await page.getByRole('dialog').getByText('Selected work',{exact:true}).waitFor();
  await page.screenshot({path:`docs/evidence/browser/${name}-profile.png`,fullPage:true});
  await page.getByRole('dialog').getByRole('button',{name:'Send inquiry',exact:true}).first().click();
  const login=page.getByRole('dialog').filter({has:page.getByRole('heading',{name:'Welcome back.'})});
  await login.getByRole('button',{name:/Sign in/}).click();
  const form=page.getByRole('dialog').filter({has:page.getByRole('heading',{name:/Let.s work with Ava/})});
  await form.getByLabel('Project title').fill(`Browser ${name} ${Date.now()}`);
  await form.getByLabel('Tell them about your project').fill('Please implement a secure customer portal with tested deployment and durable notifications.');
  await form.getByLabel('Estimated budget').fill('2500');
  await form.getByRole('button',{name:/Send inquiry/}).click();
  await page.getByText('Your inquiry was sent. Follow its status in your inbox.',{exact:true}).waitFor();
  assert.deepEqual(errors,[]);results.push({name,status:'PASS',checks:['six-persisted-providers','no-horizontal-overflow','compare-two-profiles','rich-profile','client-login','durable-inquiry','no-browser-errors']});
  await context.close();
 }
}finally{await browser.close();await writeFile('docs/evidence/browser-smoke.json',JSON.stringify({completedAt:new Date().toISOString(),base,results},null,2)+'\n');}
console.log(JSON.stringify({passed:results.length,failed:0}));
