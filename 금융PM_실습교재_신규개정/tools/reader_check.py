"""Instruction-specific checks that counts of processes alone cannot establish."""
from build import ROOT,PROCESSES,DOCS,STAGES,write,table
from reader_content import CONTENT,ORDER
from stage_materials import prepare
from reader_revision import ERP_LOOKUPS
import json,re,sys
from urllib.parse import parse_qs,urlparse
sys.path.insert(0,str(ROOT/'ERP'))
from server import listing
checks=[]
def check(name,value):
 checks.append((name,bool(value)))
 if not value:print('FAIL',name)
docs={d[0]:d[2] for d in DOCS};covered=set();count=0
for unit in range(10):
 d=json.loads((ROOT/f'ERP/lessons/{unit:02}.json').read_text())
 check(f'unit {unit} conceptual introduction',len(d.get('chapterIntro',[]))==3)
 guide=d['unitGuide']
 check(f'unit {unit} complete chapter',len(guide['sections'])==6 and len({c['id'] for c in guide['sections']})==6 and all(c['body'] and c['html'] and c['stage'] in STAGES for c in guide['sections']))
 check(f'unit {unit} preparation and outcomes',len(guide['prerequisites'])==len(guide['outcomes'])==3 and bool(guide['mission']) and bool(guide['handoff']))
 check(f'unit {unit} optional visual once',sum(bool(s.get('visualAid')) for s in d['guideSteps'])==1)
 check(f'unit {unit} reading steps',bool(d['guideSteps']))
 for s in d['guideSteps']:
  q=s.get('selfCheck',{})
  check(f'{unit}/{s["id"]} reasoned self check',bool(q.get('question')) and len(q.get('options',[]))==3 and q.get('answer') in [0,1,2] and len(q.get('explanation',''))>30)
  check(f'{unit}/{s["id"]} three complete reading phases',set(s['readingBlocks'])=={'concept','evidence','practice'} and all(s['readingBlocks'].values()))
  count+=1;covered.update(s['processes'])
  check(f'{unit}/{s["id"]} source available',all(docs[x]<=s['stage'] for x in s['sources']))
  check(f'{unit}/{s["id"]} templates exist',all((ROOT/'04_Level1_워크북/양식'/n).exists() for n in s['downloads']))
  check(f'{unit}/{s["id"]} explanation present',len(s['html'])>180)
  check(f'{unit}/{s["id"]} no obsolete UI directions',not any(x in s['html'] for x in ['G00 메모 내려받기','단원 확인·인계 기록 보관','학습 기록 내려받기']))
  if s['id'] in ERP_LOOKUPS:
   menu,field,value,*_=ERP_LOOKUPS[s['id']]
   params={'field':[field],'value':[value]} if field else {}
   result=listing(ROOT/f'ERP/data/{s["stage"]}.sqlite3',menu,params)
   check(f'{unit}/{s["id"]} ERP lookup at correct stage',result['total']==0 if s['id']=='7.3' else result['total']>0)
check('49 processes covered',covered=={p[0] for p in PROCESSES}==set(CONTENT))
check('resources before duration',ORDER[3].index('9.2')<ORDER[3].index('6.4'))
check('quality acceptance contracts closure order',ORDER[9]==['8.3','5.5','12.3','4.7'])
d=json.loads((ROOT/'ERP/lessons/01.json').read_text())
check('assumption log discoverable',any(x['name']=='A01 가정 로그.md' for x in d['downloads']))
check('charter separate approval',d['guideSteps'][-1]['stage']=='S0A')
d=json.loads((ROOT/'ERP/lessons/09.json').read_text())
check('operating procedure source visible','S14' in d['sources'])
template=(ROOT/'04_Level1_워크북/양식/D14 활동_일정표.md').read_text()
check('schedule has real writing locations',all(x in template for x in ['WBS','담당 역할','완료 증거','ES','EF','LS','LF','시작일','종료일','승인근거']))
manual=(ROOT/'ERP/처음_사용하는_ERP.md').read_text()
check('manual matches no-entry reader','웹페이지에 답을 입력할 필요는 없습니다' in manual and '자신의 기록칸' not in manual)
for stage,base in prepare().items():
 for p in (base/'ERP/lessons').glob('*.json'):
  d=json.loads(p.read_text())
  for c in d['unitGuide']['sections']:
   check(stage+'/'+p.name+'/'+c['id']+' chapter release boundary',set(c)=={'id','title','stage','locked'} if c['stage']>stage else bool(c.get('html')) and bool(c.get('body')))
  for s in d['guideSteps']:
   check(stage+'/'+p.name+'/'+s['id']+' release boundary',('html' not in s and 'sections' not in s and 'selfCheck' not in s and 'readingBlocks' not in s) if s['stage']>stage else bool(s.get('html')))
report={'passed':sum(v for _,v in checks),'total':len(checks),'guide_steps':count,'processes':len(covered),'checks':[{'name':n,'passed':v} for n,v in checks]}
write('검증/읽기교재_연결검증.json',json.dumps(report,ensure_ascii=False,indent=2))
assert all(v for _,v in checks)
print(f'{report["passed"]}/{report["total"]} reader checks passed; {count} steps, {len(covered)} processes')
