# Day3 워크북 ⑫ 성과보고 검산 스크립트 — data date 2026-09-30
# PV는 Day2 워크북 §4.5 월별 PV 표(정본). EV·AC는 Day3 시나리오 [추가 설정].
months = ["2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07","2026-08","2026-09"]
cats = ["SI","상용SW","인프라","단말","전환","시험감리","PMO"]
PV = {
 "SI":     [2.50,2.50,4.46,3.93,3.93,3.93,3.93,5.89,3.93],
 "상용SW": [0,0,8.00,6.00,3.40,0.20,0.20,0.20,0.20],
 "인프라": [0,0,0,6.40,0.40,3.40,2.50,0.40,0.40],
 "단말":   [0]*9,
 "전환":   [0,0,0,0,0.60,0.80,0.90,1.00,1.00],
 "시험감리":[0,0,0,0.80,0,0,0,1.00,0],
 "PMO":    [0.56]*9,
}
# --- EV ---
# SI: 설계 스프린트 0/100(스프린트 리뷰 인수, 1.25/회), 구현 = 인수 FP/620 × 1.96 (진행 중 스프린트 0)
fp_accepted = {"2026-04":1240,"2026-05":1080,"2026-06":1030,"2026-07":1160,"2026-08":1240,"2026-09":1270}
# 스프린트별 인수 FP (S7~S18): 620,620 | 600,480 | 470,560 | 560,600 | 620,620 | 640,630
design_ev = [1.25,2.50,3.75,0,0,0,0,0,0]
SI_EV = [design_ev[i] + (fp_accepted.get(m,0)/620*1.96) for i,m in enumerate(months)]
EV = {
 "SI": SI_EV,
 "상용SW": [0,0,8.00,0,6.00,0.20,3.60,0.20,0.20],   # MDM2차·APM 6.0 → 5월 인도, SAP 애드온 3.4 → 7월 인도
 "인프라": [0,0,0,6.40,0.40,3.40,0.40,2.50,0.40],   # 망분리 2차 2.1 → 8월
 "단말":   [0]*9,
 "전환":   [0,0,0,0,0.60,0.85,0.95,1.05,1.05],       # O-01 활용, 매핑 소폭 선행
 "시험감리":[0,0,0,0.80,0,0,0,0,1.70],              # 보안진단 1회차 1.0 → 9월, 중간감리 1차 0.7 (G2 감리 1.4의 1/2) 9월 선행
 "PMO":    [0.56]*9,
}
# --- AC ---
# SI = 인수 FP 대금 발생(EV와 동일) + 컨틴전시 집행분(대기 비용 0.42 7월, R-07 재산정 0.15 6월, R-03 폴백 재시험 0.50 8월, CR-03 0.12 9월)
SI_AC = list(SI_EV)
SI_AC[5] += 0.15; SI_AC[6] += 0.42; SI_AC[7] += 0.50; SI_AC[8] += 0.12
AC = {
 "SI": SI_AC,
 "상용SW": [0,0,8.00,0,3.00,0.20,1.90,0.20,0.20],   # 50/50 지급 조건 → 인도 시 50%만 발생
 "인프라": [0,0,0,6.40,0.50,3.80,0.50,2.80,0.50],   # 클라우드 월 0.5(개발환경 초과), 망분리 3.3·2.3
 "단말":   [0]*9,
 "전환":   [0,0,0,0,0.60,0.80,0.90,1.00,1.00],       # 고정가 용역 월 청구 = 계획
 "시험감리":[0,0,0,0.80,0,0,0,0,1.75],
 "PMO":    [0.60]*9,
}
def cum(xs):
    out=[];s=0
    for x in xs: s+=x; out.append(s)
    return out
tot = lambda D: [sum(D[c][i] for c in cats) for i in range(9)]
PVm, EVm, ACm = tot(PV), tot(EV), tot(AC)
# PV 누적은 Day2 §4.5 표의 정본 값(원값 기준 누적)을 그대로 쓴다
PVc = [3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83]
EVc, ACc = cum(EVm), cum(ACm)
print("월  | PV월 EV월 AC월 | PV누 EV누 AC누 | SV CV SPI CPI")
for i,m in enumerate(months):
    print(f"{m} | {PVm[i]:6.2f} {EVm[i]:6.2f} {ACm[i]:6.2f} | {PVc[i]:7.2f} {EVc[i]:7.2f} {ACc[i]:7.2f} | {EVc[i]-PVc[i]:6.2f} {EVc[i]-ACc[i]:6.2f} {EVc[i]/PVc[i]:.3f} {EVc[i]/ACc[i]:.3f}")
print("\n항목별 누적(9월):")
for c in cats:
    print(f"  {c:6s} PV {sum(PV[c]):6.2f}  EV {sum(EV[c]):6.2f}  AC {sum(AC[c]):6.2f}  SV {sum(EV[c])-sum(PV[c]):6.2f}  CV {sum(EV[c])-sum(AC[c]):6.2f}")
