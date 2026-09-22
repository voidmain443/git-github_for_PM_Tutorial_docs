from pathlib import Path
import csv,json,sqlite3,zipfile,shutil,datetime,html,sys
from content import PEOPLE,DOCS,PROCESSES
from case_revision import DATES
ROOT=Path(__file__).resolve().parents[1]
STAGES={'S0':('2026-10-06','착수 전'),'S0A':('2026-10-08','헌장 승인 회신'),'S1':('2026-10-15','계획 검토'),'S1A':('2026-10-19','통합 승인·킥오프'),'S2':('2026-12-01','실행·변경 검토'),'S3':('2026-12-04','변경 승인 후'),'S4':('2027-01-29','종료')}
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(x).replace('\n','<br>') for x in r)+' |' for r in rows)+'\n'
def csvwrite(path,headers,rows):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def create_db(stage):
 path=ROOT/'ERP/data'/f'{stage}.sqlite3';path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():path.unlink()
 c=sqlite3.connect(path);c.executescript((ROOT/'ERP/schema.sql').read_text())
 c.execute('INSERT INTO meta VALUES(?,?,?)',(stage,*STAGES[stage]))
 c.execute('INSERT INTO company VALUES(?,?,?)',('1000','모아페이','KRW'))
 for i,n in enumerate(['경영','PMO','운영','재무','개발','품질','보안','구매']):c.execute('INSERT INTO cost_center VALUES(?,?,?)',(f'CC{i+1:02}','1000',n))
 c.executemany('INSERT INTO person VALUES(?,?,?,?,?,?)',PEOPLE)
 c.executemany('INSERT INTO business_partner VALUES(?,?,?)',[('V01','가온시스템','공급사'),('V02','누리소프트','공급사')]+[(f'BP{i:03}',f'가맹점{i:02}','가맹점') for i in range(1,25)])
 c.execute('INSERT INTO project VALUES(?,?,?,?)',('MP-01','1000','가맹점 정산 확인·대사·예외처리 개선','P02'))
 visible=[d for d in DOCS if d[2]<=stage]
 c.executemany('INSERT INTO source_document VALUES(?,?,?,?,?,?,?,?,?)',[(d[0],d[1],d[2],d[3],d[4],d[5],'1.1',{'S01':'2026-10-05','S02':'2026-10-05','S03':'2026-10-06','S04':'2026-09-30','S05':'2026-10-05','S06':'2026-10-12','S07':'2026-10-13','S08':'2026-10-14','S09':'2026-10-19','S10':'2026-11-30','S11':'2026-12-01','S12':'2026-12-04','S13':'2027-01-29','S14':'2027-01-22','S15':'2027-01-29','S16':'2026-10-08',**DATES}[d[0]],d[6]) for d in visible])
 c.executemany('INSERT INTO document_link VALUES(?,?,?)',[(d[0],'project','MP-01') for d in visible])
 for i,title in enumerate(['정산 조회','자동 대사','예외 처리','권한·로그','운영 인수'],1):
  acceptance=['금액24/24일치','480/480정확 분류','12/12담당·기한·상태·사유','권한8/8·로그누락0','운영자3/3독립수행'][i-1]
  c.execute('INSERT INTO requirement VALUES(?,?,?,?,?)',(f'R0{i}',title,'P03' if i!=4 else 'P07',acceptance,'S03'))
 if stage>='S0A':
  c.execute('INSERT INTO approval VALUES(?,?,?,?,?)',('AP00','헌장 승인','P01','2026-10-08','S16'))
 if stage>='S1':
  c.execute('INSERT INTO physical_resource VALUES(?,?,?,?,?,?,?)',('QA-01','QA환경',1,1 if stage>='S2' else 0,'운영인계' if stage=='S4' else '사용가능' if stage>='S2' else '준비예정','P06','S10' if stage>='S2' else 'S06'))
  owners={1:'P05',2:'P05',3:'P09' if stage>='S1A' else None,4:'P06',5:'P03',6:'P05'}
  for i,n in enumerate(['요구·설계','조회','대사·예외','검증','전환·교육','안정화'],1):c.execute('INSERT INTO wbs VALUES(?,?,?,?)',(f'1.{i}','MP-01',n,owners[i]))
  c.executemany('INSERT INTO requirement_wbs VALUES(?,?)',[('R01','1.2'),('R02','1.3'),('R03','1.3'),('R04','1.2'),('R04','1.4'),('R05','1.5'),('R05','1.6')])
  c.executemany('INSERT INTO allocation VALUES(?,?,?,?,?)',[('요구팀','1.1',2,20,400000),('설계팀','1.1',3,24,500000),('조회개발','1.2',4,50,500000),('QA','1.4',3,30,500000),('운영지원','1.5',5,25,400000),('안정화','1.6',4,20,500000)])
 accounts=[('100000','현금','자산'),('110000','매출채권','자산'),('150000','유형자산','자산'),('200000','미지급금','부채'),('300000','자본','자본'),('400000','수수료매출','수익'),('610000','프로젝트비용','비용'),('620000','인건비','비용'),('630000','일반관리비','비용'),('640000','감가상각비','비용')]
 c.executemany('INSERT INTO account VALUES(?,?,?)',accounts)
 def journal(no,date,desc,source,lines):
  year=int(date[:4]);c.execute('INSERT INTO bkpf VALUES(?,?,?,?,?,?)',('1000',no,year,date,desc,source))
  for i,line in enumerate(lines,1):
   acc,amount,*extra=line; posid=extra[0] if extra else None;partner=extra[1] if len(extra)>1 else None
   c.execute('INSERT INTO acdoca VALUES(?,?,?,?,?,?,?,?,?,?)',('1000',no,year,i,'0L',acc,amount,'MP-01' if posid else None,posid,partner))
 journal('OPEN','2025-12-31','전기말 잔액','S04',[('100000',400000000),('110000',100000000),('150000',200000000),('200000',-200000000),('300000',-500000000)])
 journal('REV','2026-09-30','당기 수수료 매출','S04',[('110000',300000000),('400000',-300000000)])
 journal('COLL','2026-09-30','수수료 채권 회수','S04',[('100000',280000000),('110000',-280000000)])
 journal('OPEX','2026-09-30','인건비·관리비 지급','S04',[('620000',180000000),('630000',60000000),('100000',-240000000)])
 journal('DEP','2026-09-30','감가상각','S04',[('640000',20000000),('150000',-20000000)])
 if stage>='S1A':
  c.execute('INSERT INTO approval VALUES(?,?,?,?,?)',('AP01','최초 기준선','P01','2026-10-16','S09'))
  c.execute('INSERT INTO baseline VALUES(?,?,?,?,?,?,?)',('BL01','MP-01',120000000,12000000,'2027-01-22','AP01','이력' if stage>='S3' else '현행'))
  for month,amount in [('2026-10',8),('2026-11',52),('2026-12',48),('2027-01',12)]:c.execute('INSERT INTO budget_line VALUES(?,?,?)',('BL01',month,amount*1000000))
  c.execute('INSERT INTO contract VALUES(?,?,?,?,?,?)',('CT01','V01','MP-01',30000000,'R02/R03','S09'))
  c.execute('INSERT INTO purchase_request VALUES(?,?,?,?,?)',('PR01','1.3',30000000,'승인','S09'))
  c.execute('INSERT INTO purchase_order VALUES(?,?,?,?,?)',('PO01','PR01','CT01',30000000,'종결' if stage=='S4' else '진행'))
 if stage>='S2':
  c.execute('INSERT INTO service_acceptance VALUES(?,?,?,?,?,?)',('SA01','PO01','2026-11-30',20000000,'부분검수','S10'))
  journal('PJ01','2026-11-30','요구설계 비용','S10',[('610000',20000000,'1.1'),('100000',-20000000)])
  journal('PJ02','2026-11-30','조회개발 비용','S10',[('610000',18000000,'1.2'),('100000',-18000000)])
  journal('PJ03','2026-11-30','외주 부분검수 비용','S10',[('610000',20000000,'1.3','V01'),('200000',-20000000,None,'V01')])
  journal('PAY01','2026-11-30','외주 부분 지급','S10',[('200000',12000000,None,'V01'),('100000',-12000000)])
  c.execute('INSERT INTO invoice VALUES(?,?,?,?,?,?)',('IV01','SA01',20000000,'PJ03',2026,'1000'))
  c.execute('INSERT INTO payment VALUES(?,?,?,?,?,?,?)',('PY01','IV01',12000000,'2026-11-30','PAY01',2026,'1000'))
  c.executemany('INSERT INTO performance VALUES(?,?,?,?,?,?)',[(f'1.{i}','2026-11-30',pv*1000000,ev*1000000,ac*1000000,'S10') for i,pv,ev,ac in [(1,20,20,20),(2,20,15,18),(3,20,15,20)]])
 if stage>='S3':
  c.execute('INSERT INTO approval VALUES(?,?,?,?,?)',('AP02','CR01 변경','P01','2026-12-03','S12'))
  c.execute('INSERT INTO baseline VALUES(?,?,?,?,?,?,?)',('BL02','MP-01',128000000,12000000,'2027-01-29','AP02','현행'))
  c.execute('INSERT INTO wbs VALUES(?,?,?,?)',('1.7','MP-01','CSV 다운로드','P05'))
  c.execute('INSERT INTO requirement VALUES(?,?,?,?,?)',('R06','CSV 다운로드','P03','조회24/24일치·차단·로그3/3','S12'))
  c.execute('INSERT INTO requirement_wbs VALUES(?,?)',('R06','1.7'))
  for month,amount in [('2026-10',8),('2026-11',52),('2026-12',48),('2027-01',20)]:c.execute('INSERT INTO budget_line VALUES(?,?,?)',('BL02',month,amount*1000000))
 if stage=='S4':
  c.execute('INSERT INTO approval VALUES(?,?,?,?,?)',('AP03','프로젝트 종료','P01','2027-01-29','S21'))
  c.execute('INSERT INTO service_acceptance VALUES(?,?,?,?,?,?)',('SA02','PO01','2027-01-22',10000000,'최종잔여검수','S13'))
  journal('PJ04','2027-01-22','외주 최종 잔여비용','S13',[('610000',10000000,'1.3','V01'),('200000',-10000000,None,'V01')])
  c.execute('INSERT INTO invoice VALUES(?,?,?,?,?,?)',('IV02','SA02',10000000,'PJ04',2027,'1000'))
  for n,iv,amount in [('02','IV01',8000000),('03','IV02',10000000)]:
   journal('PAY'+n,'2027-01-25','외주 잔액 지급','S13',[('200000',amount,None,'V01'),('100000',-amount)])
   c.execute('INSERT INTO payment VALUES(?,?,?,?,?,?,?)',('PY'+n,iv,amount,'2027-01-25','PAY'+n,2027,'1000'))
  for i,amount in [(2,6),(4,14),(5,9),(6,10),(7,8)]:journal('FIN'+str(i),'2027-01-29','잔여 내부 작업비용','S13',[('610000',amount*1000000,f'1.{i}'),('100000',-amount*1000000)])
  for i,n in enumerate([24,480,12,8,3,24],1):c.execute('INSERT INTO test_result VALUES(?,?,?,?,?,?)',(f'T0{i}',f'R0{i}',n,n,0,'S13'))
 # Fixed historical anonymized sample. Exceptions are legitimate business cases, not missing case facts.
 for m in range(1,25):
  mid=f'M{m:03}';batch=f'ST{m:03}';c.execute('INSERT INTO merchant VALUES(?,?,?,?)',(mid,f'BP{m:03}',f'가맹점{m:02}',200))
  c.execute('INSERT INTO settlement_batch VALUES(?,?,?,?,?)',(batch,mid,'2026-09-30',-1000 if m==1 else 0,'표본'))
  for j in range(1,21):
   tx=f'TX{m:03}{j:03}';gross=10000+m*1000+j*100;cancel=gross if j==20 else 0;fee=(gross-cancel)*200//10000;net=gross-cancel-fee;delta=100 if m<=12 and j==1 else 0
   c.execute('INSERT INTO payment_transaction VALUES(?,?,?,?,?,?,?,?)',(tx,batch,'2026-09-29',gross,cancel,fee,net,net+delta))
   if delta:c.execute('INSERT INTO exception_case VALUES(?,?,?,?,?,?)',(f'EX{m:03}',tx,'P03','2026-10-02','분석완료','수신파일 수기 가산100원. 원천금액을 기준으로 대사 판정.'))
 c.execute("INSERT INTO settlement_revenue_bridge SELECT batch_id,'1000','REV',2026,SUM(fee) FROM payment_transaction GROUP BY batch_id")
 c.commit(); assert not c.execute('PRAGMA foreign_key_check').fetchall();c.close()

