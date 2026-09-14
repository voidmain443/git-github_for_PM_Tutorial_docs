# -*- coding: utf-8 -*-
"""Day7 (PMF 추적 D+300~600, 데이터 일자 2027-10-23) — [추가 설정] 숫자 정본과 검산.  워크북 §X.5·교재·그림·슬라이드는 이 스크립트의 출력만 인용한다.
정본(고정): 공통/가상회사_딥게이지.md §3.3(PMF 표·CAC 표), §4.5~4.9(사건), §7.1 G-01~24·G-41 D+600 열, §7.2 코호트 3장, §7.3 V v2, G-40.
실행: python3 day7_pmf.py"""
import math

# ── 0. 시점 (D+n 요일 = n mod 7, 0=월) ─────────────────────────────────
def wd(n): return "월화수목금토일"[n%7]
DATES={300:"2026-12-27",330:"2027-01-26",345:"2027-02-10",360:"2027-02-25",400:"2027-04-06",410:"2027-04-16",420:"2027-04-26",450:"2027-05-26",470:"2027-06-15",480:"2027-06-25",
       520:"2027-08-11",521:"2027-08-12",525:"2027-08-16",540:"2027-08-31",560:"2027-09-20",590:"2027-10-13",598:"2027-10-21",600:"2027-10-23"}
MILESTONES=[(300,"GA · 유료 3사 · 12명 · 판정 초안은 세영 오전 1라인 '합격 전 베타'"),
 (330,"서영채 — 월간 보고의 '계약 ARR' 표기 첫 지적 [정본 4.5]"),(345,"초안 표시 전 라인 확대(X-04 불확정 상태) · 신규 6개월 30% 프로모션 시작 [추가 설정]"),
 (360,"TIPS 운영사 조건 '유료 5개사' 달성(6개사) — B-18 온프렘 재검토 조건 충족 [추가 설정]"),(400,"강지우 CS 리드 합류 [정본 §6.1]"),
 (410,"자동판정 모드 출시(기본 OFF) — B-17 재검토 조건 미충족 상태(FN 8.1 미합격·X-04 회피 14%) [추가 설정]"),(420,"NDR 기준 시점 — 유료 17개사 [추가 설정]"),
 (450,"첫 PM 채용 공고 — 후보 3명(연봉 7,200~9,000만 + 옵션 0.4%) [정본 §3.3]"),(470,"[세영정공] 박선재 — '오후 3시 이후 크랙 놓친다' 팀장에게 구두 보고, 기록 없음 [정본 §2.3]"),
 (480,"세영정공 라인 2 신입 검사원(교대) 입사 [추가 설정]"),(520,"**사고** — 2027-08-11(수) 15:40 세영정공 라인 2, 크랙 → 양품(FN), 로트 2,400개 H사 납품 [정본 4.6]"),
 (521,"H사 선별 통보 · 세영 정미영 '우리 검사원은 시스템이 통과시킨 걸 믿었다'"),(525,"세영정공 청구 2,700만 + 해지 통보 · 계약 책임 한계 162만 [정본 4.6·G-40]"),
 (540,"eval v2 — FN 8.1→2.4 / FP 14.6→21.3 / 단가 32→67 / 지연 1.8→4.3 · 합격 기준 개정(FN ≤ 3.0 & OCR ≥ 95) [정본 4.7]"),
 (560,"강지우 메일 — 채택률 분모 3종 22 / 14 / 38% [정본 4.8]"),(590,"아웃바운드 채널 중단(payback 28.9개월) → 순소진 6,200만 [추가 설정]"),
 (598,"서영채 메일 — 'ARR 4.9억 중 1.1억이 구축비·컨설팅비' [정본 4.5]"),(600,"데이터 일자 2027-10-23(토) · 21명 · 유료 31 · 현금 6.82억")]
BASE_DAY=600

