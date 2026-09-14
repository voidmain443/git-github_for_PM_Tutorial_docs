from mplcommon import *
import numpy as np
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.4, 5.4), gridspec_kw={"width_ratios": [1.0, 1.35]})
# 좌: 원가 3층 vs 최종 AC
layers = [("승인 예산\n(이사회)", 168.00, GREY), ("집행 한도\n(헌장 §12·CR-10)", 156.00, RUST), ("PMB BL-02\n(BAC)", 146.82, NAVY)]
x = np.arange(3)
for xi, (n, v, c) in zip(x, layers):
    ax.bar(xi, v, width=0.55, color=c, alpha=0.25)
    ax.bar(xi, min(v, 151.95), width=0.55, color=c, alpha=0.75)
    ax.text(xi, v + 1.2, f"{v:.2f}", ha="center", fontsize=9, color=c, fontweight="bold")
ax.axhline(151.95, color=TEAL, lw=2.2); ax.text(-0.45, 152.5, "최종 AC 151.95", ha="left", fontsize=9, color=TEAL, fontweight="bold")
ax.axhline(145.80, color=NAVY, lw=0.8, ls=":"); ax.text(-0.3, 143.6, "BL-01 145.80 (+6.15)", fontsize=7, color=NAVY)
# 차이 화살표
def gap(xi, a, b, t, c, dx=0.36):
    ax.annotate("", xy=(xi + dx, a), xytext=(xi + dx, b), arrowprops=dict(arrowstyle="<->", color=c, lw=1.2))
    ax.text(xi + dx + 0.04, (a + b) / 2, t, fontsize=7.4, color=c, va="center")
gap(0, 168.00, 151.95, "16.05 미사용\n= 관리예비비 12.0 반납\n+ 컨틴전시 반납 4.05\n(절감 아님)", GREY)
gap(1, 156.00, 151.95, "여유 +4.05\n= 컨틴전시 반납", RUST)
gap(2, 151.95, 146.82, "VAC -5.13\n= 컨틴전시 집행\n2.50+0.77+1.86", NAVY)
ax.set_xticks(x); ax.set_xticklabels([l[0] for l in layers], fontsize=8.2)
ax.set_ylim(140, 172); ax.set_ylabel("억 원"); ax.set_xlim(-0.5, 3.1)
ax.set_title("같은 151.95가 세 층에서 세 문장이 된다", fontsize=9.8, color=NAVY)
# 우: EAC 이력
rep = ["9호\n09-30", "10호\n10-31", "11호\n11-30", "12호", "13호\n01-31", "14호", "15호\n03-31", "16호", "17호\n05-31"]
eac = [150.86, 151.20, 152.40, 151.70, 152.10, 151.95]
xr = np.array([0, 1, 2, 4, 6, 8])
ax2.plot(xr, eac, marker="o", color=NAVY, lw=2, label="공식 EAC (EAC4, 상향식)")
for xi, v in zip(xr, eac):
    ax2.text(xi, v + 0.25, f"{v:.2f}", ha="center", fontsize=8, color=NAVY)
ax2.axhline(156.00, color=RUST, lw=1.6); ax2.text(8.3, 156.2, "집행 한도 156.00 — 예외 보고 기준", ha="right", fontsize=7.6, color=RUST)
ax2.axhspan(153.0, 156.0, color=RUST, alpha=0.08); ax2.text(0.1, 153.15, "경고 대역 153~156 (진입 0회)", fontsize=7.2, color=RUST)
ax2.axhline(146.82, color=NAVY, lw=0.9, ls="--"); ax2.text(8.3, 147.0, "PMB 146.82", ha="right", fontsize=7.4, color=NAVY)
ax2.axhline(150.57, color=TEAL, lw=0.9, ls=":"); ax2.text(0.1, 150.65, "EAC1′ 150.57 (9월 조정 CPI 0.968)", fontsize=7.2, color=TEAL)
ax2.annotate("경고 A: R-10 재정제\n0.45 · CR-13", xy=(2, 152.4), xytext=(2.9, 154.5), fontsize=7.2, color=RUST, ha="center", arrowprops=dict(arrowstyle="->", color=RUST))
ax2.annotate("경고: 임시 라이선스\n0.02 · ELS 인력", xy=(6, 152.1), xytext=(5.4, 154.6), fontsize=7.2, color=RUST, ha="center", arrowprops=dict(arrowstyle="->", color=RUST))
ax2.text(8, 150.7, "확정 151.95\nCPI 0.966\n(9월 조정 0.968 → Δ0.002)", ha="center", fontsize=7.6, color=TEAL, fontweight="bold")
ax2.set_xticks(np.arange(9)); ax2.set_xticklabels(rep, fontsize=7.4); ax2.set_ylim(146, 157.5)
ax2.set_ylabel("억 원"); ax2.set_title("EAC 이력 — 9호 150.86 → 17호 151.95 (+1.09, ±2 이내), 원가 예외 보고 0회", fontsize=9.6, color=NAVY)
fig.suptitle("원가 3층과 최종 AC 151.95 — \"16.05 미사용\"과 \"VAC -5.13\"이 동시에 참인 이유 (G4 2027-05-28)", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_4_1_three_layers_final", "Day4 워크북 ⑱ 항목 2(기준선 대비 최종 성과 — 원가 축·항목별·EAC 이력)·항목 4(컨틴전시·관리예비비 총괄), src/day4_closing.py §2·§3. 3층은 Day2 ⑨·Day3 ⑫.")
