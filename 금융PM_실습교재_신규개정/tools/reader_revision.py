"""Canonical reading-first revision; invoked by guided_course before publishing."""
from pathlib import Path
from urllib.parse import urlencode
import json, re, datetime
from build import ROOT, MODULES, PROCESSES, DOCS, write, table
from teaching import PREV
from onboarding import markdown_html, STEPS as INTRO_STEPS, MANUAL
from reader_content import CONTENT, ORDER

DOC={d[0]:d for d in DOCS}
SOURCE_FOCUS={
'S01':'사업 필요, 현재값·목표값, 투자 한도와 최초 종료 목표',
'S02':'역할별 권한, 문서 검토·승인 및 변경 상정 절차',
'S03':'박다은·김소연·오수빈의 발언, R01~R05의 인수조건과 제외 범위',
'S04':'회사 재무의 기준일, 비용 인식과 지급의 차이',
'S05':'기존 정산 절차와 LL01~LL03의 교훈',
'S06':'A~G 기간·선행, WBS, 인력·단가, 월별 비용 배분',
'S07':'품질 기준, K01/K02 확률·영향·평가 규칙',
'S08':'업체 제안 점수·가중치, 회의·보고 주기와 참여 상태',
'S09':'AP01, 계약·발주와 킥오프 작업지시의 구분',
'S10':'11월 30일 PV/EV/AC, 시험·자원·참여·잔여 위험의 상태',
'S11':'CSV 요청의 이유, 세 대안의 비용·일정·자원 영향',
'S12':'AP02 승인 조건, 후속 작업·재시험·수신확인',
'S13':'최종 비용·검수·인수·종료 근거',
'S14':'운영 매뉴얼·복구 절차와 운영 책임',
'S15':'요구별 인수시험과 운영자 시연 증거',
'S16':'헌장의 수정 조건과 AP00 승인 기록',
'S17':'목표 측정 기간·담당, 기존 포털 경계, 자금·가정·종료 조건',
'S18':'패키지 인도물·담당과 T01~T05 시험 설계',
'S19':'지급·계약·보증 조건과 예방비용·예비비 운영',
'S20':'자원 배정, 교육·면담·작업·회의·점검의 원장',
'S21':'자원·보증·편익의 인계와 AP03 종료 결정'}

INPUT_FIX={'4.4':['S05','S10','S20'], '4.7':['S13','S01','S14','S17','S21']}
PREV_FIX={
'7.3':'D15 추정근거를 사용합니다. D25/D26은 5단원에서 작성하므로 지금은 S07/S19로 예비비 후보를 두고 위험 분석 후 이 표로 돌아옵니다.',
'4.4':'D03 작업기록과 앞 단계에서 작성한 D22 면담·교육 기록을 사용합니다.',
'10.2':'D23 소통계획과 D03 작업기록을 사용합니다. D05 보고 초안은 여기서 시작하고 8단원에서 지표·해석을 보완합니다.',
'4.5':'D02와 D14/D17, 7단원에서 시작한 D20/D25/D31 및 현재 점검 결과를 사용합니다.',
'8.3':'D18 품질계획, D19 절차점검과 7단원에서 시작한 D20 최초 결함 기록을 가져옵니다.',
'4.7':'앞 단계에서 완성한 D20 검사, D12 인수, D29 계약 대조와 D04 교훈·D06 변경 이력을 가져옵니다.'}

def template(code):
    return next((ROOT/'04_Level1_워크북/양식').glob(code+' *.md')).name

def source_url(s):return '/?'+urlencode({'menu':'documents','q':s})

# Menu, exact filter, fields to read, and destination in the student's document.
ERP_LOOKUPS={
 '13.1':('people','person_id','P03','조직·담당자','name은 이름, authority는 확인 권한, interest는 관심사입니다. P03의 권한을 D30에 옮기고, P04를 직접 찾아 비용 검토 역할을 추가합니다.'),
 '5.2':('requirements','요구번호','R01','요구사항 추적','요구사항·WBS·인수기준·원천문서를 읽습니다. 이것은 회사가 제공한 참조 연결이며 학생 문서의 승인이 아닙니다. S03 발언을 대조해 D08/D09의 요구와 확인 방법을 작성하고 R02를 직접 확인합니다.'),
 '9.2':('allocations','posid','1.2','자원 배정','headcount는 인원, person_days는 총 투입 인일, rate는 1인일 단가입니다. D21에 수량과 근거를 옮깁니다. 총 인일을 활동 기간으로 그대로 복사하지 말고 S06의 병행·가용 조건을 함께 읽습니다.'),
 '7.2':('allocations','posid','1.2','자원 배정','person_days × rate를 원 단위로 계산해 D15 추정근거에 남깁니다. ERP 자원 배정에 없는 외주·교육·운영이관 비용은 S06/S19에서 보완합니다. 조회된 인건비만을 전체 예산으로 쓰지 않습니다.'),
 '7.3':('budget',None,None,'예산·기준선','S1에서는 아직 승인 기준선이 없어 0건입니다. 0원 예산이라는 뜻이 아닙니다. S06/S07/S19로 D17 초안을 작성하고 7단원의 S1A 승인 후 BL01과 대조합니다.'),
 'plan-approval':('budget','버전','BL01','예산·기준선','BL01을 눌러 승인·월별비용계획을 엽니다. AP01과 금액·시점을 D02/D17 초안에 대조한 뒤 승인 버전을 보존합니다. PO01 발주가 실제 비용이나 지급을 뜻하지 않는 점도 구분합니다.'),
 '9.3':('physical','resource_id','QA-01','환경·물적자원','planned_qty는 계획 수량, allocated_qty는 배정 수량, status는 현재 상태, owner_id는 담당자입니다. S20의 확보 기록과 대조해 D21을 갱신합니다.'),
 '7.4':('performance','status_date','2026-11-30','중간 성과측정','각 WBS의 pv·ev·ac를 같은 기준일로 합산합니다. 금액은 원 단위입니다. D05의 PV/EV/AC와 편차·지수에 계산 근거를 남깁니다. 프로젝트 원가 메뉴의 누적비용과 대조하되 구매 지급액을 AC에 다시 더하지 않습니다.'),
 '9.6':('physical','resource_id','QA-01','환경·물적자원','계획·배정 수량, 상태, 책임자를 D21의 계획과 비교합니다. S10/S20의 점검 시점과 사용 가능 증거로 해석하며 인력 면담 기록과 구분합니다.'),
 'change-approved':('budget',None,None,'예산·기준선','BL01과 BL02를 각각 열어 원가 기준선·관리예비비·승인번호를 비교합니다. 두 버전을 모두 보존하고 D06 결정과 D17 새 버전을 연결합니다. 최신 기준선을 이전 실적으로 소급해 쓰지 않습니다.'),
 '8.3':('tests','test_id','T04','검증 결과','tested는 시험 수, passed는 통과 수, critical_open은 미해결 중대 결함 수입니다. req_id와 source_id로 요구·근거를 찾고 D20에 대조합니다. T02도 직접 확인하며 정확 분류와 모든 거래의 금액 일치를 혼동하지 않습니다.'),
 '5.5':('requirements','요구번호','R01','요구사항 추적','R01 상세에서 연결 WBS와 시험을 읽습니다. D09의 인수조건 및 S15 시연 결과를 대조해 D12에 현업의 인수 근거를 남깁니다. 시험 통과와 현업 인수는 별도 판단입니다.'),
 '12.3':('procurement','발주번호','PO01','구매·검수·지급','PO01을 눌러 발주·검수·청구·지급의 사건과 날짜를 차례로 읽습니다. 같은 계약의 여러 단계 금액을 더하지 않습니다. D29에서 CT01 금액과 누적 이행을 대조하고 S19/S21의 잔여 보증 책임을 인계합니다.'),
}

