// Optional diagrams never change the learner's ERP stage or saved work.
const $ = (selector) => document.querySelector(selector);
const data = JSON.parse($('#landing-data').textContent);
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const stageCopy = [
  ['모든 문장은 근거에서 시작합니다.', '회사 자료·인터뷰·거래 기록에서 사실을 찾고, 확인이 필요한 조건을 구분합니다.'],
  ['시작할 이유와 권한을 한 문서로.', '목표·범위·책임을 헌장에 담고, 담당자 검토를 거쳐 스폰서에게 승인받을 조건을 확인합니다.'],
  ['계획들은 같은 일을 설명해야 합니다.', '요구사항을 WBS로 나누고 일정·자원·예산을 연결해 실행할 수 있는 약속을 만듭니다.'],
  ['바꾸기 전에, 영향을 연결해 봅니다.', '실적과 기준선을 비교하고 변경이 범위·일정·원가에 미치는 영향을 분석해 결정을 요청합니다.'],
  ['끝났다는 말에도 증거가 필요합니다.', '검수와 인수 기록을 대조하고, 운영·보증·편익 측정의 남은 책임을 다음 담당자에게 넘깁니다.'],
];
let scene, sceneIndex = 0, sceneLoading = false, sceneWanted = false;
const toggle = $('#scene-toggle'), fallback = $('#scene-fallback'), host = $('#scene-host');
toggle.hidden = false;
function setSceneStage(index) {
  sceneIndex = index;
  document.querySelectorAll('[data-scene-stage]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.sceneStage) === index)));
  $('#scene-heading').textContent = stageCopy[index][0];
  $('#scene-description').textContent = stageCopy[index][1];
  fallback.querySelectorAll('[data-desk-stage]').forEach(el => el.classList.toggle('is-selected', Number(el.dataset.deskStage) === index));
  scene?.setStage(index);
}
function showFallback(message = '') {
  sceneWanted = false;
  scene?.dispose(); scene = undefined;
  host.hidden = true; fallback.toggleAttribute('hidden', false);
  toggle.setAttribute('aria-pressed', 'false');
  toggle.textContent = '입체 모형으로 보기';
  $('#scene-status').textContent = message;
  $('#scene-status').classList.toggle('landing-sr-only', !message);
}
document.querySelectorAll('[data-scene-stage]').forEach(b => b.addEventListener('click', () => setSceneStage(Number(b.dataset.sceneStage))));
toggle.addEventListener('click', async () => {
  if (sceneLoading) return;
  if (scene) { showFallback(); return; }
  sceneLoading = true; sceneWanted = true; toggle.disabled = true;
  toggle.textContent = '입체 모형 준비 중…';
  try {
    const { mountScene } = await import('./landing-scene.mjs');
    host.hidden = false;
    const mounted = await mountScene(host, { onSelect: setSceneStage, onError: () => showFallback('입체 모형을 표시할 수 없어 문서 그림으로 전환했습니다. 모든 단계 설명은 계속 볼 수 있습니다.') });
    if (!sceneWanted) { mounted.dispose(); return; }
    scene = mounted; scene.setStage(sceneIndex);
    fallback.toggleAttribute('hidden', true);
    toggle.setAttribute('aria-pressed', 'true'); toggle.textContent = '문서 그림으로 보기';
    $('#scene-status').textContent = '입체 모형을 표시했습니다. 아래 단계 버튼으로 문서의 연결을 살펴보세요.';
    $('#scene-status').classList.add('landing-sr-only');
  } catch { showFallback('이 환경에서는 입체 모형을 표시할 수 없습니다. 문서 그림과 단계별 설명으로 계속 살펴보세요.'); }
  finally { sceneLoading = false; toggle.disabled = false; }
});
window.addEventListener('pagehide', () => { sceneWanted = false; scene?.dispose(); scene = undefined; });
window.addEventListener('pageshow', (event) => { if (event.persisted) showFallback(); });

const flow = [
  [['사업 제안','운영 자료'],['목표·범위','권한 정리'],['운영·재무','스폰서 검토'],['헌장','이해관계자']],
  [['인터뷰','작업 조건'],['범위 분해','선후관계 계산'],['누락·자원','완료 조건 검토'],['요구 추적','WBS·일정']],
  [['견적·품질','위험 자료'],['비용·대응','계약 조건 설계'],['재무·QA','구매 검토'],['예산·품질','리스크·조달']],
  [['기준선','작업 실적'],['편차·대안','변경 영향 분석'],['관련자 검토','권한자 결정'],['성과 보고','변경 기록']],
  [['시험 결과','운영 자료'],['검수·인수','인계 조건 대조'],['역할별 인수','종료 확인'],['종료 보고','편익 추적 인계']],
];
let journeyIndex = 0, d3, diagramWidth = 0;
function drawFlow(animate = false) {
  if (!d3) return;
  const root = $('#journey-diagram');
  const narrow = root.clientWidth < 420;
  const width = narrow ? 280 : 560, height = narrow ? 302 : 110;
  const labels = ['입력', 'PM의 행동', '검토·결정', '남기는 기록'];
  const nodes = flow[journeyIndex].map((lines,i) => ({id:i,lines,x:narrow?80:8+i*142,y:narrow?8+i*76:20}));
  const svg = d3.select(root).selectAll('svg').data([0]).join('svg').attr('viewBox',`0 0 ${width} ${height}`).attr('role','img').attr('aria-label',nodes.map((n,i)=>`${labels[i]}: ${n.lines.join(' ')}`).join(' → '));
  root.querySelector('.landing-flow')?.remove();
  svg.selectAll('*').interrupt('flow');
  const edges = nodes.slice(0,-1).map((n,i)=>({id:i,x1:narrow?n.x+57:n.x+114,y1:narrow?n.y+58:n.y+32,x2:narrow?nodes[i+1].x+57:nodes[i+1].x-5,y2:narrow?nodes[i+1].y-4:n.y+32}));
  svg.selectAll('line').data(edges,d=>d.id).join('line').attr('x1',d=>d.x1).attr('y1',d=>d.y1).attr('x2',d=>d.x2).attr('y2',d=>d.y2).attr('stroke','#87aa99').attr('stroke-width',1.5);
  const groups = svg.selectAll('g').data(nodes,d=>d.id).join(enter=>{const g=enter.append('g');g.append('rect');g.append('text').attr('class','flow-label');g.append('text').attr('class','flow-line1');g.append('text').attr('class','flow-line2');return g;}).attr('transform',d=>`translate(${d.x},${d.y})`);
  groups.select('rect').attr('width',114).attr('height',58).attr('rx',3).attr('fill',d=>d.id===3?'#176a62':'#edf3ee').attr('stroke',d=>d.id===3?'#176a62':'#cbdcd0');
  groups.select('.flow-label').attr('x',narrow?-15:0).attr('y',narrow?33:-8).attr('text-anchor',narrow?'end':'start').attr('font-size',9).attr('fill','#6a8276').text(d=>labels[d.id]);
  groups.select('.flow-line1').attr('x',57).attr('y',24).attr('text-anchor','middle').attr('font-size',12).attr('fill',d=>d.id===3?'#fff':'#173443').text(d=>d.lines[0]);
  groups.select('.flow-line2').attr('x',57).attr('y',42).attr('text-anchor','middle').attr('font-size',12).attr('fill',d=>d.id===3?'#e1efe5':'#173443').text(d=>d.lines[1]);
  svg.selectAll('.flow-packet').remove();
  if (animate && !motion.matches) {
    svg.selectAll('.flow-packet').data(edges).join('circle').attr('class','flow-packet').attr('r',3).attr('fill','#d4a653').attr('cx',d=>d.x1).attr('cy',d=>d.y1).transition('flow').delay((d,i)=>i*160).duration(320).attr('cx',d=>d.x2).attr('cy',d=>d.y2).remove();
  }
}
function selectJourney(index) {
  journeyIndex = index; const item = data.path[index];
  document.querySelectorAll('[data-journey]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.journey)===index)));
  for (const field of ['title','question','action','result','artifact']) $('#journey-'+field).textContent = item[field==='title'?'label':field];
  $('#journey-units').textContent = item.units.join('·')+'단원';
  $('#journey-link').href = `learn.html?unit=${item.units[0]}`;
  const ol = $('#journey-diagram .landing-flow');
  if (ol) [...ol.children].forEach((li,i)=>li.textContent=flow[index][i].join(' · '));
  drawFlow(true);
}
document.querySelectorAll('[data-journey]').forEach(b=>b.addEventListener('click',()=>selectJourney(Number(b.dataset.journey))));
async function loadDiagram() { try { await import('./vendor/d3.min.js'); d3 = window.d3; drawFlow(); } catch { /* The semantic text flow remains available offline. */ } }
if ('IntersectionObserver' in window) { const observer = new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){observer.disconnect();loadDiagram();}},{rootMargin:'120px'});observer.observe($('#journey')); } else loadDiagram();
if ('ResizeObserver' in window) new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-diagramWidth)>1){diagramWidth=width;drawFlow();}}).observe($('#journey-diagram'));
motion.addEventListener('change',()=>drawFlow());