def docs():
 for d in DOCS:
  path=f'02_원천문서/{d[2]}/{d[0]}.md'
  write(path,f'# {d[0]} | {d[1]}\n\n공개: {d[2]} {STAGES[d[2]][1]} · 버전1.1 · 작성{d[3]} / 검토{d[4]} / 확인{d[5]}\n\n이 문서는 실습 입력이다. 사실의 확인자와 학습자가 작성할 산출물의 승인자를 혼동하지 않는다.\n\n'+d[6])
 write('01_회사자료/회사와_사람들.md','# 모아페이에 합류한 첫날\n\n'+DOCS[0][6]+'\n\n## 함께 일할 사람\n\n'+table(['ID','이름','역할','부서','권한·책임','관심'],PEOPLE)+'''\n## 조직과 질문 경로
대표 윤서진 아래 PMO 한지우, 운영 박다은, 재무 최민석, 개발 이현우, 품질 정유나, 보안 오수빈, 구매 강태훈이 있다. 배준호와 김소연은 외부 이해관계자다. ERP 인물검색에서 이름·부서·권한을 찾고, 원천문서의 작성자와 대조한다.
PM은 모든 문서의 원저자가 아니다. 사업 타당성은 스폰서, 회계전표는 재무, 기술 추정은 개발, 인수는 현업의 책임이다. PM은 근거를 모으고 관계자와 검토해 통합된 결정을 가능하게 한다.

첫 실습: S01에서 목적과 수단을 각각 밑줄 긋고 S02에서 승인권자를 찾는다. ‘정산을 빠르게 한다’는 목적에 측정 기준이 없으면 완료 여부를 판단할 수 없다. 60분/일과 측정기간4주를 함께 적어야 한다.
''')
 write('01_회사자료/재무제표_읽기.md','# 회사의 돈과 프로젝트의 돈\n\n'+DOCS[3][6]+'''\n## 직접 확인하기
1. ERP의 S0 전표조회에서 2026-09-30까지 계정별 잔액을 집계한다.
2. 자산 계정의 합계740백만원을 부채200백만원+기초자본500백만원+당기손익40백만원과 대조한다.
3. 현금계정의 당기 움직임 +40백만원을 손익과 비교한다. 이 사례에서는 감가상각20과 매출채권 증가20이 상쇄되므로 손익과 현금흐름이 우연히 같다.
4. 정산조회에 보이는 가맹점 지급예정액을 회사 수수료매출에 더하지 않는다. 표본 거래는 회계결산 전표와 별도의 학습 표본이므로 전체 회사 매출을 외삽하지 않는다.
''')
 write('01_회사자료/용어집.md','# 처음 만나는 PM 용어\n\n'+table(['용어','뜻','이 사례에서'],[
 ('헌장 / Charter','스폰서가 프로젝트의 존재·목표·PM 권한을 승인하는 문서','S01·S02로 D01 작성'),('기준선 / Baseline','변경통제를 거쳐야 바꿀 수 있는 승인된 비교기준','BL01과 BL02'),('ITTO','입력 / 도구·기법 / 출력','자료→판단 활동→사용할 결과'),('WBS','전체 범위를 산출물 중심으로 분해한 구조','1.1~1.6; 활동목록과 다름'),('인수 / Acceptance','고객·현업이 산출물을 받아들이는 결정','박다은 AT01'),('품질통제','산출물이 기준을 충족하는지 검사','정유나 테스트'),('리스크','불확실한 미래 사건','K01·K02'),('이슈','이미 발생해 처리가 필요한 문제','DF01'),('우발예비비','식별한 위험 대응을 위한 기준선 내 예산','10백만원'),('관리예비비','예측하지 못한 작업에 대비한 기준선 밖 예산','12백만원'),('PV / EV / AC','계획가치 / 획득가치 / 실제원가','60 / 50 / 58백만원'),('발주 / 비용 / 지급','약정 / 자원 소비 인식 / 현금 유출','30 / 20 / 12백만원 외주 중간시점'),('대사','서로 다른 자료의 같은 금액·건수를 비교','계산액과 수신액 비교'),('편익','프로젝트 결과의 사용으로 생기는 효과','종료 후 대사시간 감소 측정')]))
 for stage in STAGES:
  write(f'02_원천문서/{stage}/README.md',f'# {stage} {STAGES[stage][1]} 자료 공개\n\n'+ '\n'.join(f'- [{d[0]} {d[1]}]({d[0]}.md)' for d in DOCS if d[2]==stage)+f'\n\n누적 자료는 앞 단계 자료를 함께 사용한다. 대응 ERP: ERP/data/{stage}.sqlite3. 새 회차에서는 S0부터 시작한다.')

