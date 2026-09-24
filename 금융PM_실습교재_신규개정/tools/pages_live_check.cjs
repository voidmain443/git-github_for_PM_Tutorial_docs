/* Read-only smoke test of the published site; stage selection is browser-local. */
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const base=process.env.PM_PAGES_URL||'https://voidmain443.github.io/git-github_for_PM_Tutorial_docs/';
const checks=[],errors=[];let browser;
const check=(name,ok)=>{assert(ok,name);checks.push(name)};
async function run(){
 browser=await chromium.launch({headless:true,...(process.env.PM_CHROME?{executablePath:process.env.PM_CHROME}:{})});
 const page=await browser.newPage({acceptDownloads:true,viewport:{width:1360,height:960}});
 page.on('pageerror',e=>errors.push(e.message));
 const home=await page.goto(base,{waitUntil:'networkidle'});check('public homepage responds',home.ok());
 await page.getByRole('link',{name:'0단원부터 시작하기 →'}).click();await page.locator('[data-view=practice]').click();await page.waitForSelector('#step-title');
 check('public reader begins at S0',(await page.locator('#stage-caption').innerText()).includes('S0'));
 await page.locator('[data-phase=evidence]').click();await page.locator('[data-source="S01"]').click();await page.waitForSelector('#source-panel:not([hidden])');
 check('public source document opens',(await page.locator('#source-panel').innerText()).includes('모아페이'));
 await page.goto(base+'erp.html?menu=settlements&field='+encodeURIComponent('정산번호')+'&value=ST001');
 await page.waitForSelector('#results table');check('public ERP computes settlement',(await page.locator('#results').innerText()).includes('222,440'));
 const sql=await page.evaluate(()=>PMApp.api('/api/sql',{body:JSON.stringify({sql:"SELECT COUNT(*) AS n FROM v_대사조회 WHERE 판정='불일치'"})}));
 check('public browser SQL returns twelve exceptions',sql.rows[0][0]===12);
 const readonly=await page.evaluate(async()=>{try{await PMApp.api('/api/sql',{body:JSON.stringify({sql:'PRAGMA query_only=OFF'})});return false}catch(_){return true}});
 check('public SQL remains read-only',readonly);
 const [csv]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);
 check('public CSV download',(await fs.promises.readFile(await csv.path(),'utf8')).includes('222440'));
 await page.goto(base+'learn.html?view=practice&unit=1');await page.waitForSelector('#step-title');await page.locator('[data-phase=practice]').click();await page.locator('#templates summary').click();
 const [template]=await Promise.all([page.waitForEvent('download'),page.locator('#templates a[download]').first().click()]);
 check('public Korean template download',(await fs.promises.readFile(await template.path(),'utf8')).includes('프로젝트 헌장'));
 const future=await page.evaluate(()=>PMApp.api('/api/lesson?unit=9'));check('future worked examples withheld in initial lesson',future.guideSteps.every(s=>s.locked&&!s.html));
 await page.locator('#stage-caption').click();await page.selectOption('#stage','S4');await page.locator('#change-stage').click();
 await page.waitForFunction(()=>document.querySelector('#stage-caption').textContent.includes('S4'));
 await page.goto(base+'learn.html?view=practice&unit=9');await page.waitForSelector('#step-title');check('final quality step opens',(await page.locator('#step-title').innerText()).includes('검증'));
 await page.goto(base+'resources.html');check('public print stage follows selection',(await page.locator('#print-stage').innerText()).includes('S4'));
 for(const link of await page.locator('#print-links a').evaluateAll(a=>a.map(x=>x.href))){const r=await page.request.get(link);check('public PDF available',r.ok()&&(await r.body()).subarray(0,4).toString()==='%PDF')}
 await page.locator('a',{hasText:'양식 보기'}).first().click();check('public form preview opens',await page.locator('table').count()>0);
 const manifest=await (await page.request.get(base+'site-manifest.json')).json();check('public manifest excludes instructor material',manifest.files.every(f=>!/(05_강사용|06_실습수행기록|완성문서|강사_전체)/.test(f.path)));
 check('no browser exceptions',errors.length===0);
 fs.writeFileSync(path.join(__dirname,'../검증/Pages_공개주소검증.json'),JSON.stringify({checkedAt:new Date().toISOString(),url:base,passed:true,checks,errors},null,2));
 console.log(`${checks.length} live website checks passed: ${base}`);
}
run().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
