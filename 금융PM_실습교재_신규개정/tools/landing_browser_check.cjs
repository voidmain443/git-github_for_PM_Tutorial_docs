const path=require('node:path'),assert=require('node:assert/strict');

// Observe the learner-facing result previews, not their rendering implementation.
// Preview numbers belong to PREVIEW-01 and never advance the ERP source stage.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[],requests=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 page.on('request',request=>requests.push(request.url()));
 const cases=[{id:'charter',unit:1,step:'charter-3'},{id:'schedule',unit:3,step:'6.5'},{id:'change',unit:8,step:'7.4'}];
 const storage=p=>p.evaluate(()=>[localStorage,sessionStorage].map(store=>Object.fromEntries(Object.keys(store).sort().map(key=>[key,store.getItem(key)]))));
 const fits=p=>p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);
 const contrastRatio=(front,back)=>{
  const luminance=color=>(color.match(/[\d.]+/g)||[]).slice(0,3).map(Number).map(value=>{const c=value/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;}).reduce((sum,c,index)=>sum+c*[.2126,.7152,.0722][index],0);
  const a=luminance(front),b=luminance(back);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
 };
 const numeric=async locator=>Number((await locator.first().innerText()).replace(/,/g,'').match(/-?\d+(?:\.\d+)?/)?.[0]);
 const firstCTA=p=>p.getByRole('link',{name:'0단원부터 시작하기 →',exact:true});
 async function ready(p=page){await p.locator('#outcome-lab').waitFor();await p.locator('#outcome-play').waitFor({state:'visible'});}
 async function select(p,id){
  const button=p.locator(`[data-outcome="${id}"]`);await button.click();
  await p.waitForFunction(id=>document.querySelector(`[data-outcome="${id}"]`)?.getAttribute('aria-pressed')==='true',id);
  check(id+' preview has one selected result',await p.locator('[data-outcome][aria-pressed="true"]').count()===1);
 }
 async function stage(p,index){
  await p.locator(`[data-outcome-step="${index}"]`).click();
  check('preview step '+index+' announces selection',await p.locator(`[data-outcome-step="${index}"]`).getAttribute('aria-current')==='step');
  check('preview step '+index+' stops automatic playback',await p.locator('#outcome-play').getAttribute('aria-pressed')==='false');
 }
 async function mobileMenu(p){
  const toggle=p.locator('#site-menu-toggle'),links=p.locator('#site-links');
  await toggle.waitFor({state:'visible'});
  check('mobile menu begins closed',await toggle.getAttribute('aria-expanded')==='false'&&await links.isHidden());
  await toggle.click();await links.waitFor({state:'visible'});
  check('mobile menu announces opening',await toggle.getAttribute('aria-expanded')==='true');
  await p.keyboard.press('Escape');await links.waitFor({state:'hidden'});
  check('mobile menu closes with focus restored',await toggle.getAttribute('aria-expanded')==='false'&&await p.evaluate(()=>document.activeElement?.id==='site-menu-toggle'));
 }
 async function compareCase(p,item){
  await select(p,item.id);
  check(item.id+' starts with its completed preview',await p.locator('[data-outcome-step="3"]').getAttribute('aria-current')==='step');
  check(item.id+' explains the original draft',(await p.locator('#outcome-before').innerText()).trim().length>20);
  check(item.id+' has a named visible result',(await p.locator('#outcome-title').innerText()).trim().length>5&&await p.locator('#outcome-surface').isVisible());
  check(item.id+' uses a structured visual result',item.id==='charter' ? /목표/.test(await p.locator('#outcome-surface').innerText())&&/범위/.test(await p.locator('#outcome-surface').innerText())&&/PM|권한|스폰서/.test(await p.locator('#outcome-surface').innerText()) : await p.locator('#outcome-surface svg').count()>0);
  check(item.id+' gives a text explanation',(await p.locator('#outcome-caption').innerText()).trim().length>15);
  const workbook=new URL(await p.locator('#outcome-workbook').evaluate(a=>a.href));
  const lesson=new URL(await p.locator('#outcome-lesson').evaluate(a=>a.href));
  check(item.id+' opens its real visualization workbook',workbook.href.startsWith(base)&&workbook.pathname.endsWith('/visual.html')&&workbook.searchParams.get('lab')===item.id);
  check(item.id+' opens its matching lesson',lesson.href.startsWith(base)&&lesson.pathname.endsWith('/learn.html')&&lesson.searchParams.get('unit')===String(item.unit)&&lesson.searchParams.get('view')==='practice'&&lesson.searchParams.get('step')===item.step);
  const captions=[];
  for(let index=0;index<4;index++){
   await stage(p,index);captions.push((await p.locator('#outcome-caption').innerText()).trim());
   check(item.id+' step '+index+' has one selected phase',await p.locator('[data-outcome-step][aria-current="step"]').count()===1);
  }
  check(item.id+' explains four different decisions',new Set(captions).size===4);
 }
 let isolated,noScript,blocked;
 try{
  await page.setViewportSize({width:1440,height:1000});await page.goto(base);await ready();
  const initial=await storage(page);
  check('landing retains one beginner CTA',await firstCTA(page).count()===1&&await firstCTA(page).isVisible());
  check('beginner CTA opens unit zero',await firstCTA(page).evaluate(a=>new URL(a.href).pathname.endsWith('/learn.html')&&new URL(a.href).searchParams.get('unit')==='0'));
  const contrast=await firstCTA(page).evaluate(link=>{
   const style=getComputedStyle(link),luminance=color=>(color.match(/[\d.]+/g)||[]).slice(0,3).map(Number).map(value=>{const c=value/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;}).reduce((sum,c,index)=>sum+c*[.2126,.7152,.0722][index],0);
   const front=luminance(style.color),back=luminance(style.backgroundColor);return (Math.max(front,back)+.05)/(Math.min(front,back)+.05);
  });
  check('landing beginner CTA has readable contrast',contrast>=4.5);
  const menuDescriptions=await page.locator('#site-links a small').evaluateAll(labels=>labels.map(label=>({front:getComputedStyle(label).color,back:getComputedStyle(label.closest('.site-header')).backgroundColor})));
  check('site menu usage descriptions have readable contrast',menuDescriptions.length===5&&menuDescriptions.every(colors=>contrastRatio(colors.front,colors.back)>=4.5));
  check('landing presents three result types',await page.locator('[data-outcome]').count()===3);
  check('preview captions are announced',await page.locator('#outcome-caption').getAttribute('role')==='status');
  check('result preview begins with a still completed state',await page.locator('#outcome-play').getAttribute('aria-pressed')==='false'&&await page.locator('[data-outcome-step="3"]').getAttribute('aria-current')==='step');
  const notice=await page.locator('#outcome-notice').innerText();
  check('preview explicitly names its independent case',notice.includes('PREVIEW-01')&&/가상|독립/.test(notice));
  check('preview distinguishes illustration from source or approval',/원천|원본|자료 시점|승인/.test(notice));
  check('landing desktop fits',await fits(page));
  await page.screenshot({path:path.join(root,'검증/Pages_랜딩_데스크톱.png')});
  for(const item of cases)await compareCase(page,item);

  await select(page,'schedule');
  const days=page.locator('#preview-days');
  check('schedule offers a bounded duration experiment',await days.getAttribute('min')==='4'&&await days.getAttribute('max')==='6'&&await days.getAttribute('step')==='1');
  await days.focus();await days.press('Home');
  check('four-day activity yields nine-day project',await days.inputValue()==='4'&&await numeric(page.locator('.preview-finish'))===9);
  const durationColors=await page.locator('#preview-gantt .task').evaluateAll(rows=>{
   const row=rows.find(row=>row.querySelector('text')?.textContent.trim().startsWith('C'));
   const bars=row?.querySelectorAll('rect'),labels=row?.querySelectorAll('text');
   return bars?.length&&labels?.length?{front:getComputedStyle(labels[labels.length-1]).fill,back:getComputedStyle(bars[bars.length-1]).fill}:null;
  });
  check('noncritical Gantt duration remains readable on its light bar',!!durationColors&&contrastRatio(durationColors.front,durationColors.back)>=4.5);
  await days.press('End');
  check('six-day activity yields eleven-day project',await days.inputValue()==='6'&&await numeric(page.locator('.preview-finish'))===11);
  await days.press('ArrowLeft');
  check('schedule recalculates the intermediate duration',await days.inputValue()==='5'&&await numeric(page.locator('.preview-finish'))===10);
  await page.locator('#outcome-lab').screenshot({path:path.join(root,'검증/Pages_랜딩_일정결과.png')});
  await select(page,'change');
  const ac=page.locator('#preview-ac');
  check('change offers a bounded cost experiment',await ac.getAttribute('min')==='40'&&await ac.getAttribute('max')==='60'&&await ac.getAttribute('step')==='5');
  await ac.focus();await ac.press('Home');
  const cpiLow=await numeric(page.locator('.preview-cpi')),spi=await numeric(page.locator('.preview-spi'));
  await ac.press('End');const cpiHigh=await numeric(page.locator('.preview-cpi'));
  check('higher actual cost lowers the cost performance index',await ac.inputValue()==='60'&&Number.isFinite(cpiLow)&&Number.isFinite(cpiHigh)&&cpiLow>cpiHigh&&cpiHigh>0);
  check('cost-only experiment preserves schedule performance',await numeric(page.locator('.preview-spi'))===spi&&Number.isFinite(spi));
  await page.locator('#outcome-lab').screenshot({path:path.join(root,'검증/Pages_랜딩_변경결과.png')});

  await select(page,'charter');await page.locator('#outcome-play').click();
  check('playback starts only after user action',await page.locator('#outcome-play').getAttribute('aria-pressed')==='true');
  await page.waitForFunction(()=>document.querySelector('#outcome-play')?.getAttribute('aria-pressed')==='false'&&document.querySelector('[data-outcome-step="3"]')?.getAttribute('aria-current')==='step',null,{timeout:20000});
  check('playback finishes at the completed result',await page.locator('#outcome-play').getAttribute('aria-pressed')==='false');
  await page.locator('#outcome-play').click();await stage(page,1);
  await page.locator('#outcome-play').click();await select(page,'schedule');
  check('switching result cancels playback',await page.locator('#outcome-play').getAttribute('aria-pressed')==='false'&&await page.locator('[data-outcome-step="3"]').getAttribute('aria-current')==='step');
  check('landing does not request obsolete 3D assets',!requests.some(url=>/\/(?:landing-scene\.mjs|vendor\/three[^/]*\.js)(?:\?|$)/.test(url)));
  check('preview interaction does not preload tour GIFs',!requests.some(url=>/\.gif(?:\?|$)/i.test(url)));
  check('preview exploration never saves or changes ERP state',JSON.stringify(await storage(page))===JSON.stringify(initial));

  await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await ready();
  check('reduced motion starts with a still complete result',await page.locator('#outcome-play').getAttribute('aria-pressed')==='false'&&await page.locator('[data-outcome-step="3"]').getAttribute('aria-current')==='step');
  for(const item of cases){await select(page,item.id);await stage(page,1);await stage(page,3);}
  await page.setViewportSize({width:390,height:844});await page.goto(base);await ready();await mobileMenu(page);
  for(const item of cases){await compareCase(page,item);check(item.id+' mobile preview fits',await fits(page));}
  await page.locator('#outcome-lab').screenshot({path:path.join(root,'검증/Pages_랜딩_모바일결과.png')});
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(root,'검증/Pages_랜딩_모바일.png')});
  check('mobile exploration keeps browser storage unchanged',JSON.stringify(await storage(page))===JSON.stringify(initial));

  await page.locator('#site-menu-toggle').click();await page.locator('#site-links a').filter({hasText:'ERP'}).first().click();
  await page.waitForURL(url=>url.pathname.endsWith('/erp.html'));await page.locator('#nav [data-menu="settlements"]').waitFor();await mobileMenu(page);
  await page.locator('#nav [data-menu="settlements"]').click();await page.waitForFunction(()=>document.querySelector('#title')?.textContent.includes('가맹점 정산'));await page.locator('#results table').waitFor();
  check('shared menu does not interfere with ERP business navigation',!(await page.locator('#error').innerText()).trim()&&await page.locator('#results tbody tr').count()>0);
  await page.locator('#site-menu-toggle').click();await page.locator('#site-links a').filter({hasText:'교재'}).first().click();
  await page.waitForURL(url=>url.pathname.endsWith('/learn.html'));await page.locator('#chapter-title').waitFor({state:'attached'});
  check('shared navigation returns to a usable reader',await page.locator('#chapter-view').isVisible()&&await fits(page));

  isolated=await context.browser().newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
  const novice=await isolated.newPage();await novice.goto(base);await ready(novice);
  const blank=await storage(novice);await select(novice,'change');await stage(novice,2);
  check('later-work examples do not advance a new learner',JSON.stringify(await storage(novice))===JSON.stringify(blank));
  await firstCTA(novice).click();await novice.locator('#chapter-title').waitFor({state:'attached'});
  check('new learners still start with S0',await novice.evaluate(()=>PMApp.currentStage())==='S0'&&(await novice.locator('#stage-caption').innerText()).includes('S0'));

  noScript=await context.browser().newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const staticPage=await noScript.newPage();await staticPage.goto(base);
  check('static homepage retains an explanatory result',(await staticPage.locator('#outcome-surface').innerText()).includes('목표')&&(await staticPage.locator('#outcome-caption').innerText()).trim().length>15);
  check('static homepage retains a usable starting link',await firstCTA(staticPage).isVisible()&&await fits(staticPage));
  blocked=await context.newPage();const blockedErrors=[];let refused=0;
  blocked.on('pageerror',error=>blockedErrors.push(error.message));
  await blocked.route('**/vendor/d3*.js',route=>{refused++;return route.abort('failed');});
  await blocked.goto(base);await ready(blocked);await select(blocked,'schedule');
  check('unavailable chart dependency retains the calculated schedule',refused>0&&await numeric(blocked.locator('.preview-finish'))===9&&(await blocked.locator('#outcome-surface').innerText()).includes('요구 정의'));
  await blocked.locator('#preview-days').focus();await blocked.locator('#preview-days').press('End');
  check('fallback schedule still responds to keyboard changes',await numeric(blocked.locator('.preview-finish'))===11);
  await select(blocked,'change');
  check('unavailable chart dependency retains performance labels',/PV.*계획가치/.test(await blocked.locator('#outcome-surface').innerText())&&/EV.*획득가치/.test(await blocked.locator('#outcome-surface').innerText())&&await numeric(blocked.locator('.preview-spi'))===0.8);
  check('unavailable chart dependency produces no uncaught error',blockedErrors.length===0);assert.deepEqual(blockedErrors,[]);
  check('landing and shared pages have no uncaught exceptions',errors.length===0);check('landing and shared pages have no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();if(blocked)await blocked.close();if(isolated)await isolated.close();if(noScript)await noScript.close();}
};
