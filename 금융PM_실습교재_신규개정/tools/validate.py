from build import ROOT,STAGES,PROCESSES,DOCS,write,table
import sqlite3,sys,math,re,json,hashlib,datetime,importlib.util
spec=importlib.util.spec_from_file_location('erp',ROOT/'ERP/server.py');erp=importlib.util.module_from_spec(spec);spec.loader.exec_module(erp)
checks=[]
def check(name,condition):
 checks.append((name,bool(condition)))
 if not condition:print('FAIL',name)
check('49 unique processes',len(PROCESSES)==len({p[0] for p in PROCESSES})==49)
expected={'4':7,'5':6,'6':6,'7':4,'8':3,'9':6,'10':3,'11':7,'12':3,'13':4}
for area,num in expected.items():check(f'knowledge area {area}',sum(p[0].split('.')[0]==area for p in PROCESSES)==num)
for group,num in [('착수',2),('계획',24),('실행',10),('감시통제',12),('종료',1)]:check(group+' process count',sum(p[2]==group for p in PROCESSES)==num)
for p in PROCESSES:
 check('inputs exist '+p[0],all(s in {d[0] for d in DOCS} for s in p[4].split()))
 check('concrete task/output '+p[0],len(p[6])>15 and bool(p[8]) and bool(p[7]))
for stage in STAGES:
 db=ROOT/'ERP/data'/f'{stage}.sqlite3';c=sqlite3.connect(db);c.row_factory=sqlite3.Row
 scalar=lambda q:c.execute(q).fetchone()[0]
 check(stage+' integrity',scalar('PRAGMA integrity_check')=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall())
 check(stage+' no future documents',scalar(f"SELECT COUNT(*) FROM source_document WHERE release_stage>'{stage}'")==0)
 check(stage+' balanced journals',not c.execute('SELECT belnr,gjahr FROM acdoca GROUP BY bukrs,belnr,gjahr HAVING sum(hsl)<>0').fetchall())
 bal={r[0]:r[1] for r in c.execute("SELECT a.saknr,sum(a.hsl) FROM acdoca a JOIN bkpf b USING(bukrs,belnr,gjahr) WHERE b.budat<='2026-09-30' GROUP BY a.saknr")}
 check(stage+' financial statements reconcile',bal['100000']==440000000 and bal['110000']==120000000 and bal['150000']==180000000 and -bal['400000']-sum(bal[x] for x in ['620000','630000','640000'])==40000000)
 check(stage+' 480 transactions',scalar('SELECT count(*) FROM payment_transaction')==480)
 check(stage+' 12 documented exceptions',scalar("SELECT count(*) FROM v_대사조회 WHERE 판정='불일치'")==scalar('SELECT count(*) FROM exception_case')==12)
 check(stage+' fee rules',scalar('SELECT count(*) FROM payment_transaction WHERE fee <> (gross-cancel)*200/10000 OR expected_net<>gross-cancel-fee')==0)
 check(stage+' fee sample provenance',scalar('SELECT sum(sample_fee) FROM settlement_revenue_bridge')==scalar('SELECT sum(fee) FROM payment_transaction'))
 check(stage+' settlement amount',scalar('SELECT sum(지급예정액) FROM v_정산조회')==scalar('SELECT sum(expected_net) FROM payment_transaction')+scalar('SELECT sum(adjustment) FROM settlement_batch'))
 check(stage+' no future approvals',scalar('SELECT count(*) FROM baseline')==(0 if stage<'S1A' else 1 if stage<'S3' else 2))
 if stage>='S2':
  cost=scalar('SELECT sum(누적비용) FROM v_프로젝트원가')
  check(stage+' project cost',cost==(115000000 if stage=='S4' else 58000000))
  po=dict(c.execute('SELECT * FROM v_조달조회').fetchone())
  check(stage+' procurement without fanout',po['발주액']==30000000 and po['누적검수액']==(30000000 if stage=='S4' else 20000000) and po['누적지급액']==(30000000 if stage=='S4' else 12000000))
  check(stage+' budget period totals',not c.execute('SELECT b.version FROM baseline b JOIN budget_line l USING(version) GROUP BY b.version HAVING sum(l.amount)<>b.bac').fetchall())
  ev=c.execute("SELECT sum(pv),sum(ev),sum(ac) FROM performance WHERE status_date='2026-11-30'").fetchone()
  check(stage+' EVM evidence',tuple(ev)==(60000000,50000000,58000000))
 if stage=='S4':
  check('all requirements tested',scalar('SELECT count(*) FROM requirement')==scalar('SELECT count(*) FROM test_result WHERE tested=passed AND critical_open=0')==6)
  check('all requirements traced',scalar('SELECT count(*) FROM requirement r WHERE NOT EXISTS(SELECT 1 FROM requirement_wbs l WHERE l.req_id=r.req_id)')==0)
  check('project vendor payable closed',scalar("SELECT sum(hsl) FROM acdoca WHERE saknr='200000' AND partner_id='V01'")==0)
 for key in erp.MENU:
  result=erp.listing(db,key,{})
  check(stage+' UI/SQL '+key,result['total']==scalar(f'SELECT count(*) FROM "{erp.MENU[key][1]}"'))
 for sql in ['DELETE FROM person',"ATTACH DATABASE ':memory:' AS x",'PRAGMA writable_schema=ON',"SELECT load_extension('nope')",'CREATE TABLE attack(x)','SELECT 1; SELECT 2']:
  try:erp.query(db,sql);blocked=False
  except sqlite3.Error:blocked=True
  check(stage+' SQL blocked '+sql.split()[0],blocked)
 try:erp.query(db,'WITH RECURSIVE t(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM t) SELECT sum(x) FROM t');blocked=False
 except sqlite3.Error:blocked=True
 check(stage+' runaway query timeout',blocked)
 c.close()
# Dependency references in student chapter markdown.
for f in (ROOT/'03_Level1_교재').glob('*.md'):
 links=re.findall(r'\]\(([^)]+)\)',f.read_text())
 check('links '+f.name,all((f.parent/x).exists() for x in links))
check('EMV scenarios',math.isclose(.7*.8+.3*.8+.7*.2+.3*.2,1) and math.isclose(.24*10+.14*20+.06*30,7))
d=datetime.date(2026,10,19);days=[]
while len(days)<60:
 if d.weekday()<5:days.append(d)
 d+=datetime.timedelta(days=1)
check('60 business-day CPM end',str(days[-1])=='2027-01-08')
check('4 developers enough for C',50/4<=15)
passed=sum(v for _,v in checks);report={'passed':passed,'total':len(checks),'checks':[{'name':n,'passed':v} for n,v in checks]}
write('검증/자동검증.json',json.dumps(report,ensure_ascii=False,indent=2))
write('검증/자동검증.md','# 자동검증 결과\n\n'+f'{passed}/{len(checks)} 통과. 이 결과는 데이터·프로세스 연결·조회 보호 검증이며 실제 교육효과 측정은 아니다.\n\n'+table(['검증','결과'],[(n,'PASS' if v else 'FAIL') for n,v in checks]))
print(f'{passed}/{len(checks)} checks passed')
if passed!=len(checks):sys.exit(1)
