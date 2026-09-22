"""Stage-specific student copies; future examples stay in later release packs."""
from pathlib import Path
import json,copy
from build import ROOT,STAGES,MODULES

def prepare():
    results={}
    for stage in STAGES:
        base=ROOT/'배포본/단계자료'/stage;book=[];work=[]
        def put(name,text):
            p=base/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p
        for m,title in enumerate(MODULES):
            lesson=json.loads((ROOT/f'ERP/lessons/{m:02}.json').read_text())
            content=f'# {m:02}. {title}\n\n현재 공개 자료: {stage}. 이후 단계는 목차만 표시합니다.\n\n'
            worksheet=f'# {m:02}. {title} - 수행 위치 기록\n\n문서 본문은 별도 양식에서 작성합니다. 이미 작성한 문서는 항목·버전으로 참조합니다.\n\n'
            for i,s in enumerate(lesson['guideSteps']):
                content+=f'## {i+1}. {s["title"]}\n\n자료 단계: {s["stage"]}\n\n'
                if s['stage']>stage:
                    lesson['guideSteps'][i]={k:s[k] for k in ['id','title','stage','processes']}
                    lesson['guideSteps'][i]['locked']=True
                    content+='이 단계의 설명과 예제는 해당 추가팩에서 공개됩니다.\n\n'
                else:
                    for h,b in s['sections']:content+='### '+h+'\n\n'+b+'\n\n'
                    content+='작성 양식: '+', '.join(s['downloads'])+'\n\n'
                    worksheet+=f'## {s["title"]}\n\n문서·항목·버전: ____ / 근거 위치: ____ / 검토·수정 위치: ____ / 다음 사용처: ____\n\n'
            # Original exercise bodies include later review prompts; keep only coverage IDs here.
            lesson['exercises']=[{k:e[k] for k in ['id','name','output','stage']} for e in lesson['exercises']]
            lesson['situation']='설명을 읽고 해당 자료 단계에서 원천자료를 확인합니다.'
            lesson['handoff']='각 단계의 인계 안내를 확인합니다.'
            put(f'ERP/lessons/{m:02}.json',json.dumps(lesson,ensure_ascii=False,indent=2))
            put(f'03_Level1_교재/{m:02}_{title}.md',content)
            put(f'04_Level1_워크북/{m:02}_{title}.md',worksheet)
            book.append(content);work.append(worksheet)
        put('교재_인쇄원고.md','\n\n'.join(book)+'\n\n'+(ROOT/'ERP/처음_사용하는_ERP.md').read_text())
        work.extend(p.read_text() for p in sorted((ROOT/'04_Level1_워크북/양식').glob('*.md')))
        put('워크북_인쇄원고.md','\n\n'.join(work))
        results[stage]=base
    return results

if __name__=='__main__':prepare()
