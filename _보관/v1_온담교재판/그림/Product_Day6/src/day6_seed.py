# -*- coding: utf-8 -*-
"""Day6 (시드 D+120~300) — [추가 설정] 숫자 정본과 검산.  워크북 §X.5·교재·그림·슬라이드는 이 스크립트의 출력만 인용한다.
정본(고정): 공통/가상회사_딥게이지.md §3.2(시드 표·UE 표), §4.2~4.4(사건), §7.1 G-01~15 D+300 열, G-37~39, §7.3 V-01~07 v1, §7.5 K-01·K-02.
실행: python3 day6_seed.py  → 표를 stdout에 출력"""
from collections import Counter
import math

# ── 0. 시점 ──────────────────────────────────────────────────────────
D0="2026-03-02"                      # 월요일. D+n 요일 = n mod 7 (0=월)
def wd(n): return "월화수목금토일"[n%7]
DATES={120:"2026-06-30",126:"2026-07-06",149:"2026-07-29",165:"2026-08-14",217:"2026-10-05",130:"2026-07-10",137:"2026-07-17",150:"2026-07-30",151:"2026-07-31",158:"2026-08-07",172:"2026-08-21",179:"2026-08-28",
       186:"2026-09-04",200:"2026-09-18",215:"2026-10-03",230:"2026-10-18",235:"2026-10-23",240:"2026-10-28",270:"2026-11-27",280:"2026-12-07",284:"2026-12-11",297:"2026-12-24",300:"2026-12-27"}
BASE_DAY=297                          # 워크북 기준일 = D+300(일) 직전 영업일 목요일(12-25 휴일)
MILESTONES=[(120,"Day6 시작 — 5명, 현금 약 5,400만, 시드 협상 중"),(126,"조현우(앱·프론트)·서하늘(ML) 합류 — 개발 4명 = 오세진·김태오·조현우·서하늘 [추가 설정]"),
 (130,"㉖ MVP 범위 결정서 v1.0 — 41 → 24 mm"),(137,"㉘ 프라이싱·밸류메트릭 결정서 v1.0 — 라인 45만"),(150,"노들 선투자 2억(전환) — 전날 잔액 약 1,500만, 런웨이 0.4개월이던 날"),
 (151,"㉗ Eval 명세서·오류 예산·HITL v1.0"),(158,"㉙ PR/FAQ·실험 사전등록 v1.0"),(172,"㉚ 시드 텀시트 검토·캡테이블 v1 — 협상 요청 3"),
 (179,"시드 클로징 — RCPS 12억(선투자 2억 포함), pre 48 · post 60 [정본 4.2 'D+180']"),(186,"주주간계약 검토 중 옵션풀 위치 조항 부재 발견 — ㉚ v1.1 부속 메모"),
 (190,"임준호(인프라)·라벨러 2·경영지원 합류 → 10명"),(200,"동보프레스 '도면 미업로드 모드' 조건으로 파일럿 계약(김도윤 공문 확인) — B-19 승격 [추가 설정]"),
 (217,"TIPS 선정(일반트랙 8억/2년) — 운영사 추천 조건 '2027-02(D+360)까지 유료 5개사' [추가 설정]"),(230,"조현우 퇴사(통보 D+228 금) — '커스터마이징 요청만 하다가 끝난다' [정본 4.3]"),
 (235,"㉖ v1.1 — 가용 24 → 17 mm 재산정, 2차 절단"),(240,"세영정공 첫 유료 계약(라인 3 · 구축비 300만) — 첫 유료"),(260,"태산정밀 유료(라인 3 · 62항목 · 구축비 400만) [추가 설정]"),
 (270,"eval v1 측정 — OCR 91.4 / FN 8.1 / FP 14.6 / F1 0.78 [정본 V]"),(275,"동보프레스 유료(라인 3 · 구축비 500만) → 유료 3개사 [추가 설정]"),
 (280,"클라우드 청구서 — 예상 210만 → 실제 780만 [정본 4.4]"),(284,"㉘ v1.1 — 원가 붕괴 대응(항목 4) 개정"),(297,"워크북 기준일(목)"),(300,"GA · 12명 · 유료 3개사 · 현금 15.4억")]