def add_erp_lookup(step):
    if step['id'] not in ERP_LOOKUPS:return
    menu,field,value,label,read=ERP_LOOKUPS[step['id']]
    params={'menu':menu}
    route=f'ERP에서 「{label}」 → 「초기화」'
    if field:
        params.update(field=field,value=value)
        route+=f' → 정확히 일치 항목 「{field}」 → 값 「{value}」'
    route+=' → 「조회」 순서로 진행합니다.'
    step.setdefault('links',[]).append((label+' 조회 연습','/?'+urlencode(params)))
    step['sections'].insert(3,['ERP 목록과 문서 연결하기',route+'\n\n'+read+'\n\n조회 결과가 다르면 현재 자료 단계와 남은 검색조건을 먼저 확인하세요. 원천 ERP는 읽기 전용이며 작성은 내려받은 문서에서 합니다.'])

def current_reader_text(text):
    replacements={
      '작성한 기록을 파일로 보관하려면 실습실의 「G00 메모 내려받기」와 상단 「학습 기록 내려받기」를 사용합니다.':'이 단계의 작성 양식에서 G00을 내려받아 자신의 작업 폴더에서 편집·보관하세요. 웹에는 별도로 작성하지 않습니다.',
      '모든 단계의 기록과 자기확인을 마친 뒤 「단원 확인·인계 기록 보관」을 누릅니다.':'검토한 문서와 근거를 자신의 작업 폴더에 보관한 뒤 「다음 단원」으로 이동합니다.',
    }
    for a,b in replacements.items():text=text.replace(a,b)
    return text

def sections_md(step):
    return '\n\n'.join('### '+h+'\n\n'+b for h,b in step['sections'])

def lookup_text(sources):
    return '\n\n'.join(f'{i}. ERP의 원천 문서 메뉴에서 초기화 → 검색어 {s} → 조회 → 목록의 {s} 상세를 엽니다. 읽을 부분: {SOURCE_FOCUS[s]}. 확인한 사실의 단위·날짜·담당자를 함께 읽습니다.' for i,s in enumerate(sources,1))+'\n\n찾지 못하면 현재 자료 단계와 이전 검색조건을 확인하세요. 파일로 읽을 때는 같은 ID의 원천 문서를 사용합니다. SQL은 선택 경로입니다.'

