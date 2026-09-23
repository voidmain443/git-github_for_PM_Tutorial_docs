/* Calculations use source facts; no saved learner records or ERP writes. */
export function readSchedule(body) {
  const rows = [...body.matchAll(/(?:^|[. ]+)([A-G]) ([^\n.]+?) (\d+)(?:영업)?일 (선행없음|[A-G](?:,[A-G])*후)\/([^\.\n]+)/g)];
  const start = body.match(/기술 작업 시작\s*(\d{4}-\d{2}-\d{2})/)?.[1];
  if (rows.length !== 7 || !start || !body.includes('지연0')) throw Error('S06의 활동·달력 형식을 확인해 주세요.');
  return {start, activities: rows.map(([,id,name,days,pred,owner]) => ({id,name:name.trim(),duration:Number(days),predecessors:pred==='선행없음'?[]:pred.replace('후','').split(','),owner:owner.trim()}))};
}
export function schedule(activities, lags = {}) {
  const map = new Map(activities.map(a=>[a.id,{...a,predecessors:[...a.predecessors]}]));
  if (map.size!==activities.length || !map.size) throw Error('활동 ID는 중복 없이 있어야 합니다.');
  for (const a of map.values()) {
    if (!Number.isInteger(a.duration)||a.duration<1) throw Error('기간은 1 이상의 정수 영업일입니다.');
    if (a.predecessors.some(p=>!map.has(p))) throw Error('선행 활동을 찾을 수 없습니다.');
  }
  for (const [edge,lag] of Object.entries(lags)) {
    const [from,to]=edge.split('>');
    if (!map.get(to)?.predecessors.includes(from)||!Number.isInteger(lag)) throw Error('유효한 선후 관계와 정수 지연값이 필요합니다.');
  }
  const done=new Set(),order=[];
  while (done.size<map.size) {
    const available=[...map.values()].filter(a=>!done.has(a.id)&&a.predecessors.every(p=>done.has(p)));
    if (!available.length) throw Error('선후 관계가 순환합니다.');
    for (const a of available) {
      a.es=Math.max(0,...a.predecessors.map(p=>map.get(p).ef+(lags[`${p}>${a.id}`]||0)));
      a.ef=a.es+a.duration;done.add(a.id);order.push(a);
    }
  }
  const finish=Math.max(...order.map(a=>a.ef));
  for (const a of [...order].reverse()) {
    const next=order.filter(b=>b.predecessors.includes(a.id));
    a.lf=Math.min(finish,...next.map(b=>b.ls-(lags[`${a.id}>${b.id}`]||0)));
    a.ls=a.lf-a.duration;a.float=a.ls-a.es;a.critical=a.float===0;
  }
  return {activities:order,finish,critical:order.filter(a=>a.critical).map(a=>a.id)};
}
export function workdayDate(start, offset) {
  if (!Number.isInteger(offset)||offset<0) throw Error('날짜 위치는 0 이상의 영업일입니다.');
  const d=new Date(start+'T00:00:00Z');
  if (!Number.isFinite(d.valueOf())||[0,6].includes(d.getUTCDay())) throw Error('시작일은 월~금 날짜입니다.');
  for(let i=0;i<offset;) {d.setUTCDate(d.getUTCDate()+1);if(![0,6].includes(d.getUTCDay()))i++;}
  return d.toISOString().slice(0,10);
}
export function earnedValue(pv, ev, ac) {
  if (![pv,ev,ac].every(n=>Number.isFinite(n)&&n>=0)) throw Error('금액을 확인하세요.');
  return {sv:ev-pv,cv:ev-ac,spi:pv?ev/pv:null,cpi:ac?ev/ac:null};
}
export function readAlternatives(body, baseline) {
  const cost=body.match(/개발·테스트(\d+)백만원/)?.[1];
  const days=body.match(/기술 작업(\d+)영업일 추가/)?.[1];
  const end=body.match(/종료일(\d{4}-\d{2}-\d{2})/)?.[1];
  const parallel=body.match(/병렬화 대안은 추가(\d+)백만원/)?.[1];
  if (!cost||!days||!end||!parallel||!baseline) throw Error('S11과 변경 전 기준선을 확인하세요.');
  return [
    {id:'keep',name:'기존 범위 유지',cost:0,days:0,end:baseline.end_date,tradeoff:'수작업 추출을 계속합니다. 추가 요구 R06을 구현하지 않습니다.'},
    {id:'extend',name:'순차 개발·검증',cost:Number(cost)*1000000,days:Number(days),end,tradeoff:'G 이후 H를 추가합니다. 신규 투자 승인과 종료 일정 변경이 필요합니다.'},
    {id:'parallel',name:'병렬화',cost:Number(parallel)*1000000,days:0,end:baseline.end_date,tradeoff:'QA 동시작업이 현 자원 한도를 넘습니다. 자원 확보 근거 없이 실행 가능한 안으로 확정할 수 없습니다.'}
  ];
}