let comparison = data.comparisons[0];
const phases = ['초안 그대로','근거 반영','검토 가능한 문장'];
function renderComparison() {
  const phase = Number($('#compare-range').value);
  const draft = phase===0?comparison.before:phase===1?comparison.middle:comparison.after;
  $('#compare-document').textContent = `${comparison.document} · 근거 ${comparison.sources.join(', ')}`;
  $('#compare-before-title').textContent = comparison.before.title;
  $('#compare-before').textContent = comparison.before.body;
  $('#compare-after-title').textContent = draft.title;
  $('#compare-after').textContent = draft.body;
  $('#compare-phase').textContent = phases[phase];
  $('#compare-range').setAttribute('aria-valuetext', phases[phase]);
  $('#compare-changes').replaceChildren();
  const changes = phase===0?[{label:'아직 확인할 것이 남았습니다',why:'슬라이더를 움직여 원천자료를 반영하면 어떤 설명이 더해지는지 확인하세요.'}]:comparison.changes.slice(0,phase===1?1:3);
  changes.forEach(change=>{const li=document.createElement('li'),title=document.createElement('strong'),body=document.createElement('span');title.textContent=change.label;body.textContent=change.why;li.append(title,body);$('#compare-changes').append(li);});
  $('#compare-question').textContent = comparison.question;
  $('#compare-link').href = comparison.link;
}
document.querySelectorAll('[data-compare]').forEach(b=>b.addEventListener('click',()=>{comparison=data.comparisons.find(c=>c.id===b.dataset.compare);document.querySelectorAll('[data-compare]').forEach(other=>other.setAttribute('aria-pressed',String(other===b)));$('#compare-range').value='2';renderComparison();}));
$('#compare-range').addEventListener('input',renderComparison);
