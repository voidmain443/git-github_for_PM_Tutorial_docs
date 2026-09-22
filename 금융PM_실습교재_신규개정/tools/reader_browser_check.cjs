const {chromium}=require('playwright');
const {spawn}=require('child_process'),fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..'),url='http://127.0.0.1:8899';
const python=process.env.PM_PYTHON||'python3';
let server,browser;const checks=[],errors=[];function check(n,v){assert(v,n);checks.push(n)}
async function run(){
 server=spawn(python,[path.join(root,'ERP/server.py'),'--stage','S0','--port','8899']);
 await new Promise((resolve,reject)=>{let done=false;server.stdout.on('data',()=>{if(!done){done=true;resolve()}});server.on('error',reject);server.on('exit',c=>{if(!done)reject(Error('server exit '+c))})});
 browser=await chromium.launch({headless:true,...(process.env.PM_CHROME?{executablePath:process.env.PM_CHROME}:{})});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url+'/learn?unit=0');await page.waitForSelector('#step-title');
 await page.evaluate(()=>localStorage.setItem('moapay.pm.learning.v2',JSON.stringify({format:2,units:{0:{orientation:'기존 기록 보존'}}})));
 const data=await (await page.request.get(url+'/api/lesson?unit=1')).json();
 check('S0 masks charter approval example',data.guideSteps.at(-1).locked&&!data.guideSteps.at(-1).html&&!data.guideSteps.at(-1).sections);
 check('legacy exercise bodies not exposed','exercises' in data===false);
 for(let u=0;u<10;u++){
  await page.goto(url+'/learn?unit='+u);await page.waitForSelector('#step-title');
  check('unit '+u+' has no input gate',await page.locator('textarea,input[type=checkbox]').count()===0);
  check('unit '+u+' outline can be browsed',await page.locator('.outline button:not(:disabled)').count()>0);
 }
 await page.goto(url+'/learn?unit=1');await page.waitForSelector('#step-title');
 const apiLesson=await (await page.request.get(url+'/api/lesson?unit=1')).json();const a=apiLesson.guideSteps.findIndex(s=>s.downloads?.includes('A01 가정 로그.md'));
 await page.locator('.outline [data-step="'+a+'"]').click();await page.locator('#templates summary').click();
 check('assumption download visible',await page.getByText('A01 가정 로그.md 내려받기',{exact:true}).isVisible());
 await page.locator('[data-source="S17"]').click();await page.waitForSelector('#source-panel:not([hidden])');
 check('source excerpt opens with author evidence',(await page.locator('#source-panel').innerText()).includes('박다은'));
 await page.reload();await page.waitForSelector('#step-title');check('reading position restored',(await page.locator('#step-title').innerText()).includes('가정'));
 check('old authored record untouched',await page.evaluate(()=>JSON.parse(localStorage.getItem('moapay.pm.learning.v2')).units[0].orientation==='기존 기록 보존'));
 for(const stage of ['S0A','S1','S1A','S2','S3','S4']){
  if(!await page.locator('#stage').isVisible())await page.locator('#stage-caption').click();await page.selectOption('#stage',stage);await page.locator('#change-stage').click();await page.waitForFunction(s=>document.querySelector('#stage-caption').textContent.includes(s),stage);
  const meta=await (await page.request.get(url+'/api/meta')).json();check('stage switch '+stage,meta.stage===stage);
 }
 const full=[];
 for(let u=0;u<10;u++){
  const lesson=await (await page.request.get(url+'/api/lesson?unit='+u)).json();full.push(lesson);
  for(const s of lesson.guideSteps){check('S4 available '+u+'/'+s.id,!s.locked&&s.html);for(const id of s.sources){const d=await (await page.request.get(url+'/api/detail?menu=documents&id='+id)).json();assert(d.document,'missing source '+id)}}
 }
 await page.goto(url+'/learn?unit=3');await page.waitForSelector('#step-title');await page.locator('.outline button').last().click();await page.screenshot({path:path.join(root,'검증/읽기교재_일정예제.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});check('mobile no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:path.join(root,'검증/읽기교재_모바일.png'),fullPage:true});
 await page.setViewportSize({width:1440,height:1100});await page.goto(url+'/learn?unit=9');await page.waitForSelector('#step-title');check('closure begins with quality evidence',(await page.locator('#step-title').innerText()).includes('검증'));
 check('SQL writes denied',!(await page.request.post(url+'/api/sql',{data:{sql:'DELETE FROM approval'}})).ok());
 check('arbitrary stage path denied',!(await page.request.post(url+'/api/stage',{data:{stage:'../../S4'}})).ok());
 check('cross-origin stage change denied',(await page.request.post(url+'/api/stage',{headers:{Origin:'http://example.invalid'},data:{stage:'S0'}})).status()===403);
 check('no browser exceptions',errors.length===0);
 fs.writeFileSync(path.join(root,'검증/읽기교재_화면검증.json'),JSON.stringify({passed:true,checks,scope:'isolated authored functional walkthrough; no novice learner effectiveness claim'},null,2));
 console.log(checks.length+' reader browser checks passed');
}
run().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server)server.kill()});
