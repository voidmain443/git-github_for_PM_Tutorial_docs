const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
module.exports=async(context,base,check,root)=>{
 const page=await context.newPage(),errors=[],failed=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push(r.url())});
 async function stage(value){await page.selectOption('#wb-stage',value);await page.locator('#wb-stage-open').click();await page.waitForFunction(()=>!document.querySelector('#wb-stage-open').disabled);}
 async function module(name){await page.locator(`[data-module="${name}"]`).click();await page.waitForFunction(()=>!document.querySelector('#wb-stage-open').disabled);check('visual '+name+' loads',!(await page.locator('#wb-error').innerText()));}
 try{
  await page.goto(base+'visual.html');await page.waitForFunction(()=>!document.querySelector('#wb-stage-open').disabled);await stage('S0');
  check('visual workflow source steps',await page.locator('[data-flow]').count()===5);
  await page.locator('[data-flow="3"]').click();check('workflow links facts to a PM question',(await page.locator('#flow-detail').innerText()).includes('불일치'));
  await page.screenshot({path:path.join(root,'검증/Pages_시각화_업무흐름.png'),fullPage:true});
  await module('charter');check('S0 charter has no future approval',(await page.locator('#wb-content').innerText()).includes('S16 승인 회신이 없습니다'));
  await stage('S0A');check('S0A approval source appears',(await page.locator('.wb-source').allTextContents()).some(s=>s.includes('승인번호 AP00')));
  await stage('S0');await module('schedule');check('schedule locked before S1',await page.locator('.wb-lock').count()===1&&await page.locator('#duration-c').count()===0);
  await stage('S1');check('schedule ready without auto-revealing answer',await page.locator('#schedule-result').isHidden());
  await page.locator('#schedule-reveal').click();check('base network and date',(await page.locator('#schedule-result').innerText()).includes('60영업일')&&(await page.locator('#schedule-result').innerText()).includes('2027-01-08'));
  await page.locator('#scenario-c').click();check('noncritical delay uses float',(await page.locator('#schedule-result').innerText()).includes('60영업일'));
  await page.locator('#scenario-d').click();check('critical delay moves end',(await page.locator('#schedule-result').innerText()).includes('65영업일')&&(await page.locator('#schedule-result').innerText()).includes('2027-01-15'));
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#wb-download').click()]);
  const html=await fs.promises.readFile(await download.path(),'utf8');check('standalone visual export includes assumptions and SVG',html.includes('<svg')&&html.includes('D 25일')&&html.includes('65영업일')&&!html.includes('<script'));
  await page.locator('#scenario-lead').click();check('lead recalculates network',(await page.locator('#schedule-result').innerText()).includes('57영업일'));
  await page.locator('#schedule-reset').click();check('original facts restored',(await page.locator('#schedule-result').innerText()).includes('60영업일'));
  const source=await page.evaluate(()=>PMApp.api('/api/detail?menu=documents&id=S06'));check('simulation did not modify ERP',source.document.body.includes('D 대사·예외 모듈 20일'));
  await page.screenshot({path:path.join(root,'검증/Pages_시각화_간트.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});check('visual schedule mobile fits',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(root,'검증/Pages_시각화_모바일.png'),fullPage:true});
  await module('change');check('change locked before S2',await page.locator('.wb-lock').count()===1);
  await stage('S2');check('EVM uses the same ERP facts',(await page.locator('#wb-content').innerText()).includes('0.833')&&(await page.locator('#wb-content').innerText()).includes('0.862'));
  await page.locator('[data-alternative="parallel"]').click();check('resource constraint visible',(await page.locator('#change-detail').innerText()).includes('현 자원 한도를 넘습니다'));
  await page.locator('[data-alternative="extend"]').click();check('proposal is distinct from approval',(await page.locator('#change-detail').innerText()).includes('128백만원')&&(await page.locator('.wb-approval').innerText()).includes('회신 S12가 없습니다'));
  check('visual change mobile fits',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await stage('S3');check('S3 approval source available',(await page.locator('.wb-approval').innerText()).includes('AP02')&&(await page.locator('.wb-source').allTextContents()).some(s=>s.includes('BL02 원가 기준선128')));
  await stage('S0');check('earlier stage removes future data',await page.locator('.wb-lock').count()===1&&!((await page.locator('#wb-content').innerText()).includes('128백만원')));
  for(const name of ['workflow','charter','schedule','change']){
   await stage('S4');await module(name);
   for(const link of await page.locator('#wb-content a[download]').evaluateAll(a=>a.map(x=>x.href))){const r=await page.request.get(link);check('visual template resolves '+name,r.ok());}
  }
  check('visual no browser errors',errors.length===0);check('visual no missing assets',failed.length===0);
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
 }finally{await page.close();}
};
