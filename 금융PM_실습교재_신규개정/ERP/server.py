#!/usr/bin/env python3
"""Local read-only training ERP. Python 3.10+, standard library only."""
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs,quote
import argparse,sqlite3,json,csv,io,time
BASE=Path(__file__).resolve().parent
STAGE_ORDER=['S0','S0A','S1','S1A','S2','S3','S4']
MENU={
 'documents':('원천 문서','source_document','doc_id'), 'people':('조직·담당자','person','person_id'),
 'requirements':('요구사항 추적','v_요구추적','요구번호'),'budget':('예산·기준선','v_예산조회','버전'),
 'cost':('프로젝트 원가','v_프로젝트원가','WBS'),'journal':('회계 전표','v_전표조회','전표번호'),
 'procurement':('구매·검수·지급','v_조달조회','발주번호'),'settlements':('가맹점 정산','v_정산조회','정산번호'),
 'reconciliation':('거래 대사','v_대사조회','거래번호'),'tests':('검증 결과','test_result','test_id'),
 'physical':('환경·물적자원','physical_resource','resource_id'),
 'allocations':('자원 배정','allocation','person_group'),'performance':('중간 성과측정','performance','posid')}
LINKS={'S01':'S01','S02':'S02'}
def connect(path):
 c=sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
 c.execute('PRAGMA query_only=ON')
 return c

def query(path,sql):
 with connect(path) as c:
  allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION,sqlite3.SQLITE_RECURSIVE}
  c.set_authorizer(lambda action,*args: sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY)
  deadline=time.monotonic()+2
  c.set_progress_handler(lambda: int(time.monotonic()>deadline),1000)
  cur=c.execute(sql); names=[d[0] for d in cur.description or []];rows=[list(r) for r in cur.fetchmany(1001)]
  return {'columns':names,'rows':rows[:1000],'truncated':len(rows)>1000}

def listing(path,key,params):
 if key not in MENU:raise ValueError('존재하지 않는 업무 메뉴')
 name,view,pk=MENU[key]
 with connect(path) as c:
  cols=[r[1] for r in c.execute(f'PRAGMA table_info("{view}")')]
  where=[];values=[]
  q=params.get('q',[''])[0].strip()
  if q:
   where.append('('+' OR '.join(f'CAST("{x}" AS TEXT) LIKE ?' for x in cols)+')'); values += ['%'+q+'%']*len(cols)
  for key,col in [('field','value'),('field2','value2')]:
   field=params.get(key,[''])[0];val=params.get(col,[''])[0]
   if field and val:
    if field not in cols:raise ValueError('잘못된 필터 항목')
    where.append(f'CAST("{field}" AS TEXT)=?');values.append(val)
  clause=' WHERE '+' AND '.join(where) if where else ''
  total=c.execute(f'SELECT count(*) FROM "{view}"'+clause,values).fetchone()[0]
  offset=max(0,int(params.get('offset',['0'])[0]));export=params.get('format',[''])[0]=='csv';limit=10000 if export else 50
  rows=[dict(r) for r in c.execute(f'SELECT * FROM "{view}"'+clause+f' ORDER BY "{pk}" LIMIT ? OFFSET ?',values+[limit,0 if export else offset])]
  sumcols=[x for x in cols if x in ['거래금액','취소금액','수수료','지급예정액','누적비용','계산액','수신액','차이','발주액','누적검수액','누적청구액','누적지급액']]
  summary={x:c.execute(f'SELECT coalesce(sum("{x}"),0) FROM "{view}"'+clause,values).fetchone()[0] for x in sumcols}
  return {'name':name,'columns':cols,'rows':rows,'total':total,'offset':offset,'summary':summary}