BAC=145.80; LIMIT=156.00
pv,ev,ac = PVc[-1],EVc[-1],ACc[-1]
sv,cv=ev-pv,ev-ac; spi,cpi=ev/pv,ev/ac
print(f"\nBAC {BAC} / PV {pv:.2f} EV {ev:.2f} AC {ac:.2f} / SV {sv:.2f} CV {cv:.2f} SPI {spi:.3f} CPI {cpi:.3f}")
# 착시 조정: 라이선스 미발생 4.70 (6.0의 50% + 3.4의 50%)
ac_adj = ac + 4.70; cpi_adj = ev/ac_adj
print(f"발생주의 조정 AC {ac_adj:.2f} → CPI(조정) {cpi_adj:.3f}, CV(조정) {ev-ac_adj:.2f}")
# 측정 시차: S20(09-28 시작) PV 1.96 은 정상 진행에서도 EV 0
print(f"측정 시차 제거 SV {sv+1.96:.2f}, SPI(시차 제거) {ev/(pv-1.96):.3f}")
# EAC 4공식
eac1=BAC/cpi; eac2=ac+(BAC-ev); eac3=ac+(BAC-ev)/(cpi*spi)
# 상향식 ETC [추가 설정]
etc = {
 "SI 잔여 계약 (68.20-EV)": 68.20-sum(EV["SI"]),
 "SI 변경 대가 승인·예정 (+185 FP, 미반영)": 185*0.0055,
 "SI 대기 비용 잔여 추정": 0.18,
 "상용SW 잔여 PV 1.20 + 미발생 4.70": 1.20+4.70,
 "인프라 잔여 PV 7.40 × 1.07": 7.40*1.07,
 "단말 8.60 + 견적 상승 0.30": 8.90,
 "전환 잔여 (9.40-4.50) + 아카이브 정책 0.20": 9.40-4.50+0.20,
 "시험·감리 잔여 (9.70-2.50) + 부하시험 재견적 0.20": 9.70-2.50+0.20,
 "PMO 잔여 8개월 × 0.60": 8*0.60,
}
ETC=sum(etc.values()); eac4=ac+ETC
print("\nEAC1 BAC/CPI          =",round(eac1,2))
print("EAC2 AC+(BAC-EV)      =",round(eac2,2))
print("EAC3 AC+(BAC-EV)/(CPI*SPI) =",round(eac3,2))
for k,v in etc.items(): print(f"   ETC {k}: {v:.2f}")
print("ETC 합 =",round(ETC,2)," EAC4 AC+ETC =",round(eac4,2))
eac1a=BAC/cpi_adj; eac3a=ac_adj+(BAC-ev)/(cpi_adj*spi)
print(f"조정 CPI 기준: EAC1' {eac1a:.2f}, EAC3' {eac3a:.2f}")
for name,e in [("EAC1",eac1),("EAC2",eac2),("EAC3",eac3),("EAC4",eac4),("EAC3'",eac3a)]:
    print(f"  VAC({name}) = {BAC-e:6.2f}   vs 집행 한도 여유 {LIMIT-e:6.2f}")
tcpi_bac=(BAC-ev)/(BAC-ac); tcpi_lim=(BAC-ev)/(LIMIT-ac); tcpi_eac4=(BAC-ev)/(eac4-ac)
tcpi_bac_adj=(BAC-ev)/(BAC-ac_adj)
print(f"\nTCPI(BAC 145.8) {tcpi_bac:.3f} / TCPI(집행 한도 156.0) {tcpi_lim:.3f} / TCPI(EAC4) {tcpi_eac4:.3f} / TCPI(BAC, 조정 AC) {tcpi_bac_adj:.3f}")
# Earned Schedule
AT=9
n=max(i for i in range(9) if PVc[i]<=ev)  # 0-based month index where PVc<=EV
ES=(n+1)+(ev-PVc[n])/(PVc[n+1]-PVc[n])
svt=ES-AT; spit=ES/AT; PD=17; ieact=PD/spit
print(f"\nES = {n+1} + ({ev:.2f}-{PVc[n]:.2f})/({PVc[n+1]:.2f}-{PVc[n]:.2f}) = {ES:.2f}개월; AT 9; SV(t) {svt:.2f}개월; SPI(t) {spit:.3f}; IEAC(t)=17/SPI(t) = {ieact:.2f}개월 → +{ieact-17:.2f}개월 ≈ {(ieact-17)*21:.0f}영업일")
# 월별 SPI vs SPI(t)
print("\n월별 SPI / SPI(t):")
for i in range(9):
    e=EVc[i]
    if i==0: es=e/PVc[0]
    else:
        k=max(j for j in range(i+1) if PVc[j]<=e) if PVc[0]<=e else -1
        if k==i: es=i+1
        elif k<0: es=e/PVc[0]
        else: es=(k+1)+(e-PVc[k])/(PVc[k+1]-PVc[k])
    print(f"  {months[i]}  SPI {e/PVc[i]:.3f}   ES {es:.2f}  SPI(t) {es/(i+1):.3f}")