def generic_step(ex,unit):
    pid=ex['id'];title,explain,example,practice,correction=CONTENT[pid]
    stage=ex['stage'];sources=INPUT_FIX.get(pid,ex['inputs'])
    if unit==8:stage='S2';sources=[s for s in sources if DOC[s][2]<='S2']
    if pid=='4.2':stage='S1';sources=[s for s in sources if DOC[s][2]<='S1']
    if pid=='4.3':stage='S1A';sources=['S09','S02']
    if pid=='13.1':stage='S0'
    ex['inputs']=sources;ex['stage']=stage
    action_fixes={
     '4.2':['D02에 분야별 문서 버전과 소유자를 등록합니다.','요구→WBS→활동→비용→시험과 자원·계약을 대조해 불일치를 수정합니다.','수정한 분야 계획을 통합 상정하고 승인 대기로 둡니다. 다음 단계의 S1A에서 승인 조건을 대조합니다.'],
     '5.6':['기존 승인 요구와 S11의 요청을 비교합니다.','기존 결함 보완과 새 기능의 범위를 구분합니다.','요청 상태와 영향 문서를 남깁니다. 승인 후 연결은 이 단원 마지막 S3 단계에서 갱신합니다.'],
     '6.6':['D14의 기준선과 S10 실적을 비교합니다.','CR01 기간 영향의 기술 추정 근거를 S11에서 찾습니다.','기준선·실적·예측·변경 후보를 구분합니다. 승인 후 새 일정은 S3 단계에서 보관합니다.'],
     '10.3':['S20의 발송·수신·참석을 비교합니다.','결론·담당·기한 중심의 보고 형식과 미확인 후속을 정합니다.','현재 증거로 판단하고 다음 회신은 S3 단계에서 이력으로 추가합니다.'],
     '13.4':['목표 참여 상태와 S10의 관찰 근거를 비교합니다.','미확인을 반대로 단정하지 말고 확인할 행동을 정합니다.','현재 평가를 보존하고 S3 회신 수신 후 변화를 갱신합니다.']}
    ex['steps']=action_fixes.get(pid,ex['steps'])
    prev=PREV_FIX.get(pid,PREV[pid])
    if pid=='6.2':prev+=' D21은 뒤의 자원 단계에서 작성한 뒤 기간 계산에 사용합니다.'
    if pid=='9.2':prev='D11과 앞 단계에서 시작한 D14 활동 목록, D21 역할 계획을 사용합니다. 아직 날짜 계산 전입니다.'
    if pid=='9.1':prev='D01·D11과 현재 D14 활동 목록을 사용합니다. 먼저 책임을 정하고 다음 단계에서 수량을 산정합니다.'
    code=ex['output'].split()[0]
    return {'id':pid,'processes':[pid],'stage':stage,'title':title,'sources':sources,'downloads':[template(code)],'sections':[
      ['이번 업무를 이해하기',explain],['가져올 문서와 현재 상태',prev],
      ['자료를 찾아 읽기',lookup_text(sources)],['함께 따라 하는 예제',example],
      ['문서에 반영하기',f"{ex['output']} 양식을 사용합니다.\n\n"+'\n\n'.join(f'{i}. {x}' for i,x in enumerate(ex['steps'],1))],
      ['직접 확인해 보기',practice],['검토 의견으로 수정하기',correction+'\n\n검토 역할: '+ex['reviewer']+'. '+ex['review']+' 이미 충족한 경우 문장의 근거를 확인하면 됩니다. 오류를 일부러 만들 필요는 없습니다.'],
      ['다음 업무로 넘기기',f'{ex["output"]}의 현재 버전과 근거를 보존합니다. 이 문서를 다시 사용할 때 현재 상태가 초안·분야 검토·승인 중 무엇인지 확인합니다. 문서 본문은 한 번 작성하고 수행표에는 위치만 남깁니다.']], 'nextUse': ''}

# Each charter field gets a real reading step. Detailed approval belongs to S0A.
CHARTER=[
('오늘의 요청과 초안 상태 이해하기','S01 S02','문서 표지',
 '오늘은 사업을 시작할 이유와 PM 권한을 정리하는 날입니다. 프로젝트코드 MP-01, 작성자 한지우, 회사의 시나리오 날짜와 실제 학습일을 구분합니다. D01을 복사해 v0.1·초안으로 둡니다.',
 '표지는 내용을 읽는 사람이 어떤 사업의 어느 버전을 보는지 알게 합니다. 승인 전 문서에 승인일이나 AP00을 미리 적지 않습니다.',
 '원천 문서의 작성자를 학생 산출물의 승인자로 그대로 옮기지 않았는지 확인합니다.'),
('현재 문제를 사업을 시작할 이유로 연결하기','S01 S05','사업 필요',
 '현재 수작업 대조와 예외 추적 누락이 어떤 문제를 만드는지 읽습니다. 현상, 업무 영향, 개선 이유 순서로 두세 문장을 씁니다. 프로그램 이름보다 개선해야 할 업무를 먼저 설명합니다.',
 '“자료 대조에 시간이 걸린다 → 확인 업무와 예외 추적을 일관되게 관리할 필요가 있다 → 기존 거래자료를 사용하는 내부 도구 개선을 제안한다”처럼 연결합니다.',
 '“좋은 시스템 구축”이라는 표현만 있다면 현재 문제와 누구의 업무가 달라지는지 보완합니다.'),
('목표를 측정 가능한 문장으로 만들기','S01 S17','목표와 측정',
 CONTENT['4.1'][1],CONTENT['4.1'][2],
 '“60분으로 줄인다”만 있으면 박다은은 언제부터 얼마나 측정할지 알 수 없습니다. 측정 대상·기간·책임을 덧붙이고 미래 효과를 달성으로 쓰지 않습니다.'),
('상위 요구와 인수의 뜻 이해하기','S03','상위 요구와 인수',
 '헌장에는 제공할 핵심 기능과 받아들일 조건을 요약합니다. 활동별 시험 순서는 다음 계획에서 상세화합니다. 정산 계산 정확성과 대사 분류 정확성은 서로 다른 조건입니다.',
 '대사에서는 실제 금액 차이가 있어도 그것을 불일치로 정확히 찾아야 합니다. “모든 거래를 일치로 만든다”는 목표로 바꾸면 안 됩니다.',
 'R01~R05를 요약하되 상세 시험 결과나 아직 수행하지 않은 통과율을 기록하지 않습니다.'),
('포함하는 일과 제외하는 일의 경계 쓰기','S03 S17','포함·제외 경계',
 CONTENT['5.3'][1],CONTENT['5.3'][2],CONTENT['5.3'][4]),
('회사 현금과 프로젝트 자금 한도 구분하기','S01 S04 S17','자금과 예산 상태',
 '회사 현금은 회사 전체의 잔액이며 프로젝트에 쓸 권한과 다릅니다. 헌장에서는 자금 한도와 상세 계획이 아직 승인 전이라는 상태를 함께 씁니다.',
 '“회사 현금 440백만원”은 재무의 사실이고 “프로젝트 투자 한도 132백만원”은 이번 사업의 조건입니다. 같은 금액 표에 넣더라도 의미와 근거를 나눕니다.',
 CONTENT['4.1'][4]),
('지금 알 수 있는 주요 일정만 적기','S01','주요 일정',
 '착수 시점에는 종료 목표와 계획·구현·검증·이관의 순서를 설명합니다. 상세 A~G 날짜는 기술 추정과 자원 검토를 한 뒤 일정 단원에서 계산합니다.',
 'S01의 최초 종료 목표를 표시하고 상세 일정은 계획 수립 시 확정 예정이라고 적습니다. 이미 후속 단원을 읽었더라도 미래 기준선을 초안에 복사하지 않습니다.',
 '초안에 활동별 확정 날짜가 있다면 착수 당시의 근거가 있는지 확인하고 없는 날짜는 계획 수립 대상으로 돌립니다.'),
('PM이 결정할 일과 상정할 일 나누기','S02','PM 권한·상정 경로',
 'PM은 정보를 요청하고 작업을 배정하며 여러 계획을 맞춥니다. 기준선의 중요한 변경은 회사의 승인 경로를 따라야 합니다. 자신에게 없는 권한을 헌장에 추가할 수 없습니다.',
 '“PM은 변경 영향을 분석해 상정한다. 관련 역할의 검토 후 스폰서가 결정한다”라고 쓰면 업무 수행과 승인 책임이 나뉩니다.',
 '“PM은 일정을 자유롭게 변경할 수 있다”를 일상 작업 조정과 승인 기준선 변경으로 구분해 고칩니다.'),
('가정·제약·위험과 종료 책임 정리하기','S05 S17','가정·제약·초기위험 / 종료·편익 인계',
 '가정은 계획의 전제로 확인할 내용, 제약은 지켜야 할 경계, 위험은 아직 발생하지 않은 사건입니다. A01 가정 로그에서 확인 책임·시점·결과를 남깁니다. 종료 후에도 운영과 편익 책임은 이어집니다.',
 '기존 거래자료를 사용할 수 있다는 가정은 S17 회신으로 확인할 수 있습니다. 구체적인 인원·환경 확보일은 계획 단계에서 확인합니다. A01의 영향 문서에 일정·자원계획을 연결합니다.',
 '“개발 완료 시 종료”만 있다면 현업 인수·보안·운영절차·계약·잔여업무와 편익 측정 책임을 S17에서 찾아 보완합니다.'),
('역할별 검토를 받아 수정본 만들기','S01 S02 S03 S17','검토·승인 이력',
 'D01 v0.1과 D30/A01을 모아 검토합니다. 운영은 목표·인수, 재무는 한도·상태, 보안은 경계, QA는 검사 조건, 스폰서는 권한을 봅니다. 문장을 더 길게 만드는 대신 빠진 판단 조건을 보완합니다.',
 '목표에 기간이 빠졌다면 수정 이력에 “목표와 측정 / 기간 누락 → 종료 후 20영업일 추가 / S17 / 박다은 확인”으로 남깁니다. v0.1은 보존하고 v0.2는 승인 대기로 둡니다.',
 'RV01~RV06을 하나씩 대조합니다. 이미 충족했다면 근거 위치를 남기고 닫습니다. 브라우저 입력이나 형식적인 수정 횟수로 통과를 판단하지 않습니다.'),
]

