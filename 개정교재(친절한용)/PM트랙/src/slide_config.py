# -*- coding: utf-8 -*-
"""
슬라이드별 렌더링 설정 (md2beamer.py가 읽음). 키 = md의 '## 제목' 원문.
  size        : 본문 글꼴 명령 (기본 \\small)
  figs        : [{file, mode, height, width, caption, break_after}]
                mode = 'top'(본문 앞) / 'code'(코드블록 자리에) / 'end'(본문 뒤) / 'besidetable'(첫 표 오른쪽)
  breaks      : 이 접두어로 시작하는 줄 앞에서 \\framebreak
  table_font  : 표 글꼴 명령 / table_split : 표를 n행씩 나눔 / table_widths : 열 폭 비율 리스트
  breakable   : False면 allowframebreaks 끄기
그림 파일은 ../그림/PM_Day1/<file>.pdf (00_그림목록.md 참조).
"""

FIVE_DOCS_TIKZ = r"""
\begin{center}
\begin{tikzpicture}[
  doc/.style={draw=mDarkTeal, rounded corners=2pt, fill=mDarkTeal!6, align=center,
              font=\scriptsize\bfseries, inner sep=4pt, minimum height=8mm, text width=36mm},
  lab/.style={font=\tiny, text=black!75, align=center, inner sep=1pt},
  arr/.style={-{Stealth[length=2mm]}, thick, draw=mDarkTeal}, x=1mm, y=1mm]
\node[doc] (bc)   at (0,0)    {비즈니스 케이스 요약};
\node[doc] (ch)   at (95,0)   {헌장 §2 목적 / §3 성공 기준\\/ §14 중단 조건};
\node[doc] (pm)   at (0,-24)  {프리모템·초기 리스크};
\node[doc] (sr)   at (95,-24) {이해관계자 등록부};
\node[doc] (ch2)  at (0,-48)  {헌장 §9·§10 수정 (v1.1)};
\node[doc] (raci) at (95,-48) {거버넌스·RACI};
\draw[arr] (bc) -- node[lab, above] {편익 118억·손익분기 66\%·승인 조건 5} (ch);
\draw[arr] (ch) -- node[lab, left, text width=34mm] {범위 경계·제외 범위·가정·제약} (sr);
\draw[arr] (sr) -- node[lab, above] {누가 경계 안팎에 있는가 / 가정 1$\sim$6 $\rightarrow$ 리스크 원인} (pm);
\draw[arr] (pm) -- node[lab, right, text width=30mm] {분모 가정 A3 $\leftarrow$ R-12} (bc);
\draw[arr] (pm) -- node[lab, right, text width=30mm] {소유자 실명, 즉시 조치} (ch2);
\draw[arr] (sr) -- node[lab, left, text width=34mm] {현저성 유형 $\rightarrow$ 의사결정체 배정, 관계 소유자} (raci);
\draw[arr] (raci) -- node[lab, below] {A가 누구인가 $\rightarrow$ 리스크 소유자, 에스컬레이션 경로} (ch2);
\end{tikzpicture}
\end{center}
"""

