# 용어·약어·문서 ID 색인 — Product 트랙(Day5~8) 편

> PM 트랙 색인(`02_용어약어색인.md`)에 이미 있는 약어(WBS·EVM·SLA·CCB·ITIL·RACI …)는 다시 싣지 않는다. 여기에는 Product 트랙에서 새로 나오는 약어, 딥게이지 정본의 ID 체계, 이 트랙이 특별한 뜻으로 쓰는 우리말 용어를 모았다. "→"는 그 개념을 설명하는 날·절이다.

---

## 1. 영문 약어

### 발견·전략

| 약어 | 풀어 쓰면 | 이 과정에서의 뜻 | → |
|---|---|---|---|
| PM / PO / PdM | Product Manager / Product Owner / Product Manager(약칭 충돌) | 이 트랙에서 PM은 **프로덕트 매니저**다(PM 트랙의 프로젝트 매니저와 다르다). PO는 스크럼의 백로그 책임 역할. 워크북 §0에서 세 용어를 합의문으로 정리 | D5 1장 |
| JTBD | Jobs To Be Done | 고객이 어떤 상황에서 어떤 진전을 위해 제품을 "고용"하는가 — 기능이 아니라 상황·동기·결과의 문장 | D5 2장 |
| 네 가지 힘 (Four Forces) | push · pull · anxiety · habit | 전환을 미는 힘 둘과 막는 힘 둘(Moesta) | D5 2장 |
| OST | Opportunity Solution Tree | 결과 → 기회 → 해법 → 실험의 트리(Torres). 해법 명사가 기회 층에 들어가면 무효 | D5 2장 |
| SAM / TAM / SOM | Serviceable Available / Total Addressable / Serviceable Obtainable Market | 딥게이지 초기 SAM 2,150개사, 확장 SAM 11,800개사 | D5 4장 |
| ICP | Ideal Customer Profile | 이상적 고객 프로필 — 세그먼트 정의의 산출물 | D5 4장 |
| LOI | Letter of Intent | 구매 의향서 — 계약이 아니다(D+90 LOI 2건) | D5 |
| RCF | Reference Class Forecasting | PM 트랙과 같다 — 유사 버티컬 SaaS 12건의 첫 유료·첫 ARR 1억까지 개월 | D5 4장 |
| Kano | — | 당연·성능·매력 품질 분류 — 검사항목 8개 한정 | D5 (심화) |
| BMC / VPC | Business Model Canvas / Value Proposition Canvas | 참고 캔버스 — 비판 재료로만 | D5 (심화) |

### 범위·실험·AI 제품

| 약어 | 풀어 쓰면 | 뜻 | → |
|---|---|---|---|
| MVP | Minimum Viable Product | 학습을 위한 최소 제품 — 이 트랙에서는 **Appetite 안에서 자른 범위** | D6 2장 |
| Appetite | — | Shape Up(Singer)의 어휘 — 얼마나 만들지가 아니라 **얼마나 쓸지(기간)**를 먼저 고정 | D6 2장 |
| MoSCoW | Must · Should · Could · Won't | PM 트랙과 같다. Won't에는 사유와 재검토 조건 | D6 2장 |
| man-month (mm) | — | 개발 공수 단위. 가용 24 → 17 / 백로그 41 | D6 2장 |
| DoD | Definition of Done | 완료 정의 — AI 기능은 eval 합격 기준이 DoD | D6 3장 |
| eval / Eval Set | evaluation | AI 기능의 채점용 데이터셋과 지표·합격 기준(60건 = 자동차 3세트 × 20) | D6 3장 |
| OCR / VLM / STT | Optical Character Recognition / Vision-Language Model / Speech-to-Text | GAUGE의 세 AI 구성요소 | D5·D6 |
| FN / FP | False Negative / False Positive | 불량 → 양품(놓침) / 양품 → 불량(오탐). FN을 낮추면 FP가 오른다 | D6 3장, D7 5장 |
| F1 | — | 정밀도·재현율의 조화평균 — 외관 결함 분류 지표 | D6 3장 |
| HITL | Human-in-the-loop | 사람이 승인하는 흐름 — 자동판정 ON/OFF, 신뢰도 임계값, 책임 한계 문구 | D6 3장 |
| error budget | — | PM 트랙 Day4와 같은 개념을 AI 판정 오류에 적용 — 월 허용 FN/FP와 소진 시 조치 | D6 3장, D7 5장 |
| criteria drift | — | 사고 후 합격 기준을 바꾸는 것 — 개정 이력 없이 하면 eval이 무효 | D7 5장 |
| OEC | Overall Evaluation Criterion | 실험의 단일 판정 지표(Kohavi) | D6 4장 |
| SRM | Sample Ratio Mismatch | 실험군 배분 비율 이상 — 실험 무효 신호 | D6 4장 |
| peeking | — | 실험 종료 전 중간 결과를 보고 멈추는 것 — 사전등록으로 금지 | D6 4장 |
| PR/FAQ | Press Release / FAQ | Amazon Working Backwards — 출시 보도자료를 먼저 쓴다 | D6 4장 |
| GA / 알파 / 베타 | General Availability | 3단 게이트 — 베타 진입 기준서 | D6 |
| 8D / NCR / PPAP / SQ / SQE | 8 Disciplines / Non-Conformance Report / Production Part Approval Process / Supplier Quality / Supplier Quality Engineer | 자동차 협력사 품질 어휘 — 8D = 포스트모템, NCR = 부적합 보고, SQ 등급 = 1차사의 협력사 등급 | D5~D8 |
| CCP / HACCP | Critical Control Point / Hazard Analysis and Critical Control Points | 식품 위생 관리 — 온담 4번째 세트의 어휘. CCP 모니터링 = 런타임 인바리언트 감시 | D8 |
| MES | Manufacturing Execution System | 제조 실행 시스템 — 타깃군 보유율 38% | D5 |