def approval_step():
 return {'id':'charter-approval','processes':['4.1'],'stage':'S0A','title':'수정본을 승인 조건과 대조하고 다음 단원에 넘기기','sources':['S16','S17'], 'downloads':[template('D01'),template('A01'),template('D30')], 'sections':[
 ['승인 자료를 읽기 전에','D01 v0.2와 의견 처리 기록을 보존한 뒤 S0A 자료팩을 엽니다. 자료를 열었다는 사실만으로 학생 문서가 승인된 것은 아닙니다.'],
 ['자료를 찾아 읽기',lookup_text(['S16','S17'])],
 ['승인 조건 대조','목표·경계·자금 상태·권한·종료 및 편익 책임을 S16과 항목별로 비교합니다. 일치하면 D01 v1.0에 AP00·윤서진·2026-10-08을 교육용 승인 근거로 기록합니다. 다르면 해당 항목을 수정합니다.'],
 ['다음 업무로 넘기기','D01의 목적과 범위 경계는 D08~D11로, D30의 검토 역할은 참여·자원계획으로, A01의 미확인 항목은 계획 단계 확인으로 넘깁니다. 헌장 승인과 상세 범위·일정·원가 기준선 승인은 구분합니다.']]}

def extra_step(ident,title,stage,sources,processes,body,downloads):
 return {'id':ident,'title':title,'stage':stage,'sources':sources,'processes':processes,'downloads':[template(c) for c in downloads], 'sections':[['이번 단계의 순서',body],['자료를 찾아 읽기',lookup_text(sources)]]}