# ── 1. D+600 정본 지표 (G) ───────────────────────────────────────────
HEADCOUNT=dict(총=21,개발=11,세일즈=4,CS=3,경영지원=3); assert sum(v for k,v in HEADCOUNT.items() if k!="총")==21
CUSTOMERS=31; ACQUIRED=38; CHURNED=7; assert ACQUIRED-CHURNED==CUSTOMERS
ARR_CONTRACT=49000; SETUP=11000; ARR_SAAS=38000                       # 만원 (G-03~05)
MRR_CONTRACT=ARR_CONTRACT/12; MRR_SAAS=ARR_SAAS/12                    # 4,083 / 3,167
ACV_CONTRACT=ARR_CONTRACT/CUSTOMERS; ACV_SAAS=ARR_SAAS/CUSTOMERS       # 1,581 / 1,226
AI_COST=1340; AI_RATIO_C=AI_COST/MRR_CONTRACT; AI_RATIO_S=AI_COST/MRR_SAAS   # 32.8% / 42.3%
COGS_OTHER=250; COGS=AI_COST+COGS_OTHER                               # [추가 설정] 호스팅·STT·저장·온보딩 인건비 일부
GM_IR=(MRR_CONTRACT-COGS)/MRR_CONTRACT; GM_CHECK=(MRR_SAAS-COGS)/MRR_SAAS   # 61% / 49.8%
assert round(MRR_CONTRACT)==4083 and round(MRR_SAAS)==3167 and round(ACV_CONTRACT)==1581 and round(ACV_SAAS)==1226
assert round(AI_RATIO_C*100,1)==32.8 and round(AI_RATIO_S*100,1)==42.3 and round(GM_IR*100)==61 and round(GM_CHECK*100,1)==49.8
BURN=6200; NNARR_Q=9000; BURN_MULT=BURN*3/NNARR_Q; EFF=NNARR_Q/(BURN*3)   # 2.07 / 0.48
CASH=68200; RUNWAY=CASH/BURN                                          # 6.82억 / 11
assert round(BURN_MULT,2)==2.07 and round(EFF,2)==0.48 and round(RUNWAY)==11
LINES_CONTRACT=3.0; LINES_USED=1.6; ACTIVE_1M=0.68; ACTIVE_4M=0.41
ADOPT=dict(a=0.22,b=0.14,c=0.38)                                      # ㉮ AI 노출 건 / ㉯ 전체 검사기록 건 / ㉰ 활성 계정 처리 건 — 절대 건수 없음(F-08)
AUTO_ON=7; AUTO_OFF=24; assert AUTO_ON+AUTO_OFF==CUSTOMERS
# 명목 단가 vs 실효 단가 [추가 설정] — 3.8억 = 31사 × 3.0라인 × 실효단가 × 12
PRICE_NOMINAL=45.0; PRICE_EFFECTIVE=ARR_SAAS/(CUSTOMERS*LINES_CONTRACT*12); DISCOUNT=1-PRICE_EFFECTIVE/PRICE_NOMINAL   # 34.1만 · 24%
DISCOUNT_MIX=[("신규 6개월 30% 프로모션(D+345~, TIPS 5개사 시계)",0.30,14),("1차사 추천 채널 상시 15%",0.15,11),("12개월 선납 10%",0.10,9),("정가",0.0,6)]   # 고객 수 합 40 = 중복 허용 [추가 설정]

# ── 2. 코호트 3장 (정본 §7.2) ────────────────────────────────────────
NA=None
COHORTS={
 "Ret-C 자사":{"분모":"해당 분기 신규 유료 계약 로고","26Q4":[3,3,3,3,3,2,2,2],"27Q1":[14,14,14,13,12,11,10,10],"27Q2":[12,12,12,11,11,10,NA,NA]},
 "Ret-A 인쇄":{"분모":"계약 후 첫 달 말 30일 내 로그인 로고 = 활성 계정","26Q4":[4,4,4,4,4,4,3,3],"27Q1":[15,15,15,15,14,14,14,14],"27Q2":[18,18,18,17,17,17,NA,NA]},
 "Ret-A 재계산":{"분모":"총 신규 계약 로고(자사 정의)","26Q4":[6,6,6,5,4,4,3,3],"27Q1":[20,20,19,17,14,14,14,14],"27Q2":[24,24,22,19,17,17,NA,NA]},
 "Ret-B":{"분모":"자사와 동일","26Q4":[10,10,10,9,8,6,6,6],"27Q1":[22,22,21,19,17,15,13,13],"27Q2":[20,20,20,18,16,15,NA,NA]},
}
def pct(row,m): return None if row[m+1] is None else row[m+1]/row[0]   # row = [분모, M0..M6]
def last(row): v=[x for x in row if x is not None]; return v[-1]/row[0]
for name,exp in [("Ret-C 자사",(0.67,0.71,0.83)),("Ret-A 인쇄",(0.75,0.93,0.94)),("Ret-A 재계산",(0.50,0.70,0.71)),("Ret-B",(0.60,0.59,0.75))]:
    got=tuple(round(last(COHORTS[name][q]),2) for q in ("26Q4","27Q1","27Q2")); assert got==exp,(name,got)
