const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');

// Exercise authored text and visible snapshots, not internal renderer helpers.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)failed.push(r.url());});
 page.on('dialog',dialog=>dialog.accept());
 const fits=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);
 const savedStage=()=>page.evaluate(()=>Object.fromEntries(Object.keys(localStorage).filter(k=>k.startsWith('moapay.pm.stage:')).map(k=>[k,localStorage.getItem(k)])));
 async function details(id){const el=page.locator('#'+id);if(!await el.evaluate(n=>n.open))await el.locator(':scope > summary').click();}
 async function download(button){const [file]=await Promise.all([page.waitForEvent('download'),page.locator(button).click()]);return {name:file.suggestedFilename(),text:await fs.promises.readFile(await file.path(),'utf8')};}
 async function workbookReady(){await page.waitForFunction(()=>document.querySelector('#wb-stage-open')&&!document.querySelector('#wb-stage-open').disabled);}
 async function stage(value){await page.selectOption('#wb-stage',value);await page.locator('#wb-stage-open').click();await workbookReady();}
 async function capture(){await page.locator('#wr-capture').click();await page.waitForFunction(()=>document.querySelector('#wr-export')&&!document.querySelector('#wr-export').disabled);}
 try{
  await page.goto(base+'learn.html?unit=1&view=practice&step=charter-1&phase=practice');
  await page.waitForSelector('#step-title');
  await page.evaluate(()=>PMApp.api('/api/stage',{body:JSON.stringify({stage:'S0'})}));
  await page.reload();await page.waitForSelector('#step-title');
  await page.locator('[data-phase=practice]').click();await details('study-writing');
  const template=await page.locator('#study-template option').evaluateAll(o=>o.find(n=>n.textContent.includes('D01'))?.value);
  assert(template,'D01 is available for the charter draft');
  await page.selectOption('#study-template',template);await page.locator('#study-load').click();
  await page.locator('#study-document-views').waitFor({state:'visible'});
  const draftStage=await savedStage();
  const originalSource=await page.evaluate(()=>PMApp.api('/api/detail?menu=documents&id=S01'));
  const value='QA 문서 근거 A | B\n<script>window.__documentInjected=1</script>';
  await page.locator('#study-preview textarea[data-cell]').first().fill(value);
  check('document table editing preserves literal pipe and line break in source',(await page.locator('#study-editor').inputValue()).includes(value.replace(/\|/g,'\\|').replace(/\n/g,'<br>')));
  await page.locator('#study-document-tab').click();
  check('document preview displays the edited table text',(await page.locator('#study-paper').innerText()).includes('QA 문서 근거 A | B'));
  check('document preview treats imported HTML as text',await page.locator('#study-paper script').count()===0&&await page.evaluate(()=>window.__documentInjected===undefined));
  check('document view is a labelled active tab',await page.locator('#study-document-tab').getAttribute('aria-selected')==='true'&&await page.locator('#study-document-panel').isVisible()&&await page.locator('#study-edit-panel').isHidden());
  await page.locator('#study-document-tab').focus();await page.keyboard.press('ArrowLeft');
  check('document view keyboard returns to editing',await page.evaluate(()=>document.activeElement?.id==='study-edit-tab')&&await page.locator('#study-edit-panel').isVisible());
  await details('study-markdown');
  const raw=[
   '# D01 검토 초안 · QA-DOCUMENT-ROUNDTRIP',
   '', '프로젝트: MP-01', '작성자: 학습자 <검토자>', '',
   '## 근거와 판단', '| 항목 | 내 판단 |', '| --- | --- |',
   '| 원천 S01 | 숫자와 권한을 **별도로 확인**한다. |',
   '| 미결 | [확인 필요] |', '',
   '## 검토 순서', '2. 원천 위치를 찾는다.', '3. 담당자에게 확인한다.', '',
   '[안전한 참고](https://example.org/reference)',
   '[실행 금지](javascript:alert(1))',
   '<img src=x onerror="window.__documentInjected=1">',
   '<script>window.__documentInjected=1</script>', '',
   '> 결정과 승인 기록은 아직 없다.', '',
  ].join('\n');
  await page.locator('#study-editor').fill(raw);
  await page.locator('#study-document-tab').click();
  check('raw draft becomes a structured document',await page.locator('#study-paper h1').innerText()==='D01 검토 초안 · QA-DOCUMENT-ROUNDTRIP'&&await page.locator('#study-paper table').count()===1&&await page.locator('#study-paper blockquote').count()===1);
  check('document renderer preserves intentional ordered numbering',await page.locator('#study-paper ol li').first().getAttribute('value')==='2');
  check('document renderer highlights unfilled source placeholders',await page.locator('#study-paper .study-paper-gap').innerText()==='[확인 필요]');
  check('document renderer never creates unsafe elements or links',await page.locator('#study-paper script,#study-paper img,#study-paper [onerror],#study-paper a[href^="javascript:"]').count()===0);
  const html=await download('#study-export-html');
  check('draft document HTML is a styled standalone file',html.name.endsWith('_문서.html')&&html.text.includes('<style>')&&html.text.includes('Content-Security-Policy'));
  const exported=await context.newPage();
  try{
   await exported.setContent(html.text);
   check('document HTML keeps the exact editable source',await exported.locator('.study-file-source pre').textContent()===raw);
   check('document HTML keeps the visible authored paragraph',(await exported.locator('.study-paper').innerText()).includes('결정과 승인 기록은 아직 없다.'));
   check('document HTML has no executable imported markup',await exported.locator('script,img,[onerror],a[href^="javascript:"]').count()===0&&await exported.evaluate(()=>window.__documentInjected===undefined));
   await exported.setViewportSize({width:390,height:844});
   check('standalone draft document fits a narrow screen',await exported.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  }finally{await exported.close();}
  // The editable file is the round-trip source; HTML is the sharing/print view.
  const markdown=await download('#study-export');
  check('Markdown export keeps the exact source',markdown.text===raw);
  const imported=raw+'\n불러온 검토 의견: 담당자·일자를 후속 확인한다.\n';
  await page.locator('#study-import').setInputFiles({name:'D01_작성본.md',mimeType:'text/markdown',buffer:Buffer.from(imported)});
  await page.waitForFunction(()=>document.querySelector('#study-editor')?.value.includes('불러온 검토 의견'));
  await page.locator('#study-document-tab').click();
  check('import immediately updates the formatted document',(await page.locator('#study-paper').innerText()).includes('불러온 검토 의견: 담당자·일자를 후속 확인한다.'));
  check('document drafting does not alter ERP source',JSON.stringify(await page.evaluate(()=>PMApp.api('/api/detail?menu=documents&id=S01')))===JSON.stringify(originalSource));
  check('document drafting does not change selected ERP stage',JSON.stringify(await savedStage())===JSON.stringify(draftStage));
  check('learner draft is not saved to browser storage',await page.evaluate(()=>[localStorage,sessionStorage].every(s=>Object.keys(s).every(k=>!s.getItem(k).includes('QA-DOCUMENT-ROUNDTRIP')))));
  await page.setViewportSize({width:390,height:844});
  check('document reading view fits mobile',await fits());
  await page.screenshot({path:path.join(root,'검증/Pages_작성문서_모바일.png'),fullPage:true});

  await page.setViewportSize({width:1440,height:1000});
  await page.goto(base+'visual.html?lab=schedule');await workbookReady();await stage('S0');
  check('future workbook cannot create a report',await page.locator('.wb-lock').count()===1&&await page.locator('#workbook-report').isHidden()&&await page.locator('#wr-capture').count()===0);
  await stage('S1');
  await page.locator('#workbook-report').waitFor({state:'visible'});
  const reportStage=await savedStage();
  const scheduleSource=await page.evaluate(()=>PMApp.api('/api/detail?menu=documents&id=S06'));
  check('report opens only after source stage is available',await page.locator('#wr-summary,#wr-analysis,#wr-recommendation,#wr-open').count()===4&&await page.locator('#wr-export').isDisabled());
  const notes={summary:'QA-REPORT-EXACT\n요약 <검토 초안> & 사실',analysis:'차트에서 읽은 사실이다.\n\n<script>window.__reportInjected=1</script>',recommendation:'승인 요청 전 <img src=x onerror="window.__reportInjected=1"> 조건을 확인한다.',open:'운영책임자에게 확인할 질문과 기한을 적는다.'};
  await page.locator('#wr-author').fill('학습자 <검토자>');await page.locator('#wr-version').fill('v0.2');
  for(const [id,text] of Object.entries(notes))await page.locator('#wr-'+id).fill(text);
  check('report capture does not reveal the schedule answer',await page.locator('#schedule-result').isHidden());
  await capture();
  check('unrevealed report includes only the source network',await page.locator('#wr-result svg').count()===1&&!(await page.locator('#wr-result').innerText()).includes('기술 작업 기간')&&!(await page.locator('#wr-result').innerText()).includes('총여유 0인 활동'));
  check('report records source identifiers and current conditions',(await page.locator('#wr-result').innerText()).includes('S06')&&(await page.locator('#wr-result').innerText()).includes('S02')&&(await page.locator('#wr-result').innerText()).includes('D · 외주 모듈 기간'));
  check('report status keeps draft separate from approval',(await page.locator('#wr-result .doc-state').innerText()).includes('미승인'));
  const beforeReveal=await download('#wr-export');
  check('unrevealed exported report excludes computed answer',!beforeReveal.text.includes('기술 작업 기간')&&!beforeReveal.text.includes('총여유 0인 활동'));
  await page.locator('#schedule-reveal').click();
  check('revealing new results invalidates the old report',await page.locator('#wr-export').isDisabled());
  await capture();
  check('revealed report includes network and Gantt SVG',await page.locator('#wr-result svg').count()===2&&(await page.locator('#wr-result').innerText()).includes('60영업일'));
  // Capturing a playing explanation must stop its timer without deleting the
  // controls or invalidating the newly captured result via queued mutations.
  await page.locator('.wb-playback [data-speed]').selectOption('3500');
  await page.locator('.wb-playback [data-play]').click();
  check('report regression starts actual continuous playback',await page.locator('.wb-playback [data-play]').getAttribute('aria-pressed')==='true');
  await capture();
  check('capture pauses playback and retains usable controls',await page.locator('.wb-playback [data-play]').getAttribute('aria-pressed')==='false'&&await page.locator('.wb-playback [data-next]').isEnabled());
  const pausedNarration=await page.locator('.wb-playback [data-narration]').innerText();
  await page.waitForTimeout(3700); // Beyond the chosen 3.5s timer, not an animation-frame assumption.
  check('captured report remains valid after the prior playback interval',await page.locator('#wr-export').isEnabled()&&await page.locator('.wb-playback [data-narration]').innerText()===pausedNarration);
  check('captured report excludes transient motion markers',await page.locator('#wr-result .wb-traveller').count()===0);

  await page.locator('#scenario-d').click();
  check('changed schedule disables report export until recapture',await page.locator('#wr-export').isDisabled()&&(await page.locator('#wr-status').innerText()).includes('이전 조건'));
  await capture();
  check('recaptured report contains the changed calculation',(await page.locator('#wr-result').innerText()).includes('65영업일')&&(await page.locator('#wr-result').innerText()).includes('D 25일'));
  const newSummary=notes.summary+'\n수정된 내 해석을 그대로 보관한다.';
  await page.locator('#wr-summary').fill(newSummary);
  check('author edits update report without invalidating fixed conditions',await page.locator('#wr-export').isEnabled()&&(await page.locator('#wr-result').innerText()).includes('수정된 내 해석을 그대로 보관한다.'));
  const report=await download('#wr-export');
  check('report export names its project module and source stage',report.name==='MP-01_schedule_S1_검토메모.html');
  const standalone=await context.newPage();
  try{
   await standalone.setContent(report.text);
   const reportText=await standalone.locator('.doc-captured-report').innerText();
   check('standalone report retains exact learner wording',Object.values({...notes,summary:newSummary}).every(t=>t.split('\n').filter(Boolean).every(line=>reportText.includes(line))));
   check('standalone report preserves source and current condition',reportText.includes('S06')&&reportText.includes('D 25일')&&reportText.includes('65영업일'));
   check('standalone report safely escapes author text',await standalone.locator('script,img,[onerror]').count()===0&&await standalone.evaluate(()=>window.__reportInjected===undefined));
   check('standalone report keeps actual SVG drawings',await standalone.locator('.doc-captured svg').count()===2);
   await standalone.setViewportSize({width:390,height:844});
   check('standalone report fits mobile',await standalone.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  }finally{await standalone.close();}
  check('capturing reports leaves ERP schedule data unchanged',JSON.stringify(await page.evaluate(()=>PMApp.api('/api/detail?menu=documents&id=S06')))===JSON.stringify(scheduleSource));
  check('capturing reports retains the chosen source stage',JSON.stringify(await savedStage())===JSON.stringify(reportStage));
  check('report text does not leak into browser storage',await page.evaluate(()=>[localStorage,sessionStorage].every(s=>Object.keys(s).every(k=>!s.getItem(k).includes('QA-REPORT-EXACT')))));
  await page.setViewportSize({width:390,height:844});
  check('workbook report composer fits mobile',await fits());
  await page.locator('#wr-capture').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>!document.querySelector('#wr-export').disabled);
  check('report capture works from the keyboard',await page.locator('#wr-result .pm-document').count()===1);
  await page.screenshot({path:path.join(root,'검증/Pages_실습검토문서_모바일.png'),fullPage:true});
  await page.locator('[data-module=change]').click();await workbookReady();
  check('switching to a locked module removes the report and prior snapshot',await page.locator('.wb-lock').count()===1&&await page.locator('#workbook-report').isHidden()&&await page.locator('#wr-result').count()===0);
  const galleryStage=await savedStage();
  await page.goto(base+'documents.html?doc=charter');
  await page.locator('#doc-paper .pm-document[data-kind=charter]').waitFor();
  check('gallery explains its independent fictional case',(await page.locator('.doc-studio-notice').innerText()).includes('PREVIEW-02')&&(await page.locator('.doc-studio-notice').innerText()).includes('MP-01'));
  for(const kind of ['charter','schedule','change']){
   await page.locator(`[data-document="${kind}"]`).click();
   await page.locator(`#doc-paper .pm-document[data-kind="${kind}"]`).waitFor();
   check('gallery '+kind+' has a full reviewable document',await page.locator('#doc-paper .doc-section').count()>=8&&await page.locator('#doc-paper table').count()>=3&&await page.locator('#doc-paper svg[role=img]').count()===1);
   check('gallery '+kind+' displays source review history and status',await page.locator('#document-review').count()===1&&await page.locator('#document-history').count()===1&&await page.locator('#document-sources').count()===1&&(await page.locator('#doc-paper .doc-state').innerText()).includes('승인되지 않음'));
   check('gallery '+kind+' source links have real target sections',await page.locator('#doc-toc a').evaluateAll(links=>links.every(a=>document.getElementById(a.hash.slice(1)))));
   await page.locator('#doc-compare').click();
   check('gallery '+kind+' compares an incomplete memo with review requirements',await page.locator('#doc-comparison').isVisible()&&await page.locator('#doc-comparison li').count()>=3&&await page.locator('#doc-compare').getAttribute('aria-pressed')==='true');
   await page.locator('#doc-complete').focus();await page.keyboard.press('Enter');
   check('gallery '+kind+' comparison can close with keyboard',await page.locator('#doc-comparison').isHidden()&&await page.locator('#doc-complete').getAttribute('aria-pressed')==='true');
   check('gallery '+kind+' document fits mobile',await fits());
  }
  check('gallery performance shows missing future actuals honestly',(await page.locator('#document-visual').innerText()).match(/아직 없는 실적/g)?.length===6&&await page.locator('#document-visual svg circle').count()===9);
  await page.locator('[data-document=schedule]').click();
  for(const [value,days,date] of [['baseline',22,'2026-12-01'],['current',23,'2026-12-02'],['proposed',24,'2026-12-03'],['forecast',25,'2026-12-04']]){
   await page.selectOption('#doc-schedule-view',value);
   const caption=await page.locator('#doc-gantt figcaption').innerText();
   check('gallery '+value+' selected Gantt matches its computed date',caption.includes(days+'영업일')&&caption.includes(date));
   check('gallery '+value+' preserves original baseline in document',(await page.locator('#document-milestones').innerText()).includes('2026-12-01')&&(await page.locator('#document-milestones').innerText()).includes('120백만원'));
  }
  const gallery=await download('#doc-export');
  check('gallery export names its independent example',gallery.name==='PREVIEW-02_schedule_검토문서.html');
  const galleryFile=await context.newPage();
  try{
   await galleryFile.setContent(gallery.text);
   check('gallery export keeps currently selected forecast',await galleryFile.locator('svg').count()===1&&(await galleryFile.locator('figcaption').innerText()).includes('25영업일')&&(await galleryFile.locator('figcaption').innerText()).includes('2026-12-04'));
   check('gallery export remains a readable noninteractive document',await galleryFile.locator('script,select,button').count()===0&&(await galleryFile.locator('.pm-document').innerText()).includes('PREVIEW-02'));
   await galleryFile.setViewportSize({width:390,height:844});
   check('exported gallery document fits mobile',await galleryFile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  }finally{await galleryFile.close();}
  check('gallery browsing changes no ERP source stage',JSON.stringify(await savedStage())===JSON.stringify(galleryStage));
  await page.screenshot({path:path.join(root,'검증/Pages_문서예시_모바일.png'),fullPage:true});
  check('document workflows have no browser errors',errors.length===0);
  check('document workflows have no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();}
};
