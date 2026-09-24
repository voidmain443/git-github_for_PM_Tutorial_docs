const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');

// Exercise the real homepage tour, including its repository-prefixed links.
// Playback assertions follow state changes, not a particular animation clock.
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[],gifRequests=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 page.on('request',request=>{if(/\.gif$/i.test(new URL(request.url()).pathname))gifRequests.push(request.url());});
 const ids=['read','source','erp','write','review'];
 let clips;
 const href=value=>new URL(value.includes('/')?value:'tour-media/'+value,base).href;
 const fits=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);
 const storage=()=>page.evaluate(()=>[localStorage,sessionStorage].map(s=>Object.fromEntries(Object.keys(s).sort().map(key=>[key,s.getItem(key)]))));
 const source=()=>page.locator('#tour-screen').evaluate(image=>image.currentSrc||image.src);
 async function ready(){
  await page.locator('#home-tour').waitFor({state:'visible'});
  await page.waitForFunction(()=>{const image=document.querySelector('#tour-screen');return image?.complete&&image.naturalWidth>0&&document.querySelector('#home-tour-data')?.textContent.trim();});
 }
 async function stillReady(allowed){
  await page.waitForFunction(urls=>{const image=document.querySelector('#tour-screen');return image?.complete&&image.naturalWidth>0&&urls.includes(image.currentSrc||image.src);},allowed);
 }
 async function select(id){
  const clip=clips.find(item=>item.id===id);assert(clip,'known tour clip '+id);
  await page.locator(`#home-tour [data-tour-step="${id}"]`).click();
  await stillReady([href(clip.poster),href(clip.frames[0].still)]);
  check('tour selects only '+id,await page.locator('#home-tour [data-tour-step][aria-pressed="true"]').count()===1&&await page.locator(`[data-tour-step="${id}"]`).getAttribute('aria-pressed')==='true');
  return clip;
 }
 async function frame(clip,index){
  await stillReady([href(clip.frames[index].still),...(index===0?[href(clip.poster)]:[])]);
  check('tour '+clip.id+' frame '+index+' has an explanatory caption',(await page.locator('#tour-frame-label').innerText()).includes(clip.frames[index].label));
 }
 async function play(){
  await page.locator('#tour-play').click();
  await page.waitForFunction(()=>{const image=document.querySelector('#tour-screen');return image?.src.startsWith('blob:')&&image.complete&&image.naturalWidth>0;});
  check('tour explicit play has a decoded image',await page.locator('#tour-screen').evaluate(image=>image.complete&&image.naturalWidth>0));
 }
 async function stop(clip){
  await page.locator('#tour-play').click();
  await stillReady([href(clip.poster),...clip.frames.map(f=>href(f.still))]);
  check('tour stop restores a static frame',!(await source()).startsWith('blob:')&&!/\.gif(?:\?|$)/i.test(await source()));
 }
 async function zoom(closeWithEscape=false){
  const original=await source();await page.locator('#tour-zoom').click();
  await page.locator('#tour-dialog').waitFor({state:'visible'});
  await page.waitForFunction(()=>{const image=document.querySelector('#tour-zoom-image');return image?.complete&&image.naturalWidth>0;});
  check('tour enlargement is a native open dialog',await page.locator('#tour-dialog').evaluate(dialog=>dialog.tagName==='DIALOG'&&dialog.open));
  check('tour enlargement shows the selected still',await page.locator('#tour-zoom-image').evaluate(image=>image.currentSrc||image.src)===original);
  if(closeWithEscape)await page.keyboard.press('Escape');else await page.locator('#tour-dialog-close').click();
  await page.locator('#tour-dialog').waitFor({state:'hidden'});
  check('tour dialog returns keyboard focus',await page.evaluate(()=>document.activeElement?.id==='tour-zoom'));
 }
 try{
  await page.goto(base);await ready();
  const initialStorage=await storage();
  const metadata=await page.locator('#home-tour-data').textContent();
  const data=JSON.parse(metadata);clips=data.clips;
  check('tour metadata contains the five learning tasks',Array.isArray(clips)&&clips.length===5&&ids.every((id,index)=>clips[index].id===id));
  check('tour shows five accessible selectors',await page.locator('#home-tour button[data-tour-step]').count()===5&&await page.locator('#home-tour button[data-tour-step]').evaluateAll(buttons=>buttons.every(b=>b.textContent.trim()&&['true','false'].includes(b.getAttribute('aria-pressed')))));
  check('tour captions are announced without replacing the page',await page.locator('#tour-frame-label').getAttribute('role')==='status');
  check('tour has a visible status message',await page.locator('#tour-status').count()===1);
  for(const clip of clips){
   const paths=[clip.gif,clip.poster,...(clip.frames||[]).map(f=>f.still)];
   check('tour '+clip.id+' has valid image metadata',Number.isFinite(clip.durationMs)&&clip.durationMs>0&&Number.isInteger(clip.width)&&clip.width>0&&Number.isInteger(clip.height)&&clip.height>0&&Array.isArray(clip.frames)&&clip.frames.length>=2);
   check('tour '+clip.id+' uses local tour media',paths.every(value=>typeof value==='string'&&href(value).startsWith(base)&&new URL(href(value)).pathname.includes('/tour-media/')));
   check('tour '+clip.id+' separates GIF and still files',/\.gif$/i.test(clip.gif)&&/\.webp$/i.test(clip.poster)&&clip.frames.every(f=>/\.webp$/i.test(f.still)));
   check('tour '+clip.id+' frames have ordered timing and captions',clip.frames.every((f,i)=>Number.isFinite(f.atMs)&&f.atMs>=0&&f.atMs<clip.durationMs&&(i===0||f.atMs>clip.frames[i-1].atMs)&&typeof f.label==='string'&&f.label.trim().length>0));
  }
  check('tour opens on a static WebP without GIF requests',/\.webp(?:\?|$)/i.test(await source())&&gifRequests.length===0);
  for(const id of ids){
   const clip=await select(id);await frame(clip,0);
   check('tour '+id+' first frame disables previous',await page.locator('#tour-prev-frame').isDisabled());
   check('tour '+id+' first frame allows next',await page.locator('#tour-next-frame').isEnabled());
   for(let index=1;index<clip.frames.length;index++){await page.locator('#tour-next-frame').click();await frame(clip,index);}
   check('tour '+id+' last frame disables next',await page.locator('#tour-next-frame').isDisabled());
   for(let index=clip.frames.length-2;index>=0;index--){await page.locator('#tour-prev-frame').click();await frame(clip,index);}
   check('tour '+id+' returns to its first frame',await page.locator('#tour-prev-frame').isDisabled());
   const link=await page.locator('#tour-open').evaluate(a=>a.href);
   check('tour '+id+' links to a real local learning screen',link.startsWith(base)&&/\/(?:learn|erp)\.html$/.test(new URL(link).pathname));
   check('tour '+id+' download points to its actual GIF',await page.locator('#tour-gif').evaluate(a=>a.href)===href(clip.gif)&&await page.locator('#tour-gif').getAttribute('download')!==null);
  }
  check('tour reading and manual frames do not preload a GIF',gifRequests.length===0);
  await select('read');await zoom();await zoom(true);
  check('tour enlargement does not trigger playback',gifRequests.length===0);
  check('tour desktop layout fits',await fits());
  await page.screenshot({path:path.join(root,'검증/Pages_홈_화면안내.png'),fullPage:true});

  // Real downloads, rather than only file-extension checks, also verify that
  // selecting another task refreshes the downloadable asset.
  for(const id of ids){
   const clip=await select(id);
   const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#tour-gif').click()]);
   const bytes=await fs.promises.readFile(await download.path());
   check('tour '+id+' downloads an actual GIF',/\.gif$/i.test(download.suggestedFilename())&&bytes.length>10&&/^GIF8[79]a$/.test(bytes.subarray(0,6).toString('ascii')));
   check('tour '+id+' GIF dimensions match its metadata',bytes.readUInt16LE(6)===clip.width&&bytes.readUInt16LE(8)===clip.height);
  }
  let clip=await select('read');await play();await stop(clip);
  await play();clip=await select('source');
  check('tour task selection cancels the previous playback',!(await source()).startsWith('blob:'));
  await page.locator('#tour-next-frame').click();await frame(clip,1);
  check('tour remains manually usable after cancelling playback',await page.locator('#tour-prev-frame').isEnabled());

  // Motion preference changes the default, not access to the explanation.
  // Explicit playback is still a user choice; no animation timer is assumed.
  await page.emulateMedia({reducedMotion:'reduce'});
  const requestsBeforeReduced=gifRequests.length;await page.reload();await ready();
  check('tour respects reduced-motion initial presentation',await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches)&&!((await source()).startsWith('blob:'))&&gifRequests.length===requestsBeforeReduced);
  clip=await select('erp');await page.locator('#tour-next-frame').click();await frame(clip,1);await play();await stop(clip);
  await page.setViewportSize({width:390,height:844});
  for(const id of ids){
   clip=await select(id);await page.locator('#tour-next-frame').click();await frame(clip,1);
   check('tour '+id+' mobile layout fits at 390 pixels',await fits());
  }
  await select('write');await page.locator('#tour-next-frame').click();await frame(clips.find(c=>c.id==='write'),1);
  await zoom(true);check('tour mobile remains within the viewport after closing zoom',await fits());
  await page.screenshot({path:path.join(root,'검증/Pages_홈_화면안내_모바일.png'),fullPage:true});
  check('tour viewing and playback do not change stage or browser storage',JSON.stringify(await storage())===JSON.stringify(initialStorage));

  // The tour must lead to the precise reader task and phase even if an older
  // reading position exists in this shared browser context.
  await page.goto(base+'learn.html?unit=0&view=practice&step=settlement&phase=evidence');
  await page.locator('#step-title').waitFor({state:'visible'});
  const lesson=await page.evaluate(()=>PMApp.api('/api/lesson?unit=0'));
  const target=lesson.guideSteps.find(s=>s.id==='settlement');assert(target,'settlement guide task exists');
  check('tour deep link opens the requested task',(await page.locator('#step-title').innerText())===target.title);
  check('tour deep link brings its task heading into view',await page.locator('#step-title').evaluate(el=>{const r=el.getBoundingClientRect();return document.activeElement===el&&r.top>=0&&r.top<innerHeight;}));
  check('tour deep link opens evidence in practice mode',await page.locator('#practice-view').isVisible()&&await page.locator('#chapter-view').isHidden()&&await page.locator('[data-phase="evidence"][role="tab"]').getAttribute('aria-selected')==='true');
  check('tour deep link shows only the requested phase',await page.locator('.step-phase-panel:visible').count()===1&&await page.locator('.step-phase-panel[data-phase-panel="evidence"]').isVisible());
  check('tour deep link has available source controls',await page.locator('[data-source]:visible').count()>0);
  const finalStorage=await storage();
  check('tour deep link preserves the chosen ERP source stage',JSON.stringify(Object.entries(finalStorage[0]).filter(([key])=>key.startsWith('moapay.pm.stage:')))===JSON.stringify(Object.entries(initialStorage[0]).filter(([key])=>key.startsWith('moapay.pm.stage:'))));
  check('tour and linked reader have no page exceptions',errors.length===0);
  check('tour and linked reader have no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();}
};
