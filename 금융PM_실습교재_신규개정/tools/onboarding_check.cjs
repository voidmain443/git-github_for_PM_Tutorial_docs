// Historical test for the previous form-based UI. Current replacement: reader_browser_check.cjs.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/Users/voidmain443/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const base=process.env.PM_TEST_URL||'http://127.0.0.1:8878',out=path.resolve(__dirname,'../검증');
let browser;const checks=[];function check(n,v){assert(v,n);checks.push(n)}
async function main(){
 browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/learn?unit=0');await page.waitForSelector('#step-title');
 check('no note form or completion gate',await page.locator('textarea, #finish, #handoff').count()===0);
 check('all eight steps accessible',await page.locator('.stepnav button:not(:disabled)').count()===8);
 check('example visible without disclosure',await page.locator('.step-example p').isVisible());
 await page.evaluate(()=>{localStorage.setItem('moapay.pm.learning.v2',JSON.stringify({format:2,units:{0:{exercises:{},history:[],orientation:'이전 메모 유지',orientationSteps:{start:{note:'이전 작성 내용'}},orientationIndex:0}}}))});
 await page.reload();await page.waitForSelector('#step-title');
 for(let i=1;i<8;i++){await page.locator('.step-paging button.primary').click();check('read next step '+(i+1),(await page.locator('#step-title').innerText()).startsWith((i+1)+'.'))}
 check('charter handoff link',await page.locator('.step-paging a').getAttribute('href')==='/learn?unit=1');
 await page.reload();await page.waitForSelector('#step-title');
 check('reading position retained',(await page.locator('#step-title').innerText()).startsWith('8.'));
 check('previous notes preserved',await page.evaluate(()=>{const u=JSON.parse(localStorage.getItem('moapay.pm.learning.v2')).units[0];return u.orientation==='이전 메모 유지'&&u.orientationSteps.start.note==='이전 작성 내용'}));
 await page.locator('.stepnav [data-step="3"]').click();
 check('ERP query shortcut retained',(await page.locator('.step-links a').first().getAttribute('href')).includes('settlements'));
 await page.screenshot({path:path.join(out,'0단원_읽기안내.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});
 check('mobile no overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.screenshot({path:path.join(out,'0단원_읽기안내_모바일.png'),fullPage:true});
 await page.goto(base+'/learn?unit=1');await page.waitForSelector('#learning-guide');
 check('other unit preserved',await page.locator('[data-ex]').count()>0&&await page.locator('#export').isVisible());
 check('browser errors absent',errors.length===0);
 fs.writeFileSync(path.join(out,'0단원_따라하기검증.json'),JSON.stringify({passed:true,checks,scope:'Reading navigation, saved data preservation and mobile layout; not learner effectiveness'},null,2));
 console.log(checks.length+' reading guide checks passed');
}
main().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