M4={n:tuple(round(pct(COHORTS[n][q],4)*100) for q in ("26Q4","27Q1","27Q2")) for n in COHORTS}   # 자사 67/79/83 · A 인쇄 100/93/94 · A 재계산 67/70/71 · B 60/68/75
assert M4["Ret-C 자사"]==(67,79,83) and M4["Ret-A 재계산"]==(67,70,71) and M4["Ret-B"]==(60,68,75)
# 자사 유료 31 = 26Q4 잔존 2 + 27Q1 10 + 27Q2 10 + 27Q3 신규 9(M0~M1, 격자 밖) [추가 설정]
Q3_NEW=9; assert 2+10+10+Q3_NEW==CUSTOMERS and 3+14+12+Q3_NEW==ACQUIRED
# 이탈 7건 [추가 설정] — (코호트, 이탈 M, 고객, 유형, 사유)
CHURN=[("26Q4","M5","태산정밀","가치 미실현","실사용 2라인, 62항목 구조 유지 부담 — 라인 2로 축소 요청 거절 후 해지"),
       ("27Q1","M2","경일정공","미온보딩","검사원 1명 — 매핑 후 첫 달 기록 20건 미만, 팀장이 직접 촬영"),("27Q1","M3","미래오토","챔피언 이탈","도입 추진한 품질팀장 이직, 후임이 엑셀 복귀"),
       ("27Q1","M4","대양정밀","가치 미실현","배석 인터뷰(I-18) 공장 — 관리자 주도 도입, 검사원 회피 행동"),("27Q1","M5","신광기공","가격","MES 병행 — '둘 중 하나' 결정에서 MES 유지, 프로모션 종료 시점"),
       ("27Q2","M2","(익명 C13) 사출 2차","미온보딩","마스터 미제출 6주 — X-06 20일 초과 기준 첫 해당"),("27Q2","M3","(익명 C14) 절삭 3차","경쟁·대체","1차사 SQ 포털 자체 입력 모듈 개편 — '포털에서 되는데'")]
assert len(CHURN)==7
CHURN_TYPES={t:sum(1 for c in CHURN if c[3]==t) for t in ["미온보딩","챔피언 이탈","가치 미실현","가격","경쟁·대체"]}   # 2/1/2/1/1
# 세영정공: D+525 해지 통보 → 12월 갱신까지 유예, D+600 유료 31에 포함(협상 중) [추가 설정]
# GRR / NDR (G-16) — 기준 D+420 유료 17개사 MRR [추가 설정]
NDR_BASE_MRR=1530; NDR_CHURN=int(round(NDR_BASE_MRR*0.16)); NDR_EXP=int(round(NDR_BASE_MRR*0.13))
GRR=(NDR_BASE_MRR-NDR_CHURN)/NDR_BASE_MRR; NDR=(NDR_BASE_MRR-NDR_CHURN+NDR_EXP)/NDR_BASE_MRR   # 84% / 97%
assert round(GRR*100)==84 and round(NDR*100)==97
NDR_EXP_SRC=[("라인 증설(4~5라인 공장 5사)",int(round(NDR_EXP*0.7))),("Flow 애드온(8D·포털, 라인당 +8만, 6사 — D+450 도입)",NDR_EXP-int(round(NDR_EXP*0.7)))]
# 시드 5억 배분 판정 [추가 설정 — 워크북 ㉛ 항목 6]: 가상 — "세 회사 중 어디에 5억을 넣겠는가"
ALLOCATION=[("자사(Ret-C)",3.0,"27Q2 M4 83% · M4 추세 67→79→83 개선 · 분모 확인됨"),("익명 A",0.0,"판독 불가 — 분모(활성 계정) 확인 전까지 무배분. 재계산 시 50/70/71"),("익명 B",2.0,"60/59/75 · M4 60→68→75 개선 · 분모 자사와 동일"),]

