"""One authored chapter per unit and a restrained, optional visual aid policy."""
from copy import deepcopy
import re
from onboarding import markdown_html

VISUALS = {
 0:('sources','workflow','정산 흐름에서 단계 사이에 넘기는 자료와 책임을 짚어 보고 싶을 때 사용합니다.'),
 1:('charter-10','charter','헌장 초안·역할별 검토·수정·승인의 책임이 헷갈릴 때 흐름을 확인합니다.'),
 2:('5.2','scope','요구 하나가 구현·시험 패키지에 어떻게 연결되는지 비교할 때 사용합니다.'),
 3:('6.5','schedule','병렬 활동의 합류 조건과 여유가 완료일에 미치는 영향을 예상한 뒤 확인합니다.'),
 4:('7.3','cost','비용을 인식하는 달과 현금을 지급하는 달이 다른 이유를 곡선으로 확인합니다.'),
 5:('11.4','risk','발생 확률과 예비비를 바꿨을 때 감당할 수 있는 손실 범위를 비교합니다.'),
 6:('12.2','procurement','업체 평가의 가중치와 선정 이후 계약·검수·지급 책임을 구분할 때 사용합니다.'),
 7:('9.3','integration','실행 기록에서 완료 증거가 있는 일과 추가 확인이 필요한 일을 구분합니다.'),
 8:('4.6','change','변경 대안을 비교할 때 원가·일정·자원 영향과 승인 상태를 함께 확인합니다.'),
 9:('5.5','closure','시험 통과·현업 인수·운영 이관·종료 승인의 서로 다른 책임을 확인합니다.'),
}
CONCEPT={'왜 확인하나요?','먼저 이해하기','이번 업무를 이해하기','개념을 한 단계 더 이해하기','가져올 문서와 현재 상태'}
EVIDENCE={'자료를 찾아 읽기','ERP 목록과 문서 연결하기','근거를 판단으로 바꾸는 과정','함께 따라 하는 예제','예제로 이해하기','화면에서 따라 하기','승인 자료를 읽기 전에','이번 단계의 순서'}

def reading_blocks(step):
    buckets={key:[] for key in ['concept','evidence','practice']}
    for title,body in step['sections']:
        key='concept' if title in CONCEPT else 'evidence' if title in EVIDENCE else 'practice'
        buckets[key].append('### '+title+'\n\n'+body)
    return {key:markdown_html('\n\n'.join(parts)) for key,parts in buckets.items()}

def attach_unit(lesson,unit):
    from unit_lessons_early import UNITS as early
    from unit_lessons_late import UNITS as late
    units={**early,**late}
    if set(units)!=set(range(10)):raise ValueError('Every Level 1 unit needs an authored chapter')
    guide=deepcopy(units[unit])
    assert len(guide['sections'])==6
    for section in guide['sections']:
        section['title']=re.sub(r'^\d+\.\s*','',section['title'])
        section['html']=markdown_html(section['body'])
    lesson['unitGuide']=guide
    ident,lab,purpose=VISUALS[unit]
    selected=next(step for step in lesson['guideSteps'] if step['id']==ident)
    lesson['visualAnchor']={'stepId':ident,'lab':lab,'title':selected['title'],'purpose':purpose}
    for step in lesson['guideSteps']:
        step['readingBlocks']=reading_blocks(step)
        step.pop('visualAid',None)
    selected['visualAid']={'lab':lab,'purpose':purpose}

def guide_markdown(guide):
    text='## 단원 본문: 업무를 차례로 이해하기\n\n'+guide['mission']+'\n\n'
    text+='가져올 것: '+' / '.join(guide['prerequisites'])+'\n\n'
    text+='마치면 할 수 있는 일: '+' / '.join(guide['outcomes'])+'\n\n'
    for i,section in enumerate(guide['sections'],1):
        text+=f"### {i}. {section['title']} ({section['stage']})\n\n"
        text+=('이 설명은 해당 자료 시점에서 공개됩니다.' if section.get('locked') else section['body'])+'\n\n'
    return text+'다음 업무: '+guide['handoff']+'\n\n'

def restrict_guide(guide,stage):
    for i,section in enumerate(guide.get('sections',[])):
        if section['stage']>stage:guide['sections'][i]={**{key:section[key] for key in ['id','title','stage']},'locked':True}
    return guide
