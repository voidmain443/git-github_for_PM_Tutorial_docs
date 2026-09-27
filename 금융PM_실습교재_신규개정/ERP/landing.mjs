import {PREVIEW_CASE,CASES,calculateSchedule,calculatePerformance} from './outcome-model.mjs';
const $=s=>document.querySelector(s),esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const motion=matchMedia('(prefers-reduced-motion: reduce)');
const state={case:'charter',phase:3,days:4,ac:45,playing:false,timer:null};
let d3;
// Each caption describes an actual operation; playback is a finite explanation.
const phaseCopy={
 charter:['요청만 적은 메모에서 시작합니다. 누가 무엇을 확인할지 아직 빠져 있습니다.','현황 8분/건과 목표 3분/건을 구분하고, 운영책임자·측정 기간·대상을 붙입니다.','포함·제외 범위와 PM → 운영책임자 → 스폰서의 검토 경로를 연결합니다.','목표·범위·권한을 한눈에 대조합니다. 이 결과는 검토용이며 승인이나 목표 달성 기록이 아닙니다.'],
 schedule:['희망 날짜만 적으면 개발 지연이 다른 작업에 미치는 영향을 설명하기 어렵습니다.','요구 정의 2일, 개발 4일, 검수 준비 3일, 통합 검증 2일, 인계 1일을 확인합니다.','요구 정의 뒤 개발과 검수 준비를 병렬로 배치하고, 둘 다 끝난 뒤 통합 검증을 시작합니다.','파란 막대의 주공정과 검수 준비의 여유를 읽습니다. 개발 기간을 바꾸면 전체 소요기간도 다시 계산됩니다.'],
 change:['45백만원을 썼다는 사실만으로 진척을 45%라고 말할 수는 없습니다.','같은 기준시점의 계획가치 PV 50, 획득가치 EV 40, 실제원가 AC 45를 나눠 읽습니다.','SPI와 CPI를 각각 계산하고, 실제원가와 완료한 작업의 예산가치를 비교합니다.','편차의 원인과 대응 대안을 검토합니다. 완료예상원가는 가정에 따른 예측이며 승인된 예산이 아닙니다.'],
};
const headings={charter:'목표·범위·책임이 연결된 헌장',schedule:'선후관계와 여유가 보이는 일정',change:'실적의 의미와 다음 판단이 보이는 보고'};
const questions={charter:'어디까지 만들지, 누가 검토하고 결정할지 서로 다르게 이해할 수 있습니다.',schedule:'한 작업이 늦어질 때 전체 종료가 얼마나 밀리는지 알 수 없습니다.',change:'얼마나 썼는지와 얼마나 끝냈는지가 섞여 문제를 늦게 발견할 수 있습니다.'};
const answers={charter:'왜 시작하는가, 무엇을 만들고 제외하는가, 누가 검토하고 결정하는가?',schedule:'어떤 작업이 종료를 결정하는가, 어떤 작업에 여유가 있는가, 지연은 어디로 전해지는가?',change:'계획보다 얼마나 끝냈는가, 같은 일을 더 비싸게 했는가, 다음에 무엇을 확인해야 하는가?'};
const titles={charter:'“빠르고 편리하게 만들자”',schedule:'“다음 주에 개발하고 검수하자”',change:'“예산을 45% 썼으니 진척도 45%”'};
function stop(){clearTimeout(state.timer);state.timer=null;state.playing=false;$('#outcome-play').setAttribute('aria-pressed','false');$('#outcome-play').textContent=motion.matches?'한 단계씩 살펴보기':'만드는 과정 재생';}
function phase(index,animated=false){state.phase=index;$('#outcome-surface').dataset.phase=index;document.querySelectorAll('[data-outcome-step]').forEach(b=>b.setAttribute('aria-current',Number(b.dataset.outcomeStep)===index?'step':'false'));$('#outcome-caption').textContent=phaseCopy[state.case][index].replace('개발 4일',`개발 ${state.days}일`).replace('실제원가 AC 45',`실제원가 AC ${state.ac}`);renderSurface(animated);}
function list(items){return '<ul>'+items.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>';}
function renderCharter(){
 const c=CASES.charter,g=c.goals[0],p=state.phase;
 $('#outcome-surface').innerHTML=`<div class="preview-charter"><div class="preview-document-heading"><span>프로젝트 헌장 · ${PREVIEW_CASE.id}</span><strong>${PREVIEW_CASE.title}</strong><small>${PREVIEW_CASE.status}</small></div><div class="charter-goal ${p<1?'preview-unconfirmed':''}"><div><span>발송 상태 확인 시간</span><p><strong>8</strong>분/건 <b aria-hidden="true">→</b> <strong>3</strong>분/건</p><small>가상 현황 → 검토할 목표</small></div><dl><div><dt>측정 책임</dt><dd>${g.owner}</dd></div><div><dt>측정 기간</dt><dd>${g.period}</dd></div><div><dt>측정 대상</dt><dd>확인 건 전체의 평균</dd></div></dl></div><div class="charter-columns ${p<2?'preview-unconfirmed':''}"><div><h4><span class="scope-symbol">＋</span>포함할 범위</h4>${list(c.scope.included)}</div><div><h4><span class="scope-symbol minus">−</span>제외할 범위</h4>${list(c.scope.excluded)}</div></div><div class="charter-authority ${p<2?'preview-unconfirmed':''}"><span><b>PM</b><small>초안·영향 분석</small></span><i aria-hidden="true">→</i><span><b>운영책임자</b><small>업무·측정 검토</small></span><i aria-hidden="true">→</i><span><b>스폰서</b><small>승인 여부 결정</small></span></div><p class="preview-reading-note ${p<3?'preview-unconfirmed':''}">숫자에 측정 조건이 붙고, 범위에 경계가 생기고, 결정에는 책임자가 연결됩니다.</p><details class="preview-assumptions"><summary>이 예시의 측정 기준 보기</summary><p>${esc(g.baselineBasis)}입니다. ${esc(g.measurement)} ${esc(c.notes[0])}</p></details></div>`;
}
function renderSchedule(animate){
 const m=calculateSchedule(state.days),c=m.activities.find(a=>a.id==='C'),p=state.phase;
 $('#outcome-surface').innerHTML=`<div class="preview-schedule"><div class="schedule-kpis"><div><span>전체 소요기간</span><strong class="preview-finish">${m.finish}<small>영업일</small></strong></div><div><span>주공정</span><strong class="schedule-path">${m.critical.join(' → ')}</strong></div><div><span>검수 준비의 총여유</span><strong>${c.float}<small>일</small></strong></div></div><div id="preview-gantt" class="${p<2?'preview-unconfirmed':''}"></div><div class="preview-legend"><span><i class="critical-key"></i>주공정</span><span><i class="normal-key"></i>여유가 있는 작업</span><span><i class="float-key"></i>총여유</span></div><p class="preview-reading-note ${p<3?'preview-unconfirmed':''}">개발이 ${state.days-4}일 늘면 전체 일정도 ${m.finish-9}일 늘어납니다. 검수 준비는 ${c.float}일의 여유가 있지만 통합 검증 전에는 끝나야 합니다.</p><details class="preview-assumptions"><summary>일정 계산의 가정과 읽는 법</summary>${list(CASES.schedule.notes)}<p>ES/EF는 가장 빠른 시작/완료, LS/LF는 전체 종료를 늦추지 않는 가장 늦은 시작/완료입니다. 총여유 = LS − ES입니다.</p><div class="preview-table-scroll"><table><thead><tr><th>활동</th><th>ES</th><th>EF</th><th>LS</th><th>LF</th><th>총여유</th></tr></thead><tbody>${m.activities.map(a=>`<tr><th>${a.id} ${a.label}</th><td>${a.es}</td><td>${a.ef}</td><td>${a.ls}</td><td>${a.lf}</td><td>${a.float}</td></tr>`).join('')}</tbody></table></div></details></div>`;
 drawGantt(m,animate);
}
function drawGantt(model,animate){
 const host=$('#preview-gantt');if(!d3){host.innerHTML=list(model.activities.map(a=>`${a.id} ${a.label}: ${a.es}~${a.ef}일, 총여유 ${a.float}일`));return;}
 const narrow=host.clientWidth<520,w=narrow?340:760,h=260,left=narrow?88:124,right=narrow?28:45,top=36,row=42;
 const x=d3.scaleLinear().domain([0,11]).range([left,w-right]);
 const svg=d3.select(host).append('svg').attr('viewBox',`0 0 ${w} ${h}`).attr('role','img').attr('aria-label',`선후관계로 연결된 간트. 전체 ${model.finish}영업일. 주공정 ${model.critical.join(', ')}. 검수 준비의 총여유 ${model.activities[2].float}일.`);
 svg.append('text').attr('x',w-right).attr('y',12).attr('text-anchor','end').attr('font-size',11).attr('fill','#59677e').text('착수 후 경과 영업일');
 const ticks=[0,2,4,6,8,10,11];svg.selectAll('.grid').data(ticks).join('line').attr('x1',x).attr('x2',x).attr('y1',30).attr('y2',244).attr('stroke','#e0e5f0');svg.selectAll('.tick').data(ticks).join('text').attr('class','tick').attr('x',x).attr('y',26).attr('text-anchor','middle').attr('font-size',11).attr('fill','#59677e').text(d=>d);
 const map=new Map(model.activities.map((a,i)=>[a.id,{...a,y:top+i*row}]));
 const edges=svg.append('g').attr('fill','none').attr('stroke','#9cafd9').attr('stroke-width',1.3);
 for(const link of model.links){const a=map.get(link.source),b=map.get(link.target),xx=x(a.ef),yy=a.y+14,endx=x(b.es),endy=b.y+14;edges.append('path').attr('d',`M${xx},${yy}H${xx+5}V${endy}H${endx}`).attr('opacity',state.phase<2?.2:1);}
 const rows=svg.selectAll('.task').data(model.activities).join('g').attr('class','task').attr('transform',(a,i)=>`translate(0,${top+i*row})`);
 rows.append('text').attr('x',0).attr('y',19).attr('font-size',narrow?12:14).attr('font-weight',600).attr('fill','#25375b').text(a=>`${a.id}  ${a.label}`);
 rows.filter(a=>a.float>0).append('rect').attr('x',a=>x(a.ef)).attr('y',2).attr('width',a=>x(a.ef+a.float)-x(a.ef)).attr('height',25).attr('rx',3).attr('fill','#eef2f9').attr('stroke','#b5c3db').attr('stroke-dasharray','3 3');
 const bars=rows.append('rect').attr('x',a=>x(a.es)).attr('y',2).attr('height',25).attr('rx',4).attr('fill',a=>a.critical?'#3056c9':'#95a8cc').attr('width',a=>animate&&!motion.matches?0:x(a.ef)-x(a.es));
 if(animate&&!motion.matches)bars.transition('result').duration(480).attr('width',a=>x(a.ef)-x(a.es));
 rows.append('text').attr('x',a=>x(a.es)+(x(a.ef)-x(a.es))/2).attr('y',19).attr('text-anchor','middle').attr('font-size',12).attr('fill',a=>a.critical?'#fff':'#25375b').attr('font-weight',650).text(a=>`${a.duration}일`);
}
function renderChange(animate){
 const m=calculatePerformance({...CASES.change.inputs,ac:state.ac}),p=state.phase;
 $('#outcome-surface').innerHTML=`<div class="preview-performance"><div class="performance-head"><div><span>예산가치 기준 진척</span><strong>${m.progress}<small>%</small></strong><p>EV ${m.ev} ÷ BAC ${m.bac}</p></div><div><span>예산 대비 실제원가 비율</span><strong>${m.costShare}<small>%</small></strong><p>AC ${m.ac} ÷ BAC ${m.bac}</p></div><p>두 비율은<br><b>다른 질문에 답합니다.</b></p></div><div id="preview-value-bars" class="${p<1?'preview-unconfirmed':''}"></div><div class="performance-indices ${p<2?'preview-unconfirmed':''}"><div><span>일정 성과지수 SPI</span><strong class="preview-spi">${m.display.spi}</strong><small>EV / PV</small></div><div><span>원가 성과지수 CPI</span><strong class="preview-cpi">${m.display.cpi}</strong><small>EV / AC</small></div><div><span>완료예상원가 EAC</span><strong>${m.display.eac}<small>백만원</small></strong><small>BAC / CPI · 현재 효율 지속 가정</small></div></div><div class="performance-decision ${p<3?'preview-unconfirmed':''}"><span>원인 확인</span><b>→</b><span>대안 비교</span><b>→</b><span>필요 시 변경 상정</span></div><details class="preview-assumptions"><summary>단위·산식·해석의 한계 보기</summary>${list(CASES.change.notes)}<p>현재 원가 편차 CV = EV − AC = ${m.cv}백만원, 일정 편차 SV = EV − PV = ${m.sv}백만원입니다. 두 편차는 가치의 차이이며 지연 일수와 같지 않습니다.</p></details></div>`;
 const host=$('#preview-value-bars');if(!d3){host.innerHTML=list([`PV 계획가치 ${m.pv}백만원`,`EV 획득가치 ${m.ev}백만원`,`AC 실제원가 ${m.ac}백만원`]);return;}
 const w=host.clientWidth<520?340:760,left=116,right=52,x=d3.scaleLinear().domain([0,60]).range([left,w-right]),values=[{key:'PV',label:'계획가치',value:m.pv,color:'#a3b4d4'},{key:'EV',label:'획득가치',value:m.ev,color:'#3056c9'},{key:'AC',label:'실제원가',value:m.ac,color:'#b88134'}];
 const svg=d3.select(host).append('svg').attr('viewBox',`0 0 ${w} 135`).attr('role','img').attr('aria-label',`단위 백만원. PV 계획가치 ${m.pv}, EV 획득가치 ${m.ev}, AC 실제원가 ${m.ac}.`);
 const row=svg.selectAll('g').data(values).join('g').attr('transform',(d,i)=>`translate(0,${i*40+5})`);
 row.append('text').attr('x',0).attr('y',23).attr('font-size',13).attr('font-weight',550).attr('fill','#25375b').text(d=>`${d.key} ${d.label}`);
 row.append('rect').attr('x',left).attr('y',6).attr('height',25).attr('width',x(60)-left).attr('rx',4).attr('fill','#f0f3f9');
 const bars=row.append('rect').attr('x',left).attr('y',6).attr('height',25).attr('rx',4).attr('fill',d=>d.color).attr('width',d=>animate&&!motion.matches?0:x(d.value)-left);if(animate&&!motion.matches)bars.transition('result').duration(480).attr('width',d=>x(d.value)-left);
 row.append('text').attr('x',d=>x(d.value)+8).attr('y',23).attr('font-size',13).attr('font-weight',700).attr('fill','#25375b').text(d=>d.value);
}
function renderSurface(animate=false){
 if(state.case==='charter')renderCharter();else if(state.case==='schedule')renderSchedule(animate);else renderChange(animate);
 $('#outcome-surface').dataset.phase=state.phase;
}
function adjust(){const host=$('#outcome-adjust');host.hidden=state.case==='charter';if(state.case==='schedule'){host.innerHTML=`<label for="preview-days">개발 기간을 바꿔보세요</label><input id="preview-days" type="range" min="4" max="6" step="1" value="${state.days}"><output for="preview-days">${state.days}일</output><p>다른 활동 기간은 유지하고 전체 종료에 미치는 영향을 봅니다.</p>`;$('#preview-days').addEventListener('input',e=>{stop();state.days=Number(e.target.value);host.querySelector('output').textContent=state.days+'일';phase(3);});}else if(state.case==='change'){host.innerHTML=`<label for="preview-ac">실제원가만 바꿔보세요</label><input id="preview-ac" type="range" min="40" max="60" step="5" value="${state.ac}"><output for="preview-ac">${state.ac}백만원</output><p>PV·EV는 그대로입니다. 비용이 변하면 진척과 원가효율은 각각 어떻게 달라질까요?</p>`;$('#preview-ac').addEventListener('input',e=>{stop();state.ac=Number(e.target.value);host.querySelector('output').textContent=state.ac+'백만원';phase(3);});}else host.replaceChildren();}
function selectCase(id){stop();state.case=id;state.phase=3;document.querySelectorAll('[data-outcome]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.outcome===id)));const c=CASES[id];$('#outcome-before-title').textContent=titles[id];$('#outcome-before').textContent=c.beforeText;$('#outcome-question').textContent=questions[id];$('#outcome-title').textContent=headings[id];$('#outcome-answer').textContent=answers[id];$('#outcome-workbook').href=c.workbookLink;$('#outcome-document').href='documents.html?doc='+id;$('#outcome-lesson').href=c.lessonLink;adjust();phase(3,true);}
function advance(){if(!state.playing)return;if(state.phase===3){stop();return;}phase(state.phase+1,true);state.timer=setTimeout(advance,1500);}
$('#outcome-play').hidden=false;
$('#outcome-play').addEventListener('click',()=>{if(state.playing){stop();return;}if(motion.matches){phase((state.phase+1)%4);return;}state.days=4;state.ac=45;adjust();state.playing=true;$('#outcome-play').setAttribute('aria-pressed','true');$('#outcome-play').textContent='재생 멈추기';phase(0);state.timer=setTimeout(advance,1500);});
$('#outcome-notice').textContent=PREVIEW_CASE.notice+' '+PREVIEW_CASE.status+' · 조작해도 ERP 원본이나 자료 시점은 바뀌지 않습니다.';
document.querySelectorAll('[data-outcome]').forEach(b=>b.addEventListener('click',()=>selectCase(b.dataset.outcome)));
document.querySelectorAll('[data-outcome-step]').forEach(b=>b.addEventListener('click',()=>{stop();phase(Number(b.dataset.outcomeStep),true);}));
motion.addEventListener('change',()=>{stop();renderSurface();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
window.addEventListener('pagehide',stop);
if('IntersectionObserver' in window)new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop();}).observe($('#outcome-lab'));
let width=0;if('ResizeObserver'in window)new ResizeObserver(entries=>{const next=entries[0].contentRect.width;if(Math.abs(next-width)>1){width=next;renderSurface();}}).observe($('#outcome-surface'));
selectCase('charter');
try{await import('./vendor/d3.min.js');d3=window.d3;renderSurface();}catch{/* A readable HTML result remains available if the chart library cannot load. */}