G = '그림 '
CONFIG = {
    # ---------------- 1교시
    '온담으로 읽기 — ONE ONDAM은 프로그램이다': {
        'figs': [{'file': 'fig_1_1_hierarchy', 'mode': 'top',
                  'caption': G + '1-1. 포트폴리오·프로그램·프로젝트·운영의 관계와 MSP 가치 사슬'}]},
    '프로젝트는 왜 실패하는가 — "성공률 30%"를 믿으면 안 되는 이유': {
        'figs': [{'file': 'fig_1_2_chaos_bias', 'mode': 'top',
                  'caption': G + '1-2. CHAOS 성공 정의의 결함 — 6% / 94% / 70%'}]},
    'Flyvbjerg — 다른 데이터, 다른 결론': {
        'figs': [{'file': ['fig_1_2_flyvbjerg_multiply', 'fig_1_2_rcf'], 'mode': 'top',
                  'caption': G + '1-3. iron law와 세 차원의 곱셈 구조 / ' + G + '1-4. RCF 3단계와 앵커링'}]},
    '성공의 두 정의 — Cooke-Davies (2002)': {
        'figs': [{'file': 'fig_1_2_cooke_davies', 'mode': 'top',
                  'caption': G + '1-6. Cooke-Davies 성공 세 정의와 2×2 조합 (스마트오더 위치)'}]},
    '프로젝트를 임시조직으로 본다는 것 — Lundin & Söderholm (1995)': {
        'figs': [{'file': 'fig_1_3_temporary_org', 'mode': 'end', 'height': 0.8,
                  'caption': G + '1-7. 임시조직 이론 — 4T·4 행위 개념·실무 현상'}]},
    '온담 P1을 NTCP로 진단하면 — "표준 SI 프로젝트"가 아니다': {
        'figs': [{'file': 'fig_1_4_ntcp', 'mode': 'top',
                  'caption': G + '1-8. NTCP 다이아몬드 — 온담 P1의 위치 (3/4/3/4)'}]},
    '분야별 대조 — 같은 단어, 다른 리듬, 다른 되돌림 비용': {
        'table_font': r'\scriptsize',
        'figs': [{'file': 'fig_1_5_reversal_cost', 'mode': 'top',
                  'caption': G + '1-9. 분야별 되돌림 비용 시간축 대조 (SI·EPC·NPD·제약)'}]},
    # ---------------- 2교시
    '왜 계보를 알아야 하는가 — PMBOK은 참고서인데': {
        'figs': [{'file': 'fig_2_1_pmbok_timeline', 'mode': 'code', 'height': 0.56,
                  'caption': G + '2-1. PMBOK 계보와 주변 표준 연표 1996–2026 (비선형 축)'}]},
    '7판 (2021) 실험 → 8판 (2025) 부분 회귀': {
        'figs': [{'file': 'fig_2_2_pmbok8_structure', 'mode': 'top',
                  'caption': G + '2-2. PMBOK 8판 구조 — 6 원칙 / 7 도메인 / 5 Focus Areas·40 프로세스'}]},
    '한국 사내 표준은 6판에 머물러 있다 — 그 함의와 처방': {
        'figs': [{'file': 'fig_2_2_domain_mapping', 'mode': 'top',
                  'caption': G + '2-3. 6판 10 KA → 8판 7 도메인 재매핑 (실선/파선)'}]},
    'PRINCE2 장치 ① Project Board 3역할 · ② Manage by Exception': {
        'figs': [{'file': 'fig_2_3_prince2', 'mode': 'top',
                  'caption': G + '2-4. PRINCE2 7 삼중 구조 + Project Board 3역할 (온담 배정)'}]},
    '애자일·SAFe·하이브리드의 위치 — 표준의 반대편이 아니다': {
        'figs': [{'file': 'fig_2_4_standards_map', 'mode': 'top',
                  'caption': G + '2-5. 표준 지형도 — 지식체계/방법론 × 거버넌스/인도 층'}]},
    '테일러링의 기준은 하나 — 되돌림 비용': {
        'figs': [{'file': 'fig_2_6_reversal_axis', 'mode': 'top',
                  'caption': G + '2-6. 되돌림 비용 축 위의 P1 vs P2'}]},
    'Boehm-Turner 5축 (2003) — 축이 갈리면 시스템을 쪼개라': {
        'figs': [{'file': 'fig_2_6_boehm_turner', 'mode': 'top',
                  'caption': G + '2-7. Boehm-Turner 5축 극좌표 — P1 전체와 SRS/SyRS 분할'}]},
    'Cynefin — 방법론 선택 도구가 아니다 (Snowden & Boone, 2007 HBR)': {
        'figs': [{'file': 'fig_2_6_cynefin', 'mode': 'top',
                  'caption': G + '2-8. Cynefin 네 도메인과 의사결정 순서 — P1 결정 예시'}]},
    # ---------------- 3교시
    '착수의 첫 번째 일은 검증이다 — 비즈니스 케이스를 온담 P1로 채우면': {'breaks': ['| 항목 | 무엇을 적는가']},
    'PMBOK 8판의 7 performance domains': {'table_split': 4},
    '온담의 이해관계자를 이 모델로 읽기 — 가장 위험한 사람은 권력자가 아니다': {'table_split': 5},
    '편익은 누가 소유하는가 — Zwikael & Smyrk의 ITO 모델 (2011)': {
        'figs': [{'file': 'fig_3_1_ito', 'mode': 'code', 'height': 0.5,
                  'caption': G + '3-1. Zwikael & Smyrk ITO 모델 — 책임의 분리선'}]},
    '편익 실현은 왜 대부분 실패하는가 — Ward & Daniel의 BDN': {
        'figs': [{'file': 'fig_3_1_bdn', 'mode': 'code', 'height': 0.45,
                  'caption': G + '3-2. 온담 편익의 BDN — 폐기율·가맹 발주 리드타임'}]},
    '프로젝트 헌장은 권한 문서다 — 항목별 의미 ① 목적 · 성공 기준 · 범위/제외': {
        'figs': [{'file': 'fig_3_2_doc_flow', 'mode': 'top',
                  'caption': G + '3-3. 착수 문서 흐름 — 비즈니스 케이스 → 헌장 → 계획서, PRINCE2·ISO 대응'}]},
    'Mitchell-Agle-Wood 현저성(Salience) 모델 (1997, AMR) — 3속성 7유형': {
        'figs': [{'file': 'fig_3_3_salience', 'mode': 'top',
                  'caption': G + '3-4. Mitchell-Agle-Wood 3속성 벤 다이어그램 7유형 + 온담 인물'}]},
    # ---------------- 5교시
    '거버넌스 — 조직도가 아니라 결정의 흐름': {
        'table_split': 3,
        'figs': [{'file': 'fig_3_4_governance', 'mode': 'top',
                  'caption': G + '3-5. 온담 P1 거버넌스 — 결정의 흐름(위임↓/예외↑)과 변경 통제 3층'}]},
    'Manage by Exception — 허용범위 격자 (온담 초안, 사례 §5.6)': {
        'figs': [{'file': 'fig_3_4_tolerance_grid', 'mode': 'besidetable', 'leftwidth': 0.42}],
        'table_font': r'\scriptsize'},
    '프리모템 — Gary Klein (2007, HBR, 2페이지)': {
        'figs': [{'file': 'fig_3_5_premortem', 'mode': 'top',
                  'caption': G + '3-7. 프리모템 절차와 "실패했다"의 문법'}]},
    # ---------------- 6교시
    '다섯 문서의 상호 관계 — 순서대로 쓰지만 순서대로 완성되지 않는다': {
        'figs': [{'mode': 'code', 'tex': FIVE_DOCS_TIKZ}]},
    # ---------------- 마무리
    'Rethinking Project Management (2006) — 다섯 방향이 이 교재의 뼈대다': {
        'figs': [{'file': 'fig_4_1_rpm', 'mode': 'top',
                  'caption': G + '4-1. Rethinking PM 다섯 방향 FROM→TOWARDS + Day1 대응 절'}]},
    'Staw — 몰입의 상승(escalation of commitment)과 결정자의 분리': {
        'figs': [{'file': 'fig_4_4_staw', 'mode': 'top',
                  'caption': G + '4-2. Staw 몰입의 상승 순환과 두 가지 조직 설계 처방'}]},
}