# ── 1. 인원·고정비 [추가 설정 — G-01 12명, G-11 6,900만에 맞춤] ─────────────
STAFF=[("강민수","CEO",0),("오세진","CTO",0),("윤하경","CPO",0),("김태오","백엔드 개발",45),("이수민","현장 CS(전 검사원)",70),
       ("조현우","앱·프론트 개발 (D+230 퇴사)",126),("서하늘","ML 엔지니어",126),("임준호","인프라·보안",190),("라벨러 2인","데이터 라벨링·검수",190),
       ("최은서","경영지원",190),("박정우","필드 세일즈",200),("CS 2호","온보딩·지원",250)]
HEADCOUNT_D300=12                     # G-01 (조현우 제외: 3+2+1+1+2+1+1+1 = 12)
BURN_D300=6900                        # G-11 (만원/월): 급여 5,000 + 클라우드 780 + 사무실 450 + 기타 670 [추가 설정]
DEV4=["오세진(CTO, 실무 50%→100%)","김태오","조현우","서하늘"]   # 4명 × 6개월 = 24 mm (G-37)

# ── 2. 백로그 41 mm [추가 설정 — G-38] (B-ID, 항목, 상위 노드(㉓), 견적 mm, MoSCoW v1.0, 근거·의존) ──
BACKLOG=[
 ("B-01","사진 촬영·업로드 앱(오프라인 큐·라인 선택)","OP-01(a)",2.0,"Must","X-01 방식의 자동화. 기록이 나는 곳"),
 ("B-02","치수 OCR 파이프라인(VLM 호출·검사항목 매핑·신뢰도)","OP-01(a)",2.5,"Must","X-02 88.7% — 오전 조건 93.1에서 시작. 조도 변수 재작업 위험"),
 ("B-03","음성 메모 첨부·텍스트 변환(STT)","OP-01(b)",0.5,"Must","문장 생성(B-26)과 분리 — 변환만"),
 ("B-04","검사기록 편집·승인 화면(웹)","OP-01",1.5,"Must","HITL 승인의 자리(㉗ 항목 6)"),
 ("B-05","검사항목 마스터 매핑 도구(엑셀 업로드·매핑)","OP-01 / A-08",1.0,"Must","온보딩 2주(X-06)의 전제"),
 ("B-06","조도 경고(사진 밝기 검사·재촬영 안내)","OP-05 / X-02",0.5,"Should","X-02 오후 84.7% 대응. 싸고 안전"),
 ("B-07","부적합(NCR) 등록 — 사진·기록·판정 묶음","OP-02(a)",1.5,"Must","팀장이 돈을 내는 이유(A-03)"),
 ("B-08","H사 SQ 포털 제출 초안(규격 1종)","OP-02(a)",1.5,"Must","파일럿 3사 모두 H사 계열·납품"),
 ("B-09","포털 규격 3종 추가(K사·M사·S사)","OP-02(a) / OP-07",3.0,"Could","유료 5개사 확장 시 필요 — 지금은 아님"),
 ("B-10","8D 리포트 초안 D1~D4 자동 생성","OP-03(a)",1.5,"Must","11.5시간의 '붙이는' 부분"),
 ("B-11","8D D5~D8 템플릿·첨부","OP-03(b)",1.0,"Could","D5~D8은 사람의 판단"),
 ("B-12","판정 로그(누가·언제·어느 사진·어느 기준·초안 여부)","OP-04(a)",0.5,"Must","커널 행동 4. 다른 항목의 부산물"),
 ("B-13","감사용 판정 근거 월 리포트","OP-04(b)",1.0,"Could","로그가 쌓인 뒤"),
 ("B-14","외관 결함 분류·판정 초안 표시(오전 라인 베타·승인 필수)","OP-05(a)",1.5,"Should","㉓ 4순위. ㉗ 합격 기준·HITL 아래에서만"),
 ("B-15","판정 편차 리포트(검사원별·시간대별)","OP-05(c)",1.0,"Could","B-12 로그의 부산물"),
 ("B-16","기준 사진 라이브러리(양품/불량 예시)","OP-05(b)",1.0,"Could","㉓ 5순위"),
 ("B-17","자동판정 모드(승인 없이 확정)","OP-05(a)",2.0,"Won't","A-05b 미제거 · FN 기준 미충족 — 재검토 조건 ㉗"),
 ("B-18","온프렘 배포 패키지(GPU·설치·릴리스)","OP-07",6.0,"Won't","㉕ 하지 않는 것 1. 유료 5개사 후 재검토"),
 ("B-19","도면 미업로드 모드(마스터만·도면 이미지 제외)","OP-07",0.5,"Could","김도윤 I-27 — H사 계열 클라우드 도입의 열쇠일 수 있음"),
 ("B-20","태산정밀 라인 전용 검사항목 62개(항목 구조 확장)","(고객 요청)",1.5,"Could","LOI 조건. 첫 커스터마이징 — 구조로 풀 것인지 미정"),
 ("B-21","MES 검사 모듈 연동(push)","OP-01 / (고객 요청)",3.0,"Won't","MES 보유 38%·엑셀 병행 71% — 연동은 SI"),
 ("B-22","관리자 대시보드(라인별 현황·승인 대기)","OP-02 / OP-04",1.0,"Should","팀장 화면. 없으면 엑셀로 대체 가능"),
 ("B-23","부적합 발생 알림(팀장·1차사)","OP-02(b)",0.5,"Could","반쪽 해법 — B-07 뒤에"),
 ("B-24","사용자·권한·라인 관리·과금 연동","(기반)",1.0,"Must","라인 과금(㉘)의 기반"),
 ("B-25","eval 하네스·데이터셋 라벨링 도구","㉗",0.5,"Must","합격 기준을 잴 도구"),
 ("B-26","음성 메모 → 검사기록 문장 생성","OP-01(b)",1.0,"Should","B-03 위에. 없어도 기록은 된다"),
 ("B-27","SSO·감사 로그·보안(ISMS 준비)","(고객 요청)",1.0,"Could","대기업 계열 요구 — 지금 고객은 아님"),
 ("B-28","검사원 교육 모드·튜토리얼","A-01",1.0,"Could","이수민이 현장에서 대신한다"),
 ("B-29","데이터 내보내기(엑셀·API)","(고객 요청)",0.5,"Could","MES 연동의 최소 대체"),
]
TOTAL_MM=sum(b[3] for b in BACKLOG)
MOSCOW=Counter(); [MOSCOW.update({b[4]:b[3]}) for b in BACKLOG]
assert abs(TOTAL_MM-41.0)<1e-9, TOTAL_MM
assert MOSCOW["Must"]==14.0 and MOSCOW["Should"]==4.0 and MOSCOW["Could"]==12.0 and MOSCOW["Won't"]==11.0, MOSCOW
CAP_V10=24.0; RESERVE_RATE=0.25; MUST_CAP_RATE=0.60
reserve_v10=CAP_V10*RESERVE_RATE                                  # 6.0 — 버그·파일럿 지원·온보딩
must_ratio_v10=MOSCOW["Must"]/CAP_V10                             # 58.3%
in_appetite_v10=MOSCOW["Must"]+MOSCOW["Should"]+reserve_v10       # 24.0
assert abs(in_appetite_v10-24.0)<1e-9