MODULES=['회사에 합류하기','프로젝트 착수','요구사항과 범위','일정과 자원','원가와 예산','품질과 리스크','조달과 협업','계획 통합과 실행','성과와 변경 통제','검수·이관·종료']
INTRO=[
 'PM은 프로젝트의 모든 전문지식을 대신 아는 사람이 아니다. 사실을 확인하고 담당자·승인권자를 연결하는 사람이다. 회사자료와 S01~S05를 읽고 ERP S0에서 사람·거래·전표를 찾아보자. 한 행의 금액이 전체 회사의 금액인지 표본인지 먼저 확인한다.',
 '헌장은 상세 계획보다 먼저 작성한다. 왜 시작하는지, 무엇을 성공으로 볼지, PM에게 어떤 권한이 있는지 정한다. 목표와 실행 수단을 구분하고 가정·제약을 기록한다. 스폰서의 사업제안은 입력이며 학습자가 대신 사업 승인 사실을 만들어서는 안 된다.',
 '요구사항은 이해관계자가 필요한 것, 범위는 프로젝트가 제공하기로 한 것, WBS는 그 범위를 빠뜨리지 않도록 나눈 구조다. 요구사항에 ID를 붙이고 수락기준과 WBS를 연결하면 이후 변경과 검수의 근거가 된다.',
 '일정표는 날짜를 나열한 표보다 먼저 작업 사이의 관계다. 기간과 공수를 구별하고 선행 작업·동시 인원·달력을 함께 확인한다. 한 경로가 길어지는 이유를 설명할 수 있어야 종료일을 협의할 수 있다.',
 '견적의 합계가 곧 승인 예산은 아니다. 작업비와 위험 대응비를 합쳐 원가 기준선을 만들고 관리예비비를 따로 둔다. 비용이 발생한 시점과 돈을 지급한 시점을 구분해야 실제원가를 정확히 비교할 수 있다.',
 '품질은 끝에서 검사하는 것만이 아니다. 요구사항과 테스트 연결을 미리 점검하는 절차도 품질관리다. 리스크는 현재 문제가 아니라 미래의 불확실성이다. 정량분석은 가정과 단위를 밝히고 숫자가 갖는 한계까지 설명한다.',
 '계약은 구매부서만의 문서가 아니다. PM은 납품 범위·일정·품질·인수 조건이 프로젝트 계획과 맞는지 확인한다. 평가 기준은 제안서를 보기 전에 정하고 사람마다 필요한 소통 내용과 참여방식을 구분한다.',
 '각 영역의 계획을 합친 것만으로 통합계획이 되지 않는다. 일정에 배정한 사람이 예산에도 반영되어 있는지, 인수기준을 테스트할 수 있는지 확인해야 한다. 이후 회의의 결정은 담당자·기한·증거가 있는 작업으로 전환한다.',
 '실적을 보고할 때 사실·해석·예측·요청을 분리한다. 과거의 비용 비효율이 앞으로도 계속될지에 따라 전망은 달라진다. 변경은 좋은 아이디어라도 승인되기 전까지 기존 기준선에 포함되지 않는다.',
 '테스트 통과는 검증이고 현업 서명은 인수다. 종료는 산출물·계약·기록·잔여책임이 정리되었음을 뜻한다. 사용 후 나타나는 편익은 운영 책임자가 계속 측정하도록 넘긴다.'
]
DOMAINS={'4':'거버넌스','5':'범위','6':'일정','7':'재무','8':'거버넌스·품질 원칙','9':'자원','10':'이해관계자','11':'리스크','12':'거버넌스·재무·자원','13':'이해관계자'}
def curriculum():
 rows=[]
 for p in PROCESSES:
  id,name,group,module,inputs,tech,task,answer,out,nxt,review=p
  stage=max(next(d[2] for d in DOCS if d[0]==s) for s in inputs.split())
  rows.append([id,name,group,module,inputs,tech,out,nxt,DOMAINS[id.split('.')[0]],stage])
 csvwrite('00_설계/49개_프로세스_추적표.csv',['6판ID','프로세스','그룹','단원','입력','기법','출력','후속','8판관점','공개단계'],rows)
 write('00_설계/49개_프로세스_추적표.md','# 프로세스와 실습 연결\n\n이는 PMI 원문 ITTO의 복제가 아니라 사례에 맞춰 선정한 학습용 연결표다. 49개 프로세스 모두 수행하지만 모든 도구를 강제로 사용하지 않는다.\n\n'+table(['ID','프로세스','그룹','단원','입력','기법','출력','후속','8판 관점','시점'],rows))
 allbook=[]; allwork=[]; allanswer=[]
 for m,title in enumerate(MODULES):
  book=f'# {m:02}. {title}\n\n{INTRO[m]}\n\n'
  work=f'# {m:02}. {title} - 실습 워크북\n\n담당 PM: __________ / 실습일: __________ / 사용 스냅샷: __________\n\n'
  ans=f'# {m:02}. {title} - 강사용 해설\n\n'
  if m==0:
   work+='회사자료를 읽고 다음을 작성한다.\n\n1. 스폰서·현업 인수자·재무책임자 이름과 각 권한.\n2. 회사 매출과 가맹점 거래원금의 차이.\n3. S0 ERP에서 대사 불일치 거래를 찾는 조건과 결과 건수.\n4. 원천문서 작성자와 산출물 승인자의 차이.\n\n작성: ____________________________________________________\n'
   ans+='윤서진/박다은/최민석. 회사 매출은 계약상 수수료이며 거래원금은 가맹점 귀속. 대사 불일치12건, 전체480건. 조회 SQL은 ERP/queries.sql 참조.\n'
  for p in [p for p in PROCESSES if p[3]==m]:
   id,name,group,module,inputs,tech,task,answer,out,nxt,review=p
   source_links=' · '.join(f'[{s}](../02_원천문서/{next(d[2] for d in DOCS if d[0]==s)}/{s}.md)' for s in inputs.split())
   book+=f'## {id} {name}\n\n**상황과 목적.** {task}\n\n**입력.** {source_links}. 먼저 해당 자료의 시점과 작성자를 확인한다. 이전에 작성한 {out}이 있으면 새 파일을 만들기 전에 변경할 항목을 표시한다.\n\n**도구·기법.** {tech}. 아래 순서로 수행한다.\n\n1. 원문에서 이번 판단에 필요한 사실·수치·권한을 추출하고 문서 ID를 적는다.\n2. {task}\n3. 사실과 자신의 제안을 분리하고 계산·비교·회의 기록을 남긴다.\n4. {review}에게 근거와 검토 요청을 함께 전달한다. 승인 대상이면 S02 절차를 적용한다.\n\n**출력과 사용처.** {out}을 작성·갱신하며 다음 활동 {nxt}에 인계한다. 입력자료·버전·결정 책임자가 없으면 다음 담당자가 결과를 신뢰할 수 없다.\n\n**8판에서 다시 보기.** {DOMAINS[id.split(".")[0]]} 관점에서 이 결과가 누구의 판단을 가능하게 하는지 한 문장으로 설명한다.\n\n'
   work+=f'## 실습 {id} | {name}\n\n입력: {inputs} / 수행기법: {tech} / 제출: {out}\n\n{task}\n\n'+table(['작성 항목','기록'],[['문서 ID / 버전 / 작성일',''],['사용한 원천자료 ID·문단·조회조건',''],['이전 산출물에서 가져온 항목',''],['분석·계산·회의의 실제 수행 흔적',''],['결과 및 판단 근거',''],['검토자 의견·수정사항',''],['승인 필요 여부·승인자·근거',''],['다음 사용처·담당자·갱신 시점','']])+ '\n자기 점검: 자료에 없는 사실을 만들지 않았는가? 기법의 수행 흔적이 있는가? 다음 담당자가 사용할 수 있는가?\n\n'
   ans+=f'## {id} {name}\n\n**기준 답안.** {answer}\n\n**근거.** {inputs}; 검토역할 {review}. **인계:** {out} → {nxt}.\n\n**채점.** 사실·계산 정확성4점, 기법 수행2점, 문서 연결2점, 권한·버전2점. 결론만 적고 계산/비교/회의 기록이 없으면 기법 점수0. 동일 근거를 사용한 다른 표현과 합리적인 추가 관리항목은 허용한다. 금액·날짜·승인권한을 근거 없이 바꾸는 것은 허용하지 않는다.\n\n'
  write(f'03_Level1_교재/{m:02}_{title}.md',book);write(f'04_Level1_워크북/{m:02}_{title}.md',work);write(f'05_강사용/{m:02}_{title}_해설.md',ans)
  allbook.append(book);allwork.append(work);allanswer.append(ans)
 # Combined sources for print are separate from split files.
 write('출판원고/Level1_교재.md','\n\n'.join(allbook));write('출판원고/Level1_워크북.md','\n\n'.join(allwork));write('출판원고/강사용_해설.md','\n\n'.join(allanswer))
 # Shared document templates by output, plus calculation-friendly CSV.
 for output in sorted(set(p[8] for p in PROCESSES)):
  related=[p for p in PROCESSES if p[8]==output]
  write(f'04_Level1_워크북/양식/{output.replace("·","_")}.md',f'# {output}\n\n프로젝트: MP-01 / 버전: ____ / 상태: 초안 / 작성자: ____ / 검토자: ____ / 승인자: ____\n\n'+table(['항목','작성 내용','근거 ID'],[['목적·대상','', ''],['입력·가정·제약','',''],['분석·기법 적용','',''],['결과·결정·관리기준','',''],['담당자·기한','',''],['검토·수정·승인','',''],['후속 사용처','','']])+ '\n## 이 문서에서 수행할 실습\n\n'+'\n'.join(f'- {p[0]}: {p[6]}' for p in related))
 write('05_강사용/운영과_평가.md','''# 강사 운영 안내

S0→S0A→S1→S1A→S2→S3→S4 순서로 자료를 공개한다. S0A는 헌장 수정 후 승인 조건을 대조하는 자료다. S1은 기준선 승인 전 계획 검토 자료다. 단원7 통합점검 후 S1A의 S09를 제공하고, 작업지시를 작성한 후 S2의 S10을 제공한다. CR01 영향분석을 제출한 후에만 S12를 공개한다. 종료 실습 전까지 S13을 공개하지 않는다.

폴더 전체에는 강사용 미래자료가 있으므로 학생에게 전체 폴더를 복사하지 않는다. 배포본/학습자_시작.zip과 단계별 추가팩을 사용한다. 개인 학습자는 각 단계를 완료한 뒤 스스로 다음 팩을 연다. ERP 서버는 시작할 때 지정한 한 스냅샷만 제공하며 화면에서 미래 단계로 전환할 수 없다.

49개 실습은 각10점, 총490점. 통과 기준은392점(80%) 이상이며 근거없는 승인·미승인 변경 구현·정산원금을 회사매출로 처리·원가 이중집계 오류는 수정 후 재제출한다. 속도보다 근거와 연결을 평가한다. 실제 초보 수강생 파일럿 전에는 시간 추정을 확정하지 않는다.

역할 진행: 강사는 입력문서 작성자의 발언을 읽고, 학습자가 검토를 요청하면 제공된 기준에 맞춰 회신한다. 임의의 숨은 조건을 추가하지 않는다. 팀 실습은 PM·현업·재무·개발/QA 역할을 돌아가며 수행하되 개인도49개 프로세스 기록을 제출한다.

피드백 순서: 근거 확인→계산/기법 확인→권한·버전 확인→문서 표현 개선. 모범답안은 표현의 유일한 정답이 아니다. 자료가 부족하면 수강생에게 지어내게 하지 말고 제작 결함으로 기록한다.

수행시간 기록: 실습ID/시작/종료/조회시간/작성시간/질문/막힌 입력/수정횟수를 기록한다. 전체 교재를 한번 수행한 뒤 휴식·피드백 시간을 별도로 더해 부트캠프 일정을 편성한다.
''')

if __name__=='__main__':
 for stage in STAGES:create_db(stage)
 docs();curriculum()
 print('Built 7 snapshots, source documents, curriculum, workbooks and answer guides.')
