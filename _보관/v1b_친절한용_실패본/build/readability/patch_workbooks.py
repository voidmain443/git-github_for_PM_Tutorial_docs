import re,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__))
from xref_map import MAP
from wb_cards import CARDS
ROOT="/Users/voidmain443/Agent_base_codebase/Project_M_crash_course/교재/PM트랙"

def sec_titles(day):
    t={}
    for l in open(f"{ROOT}/Day{day}_교재.md",encoding='utf-8'):
        m=re.match(r'^## (\d+\.\d+) (.*)',l)
        if m:
            title=m.group(2).split(' — ')[0].strip()
            if len(title)>26: title=title[:25]+'…'
            t[m.group(1)]=title
    return t
TITLES={d:sec_titles(d) for d in range(1,5)}

def ref_str(day, refs):
    parts=[]
    for r in refs:
        if r.startswith('D'):
            dd=int(r[1]); num=r[3:]
            parts.append(f"Day{dd} 교재 {num}절({TITLES[dd].get(num,'')})")
        else:
            parts.append(f"{r}절({TITLES[day].get(r,'')})")
    return ' · '.join(parts)

LOOP = """> **■ 이 워크북을 따라가는 순서 — 모든 산출물 공통**
> 1. **읽는다.** X.1(왜 쓰는가) → X.2(표준 위치) → X.3(항목별 작성 가이드). 막히면 각 항목 아래 📖 표시가 가리키는 교재 절을 펼친다.
> 2. **찾는다.** X.3 끝의 **◆ 실습 입력 카드**에서 이 산출물에 쓰이는 사례 정본 §·앞 산출물·추가 조건을 확인한다. 카드에 없는 숫자는 만들어 내지 말고 "미확정"으로 적는다.
> 3. **쓴다.** 카드의 **★ 수업 중 과제**에 적힌 항목을 X.4 빈 템플릿(또는 인쇄용 PDF)에 온담 P1로 직접 쓴다. **이때 X.5 예시본은 아직 펼치지 않는다.**
> 4. **대조한다.** 다 쓴 뒤 X.5 완성 예시본과 칸별로 대조하고, X.6 해설에서 차이가 난 칸이 왜 그렇게 쓰였는지 읽는다. 예시본은 정답이 아니라 판단의 흔적이 보이는 한 예다.
> 5. **바꿔 쓴다.** X.7 실습(조건을 바꾼 변형 과제·자기 회사 과제)은 복습과 과정 후 과제다.
>
> 하루에 다섯 산출물을 이 순서로 다 하기에는 시간이 모자란다. 수업에서는 3단계를 산출물당 20~50분(카드의 ★에 적힌 시간)으로 하고, X.5·X.6은 그날 저녁에 읽는 것이 정상이다.
"""

def patch(day):
    p=f"{ROOT}/Day{day}_워크북.md"
    L=open(p,encoding='utf-8').read().split('\n')
    if any('■ 이 워크북을 따라가는 순서' in l for l in L):
        print(f"Day{day}: already patched"); return
    out=[]; cur_sec=None; i=0
    n_items=0; n_cards=0
    while i<len(L):
        l=L[i]
        m=re.match(r'^## ([0-7])\. ',l)
        if m: cur_sec=int(m.group(1))
        out.append(l)
        # (A) loop box after 0.1 heading
        if re.match(r'^### 0\.1 ',l):
            out.append(''); out.append(LOOP.rstrip('\n'))
        # (B) 📖 먼저 읽기 after X.1 heading
        m1=re.match(r'^### ([1-5])\.1 ',l)
        if m1 and cur_sec in MAP[day]:
            s=int(m1.group(1))
            cnt=collections.Counter(r for refs in MAP[day][s].values() for r in refs)
            top=[r for r,_ in cnt.most_common() if not r.startswith('D')][:3]
            chs=sorted({r.split('.')[0] for r in top})
            out.append('')
            out.append(f"> 📖 **먼저 읽기** — Day{day} 교재 제{'·'.join(chs)}장: {ref_str(day, top)}. 이 산출물의 개념·표준·온담 사례는 거기에 있고, 여기서는 칸을 채우는 법만 다룬다.")
        # (C) per-item 📖 line after '#### 항목 N.'
        m2=re.match(r'^#### 항목 (\d+)\.',l)
        if m2 and cur_sec in MAP[day]:
            n=int(m2.group(1)); refs=MAP[day][cur_sec].get(n)
            if refs:
                out.append(''); out.append(f"*📖 교재 {ref_str(day, refs)}*"); n_items+=1
        # (D) card before '### X.4 빈 템플릿'
        m3=re.match(r'^### ([1-5])\.4 ',L[i+1]) if i+1<len(L) else None
        if m3 and (day,int(m3.group(1))) in CARDS and l.strip()=='' :
            c=CARDS[(day,int(m3.group(1)))]
            # avoid double insert: check previous lines
            if not any('◆ 실습 입력 카드' in x for x in out[-40:]):
                box=["> **◆ 실습 입력 카드 — 이 산출물을 쓰기 위해 주어지는 것**",
                     ">",
                     f"> **사례 정본에서 찾는다** (`교재/공통/가상회사_온담F앤B.md`): {c['src']}",
                     ">",
                     f"> **앞 산출물에서 가져온다**: {c['prev']}",
                     ">",
                     "> **추가로 주어지는 조건** — 정본에 없는 값이다. 예시본은 이 값을 쓰며, 여러분도 그대로 쓴다:",]
                for e in c['extra']: box.append(f"> - {e}")
                box += [">", f"> **★ 수업 중 과제** — {c['task']}"]
                out.extend(box); out.append(''); n_cards+=1
        # (E) reminder after '### X.5 온담 P1 완성 예시본'
        m4=re.match(r'^### ([1-5])\.5 ',l)
        if m4 and cur_sec in MAP[day]:
            s=m4.group(1)
            out.append(''); out.append(f"> ■ **먼저 쓰고 나서 펼치라.** ★ 수업 중 과제의 항목을 §{s}.4에 직접 쓴 뒤 이 예시본과 칸별로 대조한다. 차이가 난 칸은 §{s}.6 해설에서 이유를 찾는다.")
        i+=1
    open(p,'w',encoding='utf-8').write('\n'.join(out))
    print(f"Day{day}: items tagged {n_items}, cards {n_cards}, lines {len(L)}→{len(out)}")

for d in range(1,5): patch(d)