# ── 3. 24 → 17: 손실 분해 (D+235, 조현우 퇴사 후) [추가 설정 — G-37] ─────────
LOSS=[("조현우 잔여 기간(D+230~300, 2.17개월 × 1명)",2.2),("태산정밀 62항목 커스텀 — 계획 외 착수(B-20 Could, 조현우 1.4 + 김태오 0.8)",2.2),
      ("인수인계·채용 면접(3명 × 0.15 × 2.17개월)",1.0),("조현우 WIP 폐기(오프라인 큐 재설계·포털 제출 초안)",0.7),("B-02 조도 재작업 초과(계획 2.5 → 실제 3.4)",0.9)]
CAP_V11=CAP_V10-sum(l[1] for l in LOSS)
assert abs(CAP_V11-17.0)<1e-9, CAP_V11
DONE_BY_235=["B-01","B-02","B-04","B-05","B-07","B-12","B-24"]          # 완료(계획 mm 기준 10.0)
done_mm=sum(b[3] for b in BACKLOG if b[0] in DONE_BY_235)
WIP_KEPT={"B-03":0.3,"B-08":0.2,"B-10":0.2}                              # 진행 중 — 살린 부분 0.7
reserve_used=0.8                                                          # 파일럿 지원에 이미 쓴 예비
remaining_eff=CAP_V11-done_mm-sum(WIP_KEPT.values())-reserve_used         # 5.5
assert abs(remaining_eff-5.5)<1e-9, remaining_eff
# v1.1 재절단 — 남은 5.5로 무엇을 끝내는가
V11_PLAN=[("B-03","음성 변환 마무리",0.2,"Must"),("B-08","포털 제출 초안 → 규격 엑셀·PDF 내보내기(사람이 업로드)",0.4,"Must(축소)"),
          ("B-10","8D 초안 D1~D3만(사진·기록 자동 첨부)",0.5,"Must(축소)"),("B-06","조도 경고",0.5,"Should"),("B-14","판정 초안 표시 — 세영 오전 1라인 베타",1.0,"Should(축소)"),
          ("예비","온보딩 3사·GA 버그",2.9,"—")]
