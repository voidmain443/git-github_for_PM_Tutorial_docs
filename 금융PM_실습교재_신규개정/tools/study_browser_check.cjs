const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');

// Runs inside the Pages test context; the base URL may contain a repository prefix.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[],dialogs=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)failed.push(r.url());});
 page.on('dialog',async dialog=>{dialogs.push(dialog.type());await dialog.accept();});

 async function ready(){await page.waitForSelector('#step-title');}
 async function stage(value){
  await page.evaluate(stage=>PMApp.api('/api/stage',{body:JSON.stringify({stage})}),value);
  await page.reload();await page.locator('[data-view=practice]').click();await ready();
  check('study stage '+value,(await page.locator('#stage-caption').innerText()).includes(value));
 }
 async function unit(value){
  await page.selectOption('#unit',String(value));await page.locator('#open').click();
  await page.waitForFunction(value=>document.querySelector('.outline h2')?.textContent.startsWith(value+'.'),String(value));
  await page.locator('[data-view=practice]').click();await ready();
 }
 async function details(id){
  const panel=page.locator('#'+id);await panel.waitFor();
  if(!await panel.evaluate(el=>el.open))await panel.locator(':scope > summary').click();
  return panel;
 }
 async function firstStep(){await page.locator('.outline [data-step="0"]').click();}
 async function writing(){
  await page.locator('[data-phase=practice]').click();
  await details('study-writing');
  const option=await page.locator('#study-template option').evaluateAll(options=>options.find(o=>o.textContent.includes('D01'))?.value);
  assert(option,'D01 template option exists');
  await page.selectOption('#study-template',option);await page.locator('#study-load').click();
  await page.waitForFunction(()=>document.querySelector('#study-editor')?.value.includes('헌장'));
  return page.locator('#study-editor');
 }
 async function frameReady(){
  const iframe=page.locator('#study-simulation iframe');await iframe.waitFor();
  await iframe.scrollIntoViewIfNeeded();
  const frame=await (await iframe.elementHandle()).contentFrame();
  assert(frame,'embedded simulation frame exists');
  await frame.waitForFunction(()=>document.querySelector('#wb-stage-open')&&!document.querySelector('#wb-stage-open').disabled&&document.querySelector('#wb-content .wb-intro'));
  return frame;
 }
 const fits=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);

 try{
  await page.goto(base+'learn.html?view=practice&unit=0');await ready();
  await page.evaluate(()=>localStorage.removeItem('moapay.pm.reader.positions'));
  await stage('S0');await firstStep();
  await page.locator('[data-phase=practice]').click();
  check('study question offers choices',await page.locator('#study-quiz [data-answer]').count()>=2);
  await page.locator('#study-quiz [data-answer]').first().click();
  await page.locator('#study-feedback').waitFor({state:'visible'});
  check('study answer has explanatory feedback',(await page.locator('#study-feedback').innerText()).trim().length>25);

  const initial=await page.evaluate(()=>PMApp.api('/api/lesson?unit=0'));
  await page.locator('[data-view=chapter]').click();
  const chapterText=await page.locator('#chapter-view').innerText();
  check('whole chapter includes all available reading sections',initial.unitGuide.sections.filter(s=>!s.locked).every(s=>chapterText.includes(s.title)));
  check('whole chapter contains substantial authored prose',chapterText.length>1500);
  await page.locator('[data-view=practice]').click();
  await page.locator('.outline [data-step="'+initial.guideSteps.findIndex(s=>s.visualAid)+'"]').click();
  await page.locator('[data-phase=evidence]').click();
  await details('study-simulation');
  const embedded=await frameReady();
  check('embedded workflow follows parent S0',(await embedded.locator('#wb-stage-label').innerText()).includes('S0'));
  check('embedded workflow has source-connected steps',await embedded.locator('[data-flow]').count()===5);
  check('embedded workflow has a readable SVG',await embedded.locator('#wb-content svg[role="img"]').count()>0);
  await embedded.locator('[data-flow="3"]').click();
  check('embedded simulation can be used inside the chapter',(await embedded.locator('#flow-detail').innerText()).includes('불일치'));

  await unit(1);await firstStep();
  let editor=await writing();
  check('workbook opens an editable table',await page.locator('#study-preview table').count()>0&&await page.locator('#study-preview [data-cell]').count()>0);
  const cellText='학습자 검증: 측정 기간을 원천자료에서 확인합니다.';
  await page.locator('#study-preview textarea[data-cell]').first().fill(cellText);
  check('visual workbook cell updates the Markdown',(await editor.inputValue()).includes(cellText));
  await details('study-markdown');
  const marker='PM-STUDY-ROUNDTRIP-20260924';
  const draft=(await editor.inputValue())+'\n\n## 나의 판단\n'+marker+'\n';
  await editor.fill(draft);
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#study-export').click()]);
  const exported=await fs.promises.readFile(await download.path(),'utf8');
  check('workbook exports edited Korean Markdown',download.suggestedFilename().endsWith('.md')&&exported.includes(marker)&&exported.includes(cellText));

  await page.locator('.outline [data-step="1"]').click();await firstStep();editor=await writing();
  check('same document survives a step change',(await editor.inputValue()).includes(marker));
  const imported=exported+'\n불러온 초안에서 보완한 검토 근거입니다.\n';
  await page.locator('#study-import').setInputFiles({name:'D01_학습자_초안.md',mimeType:'text/markdown',buffer:Buffer.from(imported,'utf8')});
  await page.waitForFunction(()=>document.querySelector('#study-editor')?.value.includes('불러온 초안에서 보완한'));
  check('workbook imports an exported draft',(await editor.inputValue()).includes(marker));
  check('draft text is not written to browser storage',await page.evaluate(marker=>[localStorage,sessionStorage].every(storage=>Object.keys(storage).every(key=>!String(storage.getItem(key)).includes(marker))),marker));
  await details('study-markdown');
  await editor.fill(imported+'\n아직 파일로 보관하지 않은 변경입니다.\n');
  await page.reload();await ready();
  check('unsaved draft warns before leaving',dialogs.includes('beforeunload'));
  await firstStep();editor=await writing();
  check('a reload starts without retaining student draft',(await editor.inputValue()).includes(marker)===false);

  // Future stages must not leak new worked examples or quiz answers in the API or full chapter.
  for(const value of [8,9]){
   await unit(value);await firstStep();
   const locked=await page.evaluate(value=>PMApp.api('/api/lesson?unit='+value),value);
   check('S0 unit '+value+' protects future teaching data',locked.guideSteps.every(s=>s.locked&&!s.html&&!s.sections&&!s.selfCheck));
   await page.locator('[data-view=chapter]').click();const text=await page.locator('#chapter-view').innerText();
   check('S0 unit '+value+' explains the release boundary',/S[234]/.test(text)&&/(자료|공개|확인)/.test(text));
   check('S0 unit '+value+' has no future quiz answers',await page.locator('#study-quiz [data-answer]').count()===0);
   check('S0 unit '+value+' has no active future worksheet',await page.locator('#study-editor').count()===0);
  }

  await stage('S4');
  const all=await page.evaluate(async()=>{const out=[];for(let unit=0;unit<10;unit++)out.push(await PMApp.api('/api/lesson?unit='+unit));return out;});
  const steps=all.flatMap(lesson=>lesson.guideSteps);
  check('all 69 steps have explained three-choice self-checks',steps.length===69&&steps.every(s=>{
   const q=s.selfCheck;return q&&typeof q.question==='string'&&q.question.trim().length>0&&
    Array.isArray(q.options)&&q.options.length===3&&q.options.every(o=>typeof o==='string'&&o.trim())&&
    Number.isInteger(q.answer)&&q.answer>=0&&q.answer<q.options.length&&typeof q.explanation==='string'&&q.explanation.trim().length>25;
  }));
  for(let value=0;value<10;value++){
   await unit(value);await firstStep();await page.locator('[data-phase=practice]').click();
   check('unit '+value+' offers an in-page self-check',await page.locator('#study-quiz [data-answer]').count()>=2);
   await page.locator('[data-view=chapter]').click();const text=await page.locator('#chapter-view').innerText();
   check('unit '+value+' has full chapter reading',all[value].unitGuide.sections.every(s=>text.includes(s.title)));
   await page.locator('[data-view=practice]').click();
   await page.locator('.outline [data-step="'+all[value].guideSteps.findIndex(s=>s.visualAid)+'"]').click();
   await page.locator('[data-phase=evidence]').click();await details('study-simulation');const frame=await frameReady();
   check('unit '+value+' embeds its own simulation',(await frame.locator('.wb-intro .eyebrow').innerText()).includes('UNIT '+String(value).padStart(2,'0')));
   check('unit '+value+' embedded stage follows S4',(await frame.locator('#wb-stage-label').innerText()).includes('S4'));
  }

  await unit(0);await firstStep();await page.setViewportSize({width:390,height:844});
  await page.locator('.outline [data-step="'+all[0].guideSteps.findIndex(s=>s.visualAid)+'"]').click();
  await page.locator('[data-phase=evidence]').click();await details('study-simulation');
  const mobileFrame=await frameReady();
  check('optional simulation fits mobile',await fits());
  check('embedded simulation fits its mobile viewport',await mobileFrame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(root,'검증/Pages_통합교재_모바일.png'),fullPage:true});
  await unit(1);await firstStep();await writing();await details('study-markdown');
  check('visual worksheet and source editor fit mobile',await fits());
  await page.emulateMedia({reducedMotion:'reduce'});
  check('reduced motion preference is active',await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches));
  await page.locator('#study-quiz [data-answer]').first().click();
  check('self-check works with reduced motion',await page.locator('#study-feedback').isVisible());

  await page.goto(base+'visual.html?lab=workflow');
  await page.waitForFunction(()=>document.querySelector('#wb-stage-open')&&!document.querySelector('#wb-stage-open').disabled);
  const modules=await page.locator('[data-module]').evaluateAll(buttons=>buttons.map(button=>button.dataset.module));
  check('visual workbook covers ten distinct units',modules.length===10&&new Set(modules).size===10);
  for(const name of modules){
   await page.locator(`[data-module="${name}"]`).click();
   await page.waitForFunction(()=>!document.querySelector('#wb-stage-open').disabled);
   check('full visual module '+name+' has no error',!(await page.locator('#wb-error').innerText()).trim()&&await page.locator('.wb-lock').count()===0);
   check('full visual module '+name+' has teaching content',(await page.locator('#wb-content').innerText()).length>250);
   check('full visual module '+name+' has a diagram or data view',await page.locator('#wb-content svg, #wb-content table, #wb-content .wb-bars, #wb-content .wb-board, #wb-content .wb-lanes').count()>0);
   check('full visual module '+name+' links back to reading',await page.locator('#wb-content a[href*="learn.html?unit="]').count()>0);
   check('full visual module '+name+' fits mobile',await fits());
  }
  check('study has no browser exceptions',errors.length===0);
  check('study has no missing lesson or simulation assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();}
};