# ── 3. 채널별 CAC · payback · LTV (정본 §3.3 표 + 추가 설정) ───────────────
CAC={"인바운드":310,"아웃바운드":1470,"1차사 추천":90,"blended":620}
def payback(cac,acv_monthly,gm=1.0): return cac/(acv_monthly*gm)
PAYBACK={}
for ch,c in CAC.items():
    PAYBACK[ch]=dict(ir=payback(c,ACV_CONTRACT/12),gm61=payback(c,ACV_SAAS/12,GM_IR),gm498=payback(c,ACV_SAAS/12,GM_CHECK))
assert round(PAYBACK["인바운드"]["ir"],1)==2.4 or round(PAYBACK["인바운드"]["ir"],2)==2.35   # IR 덱 "2.3"은 반올림 전 표기(정본 §3.3)
CANON_PAYBACK={"인바운드":(2.3,4.98,6.10),"아웃바운드":(10.9,23.60,28.93),"1차사 추천":(0.7,1.44,1.77),"blended":(4.6,9.95,12.20)}   # 정본 §3.3 표기(반올림 차 ±0.03)
for ch,(a,b,c) in CANON_PAYBACK.items(): assert abs(PAYBACK[ch]["gm61"]-b)<0.05 and abs(PAYBACK[ch]["gm498"]-c)<0.05,(ch,PAYBACK[ch])
ORGANIC=0.41; CAC_PAID=CAC["blended"]/(1-ORGANIC)                     # 1,051만 (G-41)
assert round(CAC_PAID)==1051
# LTV:CAC 세 계산 [추가 설정 — 가정 열거]
LIFE_IR_YEARS=3.75                                                    # IR 덱: 이탈 미반영, 관행 수명 45개월
LTV_IR=ACV_CONTRACT*GM_IR*LIFE_IR_YEARS; RATIO_IR=LTV_IR/CAC["blended"]          # 5.8
MONTHLY_LOGO_CHURN=0.0432                                             # 최근 6개월 가중 로고 이탈률 [추가 설정] — 27Q1 M6 29% · 27Q2 M4 17%에서
LIFE_CHECK_YEARS=1/MONTHLY_LOGO_CHURN/12                              # 1.94년
LTV_CHECK=ACV_SAAS*GM_CHECK*LIFE_CHECK_YEARS; RATIO_CHECK=LTV_CHECK/CAC["blended"]   # 1.9
RATIO_PAID=LTV_CHECK/CAC_PAID                                         # 1.12
assert round(RATIO_IR,1)==5.8 and round(RATIO_CHECK,1)==1.9 and round(RATIO_PAID,2)==1.12

# ── 4. 현금 D+300 → D+600 [추가 설정 — G-15 6.82억 · G-11 6,200에 맞춤] ───────
CASH_D300=154015
BURN_PATH=[("1월",7400,"13명 · 프로모션 시작"),("2월",7900,"15명"),("3월",8300,"17명 · 세일즈 4"),("4월",8700,"강지우 · 자동판정 모드"),("5월",9100,"19명 · 마케팅"),("6월",9400,"21명"),
           ("7월",9600,"2-pass 실험 원가"),("8월",9900,"사고 대응 · eval v2 원가 2.1배"),("9월",9300,"신규 채용 동결"),("10월",6200,"아웃바운드 중단(D+590) · 순SaaS MRR 3,167")]
CASH_D600=CASH_D300-sum(b for _,b,_ in BURN_PATH)
assert abs(CASH_D600-CASH)<300, CASH_D600
# TIPS 2차년도 3억은 1차년도 평가 후 D+620(2027-11) 집행 예정 — 이 구간 밖 [추가 설정]