assert abs(sum(p[2] for p in V11_PLAN)-remaining_eff)<1e-9
V11_CUT=[("B-08","1.5 → 0.4","자동 제출 → 내보내기. 포털 업로드는 팀장이 한다(2분)"),("B-10","1.5 → 0.5","D4 원인 문장은 사람이. D1~D3 자동 첨부만"),
         ("B-25","0.5 → 0","eval 도구는 CTO가 노트북 스크립트로 — 백로그 밖"),("B-22","1.0 → Won't(다음 사이클)","팀장 화면은 엑셀 내보내기로 대체"),
         ("B-26","1.0 → Could","음성 문장 생성 — 변환(B-03)까지만"),("B-14","1.5 → 1.0","베타 범위를 세영 1라인으로 축소")]
must_total_v11=done_mm+sum(WIP_KEPT.values())+sum(p[2] for p in V11_PLAN if p[3].startswith("Must"))   # 11.8
must_ratio_v11=must_total_v11/CAP_V11                                                                  # 69.4%
rem_must=sum(p[2] for p in V11_PLAN if p[3].startswith("Must")); rem_should=sum(p[2] for p in V11_PLAN if p[3].startswith("Should")); rem_res=2.9

# ── 4. eval v1 데이터셋 60건 [추가 설정 — V-01~07] ───────────────────────
DATASET=[("A","세영정공(절삭) 20건","D+160~175 · 오전 9~11시"),("B","동보프레스(프레스) 20건","D+176~188 · 오전 9~11시"),("C","한빛금속(단조) 20건","D+189~200 · 오전 9~11시")]
N_CASES=60; N_ITEMS=1480; N_DEFECT=296; N_GOOD=N_ITEMS-N_DEFECT; N_DIM=1050; N_APPEAR=430; APPEAR_DEFECT=96
FN_CNT=24; FP_CNT=173; OCR_OK=960; TP_AP=76; FN_AP=20; FP_AP=23
FN_RATE=FN_CNT/N_DEFECT; FP_RATE=FP_CNT/N_GOOD; OCR_RATE=OCR_OK/N_DIM
prec=TP_AP/(TP_AP+FP_AP); rec=TP_AP/(TP_AP+FN_AP); F1=2*prec*rec/(prec+rec)
assert round(FN_RATE*100,1)==8.1 and round(FP_RATE*100,1)==14.6 and round(OCR_RATE*100,1)==91.4 and round(F1,2)==0.78, (FN_RATE,FP_RATE,OCR_RATE,F1)
assert TP_AP+FN_AP==APPEAR_DEFECT
CRITERIA_V1=dict(FN=8.0,OCR=90.0)                                   # V-06
PASS_V1=dict(FN=FN_RATE*100<=CRITERIA_V1["FN"],OCR=OCR_RATE*100>=CRITERIA_V1["OCR"])   # FN 불합격(0.1%p), OCR 합격
LATENCY_V1=1.8; UNIT_COST_V1=32                                     # V-05
LABEL_DISAGREE=0.068; CONF_THRESHOLD=0.85
ERROR_BUDGET=dict(fn_monthly="라인별 — 초안 '양품' 중 검사원이 '불량'으로 뒤집은 비율 ≤ 8.0%(HITL 수정 로그)",fp_monthly="초안 '불량' 중 검사원이 '양품'으로 뒤집은 비율 ≤ 15%",
                  threshold="신뢰도 0.85 미만은 초안 미표시('판정 보류')",exhaust="해당 라인 초안 표시 OFF → 원인 분석 → 재학습 → 재측정 합격 후 ON. 초과 기간 모델 릴리스 동결",report="주간(내부) · 월간(고객 품질팀장)")

# ── 5. 프라이싱·UE (정본 §3.2 표) + 청구서 (G-39, 4.4) ───────────────────────
PRICE_LINE=45; LINES=3.0; SEATS="무제한"
UE={"표준 공장":dict(photos=4100,vlm=32,stt=3.8,store=1.2),"헤비 고객(동보프레스)":dict(photos=19400,vlm=32,stt=3.8,store=3.6)}
def ue(d):
    infer=d["photos"]*d["vlm"]/10000; var=infer+d["stt"]+d["store"]; rev=LINES*PRICE_LINE
    return dict(infer=infer,var=var,rev=rev,var_rate=var/rev,cm=1-var/rev)
