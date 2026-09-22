/* SQLite stays in a worker so a long student query cannot freeze the lesson. */
'use strict';
importScripts('vendor/sql-wasm.js');
const initialized = initSqlJs({locateFile: name => new URL('vendor/' + name, self.location.href).href});
let db, loadedStage, queue = Promise.resolve();
const stages = ['S0','S0A','S1','S1A','S2','S3','S4'];
const menus = {
 documents:['원천 문서','source_document','doc_id'], people:['조직·담당자','person','person_id'],
 requirements:['요구사항 추적','v_요구추적','요구번호'],budget:['예산·기준선','v_예산조회','버전'],
 cost:['프로젝트 원가','v_프로젝트원가','WBS'],journal:['회계 전표','v_전표조회','전표번호'],
 procurement:['구매·검수·지급','v_조달조회','발주번호'],settlements:['가맹점 정산','v_정산조회','정산번호'],
 reconciliation:['거래 대사','v_대사조회','거래번호'],tests:['검증 결과','test_result','test_id'],
 physical:['환경·물적자원','physical_resource','resource_id'],allocations:['자원 배정','allocation','person_group'],
 performance:['중간 성과측정','performance','posid']
};
const ident = name => '"' + name.replace(/"/g, '""') + '"';
function rows(sql, values = []) {
  const s = db.prepare(sql); try { s.bind(values); const out=[]; while(s.step()) out.push(s.getAsObject()); return out; } finally { s.free(); }
}
async function open(stage) {
  if (!stages.includes(stage)) throw Error('자료 단계가 올바르지 않습니다.');
  if (db && stage === loadedStage) return;
  const SQL = await initialized, response = await fetch(new URL(`data/${stage}.sqlite3`, self.location.href));
  if (!response.ok) throw Error('자료를 내려받지 못했습니다. 인터넷 연결을 확인한 뒤 다시 시도하세요.');
  const next = new SQL.Database(new Uint8Array(await response.arrayBuffer()));
  const actual = next.exec('SELECT stage FROM meta')[0]?.values[0]?.[0];
  if (actual !== stage) { next.close(); throw Error('자료의 시점이 일치하지 않습니다.'); }
  next.run('PRAGMA query_only=ON');
  if (db) db.close(); db = next; loadedStage = stage;
}
function listing(p) {
  if (!Object.hasOwn(menus,p.menu)) throw Error('존재하지 않는 업무 메뉴입니다.');
  const [name,view,pk] = menus[p.menu], columns=rows(`PRAGMA table_info(${ident(view)})`).map(r=>r.name);
  const where=[], values=[], q=(p.q||'').trim();
  if(q){where.push('('+columns.map(c=>`CAST(${ident(c)} AS TEXT) LIKE ?`).join(' OR ')+')');values.push(...columns.map(()=>'%'+q+'%'));}
  for(const [field,value] of [[p.field,p.value],[p.field2,p.value2]]) if(field&&value){
    if(!columns.includes(field))throw Error('잘못된 필터 항목입니다.');
    where.push(`CAST(${ident(field)} AS TEXT)=?`); values.push(value);
  }
  const clause=where.length?' WHERE '+where.join(' AND '):'', total=rows(`SELECT COUNT(*) AS n FROM ${ident(view)}${clause}`,values)[0].n;
  const offset=Math.max(0,Number.parseInt(p.offset||'0',10)||0), exporting=p.format==='csv';
  const data=rows(`SELECT * FROM ${ident(view)}${clause} ORDER BY ${ident(pk)} LIMIT ? OFFSET ?`,[...values,exporting?10000:50,exporting?0:offset]);
  const summary={};
  for(const c of columns.filter(c=>['거래금액','취소금액','수수료','지급예정액','누적비용','계산액','수신액','차이','발주액','누적검수액','누적청구액','누적지급액'].includes(c)))
    summary[c]=rows(`SELECT COALESCE(SUM(${ident(c)}),0) AS n FROM ${ident(view)}${clause}`,values)[0].n;
  return {name,columns,rows:data,total,offset,summary};
}
function detail(k,v) {
  const q=sql=>rows(sql,[v]);
  if(k==='documents')return {document:q('SELECT * FROM source_document WHERE doc_id=?')[0]||null};
  const definitions={
    procurement:{발주:'SELECT * FROM purchase_order WHERE ebeln=?',검수:'SELECT * FROM service_acceptance WHERE ebeln=?',청구:'SELECT i.* FROM invoice i JOIN service_acceptance s USING(acceptance_id) WHERE ebeln=?',지급:'SELECT p.* FROM payment p JOIN invoice i USING(invoice_id) JOIN service_acceptance s USING(acceptance_id) WHERE ebeln=?'},
    reconciliation:{원천거래:'SELECT * FROM payment_transaction WHERE tx_id=?',예외처리:'SELECT * FROM exception_case WHERE tx_id=?'},
    people:{담당자:'SELECT * FROM person WHERE person_id=?',작성문서:'SELECT doc_id,title,release_stage FROM source_document WHERE author_id=?'},
    budget:{기준선:'SELECT * FROM baseline WHERE version=?',월별비용계획:'SELECT * FROM budget_line WHERE version=?',승인:'SELECT a.* FROM approval a JOIN baseline b USING(approval_id) WHERE b.version=?'},
    cost:{작업패키지:'SELECT * FROM wbs WHERE posid=?',비용전표:"SELECT * FROM acdoca WHERE posid=? AND saknr='610000'"},
    settlements:{거래:'SELECT * FROM payment_transaction WHERE batch_id=?',예외:'SELECT e.* FROM exception_case e JOIN payment_transaction t USING(tx_id) WHERE batch_id=?'},
    journal:{헤더:'SELECT * FROM bkpf WHERE belnr=?',항목:'SELECT * FROM acdoca WHERE belnr=?'},
    requirements:{작업패키지:'SELECT w.* FROM wbs w JOIN requirement_wbs l USING(posid) WHERE req_id=?',시험:'SELECT * FROM test_result WHERE req_id=?'}
  };
  if(Object.hasOwn(definitions,k))return Object.fromEntries(Object.entries(definitions[k]).map(([name,sql])=>[name,q(sql)]));
  if(Object.hasOwn(menus,k))return {기록:q(`SELECT * FROM ${ident(menus[k][1])} WHERE ${ident(menus[k][2])}=?`)};
  return {};
}
function query(sql) {
  if(typeof sql!=='string'||sql.length>16384)throw Error('조회문은 16KB 이하로 작성하세요.');
  // Inspect before SQLite prepares anything: some PRAGMAs act during preparation.
  // Mask literals, quoted identifiers and comments without treating their punctuation as SQL.
  const masked=sql.replace(/'(?:''|[^'])*'|"(?:""|[^"])*"|`(?:``|[^`])*`|\[[^\]]*\]|\/\*[\s\S]*?\*\/|--[^\n]*/g,' ');
  const statements=masked.split(';').filter(x=>x.trim());
  if(statements.length!==1)throw Error('한 번에 조회문 하나만 실행하세요.');
  if(!/^\s*(SELECT|WITH)\b/i.test(masked)||/\b(INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|PRAGMA|ATTACH|DETACH|VACUUM|REINDEX|ANALYZE|BEGIN|COMMIT|ROLLBACK|SAVEPOINT|RELEASE|LOAD_EXTENSION)\b/i.test(masked)||/\bREPLACE\b(?!\s*\()/i.test(masked))
    throw Error('읽기 전용 SELECT 조회만 사용할 수 있습니다.');
  db.run('PRAGMA query_only=ON');
  const statement=db.prepare(sql);
  try {
    const columns=statement.getColumnNames(), data=[];
    while(data.length<1001&&statement.step())data.push(statement.get());
    return {columns,rows:data.slice(0,1000),truncated:data.length>1000};
  } finally { statement.free(); }
}
async function handle({route,params:p,body,stage}) {
  await open(stage);
  if(route==='/api/meta')return {...rows('SELECT * FROM meta')[0],menu:Object.fromEntries(Object.entries(menus).map(([k,v])=>[k,v[0]])),keys:Object.fromEntries(Object.entries(menus).map(([k,v])=>[k,v[2]])),schema:rows("SELECT name,type,sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")};
  if(route==='/api/state')return {availableSources:rows('SELECT doc_id FROM source_document').map(r=>r.doc_id),approvals:rows('SELECT * FROM approval')};
  if(route==='/api/list')return listing(p);
  if(route==='/api/detail')return detail(p.menu,p.id);
  if(route==='/api/sql')return query(body.sql);
  throw Error('지원하지 않는 조회입니다.');
}
self.onmessage=({data})=>{queue=queue.then(async()=>{try{self.postMessage({id:data.id,result:await handle(data)});}catch(e){self.postMessage({id:data.id,error:e.message});}});};
