/* Optional browser QA. npm install --prefix .cache/qa --ignore-scripts playwright */
const { chromium } = require('../.cache/qa/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch({channel:process.env.QA_BROWSER_CHANNEL || 'chrome',headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
  const errors=[], requests=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('response',response=>{if(response.status()>=400)errors.push(`${response.status()} ${response.url()}`);});
  page.on('request',request=>requests.push(request.url()));
  let checks=0;
  const verify=(value,message)=>{assert.ok(value,message);checks++;};
  try {
    await page.goto(process.env.QA_URL || 'http://127.0.0.1:8079/',{waitUntil:'networkidle'});
    verify((await page.title()).includes('MiroFish'),'Page title');
    verify(await page.locator('[data-actor]').count()===6,'Six graph actors');
    for(const scenario of ['pricing','crisis','story']){
      await page.locator(`[data-scenario="${scenario}"]`).click();
      verify(await page.locator('[data-step="0"]').getAttribute('aria-pressed')==='true','Scenario resets stage');
      for(const strategy of ['baseline','response']){
        await page.locator('#strategy').selectOption(strategy);
        await page.locator('[data-step="1"]').click();
        verify(await page.locator('.config-grid article').count()===3,'Environment setup cards');
        await page.locator('[data-step="2"]').click();
        await page.locator('#round').fill('0');
        verify(await page.locator('.hidden-round').count()===3,'Timeline hides future rounds');
        await page.locator('#round').fill('3');
        verify(await page.locator('.post').count()===4 && await page.locator('.hidden-round').count()===0,'All events visible');
        const expected=await page.evaluate(({scenario,strategy})=>window.MIRO_SCENARIOS[scenario].events[strategy][3].text,{scenario,strategy});
        verify((await page.locator('#timeline').innerText()).includes(expected),'Correct branch event');
        await page.locator('[data-step="3"]').click();
        verify(await page.locator('.report-grid article').count()===3,'Report observations, risks, validation');
        const downloadEvent=page.waitForEvent('download');
        await page.locator('#download').click();
        const download=await downloadEvent;
        const body=await fs.readFile(await download.path(),'utf8');
        verify(body.includes('人工编写') && body.includes(expected) && download.suggestedFilename().includes(strategy),'Export branch and disclosure');
        await page.locator('[data-step="4"]').click();
        for(let actor=0;actor<6;actor++){
          await page.locator('#interview-actor').selectOption(String(actor));
          for(let question=0;question<3;question++){
            await page.locator(`[data-question="${question}"]`).click();
            const answer=await page.evaluate(({scenario,actor,question})=>{const a=window.MIRO_SCENARIOS[scenario].actors[actor];return[a.motive,a.influence,a.proof][question];},{scenario,actor,question});
            verify(await page.locator('#interview-answer').innerText()===answer,'Preset interview answer');
          }
        }
      }
    }
    await page.locator('[data-scenario="pricing"]').click();
    await page.locator('[data-actor="3"]').focus();await page.keyboard.press('Enter');
    verify(await page.locator('#role-name').innerText()==='团队采购','Keyboard graph selection');
    await page.locator('#next').click();await page.locator('#previous').click();
    verify(await page.locator('#previous').isDisabled(),'Previous disabled at start');
    await page.clock.install();
    await page.locator('#play').click();await page.clock.fastForward(4700);
    verify(await page.locator('[data-step="1"]').getAttribute('aria-pressed')==='true','Playback advances');
    await page.locator('#play').click();await page.clock.fastForward(5000);
    verify(await page.locator('[data-step="1"]').getAttribute('aria-pressed')==='true','Pause holds stage');
    await page.locator('#reset').click();
    verify(await page.locator('#strategy').inputValue()==='baseline','Reset restores branch');
    await page.locator('[data-step="2"]').click();
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(root,'assets','cover.png')});
    for(const width of [1440,900,390,320]){
      await page.setViewportSize({width,height:1000});
      verify(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`No horizontal overflow at ${width}`);
      await page.locator('[data-step="4"]').click();
      await page.locator('#interview-actor').selectOption('2');
      verify(await page.locator('#interview-answer').isVisible(),`Interview usable at ${width}`);
      if(width===390){await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(root,'.cache','mobile.png'),fullPage:true});}
    }
    await page.setViewportSize({width:1440,height:1050});
    await page.locator('[data-step="2"]').click();
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(root,'.cache','desktop-full.png'),fullPage:true});
    verify(await page.locator('img').evaluateAll(images=>images.every(img=>img.complete&&img.naturalWidth>0)),'All images loaded');
    verify(errors.length===0,`Browser errors: ${errors.join('; ')}`);
    verify(requests.every(url=>url.startsWith('http://127.0.0.1:8079/')),'No external runtime requests');
    const result={date:'2026-09-16',checks,passed:true,browser:'Chromium via '+(process.env.QA_BROWSER_CHANNEL||'chrome'),viewports:[1440,900,390,320],errors,scope:'Independent teaching exhibit, not upstream simulation'};
    await fs.writeFile(path.join(root,'notes','ui-checks.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result,null,2));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