### 지표·유닛이코노믹스

| 약어 | 풀어 쓰면 | 뜻 | → |
|---|---|---|---|
| PMF | Product-Market Fit | 곡선이 평탄해졌는가 — 리텐션 평탄선 + 유닛이코노믹스 + 채널 | D7 1장 |
| ARR / MRR | Annual / Monthly Recurring Revenue | **구축비·컨설팅비는 ARR이 아니다**(계약 4.9억 vs 순SaaS 3.8억) | D6·D7 |
| ACV | Annual Contract Value | 고객당 연 계약액 — 계약 기준 / 순SaaS 기준 둘 | D7 |
| GM / COGS | Gross Margin / Cost of Goods Sold | 매출총이익률 — AI 추론 원가가 COGS의 주인. 분모에 따라 61% / 49.8% | D7 4장 |
| CAC | Customer Acquisition Cost | 채널별(인바운드 310만·아웃바운드 1,470만·추천 90만·blended 620만). 오가닉을 빼면 유료 획득 CAC 1,051만 | D7 4장 |
| payback | — | CAC 회수 개월 — 매출 기준(2.3)과 GM 기준(6.1)이 다르다 | D7 4장 |
| LTV | Lifetime Value | 고객 생애 가치 — 이탈률·GM·ACV의 가정에 따라 5.8:1과 1.9:1 | D7 4장 |
| GRR / NDR | Gross / Net Revenue Retention | 이탈만 반영 / 확장까지 반영(84% / 97%) — NDR > 100%가 되려면 밸류메트릭에 확장 여지가 있어야 | D6·D7 |
| burn multiple | — | 순소진 ÷ Net New ARR(Sacks). 4.26 → 2.07 → 1.20. efficiency score는 역수 | D7 4장 |
| North Star | — | 제품이 고객에게 준 가치를 대표하는 한 지표 + 그것을 움직이는 입력 지표 트리 | D7 3장 |
| OKR | Objectives and Key Results | KR은 지표가 아니라 결과로 쓴다 | D7 (심화) |
| 채택률 / 활성률 | — | 자동판정 채택률(수정 없이 승인 ÷ 분모 3종) / 검사원 계정 활성률(68 → 41%) | D7 |
| 코호트 / 삼각행렬 | cohort / triangle | 같은 시기에 계약한 로고 집단의 월별 잔존 — M0~M6 격자, 미도달 셀은 ▨ | D7 2장 |

### 자본

| 약어 | 풀어 쓰면 | 뜻 | → |
|---|---|---|---|
| RCPS | Redeemable Convertible Preferred Stock | 상환전환우선주 — 시드 12억. 참가적 1x + 상환권 연 3% + drag 60% | D6 5장 |
| pre / post(-money) | — | 투자 전/후 기업가치(48 / 60억). 옵션풀이 pre에 있으면 기존 주주가 희석을 진다 | D6·D8 |
| FD | Fully Diluted | 완전 희석 기준 주식수(옵션풀·전환 포함) | D6·D8 |
| 참가적 / 비참가적 | participating / non-participating | 청산 시 우선권 회수 후 잔여에도 참가하는가 | D6 5장 |
| drag-along / ROFR | — | 동반 매도권 / 우선매수권 | D6·D8 |
| TIPS | Tech Incubator Program for Startup | 민간 투자 연계 정부 R&D — 8억(2년), 조건 "6개월 내 유료 5개사" | D6 |
| SAFE | Simple Agreement for Future Equity | 브릿지 8억, post-money cap 180억, discount 20% → cap 적용 | D8 4장 |
| cap / discount | — | 전환 상한 기업가치 / 전환 할인율 | D8 4장 |
| 옵션풀 / ESOP | — | 임직원 스톡옵션 유보 — 15% pre-money 조항의 효과 1.29%p(= 풀 가치 25.4억) | D8 4장 |
| IC | Investment Committee | 투자심의위원회 — 파트너 반대신문 | D8 |
| IR | Investor Relations | IR 덱·IR 1페이저 — "IR 기재값"은 검산값과 구별한다 | D7·D8 |
| BATNA | Best Alternative To a Negotiated Agreement | 대한기공 연 2.4억 × 3년 | D8 |
| 텀시트 | term sheet | 투자 조건 요약 — 법적 구속력은 일부 조항만 | D6·D8 |