# ── 5. eval v1 → v2 (DS-v1 동일: 1,480항목 · 불량 296 · 양품 1,184 · 치수 1,050 · 외관 결함 96) ────
N_DEFECT=296; N_GOOD=1184; N_DIM=1050; APPEAR_DEFECT=96
V1=dict(ocr=960,fn=24,fp=173,tp_ap=76,fn_ap=20,fp_ap=23,lat=1.8,cost=32)
V2=dict(ocr=1000,fn=7,fp=252,tp_ap=89,fn_ap=7,fp_ap=27,lat=4.3,cost=67)
def rates(v):
    p=v["tp_ap"]/(v["tp_ap"]+v["fp_ap"]); r=v["tp_ap"]/(v["tp_ap"]+v["fn_ap"])
    return dict(OCR=v["ocr"]/N_DIM,FN=v["fn"]/N_DEFECT,FP=v["fp"]/N_GOOD,F1=2*p*r/(p+r),P=p,R=r)
R1=rates(V1); R2=rates(V2)
assert (round(R1["FN"]*100,1),round(R1["FP"]*100,1),round(R1["OCR"]*100,1),round(R1["F1"],2))==(8.1,14.6,91.4,0.78)
assert (round(R2["FN"]*100,1),round(R2["FP"]*100,1),round(R2["OCR"]*100,1),round(R2["F1"],2))==(2.4,21.3,95.2,0.84),R2
assert V2["fn_ap"]==V2["fn"]   # v2의 FN 7건은 전부 외관(크랙) — 치수 FN 0
CRITERIA_V1="FN ≤ 8.0% & OCR ≥ 90% on DS-v1"; CRITERIA_V2="FN ≤ 3.0% & OCR ≥ 95% on DS-v1 (D+540 개정 — 데이터셋 변경 없음, 오후 조도 세트 미추가)"
COST_MULT=V2["cost"]/V1["cost"]; LAT_MULT=V2["lat"]/V1["lat"]         # 2.09 / 2.39
AI_COST_V1_EQUIV=int(round(AI_COST/COST_MULT))                        # v1 단가였다면 월 640만 [추가 설정 — 참고]
# ── 6. 사고 INC-01 [추가 설정 — 정본 4.6·G-36·G-40] ──────────────────────
INCIDENT=dict(id="INC-01",when="2027-08-11(수) 15:40",where="[세영정공] 라인 2(교대 조, 신입 검사원 D+480 입사)",part="브래킷 크랙(외관)",lot=2400,claim=2700,claim_split="선별 1,100 + 특별운송 400 + 페널티 1,200(G-36)",
              liability=162,acv=1620,conf=0.87,threshold=0.85,glare="조도 경고 표시됨 — 재촬영 건너뜀(1탭)",log="라인 2 FN 신호 3개월 0건(검사원이 초안을 뒤집은 적 없음) — 예산이 놓치는 FN",
              warning="D+470 박선재 구두 보고 '오후 3시 이후 크랙 놓친다' — 기록 없음",quote="[세영정공] 정미영: '우리 검사원은 시스템이 통과시킨 걸 믿었다' — GAUGE 로그가 근거")
INC_TIMELINE=[("08-11 15:40","라인 2 검사 — 초안 '양품'(신뢰도 0.87), 조도 경고 표시, 재촬영 생략, 검사원 승인","신입 검사원","판정 로그 B-12"),
              ("08-11 17:10","로트 2,400개 출하 → H사 납품","세영 출하팀","출하 전표"),("08-12 09:30","H사 수입검사 크랙 발견, 선별 착수 → 세영 통보","H사 SQE 김도윤","H사 통보서"),
              ("08-12 11:00","세영 정미영 → 딥게이지 강민수 전화 · 로그 요청","강민수","통화 기록"),("08-12 14:00","내부 통보 · 판정 로그 추출(초안 양품·승인·조도 경고 플래그)","오세진·강지우","로그 덤프"),
              ("08-12 16:00","임시 조치 — 전 고객 오후 3시 이후 판정 초안 표시 OFF · 자동판정 ON 7사 전원 OFF 권고","오세진","공지 메일"),("08-16","세영 청구 2,700만 + 해지 통보 접수 · 계약 책임 한계 162만 회신 보류","강민수","공문"),
              ("08-31 (D+540)","eval v2 — 2-pass 도입, FN 2.4% · 합격 기준 개정","오세진","eval 리포트 v2")]
