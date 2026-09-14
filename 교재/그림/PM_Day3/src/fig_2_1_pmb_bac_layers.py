from mplcommon import *
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
months = ["26-01","26-02","26-03","26-04","26-05","26-06","26-07","26-08","26-09","26-10","26-11","26-12","27-01","27-02","27-03","27-04","27-05"]
PVc = np.array([3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83,84.12,91.81,103.00,119.20,129.19,136.77,142.02,145.80])
EVc = np.array([1.81,4.87,17.18,28.86,39.83,48.10,57.28,65.51,73.43]); ACc = np.array([1.85,4.95,17.30,29.02,37.13,45.94,53.93,62.95,71.13])
fig, (ax0, ax) = plt.subplots(1, 2, figsize=(11.5, 5.8), gridspec_kw=dict(width_ratios=[0.8, 1.2]))
# ---- 왼쪽: 3층 세로 막대
ax0.bar(0, 145.8, color=NAVY, width=0.9)
ax0.bar(0, 10.2, bottom=145.8, color=TEAL, width=0.9)
ax0.bar(0, 12.0, bottom=156.0, color=GREY, width=0.9, alpha=0.6)
ax0.text(0, 72, "PMB = BAC\n145.80\n\n시간대별 배분\n= PV 곡선의 합\n\n소유 P1 PM", ha="center", va="center", fontsize=8.5, color="white")
ax0.text(0.5, 151.3, "컨틴전시 10.20 (CR) — 배정 5.30·미배정 2.47·집행 1.41·BL-02 편입 1.02 / PM 전결, 월 CCB 보고", ha="left", va="center", fontsize=6.6, color=TEAL)
ax0.text(0.5, 162.6, "관리예비비 12.00 (MR) — 스폰서 결재, PMB 밖 / 대상 R-01·R-14·R-17 (EMV 2.20)", ha="left", va="center", fontsize=6.6, color="#555555")
for yv, ty, lab, col in [(145.8, 146.5, "145.80  PMB = BAC", NAVY), (156.0, 156.7, "156.00  집행 한도 = 예외 판정 기준 (헌장 §12, CR-10)", RUST), (168.0, 168.7, "168.00  승인 예산 (이사회)", GREY)]:
    ax0.axhline(yv, color=col, lw=1.0, ls="--" if yv != 156.0 else "-"); ax0.text(0.5, ty, lab, fontsize=7.4, color=col, ha="left", va="bottom", fontweight="bold")
ax0.text(0.5, 28, "ANSI/PMI 19-006-2019 용어\nPMB = 승인된 시간대별 계획 (CR·MR 제외)\nBAC = PMB의 총액 — 온담 145.80\nMR = 관리예비비 (PMB 밖) — 12.00\nUB = 미배분 예산 — 승인·미편입 변경\n(CR-08·09·11의 1.02, 10-23 BL-02까지)", fontsize=6.9, color=NAVY, va="center")
ax0.set_xlim(-0.5, 3.6); ax0.set_ylim(0, 178); ax0.set_xticks([]); ax0.set_ylabel("억 원")
ax0.set_title("온담 원가 3층", fontsize=10, color=NAVY)
# ---- 오른쪽: PV 곡선 + EV/AC
x = np.arange(1, 18)
ax.plot(x, PVc, color=NAVY, lw=2.4, marker="o", ms=3.5, label="PV 누적 (BL-01) — 합 145.80 = BAC")
ax.plot(x[:9], EVc, color=TEAL, lw=2.0, marker="s", ms=3.5, label="EV 누적 73.43 (2026-09-30)")
ax.plot(x[:9], ACc, color=RUST, lw=2.0, marker="^", ms=3.5, ls="--", label="AC 누적 71.13")
ax.axhline(145.8, color=NAVY, lw=1.0, ls="--"); ax.text(0.8, 147.0, "BAC = PV 곡선의 합 = 145.80", fontsize=8, color=NAVY)
ax.axhline(156.0, color=RUST, lw=1.2); ax.text(0.8, 157.2, "집행 한도 156.00 — 예외 판정 기준(EAC > 156.0). BAC가 아니다", fontsize=8, color=RUST)
ax.add_patch(Rectangle((1, 145.8), 16, 10.2, fill=False, ls=":", ec=TEAL, lw=1.2))
ax.text(4.5, 128, "컨틴전시 10.20 — 곡선 위 어디에도 배분되어 있지 않다\n(BAC에 넣으면 종료 시 EV가 BAC에\n도달하지 못해 SPI ≠ 1)", fontsize=7.6, color=TEAL, ha="center", va="center")
ax.axvline(9, color=GREY, lw=0.8, ls=":"); ax.text(8.85, 100, "데이터 일자 2026-09-30", fontsize=7.5, color=GREY, rotation=90, va="bottom", ha="right")
ax.annotate("EV 73.43 / AC 71.13 / PV 77.83", xy=(9, 73.43), xytext=(10.2, 60), fontsize=7.8, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.8))
# PV 없는 AC 막대
ax.bar(9.65, 1.19, bottom=0, width=0.5, color=RUST, alpha=0.55)
ax.text(10.05, 1.0, "컨틴전시 집행 1.41 중 AC 발생 1.19\n= 'PV 없는 AC' (R-07 0.15·R-05 0.42·\nR-03 0.50·CR-03 0.12) → SI CV -1.19", fontsize=7.2, color=RUST, va="bottom", ha="left")
ax.set_xticks(x); ax.set_xticklabels(months, fontsize=7.2, rotation=45); ax.set_ylim(0, 170); ax.set_xlim(0.5, 17.5)
ax.set_ylabel("누적 (억 원)"); ax.legend(loc="lower right", fontsize=7.8, frameon=False, bbox_to_anchor=(1.0, 0.12))
ax.set_title("PV 곡선(17개월)과 2026-09-30의 EV·AC — 컨틴전시는 곡선 밖", fontsize=10, color=NAVY)
fig.tight_layout()
save(fig, "fig_2_1_pmb_bac_layers", "Day3 워크북 ⑫ 항목 1(BAC = PMB 145.80, 집행 한도 156.00)·항목 3(PV·EV·AC 누적)·⑬ 항목 7(컨틴전시 집행 1.41 / AC 1.19); Day2 워크북 §4 항목 2·5. 용어는 ANSI/PMI 19-006-2019.")