UE_OUT={k:ue(v) for k,v in UE.items()}
assert round(UE_OUT["표준 공장"]["var"],1)==18.1 and round(UE_OUT["헤비 고객(동보프레스)"]["var"],1)==69.5
assert round(UE_OUT["표준 공장"]["cm"]*100,1)==86.6 and round(UE_OUT["헤비 고객(동보프레스)"]["cm"]*100,1)==48.5
BILL_EXPECTED=210; BILL_ACTUAL=780; BILL_EXCESS=BILL_ACTUAL-BILL_EXPECTED; HEAVY_EXCESS=444; HEAVY_SHARE=HEAVY_EXCESS/BILL_EXCESS   # 77.9%
HEAVY_MULT=HEAVY_EXCESS/UE_OUT["헤비 고객(동보프레스)"]["var"]     # 6.39배 (F-09)
BILL_BY_SERVICE=[("VLM API 호출",612),("STT",41),("저장·전송",58),("GPU·컴퓨트(서빙·배치)",69)]   # [추가 설정] 서비스별로는 보이고 고객·사진 단위로는 안 보인다
assert sum(v for _,v in BILL_BY_SERVICE)==BILL_ACTUAL
HYPOTHESES=[("H1","검사원이 같은 부위를 재촬영한다(습관·조도 불안)","앱 UX·조도 경고·교육","사진 단위 재촬영 플래그"),("H2","앱의 저신뢰도 자동 재시도 루프(타임아웃 재호출)","버그 수정","호출 단위 재시도 카운트"),
            ("H3","모델 갱신 시 전량 재추론 배치가 동보 사진에 걸렸다","배치 정책","배치 작업별 사진 수"),("H4","프레스 라인의 사진 건수 자체가 계약 시 추정(19,400)보다 많다","건수 상한·공정 사용 조항","고객·라인·월 사진 수")]
FAIR_USE_PHOTOS=6000; OVERAGE_PER_PHOTO=40; WARN_PHOTOS=4500        # [추가 설정] 라인당 월
# 매출 (G-03~07)
CUSTOMERS=[("세영정공",3,300,240),("태산정밀",3,400,260),("동보프레스",3,500,275)]   # 라인, 구축비(만), 유료 시작 D+
SAAS_ARR=sum(c[1]*PRICE_LINE*12 for c in CUSTOMERS); SETUP=sum(c[2] for c in CUSTOMERS); CONTRACT_TOTAL=SAAS_ARR+SETUP
MRR_SAAS=SAAS_ARR/12; MRR_CONTRACT=CONTRACT_TOTAL/12; ACV_SAAS=SAAS_ARR/3; ACV_CONTRACT=CONTRACT_TOTAL/3
assert SAAS_ARR==4860 and SETUP==1200 and CONTRACT_TOTAL==6060 and MRR_SAAS==405 and MRR_CONTRACT==505
AI_COST_D300=210; AI_RATIO_CONTRACT=AI_COST_D300/MRR_CONTRACT; AI_RATIO_SAAS=AI_COST_D300/MRR_SAAS     # 41.6% / 51.9% (G-09)
COGS_OTHER=88; GM_IR=(MRR_CONTRACT-AI_COST_D300-COGS_OTHER)/MRR_CONTRACT                                # 41% (G-10)
GM_DEC_ACTUAL=(MRR_CONTRACT-BILL_ACTUAL-COGS_OTHER)/MRR_CONTRACT                                        # 12월 실제 청구서 반영 시
LIABILITY_CAP=ACV_SAAS*0.10                                                                             # 162만 (G-40)
assert round(AI_RATIO_CONTRACT*100,1)==41.6 and round(AI_RATIO_SAAS*100,1)==51.9 and round(GM_IR*100)==41 and LIABILITY_CAP==162
NET_NEW_ARR_Q=4860; BURN_Q=BURN_D300*3; BURN_MULTIPLE=BURN_Q/NET_NEW_ARR_Q; EFFICIENCY=NET_NEW_ARR_Q/BURN_Q     # 4.26 / 0.23 (G-13·14)
assert round(BURN_MULTIPLE,2)==4.26