def update_templates():
    # Narrow tables keep calculations legible in both print and the browser.
    groups=[('활동 정의',['활동','WBS','담당 역할','인도물·완료 증거']),
      ('선행과 기간',['활동','기간_영업일','선행','추정 근거']),
      ('네트워크 계산: 0시점',['활동','ES','EF','LS','LF','총여유_일']),
      ('일차와 달력',['활동','시작_일차','종료_일차','시작일','종료일']),
      ('기준선·실적·예측 구분',['기준일','문서 버전','승인근거','실적·예측','변경 내용'])]
    text='# D14 활동·일정표\n\n프로젝트: ____ / 버전: ____ / 자료 단계: ____ / 상태: ____\n\n활동 정의와 선행은 3단원에서 시작합니다. 자원을 확인한 뒤 기간과 날짜를 계산합니다. 8단원에서는 이전 기준선을 보존하고 새 버전과 예측을 구분합니다.\n\n'
    for title,headers in groups:
        rows=[[a]+['']*(len(headers)-1) for a in 'ABCDEFG'] if '기준선' not in title else [['']*len(headers)]*3
        text+='## '+title+'\n\n'+table(headers,rows)+'\n'
    text+='시작 일차=ES+1, 종료 일차=EF입니다. 달력은 월~금이며 교육상 공휴일을 별도 제외하지 않습니다. 근거와 검토 의견은 같은 문서 끝에 남깁니다.\n'
    write('04_Level1_워크북/양식/D14 활동_일정표.md',text)
    from build import csvwrite
    headers=['활동','WBS','담당 역할','완료 증거','기간_영업일','선행','ES','EF','LS','LF','총여유_일','시작_일차','종료_일차','시작일','종료일','버전','승인근거']
    csvwrite('04_Level1_워크북/양식/D14 활동_일정표.csv',headers,[[a]+['']*(len(headers)-1) for a in 'ABCDEFG'])
    # Worked calculation trace is instructor-only; not inserted into blank forms.
    times=[(0,10,0,10),(10,20,10,20),(20,35,25,40),(20,40,20,40),(40,50,40,50),(50,55,50,55),(55,60,55,60)]
    days=[];day=datetime.date(2026,10,19)
    while len(days)<60:
        if day.weekday()<5:days.append(day.isoformat())
        day+=datetime.timedelta(days=1)
    p=ROOT/'05_강사용/완성문서/D14 활동_일정표.md'
    answer=p.read_text()+'\n## 전진·역진과 실제 날짜 대조\n\n'
    answer+=table(['활동','ES','EF','LS','LF','총여유'],[[a,*t,t[2]-t[0]] for a,t in zip('ABCDEFG',times)])
    answer+='\n'+table(['활동','시작일','종료일'],[[a,days[t[0]],days[t[1]-1]] for a,t in zip('ABCDEFG',times)])
    p.write_text(answer)
    additions={
      'D02':('계획 연결 대조',['요구·인수조건','WBS·활동','일정·비용','시험·책임','대조·수정 근거']),
      'D21':('자원 수량과 가용성',['활동·환경','필요 수량','배정 조건·기간','확약 근거','실제 상태·인계']),
      'D25':('대응과 실행 이력',['위험ID','트리거','조치·기한','책임','실행 증거·일자','잔여 평가 근거']),
      'D28':('契約 검토'.replace('契約','계약'),['조항','제안 조건','검토 의견','보완·합의','서명 상태·근거']),
      'D29':('잔여 책임 인계',['책임','기간·기한','담당·창구','인계 근거']),
      'D30':('역할별 확인 계획',['인물ID','내부·외부','영향력·판단근거','검토·승인 책임','확인할 내용·시점']),
      'D23':('보고·회의 본문과 수신 이력',['기준일·수신자','결론·영향','담당·기한','결정 요청','발송·수신 확인'])}
    for code,(title,headers) in additions.items():
        p=ROOT/'04_Level1_워크북/양식'/template(code)
        p.write_text(p.read_text()+'\n## '+title+'\n\n'+table(headers,[['']*len(headers)]*3))

