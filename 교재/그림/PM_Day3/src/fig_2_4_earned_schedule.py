from mplcommon import *
import numpy as np
# 워크북 ⑫ 항목 3(PV·EV 누적)·항목 6(ES)·SPI vs SPI(t) 표
months = ["26-01","26-02","26-03","26-04","26-05","26-06","26-07","26-08","26-09","26-10","26-11","26-12","27-01","27-02","27-03","27-04","27-05"]
PVc = np.array([3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83,84.12,91.81,103.00,119.20,129.19,136.77,142.02,145.80])
EVc = np.array([1.81,4.87,17.18,28.86,39.83,48.10,57.28,65.51,73.43])
t = np.arange(1, 18)  # 월 번호 1..17
te = np.arange(1, 10)
SPI  = [0.898,0.784,0.871,0.881,0.914,0.913,0.943]
SPIt = [0.950,0.887,0.868,0.878,0.904,0.914,0.920]
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.4, 8.2), gridspec_kw=dict(height_ratios=[1.55, 1]))
# ---- 위: ES 개념도
ax.plot(np.r_[0, t], np.r_[0, PVc], color=NAVY, lw=2.4, marker="o", ms=3.5, label="PV 누적 (BL-01, 17개월, BAC 145.80)")
ax.plot(np.r_[0, te], np.r_[0, EVc], color=TEAL, lw=2.4, marker="s", ms=3.5, label="EV 누적 (2026-09-30까지 9개월)")
ES = 8.28; AT = 9; EV = 73.43
ax.plot([ES, AT], [EV, EV], color=RUST, lw=2.2)
ax.plot([ES, ES], [0, EV], color=RUST, lw=1.0, ls="--")
ax.plot([AT, AT], [0, EV], color=GREY, lw=1.0, ls=":")
ax.plot([ES], [EV], marker="o", color=RUST, ms=7, zorder=5)
ax.annotate("ES = 8.28개월\n= 8 + (73.43 - 71.74) / (77.83 - 71.74)\n(EV 73.43이 PV 곡선에서 도달한 시점)", xy=(ES, EV), xytext=(3.2, 92), fontsize=8, color=RUST,
            arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax.annotate("AT = 9 (데이터 일자 2026-09-30)", xy=(AT, 0.5), xytext=(9.6, 8), fontsize=8, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
ax.annotate("SV(t) = ES - AT = -0.72개월 (≈ -15영업일)\nSPI(t) = 8.28 / 9 = 0.920", xy=((ES+AT)/2, EV), xytext=(9.6, 92), fontsize=8, color=RUST, ha="left", arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax.annotate("SV = EV - PV = -4.40 (돈)", xy=(AT, PVc[8]), xytext=(11.2, 60), fontsize=8, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
ax.plot([AT, AT], [EV, PVc[8]], color=NAVY, lw=2.2)
# IEAC(t)
ax.axhline(145.8, color=GREY, lw=0.8)
ax.text(0.2, 148, "BAC 145.80 — 종료 시 EV = PV = BAC → SPI는 1로 수렴", fontsize=7.8, color=GREY)
ax.annotate("", xy=(18.48, 145.8), xytext=(17, 145.8), arrowprops=dict(arrowstyle="->", color=RUST, lw=1.6))
ax.text(10.3, 141, "IEAC(t) = PD / SPI(t)\n= 17 / 0.920 = 18.48개월\n(+1.48개월 ≈ +31영업일\n→ 추세 종료 2027-07-12)", fontsize=7.8, color=RUST, ha="center", va="top")
ax.axvline(17 + 15/21, color=RUST, lw=0.9, ls=":")
ax.text(17 + 15/21 + 0.08, 4, "허용범위 G4 +15영업일\n(2027-06-18)", fontsize=7.5, color=RUST, rotation=90, va="bottom", ha="left")
ax.axvline(17, color=GREY, lw=0.7, ls=":"); ax.text(16.95, 60, "PD 17개월\n(2027-05-28)", fontsize=7.5, color=GREY, rotation=90, va="bottom", ha="right")
ax.set_xlim(0, 20.4); ax.set_ylim(0, 160)
ax.set_xticks(np.r_[t, 18, 19]); ax.set_xticklabels(months + ["27-06","27-07"], fontsize=7.2, rotation=45)
ax.set_ylabel("누적 (억 원)")
ax.legend(loc="upper left", fontsize=7.8, frameon=False, bbox_to_anchor=(0.0, 0.93))
ax.set_title("Earned Schedule — EV 73.43이 PV 곡선에서 '언제'에 해당하는가 (2026-09-30, 워크북 ⑫ 항목 6)", fontsize=10.5, color=NAVY, pad=8)
# ---- 아래: SPI vs SPI(t)
xm = np.arange(3, 10)
ax2.plot(xm, SPI, color=NAVY, lw=2.2, marker="o", ms=4, label="SPI = EV / PV (누적, 돈)")
ax2.plot(xm, SPIt, color=RUST, lw=2.2, marker="s", ms=4, ls="--", label="SPI(t) = ES / AT (시간)")
ax2.fill_between(xm[4:], SPI[4:], SPIt[4:], color=RUST, alpha=0.15)
for x, a, b in zip(xm, SPI, SPIt):
    ax2.text(x, a+0.008, f"{a:.3f}", fontsize=7.2, color=NAVY, ha="center", va="bottom")
    ax2.text(x, b-0.010, f"{b:.3f}", fontsize=7.2, color=RUST, ha="center", va="top")
ax2.annotate("7월부터 벌어짐 — SPI는 회복처럼, SPI(t)는 정체\n9월 차이 -0.023 (수렴 착시, 확대 중)", xy=(9, 0.9315), xytext=(6.1, 1.01), fontsize=8, color=RUST,
             arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax2.annotate("4월: 돈으로는 -8.0 (조달 이연 6.0 포함)\n시간으로는 -0.45개월 → SPI(t)가 관대", xy=(4, 0.784), xytext=(4.4, 0.755), fontsize=7.6, color=NAVY,
             arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
ax2.axhline(1.0, color=GREY, lw=0.8); ax2.text(3.0, 1.003, "1.0", fontsize=7.5, color=GREY)
ax2.set_xlim(2.6, 9.6); ax2.set_ylim(0.74, 1.04)
ax2.set_xticks(xm); ax2.set_xticklabels(months[2:9]); ax2.set_ylabel("지수")
ax2.legend(loc="lower right", fontsize=7.8, frameon=False)
ax2.set_title("월별 SPI(실선)와 SPI(t)(파선) — 2026-03 ~ 09", fontsize=9.5, color=NAVY, pad=6)
fig.tight_layout(h_pad=2.2)
save(fig, "fig_2_4_earned_schedule", "Day3 워크북 ⑫ 완성 예시본 항목 3(월별 PV·EV 누적)·항목 6(ES 8.28, SV(t) -0.72, SPI(t) 0.920, IEAC(t) 18.48)·SPI/SPI(t) 표. PV는 Day2 워크북 §4 항목 5 정본. Lipke(2003) 개념을 온담 값으로 재구성.")
