import {readSchedule,schedule,workdayDate,earnedValue,readAlternatives} from './visual-model.mjs';
const $=s=>document.querySelector(s),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const api=window.PMApp.api;
const stages={S0:'착수 전',S0A:'헌장 승인',S1:'분야 계획',S1A:'통합 승인·킥오프',S2:'실행·변경 분석',S3:'변경 승인',S4:'검수·종료'};
const modules={workflow:{unit:0,title:'정산 업무를 한 장의 흐름으로',stage:'S0'},charter:{unit:1,title:'헌장이 검토와 승인을 통과하는 과정',stage:'S0'},schedule:{unit:3,title:'선후관계가 간트차트가 되는 과정',stage:'S1'},change:{unit:8,title:'성과를 읽고 변경 대안을 비교하기',stage:'S2'}};
let active=new URLSearchParams(location.search).get('lab')||'workflow',generation=0,currentStage='S0';
if(!Object.hasOwn(modules,active))active='workflow';
const money=n=>(n/1000000).toLocaleString('ko-KR',{maximumFractionDigits:2})+'백만원';
const doc=id=>api('/api/detail?menu=documents&id='+id).then(d=>d.document);
const query=async sql=>{const d=await api('/api/sql',{body:JSON.stringify({sql})});return d.rows.map(r=>Object.fromEntries(d.columns.map((c,i)=>[c,r[i]])));};
function intro(k,description){const m=modules[k];return `<section class="wb-intro"><span class="eyebrow">UNIT ${String(m.unit).padStart(2,'0')} / ${esc(currentStage)}</span><h2>${esc(m.title)}</h2><p>${description}</p><div class="wb-reading-links"><a href="learn.html?unit=${m.unit}">${m.unit}단원 교재로 돌아가기 →</a><a href="resources.html">작성 양식 찾기 →</a></div></section>`;}
function sources(docs){return '<div class="wb-facts">'+docs.filter(Boolean).map(d=>`<a href="erp.html?menu=documents&q=${esc(d.doc_id)}" target="_blank" rel="noopener">${esc(d.doc_id)} ${esc(d.title)} ↗</a>`).join('')+'</div>'+docs.filter(Boolean).map(d=>`<details class="wb-source"><summary>${esc(d.doc_id)} 원천 내용 확인 · ${esc(d.version)} · ${esc(d.effective_date)}</summary><p>${esc(d.body)}</p></details>`).join('');}
function prompt(title,items,file){return `<section class="wb-prompt"><h3>${title}</h3><ol>${items.map(s=>'<li>'+s+'</li>').join('')}</ol>${file?`<a download href="templates/${encodeURIComponent(file)}">${esc(file.replace('.md',''))} 양식 내려받기 →</a>`:''}</section>`;}
function marker(id){return `<defs><marker id="${id}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#8391a9"/></marker></defs>`;}
function metric(label,value,note){return `<div class="wb-metric"><span>${label}</span><strong>${esc(value)}</strong><small>${note}</small></div>`;}
async function workflow(){
 const s05=await doc('S05');
 const steps=[...s05.body.matchAll(/(\d{2}:\d{2}) ([^→.\n]+)(?=→|\.)/g)].map(m=>({time:m[1],name:m[2]}));
 if(steps.length!==5)throw Error('S05의 정산 업무 순서를 확인해 주세요.');
 const notes=[
 ['입력의 범위를 확인합니다','어떤 날짜·가맹점의 자료인지 확인하세요. 거래파일 수신 시각과 실제 정산일을 같은 뜻으로 쓰지 않습니다.','거래번호, 정산번호, 기준일을 G00에 연결합니다.'],
 ['취소 반영 여부를 확인합니다','결제 총액만 보고 지급액을 정할 수 없습니다. 거래의 취소금액을 별도로 읽으세요.','가맹점 정산에서 거래금액과 취소금액을 나란히 확인합니다.'],
 ['금액의 주인을 구분합니다','수수료와 가맹점 지급예정액은 다릅니다. 배치 조정은 거래별 수수료와 별개입니다.','ST001을 조회한 뒤 수수료·조정·지급예정액을 구분해 적습니다.'],
 ['두 자료가 같은 거래를 가리키는지 봅니다','계산액과 수신액을 거래번호로 대조합니다. 금액이 다르면 원인과 담당자를 확인할 일이 남습니다.','거래 대사에서 판정=불일치 조건으로 조회하고 한 건의 차이를 설명합니다.'],
 ['예외의 인계 조건을 정합니다','예외를 전달했다는 사실만으로 해결된 것은 아닙니다. 담당자·사유·기한을 읽고 후속 확인을 남기세요.','TX001001의 예외 담당자와 사유를 확인해 PM의 후속 질문을 적습니다.']
 ];
 const diagram=i=>`<div class="wb-figure"><svg viewBox="0 0 1020 180" role="img" aria-label="S05 정산 절차: ${esc(steps.map(s=>s.time+' '+s.name).join(' → '))}">${marker('flow-arrow')}${steps.map((s,j)=>`${j<4?`<path class="arrow" d="M${j*204+186},83 H${(j+1)*204+6}" marker-end="url(#flow-arrow)"/>`:''}<rect class="node ${i===j?'chosen':''}" x="${j*204+10}" y="30" width="176" height="110" rx="10"/><text x="${j*204+27}" y="61" class="light">${s.time} · 운영팀</text><text x="${j*204+27}" y="93">${esc(s.name)}</text><text x="${j*204+27}" y="120" class="light">${j+1} / 5</text>`).join('')}</svg></div>`;
 $('#wb-content').innerHTML=intro('workflow','S05에 적힌 현행 업무를 펼친 그림입니다. 그림 아래 단계 버튼을 눌러 PM이 어떤 자료와 인계 조건을 확인하는지 읽어 보세요.')+sources([s05])+`<section class="card"><div id="flow-diagram"></div><p class="wb-caption">시각은 단계 시작·전달 시점입니다. 각 구간의 공수나 단계별 소요시간을 뜻하지 않습니다. S05의 운영팀 3명은 서로 단계를 대신 수행할 수 있습니다.</p><div class="wb-selectors">${steps.map((s,i)=>`<button data-flow="${i}">${i+1}. ${esc(s.name)}</button>`).join('')}</div><div id="flow-detail" class="wb-detail"></div></section>`+prompt('G00에 그림의 의미를 옮기세요',['수신 → 취소 → 수수료 → 대조 → 예외 전달 중, 다른 단계의 결과를 기다리는 곳을 표시하세요.','정산금·수수료·회사 매출을 구분하고 ST001의 근거를 한 줄로 적으세요.','예외 한 건에서 담당자·기한·완료 확인 방법을 찾아 다음 질문을 작성하세요.'],'G00_업무파악_작성용초안.md');
 const choose=i=>{$('#flow-diagram').innerHTML=diagram(i);$('#flow-detail').innerHTML=`<h3>${esc(notes[i][0])}</h3><p>${esc(notes[i][1])}</p><p><strong>직접 확인:</strong> ${esc(notes[i][2])}</p><a href="erp.html?menu=${i<3?'settlements&field='+encodeURIComponent('정산번호')+'&value=ST001':'reconciliation&field='+encodeURIComponent('판정')+'&value='+encodeURIComponent('불일치')}" target="_blank" rel="noopener">관련 ERP 자료 열기 ↗</a>`;document.querySelectorAll('[data-flow]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.flow)===i));};
 document.querySelectorAll('[data-flow]').forEach(b=>b.onclick=()=>choose(Number(b.dataset.flow)));choose(0);
}
async function charter(){
 const [s02,s17,s16]=await Promise.all([doc('S02'),doc('S17'),doc('S16')]);
 const steps=[['원천 확인','PM 한지우','S01 사업 필요, S02 권한, S03 요구, S17 측정·경계를 확인합니다. 각 문장의 출처를 D01 항목에 연결하세요.','초안 준비'],['헌장 초안','PM 한지우','사업 목적·목표·제외범위·PM 권한·초기 위험을 작성합니다. 132백만원을 상세 원가기준선 승인으로 적지 않습니다.','D01 v0.1'],['담당자 검토','운영·재무·개발·보안','운영에는 측정과 인수, 재무에는 자금 확보, 개발에는 구현 가능성, 보안에는 포털 경계를 확인합니다. 역할별 회신을 검토 의견으로 구분하세요.','검토 의견'],['수정·대조','PM 한지우','목표에 측정 기간·책임자를 붙이고, 투자 한도와 승인 상태를 구분합니다. 초안과 수정 이유를 남깁니다.','검토 반영본'],['스폰서 결정','윤서진','S0A의 S16 회신을 연 뒤 AP00 조건과 자신의 수정본을 대조합니다. 다른 조건이 남았다면 임의로 승인되었다고 적지 않습니다.','승인 근거 확인']];
 const xs=[24,24,365,24,706];
 const svg=i=>`<div class="wb-figure"><svg viewBox="0 0 1010 540" role="img" aria-label="헌장 업무: PM 초안 → 담당자 검토 → PM 수정 → 스폰서 승인">${marker('charter-arrow')}${['PM · 한지우','실무 검토자','스폰서 · 윤서진'].map((t,j)=>`<rect x="${j*341+8}" y="10" width="325" height="520" rx="8" fill="${j===1?'#edf2fa':'#f6f4ef'}"/><text x="${j*341+28}" y="40">${t}</text>`).join('')}${steps.map((s,j)=>`${j<4?`<path class="arrow" d="M${xs[j]+137},${j*88+127} L${xs[j+1]+137},${(j+1)*88+65}" marker-end="url(#charter-arrow)"/>`:''}<rect class="node ${i===j?'chosen':''}" x="${xs[j]}" y="${j*88+65}" width="274" height="62" rx="8"/><text x="${xs[j]+16}" y="${j*88+90}">${j+1}. ${esc(s[0])}</text><text class="light" x="${xs[j]+16}" y="${j*88+112}">${esc(s[3])}</text>`).join('')}</svg></div>`;
 $('#wb-content').innerHTML=intro('charter','헌장은 작성자·검토자·승인자를 거쳐 갑니다. 그림 아래 단계 버튼을 눌러 필요한 입력과 다음으로 넘길 증거를 확인하세요. 그림을 누르는 것은 승인 행위가 아닙니다.')+sources([s02,s17])+`<section class="card"><div id="charter-diagram"></div><div class="wb-selectors">${steps.map((s,i)=>`<button data-charter="${i}">${i+1}. ${s[0]}</button>`).join('')}</div><div id="charter-detail" class="wb-detail"></div></section><section class="wb-approval"><strong>현재 ERP의 헌장 승인 자료</strong><p>${s16?'S16 · AP00 회신이 공개되어 있습니다. 자신의 문서가 회신 조건과 일치하는지 확인한 후 버전과 승인 근거를 기록하세요.':'현재 자료에는 S16 승인 회신이 없습니다. 먼저 1단원의 검토·수정을 마친 뒤 S0A 자료를 여세요.'}</p>${sources([s16])}</section>`+prompt('D01 초안 → 검토본 → 승인본을 구분하세요',['원천의 사실, PM의 판단, 스폰서의 승인을 서로 다른 칸으로 표시하세요.','검토 의견 한 건에서 수정 전 문장 → 확인한 근거 → 수정 문장을 연결하세요.','AP00 조건과 수정본이 일치하는지 확인하고, 초안·검토 이력을 보존하세요.'],'D01 헌장.md');
 const choose=i=>{$('#charter-diagram').innerHTML=svg(i);$('#charter-detail').innerHTML=`<h3>${i+1}. ${steps[i][0]} · ${steps[i][1]}</h3><p>${steps[i][2]}</p><span class="wb-chip">남길 증거: ${steps[i][3]}</span>`;document.querySelectorAll('[data-charter]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.charter)===i));};
 document.querySelectorAll('[data-charter]').forEach(b=>b.onclick=()=>choose(Number(b.dataset.charter)));choose(0);
}
function network(model,result,lag=0){
 const positions={A:[14,112],B:[174,112],C:[334,40],D:[334,184],E:[494,112],F:[654,112],G:[814,112]};
 const current=result?.activities||model.activities;
 const edges=current.flatMap(a=>a.predecessors.map(p=>{const [x,y]=positions[p],[nx,ny]=positions[a.id];const mid=(x+132+nx)/2;return `<path class="arrow" d="M${x+132},${y+40} H${mid} V${ny+40} H${nx-3}" marker-end="url(#network-arrow)"/>`;})).join('');
 const nodes=current.map(a=>{const [x,y]=positions[a.id];const critical=result&&a.critical;return `<rect x="${x}" y="${y}" width="132" height="80" rx="8" class="node ${critical?'critical':''}"/><text x="${x+10}" y="${y+23}" class="${critical?'white':''}">${a.id} · ${esc(({D:'대사·예외',F:'교육·전환'})[a.id]||a.name)}</text><text x="${x+10}" y="${y+47}" class="${critical?'white':'light'}">${a.duration}영업일${critical?' · 주공정':''}</text><text x="${x+10}" y="${y+66}" class="${critical?'white':'light'}">${result?`ES ${a.es} / EF ${a.ef}`:esc(a.owner)}</text>`;}).join('');
 return `<div class="wb-figure"><svg viewBox="0 0 960 285" role="img" aria-label="활동 네트워크 A에서 B, C와 D로 분기, E에서 합류 후 F, G">${marker('network-arrow')}${edges}${nodes}</svg></div><p class="wb-caption">C와 D는 병렬입니다. E는 두 선행 조건을 모두 만족해야 합니다. D → E 관계: FS ${lag>=0?'+':''}${lag}영업일. ${result?'갈색과 ‘주공정’ 표시는 총여유 0인 활동입니다.':'계산 전에 두 경로의 길이를 먼저 예상해 보세요.'}</p>`;
}
function gantt(original,current,start){
 const end=Math.ceil(Math.max(original.finish,current.finish)/5)*5,width=680/end,left=225,height=90+current.activities.length*60;
 const grid=Array.from({length:end/5+1},(_,i)=>`<path class="gridline" d="M${left+i*5*width},40 V${height-25}"/><text class="light" text-anchor="middle" x="${left+i*5*width}" y="27">${i*5}</text>`).join('');
 const rows=current.activities.map((a,i)=>{const b=original.activities.find(b=>b.id===a.id),y=54+i*60;return `<text x="10" y="${y+16}">${a.id} · ${esc(a.name)}</text><text class="light" x="10" y="${y+36}">${workdayDate(start,a.es)} → ${workdayDate(start,a.ef-1)}</text><rect class="${a.critical?'critical':'normal'}" x="${left+a.es*width}" y="${y}" width="${a.duration*width}" height="22" rx="3"/><text class="white" x="${left+a.es*width+5}" y="${y+15}">${a.duration}일${a.critical&&a.duration>=10?' · 주공정':''}</text><rect class="original" x="${left+b.es*width}" y="${y+28}" width="${b.duration*width}" height="14" rx="2"/>`;}).join('');
 return `<div class="wb-figure"><svg viewBox="0 0 950 ${height}" role="img" aria-label="S06 원안 점선과 연습안 실선 간트 비교. 기술 작업 ${current.finish}영업일">${grid}${rows}<text class="light" x="225" y="${height-4}">영업일 경계 · 0은 착수 시점 / 월~금 교육 달력</text></svg></div>`;
}
async function scheduleLab(){
 const [s06,s02]=await Promise.all([doc('S06'),doc('S02')]);
 const model=readSchedule(s06.body),original=schedule(model.activities),c=model.activities.find(a=>a.id==='C'),d=model.activities.find(a=>a.id==='D');
 $('#wb-content').innerHTML=intro('schedule','S06의 원안을 먼저 읽고 두 경로의 길이를 예상하세요. 계산을 펼친 뒤 기간과 선행·지연을 바꾸면 후속 일정과 여유가 함께 바뀝니다.')+sources([s06,s02])+`<section class="card"><span class="wb-chip">원천 조건: FS · 지연 0</span><span class="wb-chip">연습용 변경 · 승인 전</span><p>FS(Finish-to-Start)는 앞 작업이 끝난 뒤 다음 작업을 시작하는 관계입니다. Lag +3은 3영업일 대기, Lead 3은 FS −3으로 표시한 3영업일 겹치기입니다. 두 개념은 총여유와 다릅니다.</p><div class="wb-slider-grid"><div class="wb-slider"><label for="duration-c">C · 조회개발 기간</label><input id="duration-c" type="range" min="5" max="35" value="${c.duration}"><output id="value-c" for="duration-c">${c.duration}영업일</output><p>S06 원안 ${c.duration}영업일</p></div><div class="wb-slider"><label for="duration-d">D · 외주 모듈 기간</label><input id="duration-d" type="range" min="5" max="40" value="${d.duration}"><output id="value-d" for="duration-d">${d.duration}영업일</output><p>S06 원안 ${d.duration}영업일</p></div><div class="wb-slider"><label for="edge-lag">D → E · 선행·지연</label><input id="edge-lag" type="range" min="-5" max="10" value="0"><output id="value-lag" for="edge-lag">FS +0영업일</output><p>음수: Lead(겹치기) · 양수: Lag(대기)</p></div></div><div class="wb-selectors"><button id="scenario-c">C만 5일 늘려 보기</button><button id="scenario-d">D만 5일 늘려 보기</button><button id="scenario-lead">D → E를 3일 겹쳐 보기</button><button id="schedule-reset">S06 원안으로 초기화</button></div><p class="wb-note">겹쳐 수행하려면 부분 인도·시험 준비·자원·재작업 위험을 검토해야 합니다. 계산상 단축을 실행 승인으로 해석하지 않습니다. 이 실습은 기간·FS 관계만 계산하며 자원 평준화와 실제 공휴일은 적용하지 않습니다.</p><button id="schedule-reveal" class="button primary">먼저 예상한 뒤 계산 결과 펼치기</button></section><section class="card"><h3>선후관계 네트워크</h3><div id="schedule-network">${network(model)}</div></section><div id="schedule-result" class="wb-result" hidden></div>`+prompt('D14 일정표로 가져갈 세 가지',['C의 기간이 5일 늘 때와 D가 5일 늘 때, 전체 완료일에 미치는 영향이 다른 이유를 설명하세요.','D → E에 Lead를 적용해도 C의 완료 조건이 남는지 확인하세요. 겹칠 수 있는 인도물과 확인 담당자를 적으세요.','선택한 연습안의 기간·선후관계·ES/EF·여유·날짜를 적고, 원안과 변경 사유를 함께 보존하세요. 기술 작업 완료일과 종료 행정 완료일은 별도입니다.'],'D14 활동_일정표.md')+'<p class="wb-note">개념 참고: <a href="https://www.pmi.org/learning/library/critical-path-scheduling-work-breakdown-6212" target="_blank" rel="noopener">PMI의 주공정·선행·지연 설명</a>. 회사 수치와 달력은 S06·S02의 교육용 가정입니다.</p>';
 let revealed=false;
 const calculate=()=>{
  const cd=Number($('#duration-c').value),dd=Number($('#duration-d').value),lag=Number($('#edge-lag').value);
  $('#value-c').textContent=cd+'영업일';$('#value-d').textContent=dd+'영업일';$('#value-lag').textContent=`FS ${lag>=0?'+':''}${lag}영업일`;
  const activities=model.activities.map(a=>({...a,duration:a.id==='C'?cd:a.id==='D'?dd:a.duration}));
  if(!revealed){$('#schedule-network').innerHTML=network({...model,activities},null,lag);return;}
  const result=schedule(activities,{'D>E':lag}),delta=result.finish-original.finish,changed=cd!==c.duration||dd!==d.duration||lag!==0;
  $('#schedule-reveal').hidden=true;$('#schedule-result').hidden=false;$('#schedule-network').innerHTML=network(model,result,lag);
  const rows=result.activities.map(a=>`<tr><th>${a.id} ${esc(a.name)}</th><td>${a.duration}</td><td>${a.es}</td><td>${a.ef}</td><td>${a.ls}</td><td>${a.lf}</td><td>${a.float}${a.critical?' · 주공정':''}</td><td>${workdayDate(model.start,a.es)}</td><td>${workdayDate(model.start,a.ef-1)}</td></tr>`).join('');
  $('#schedule-result').innerHTML=`<div class="wb-detail"><strong>${changed?'연습 가정 적용 · 승인 전':'S06 원안 계산 · 승인 상태와 별개'}</strong><p>C ${cd}일 / D ${dd}일 / D → E: FS ${lag>=0?'+':''}${lag}일. 이 조건으로 계산한 기술 작업 일정입니다.</p></div><div class="wb-grid">${metric('기술 작업 기간',result.finish+'영업일',`원안 ${original.finish}일 대비 ${delta>0?'+':''}${delta}일`)}${metric('기술 작업 완료',workdayDate(model.start,result.finish-1),'종료 행정과 편익 측정은 별도')}${metric('총여유 0인 활동',result.critical.join(' · '),'갈색 + 주공정 표시로 함께 구분')}</div><section class="card"><h3>원안과 연습안을 겹쳐 보는 간트차트</h3><p class="wb-legend">색 막대: 현재 계산 / 점선: S06 원안 / 갈색: 총여유 0 · 넓은 그림은 가로로 움직여 보세요.</p>${gantt(original,result,model.start)}</section><section class="card"><h3>계산을 문서로 옮기는 표</h3><p class="wb-note">ES/EF/LS/LF는 0에서 세는 경계값입니다. 시작 일차는 ES+1, 종료 일차는 EF입니다. 총여유 = LS−ES.</p><div class="reading-table"><table><thead><tr><th>활동</th><th>기간</th><th>ES</th><th>EF</th><th>LS</th><th>LF</th><th>총여유</th><th>시작일</th><th>종료일</th></tr></thead><tbody>${rows}</tbody></table></div></section>`;
 };
 const show=()=>{revealed=true;calculate();};
 const reset=()=>{$('#duration-c').value=c.duration;$('#duration-d').value=d.duration;$('#edge-lag').value=0;calculate();};
 for(const id of ['duration-c','duration-d','edge-lag'])$('#'+id).oninput=calculate;
 $('#schedule-reveal').onclick=show;$('#schedule-reset').onclick=reset;
 $('#scenario-c').onclick=()=>{reset();$('#duration-c').value=c.duration+5;show();};
 $('#scenario-d').onclick=()=>{reset();$('#duration-d').value=d.duration+5;show();};
 $('#scenario-lead').onclick=()=>{reset();$('#edge-lag').value=-3;show();};
}
async function change(){
 const [s10,s11,s12,performance,baselines]=await Promise.all([doc('S10'),doc('S11'),doc('S12'),query('SELECT SUM(pv) AS pv,SUM(ev) AS ev,SUM(ac) AS ac FROM performance'),query('SELECT * FROM baseline ORDER BY version')]);
 const base=baselines.find(b=>b.version==='BL01'),totals=performance[0],evm=earnedValue(totals.pv,totals.ev,totals.ac),alts=readAlternatives(s11.body,base);
 const max=Math.max(totals.pv,totals.ev,totals.ac,1);
 const bars=[['PV 계획가치',totals.pv,''],['EV 획득가치',totals.ev,'ev'],['AC 실제원가',totals.ac,'ac']].map(([label,n,cls])=>`<div class="wb-bar-row"><span>${label}</span><div class="wb-bar-track"><div class="wb-bar ${cls}" style="width:${n/max*100}%"></div></div><strong>${money(n)}</strong></div>`).join('');
 $('#wb-content').innerHTML=intro('change','S10의 실적에서 편차를 읽고, S11의 세 대안을 비교합니다. 후보를 선택하는 것과 스폰서가 기준선을 승인하는 것은 다른 일입니다.')+sources([s10,s11])+`<section class="card"><h3>같은 기준일의 계획·가치·원가</h3><p class="wb-note">S10 · 2026-11-30 · performance 원천 집계 / 단위 백만원</p><div class="wb-bars">${bars}</div><div class="wb-grid">${metric('일정 성과지수 SPI',evm.spi.toFixed(3),'EV / PV · 일수로 직접 환산하지 않음')}${metric('원가 성과지수 CPI',evm.cpi.toFixed(3),'EV / AC · 지출액을 진척률로 쓰지 않음')}${metric('원가 편차 CV',money(evm.cv),'EV − AC · 음수는 원가 초과 방향')}</div><p>일정 편차 SV는 ${money(evm.sv)}의 가치 차이입니다. 실제 지연 일수는 선후관계와 잔여 작업을 별도로 분석합니다. AC는 비용이며 현금 지급과 같지 않습니다.</p></section><section class="card"><h3>CR01 요청 → 영향 분석 → 검토 → 승인</h3><p>R06 CSV 다운로드 요청의 비용·납기·자원 조건을 비교하세요. 현재 화면의 선택은 검토 후보입니다.</p><div class="wb-selectors">${alts.map(a=>`<button data-alternative="${a.id}" aria-pressed="false">${a.name}</button>`).join('')}</div><div id="change-detail" class="wb-detail"><p>세 대안 중 하나를 눌러 영향과 검토 질문을 확인하세요.</p></div></section><section class="wb-approval"><strong>공식 변경 승인 자료</strong><p>${s12?'S12 · AP02가 현재 자료에 있습니다. 아래 원천 회신을 읽고 자신의 비교·권고와 실제 승인 내용을 대조하세요. BL01 이력을 보존하고 승인된 BL02에만 적용합니다.':'현재 자료에는 변경 승인 회신 S12가 없습니다. S11의 권고를 승인으로 기록하지 마세요. 대안 검토를 마친 뒤 S3 자료를 엽니다.'}</p>${sources([s12])}</section>`+prompt('D05·D06에 판단 근거를 남기세요',['SPI와 CPI를 설명하되 SPI 부족분을 지연 일수로 바꾸지 마세요.','세 대안의 비용·완료일·자원 제약을 비교하고 권고 이유와 확인할 담당자를 적으세요.','PM 분석 → 최민석·이현우·박다은 검토 → 윤서진 승인 → 관련 문서 갱신의 순서와 근거를 연결하세요.'],'D06 변경요청_결정대장.md');
 document.querySelectorAll('[data-alternative]').forEach(button=>button.onclick=()=>{const a=alts.find(a=>a.id===button.dataset.alternative);document.querySelectorAll('[data-alternative]').forEach(b=>b.setAttribute('aria-pressed',b===button));$('#change-detail').innerHTML=`<span class="wb-chip">검토 후보 · 선택은 승인 아님</span><h3>${a.name}</h3><div class="wb-grid">${metric('추가 작업 비용',money(a.cost),'변경 전 원가 기준선 '+money(base.bac))}${metric('제안 원가 기준선',money(base.bac+a.cost),'관리예비비는 별도 · 신규 투자 검토')}${metric('제안 종료일',a.end,`기술 작업 ${a.days?'+':''}${a.days}영업일 영향`)}</div><p>${a.tradeoff}</p><p><strong>검토 질문:</strong> 추가 비용은 누가 승인하고, 운영 인수·QA 자원·종료 후 편익 측정에는 어떤 영향이 있나요?</p>`;});
}
async function load(){
 const token=++generation;$('#wb-error').textContent='';$('#wb-content').textContent='현재 시점의 원천자료를 읽고 있습니다…';$('#wb-download').disabled=true;$('#wb-print').disabled=true;
 document.querySelectorAll('[data-module]').forEach(b=>b.setAttribute('aria-current',b.dataset.module===active));
 try{
  const meta=await api('/api/meta');if(token!==generation)return;
  currentStage=meta.stage;$('#wb-stage-label').textContent=`현재 자료: ${meta.stage} · ${stages[meta.stage]} / ${meta.as_of}`;
  $('#wb-stage').innerHTML=Object.entries(stages).map(([id,name])=>`<option value="${id}">${id} · ${name}</option>`).join('');$('#wb-stage').value=meta.stage;
  const m=modules[active];history.replaceState(null,'','visual.html?lab='+active);
  if(Object.keys(stages).indexOf(meta.stage)<Object.keys(stages).indexOf(m.stage)){
   $('#wb-content').innerHTML=intro(active,'이 실습은 앞 단원의 문서 검토 이후에 진행합니다.')+`<section class="wb-lock"><h3>${m.stage} · ${stages[m.stage]} 자료가 필요합니다</h3><p>현재 자료에는 이 실습의 입력이 아직 없습니다. ${m.unit}단원 교재에서 준비할 문서를 확인한 뒤 위쪽의 자료 선택에서 해당 시점을 여세요. 미래 수치와 계산 결과는 지금 표시하지 않습니다.</p><a href="learn.html?unit=${m.unit}">${m.unit}단원 준비사항 읽기 →</a></section>`;return;
  }
  // Disable module changes while rendering, so an older request cannot replace a newer view.
  await ({workflow,charter,schedule:scheduleLab,change}[active])();
  if(token===generation){$('#wb-download').disabled=false;$('#wb-print').disabled=false;}
 }catch(e){if(token===generation){$('#wb-content').textContent='실습 자료를 열지 못했습니다.';$('#wb-error').textContent=e.message;}}
}
let busy=false;
async function navigate(next){if(busy)return;busy=true;document.querySelectorAll('[data-module]').forEach(b=>b.disabled=true);$('#wb-stage-open').disabled=true;try{active=next;await load();}finally{busy=false;document.querySelectorAll('[data-module]').forEach(b=>b.disabled=false);$('#wb-stage-open').disabled=false;}}
 document.querySelectorAll('[data-module]').forEach(b=>b.onclick=()=>navigate(b.dataset.module));
$('#wb-stage-open').onclick=async()=>{if(busy)return;busy=true;$('#wb-stage-open').disabled=true;document.querySelectorAll('[data-module]').forEach(b=>b.disabled=true);try{await api('/api/stage',{body:JSON.stringify({stage:$('#wb-stage').value})});await load();}catch(e){$('#wb-error').textContent=e.message;}finally{busy=false;$('#wb-stage-open').disabled=false;document.querySelectorAll('[data-module]').forEach(b=>b.disabled=false);}};
$('#wb-print').onclick=()=>window.print();
$('#wb-download').onclick=()=>{
 const content=$('#wb-content').cloneNode(true);
 content.querySelectorAll('button,.wb-slider-grid,.wb-selectors,.wb-reading-links').forEach(e=>e.remove());
 content.querySelectorAll('a[href]').forEach(a=>a.href=new URL(a.getAttribute('href'),location.href).href);
 const css=[...document.styleSheets].map(s=>[...s.cssRules].map(r=>r.cssText).join('\n')).join('\n');
 const title='모아페이 시각화 워크북 · '+modules[active].title;
 const html=`<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${css}</style><main><p>학습용 그림·계산 결과 / 자료 ${esc(currentStage)} / 원천 및 승인 기준선과 별도로 보관합니다.</p><div id="wb-content">${content.innerHTML}</div></main></html>`;
 const url=URL.createObjectURL(new Blob([html],{type:'text/html;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=`모아페이_시각화_${active}_${currentStage}.html`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
navigate(active);