def apply_revision():
    assert set(CONTENT)=={p[0] for p in PROCESSES}
    update_templates()
    # Align 0-unit and ERP instructions with the reading UI, at the source level.
    manual=MANUAL
    a=manual.index('실습실은');b=manual.index('## 2.')
    manual=manual[:a]+'''학습 안내 /learn에서는 설명·조회 경로·예제를 읽습니다. ERP 기본 화면 /에서는 회사 자료를 조회합니다. 「원천 ERP 열기」로 새 탭을 열고, 조회 후 안내 탭으로 돌아오세요. 웹페이지에 답을 입력할 필요는 없습니다.

문서를 직접 작성할 때는 해당 단계의 양식을 내려받아 자신의 작업 폴더에서 편집합니다. 원천 ERP는 바뀌지 않습니다. 문서 본문은 한 번 작성하고 워크북에는 사용한 문서·항목 위치만 남겨도 됩니다.

'''+manual[b:]
    manual=manual.replace('실습 기록이 안 보이면 같은 브라우저·주소·포트인지 확인하세요. 자동 저장은 현재 브라우저 주소에 연결됩니다. 다른 환경으로 옮길 때에는 JSON 기록을 내려받아 「기록 이어받기」로 불러옵니다. 내려받기와 CSV 내보내기는 각각 학습 기록과 ERP 조회 결과라는 서로 다른 파일입니다.',
      '읽던 위치는 이 브라우저에만 보존됩니다. 이전 버전에서 작성한 학습 기록은 삭제하지 않으며 「이전 작성 기록 내려받기」로 보관할 수 있습니다. 새 문서는 내려받은 양식에서 작성합니다. ERP의 CSV 내보내기는 조회 결과를 보관하는 별도 기능입니다.')
    manual+='\n## 10. 자료팩을 바꾸는 순서\n\n안내 목차는 어느 단원이든 볼 수 있습니다. 회사의 미래 자료와 그 결과를 쓰는 예제는 해당 자료팩을 열어야 표시됩니다. 먼저 현재 단계의 문서·검토를 마칩니다. 강사는 다음 팩을 공개하고, 개인 학습자는 완료 기준을 대조한 뒤 팩을 엽니다. 추가팩은 기존 폴더에 풀고 학습 안내 상단의 자료 단계에서 선택한 뒤 「선택한 자료 열기」를 누릅니다. 서버를 다시 시작하지 않아도 조회 시점이 바뀝니다. 아직 설치되지 않은 팩은 선택할 수 없습니다. 같은 서버를 쓰는 모든 탭에 적용되므로 ERP 탭도 새로고침합니다. 자료 열기는 문서 승인이나 학습 평가를 대신하지 않습니다.\n'
    write('ERP/처음_사용하는_ERP.md',manual)
    guide=(ROOT/'ERP/guide.html').read_text();guide=guide[:guide.index('</nav>')+6]+markdown_html(manual)+'</main></html>';write('ERP/guide.html',guide)
    overview=[];mapping=[];fieldmap=[];assess=[]
    for m in range(10):
        path=ROOT/f'ERP/lessons/{m:02}.json';lesson=json.loads(path.read_text())
        exercises={x['id']:x for x in lesson['exercises']};steps=[]
        if m==0:
            for s in INTRO_STEPS:
                sources=sorted(set(re.findall(r'\bS\d\d\b',str(s))))
                sources=[x for x in sources if x in DOC and DOC[x][2]=='S0']
                steps.append({'id':s['id'],'title':s['title'],'stage':'S0','processes':[], 'sources':sources,'downloads':['G00_업무파악_작성용초안.md','Q00_자료조회_작성용초안.md'],'links':s['links'], 'sections':[
                    ['왜 확인하나요?',s['why'].replace('0단원의 결과는 정식 사업 승인 문서가 아니라 PM의 업무 파악 메모 G00입니다.','필요하면 G00 메모를 활용할 수 있습니다.')],
                    ['먼저 이해하기',s['read']],['화면에서 따라 하기','\n\n'.join(f'{i}. {a}' for i,a in enumerate(s['actions'],1))],
                    ['예제로 이해하기',s['example'].replace('다음 칸의 업무 목적을 자신의 말로 적으세요.','업무 목적을 자신의 말로 설명해 보세요.')],
                    ['직접 확인해 보기',s['task']+' 문서로 연습하려면 별도 양식을 사용하세요. 웹 입력은 필요하지 않습니다.'],
                    ['다음 단계로 가기 전에',s['check']],['막혔을 때',s['help']]]})
        elif m==1:
            for i,(title,srcs,field,explain,example,review) in enumerate(CHARTER):
                if i==2:steps.append(generic_step(exercises['13.1'],m))
                steps.append({'id':f'charter-{i+1}','title':title,'stage':'S0','processes':['4.1'],'sources':srcs.split(),'downloads':[template('D01')]+([template('A01')] if i==8 else []),'sections':[
                 ['이번 업무를 이해하기',explain],['자료를 찾아 읽기',lookup_text(srcs.split())],['함께 따라 하는 예제',example],
                 ['문서에 반영하기','D01의 「'+field+'」 항목에 반영합니다. 사실에는 자료 ID와 읽은 부분을, 자신의 판단에는 판단 이유를 붙이세요. 필요한 경우 해당 양식을 내려받아 작성합니다.'],
                 ['검토와 수정',review],['다음 업무로 넘기기','작성한 항목은 D01 초안에 모읍니다. 다음 단계에서는 이 내용을 새로 만들지 않고 같은 버전에서 보완합니다.']]})
            steps.append(approval_step())
        else:
            for pid in ORDER[m]:
                if m==7 and pid=='4.3':steps.append(extra_step('plan-approval','계획 승인과 계약을 확인하고 킥오프 준비하기','S1A',['S09'],['4.2','12.2'],
                  'S1에서 통합 대조와 수정을 마친 뒤 S1A를 엽니다. AP01 조건과 분야 계획을 대조해 승인 버전을 보관합니다. CT01/PO01은 선정 권고와 다른 사건입니다. 기준선과 계약이 확인된 뒤 다음 단계에서 회의 결정을 작업지시로 바꿉니다. 예산·기준선 메뉴의 BL01 상세에서 승인과 월별 배분을 함께 확인하세요.',['D02','D28']))
                steps.append(generic_step(exercises[pid],m))
            if m==8:steps.append(extra_step('change-approved','승인 결과에 따라 문서와 후속 점검을 함께 갱신하기','S3',['S12'],['4.6','5.6','6.6','7.4','10.3','11.7','13.4'],
                'S2의 성과보고·대안 비교·권고안을 보존하고 S3를 엽니다. AP02의 승인 조건을 D06 결정란에 기록합니다. 승인된 R06을 WBS 1.7·시험 T06·작업 WO02와 연결하고 D09/D11/D14/D17/D18/D21/D23/D25/D31의 영향을 확인합니다. BL01은 보존하고 BL02를 새 버전으로 둡니다. 승인 원가기준선 128백만원과 관리예비비 12백만원, 종료 목표 1월 29일을 예측 EAC와 구분합니다. 기존 외주 CT01은 변경하지 않는 조건도 확인합니다. S12의 재시험·수신확인·참여 변화는 최초 기록을 덮어쓰지 않고 새 증거로 추가합니다.',['D06','D09','D11','D14','D17','D18','D21','D23','D25','D31']))
        for i,s in enumerate(steps):
            s['sections']=[[h,current_reader_text(b)] for h,b in s['sections']]
            add_erp_lookup(s)
            if i+1<len(steps):
                s['sections'].append(['다음에 이어 할 일',steps[i+1]['title']+' 단계로 이어집니다. 현재 작성한 문서의 항목·근거를 가져가세요. 자료 단계가 바뀌면 먼저 현재 기록을 보존합니다.'])
            else:s['sections'].append(['단원 마무리',lesson['handoff'] if m else '사람·정산·대사·세 가지 돈의 뜻을 설명할 수 있으면 1단원으로 갑니다. G00은 필요한 경우 사용하는 업무 파악 메모입니다.'])
            s['html']=markdown_html(sections_md(s))
            mapping.append([m,s['title'],s['stage'],','.join(s['processes']),' '.join(s['sources']),', '.join(s['downloads'])])
        lesson['guideSteps']=steps;lesson['exercises']=[exercises[k] for k in ORDER.get(m,[])];lesson.pop('onboarding',None)
        lesson['sources']=sorted(set(x for s in steps for x in s['sources']))
        lesson['sourceTitles']={sid:DOC[sid][1] for sid in lesson['sources']}
        lesson['downloads']=[{'name':n,'url':'/download?'+urlencode({'name':n})} for n in dict.fromkeys(n for s in steps for n in s['downloads'])]
        lesson['readerHtml']='';lesson['reading']='설명과 예제를 한 단계씩 읽고 ERP에서 확인합니다. 문서는 양식을 내려받아 별도로 작성합니다.'
        intro=f'# {m:02}. {MODULES[m]}\n\n{lesson["situation"]}\n\n'
        intro+='이 단원은 설명 → 자료 조회 → 예제 → 직접 확인 → 검토·수정 → 다음 업무 순서로 진행합니다. 웹 입력은 필요하지 않습니다. 문서를 작성할 때는 양식을 내려받고 같은 문서의 버전을 이어 갑니다.\n\n'
        intro+=table(['순서','할 일','필요 자료'],[[i+1,s['title'],s['stage']] for i,s in enumerate(steps)])
        book=intro
        for i,s in enumerate(steps):
            book+=f'\n## {i+1}. {s["title"]}\n\n자료 단계: {s["stage"]}. 관련 프로세스: '+(', '.join(s['processes']) or '사전 준비')+'.\n\n'
            book+=' · '.join(f'[{sid} {DOC[sid][1]}](../02_원천문서/{DOC[sid][2]}/{sid}.md)' for sid in s['sources'])+'\n\n'
            book+=sections_md(s)+'\n\n작성 양식: '+' · '.join(f'[{n}](../04_Level1_워크북/양식/{n})' for n in s['downloads'])+'\n'
        write(f'03_Level1_교재/{m:02}_{MODULES[m]}.md',book)
        path.write_text(json.dumps(lesson,ensure_ascii=False,indent=2))
        # No repeated copies of the same content across web, worksheet, and deliverable.
        work=f'# {m:02}. {MODULES[m]} - 문서 실습 안내\n\n교재의 단계별 설명을 읽은 뒤 실제 산출물을 작성합니다. 웹에 다시 입력하거나 이 워크북에 본문을 중복 복사할 필요는 없습니다.\n\n'
        for ex in lesson['exercises']:
            work+=f'## {CONTENT[ex["id"]][0]} ({ex["id"]})\n\n사용 문서: {ex["output"]}. 근거: '+', '.join(ex['inputs'])+'.\n\n'
            work+=f'확인할 수행: {CONTENT[ex["id"]][3]}\n\n검토: {CONTENT[ex["id"]][4]}\n\n'
        work+='## 수행 위치와 검토 기록\n\n'+table(['활동·단계','문서ID·항목·버전','근거·계산 위치','검토·수정 위치','다음 사용처'],[['']*5 for _ in range(max(3,len(lesson['exercises'])))])
        work+='\n핵심 사실·권한·시점이 틀렸다면 해당 문서를 수정합니다. 이미 충족했다면 근거를 확인합니다. 근거 자료가 부족하면 학생의 추측으로 메우지 않고 자료 결함으로 기록합니다.\n'
        write(f'04_Level1_워크북/{m:02}_{MODULES[m]}.md',work)
        overview.append([m,MODULES[m],lesson['stage'],len(steps),lesson['handoff'] if m else '자료의 주인·기간·단위를 설명하고 헌장에 사용할 자료를 찾는다.'])
        for ex in lesson['exercises']:
            assess.append([m,ex['id'],CONTENT[ex['id']][3],CONTENT[ex['id']][4],ex['output']])
    write('03_Level1_교재/학습경로와_검토회신.md','# 학생이 따라가는 순서\n\n웹은 읽기와 조회 안내, ERP는 회사의 원천자료, 문서 양식은 학생의 실제 산출물입니다. 기록을 중복 입력하지 않습니다. 각 단계에는 목적·찾는 방법·부분 예제·직접 수행·검토·다음 사용처가 있습니다. 전체 답안은 강사용에 둡니다.\n\n'+table(['단원','업무','시작 자료','안내 단계 수','다음에 넘길 것'],overview)+'\n자료 순서: S0 → S0A → S1 → S1A → S2 → S3 → S4. 자료팩은 각 검토를 마친 뒤 엽니다. 안내 목차는 자유롭게 볼 수 있지만 미래 자료의 예제는 공개 전 표시하지 않습니다. 3~4단원 초안은 5~6단원 검토 후 다시 갱신하고 7단원에서 통합 승인합니다. 실제 승인 대상과 담당자 확인 기록을 구분합니다.\n')
    write('00_설계/학생단계_원천자료_양식_연결.md','# 학생 단계·원천자료·양식 연결\n\n'+table(['단원','학생 행동','시점','프로세스','근거','양식'],mapping))
    write('05_강사용/단원별_핵심오류와_완료증거.md','# 수행별 완료 증거와 핵심 오류\n\n기존 공통 평가와 함께 사용합니다. 표현은 달라도 근거·계산·권한·시점이 일치하면 허용합니다. 실제 학생 검증은 아직 실시 전입니다.\n\n'+table(['단원','프로세스','독립 수행 증거','핵심 오류와 수정','확인 문서'],assess))
    write('05_강사용/입문자_파일럿_운영과_관찰지.md',PILOT)
    # Provenance index includes row-oriented charter fields and the assumptions log.
    for p in sorted((ROOT/'04_Level1_워크북/양식').glob('*.md')):
        if not re.match(r'[AD]\d\d ',p.name):continue
        code=p.name.split()[0];uses=[x for x in PROCESSES if x[8].startswith(code+' ')]
        srcs=sorted(set(s for x in uses for s in INPUT_FIX.get(x[0],x[4].split())))
        if code=='A01':srcs=['S01','S02','S05','S17'];uses=[x for x in PROCESSES if x[0]=='4.1']
        headers=[]
        lines=p.read_text().splitlines()
        for i,line in enumerate(lines[:-1]):
            if line.startswith('|') and lines[i+1].startswith('|---'):headers+=line.strip('|').split('|')
        for header in dict.fromkeys(h.strip() for h in headers):
            kind='학생 판단·문서 관리' if any(k in header for k in ['검토','수정','판정','버전','처리','후속','합의','해석','추정']) else '원천 사실 또는 이전 문서에서 확인'
            fieldmap.append([code,header,kind,' '.join(srcs),'/'.join(x[0] for x in uses),'단계 안내의 예제와 작성 지시를 대조; 승인·실적은 해당 공개 후만 작성'])
        if code=='D01':
            for _,source,field,*_ in CHARTER:
                fieldmap.append([code,field,'헌장 항목: 사실과 판단 구분',source,'4.1','헌장 해당 단계의 읽을 부분·예제·검토를 적용'])
            fieldmap.append([code,'사람과 문서 책임','사실: 역할·권한','S02 S03','13.1','D30에서 확인한 역할과 권한을 요약'])
    write('00_설계/양식_필드별_근거점검표.md','# 양식 필드별 근거 점검표\n\nD01~D31과 A01의 모든 표 열 및 헌장의 행별 작성 항목을 관련 원천·수행에 연결한 점검용 색인입니다. 한 항목에 여러 원천이 연결될 수 있으므로 학생 단계의 읽을 부분과 예제를 함께 사용합니다. 자동 추출은 모든 학생 해석의 타당성을 증명하지 않습니다.\n\n'+table(['문서','항목','작성 성격','관련 원천','수행','시점·점검'],fieldmap))
    write('README.md',README)