def related(path,key,value):
 with connect(path) as c:
  if key=='documents':
   d=c.execute('SELECT * FROM source_document WHERE doc_id=?',(value,)).fetchone()
   return {'document':dict(d) if d else None}
  if key=='procurement':
   return {'발주':[dict(r) for r in c.execute('SELECT * FROM purchase_order WHERE ebeln=?',(value,))], '검수':[dict(r) for r in c.execute('SELECT * FROM service_acceptance WHERE ebeln=?',(value,))], '청구':[dict(r) for r in c.execute('SELECT i.* FROM invoice i JOIN service_acceptance s USING(acceptance_id) WHERE ebeln=?',(value,))], '지급':[dict(r) for r in c.execute('SELECT p.* FROM payment p JOIN invoice i USING(invoice_id) JOIN service_acceptance s USING(acceptance_id) WHERE ebeln=?',(value,))]}
  if key=='reconciliation':return {'원천거래':[dict(r) for r in c.execute('SELECT * FROM payment_transaction WHERE tx_id=?',(value,))], '예외처리':[dict(r) for r in c.execute('SELECT * FROM exception_case WHERE tx_id=?',(value,))]}
  if key=='people':return {'담당자':[dict(r) for r in c.execute('SELECT * FROM person WHERE person_id=?',(value,))],'작성문서':[dict(r) for r in c.execute('SELECT doc_id,title,release_stage FROM source_document WHERE author_id=?',(value,))]}
  if key=='budget':return {'기준선':[dict(r) for r in c.execute('SELECT * FROM baseline WHERE version=?',(value,))],'월별비용계획':[dict(r) for r in c.execute('SELECT * FROM budget_line WHERE version=?',(value,))],'승인':[dict(r) for r in c.execute('SELECT a.* FROM approval a JOIN baseline b USING(approval_id) WHERE b.version=?',(value,))]}
  if key=='cost':return {'작업패키지':[dict(r) for r in c.execute('SELECT * FROM wbs WHERE posid=?',(value,))],'비용전표':[dict(r) for r in c.execute("SELECT * FROM acdoca WHERE posid=? AND saknr='610000'",(value,))]}
  if key=='settlements':return {'거래':[dict(r) for r in c.execute('SELECT * FROM payment_transaction WHERE batch_id=?',(value,))],'예외':[dict(r) for r in c.execute('SELECT e.* FROM exception_case e JOIN payment_transaction t USING(tx_id) WHERE batch_id=?',(value,))]}
  if key=='journal':return {'헤더':[dict(r) for r in c.execute('SELECT * FROM bkpf WHERE belnr=?',(value,))],'항목':[dict(r) for r in c.execute('SELECT * FROM acdoca WHERE belnr=?',(value,))]}
  if key=='requirements':return {'작업패키지':[dict(r) for r in c.execute('SELECT w.* FROM wbs w JOIN requirement_wbs l USING(posid) WHERE req_id=?',(value,))],'시험':[dict(r) for r in c.execute('SELECT * FROM test_result WHERE req_id=?',(value,))]}
  if key in MENU:
   _,view,pk=MENU[key]
   return {'기록':[dict(r) for r in c.execute(f'SELECT * FROM "{view}" WHERE "{pk}"=?',(value,))]}
 return {}

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def send(self,status,body,ctype='application/json; charset=utf-8'):
  if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False).encode()
  self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
 def do_GET(self):
  u=urlparse(self.path);p=parse_qs(u.query)
  try:
   if u.path=='/':return self.send(200,(BASE/'index.html').read_bytes(),'text/html; charset=utf-8')
   if u.path=='/learn':return self.send(200,(BASE/'learn.html').read_bytes(),'text/html; charset=utf-8')
   if u.path=='/guide':return self.send(200,(BASE/'guide.html').read_bytes(),'text/html; charset=utf-8')
   if u.path in ['/study-workspace.js','/study-workspace.css']:
    return self.send(200,(BASE/u.path[1:]).read_bytes(),'text/css; charset=utf-8' if u.path.endswith('.css') else 'text/javascript; charset=utf-8')
   if u.path=='/onboarding.js':return self.send(200,(BASE/'onboarding.js').read_bytes(),'text/javascript; charset=utf-8')
   if u.path=='/app.js':return self.send(200,(BASE/'app.js').read_bytes(),'text/javascript; charset=utf-8')
   if u.path=='/download':
    # Only learner template basenames are downloadable. No arbitrary paths or teacher files.
    name=p.get('name',[''])[0]
    allowed={f.name:f for f in (BASE.parent/'04_Level1_워크북/양식').glob('*.md')}
    if name not in allowed:return self.send(404,{'error':'제공하는 학습자 양식을 선택하세요.'})
    body=allowed[name].read_bytes()
    self.send_response(200);self.send_header('Content-Type','text/markdown; charset=utf-8')
    self.send_header('Content-Disposition',"attachment; filename*=UTF-8''"+quote(name))
    self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body);return
   if u.path=='/api/lesson':
    unit=int(p.get('unit',['0'])[0])
    if not 0<=unit<=9:raise ValueError('단원은 0~9입니다')
    lesson=json.loads((BASE/'lessons'/f'{unit:02}.json').read_text())
    with connect(self.server.db) as c:
     stage=c.execute('SELECT stage FROM meta').fetchone()[0]
     lesson['currentStage']=stage
     lesson['availableSources']=[r[0] for r in c.execute('SELECT doc_id FROM source_document')]
     lesson['approvals']=[dict(r) for r in c.execute('SELECT * FROM approval')]
    # Navigation remains visible. Future worked examples and answers are not sent.
    for i,step in enumerate(lesson.get('guideSteps',[])):
     if step['stage']>stage:
      lesson['guideSteps'][i]={k:step[k] for k in ['id','title','stage','processes']}
      lesson['guideSteps'][i]['locked']=True
    lesson.pop('readerHtml',None);lesson.pop('exercises',None)
    lesson['availableStages']=[s for s in STAGE_ORDER if (BASE/'data'/f'{s}.sqlite3').is_file()]
    return self.send(200,lesson)
   if u.path=='/api/meta':
    with connect(self.server.db) as c:
     meta=dict(c.execute('SELECT * FROM meta').fetchone());meta['menu']={k:v[0] for k,v in MENU.items()};meta['keys']={k:v[2] for k,v in MENU.items()};meta['schema']=[dict(r) for r in c.execute("SELECT name,type,sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")]
    return self.send(200,meta)
   if u.path=='/api/list':
    result=listing(self.server.db,p.get('menu',['documents'])[0],p)
    if p.get('format',[''])[0]=='csv':
     buf=io.StringIO();w=csv.writer(buf);w.writerow(result['columns']);w.writerows([[r[x] for x in result['columns']] for r in result['rows']]);return self.send(200,('\ufeff'+buf.getvalue()).encode(),'text/csv; charset=utf-8')
    return self.send(200,result)
   if u.path=='/api/detail':return self.send(200,related(self.server.db,p.get('menu',[''])[0],p.get('id',[''])[0]))
   return self.send(404,{'error':'찾을 수 없습니다'})
  except (ValueError,sqlite3.Error) as e:return self.send(400,{'error':str(e)})
 def do_POST(self):
  if self.path not in ['/api/sql','/api/stage']:return self.send(404,{'error':'찾을 수 없습니다'})
  # Local only, same-origin requests. No state-changing SQL accepted.
  if self.headers.get('Origin') and self.headers['Origin']!='http://'+self.headers.get('Host',''):return self.send(403,{'error':'다른 출처의 요청은 허용하지 않습니다'})
  try:
   size=int(self.headers.get('Content-Length','0'))
   if not 0<size<=16384:raise ValueError('쿼리는 16KB 이하여야 합니다')
   body=json.loads(self.rfile.read(size))
   if self.path=='/api/stage':
    stage=body.get('stage')
    if stage not in STAGE_ORDER:raise ValueError('자료 단계가 올바르지 않습니다')
    path=BASE/'data'/f'{stage}.sqlite3'
    if not path.is_file():return self.send(409,{'error':'해당 추가팩을 같은 폴더에 먼저 설치하세요.'})
    with connect(path) as c:
     if c.execute('SELECT stage FROM meta').fetchone()[0]!=stage:raise ValueError('자료팩의 시점이 일치하지 않습니다')
    self.server.db=path
    return self.send(200,{'stage':stage,'message':'선택한 자료를 열었습니다. ERP 탭도 새로고침하세요.'})
   return self.send(200,query(self.server.db,body.get('sql','')))
  except (ValueError,sqlite3.Error) as e:return self.send(400,{'error':str(e)})

def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['S0','S0A','S1','S1A','S2','S3','S4'],default='S0');p.add_argument('--port',type=int,default=8765);a=p.parse_args()
 db=BASE/'data'/f'{a.stage}.sqlite3'
 if not db.exists():p.error('이 배포팩에는 선택한 스냅샷이 없습니다. 해당 단계 추가팩을 받으세요.')
 srv=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);srv.db=db
 print(f'모아페이 ERP | {a.stage} | http://127.0.0.1:{a.port}',flush=True)
 try:srv.serve_forever()
 except KeyboardInterrupt:pass
 finally:srv.server_close()
if __name__=='__main__':main()