### 엔터프라이즈·온담 딜

| 약어 | 뜻 | → |
|---|---|---|
| RFI / RFP / SOW | 정보 요청서 / 제안 요청서 / 작업 명세서 — 온담 RFI 2027-11-02 | D8 |
| 온프렘 / 클라우드 | on-premises — GPU 서버 2대 + 운영 0.7 FTE, 릴리스 분기 1회 | D8 |
| 커스터마이징 / 제품화 / 거절 | 47건의 3분류 — 유상 커스텀(별도 SOW) / 로드맵 편입(무상) / 대안 제시 | D8 2장 |
| 집중 리스크 | 한 고객의 비중 — ARR 37% / 24.1% / 개발 용량 82% 세 표기 | D8 1장 |
| SLA·OLA·UC / 배상 상한 | PM 트랙 Day4와 같은 3층 — 배상 상한 10%(딥게이지) vs 100%(온담) | D8 3장 |
| fit criterion | ISO/IEC 25010의 어휘 — 인수 기준의 수치와 **모집단** | D8 5장 |
| ISMS-P | 정보보호·개인정보보호 관리체계 인증 — 딥게이지 미인증, 218문항의 배경 | D8 |

---

## 2. 문서 ID 체계

| 접두어 | 종류 | 정본 위치 | 예 |
|---|---|---|---|
| G-nn | 딥게이지 단계별 지표 | 딥 정본 §7.1 | G-03 ARR, G-17 코호트, G-20/20b/20c 채택률 분모 3종 |
| V-nn | eval 정본(v1 / v2) | §7.3 | V-03 FN 8.1 → 2.4%, V-04 FP 14.6 → 21.3% |
| E-nn | 온담 딜 | §7.4 | E-04 라이선스 3.78억, E-10 47건/138 mm |
| K-nn | 캡테이블 시점 | §7.5 | K-02 시드, K-04 한강, K-05 코너스톤 |
| Ret-A / Ret-B / Ret-C | 코호트 삼각행렬 3장(익명 A / 익명 B / 자사) | §7.2 | Ret-A 분모 = 활성 계정 |
| D+n | 설립(2026-03-02)부터의 일수 | 전체 | D+300 = 2026-12-27, D+600 = 2027-10-23 |
| ㉑~㊵ | Product 트랙 산출물 20종 | 워크북 §0.2 | ㉗ Eval 명세서, ㊵ 편익 원장 공동 확정본 |
| ①~⑳ | PM 트랙 산출물(입력으로 쓰인다) | PM 워크북 | ⑱ 이관 목록, ⑳ 편익 원장 |
| F-nn | 설계된 함정(강사·저자용, 제작 노트) | 14_제작노트 §3 | F-06 코호트 분모 |
| OP-nn (기회) / A-nn (가정) / X-01~03 (실험) | Day5 트리·가정 맵·실험 카드의 ID — 워크북이 정한다 | D5 워크북 | OP-01 전기 31분, A-05b 수용 |
| B-nn (백로그) / DS-vn (데이터셋) / H1~4 (청구서 가설) | Day6 백로그 29건 · eval 데이터셋 버전 · 원가 붕괴 가설 — 워크북이 정한다 | D6 워크북 | B-17 자동판정(Won't), DS-v1 60건, H1 재촬영 |
| X-04~07 | Day6 사전등록 실험(판정 초안 베타 · 라인 과금 · 온보딩 · 조도 경고) | D6 워크북 ㉙ | X-07 표본 177/arm |
| INC-nn / D1~D8 / NS-n / CR-nnn | Day7 사고 보고서(8D 단계) · North Star 후보 · 변경요청 번호 — 워크북이 정한다 | D7 워크북 | INC-01 세영정공 D+520, NS-1 주간 승인 검사기록, CR-044 온프렘 전환 |
| C-01~47 | 온담 커스터마이징 요구 번호 — 저자별 19/11/9/5/3, 차원 태그 ①~⑤·—, 3분류 — 워크북이 정한다 | D8 워크북 ㊱ | C-05 마스터 구축(거절), C-31 온프렘(유상) |
| D-1~D-4 | 온담 4세트 측정 세트(냉장 / HACCP / 입고 / 안성) × 20건 = 80건 | D8 워크북 ㊵ 항목 4 | D-2 재현율 ≥ 97% |
| B-09 / B-10 | ㊵ 원장 v2 신설 편익(검사기록 공수 · CCP 리드타임) — PM B-01~08 뒤에 | D8 워크북 ㊵ | B-09 1,260 인시 |
| T2 / T3 A안·B안 | 캡테이블 시점 — SAFE 전환 후 / 한강 / 코너스톤(= K-03 / K-04 / K-05) | D8 워크북 ㊴ | T3 A안 FD 1,772,879 |
| ㉮ ㉯ ㉰ | 채택률 분모 3종 | §7.1 | — |

**충돌 주의**: PM 트랙의 `O-nn`은 온담 운영 지표(O-08 재고 정확도)이고 Product 트랙의 `O-nn`은 기회(Opportunity)다 — Day8에서 둘이 한 문서(㊵)에 만나므로 Product 쪽은 `OP-nn`으로 쓴다. `P1`은 온담 프로젝트이자 운영 인시던트 등급이며 Product 트랙에서는 쓰지 않는다.

---

## 3. 이 트랙이 특별한 뜻으로 쓰는 우리말 용어

| 용어 | 뜻 | → |
|---|---|---|
| 역할 전환 | 발주자 → 공급자. 같은 문서를 반대편에서 쓴다는 선언(산출물이 아니라 서명) | D5 0교시 |
| 기회 | 고객의 진전을 막는 미충족 욕구 — 해법 명사가 없는 문장 | D5 2장 |
| 가정 맵 | 가치·사용성·실현·사업성 가정을 중요도 × 증거 부족으로 배치 | D5 3장 |
| 실험 카드 | 가설·방법·표본·지표·성공 기준·기간을 사전등록한 한 장 | D5 3장 |
| 전략 커널 | 진단 / 추진 방침 / 일관된 행동(Rumelt) — 한 장 | D5 4장 |
| 해법 명사 금지 | 기회 문장에 제품·기능·기술 이름을 쓰지 않는 규칙 | D5 |
| 절단 | 백로그를 Appetite에 맞춰 자르는 결정 — Won't에 사유 | D6 2장 |
| 합격 기준 | eval의 수치 기준(FN ≤ 3.0% & OCR ≥ 95%) — 개정에는 승인권자와 이력 | D6 3장 |
| 밸류메트릭 | 무엇에 과금하는가(좌석/라인/건수/성과) — 고객 가치와 원가에 동시에 정렬해야 | D6 4장 |
| 공헌이익률 | 매출 − 변동원가(추론·STT·저장) ÷ 매출 — 헤비 고객 48.5% | D6 4장 |
| ARR 오염 | 구축비·컨설팅비를 ARR에 넣는 것 | D6·D7 |
| 분모 선언 | 지표의 분모를 표 첫 열에 쓰는 규칙 — 계약 MRR vs 순SaaS MRR, 활성 계정 vs 신규 계약 로고 | D7 |
| 평탄선 | 코호트 잔존율이 더 이상 떨어지지 않는 높이 — PMF의 첫 신호 | D7 2장 |
| 동일 연령 비교 | 코호트를 같은 경과 월(M4)로 줄 세워 비교 | D7 2장 |
| 무배분은 무판정이 아니다 | 판독 불가한 것에 배분하지 않는 것이 가장 강한 판정 | D7 2장 |
| 게임 가능성 | 지표를 실제 가치 없이 올릴 수 있는 방법 — North Star 후보 검증 | D7 3장 |
| 예산 3분리 | 차별화 / 위생 / 신뢰 복구 — 사고 후 로드맵 예산 | D7 6장 |
| 같은 금액의 비대칭 | 21억 = 온담의 4.9% = 딥게이지의 37% | D8 1장 |
| 5차원 표 | 판정 라벨·식별자·단위·규격 근거·부적합 흐름 — 47건을 40분에 판정하는 도구 | D8 2장 |
| 제품-프로젝트 경계 | 제품 라인 / 유상 커스텀 / 고객 자체 개발 — 소유권·재사용권·유지보수 | D8 3장 |
| 인수 기준의 모집단 | FN 2.4%가 어느 데이터셋에서 나왔는가 — 모집단 없는 fit criterion은 무효 | D8 5장 |
| 공동 확정본 | 두 트랙이 같은 표에 각자 서명하는 8일의 유일한 공동 산출물(㊵ = ⑳) | D8 5장 |
