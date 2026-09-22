from build import *
from teaching import PREV

def finish():
 write('03_Level1_교재/표준을_읽는_방법.md','''# PMBOK 6판과 8판을 함께 읽는 방법

이 과정의 목적은 표준 암기가 아니라 프로젝트를 관리하는 행동을 익히는 것이다. 6판의 프로세스 구조로 작업을 빠짐없이 경험하고, 8판의 원칙과 성과영역으로 그 작업이 가치와 책임 있는 결과를 만드는지 살핀다.

| 비교 | 6판을 사용하는 방식 | 8판을 사용하는 방식 |
|---|---|---|
| 구성 | 10개 지식영역·5개 프로세스그룹·49개 프로세스 | 6개 원칙·7개 성과영역과 프로세스 지침 |
| 학습 질문 | 어떤 입력으로 어떤 기법을 적용해 무엇을 만드는가 | 그 활동이 가치·품질·책임 있는 성과에 어떻게 기여하는가 |
| 문서 | 헌장·계획·등록부·보고·변경기록의 연결 | 상황에 맞는 문서와 방법을 선택하고 효과를 검토 |
| Level1 적용 | 49개 프로세스의 실제 수행 흔적 남기기 | 각 문서의 사용자·의사결정·성과를 설명하기 |

6판의 지식영역은 통합·범위·일정·원가·품질·자원·의사소통·리스크·조달·이해관계자다. 5개 프로세스 그룹은 착수·계획·실행·감시통제·종료다. 프로세스 그룹은 프로젝트 단계를 뜻하지 않는다. 실행 중에도 계획을 반복하고 변경 영향을 통합한다.

8판의 성과영역은 거버넌스·범위·일정·재무·이해관계자·자원·리스크다. 여섯 원칙은 전체를 보는 관점, 가치 집중, 품질 내재화, 책임 있는 리더십, 지속가능성 통합, 권한을 갖춘 팀 구축으로 이해할 수 있다. 영역 이름에서 품질·소통·조달이 독립 항목으로 보이지 않아도 그 업무를 생략하지 않는다. 6판의 통합관리를8판의거버넌스로단순치환하지않고 각관리활동의연결과의사결정책임을 함께 본다.

이 과정은 예측형 계획과 승인 기준선을 중심으로 실습한다. 반복개발을 금지하는 뜻은 아니다. Level1에서 먼저 근거·변경·인수의 관계를 익힌 뒤 상위레벨에서 불확실성에 맞춰 방법을 조정한다. 모든 프로젝트에49개문서를 만들라고 요구하는 것도 아니다.

헌장의 예: 6판 관점에서는 사업제안·조직규정·이해관계자 의견을 입력으로 스폰서 면담과 분석을 거쳐 헌장을 작성한다. 8판 관점에서는 그 헌장이 실제로 가치 목표·의사결정권한·팀의 책임을 명확히 했는지 검토한다. 이것이 이 교재의 교육적 적용이며 공식 판본 간 일대일 대응표는 아니다.

## 확인한 1차 출처
- PMI 6판 과정 안내: https://www.pmi.org/events/ncpmi-summer-pmp-prep-class
- PMI Process Groups: A Practice Guide 공식서점: https://pmi.bookstore.ipgbook.com/process-groups--a-practice-guide-products-9781628257830.php
- PMI PMBOK Guide 8판 공식안내: https://www.pmi.org/standards/pmbok

기준일2026-09-17. 원문 표준의 전체 ITTO를 재인쇄하지 않고 이 가상사례에 필요한 입력·기법·결과를 독자적으로 설명한다.
''')
 rows=[]
 for p in PROCESSES:
  rows.append([p[0],p[1],p[2],p[3],p[4],PREV[p[0]],p[5],p[8],p[9],DOMAINS[p[0].split('.')[0]]])
 headers=['6판ID','프로세스','그룹','단원','원천입력','이전산출물','기법','출력','후속','8판관점']
 csvwrite('00_설계/49개_프로세스_추적표.csv',headers,rows)
 write('00_설계/49개_프로세스_추적표.md','# 49개 프로세스 추적표\n\n이전 산출물은 초안으로 시작해 관련 계획을 완성할 때 다시 대조한다. 원천 사실의 공개시점은02_원천문서 폴더를 따른다.\n\n'+table(headers,rows))
 p=ROOT/'01_회사자료/재무제표_읽기.md';text=p.read_text().split('\n## 재무제표 요약표')[0]
 text+='\n## 재무제표 요약표\n\n단위: 백만원. 손익과현금흐름 기간2026-01-01~09-30.\n\n'
 text+=table(['재무상태표','2025-12-31','2026-09-30'],[['현금',400,440],['매출채권',100,120],['유형자산',200,180],['자산합계',700,740],['부채',200,200],['자본(당기손익포함)',500,540],['부채+자본',700,740]])
 text+='\n'+table(['손익계산서','당기'],[['수수료매출',300],['인건비',180],['일반관리비',60],['감가상각비',20],['순이익',40]])
 text+='\n'+table(['현금흐름표','당기'],[['영업현금유입',280],['영업현금유출',-240],['순영업현금흐름',40],['투자현금흐름',0],['재무현금흐름',0],['기초현금',400],['기말현금',440]])
 p.write_text(text)
 # Include early orientation and standards once, then source-independent company appendices.
 book=(ROOT/'03_Level1_교재/표준을_읽는_방법.md').read_text()+'\n\n'
 book+='\n\n'.join((ROOT/f'03_Level1_교재/{m:02}_{title}.md').read_text() for m,title in enumerate(MODULES))
 book+='\n\n'+(ROOT/'03_Level1_교재/학습경로와_검토회신.md').read_text()+'\n# 회사자료 부록\n\n'+'\n\n'.join(p.read_text() for p in sorted((ROOT/'01_회사자료').glob('*.md')))
 write('출판원고/Level1_교재.md',book)
 # Append explicit finance linkage to the data dictionary.
 p=ROOT/'ERP/데이터사전_SAP대응.md';s=p.read_text();marker='\n## 금융 표본과 회계의 연결'
 p.write_text(s.split(marker)[0]+marker+'\n\nsettlement_revenue_bridge는 표본배치의 수수료가 REV집계전표에 포함되는 관계를 기록한다. 표본수수료를REV매출에다시더하지않는다. 가맹점원금·조정금은 프로젝트원가가 아니다. QA환경같은물적자원은 physical_resource에서 별도로조회하며 인력 갈등 관리와 구분한다.\n')
 # Actual row-level field dictionary from database DDL.
 c=sqlite3.connect(ROOT/'ERP/data/S4.sqlite3');fieldrows=[]
 for name, in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
  fks={r[3]:r[2]+'.'+(r[4] or 'PRIMARY KEY') for r in c.execute(f'PRAGMA foreign_key_list("{name}")')}
  for col in c.execute(f'PRAGMA table_info("{name}")'):
   fieldrows.append([name,col[1],col[2],'PK'+str(col[5]) if col[5] else '',fks.get(col[1],''),'금액은 원 단위 정수' if col[1] in ['hsl','bac','amount','gross','fee','cancel','expected_net','received_net','pv','ev','ac','management_reserve','sample_fee'] else 'schema.sql 및 SAP대응 문서 참조'])
 c.close();csvwrite('ERP/필드사전.csv',['테이블','필드','자료형','기본키순번','외래키대상','설명'],fieldrows)
 # Rebuild instructions specify all authoring steps, no hidden dependencies.
 p=ROOT/'README.md';s=p.read_text().replace('python3 tools/teaching.py\npython3 tools/validate.py','python3 tools/teaching.py\npython3 tools/finish_content.py\npython3 tools/validate.py');p.write_text(s)
if __name__=='__main__':finish();print('Finalized standards comparison, finance statements and field dictionary.')
