const path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');

// Checks the redesigned front door independently of the longer reader, ERP,
// tour and visualization suites. All links are resolved under the Pages prefix.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[],requests=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 page.on('request',request=>requests.push(request.url()));
 const expected=JSON.parse(execFileSync(process.env.PM_PYTHON||'python3',['-c',
  'import json,sys;sys.path.insert(0,sys.argv[1]);from landing_content import COMPARISONS,LESSON_PATH,COMPARISON_NOTICE;print(json.dumps(dict(comparisons=COMPARISONS,journey=LESSON_PATH,notice=COMPARISON_NOTICE),ensure_ascii=False))',path.join(root,'tools')],{encoding:'utf8'}));
 const href=value=>new URL(value,base).href;
 const storage=p=>p.evaluate(()=>[localStorage,sessionStorage].map(store=>Object.fromEntries(Object.keys(store).sort().map(key=>[key,store.getItem(key)]))));
 const fits=p=>p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);
 const primaryContrast=p=>p.locator('a.landing-primary').evaluateAll(links=>links.map(link=>{
  const style=getComputedStyle(link),rgb=color=>(color.match(/[\d.]+/g)||[]).slice(0,3).map(Number);
  const luminance=color=>rgb(color).map(value=>{const c=value/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;}).reduce((sum,c,index)=>sum+c*[.2126,.7152,.0722][index],0);
  const front=luminance(style.color),back=luminance(style.backgroundColor);
  return (Math.max(front,back)+.05)/(Math.min(front,back)+.05);
 }));
 const threeRequests=()=>requests.filter(url=>/\/(?:landing-scene\.mjs|vendor\/three[^/]*\.js)(?:\?|$)/.test(url));
 const d3Requests=()=>requests.filter(url=>/\/vendor\/d3[^/]*\.js(?:\?|$)/.test(url));
 async function ready(p=page){await p.locator('#scene-toggle').waitFor({state:'visible'});await p.locator('#comparison [data-compare]').first().waitFor({state:'attached'});}
 async function selected(p,selector,value,label){
  const button=p.locator(`${selector}="${value}"]`);await button.click();
  check(label+' selects the requested control',await button.getAttribute('aria-pressed')==='true');
  const attr=selector.slice(selector.lastIndexOf('['));
  check(label+' keeps exactly one selection',await p.locator(attr+'][aria-pressed="true"]').count()===1);
 }
 async function mobileMenu(p){
  const toggle=p.locator('#site-menu-toggle'),links=p.locator('#site-links');
  await toggle.waitFor({state:'visible'});
  check('site mobile navigation begins closed',await toggle.getAttribute('aria-expanded')==='false'&&await links.isHidden());
  await toggle.click();await links.waitFor({state:'visible'});
  check('site mobile navigation announces its open state',await toggle.getAttribute('aria-expanded')==='true');
  await p.keyboard.press('Escape');await links.waitFor({state:'hidden'});
  check('site mobile Escape closes and restores focus',await toggle.getAttribute('aria-expanded')==='false'&&await p.evaluate(()=>document.activeElement?.id==='site-menu-toggle'));
 }
 async function sceneAttempt(p){
  const previous=await p.locator('#scene-status').innerText();
  await p.locator('#scene-toggle').click();
  await p.waitForFunction(previous=>{
   const toggle=document.querySelector('#scene-toggle'),host=document.querySelector('#scene-host'),status=document.querySelector('#scene-status');
   return toggle&&!toggle.disabled&&(!!host?.querySelector('canvas')||toggle.getAttribute('aria-pressed')==='false'&&status?.textContent.trim()!==previous.trim()&&!/(불러오는|불러오고|준비 중)/.test(status.textContent));
  },previous);
  return await p.locator('#scene-host canvas').count()>0;
 }
 let isolated,blocked;
 try{
  await page.setViewportSize({width:1440,height:1000});await page.goto(base);await ready();
  const initial=await storage(page);
  check('landing preserves the primary beginner link',await page.getByRole('link',{name:'0단원부터 시작하기 →',exact:true}).first().isVisible());
  check('landing beginner CTA opens unit zero',await page.getByRole('link',{name:'0단원부터 시작하기 →',exact:true}).first().evaluate(a=>new URL(a.href).pathname.endsWith('/learn.html')&&new URL(a.href).searchParams.get('unit')==='0'));
  const desktopContrast=await primaryContrast(page);
  check('landing primary CTA text contrasts with its background',desktopContrast.length>0&&desktopContrast.every(ratio=>ratio>=4.5));
  check('landing initially keeps WebGL optional',await page.locator('#scene-toggle').getAttribute('aria-pressed')==='false'&&await page.locator('#scene-host canvas').count()===0&&threeRequests().length===0);
  check('landing explains its default scene through SVG',await page.locator('#scene-fallback').isVisible()&&await page.locator('#scene-fallback').evaluate(el=>el.matches('svg')||!!el.querySelector('svg')));
  check('landing scene status is accessible',await page.locator('#scene-status').getAttribute('role')==='status');
  check('landing has five accessible scene controls',await page.locator('[data-scene-stage]').count()===5);
  const journeyTop=await page.locator('#journey').evaluate(el=>el.getBoundingClientRect().top);
  if(journeyTop>1500)check('offscreen journey does not preload D3',d3Requests().length===0);
  const sceneHeadings=[];
  for(let index=0;index<5;index++){
   await selected(page,'[data-scene-stage',index,'scene '+index);
   sceneHeadings.push((await page.locator('#scene-heading').innerText()).trim());
   check('scene '+index+' explains the selected document',(await page.locator('#scene-description').innerText()).trim().length>15);
  }
  check('five scene stages have distinct readable headings',sceneHeadings.every(Boolean)&&new Set(sceneHeadings).size===5);
  check('scene selection does not activate WebGL',await page.locator('#scene-host canvas').count()===0&&threeRequests().length===0);
  check('landing fits desktop width',await fits(page));
  await page.screenshot({path:path.join(root,'검증/Pages_랜딩_데스크톱.png')});

  await page.locator('#journey').scrollIntoViewIfNeeded();
  await page.locator('#journey-diagram svg').waitFor({state:'attached'});
  check('landing offers five chapters in its journey',await page.locator('#journey [data-journey]').count()===5);
  for(let index=0;index<expected.journey.length;index++){
   const chapter=expected.journey[index];await selected(page,'#journey [data-journey',index,'journey '+index);
   for(const [selector,key] of [['#journey-title','label'],['#journey-question','question'],['#journey-action','action'],['#journey-result','result']])
    check('journey '+index+' explains '+key,(await page.locator(selector).innerText()).includes(chapter[key]));
   const link=new URL(await page.locator('#journey-link').evaluate(a=>a.href));
   check('journey '+index+' links to its first unit',link.href.startsWith(base)&&link.pathname.endsWith('/learn.html')&&link.searchParams.get('unit')===String(chapter.units[0]));
   check('journey '+index+' retains its readable diagram',await page.locator('#journey-diagram').isVisible()&&await page.locator('#journey-diagram').evaluate(el=>el.matches('svg')||!!el.querySelector('svg')));
  }
  check('journey units cover Level 1 in order',JSON.stringify(expected.journey.flatMap(chapter=>chapter.units))===JSON.stringify([0,1,2,3,4,5,6,7,8,9]));

  const compare=page.locator('#comparison'),range=page.locator('#compare-range');
  await compare.scrollIntoViewIfNeeded();
  check('comparison offers four source-grounded examples',await compare.locator('[data-compare]').count()===4);
  check('comparison range has three deliberate positions',await range.getAttribute('min')==='0'&&await range.getAttribute('max')==='2'&&await range.getAttribute('step')==='1'&&await range.inputValue()==='2');
  check('comparison marks the teaching example as illustrative',(await compare.innerText()).includes(expected.notice));
  for(const item of expected.comparisons){
   await selected(page,'#comparison [data-compare',item.id,'comparison '+item.id);
   check('comparison '+item.id+' begins with the complete comparison',await range.inputValue()==='2');
   check('comparison '+item.id+' presents its draft',(await page.locator('#compare-before').innerText()).includes(item.before.body));
   check('comparison '+item.id+' presents its revision',(await page.locator('#compare-after').innerText()).includes(item.after.body));
   const changes=await page.locator('#compare-changes').innerText();
   check('comparison '+item.id+' explains each revision',item.changes.every(change=>changes.includes(change.label)&&changes.includes(change.why)));
   check('comparison '+item.id+' uses an exact practice link',await page.locator('#compare-link').evaluate(a=>a.href)===href(item.link));
   const phases=[];await range.focus();
   for(const [key,value] of [['Home','0'],['ArrowRight','1'],['End','2']]){
    await range.press(key);check('comparison '+item.id+' range reaches '+value,await range.inputValue()===value);
    const phase=(await page.locator('#compare-phase').innerText()).trim();phases.push(phase);
    check('comparison '+item.id+' range explains position '+value,phase.length>0);
    const revision=await page.locator('#compare-after').innerText(),visibleChanges=await page.locator('#compare-changes').innerText();
    check('comparison '+item.id+' position '+value+' shows the intended wording',revision.includes(value==='0'?item.before.body:value==='1'?item.middle.body:item.after.body));
    if(value==='1')check('comparison '+item.id+' explains the first change progressively',visibleChanges.includes(item.changes[0].why)&&item.changes.slice(1).every(change=>!visibleChanges.includes(change.why)));
    if(value==='2')check('comparison '+item.id+' completes the revision explanation',item.changes.every(change=>visibleChanges.includes(change.why)));
   }
   check('comparison '+item.id+' range labels are distinct',new Set(phases).size===3);
  }
  await compare.screenshot({path:path.join(root,'검증/Pages_랜딩_문장비교.png')});
  check('landing interactions do not request tour animations',!requests.some(url=>/\.gif(?:\?|$)/i.test(url)));
  check('landing exploration preserves browser storage',JSON.stringify(await storage(page))===JSON.stringify(initial));

  await page.locator('#scene-toggle').scrollIntoViewIfNeeded();
  const supported=await sceneAttempt(page);
  check('3D loads only after its explicit control is used',threeRequests().length>0);
  if(supported){
   check('successful 3D announces its active state',await page.locator('#scene-toggle').getAttribute('aria-pressed')==='true');
   check('successful 3D hides the SVG illustration',await page.locator('#scene-fallback').isHidden());
   check('successful 3D has a visible scene host',await page.locator('#scene-host').isVisible());
   await selected(page,'[data-scene-stage',3,'active 3D scene');
   await page.locator('#scene-toggle').click();await page.locator('#scene-host canvas').waitFor({state:'detached'});
   check('closing 3D restores the SVG scene',await page.locator('#scene-toggle').getAttribute('aria-pressed')==='false'&&await page.locator('#scene-fallback').isVisible());
  }else check('unsupported 3D retains usable fallback',await page.locator('#scene-fallback').isVisible()&&(await page.locator('#scene-status').innerText()).trim().length>0);
  check('optional 3D does not save learner or ERP state',JSON.stringify(await storage(page))===JSON.stringify(initial));

  await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await ready();
  check('reduced motion starts with the still scene',await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches)&&await page.locator('#scene-host canvas').count()===0&&await page.locator('#scene-fallback').isVisible());
  await selected(page,'[data-scene-stage',4,'reduced-motion scene');
  await selected(page,'#journey [data-journey',4,'reduced-motion journey');
  check('reduced motion retains the chapter explanation',(await page.locator('#journey-result').innerText()).includes(expected.journey[4].result));
  await page.setViewportSize({width:390,height:844});await page.goto(base);await ready();
  check('mobile primary CTA text remains readable',(await primaryContrast(page)).every(ratio=>ratio>=4.5));
  await mobileMenu(page);
  for(const item of expected.comparisons){await selected(page,'#comparison [data-compare',item.id,'mobile comparison '+item.id);check('mobile comparison '+item.id+' fits',await fits(page));}
  for(let index=0;index<5;index++){await selected(page,'#journey [data-journey',index,'mobile journey '+index);check('mobile journey '+index+' fits',await fits(page));}
  await page.locator('#comparison').screenshot({path:path.join(root,'검증/Pages_랜딩_모바일비교.png')});
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(root,'검증/Pages_랜딩_모바일.png')});
  check('mobile landing does not alter browser storage',JSON.stringify(await storage(page))===JSON.stringify(initial));

  // Exercise the shared menu on the ERP itself, where its native business menu
  // must remain independent from site-navigation controls.
  await page.locator('#site-menu-toggle').click();
  const erpLink=page.locator('#site-links a').filter({hasText:'ERP'}).first();
  await erpLink.click();await page.waitForURL(url=>url.pathname.endsWith('/erp.html'));
  await page.locator('#nav [data-menu="settlements"]').waitFor();await mobileMenu(page);
  await page.locator('#nav [data-menu="settlements"]').click();await page.waitForFunction(()=>document.querySelector('#title')?.textContent.includes('가맹점 정산'));
  await page.locator('#results table').waitFor();
  check('ERP business navigation survives the site menu',!(await page.locator('#error').innerText()).trim()&&await page.locator('#results tbody tr').count()>0);
  await page.locator('#site-menu-toggle').click();
  const readerLink=page.locator('#site-links a').filter({hasText:'교재'}).first();await readerLink.click();
  await page.waitForURL(url=>url.pathname.endsWith('/learn.html'));await page.locator('#chapter-title').waitFor({state:'attached'});
  check('ERP shared navigation returns to the reader',await page.locator('#chapter-view').isVisible()&&await fits(page));

  // A new browser profile remains at S0. The homepage never advances source
  // releases merely because a later chapter or example has been explored.
  isolated=await context.browser().newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
  const novice=await isolated.newPage();await novice.goto(base);await ready(novice);
  const blank=await storage(novice);await selected(novice,'#journey [data-journey',4,'new learner final-chapter preview');
  check('new learner previews leave storage unchanged',JSON.stringify(await storage(novice))===JSON.stringify(blank));
  await novice.getByRole('link',{name:'0단원부터 시작하기 →',exact:true}).first().click();await novice.locator('#chapter-title').waitFor({state:'attached'});
  check('new learner still starts with S0',await novice.evaluate(()=>PMApp.currentStage())==='S0'&&(await novice.locator('#stage-caption').innerText()).includes('S0'));

  // Deliberately refuse the optional 3D dependency. Static learning material,
  // stage selectors and navigation must remain usable after the failure.
  blocked=await context.newPage();const blockedErrors=[];let refused=0;
  blocked.on('pageerror',error=>blockedErrors.push(error.message));
  await blocked.route('**/vendor/three*.js',route=>{refused++;return route.abort('failed');});
  await blocked.goto(base);await ready(blocked);await blocked.locator('#scene-toggle').scrollIntoViewIfNeeded();
  await sceneAttempt(blocked);
  check('blocked 3D was requested only on demand',refused>0);
  check('blocked 3D keeps the SVG and clears active state',await blocked.locator('#scene-fallback').isVisible()&&await blocked.locator('#scene-host canvas').count()===0&&await blocked.locator('#scene-toggle').getAttribute('aria-pressed')==='false');
  check('blocked 3D explains the available alternative',/(기본|대신|지원|표시|불러)/.test(await blocked.locator('#scene-status').innerText()));
  await selected(blocked,'[data-scene-stage',2,'blocked 3D fallback selection');
  await selected(blocked,'#comparison [data-compare','purpose','blocked 3D comparison');
  check('blocked 3D leaves educational content available',(await blocked.locator('#compare-after').innerText()).includes(expected.comparisons[0].after.body));
  check('blocked optional dependency produces no uncaught exception',blockedErrors.length===0);assert.deepEqual(blockedErrors,[]);
  check('landing and shared pages have no uncaught exception',errors.length===0);check('landing and shared pages have no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();if(blocked)await blocked.close();if(isolated)await isolated.close();}
};
