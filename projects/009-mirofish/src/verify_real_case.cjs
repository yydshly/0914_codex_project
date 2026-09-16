const { chromium } = require('../.cache/qa/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
 const errors=[];let checks=0;
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 const verify=(ok,message)=>{assert.ok(ok,message);checks++;};
 try{
  await page.goto('http://127.0.0.1:8079/',{waitUntil:'networkidle'});
  verify(await page.locator('#real-case-title').isVisible(),'Real case visible');
  verify(await page.locator('.case-timeline article').count()===3,'Three dated historical entries');
  for(const [key,text] of [['price','费用降下来'],['terms','规则保障说清楚'],['model','改回订阅']]){
   await page.locator(`[data-plan="${key}"]`).click();
   verify((await page.locator('#case-plan-result').innerText()).includes(text),`Correct plan ${key}`);
   verify(await page.locator('.case-plan-buttons [aria-pressed=true]').count()===1,'Exactly one plan selected');
  }
  await page.locator('[data-plan="price"]').focus();await page.keyboard.press('Enter');
  verify(await page.locator('[data-plan="price"]').getAttribute('aria-pressed')==='true','Keyboard plan selection');
  for(const file of ['unity-seed.md','unity-experiment.md']){
   const event=page.waitForEvent('download');await page.locator(`a[download][href$="${file}"]`).click();
   const download=await event,body=await fs.readFile(await download.path(),'utf8');
   verify(body.includes('2023-09-22') && body.length>500,`Download ${file}`);
  }
  await page.locator('[data-plan="terms"]').click();
  for(const width of [1440,900,390,320]){
   await page.setViewportSize({width,height:1100});
   verify(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`No overflow ${width}`);
   await page.locator('[data-plan="model"]').click();
   verify((await page.locator('#case-plan-result').innerText()).includes('改回订阅'),`Plan works ${width}`);
   if(width===390)await page.locator('#real-case').screenshot({path:path.join(root,'.cache','real-case-mobile.png')});
  }
  await page.setViewportSize({width:1440,height:1100});
  await page.locator('[data-plan="terms"]').click();
  await page.locator('#real-case-title').click();
  await page.locator('#real-case').screenshot({path:path.join(root,'assets','unity-real-case.png')});
  await page.locator('[data-scenario="crisis"]').click();await page.locator('[data-step="2"]').click();
  verify(await page.locator('.post').count()===4,'Existing timeline works');
  await page.locator('[data-step="4"]').click();
  verify(await page.locator('#interview-answer').isVisible(),'Existing interview works');
  verify(errors.length===0,errors.join('; '));
  const result={date:'2026-09-16',checks,passed:true,viewports:[1440,900,390,320],errors,scope:'Real historical case presentation and proposed experiments; no model simulation'};
  await fs.writeFile(path.join(root,'notes','real-case-ui-checks.json'),JSON.stringify(result,null,2)+'\n');console.log(result);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
