// Historical test for the previous form-based UI. Current replacement: reader_browser_check.cjs.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/Users/voidmain443/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {spawn}=require('child_process'),fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..'),python=process.env.PM_PYTHON||'/Users/voidmain443/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const port=8897,base=`http://127.0.0.1:${port}`,out=path.join(root,'검증');let child,browser;const checks=[];
async function start(stage){child=spawn(python,[path.join(root,'ERP/server.py'),'--stage',stage,'--port',String(port)]);await new Promise((resolve,reject)=>{child.stdout.once('data',resolve);child.once('error',reject);child.once('exit',c=>reject(Error('ERP exited '+c)))});}
async function stop(){if(child){const p=child;child=null;await new Promise(resolve=>{p.once('exit',resolve);p.kill('SIGTERM')})}}
function check(name,ok){assert(ok,name);checks.push(name)}
async function main(){
 await start('S0');browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const context=await browser.newContext({viewport:{width:1440,height:1050}}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/learn?unit=1');await page.waitForSelector('[data-ex="4.1"]');
 check('S16 hidden before charter approval',await page.locator('[data-source="S16"]').isDisabled());
 await page.locator('[data-source="S17"]').click();await page.waitForFunction(()=>document.querySelector('#source').textContent.includes('20영업일'));
 check('source details visible alongside writing',(await page.locator('#source').innerText()).includes('기존 포털')||(await page.locator('#source').innerText()).includes('웹 포털'));
 await page.screenshot({path:path.join(out,'실습실_헌장_입력자료.png'),fullPage:false});
 const fixture={
 '4.1':[
 'MP-01 / D01 / 한지우 / 2026-10-06 / v0.1 초안',
 'S01/S05: 팀 대사120분과 예외추적 월12건 문제를 개선한다.',
 'S01/S17: 종료 다음 영업일부터20영업일 평균60분 이하. 박다은 측정·윤서진 보고. 이력100%, 계산100%.',
 'S03: 정산 조회·480거래 정확 분류·12예외 이력·권한8개·운영자3명5과업.',
 'S03/S17: 내부 도구 개선과 기존 포털 권한 회귀시험. 신규 포털·앱·결제엔진·ERP교체 제외.',
 'S01: 종료 목표2027-01-22. 상세 활동 일정은 계획 단계 추정 후 승인.',
 'S01/S04/S17: 한도132백만원, 기준선 후보120, 관리예비비12. 회사현금440은 배정액이 아님.',
 'S02: PM 업무배정·정보요청·변경상정. 기준선 변경은 검토 후 윤서진 승인.',
 'S02: 박다은 인수, 최민석 재무 검토, 이현우 기술, 정유나 품질, 오수빈 보안. D30 연결.',
 'S05/S17: 자료사용·검토협조 확인. 기존서비스 유지 제약. 운영숙련·성과측정·비용중복 위험은 계획에서 검토.',
 'S17: 인수·보안·운영·계약·재무·자원·교훈 대조 후 종료 상정. 편익 박다은 인계. 중단은 윤서진 결정.',
 'v0.1 / 검토 준비 / S0이므로 AP00 승인 대기.',
 '원천문서S01~S05/S17 문단과 인물P01/P03/P04를 대조. 작성시 미래실적 사용하지 않음.'
 ],
 '13.1':[
 '회사 인물표P01~P10, S02 역할·권한, S17 회신.',
 'D01 v0.2의 목표·검토역할·권한을 가져옴.',
 'D30에10명, 내부8명·외부2명. 외주 역할은 계약 전 후보.',
 '윤서진 승인·박다은 인수·최민석 재무·정유나 품질·오수빈 보안으로 구분.',
 '문서별 요청 시점: 헌장 스폰서, 요구 운영, 시험 QA, 계약 구매. 영향도 평가는 PM 판단으로 표시.',
 'D30 v0.1: 인물·역할·근거·관심·참여방법 표를 작성.',
 '인물 권한을 S02와 대조한 검토 기록. 인수와 종료를 구분.'
 ]};
 for(const id of ['4.1','13.1']){
  const e=page.locator(`[data-ex="${id}"]`);await e.locator(':scope > summary').click();
  await e.locator('[data-action="review"]').click();check(id+' empty submission blocked',(await page.locator('#notice').innerText()).includes('모든 작성'));
  const fields=e.locator('[data-answer]');check(id+' field fixture count',await fields.count()===fixture[id].length);
  for(let i=0;i<fixture[id].length;i++)await fields.nth(i).fill(fixture[id][i]);
  await e.locator('[data-action="review"]').click();await e.locator('[data-revision]').fill(id==='4.1'?'RV01~RV06 대조: 측정 기간·예산 후보·채널·분류·권한·종료 인계를 근거대로 명시했다. 수정 전 모호한 목표→수정 후 대상·기간·책임을 추가. S17.':'인수와 승인 권한 구분을 확인. 후보 외주와 확정 계약을 구분하도록 참여상태를 수정. S02.');
  await e.locator('[data-action="revise"]').click();await e.locator('[data-action="complete"]').click();check(id+' attestation required',(await page.locator('#notice').innerText()).includes('체크'));
  await e.locator('[data-attest]').check();await e.locator('[data-action="complete"]').click();
 }
 await page.locator('#handoff').check();await page.locator('#finish').click();check('S0 cannot claim AP00',(await page.locator('#notice').innerText()).includes('승인 자료가 아직'));
 await page.reload();await page.waitForSelector('[data-ex="4.1"]');
 check('draft revision and completion survive reload',await page.evaluate(()=>JSON.parse(localStorage.getItem('moapay.pm.learning.v2')).units[1].exercises['4.1'].history.length===3));
 check('later unit blocked server side',(await (await page.request.get(base+'/api/lesson?unit=2')).json()).error.includes('S1'));
 check('future document not exposed',(await (await page.request.get(base+'/api/detail?menu=documents&id=S16')).json()).document===null);
 await stop();await start('S0A');await page.reload();await page.waitForSelector('[data-ex="4.1"]');
 check('charter reply available at approval stage',!(await page.locator('[data-source="S16"]').isDisabled()));
 await page.locator('[data-source="S16"]').click();await page.waitForFunction(()=>document.querySelector('#source').textContent.includes('AP00'));
 await page.locator('#handoff').check();await page.locator('#finish').click();await page.waitForFunction(()=>document.querySelector('#completion').textContent.includes('AP00'));
 check('approval linked to evidence and marked self assessment',(await page.locator('#completion').innerText()).includes('자기평가'));
 const d=page.waitForEvent('download');await page.locator('#export').click();const download=await d;await download.saveAs(path.join(out,'실습실_모의헌장기록.json'));
 await page.screenshot({path:path.join(out,'실습실_헌장_승인인계.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(out,'실습실_모바일.png'),fullPage:false});
 check('mobile no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 // Editing a completed response must invalidate its approval without erasing the old snapshot.
 const e=page.locator('[data-ex="4.1"]');await e.locator(':scope > summary').click();await e.locator('[data-answer="0"]').fill('MP-01 / D01 / 수정 제안 검토 중');
 check('editing invalidates approval',await page.evaluate(()=>{const u=JSON.parse(localStorage.getItem('moapay.pm.learning.v2')).units[1];return !u.approval&&u.exercises['4.1'].status==='초안'&&u.exercises['4.1'].history.length===3}));
 check('no browser runtime errors',errors.length===0);
 fs.writeFileSync(path.join(out,'실습실_브라우저검증.json'),JSON.stringify({passed:true,checks,scope:'software workflow checks with authored fixtures; not a novice learner study'},null,2));
 console.log(`${checks.length} guided browser checks passed`);
}
main().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();await stop()});
