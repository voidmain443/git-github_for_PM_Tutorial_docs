# -*- coding: utf-8 -*-
"""DayN_슬라이드_body.tex(정본) → DayN_슬라이드.md(텍스트 미러) 변환. Day 번호는 입력 파일명에서 읽는다.
사용: python3 src/beamer2md.py Day1_슬라이드_body.tex Day1_슬라이드.md  (Day2도 같은 형식)
슬라이드별 제목·불릿·표·그림·핵심 메시지·강사 노트를 md로 옮긴다. 형식은 v1 md와 같다
('---' 구분, '## 제목', '> **강사 노트**: …'). md를 고쳐도 슬라이드는 바뀌지 않는다 — .tex를 고칠 것."""
import re, sys
DAY = 1

FIVE_DOCS_ASCII = """```
비즈니스 케이스 요약 ──(편익 118억·손익분기 66%·승인 조건 5)──▶ 헌장 §2 목적 / §3 성공 기준 / §14 중단 조건
        ▲                                                            │
        │ (분모 가정 A3 ← R-12)                                       │ (범위 경계·제외 범위·가정·제약)
        │                                                            ▼
프리모템·초기 리스크 ◀──(가정 1~6 → 리스크 원인)── 이해관계자 등록부 ◀──(누가 경계 안팎에 있는가)
        │                                                            │
        │ (소유자 실명, 즉시 조치)                                     │ (현저성 유형 → 의사결정체 배정, 관계 소유자)
        ▼                                                            ▼
헌장 §9·§10 수정 (v1.1) ◀────────────── 거버넌스·RACI ◀──────────────┘
                                          (A가 누구인가 → 리스크 소유자, 에스컬레이션 경로)
```"""

