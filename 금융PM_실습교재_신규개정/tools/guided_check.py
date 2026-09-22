"""Check source boundaries and instructional links after authored course rebuild."""
from build import ROOT, STAGES, PROCESSES, DOCS, write, table
from guided_steps import STEPS
import sqlite3, json, re, datetime, math

checks=[]
def check(name, ok):
    checks.append((name,bool(ok)))
    if not ok: print('FAIL',name)

check('49 explicit writing and review activities', len(STEPS)==49 and set(STEPS)=={p[0] for p in PROCESSES})
for stage in STAGES:
    with sqlite3.connect(ROOT/f'ERP/data/{stage}.sqlite3') as c:
        present={r[0] for r in c.execute('SELECT doc_id FROM source_document')}
        check(stage+' exact source set',present=={d[0] for d in DOCS if d[2]<=stage})
        check(stage+' no future effective dates',c.execute('SELECT COUNT(*) FROM source_document WHERE effective_date>(SELECT as_of FROM meta)').fetchone()[0]==0)
        if stage in ('S0','S0A','S1','S1A'):
            check(stage+' no execution performance',c.execute('SELECT COUNT(*) FROM performance').fetchone()[0]==0)
            check(stage+' no future actual costs',c.execute("SELECT COUNT(*) FROM acdoca WHERE saknr='610000'").fetchone()[0]==0)
        if stage=='S0A':
            check('charter approval only',c.execute('SELECT approval_id FROM approval').fetchall()==[('AP00',)])
            check('charter gate has no detailed estimates','S06' not in present and 'S09' not in present)
        if stage=='S1A':
            check('plan approval before results','S09' in present and 'S10' not in present and 'S11' not in present)
        for ident in present:
            stage_doc=next(d[2] for d in DOCS if d[0]==ident)
            text=(ROOT/f'02_원천문서/{stage_doc}/{ident}.md').read_text()
            body=c.execute('SELECT body FROM source_document WHERE doc_id=?',(ident,)).fetchone()[0]
            check(stage+' file and ERP '+ident,body in text)
for f in (ROOT/'03_Level1_교재').glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
        if not link.startswith(('https:','http:','#')):check(f.name+' link '+link,(f.parent/link).exists())
seen=[]
for m in range(10):
    lesson=json.loads((ROOT/f'ERP/lessons/{m:02}.json').read_text())
    for ex in lesson['exercises']:
        seen.append(ex['id'])
        check('specific instructions '+ex['id'],len(ex['steps'])==3 and len(ex['review'])>20 and bool(ex['fields']))
        check('no model answers '+ex['id'],'answer' not in ex)
check('app covers each process once',len(seen)==len(set(seen))==49)
check('new source facts','S17' in {d[0] for d in DOCS} and 'S21' in {d[0] for d in DOCS})
check('cash/work cost bridge',8+44+28+30==110 and 8+52+48+12==120 and 110+10+12==132)
check('EVM forecasts',math.isclose(120/(50/58),139.2) and 58+(120-50)==128)
check('vendor scoring',90*.5+80*.3+80*.2==85 and 70*.5+70*.3+100*.2==76)
days=[];d=datetime.date(2027,2,1)
while len(days)<20:
    if d.weekday()<5:days.append(d)
    d+=datetime.timedelta(days=1)
check('benefit 20 business days',str(days[-1])=='2027-02-26')
report={'passed':sum(v for _,v in checks),'total':len(checks),'checks':[{'name':n,'passed':v} for n,v in checks]}
write('검증/학습흐름검증.json',json.dumps(report,ensure_ascii=False,indent=2))
write('검증/학습흐름검증.md','# 학습 흐름·입력 검증\n\n'+f"{report['passed']}/{report['total']} 통과. 실제 학생의 이해도 검증과 구분합니다.\n\n"+table(['확인','결과'],[(n,'PASS' if v else 'FAIL') for n,v in checks]))
assert all(v for _,v in checks)
print(f"Guided course checks: {report['passed']}/{report['total']}")
