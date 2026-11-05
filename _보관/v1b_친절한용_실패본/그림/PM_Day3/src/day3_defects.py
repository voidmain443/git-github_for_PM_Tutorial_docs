# Day3 워크북 ⑭ 품질 통제 — 주차별 결함 누적표 생성·검산 (2026-02-02 ~ 2026-09-27, 34주) [추가 설정]
from datetime import date, timedelta
start = date(2026,2,2)
# 주차별 발견 (설계 검토 D / 스프린트 시험 T), 해소 C — 손으로 정한 값
D = [18,26,31,34,29,33,24,15] + [0]*26                       # S3~S6 설계 검토 결함 210
T = [0]*8 + [14,22,31,38, 36,41, 40,47, 33,52, 46,50, 48,44, 39,46, 44,38, 12,9,11, 27,44,52,38,28]  # S7~ 스프린트 단위·통합 시험 결함 910
C = [4,15,22,30,31,33,30,26, 18,20,26,33, 34,38, 37,42, 34,44, 35,43, 40,41, 36,39, 37,35, 17,10,11, 19,33,41,39,31]
assert len(D)==34 and len(T)==34 and len(C)==34
fp_cum = {  # 인수 FP 누적 (스프린트 리뷰 인수 시점 주차) — ⑫와 동일 값
 date(2026,4,12):620, date(2026,4,26):1240, date(2026,5,10):1840, date(2026,5,29):2320, date(2026,6,14):2790,
 date(2026,6,28):3350, date(2026,7,12):3910, date(2026,7,26):4510, date(2026,8,9):5130, date(2026,8,23):5750,
 date(2026,9,6):6390, date(2026,9,25):7020 }
found=closed=0; fd=ft=0; fp=0
print("주 시작 | 설계검토 | 시험 | 주 발견 | 누적 발견 | 주 해소 | 누적 해소 | 미해결 | 인수FP누적 | 시험결함/FP")
for i in range(34):
    ws = start+timedelta(days=7*i); we = ws+timedelta(days=6)
    for k,v in fp_cum.items():
        if ws<=k<=we: fp=v
    fd+=D[i]; ft+=T[i]; found+=D[i]+T[i]; closed+=C[i]
    dens = f"{ft/fp:.3f}" if fp else "—"
    print(f"{ws} | {D[i]:3d} | {T[i]:3d} | {D[i]+T[i]:3d} | {found:5d} | {C[i]:3d} | {closed:5d} | {found-closed:4d} | {fp:5d} | {dens}")
print(f"\n합계: 설계 검토 {fd}, 시험 {ft}, 총 발견 {found}, 해소 {closed}, 미해결 {found-closed}")
print(f"시험 결함밀도(중간) = {ft} / {fp} FP = {ft/fp:.3f}건/FP  (작업패키지 계층 기준 0.13)")
print(f"총 발견 ÷ 12,400 = {found/12400:.3f} (프로젝트 계층 0.4는 통합시험~UAT 기준이므로 아직 해당 없음)")
# 심각도 분포 (미해결 116)
sev = {"1":0,"2":7,"3":58,"4":51}
assert sum(sev.values())==found-closed
print("미해결 심각도:",sev)
# 월별 요약
import collections
mon=collections.OrderedDict()
for i in range(34):
    ws=start+timedelta(days=7*i); m=ws.strftime("%Y-%m")
    a=mon.setdefault(m,[0,0,0]); a[0]+=D[i]; a[1]+=T[i]; a[2]+=C[i]
print("\n월 | 설계 | 시험 | 해소")
for m,(d,t,c) in mon.items(): print(m,d,t,c)