POSITIONS=[("전액 2,700만","고객 관계 유지 · 시리즈A 전 레퍼런스 보호 / 계약 문구 무력화 선례 · 현금 2,700","—"),("계약 한계 162만","문구 방어 · 선례 유지 / 해지 확정·레퍼런스 손실·1차사(김도윤) 채널 영향","—"),
           ("중간 — 162만 + 6개월 무상 + 재발 방지 증빙","문구는 지키고(책임 상한 그대로) 신뢰 복구는 서비스로 / 세영이 '사과 = 책임 인정'으로 읽을 위험","선택")]
# 오류 예산 개정 [추가 설정]
BUDGET_V1=dict(fn="≤ 8.0%(라인별, HITL 수정 로그)",fp="≤ 15%",thr="0.85",auto="기능 없음 → D+410 기본 OFF",action="라인 초안 OFF → 재학습 → 재측정 → ON")
BUDGET_V2=dict(fn="≤ 3.0% + **FN 신호 0건 라인은 '미감시'로 표기**(뒤집힌 적 없음 = 안전이 아니라 무신호)",fp="≤ 15% 유지 — v2 21.3%는 예산 초과 상태로 출발",thr="0.85 → 0.90 (오후 조도 사진은 0.95)",auto="기본 OFF 고정 · ON은 FP 예산 충족 라인만",action="유지 + 오후 조도 세트 DS-v2 측정 합격 전 오후 초안 OFF")

# ── 7. North Star 후보 3 [추가 설정] ──────────────────────────────────────
WEEKLY_RECORDS=int(round(CUSTOMERS*LINES_USED*250)); ACTIVE_LINES=int(round(CUSTOMERS*LINES_USED))   # 12,400 · 50
NS=[("NS-1 주간 승인 검사기록 건수(검사원이 승인한)",f"{WEEKLY_RECORDS:,}건/주","31사 × 실사용 1.6라인 × 250건","빈 기록 승인·자동판정 확정 건 포함 → 분자를 '수정 없이 승인 + 수정 승인'으로 한정, 자동판정 확정 건 제외"),
    ("NS-2 활성 라인 수(주 100건 이상 기록)",f"{ACTIVE_LINES}라인","계약 93 중 실사용 50","라인 정의 느슨(1라인을 2로 등록) → 라인 = 검사기준서 단위로 고정"),
    ("NS-3 자동판정 채택 건수","비율만 — 22 / 14 / 38%(절대 건수 없음)","㉮㉯㉰","임계값을 낮추면 채택 ↑ FP ↑ → 채택률은 North Star가 아니라 가드레일")]
INPUTS=[("실사용 라인 수(주 100건 이상)","50 / 계약 93(31사 × 3.0)","측정 가능","박정우·강지우","70"),("검사원 계정 활성률(4개월)","41%(1개월 68%)","측정 가능","강지우","55%"),
        ("온보딩 완료율(매핑 ≤ 10영업일 & 첫 달 100건)","27Q2 코호트 10/12","측정 가능","이수민","11/12"),("판정 초안 수용률(수정 없이 승인 ÷ 노출)","22%(㉮)","측정 가능","오세진","30%"),
        ("부적합 통보 리드타임(발생 → 포털 제출)","추정 1.4일(자기 보고)","추정 — 포털 제출 시각 미수집","윤하경","측정 체계 먼저")]