HEADERS = {
1: """# PM 트랙 Day 1 슬라이드 — 프로젝트 매니지먼트 일반론과 착수(Initiating)

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day1_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `./build.sh slides`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것(제목·불릿·표·그림·핵심 메시지 한 줄)과 `> **강사 노트**`(강사가 말할 것 — 교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day1_교재.md`)에 없는 내용은 없다. 슬라이드는 `---`로 구분한다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분 / 2교시 90분 / 점심 / 3교시 90분 / 4교시 90분(실습 ①) / 5교시 75분 / 6교시 75분(실습 ②) / 마무리 30분. 각 교시의 첫 슬라이드는 "이 교시에서 배우는 것", 마지막 슬라이드는 "핵심 정리"다. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
2: """# PM 트랙 Day 2 슬라이드 — 계획(Planning): 범위·일정·원가·리스크 기준선

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day2_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `sh src/build.sh 2`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것(제목·불릿·표·그림·핵심 메시지 한 줄)과 `> **강사 노트**`(강사가 말할 것 — 교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day2_교재.md`)와 워크북(`Day2_워크북.md`)에 없는 내용은 없다. 슬라이드는 `---`로 구분한다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분(계획론·범위와 요구사항) / 2교시 90분(일정) / 점심 / 3교시 90분(원가와 조달) / 4교시 90분(실습 ① 범위 기술서·WBS·RTM) / 5교시 75분(리스크) / 6교시 75분(실습 ② 일정·원가 기준선·리스크 등록부) / 마무리 30분. 각 교시의 첫 슬라이드는 "이 교시에서 배우는 것", 마지막 슬라이드는 "핵심 정리"다. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
3: """# PM 트랙 Day 3 슬라이드 — 실행과 통제(Executing · Monitoring & Controlling): EVM·변경·품질·이슈

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day3_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `sh src/build.sh 3`을 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것(제목·불릿·표·그림·핵심 메시지 한 줄)과 `> **강사 노트**`(강사가 말할 것 — 교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day3_교재.md`)와 워크북(`Day3_워크북.md`)에 없는 내용은 없다. 슬라이드는 `---`로 구분한다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분(통제론·성과 측정 EVM) / 2교시 90분(Earned Schedule·착시·흐름 지표·임계경로) / 점심 / 3교시 90분(변경 관리) / 4교시 90분(실습 ① 변경요청서·CCB + 성과보고 EVM 손계산) / 5교시 75분(품질·이슈·리스크·조달 통제) / 6교시 75분(실습 ② 이슈 로그·품질 기록·감리 대응·검수 보류 회신) / 마무리 30분. 각 교시의 첫 슬라이드는 "이 교시에서 배우는 것", 마지막 슬라이드는 "핵심 정리"다. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
4: """# PM 트랙 Day 4 슬라이드 — 전환과 종료(Transition · Closing): 컷오버·서비스 전환·종료·편익

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day4_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `sh src/build.sh 4`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것(제목·불릿·표·그림·핵심 메시지 한 줄)과 `> **강사 노트**`(강사가 말할 것 — 교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day4_교재.md`)와 워크북(`Day4_워크북.md`)에 없는 내용은 없다. 슬라이드는 `---`로 구분한다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분(전환·종료론과 컷오버) / 2교시 90분(서비스 전환: ITIL·SAC·SLA 세 층·error budget) / 점심 / 3교시 90분(종료: 보고서·계약 종결·미해결 이관) / 4교시 90분(실습 ① 컷오버 런북·SAC + 운영 이관·SLA 3층) / 5교시 75분(교훈과 편익) / 6교시 75분(실습 ② 종료 보고서·이관·교훈·편익 원장) / 마무리 30분(PM 트랙을 마치며·Product 트랙 예고). 각 교시의 첫 슬라이드는 "이 교시에서 배우는 것", 마지막 슬라이드는 "핵심 정리"다.
""",
5: """# Product 트랙 Day 5 슬라이드 — 프리시드 — 검사기록은 정말 문제인가

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day5_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `./build.sh slides Day5`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것과 `> **강사 노트**`(교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day5_교재.md`)와 워크북(`Day5_워크북.md`)에 없는 내용은 없다. 총 7개 블록(0교시 역할 전환 + 6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 0교시 20분(역할 전환·딥게이지 브리핑) / 1교시 80분 / 2교시 90분 / 점심 / 3교시 90분 / 4교시 90분(실습 ①) / 5교시 75분 / 6교시 75분(실습 ②) / 마무리 20분. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
6: """# Product 트랙 Day 6 슬라이드 — 시드 — 무엇을 안 만들 것인가, 얼마를 받을 것인가

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day6_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `./build.sh slides Day6`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것과 `> **강사 노트**`(교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day6_교재.md`)와 워크북(`Day6_워크북.md`)에 없는 내용은 없다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분 / 2교시 90분 / 점심 / 3교시 90분 / 4교시 90분(실습 ①) / 5교시 75분 / 6교시 75분(실습 ②) / 마무리 30분. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
7: """# Product 트랙 Day 7 슬라이드 — PMF 추적 — 곡선은 평탄해졌는가

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day7_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `./build.sh slides Day7`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것과 `> **강사 노트**`(교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day7_교재.md`)와 워크북(`Day7_워크북.md`)에 없는 내용은 없다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분 / 2교시 90분 / 점심 / 3교시 90분 / 4교시 90분(실습 ①) / 5교시 75분 / 6교시 75분(실습 ②) / 마무리 30분. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
""",
8: """# Product 트랙 Day 8 슬라이드 — 시리즈A와 첫 엔터프라이즈 — 제품 회사로 남을 수 있는가

> **이 문서의 위치** — 슬라이드의 정본(소스)은 `Day8_슬라이드_body.tex`(Beamer)이고, 이 md는 `src/beamer2md.py`가 거기서 만든 **텍스트 미러**다(검색·검토용). 슬라이드를 고치려면 .tex를 고치고 `./build.sh slides Day8`를 돌리면 이 md도 다시 생성된다. 각 슬라이드는 화면에 보이는 것과 `> **강사 노트**`(교재 절 번호 §, 워크북 절 번호, 예상 소요 분)로 되어 있다. 교재(`Day8_교재.md`)와 워크북(`Day8_워크북.md`)에 없는 내용은 없다. 총 7개 블록(6교시 + 마무리), 슬라이드 {n}장.
>
> **블록 구성** — 1교시 90분 / 2교시 90분 / 점심 / 3교시 90분 / 4교시 90분(실습 ①) / 5교시 75분 / 6교시 75분(실습 ②) / 마무리 30분. 실습 교시의 슬라이드는 "과제 지시 → 작성 요령 → 흔한 오류 → 예시본 참조" 순서다.
"""
}
def inline(t):
    t = t.strip()
    t = re.sub(r'\\ra\{\}|\\ra(?=\s|$)', '→', t)
    t = re.sub(r'\\til\{\}|\\til(?=\s|$)', '~', t)
    for _ in range(3):
        t = re.sub(r'\\textbf\{([^{}]*)\}', r'**\1**', t)
    t = t.replace(r'$\rightarrow$', '→').replace(r'$\leftarrow$', '←').replace(r'$\sim$', '~').replace('$-$', '−')
    t = t.replace(r'\&', '&').replace(r'\%', '%').replace(r'\#', '#').replace(r'\_', '_')
    t = t.replace(r'\relax', '').replace(r'\\', '')
    t = re.sub(r'\\(small|footnotesize|scriptsize|tiny|normalsize|centering|par|smallskip|vfill)\b', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def table_to_md(rows):
    cells = [[inline(c.replace('\x00', '\\&')) for c in r.replace('\\&', '\x00').split('&')] for r in rows]
    n = max(len(r) for r in cells)
    cells = [r + [''] * (n - len(r)) for r in cells]
    out = ['| ' + ' | '.join(cells[0]) + ' |', '|' + '---|' * n]
    for r in cells[1:]:
        out.append('| ' + ' | '.join(r) + ' |')
    return '\n'.join(out)

def convert(tex):
    out = []
    frames = 0
    i = 0
    lines = tex.split('\n')
    in_frame = False
    frame_title = ''
    enum = None            # None | counter
    table_rows = None
    table_buf = ''
    in_tikz = False
    while i < len(lines):
        ln = lines[i].rstrip()
        i += 1
        s = ln.strip()
        if not in_frame:
            m = re.match(r'\\section\{(.*)\}', s)
            if m:
                out.append('---\n# ' + inline(m.group(1)) + '\n')
                continue
            m = re.match(r'\\begin\{frame\}(?:\[[^\]]*\])?\{(.*)\}\s*$', s)
            if m:
                in_frame = True; frames += 1
                frame_title = inline(m.group(1))
                out.append('---\n## ' + frame_title)
                enum = None; table_rows = None; in_tikz = False
            continue
        # inside frame
        if s.startswith(r'\end{frame}'):
            in_frame = False; out.append(''); continue
        if in_tikz:
            if s.startswith(r'\end{tikzpicture}'):
                in_tikz = False; out.append(FIVE_DOCS_ASCII)
            continue
        if s.startswith(r'\begin{tikzpicture}'):
            in_tikz = True; continue
        if table_rows is not None:
            if s.startswith(r'\end{tbl}'):
                if table_buf.strip(): table_rows.append(table_buf)
                out.append(table_to_md(table_rows)); table_rows = None; table_buf = ''
                continue
            s = re.sub(r'\\(midrule|toprule|bottomrule)', '', s).strip()
            if not s: continue
            table_buf += ' ' + s
            while '\\\\' in table_buf:
                row, table_buf = table_buf.split('\\\\', 1)
                table_rows.append(row)
            continue
        if s.startswith(r'\begin{tbl}'):
            table_rows = []; table_buf = ''; continue
        m = re.match(r'\\note\{(.*)\}\s*$', s)
        if m:
            out.append('\n> **강사 노트**: ' + inline(m.group(1))); continue
        m = re.match(r'\\keymsg\{(.*)\}\s*$', s)
        if m:
            out.append('\n**' + inline(m.group(1)).replace('**', '') + '**'); continue
        m = re.match(r'\\figcap\{(.*)\}\s*$', s)
        if m:
            out.append('*' + inline(m.group(1)) + '*'); continue
        m = re.match(r'\\fig(?:\[[^\]]*\])?\{(.*)\}\s*$', s)
        if m:
            out.append('![' + m.group(1) + '](../그림/PM_Day' + str(DAY) + '/' + m.group(1) + '.png)'); continue
        m = re.match(r'\\subhead\{(.*)\}\s*$', s)
        if m:
            out.append('**' + inline(m.group(1)).replace('**', '') + '**'); continue
        if s.startswith(r'\begin{enumerate}'):
            enum = 0
            m = re.search(r'\\setcounter\{enumi\}\{(\d+)\}', s)
            if m: enum = int(m.group(1))
            continue
        if s.startswith(r'\end{enumerate}'):
            enum = None; continue
        if s.startswith(r'\item'):
            body = inline(s[5:])
            if enum is not None:
                enum += 1; out.append(f'{enum}. ' + body)
            else:
                out.append('- ' + body)
            continue
        if re.match(r'\\(begin|end)\{(itemize|columns|column|center)\}', s) or s.startswith('%') or s == '':
            continue
        # anything else: plain text
        t = inline(s)
        if t: out.append(t)
    return out, frames

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    m = re.search(r'Day(\d)', src)
    DAY = int(m.group(1)) if m else 1
    tex = open(src, encoding='utf-8').read()
    body, n = convert(tex)
    text = HEADERS[DAY].replace('{n}', str(n)) + '\n' + '\n'.join(body).rstrip() + '\n'
    text = re.sub(r'\n{3,}', '\n\n', text)
    open(dst, 'w', encoding='utf-8').write(text)
    print(f'{dst}: 슬라이드 {n}장')
