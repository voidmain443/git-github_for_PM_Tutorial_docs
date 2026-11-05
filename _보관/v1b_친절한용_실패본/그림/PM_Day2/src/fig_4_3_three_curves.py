from mplcommon import *
import numpy as np
months = ["26-01","26-02","26-03","26-04","26-05","26-06","26-07","26-08","26-09","26-10","26-11","26-12","27-01","27-02","27-03","27-04","27-05"]
# PV — 워크북 §4 완성 예시본 항목 5 (= 교재 4.5절 표) 월별 PV 누적 (작업 시점 기준)
pv = np.array([3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83,84.12,91.81,103.00,119.20,129.19,136.77,142.02,145.80])
# 약정(commitment) — 계약·발주 시점 기준 [추가 설정, 개념도]: SI 68.2 계약(1월), 상용SW 19.4 발주(2~3월), 인프라 20.9(2~4월), 데이터 전환 9.4(4월), 단말 8.6(10월), 시험·감리 9.7(4·10월), PMO 9.6 균등(월 0.56)
com = np.array([68.2+0.56, 68.2+9.0+10.0+1.12, 68.2+19.4+14.0+1.68, 68.2+19.4+20.9+9.4+4.0+2.24, 0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=float)
com[4:10] = com[3] + np.arange(1,7)*0.56
com[9] = com[8] + 8.6 + 5.7 + 0.56
com[10:] = com[9] + np.arange(1,8)*0.56
com[-1] = 145.8
# 현금(cash) — 지급 시점 기준 [추가 설정, 개념도]: SI 선급 20%·중도 G1/G2 30/30·잔금 G4 20, 라이선스 검수 후 익월, 단말 설치 후, PMO 월별
cash = np.array([2.0, 5.0, 8.0, 14.0, 30.0, 40.0, 45.0, 50.0, 55.0, 60.0, 66.0, 84.0, 98.0, 106.0, 124.0, 130.0, 145.8])
x = np.arange(len(months))
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(x, com, color=GREY, lw=2, ls="--", marker="s", ms=3, label="약정 (commitment) — 계약·발주 시점 기준. 구매(강현도)·재경이 본다 → 계약·발주 한도 168.0")
ax.plot(x, pv, color=NAVY, lw=2.4, marker="o", ms=3.5, label="PV (계획가치) — 작업 시점 기준. PM이 본다 → Day3 EVM의 PV")
ax.plot(x, cash, color=RUST, lw=2, ls="-.", marker="^", ms=3.5, label="현금 (cash) — 지급 시점 기준. 재경이 본다 → 자금 계획, 연차 예산 176/198/54")
# 자금 조달 한도 (개념)
lim = np.array([5,10,15,25,35,45,55,65,75,85,95,95,95,95,120,135,148])
ax.step(x, lim, where="post", color=TEAL, lw=1.4, ls=":", label="자금 조달 한도 (funding limit) — 기간별 쓸 수 있는 현금 [개념]")
ax.fill_between(x, cash, lim, where=(cash > lim), color=RUST, alpha=0.15, interpolate=True)
ax.annotate("현금 > 한도 구간 (2027-01~03)\n→ 작업을 미루거나(funding limit reconciliation)\n   한도를 올려야 한다", xy=(13.0, 106), xytext=(3.2, 100), fontsize=7.5, color=RUST, ha="left", arrowprops=dict(arrowstyle="->", color=RUST, lw=1))
ax.axhline(145.8, color=GREY, lw=0.8); ax.text(0, 140, "같은 145.8 — 세 곡선은 모두 여기서 만난다", fontsize=8, color=GREY)
for gx, gl in [(3, "G1"), (10, "G2"), (13, "G3·컷오버"), (16, "G4")]:
    ax.axvline(gx, color=GREY, lw=0.6, ls=":"); ax.text(gx, 150, gl, fontsize=7.5, color=GREY, ha="center", va="bottom")
ax.set_xticks(x); ax.set_xticklabels(months, fontsize=7.5, rotation=45); ax.set_ylabel("누적 (억 원)"); ax.set_ylim(0, 162)
ax.legend(loc="lower right", fontsize=7.2, frameon=True, framealpha=0.9, edgecolor="none", bbox_to_anchor=(1.0, 0.02))
ax.set_title("같은 145.8이 세 개의 다른 S-curve가 된다 — PV·약정·현금, 그리고 자금 조달 한도", fontsize=10.5, color=NAVY, pad=10)
fig.subplots_adjust(bottom=0.17)
save(fig, "fig_4_3_three_curves", "PV 누적은 워크북 §4 완성 예시본 항목 5 월별 PV 표(= 교재 4.5절 표). 약정·현금 곡선과 자금 조달 한도는 지급 조건(선급·중도·잔금)과 발주 시점을 가정한 개념도 [추가 설정]이며 실측이 아니다.\n        PMBOK 8판 Finance 성과영역의 funding limit reconciliation 개념을 교재 4.3절에 따라 재구성.")
