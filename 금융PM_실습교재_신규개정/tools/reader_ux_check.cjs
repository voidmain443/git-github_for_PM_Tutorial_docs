const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');

// The chapter is the default reading path; simulations are optional at ten
// selected practice steps. Use the same API and repository prefix as Pages.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[],visualRequests=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 page.on('request',request=>{
  if(/\/(?:visual(?:-[^/]+)?\.(?:html|mjs|css)|vendor\/d3[^/]*)/.test(new URL(request.url()).pathname))visualRequests.push(request.url());
 });
 const rank=Object.fromEntries(['S0','S0A','S1','S1A','S2','S3','S4'].map((s,i)=>[s,i]));
 const anchors=['sources','charter-10','5.2','6.5','7.3','11.4','12.2','9.3','4.6','5.5'];
 const labs=['workflow','charter','scope','schedule','cost','risk','procurement','integration','change','closure'];

 async function ready(){await page.waitForSelector('#chapter-title',{state:'attached'});}
 async function stage(value){
  await page.evaluate(stage=>PMApp.api('/api/stage',{body:JSON.stringify({stage})}),value);
  await page.reload();await ready();
  check('reader UX uses stage '+value,(await page.locator('#stage-caption').innerText()).includes(value));
 }
 async function unit(value){
  await page.selectOption('#unit',String(value));await page.locator('#open').click();
  await page.waitForFunction(value=>new URLSearchParams(location.search).get('unit')===String(value),value);
  await page.locator('#chapter-view').waitFor({state:'visible'});
 }
 async function mode(value){
  await page.locator(`#reader-view [data-view="${value}"]`).click();
  await page.locator(value==='chapter'?'#chapter-view':'#practice-view').waitFor({state:'visible'});
 }
 async function phase(value){
  await page.locator(`[data-phase="${value}"][role="tab"]`).click();
  check('reader phase '+value+' is selected',await page.locator(`[data-phase="${value}"][role="tab"]`).getAttribute('aria-selected')==='true');
  check('one practice phase is visible',await page.locator('.step-phase-panel:visible').count()===1);
 }
 async function step(index){
  await page.locator(`.outline [data-step="${index}"]`).click();
  await page.waitForFunction(index=>document.querySelector(`.outline [data-step="${index}"]`)?.getAttribute('aria-current')==='step',index);
 }
 async function lesson(value){return page.evaluate(value=>PMApp.api('/api/lesson?unit='+value),value);}
 const fits=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);

 try{
  await page.goto(base+'learn.html?unit=0');await ready();await stage('S0');
  check('chapter reading is the default',await page.locator('#chapter-view').isVisible()&&await page.locator('#practice-view').isHidden());
  check('default reading does not preload a simulation',visualRequests.length===0&&await page.locator('#study-frame').count()===0);
  const start=await lesson(0),guide=start.unitGuide;
  check('unit zero has a mission and handoff',typeof guide.mission==='string'&&guide.mission.length>0&&typeof guide.handoff==='string'&&guide.handoff.length>0);
  check('unit zero introduces preparation and outcomes',guide.prerequisites.length===3&&guide.outcomes.length===3);
  check('unit zero has six authored chapter sections',guide.sections.length===6&&guide.sections.every(s=>s.body&&s.html&&!s.locked));
  check('the whole chapter is readable without expanding a details element',await page.locator('#chapter-view .chapter-section:visible').count()===6);
  const chapterText=await page.locator('#chapter-view').innerText();
  check('chapter shows its mission and six section titles',chapterText.includes(guide.mission)&&guide.sections.every(s=>chapterText.includes(s.title)));

  await page.locator('#chapter-to-practice').click();await page.locator('#practice-view').waitFor({state:'visible'});
  check('practice replaces rather than duplicates chapter reading',await page.locator('#chapter-view').isHidden());
  await step(0);await phase('concept');
  check('concept phase keeps source and writing tools out of the way',await page.locator('[data-source]:visible').count()===0&&await page.locator('#study-writing:visible').count()===0);
  check('non-anchor step offers no repeated simulation',await page.locator('#study-simulation').count()===0);
  await phase('evidence');
  check('evidence phase exposes the actual source buttons',await page.locator('[data-source]:visible').count()>0);
  await page.locator('[data-source]:visible').first().click();await page.locator('#source-panel').waitFor({state:'visible'});
  check('source evidence remains available in its phase',(await page.locator('#source-panel').innerText()).length>60);
  await phase('practice');
  check('practice phase provides the self-check and optional worksheet',await page.locator('#study-quiz').isVisible()&&await page.locator('#study-writing').isVisible());
  check('source content is hidden when writing and reviewing',await page.locator('#source-panel').isHidden());
  // No answer, worksheet entry or completion checkbox is needed to move on.
  await page.locator('.paging [data-step="1"]').click();
  check('next step needs no forced completion',(await page.locator('#step-title').innerText())===start.guideSteps[1].title);
  await page.locator('.paging [data-step="0"]').click();
  check('previous step restores the earlier task',(await page.locator('#step-title').innerText())===start.guideSteps[0].title);
  await phase('practice');
  await page.locator('#study-writing > summary').click();await page.locator('#study-load').click();
  await page.waitForFunction(()=>document.querySelector('#study-editor')?.value.length>0);
  const memoryMarker='단원 이동 후에도 유지할 학습자 근거 메모';
  await page.locator('#study-preview textarea[data-cell]').first().fill(memoryMarker);
  const [saved]=await Promise.all([page.waitForEvent('download'),page.locator('#study-export').click()]);
  check('optional draft can be saved before changing units',(await fs.promises.readFile(await saved.path(),'utf8')).includes(memoryMarker));
  await mode('chapter');
  await page.locator('#unit-next').click();await page.waitForFunction(()=>new URLSearchParams(location.search).get('unit')==='1');
  check('next unit starts with its chapter',await page.locator('#chapter-view').isVisible()&&await page.locator('#practice-view').isHidden());
  await page.locator('#unit-prev').click();await page.waitForFunction(()=>new URLSearchParams(location.search).get('unit')==='0');
  check('previous unit returns without leaving the reader',page.url().includes('learn.html')&&await page.locator('#chapter-view').isVisible());
  await mode('practice');await phase('practice');await page.locator('#study-writing > summary').click();
  await page.locator('#study-load').click();
  check('same-page unit navigation retains the optional draft',(await page.locator('#study-editor').inputValue()).includes(memoryMarker));
  await mode('chapter');

  // Review data boundaries across every source stage before rendering all ten
  // chapters. Hidden sections must lose their bodies in JSON, not only in CSS.
  const releases=await page.evaluate(async()=>{
   const result=[];
   for(const stage of ['S0','S0A','S1','S1A','S2','S3','S4']){
    await PMApp.api('/api/stage',{body:JSON.stringify({stage})});
    for(let unit=0;unit<10;unit++)result.push({stage,unit,lesson:await PMApp.api('/api/lesson?unit='+unit)});
   }
   return result;
  });
  for(const release of releases){
   const sections=release.lesson.unitGuide.sections;
   check('chapter release boundary '+release.stage+' unit '+release.unit,sections.length===6&&sections.every(section=>
    rank[section.stage]>rank[release.stage]?
     section.locked&&Object.keys(section).every(key=>['id','title','stage','locked'].includes(key)):
     !section.locked&&typeof section.body==='string'&&section.body.trim().length>0&&typeof section.html==='string'&&section.html.trim().length>0));
  }
  const full=releases.filter(r=>r.stage==='S4').map(r=>r.lesson);
  check('chapter section identifiers are unique within each unit',full.every(l=>new Set(l.unitGuide.sections.map(s=>s.id)).size===6));
  for(let u=0;u<10;u++){
   const l=full[u],selected=l.guideSteps.filter(s=>s.visualAid);
   check('unit '+u+' has only its intended visual anchor',selected.length===1&&selected[0].id===anchors[u]&&selected[0].visualAid.lab===labs[u]&&selected[0].visualAid.purpose.trim().length>0);
   check('unit '+u+' explains the optional visual purpose',l.visualAnchor.stepId===anchors[u]&&l.visualAnchor.lab===labs[u]&&l.visualAnchor.title&&l.visualAnchor.purpose);
  }

  await stage('S0');await unit(9);
  const early=await lesson(9),earlyText=await page.locator('#chapter-view').innerText(),closed=early.unitGuide.sections.filter(s=>s.locked);
  check('future chapter sections explain their lock',closed.length>0&&await page.locator('#chapter-view .chapter-lock').count()===closed.length);
  check('future chapter retains navigable section titles',closed.every(s=>earlyText.includes(s.title)));
  const finalSection=full[9].unitGuide.sections.find(s=>s.stage==='S4');
  assert(finalSection,'unit nine has a closing-stage section');
  check('S0 chapter does not display future closing prose',!earlyText.includes(finalSection.body.trim().slice(0,80)));
  check('future material is distinguished from required student completion',!/(학습을 완료해야|정답을 맞혀야|필수 입력을 완료)/.test(earlyText));

  // Integration playback is recommended only with its S2 execution evidence,
  // never at the earlier kickoff task or by silently opening a future snapshot.
  await stage('S1A');await unit(7);await mode('practice');
  await step(full[7].guideSteps.findIndex(s=>s.id==='4.3'));await phase('evidence');
  check('kickoff task does not recommend a future visual',await page.locator('#study-simulation').count()===0&&await page.locator('#study-frame').count()===0);
  const kickoff=await lesson(7),execution=kickoff.guideSteps.find(s=>s.id==='9.3');
  check('execution visual anchor remains locked before S2',execution.locked&&!execution.html&&!execution.visualAid);
  await step(full[7].guideSteps.findIndex(s=>s.id==='9.3'));
  check('locked execution task creates no active visual',await page.locator('#study-simulation').count()===0&&await page.locator('#study-frame').count()===0);
  check('browsing future execution does not advance the ERP snapshot',(await page.evaluate(()=>PMApp.api('/api/meta'))).stage==='S1A');

  await stage('S4');
  for(let u=0;u<10;u++){
   await unit(u);
   check('unit '+u+' full chapter is visible',await page.locator('#chapter-view .chapter-section:visible').count()===6&&await page.locator('#chapter-view .chapter-lock').count()===0);
   check('unit '+u+' prose is present',full[u].unitGuide.sections.every(s=>s.body.trim().length>=200));
   await mode('practice');
   const index=full[u].guideSteps.findIndex(s=>s.id===anchors[u]);await step(index);await phase('evidence');
   check('unit '+u+' visual stays closed by default',await page.locator('#study-simulation').evaluate(el=>!el.open));
   check('unit '+u+' does not preload its recommended visual',await page.locator('#study-frame').count()===0);
   const other=full[u].guideSteps.findIndex(s=>s.id!==anchors[u]);await step(other);
   check('unit '+u+' does not repeat the visual on other tasks',await page.locator('#study-simulation').count()===0);
  }
  check('reading every unit and task loads no visual assets',visualRequests.length===0);

  await unit(0);await mode('practice');await step(full[0].guideSteps.findIndex(s=>s.id==='sources'));await phase('evidence');
  await page.locator('#study-simulation > summary').click();
  const frameElement=page.locator('#study-frame');await frameElement.waitFor();await frameElement.scrollIntoViewIfNeeded();
  const frame=await(await frameElement.elementHandle()).contentFrame();assert(frame,'selected optional simulation exists');
  await frame.waitForSelector('[data-flow]');
  check('explicit choice loads the selected simulation',visualRequests.some(url=>url.includes('visual.html?lab=workflow'))&&await frame.locator('[data-flow]').count()===5);
  await page.locator('#study-simulation > summary').click();
  await page.waitForFunction(()=>{const f=document.querySelector('#study-frame');return !f||!f.getAttribute('src');});
  check('closing the optional visual removes its running document',await page.evaluate(()=>{const f=document.querySelector('#study-frame');return !f||!f.getAttribute('src');}));

  await page.setViewportSize({width:390,height:844});await mode('chapter');
  check('chapter fits a narrow mobile viewport',await fits());
  await page.screenshot({path:path.join(root,'검증/Pages_통독교재_모바일.png'),fullPage:true});
  await page.locator('#chapter-to-practice').click();
  for(const value of ['concept','evidence','practice']){await phase(value);check('mobile '+value+' phase fits',await fits());}
  await page.screenshot({path:path.join(root,'검증/Pages_과업단계_모바일.png'),fullPage:true});
  await mode('chapter');await page.locator('#unit-next').click();
  await page.waitForFunction(()=>new URLSearchParams(location.search).get('unit')==='1');
  check('mobile next-unit navigation starts reading mode',await page.locator('#chapter-view').isVisible()&&await fits());
  await page.locator('#unit-prev').click();await page.waitForFunction(()=>new URLSearchParams(location.search).get('unit')==='0');
  check('mobile previous-unit navigation works',await page.locator('#chapter-view').isVisible());
  await page.goto(base+'learn.html?unit=3&view=practice');await ready();
  check('a direct practice link keeps the requested mode',await page.locator('#practice-view').isVisible()&&await page.locator('#chapter-view').isHidden());
  check('reader UX has no page errors',errors.length===0);check('reader UX has no failed assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();}
};