# ── 8. 로드맵·예산 3분리 [추가 설정] ──────────────────────────────────────
DEV=11; QUARTER_MM=DEV*3; RESERVE=0.25
BUDGET_SPLIT=[("차별화",35,"Flow 애드온 확장 · 포털 규격 2종 · 사용량 계측 → 공정 사용 시행"),("위생",30,"기술 부채 · 보안(ISMS 준비) · 온프렘 검토(CR-044) · 2-pass 원가 최적화"),("신뢰 복구",35,"DS-v2 오후 조도 세트 · 수정 로그 감시 대시보드 · 미감시 라인 표기 · HITL 재설계 · 온보딩 개선")]
assert sum(b for _,b,_ in BUDGET_SPLIT)==100
ROADMAP=[("Now","DS-v2 오후 조도 세트 20건 + 오후 라인 재측정","OP-05 / A-02","X-07 · INC-01","M","합격 전 오후 초안 OFF 유지"),("Now","수정 로그 감시 대시보드 — FN 신호 0건 라인 '미감시' 표기","OP-04","INC-01","S","전 라인 주간 리포트"),
         ("Now","온보딩 개선 — 첫 달 100건 미만 자동 알림 · 이수민 현장 2회","A-08 / OP-01","X-06 · 이탈 미온보딩 2","S","27Q3 코호트 M2 ≥ 90%"),("Now","사용량 계측(사진 단위 재촬영·재시도·배치 태그)","㉘ 항목 4","청구서 780만","S","1월 데이터로 H1~H4 판별"),
         ("Next","공정 사용 조항 시행(신규·갱신) + 경고 임계값","㉘ 항목 4","계측 결과","S","H1~H4 판별 후"),("Next","Flow 애드온 확장(8D D4 초안·포털 규격 K사)","OP-02·03","NDR 확장 13% 중 Flow 비중","M","활성률 55% 도달 후"),
         ("Next","자동판정 ON 조건 재정의 — FP 예산 충족 라인만","OP-05","eval v2 FP 21.3","S","FP ≤ 15% 라인"),("Later","온프렘 배포 패키지 — CR-044","OP-07","B-18 재검토 조건 충족(D+360)","L","CR-044 판정 · 시리즈A 후"),
         ("Later","MES 연동 · 검사원 교육 모드","OP-01 / A-01","—","M","다음 사이클")]
WONT_UPDATE=[("B-17","자동판정 모드","승격(D+410) — 재검토 조건 미충족 상태에서 출시, 사후 기록","기본 OFF 고정 · ON 조건 FP 예산 충족 라인만 — ㉞ 항목 7"),("B-18","온프렘 배포","재검토 → CR-044 진술 패킷","유료 5개사 달성(D+360)으로 조건 충족 · 판정은 이 문서 항목 5"),
             ("B-21","MES 연동","유지","이탈 1건(신광기공) 사유이나 '둘 중 하나' 구조 — 조건 미충족"),("B-22","관리자 대시보드","승격 → Now(감시 대시보드로 재정의)","INC-01 재발 방지 — 엑셀 내보내기로는 감시 불가"),
             ("신규","오후 조도 판정 초안","Won't(DS-v2 합격 전)","INC-01"),("신규","'AI 검사' 마케팅 문구","Won't 유지","㉕ 항목 6-3 — 사고 후 재확인")]
CR044=dict(title="CR-044 검사 AI 온프렘 전환(H사 계열 3사 + 1차사 채널)",requester="박정우(세일즈) · 김도윤(H사 SQE, 공문)",evidence="파이프라인 40사 중 온프렘 요구 12사 · 도면 미업로드 모드로 해소 5사 · 잔여 7사 — 1차사 채널 계약 조건 '온프렘 또는 전용망'",
           benefit="7사 × 3라인 × 34.1만 × 12 = 8,600만 ARR + 1차사 채널 CAC 90만",cost="B-18 6.0 mm + 운영 0.7 FTE(연 5,600만) + GPU 2대 + 릴리스 분기 1회 → 순SaaS ARR 8,600만에 원가 5,600만",
           giveup="Flow 애드온 확장(M) 또는 포털 규격 2종 — 차별화 35%에서",decision="판정 요청: '보류 — 시리즈A 후 재검토, 1차사 채널 계약서 서명 시 즉시 착수' · 시한 D+660")

