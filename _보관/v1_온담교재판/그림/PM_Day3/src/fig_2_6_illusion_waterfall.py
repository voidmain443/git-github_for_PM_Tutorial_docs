from mplcommon import *
import numpy as np
fig, axes = plt.subplots(1, 4, figsize=(12.6, 5.4), gridspec_kw=dict(width_ratios=[1.0, 0.95, 1.55, 0.6]))
def wf(ax, steps, title, ylim):
    # steps: (label, delta or None for total, value)
    x = 0; cur = 0
    for i, (lab, kind, v, col) in enumerate(steps):
        if kind == "total":
            ax.bar(i, v, color=col, width=0.62); cur = v
            ax.text(i, v + (0.25 if v >= 0 else -0.25), f"{v:+.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, color=col, fontweight="bold")
        else:
            bottom = cur; ax.bar(i, v, bottom=bottom, color=col, width=0.62, alpha=0.85)
            ax.text(i, bottom + v + (0.25 if v >= 0 else -0.25), f"{v:+.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, color=col)
            ax.plot([i-1+0.31, i-0.31], [cur, cur], color=GREY, lw=0.7, ls=":")
            cur += v
        ax.text(i, ylim[0] + 0.15, lab, ha="center", va="bottom", fontsize=7.0, color="#222222")
    ax.axhline(0, color=GREY, lw=0.8); ax.set_xticks([]); ax.set_ylim(*ylim); ax.set_xlim(-0.6, len(steps)-0.4)
    ax.set_title(title, fontsize=9.2, color=NAVY, pad=6)
wf(axes[0], [("CV 본값\n(EV 73.43\n- AC 71.13)", "total", 2.30, NAVY),
             ("착시 1\n라이선스 미발생\n4.70 가산\n(6.0×50%+3.4×50%)", "delta", -4.70, RUST),
             ("실질 CV\n(발생주의)\nCPI 0.968", "total", -2.40, TEAL)],
   "원가 — CV +2.30은 무엇으로 되어 있나", (-6.5, 4.5))
# 열별 CV
cats = ["SI", "상용SW", "인프라", "전환", "시험·감리", "PMO"]
cv = [-1.19, 4.70, -1.00, 0.20, -0.05, -0.36]
cols = [RUST if v < 0 else TEAL for v in cv]
axes[1].bar(range(len(cats)), cv, color=cols, width=0.62)
for i, v in enumerate(cv):
    axes[1].text(i, v + (0.15 if v >= 0 else -0.15), f"{v:+.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8, color=cols[i])
axes[1].text(0, -1.9, "착시 2\n고정가 SI CPI≡1\n→ CV = 컨틴전시\n집행 1.19", fontsize=7, color=RUST, ha="center", va="top")
axes[1].text(1, 5.1, "착시 1", fontsize=7.6, color=RUST, ha="center", fontweight="bold")
axes[1].axhline(0, color=GREY, lw=0.8); axes[1].set_xticks(range(len(cats))); axes[1].set_xticklabels(cats, fontsize=7.6)
axes[1].set_ylim(-4.2, 6.2); axes[1].set_title("열별 CV (누적, 억)", fontsize=9.2, color=NAVY, pad=6)
wf(axes[2], [("SV 본값\n(EV - PV)", "total", -4.40, NAVY),
             ("착시 3\n측정 시차\n제거 (S20\nPV 1.96)", "delta", 1.96, TEAL),
             ("실질 SV\nSPI 0.968\n≈1.7 스프린트", "total", -2.44, NAVY),
             ("착시 5\n감리 선행\n+0.70 제거\n(시점 이동)", "delta", -0.70, RUST),
             ("SI 실질\n지연\n(전환 +0.20\n포함)", "total", -3.14, RUST)],
   "일정 — SV -4.40은 무엇으로 되어 있나", (-7.2, 3.2))
# 착시 4
ax = axes[3]
ax.bar([0, 1], [0.943, 0.920], color=[NAVY, RUST], width=0.55)
ax.text(0, 0.946, "0.943", ha="center", va="bottom", fontsize=9, color=NAVY, fontweight="bold")
ax.text(1, 0.923, "0.920", ha="center", va="bottom", fontsize=9, color=RUST, fontweight="bold")
ax.set_xticks([0, 1]); ax.set_xticklabels(["SPI\n(돈)", "SPI(t)\n(시간)"], fontsize=8)
ax.set_ylim(0.85, 0.97); ax.set_title("착시 4 — SPI 수렴", fontsize=9.2, color=NAVY, pad=6)
ax.text(0.5, 0.955, "차이 +0.023, 확대 중\n8월 0.913 → 9월 0.943은\n회복이 아니라 수렴", fontsize=7.4, color=RUST, ha="center", va="bottom")
fig.suptitle("온담 2026-09-30 다섯 착시의 크기 — 조정값은 본값 옆에 병기하되 대체하지 않는다", fontsize=10.5, color=NAVY, y=0.99)
fig.tight_layout(rect=(0, 0.02, 1, 0.95))
save(fig, "fig_2_6_illusion_waterfall", "Day3 워크북 ⑫ 완성 예시본 항목 4(조정 1·2·1+2, 열별)·항목 7(착시 1~5 표)·항목 3 열별 CV. 'SI 실질 일정 지연' -3.14는 실질 SV -2.44에서 착시 5(+0.70)를 뺀 값(전환 선행 +0.20 포함).")