PILOT='''# 입문자 파일럿 운영과 관찰지

상태: 실제 수강생 검증 실시 전. 제작자·자동 수행을 수강생 실적으로 대체하지 않습니다.

먼저 0~1단원, 이어 2~4단원 연결, 마지막으로 전 과정을 진행합니다. 학생용 시작팩과 필요한 단계 추가팩만 제공합니다. 강사는 기존 자료를 가리킬 수 있지만 새 숫자·권한·사건을 즉흥적으로 추가하지 않습니다. 설명을 보충해야 했다면 어느 문장이 부족했는지 기록합니다.

1. 학생이 시작 위치와 자료를 찾는 과정을 관찰합니다.
2. 예제 다음의 다른 건을 직접 해석·작성하게 합니다.
3. 근거 위치와 계산, 검토 후 수정 이유를 학생이 설명하게 합니다.
4. 다음 문서에서 이전 결과를 실제 사용하는지 확인합니다.
5. 자료·양식 결함을 수정하고 같은 과제를 다시 수행합니다.

| 단계·학습자 코드 | 조회 시간 | 작성 시간 | 막힌 문장·자료·필드 | 학생 질문 | 강사 도움·추가 사실 | 수정·재수행 결과 |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

핵심 오류: 근거 없는 승인, 미승인 변경 구현, 정산금을 회사 매출로 처리, 비용 중복 집계, 계획과 실제 혼동. 이 오류는 해당 문서를 보완한 뒤 다시 확인합니다. 수행시간은 수업 편성에 쓰고 속도를 성취로 보지 않습니다. 수업 시간표는 관찰 뒤 결정합니다.
'''
README='''# 모아페이 금융 프로젝트 PM 교재

처음에는 학습 안내의 0단원에서 시작합니다. 웹은 설명과 ERP 조회 안내를 제공합니다. 문서는 해당 단계에서 양식을 내려받아 별도 작업 폴더에서 작성합니다. 웹 입력·제출은 요구하지 않습니다.

공개 웹 교재: https://voidmain443.github.io/git-github_for_PM_Tutorial_docs/

GitHub Pages에서는 설치 없이 교재·ERP·자료실을 사용합니다. 공개 배포 구조와 자동 검증 절차는 [GitHub Pages 운영 안내](README_GitHub_Pages.md)에 정리했습니다. 아래 실행 방법은 로컬 배포팩을 사용할 때만 필요합니다.

## 실행

Python 3.10 이상에서 이 폴더를 열고 실행합니다.

```sh
python3 ERP/server.py --stage S0 --port 8878
```

http://127.0.0.1:8878/learn?unit=0 을 엽니다. 종료는 Ctrl+C입니다. 회사 자료는 로컬 SQLite의 읽기 전용 조회로 제공하며 외부 계정·SAP 설치가 필요 없습니다. 실행 환경 문제가 있으면 README_실행환경.md를 확인합니다.

## 학생이 쓰는 자료

- 03_Level1_교재: 업무 이유·단계·조회·부분 예제·검토·인계.
- 04_Level1_워크북: 문서별 양식과 수행 위치 기록. 본문을 중복 작성하지 않습니다.
- ERP: 회사 원천자료와 첫 사용 안내 /guide.
- 01_회사자료·02_원천문서: 같은 사실을 파일로 읽는 경로.

## 자료팩 전환

S0 → S0A 헌장 승인 → S1 계획 → S1A 통합 승인·킥오프 → S2 실행·변경 분석 → S3 변경 승인 → S4 종료 순서입니다. 현재 문서 검토를 마친 뒤 다음 추가팩을 같은 폴더에 풉니다. 학습 안내 상단의 자료 단계를 선택하고 「선택한 자료 열기」를 누릅니다. 해당 자료팩이 설치된 경우에만 열 수 있습니다. 회사의 조회 시점이 모든 탭에서 함께 바뀌므로 ERP 탭을 새로고침하세요. 미래 자료를 미리 열어야 현재 실습이 완성되는 구조가 아닙니다.

## 제작·검증

기본 골격은 10단원·49개 프로세스·31개 문서 계열입니다. 상세 읽기 원고는 tools/reader_content.py와 tools/reader_revision.py에서 관리합니다. 생성된 본문만 직접 고치면 재생성 때 사라질 수 있습니다. 전체 재생성은 다음과 같습니다.

```sh
python3 tools/rebuild.py --pdf --package
```

05_강사용·00_설계·검증은 제작자용입니다. 학생에게 전체 폴더를 배포하지 않고 배포본/학습자_시작.zip과 추가팩을 사용합니다. 최신 확인 결과는 검증/현재_검증상태.md를 확인하세요. 실제 입문자 파일럿은 실시 전이며 강사 관찰지를 제공합니다. Level 2~4 상세 제작은 Level 1 검증 이후로 둡니다.
'''
