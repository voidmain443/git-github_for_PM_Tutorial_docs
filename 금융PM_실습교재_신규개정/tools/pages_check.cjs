const {chromium}=require('playwright');
const {execFileSync}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),site=path.join(root,'_site'),prefix='/git-github_for_PM_Tutorial_docs/';
const python=process.env.PM_PYTHON||'python3';
const expected=JSON.parse(execFileSync(python,[path.join(__dirname,'pages_expected.py')],{maxBuffer:40*1024*1024}));
const checks=[],errors=[];let server,browser;
const check=(name,value)=>{assert(value,name);checks.push(name)};
async function run(){
 server=http.createServer((req,res)=>{
  let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://test').pathname)}catch(_){res.writeHead(400).end();return}
  if(!pathname.startsWith(prefix)){res.writeHead(404).end();return}
  const file=path.resolve(site,pathname.slice(prefix.length)||'index.html');
  if(!file.startsWith(site+path.sep)){res.writeHead(403).end();return}
  try{const data=fs.readFileSync(file),types={'.html':'text/html;charset=utf-8','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.wasm':'application/wasm','.pdf':'application/pdf','.md':'text/markdown;charset=utf-8'};res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'}).end(data)}catch(_){res.writeHead(404).end()}
 });
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port+prefix;
 browser=await chromium.launch({headless:true,...(process.env.PM_CHROME?{executablePath:process.env.PM_CHROME}:{})});
 const context=await browser.newContext({acceptDownloads:true,viewport:{width:1440,height:1000}}),page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 const badResponses=[];page.on('response',r=>{if(r.status()>=400)badResponses.push(r.url())});
 await page.goto(base);check('starting directions visible',await page.getByRole('link',{name:'0단원부터 시작하기 →'}).isVisible());
 await page.screenshot({path:path.join(root,'검증/Pages_시작안내.png'),fullPage:true});
 await page.getByRole('link',{name:'0단원부터 시작하기 →'}).click();await page.locator('[data-view=practice]').click();await page.waitForSelector('#step-title');
 check('subpath navigation works',page.url().includes(prefix+'learn.html'));
 check('initial stage S0',(await page.locator('#stage-caption').innerText()).includes('S0'));
 // Compare actual browser SQLite results with the local Python implementation.
 const result=await page.evaluate(async cases=>{
   let stage;for(let i=0;i<cases.length;i++){
     const c=cases[i];if(c.stage!==stage){await PMApp.api('/api/stage',{body:JSON.stringify({stage:c.stage})});stage=c.stage}
     const actual=await PMApp.api(c.route+'?'+new URLSearchParams(c.params||{}),c.body?{body:JSON.stringify(c.body)}:undefined);
     const canonical=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort()):v);
     if(canonical(actual)!==canonical(c.expected))return {i,c,actual};
   }return null;
 },expected);
 assert.equal(result,null,JSON.stringify(result));check(expected.length+' local / browser query comparisons',true);
 const denied=await page.evaluate(async()=>{
  const queries=['DELETE FROM approval','PRAGMA query_only=OFF','SELECT 1; SELECT 2','SELECT 1; PRAGMA query_only=OFF',"ATTACH DATABASE ':memory:' AS x",'WITH t AS (SELECT 1) DELETE FROM approval'];
  const out=[];for(const sql of queries){try{const data=await PMApp.api('/api/sql',{body:JSON.stringify({sql})});out.push({sql,denied:false,data})}catch(e){out.push({sql,denied:true,error:e.message})}}return out;
 });assert(denied.every(x=>x.denied),JSON.stringify(denied));check('SQL writes and multiple statements rejected',true);
 await page.evaluate(()=>PMApp.api('/api/stage',{body:JSON.stringify({stage:'S0'})}));await page.reload();await page.waitForSelector('#step-title');
 const future=await page.evaluate(()=>PMApp.api('/api/lesson?unit=9'));check('future stage hides examples',future.guideSteps.every(s=>s.locked&&!s.html&&!s.sections));
 await page.goto(base+'learn.html?view=practice&unit=1');await page.waitForSelector('#step-title');
 await page.locator('[data-phase=evidence]').click();await page.locator('[data-source="S01"]').click();await page.waitForSelector('#source-panel:not([hidden])');check('source document readable',(await page.locator('#source-panel').innerText()).includes('모아페이'));
 const assumption=await page.evaluate(()=>lesson.guideSteps.findIndex(s=>s.downloads?.includes('A01 가정 로그.md')));
 await page.locator(`[data-step="${assumption}"]`).first().click();await page.locator('[data-phase=practice]').click();await page.locator('#templates summary').click();
 const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('link',{name:'A01 가정 로그.md 내려받기'}).click()]);
 check('Korean template download',(await fs.promises.readFile(await download.path(),'utf8')).includes('확인 책임'));
 const other=await context.newPage();await other.goto(base+'erp.html?menu=settlements&field='+encodeURIComponent('정산번호')+'&value=ST001');await other.waitForSelector('#results table');
 check('ERP exact link',(await other.locator('#count').innerText()).includes('검색 결과 1건'));
 check('settlement amount visible',(await other.locator('#results').innerText()).includes('222,440'));
 const [csv]=await Promise.all([other.waitForEvent('download'),other.locator('#export').click()]);check('CSV current filter',(await fs.promises.readFile(await csv.path(),'utf8')).includes('222440'));
 await page.locator('#stage-caption').click();await page.selectOption('#stage','S1');await page.locator('#change-stage').click();await page.waitForFunction(()=>document.querySelector('#stage-caption').textContent.includes('S1'));
 await other.waitForFunction(()=>document.querySelector('#stage').textContent.includes('S1'));check('other tab refreshes after stage change',true);
 const independent=await browser.newContext();const isolated=await independent.newPage();await isolated.goto(base+'learn.html?view=practice&unit=0');await isolated.waitForSelector('#step-title');check('another student remains at S0',(await isolated.locator('#stage-caption').innerText()).includes('S0'));await independent.close();
 for(const stage of ['S0','S0A','S1','S1A','S2','S3','S4']){
  await page.evaluate(stage=>PMApp.api('/api/stage',{body:JSON.stringify({stage})}),stage);
  for(let u=0;u<10;u++){
   const lesson=await page.evaluate(u=>PMApp.api('/api/lesson?unit='+u),u);
   check(stage+' unit '+u+' release boundary',lesson.guideSteps.every(s=>s.stage>stage?s.locked&&!s.html:!s.locked&&s.html));
  }
 }
 await page.goto(base+'learn.html?view=practice&unit=3');await page.waitForSelector('#step-title');await page.locator('.outline button').last().click();
 await page.screenshot({path:path.join(root,'검증/Pages_단계안내.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});check('reader mobile fits',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:path.join(root,'검증/Pages_모바일.png'),fullPage:true});
 await page.goto(base);check('home mobile fits',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.goto(base+'resources.html');check('stage-specific print links',(await page.locator('#print-links').innerHTML()).includes('print/S4/'));
 for(const link of await page.locator('#print-links a').evaluateAll(a=>a.map(x=>x.href))){const r=await page.request.get(link);check('print PDF available',r.ok()&&(await r.body()).subarray(0,4).toString()==='%PDF')}
 await page.locator('a', {hasText:'양식 보기'}).first().click();check('form preview table',await page.locator('table').count()>0);
 // A killed slow SQL worker recovers cleanly and retains the selected snapshot.
 await page.goto(base+'erp.html?menu=sql');await page.waitForSelector('#sqlpane', {state:'visible'});
 const slow=await page.evaluate(async()=>{try{await PMApp.api('/api/sql',{body:JSON.stringify({sql:'WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM t) SELECT SUM(n) FROM t'})});return false}catch(e){return e.message.includes('중단')}});
 check('slow SQL stops without freezing page',slow);check('worker recovers after timeout',(await page.evaluate(()=>PMApp.api('/api/meta'))).stage==='S4');
 await require('./visual_browser_check.cjs')(context,base,check,root);
 await require('./study_browser_check.cjs')(context,base,check,root);
 await require('./reader_ux_check.cjs')(context,base,check,root);
 check('no page exceptions',errors.length===0);check('no failed asset loads',badResponses.length===0);
 const publicFiles=JSON.parse(fs.readFileSync(path.join(site,'site-manifest.json'),'utf8')).files;
 check('teacher and private records absent',publicFiles.every(f=>!/(05_강사용|06_실습수행기록|강사_전체|완성문서)/.test(f.path)));
 fs.writeFileSync(path.join(root,'검증/Pages_브라우저검증.json'),JSON.stringify({passed:true,queryComparisons:expected.length,checks,errors,badResponses},null,2));
 console.log(`${checks.length} Pages checks passed; ${expected.length} local/browser queries matched`);
}
run().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server)server.close()});