# ── 6. 캡테이블 T0 → T1 (K-01 → K-02) ─────────────────────────────────
INV=12e8; PRE=48e8; POST=PRE+INV; FD0=1_000_000; PRICE=PRE/FD0; N_INV=int(INV/PRICE); FD1=FD0+N_INV
T0={"강민수":450_000,"오세진":300_000,"윤하경":150_000,"옵션풀":100_000}
T1=dict(T0); T1["노들투자파트너스(RCPS)"]=N_INV
assert PRICE==4800 and FD1==1_250_000 and N_INV==250_000
PCT1={k:v/FD1 for k,v in T1.items()}; assert round(PCT1["강민수"]*100,1)==36.0 and round(PCT1["옵션풀"]*100,1)==8.0
# 옵션풀 위치가 정해졌더라면 — 풀 합계 10%를 라운드 후 FD 기준으로 요구받았을 때 (Day5 그림 4-4와 같은 모형)
fd_post=(FD1-T0["옵션풀"])/0.9; pool_post=0.10*fd_post; inv_post=N_INV/fd_post; fnd_post=900_000/fd_post
fd_pre=900_000/(1-0.20-0.10); inv_pre=0.20; fnd_pre=0.70; price_pre=PRE/(fd_pre-0.20*fd_pre)
# 매각가 3구간 워터폴 — 참가적 1x(상한 없음) vs 비참가적 × 투자자 지분(풀 pre 20.0% / 풀 post 19.6%)
EXITS=[30,100,300]   # 억
def payout(exit_b, inv_share, participating):
    inv_pref=12.0
    if participating: inv=inv_pref+inv_share*(exit_b-inv_pref); rest=exit_b-inv
    else:
        conv=inv_share*exit_b; inv=max(inv_pref,conv); rest=exit_b-inv
    return inv, rest
WATERFALL=[]
for label,share,part,fnd in [("비참가적 · 풀 post",inv_post,False,fnd_post),("비참가적 · 풀 pre",inv_pre,False,fnd_pre),("참가적 1x · 풀 post",inv_post,True,fnd_post),("참가적 1x · 풀 pre",inv_pre,True,fnd_pre)]:
    row=[]
    for e in EXITS:
        inv,rest=payout(e,share,part)
        fnd_take=rest*fnd/(1-share)   # 잔여를 보통주(창업자+풀)가 나눔 — 풀은 전량 부여·행사 가정(보수적)
        row.append((inv,fnd_take))
    WATERFALL.append((label,row))
K02_ACTUAL=[(e,)+payout(e,0.20,True)+(payout(e,0.20,True)[1]*0.72/0.80,) for e in EXITS]   # 실제 K-02: 추가 풀 없음, 창업자 72%·풀 8%
REDEMPTION=[(y,12*1.03**y) for y in (1,3,5)]
DRAG=dict(threshold=0.60,nodle=0.20,kang=0.36,note="노들 + 강민수 = 56% < 60%: 창업자 둘 이상이 함께해야 발동 · 창업자 3인 72%만으로는 발동 가능(투자자 동의 조항 없으면)")

# ── 7. 현금 흐름 D+120 → D+300 [추가 설정 — G-15 15.4억/22개월에 맞춤] ──────────
CASH_D120=5405            # Day5: D+90 8,635 − 1개월 3,230
INFLOWS=[(165,10000,"초기창업패키지 선정 1억 [추가 설정]"),(150,20000,"노들 선투자 2억(시드 시 RCPS로 전환 — 12억에 포함)"),(179,100000,"시드 잔여 납입 10억"),(217,50000,"TIPS 1차년도 5억(8억 중) [추가 설정]"),
         (240,300+135,"세영정공 구축비 300 + 첫 달 SaaS 135"),(260,400+135,"태산정밀 구축비 400 + SaaS 135"),(270,270,"11월 SaaS(세영·태산)"),(275,500+135,"동보프레스 구축비 500 + SaaS 135"),(297,405,"12월 SaaS 3사")]
BURN_MONTHLY=[(149,3900,"7월 — 7명(개발 2 합류)"),(180,4200,"8월 — 7명 + 클라우드 증가"),(210,5500,"9월 — 10명 + 성수 12석 이전(일회성 400)"),(240,6300,"10월 — 11명(조현우 −, 세일즈 +) + 이전 잔금 600"),(270,6300,"11월 — 12명"),(300,6900+570,"12월 — 12명 + 청구서 초과 570")]
def cash_path():
    events=sorted([(d,a,s) for d,a,s in INFLOWS]+[(d,-a,s) for d,a,s in BURN_MONTHLY],key=lambda x:(x[0],-x[1]))
    c=CASH_D120; out=[(120,c,"시작")]
    for d,a,s in events: c+=a; out.append((d,c,s))
    return out
PATH=cash_path(); CASH_D300=PATH[-1][1]; RUNWAY_D300=CASH_D300/BURN_D300
CASH_MIN=min(c for d,c,s in PATH if d<150)