if __name__=="__main__":
    print("== 시점"); [print(f"  D+{d:<3} {DATES.get(d,''):<10} {wd(d)}  {s}") for d,s in MILESTONES]
    print(f"\n== D+600: {HEADCOUNT} · 유료 {CUSTOMERS}(획득 {ACQUIRED} − 이탈 {CHURNED}) · ARR 계약 {ARR_CONTRACT:,} / 순SaaS {ARR_SAAS:,}(구축비 {SETUP:,}) · MRR {MRR_CONTRACT:,.0f}/{MRR_SAAS:,.0f} · ACV {ACV_CONTRACT:,.0f}/{ACV_SAAS:,.0f}")
    print(f"  AI 원가 {AI_COST:,} = {AI_RATIO_C:.1%}/{AI_RATIO_S:.1%} · COGS {COGS:,} → GM {GM_IR:.0%}/{GM_CHECK:.1%} · 순소진 {BURN:,} · burn multiple {BURN_MULT:.2f} · efficiency {EFF:.2f} · 현금 {CASH/10000:.2f}억/{RUNWAY:.0f}개월")
    print(f"  명목 {PRICE_NOMINAL}만 vs 실효 {PRICE_EFFECTIVE:.1f}만/라인/월 (할인 {DISCOUNT:.0%}) · 계약 라인 {LINES_CONTRACT}/실사용 {LINES_USED} · 활성률 {ACTIVE_1M:.0%}→{ACTIVE_4M:.0%} · 채택률 {ADOPT} · 자동판정 ON {AUTO_ON}/OFF {AUTO_OFF}")
    print("\n== 코호트 M4 동일 연령:",M4); print("  이탈 7:",CHURN_TYPES); print(f"  GRR {GRR:.0%} / NDR {NDR:.0%} (기준 D+420 17사 MRR {NDR_BASE_MRR:,} · 이탈 {NDR_CHURN} · 확장 {NDR_EXP} = {NDR_EXP_SRC})")
    print("\n== payback (IR 매출기준 / GM 61% / GM 49.8%):"); [print(f"  {ch:<8} CAC {c:>5} → {PAYBACK[ch]['ir']:.2f} / {PAYBACK[ch]['gm61']:.2f} / {PAYBACK[ch]['gm498']:.2f}") for ch,c in CAC.items()]
    print(f"  유료 획득 CAC {CAC_PAID:,.0f} · LTV:CAC — IR {RATIO_IR:.1f}(ACV {ACV_CONTRACT:,.0f}·GM {GM_IR:.0%}·수명 {LIFE_IR_YEARS}년·CAC 620) / 검산 {RATIO_CHECK:.1f}(ACV {ACV_SAAS:,.0f}·GM {GM_CHECK:.1%}·월 이탈 {MONTHLY_LOGO_CHURN:.1%}→{LIFE_CHECK_YEARS:.2f}년) / 유료 CAC {RATIO_PAID:.2f}")
    print(f"\n== 현금 {CASH_D300/10000:.2f}억 → {CASH_D600/10000:.2f}억 (소진 합 {sum(b for _,b,_ in BURN_PATH):,})")
    print(f"\n== eval v1→v2: OCR {R1['OCR']:.1%}→{R2['OCR']:.1%} · FN {V1['fn']}/{N_DEFECT}={R1['FN']:.1%}→{V2['fn']}/{N_DEFECT}={R2['FN']:.1%} · FP {V1['fp']}→{V2['fp']}/{N_GOOD}={R2['FP']:.1%} · F1 {R1['F1']:.2f}→{R2['F1']:.2f}(P {R2['P']:.3f} R {R2['R']:.3f}) · 단가 ×{COST_MULT:.2f} 지연 ×{LAT_MULT:.2f} · v1 단가면 월 {AI_COST_V1_EQUIV}만")
    print(f"  사고 {INCIDENT['when']} {INCIDENT['where']} · 청구 {INCIDENT['claim']:,} vs 책임 {INCIDENT['liability']} · 신뢰도 {INCIDENT['conf']}")
    print(f"\n== North Star 후보 현재값: {[(n[0][:12],n[1]) for n in NS]} · 개발 {DEV}명 분기 {QUARTER_MM} mm · 예산 {BUDGET_SPLIT}")
