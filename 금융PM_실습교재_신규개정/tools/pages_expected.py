"""Oracle from the local Python ERP for browser SQLite compatibility checks."""
import sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'ERP'))
from server import listing,related,query,MENU,STAGE_ORDER
cases=[]
for stage in STAGE_ORDER:
    db=root/f'ERP/data/{stage}.sqlite3'
    for menu,(_,_,pk) in MENU.items():
        for params in [{},{'q':['P03']},{'offset':['50']}]:
            result=listing(db,menu,params)
            cases.append({'stage':stage,'route':'/api/list','params':{'menu':menu,**{k:v[0] for k,v in params.items()}},'expected':result})
        first=listing(db,menu,{})
        if first['rows']:
            value=str(first['rows'][0][pk])
            cases.append({'stage':stage,'route':'/api/detail','params':{'menu':menu,'id':value},'expected':related(db,menu,value)})
    for menu,field,value in [('reconciliation','판정','불일치'),('settlements','정산번호','ST001'),('budget','버전','BL01'),('procurement','발주번호','PO01'),('physical','resource_id','QA-01')]:
        params={'field':[field],'value':[value],'format':['csv']}
        cases.append({'stage':stage,'route':'/api/list','params':{'menu':menu,**{k:v[0] for k,v in params.items()}},'expected':listing(db,menu,params)})
    for sql in ['SELECT * FROM meta',"SELECT * FROM v_대사조회 WHERE 판정='불일치'",'SELECT * FROM v_예산조회',"SELECT SUM(pv) AS PV,SUM(ev) AS EV,SUM(ac) AS AC FROM performance WHERE status_date='2026-11-30'",'SELECT * FROM source_document WHERE 0','WITH n AS (SELECT 1 AS x) SELECT x FROM n',"SELECT ';--' AS literal",'SELECT a.tx_id FROM payment_transaction a CROSS JOIN payment_transaction b LIMIT 1002']:
        cases.append({'stage':stage,'route':'/api/sql','body':{'sql':sql},'expected':query(db,sql)})
print(json.dumps(cases,ensure_ascii=False))