# ── 8. 사전등록 — 최소 표본 (X-07 조도 경고: 재촬영률 18% → 8%, α .05 양측, power .8) ─────
def n_two_prop(p1,p2,za=1.96,zb=0.84):
    pbar=(p1+p2)/2; return math.ceil((za*math.sqrt(2*pbar*(1-pbar))+zb*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2/(p1-p2)**2)
N_X07=n_two_prop(0.18,0.08)          # 177/arm → 200 사진씩
EXPERIMENTS={
 "X-04":dict(name="판정 초안 베타 — 세영 오전 1라인",assump="A-05b, A-11",oec="초안 수용률(수정 없이 승인) ≥ 70% 그리고 회피 행동(재촬영·별도 메모) < 10%",n="판정 600건(검사원 3 × 시간대 2 × 100 · 설계효과 3 반영)",when="D+290 고정",stop="회피 행동 20% 초과 시 즉시 중단(초안 OFF)",result="수용률 71% ✓ / 회피 행동 14% ✗(10~20%) → 불확정 — 초안 유지, A-05b 열어 둠 [추가 설정]"),
 "X-05":dict(name="라인 과금 수용 — 파일럿 3사 유료 전환",assump="A-06",oec="계약 라인 ÷ 실사용 라인 ≥ 0.8 그리고 좌석 단위 요구 0건",n="3사 전수",when="각 사 유료 전환일",stop="1사라도 좌석 과금 요구 시 ㉘ 항목 1 재검토",result="3/3 라인 계약(각 3라인) · 좌석 요구 0 → 성공. 단 태산 실사용 2 예상(계약 3 / 실사용 2.4 평균, G-18)"),
 "X-06":dict(name="온보딩 2주 — 마스터 매핑",assump="A-08",oec="마스터 매핑 완료까지 영업일 ≤ 10",n="3사 전수(마스터 217 · 62 · 183개)",when="각 사 계약 후 15영업일",stop="1사라도 20일 초과 시 B-05 재설계",result="세영 9일 · 태산 6일(62항목) · 동보 10일 → 3/3 성공"),
 "X-07":dict(name="조도 경고 효과 — 오후 재촬영률",assump="A-02(부분)",oec="오후 3시 이후 재촬영률 18% → 8% 미만",n=f"arm당 {N_X07} → 200 사진(오전 대조군 동수)",when="D+280 고정 · SRM: 오전/오후 사진 비율 55:45 ± 5",stop="경고 표시 후 기록 시간 +5분 이상이면 중단",result="오후 재촬영률 18% → 9.4%(경고 ON) vs 17.1%(OFF), n 212/208, SRM 통과 → 불확정(8% 이상·12% 미만) — 경고 유지, 오후 라인 판정 초안 제외 유지"),
}
GATES=[("알파","D+200","내부 + 세영 1라인 · 기록 자동 생성 성공률 ≥ 90% · 앱 크래시 0건/주 · 마스터 매핑 완료","CTO"),
       ("베타","D+240","3사 전 라인 · 검사원 기록 시간 ≤ 25분/일(X-01 재현) · 오전 OCR ≥ 90% · 재촬영률 < 15% · 판정 초안은 세영 오전 1라인만(X-04)","CPO"),
       ("GA","D+300","유료 3사 · eval v1 측정 완료 · 오류 예산 정책 가동 · 판정 초안 HITL(승인 필수) · 자동판정 OFF · 초안 미합격 시 '합격 전 베타' 표시","CEO(전원)")]

if __name__=="__main__":
    print("== 시점 (요일 = D+n mod 7)"); [print(f"  D+{d:<3} {DATES.get(d,''):<10} {wd(d)}  {s}") for d,s in MILESTONES]
    print(f"\n== 백로그 {len(BACKLOG)}건 합계 {TOTAL_MM} mm  MoSCoW {dict(MOSCOW)}")
    print(f"  v1.0 가용 {CAP_V10}: Must {MOSCOW['Must']} ({must_ratio_v10:.1%}) + Should {MOSCOW['Should']} + 예비 {reserve_v10} = {in_appetite_v10}  → 범위 밖 Could {MOSCOW['Could']} · Won't {MOSCOW[chr(87)+'on'+chr(39)+'t']}")
    print("  손실 분해 24 → 17:"); [print(f"    −{v:.1f}  {k}") for k,v in LOSS]
    print(f"  v1.1 가용 {CAP_V11}: 완료 {done_mm} + WIP {sum(WIP_KEPT.values()):.1f} + 예비 사용 {reserve_used} + 남은 유효 {remaining_eff}")
    print(f"  v1.1 Must 총량 {must_total_v11:.1f} = {must_ratio_v11:.1%} (> 60%) · 남은 {remaining_eff}: Must {rem_must} / Should {rem_should} / 예비 {rem_res}")
    print(f"\n== eval v1 (60건 = 3세트 × 20 · 판정 단위 {N_ITEMS:,} · 불량 {N_DEFECT} / 양품 {N_GOOD:,} · 치수 {N_DIM:,} · 외관 {N_APPEAR})")
    print(f"  OCR {OCR_OK}/{N_DIM} = {OCR_RATE:.1%} · FN {FN_CNT}/{N_DEFECT} = {FN_RATE:.1%} · FP {FP_CNT}/{N_GOOD} = {FP_RATE:.1%} · 외관 F1 {F1:.3f} (P {prec:.3f} R {rec:.3f})")
    print(f"  합격 기준 v1 FN ≤ {CRITERIA_V1['FN']} & OCR ≥ {CRITERIA_V1['OCR']} → FN {'합격' if PASS_V1['FN'] else '불합격(0.1%p)'} / OCR {'합격' if PASS_V1['OCR'] else '불합격'}")
    print("\n== UE v1"); [print(f"  {k}: 추론 {v['infer']:.1f} · 변동원가 {v['var']:.1f}만 · 매출 {v['rev']:.0f}만 · 변동원가율 {v['var_rate']:.1%} · 공헌이익률 {v['cm']:.1%}") for k,v in UE_OUT.items()]
    print(f"  청구서 예상 {BILL_EXPECTED} → 실제 {BILL_ACTUAL} (초과 {BILL_EXCESS}, 동보 {HEAVY_EXCESS} = {HEAVY_SHARE:.0%}) · 동보 초과 ÷ 원가표 {HEAVY_MULT:.2f}배 · 서비스별 {BILL_BY_SERVICE}")
    print(f"  매출 D+300: 순SaaS ARR {SAAS_ARR:,} · 구축비 {SETUP:,} · 계약 총액 {CONTRACT_TOTAL:,} · MRR {MRR_CONTRACT:.0f}/{MRR_SAAS:.0f} · ACV {ACV_CONTRACT:.0f}/{ACV_SAAS:.0f} · AI 원가율 {AI_RATIO_CONTRACT:.1%}/{AI_RATIO_SAAS:.1%} · GM {GM_IR:.0%} (12월 실제 청구서 반영 시 {GM_DEC_ACTUAL:.0%}) · 책임 한계 {LIABILITY_CAP:.0f}만 · burn multiple {BURN_MULTIPLE:.2f}")
    print(f"\n== 캡테이블 T1 (주당 {PRICE:,.0f}원 · FD {FD1:,}):",{k:f"{v:,} ({PCT1[k]:.1%})" for k,v in T1.items()})
    print(f"  풀 10% 요구 시 — post 기준: 투자자 {inv_post:.2%} 창업자 {fnd_post:.2%} / pre 기준: 투자자 {inv_pre:.0%} 창업자 {fnd_pre:.0%} (주당 {price_pre:,.0f}원)")
    print("  워터폴 (억): 투자자 / 창업자 3인 —",EXITS); [print(f"    {l:<18}",["%.1f / %.1f"%x for x in r]) for l,r in WATERFALL]
    print("    실제 K-02(추가 풀 없음, 참가적):",["%d억: 투자자 %.1f / 창업자 %.1f"%(e,i,f) for e,i,_,f in K02_ACTUAL])
    print(f"  상환권 12억 × 1.03^n: {[(y,round(v,2)) for y,v in REDEMPTION]} · drag: {DRAG['note']}")
    print("\n== 현금 D+120 → D+300 (만원)"); [print(f"  D+{d:<3} {c:>9,.0f}  {s}") for d,c,s in PATH]
    print(f"  D+300 {CASH_D300/10000:.2f}억 / 런웨이 {RUNWAY_D300:.1f}개월 (정본 G-15: 15.4억 / 22) · 최저점 D+150 직전 {CASH_MIN:,.0f}만")
    print(f"\n== 사전등록 X-07 최소 표본 {N_X07}/arm · 게이트 {[g[0]+' '+g[1] for g in GATES]}"); [print(f"  {k}: {v['result']}") for k,v in EXPERIMENTS.items()]
