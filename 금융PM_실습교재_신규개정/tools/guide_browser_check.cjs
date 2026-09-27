const path=require('node:path'),assert=require('node:assert/strict');

// The guide should answer when to open a tool, show one complete first task,
// and lead to the exact S0 material without changing a learner's source stage.
module.exports=async(context,base,check,root)=>{
 const profile=await context.browser().newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await profile.newPage(),errors=[],failed=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 const sections=['start','menus','first-lab','save','next','faq','reference'];
 const storage=()=>page.evaluate(()=>[localStorage,sessionStorage].map(store=>Object.fromEntries(Object.keys(store).sort().map(key=>[key,store.getItem(key)]))));
 const fits=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);
 async function ready(){await page.locator('#guide-start').waitFor({state:'visible'});}
 try{
  await page.goto(base+'guide.html');await ready();const original=await storage();
  check('guide has one clear page heading',await page.locator('main h1').count()===1);
  for(const section of sections){
   const block=page.locator('#guide-'+section);
   check('guide exposes '+section,await block.count()===1&&(await block.textContent()).trim().length>20);
  }
  const navigation=page.locator('.guide-nav');
  check('guide provides a local contents navigation',await navigation.isVisible());
  const destinations=await navigation.locator('a[href^="#"]').evaluateAll(links=>links.map(a=>a.getAttribute('href')));
  check('guide contents have useful distinct destinations',destinations.length>=5&&new Set(destinations).size===destinations.length);
  for(const target of destinations)check('guide contents destination '+target+' exists',await page.locator(target).count()===1);
  const menus=page.locator('#guide-menus');
  for(const [name,file] of [['교재','learn.html'],['ERP','erp.html'],['시각화','visual.html'],['자료실','resources.html']]){
   check('guide explains when to use '+name,(await menus.innerText()).includes(name));
   check('guide links to '+name,await menus.locator('a').evaluateAll((links,file)=>links.some(a=>new URL(a.href).pathname.endsWith('/'+file)),file));
  }
  const first=await page.locator('#guide-first-lab').innerText();
  check('first task names its S0 source release',first.includes('S0'));
  check('first task names its starting source and written output',first.includes('S01')&&first.includes('G00'));
  check('first task gives a transaction to investigate',/ST00[12]/.test(first));
  check('guide distinguishes the worked example from independent practice',(await page.locator('main').innerText()).includes('ST001')&&(await page.locator('main').innerText()).includes('ST002'));
  const save=await page.locator('#guide-save').innerText();
  check('guide tells students to download their document',/내려받|다운로드/.test(save));
  check('guide explains temporary browser drafts',/새로고침|페이지를 떠나|사라/.test(save));
  check('guide explains returning with the saved file',/불러오기|불러와|불러올/.test(save));
  const next=await page.locator('#guide-next').innerText();
  check('guide distinguishes source release from approval',/승인/.test(next)&&/자료|시점|단계/.test(next));
  await page.locator('#guide-reference summary').click();
  const references=await page.locator('#guide-reference').innerText();
  check('guide keeps lookup details available',/검색|조건|SQL|조회/.test(references));
  await page.locator('#guide-reference summary').click();
  check('guide desktop has no horizontal overflow',await fits());
  await page.screenshot({path:path.join(root,'검증/Pages_학습가이드_데스크톱.png')});
  await page.locator('#guide-first-lab').screenshot({path:path.join(root,'검증/Pages_학습가이드_첫실습.png')});
  const faq=page.locator('#guide-faq details');
  for(let i=0;i<await faq.count();i++){
   const item=faq.nth(i);await item.locator('summary').click();
   check('guide troubleshooting '+i+' reveals its explanation',await item.evaluate(el=>el.open)&&((await item.innerText()).trim().length>30));
   await item.locator('summary').click();
  }
  check('reading and expanding the guide preserve learner state',JSON.stringify(await storage())===JSON.stringify(original));

  // Validate only the public route/query contract here; the ERP suite already
  // checks every underlying SQLite row and the reader suite every unit.
  const localLinks=await page.locator('main a[href]').evaluateAll(links=>links.map(a=>({href:a.href,text:a.textContent.trim()})));
  check('guide routes stay under the repository prefix',localLinks.filter(link=>new URL(link.href).origin===new URL(base).origin).every(link=>link.href.startsWith(base)));
  const lessonLink=localLinks.find(link=>{const url=new URL(link.href);return url.pathname.endsWith('/learn.html')&&url.searchParams.get('unit')==='0'&&url.searchParams.get('view')==='practice'&&url.searchParams.has('step');});
  check('guide provides a precise first-practice link',!!lessonLink);
  if(lessonLink){
   await page.goto(lessonLink.href);await page.locator('#step-title').waitFor({state:'visible'});
   const url=new URL(lessonLink.href);
   check('guide practice link opens its requested task',await page.evaluate(async step=>{const lesson=await PMApp.api('/api/lesson?unit=0'),task=lesson.guideSteps.find(item=>item.id===step);return document.querySelector('#step-title')?.textContent===task?.title;},url.searchParams.get('step')));
   check('guide practice link preserves S0',await page.evaluate(()=>PMApp.currentStage())==='S0');
   if(url.searchParams.has('phase'))check('guide practice link opens its requested phase',await page.locator(`[data-phase="${url.searchParams.get('phase')}"][role="tab"]`).getAttribute('aria-selected')==='true');
  }
  const erpLink=localLinks.find(link=>{const url=new URL(link.href);return url.pathname.endsWith('/erp.html')&&url.searchParams.get('menu')==='settlements'&&url.searchParams.get('field')==='정산번호'&&['ST001','ST002'].includes(url.searchParams.get('value'));});
  check('guide provides a reproducible settlement query link',!!erpLink);
  if(erpLink){
   const target=new URL(erpLink.href).searchParams.get('value');await page.goto(erpLink.href);await page.waitForFunction(target=>document.querySelector('#field')?.value==='정산번호'&&document.querySelector('#value')?.value===target&&document.querySelectorAll('#results tbody tr').length===1,target);
   check('guide settlement link returns exactly its record',await page.locator('#results tbody tr').count()===1&&(await page.locator('#results tbody tr').innerText()).includes(target));
   check('guide settlement link applies both field and value',await page.locator('#field').inputValue()==='정산번호'&&await page.locator('#value').inputValue()===target);
   if(target==='ST001')check('guide worked settlement amount matches ERP',(await page.locator('#results').innerText()).includes('222,440'));
   check('guide query is usable without an error',!(await page.locator('#error').innerText()).trim());
  }

  await page.setViewportSize({width:390,height:844});await page.goto(base+'guide.html');await ready();
  for(const section of sections){await page.locator('#guide-'+section).scrollIntoViewIfNeeded();check('guide '+section+' fits a narrow screen',await fits());}
  await page.locator('#guide-first-lab').screenshot({path:path.join(root,'검증/Pages_학습가이드_모바일첫실습.png')});
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(root,'검증/Pages_학습가이드_모바일.png')});
  const toggle=page.locator('#site-menu-toggle');await toggle.click();
  check('guide mobile menu exposes the reader link',await page.locator('#site-links a').filter({hasText:'교재'}).first().isVisible());
  await page.keyboard.press('Escape');check('guide mobile menu closes with Escape',await toggle.getAttribute('aria-expanded')==='false');
  check('guide and linked screens have no uncaught exceptions',errors.length===0);check('guide and linked screens have no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await profile.close();}
};
