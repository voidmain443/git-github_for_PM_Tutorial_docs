from mplcommon import *
import numpy as np
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.2, 6.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
# ---- 왼쪽: 잔여 위협 EMV 폭포 (워크북 ⑬ 항목 6 변동 분해)
steps = [("v1.0\n(03-27)\n11+2건", 6.78, "total", NAVY),
         ("종결·실현·이관\nR-03 0.48 · R-04 1.00\nR-09 0.30 · R-12 0.20", -1.98, "delta", TEAL),
         ("신규 7건\nR-14 0.80 · R-15 0.24\nR-16 0.24 · R-17 0.80\nR-18 0.15 · R-19 0.60\nR-20 0.30", 3.13, "delta", RUST),
         ("재평가 순증\nR-01 -0.60 · R-10 +0.38\nR-05 -0.10 · R-06 -0.15\nR-08 -0.10 · R-11 -0.10", -0.67, "delta", TEAL),
         ("v1.2\n(09-30)\n16건", 7.26, "total", NAVY)]
cur = 0
for i, (lab, v, k, c) in enumerate(steps):
    if k == "total":
        ax.bar(i, v, color=c, width=0.6); cur = v; ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=9, color=c, fontweight="bold")
    else:
        b = cur if v >= 0 else cur + v
        ax.bar(i, abs(v), bottom=b, color=c, width=0.6, alpha=0.85)
        ax.text(i, b + abs(v) + 0.12, f"{v:+.2f}", ha="center", fontsize=9, color=c)
        ax.plot([i-1+0.3, i-0.3], [cur, cur], color=GREY, lw=0.7, ls=":"); cur += v
    ax.text(i, -0.25, lab, ha="center", va="top", fontsize=6.9, color="#222222")
# 2차 리스크 음영 (신규 3.13 중 R-14·15·16·17·18 = 2.23)
ax.bar(2, 2.23, bottom=4.80, color=RUST, width=0.6, alpha=0.35, hatch="//", edgecolor="white")
ax.text(2.35, 5.9, "2차 리스크 5건 2.23\n(대응이 만든 노출)", fontsize=7.2, color=RUST, va="center")
ax.text(1.65, 7.55, "R-19·R-20 0.90\n(회복 계획·감리)", fontsize=7.2, color=RUST, va="center", ha="right")
# 관리예비비 대상 구간
ax.bar(4, 2.20, bottom=0, color="none", edgecolor="white", width=0.6, hatch="xx", lw=0)
ax.text(4.35, 1.1, "관리예비비 대상 2.20\nR-01 0.60 · R-14 0.80\nR-17 0.80 (v1.0과 같은\n숫자, 다른 내용)", fontsize=7.0, color=NAVY, va="center")
ax.text(4.35, 4.7, "컨틴전시 대상 5.06\n(13건)", fontsize=7.2, color=NAVY, va="center")
ax.axhline(8.0, color=RUST, lw=1.3); ax.text(-0.3, 8.6, "허용범위 8.0억 (잔여 위협 EMV) — 여유 1.22 → 0.74, 예외 보고 불요·경고", fontsize=7.8, color=RUST)
ax.annotate("", xy=(4.45, 8.0), xytext=(4.45, 7.26), arrowprops=dict(arrowstyle="<->", color=RUST, lw=1.0)); ax.text(4.55, 7.63, "여유 0.74", fontsize=7.6, color=RUST, ha="left", va="center", fontweight="bold")
ax.text(4.0, 9.45, "R-10 0.76 하나의 크기 —\nG2 후 실현 시 즉시 초과", fontsize=7.2, color=RUST, ha="center", va="bottom")
ax.set_xlim(-0.6, 5.4); ax.set_ylim(-2.4, 10.9); ax.set_xticks([]); ax.axhline(0, color=GREY, lw=0.8)
ax.set_ylabel("잔여 위협 EMV (억 원)"); ax.set_title("잔여 위협 EMV 변동 분해 — 6.78 → 7.26 (v1.0 → v1.2)", fontsize=10, color=NAVY)
# ---- 오른쪽: 컨틴전시 10.20 누적 막대 (항목 7)
labels = ["v1.0 (G1)", "v1.2 (09-30, BL-02 반영)"]
v10 = [("배정 4.60 (11건)", 4.60, NAVY), ("미배정 풀 5.60 (스프린트 4회분)", 5.60, "#8FA9C9")]
v12 = [("배정 5.30 (13건)", 5.30, NAVY), ("미배정 풀 2.47 (1.75회분)", 2.47, "#8FA9C9"), ("집행(약정) 1.41 — AC 발생 1.19", 1.41, RUST), ("BL-02 편입 1.02 (CR-08·09·06)", 1.02, TEAL)]
for xi, parts in [(0, v10), (1, v12)]:
    b = 0
    for lab, v, c in parts:
        bx.bar(xi, v, bottom=b, color=c, width=0.7, edgecolor="white")
        if v >= 2.0:
            bx.text(xi, b + v/2, lab, ha="center", va="center", fontsize=7.0, color="white" if c in (NAVY, RUST, TEAL) else "#222222")
        else:
            bx.text(xi + 0.4, b + v/2, lab, ha="left", va="center", fontsize=7.0, color=c)
        b += v
    bx.text(xi, 10.4, f"합 {b:.2f}", ha="center", fontsize=8.5, color=NAVY, fontweight="bold")
bx.annotate("미배정 풀 5.60 → 2.47\n= 배정 이동 1.785 + BL-02 편입 1.005\n+ 집행 0.34 (CR-03·07)\n→ 신규 리스크 2건이면 풀 소진", xy=(1.35, 5.3 + 2.47/2), xytext=(1.45, 6.0), fontsize=7.2, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
bx.text(1.45, 2.6, "집행 1.41 = R-07 0.15(6월)\n+ R-05 0.42(7월) + R-03 0.50(8월)\n+ CR-03 0.12(9월) + CR-07 0.22(약정)\n소진율 13.8% vs 원가 진척 50.4%\n— 소진은 집행이 아니라 배정으로", fontsize=7.0, color=RUST, va="center")
bx.set_xticks([0, 1]); bx.set_xticklabels(labels, fontsize=8.5); bx.set_ylim(0, 11.4); bx.set_xlim(-0.5, 2.7)
bx.set_ylabel("컨틴전시 10.20 (억 원)"); bx.set_title("컨틴전시 10.20의 구성 — 배정 · 미배정 · 집행 · 편입", fontsize=10, color=NAVY)
fig.tight_layout()
save(fig, "fig_4_5_emv_contingency", "Day3 워크북 ⑬ 완성 예시본 항목 6(잔여 EMV 대조·변동 분해 6.78 - 1.98 + 3.13 - 0.67 = 7.26)·항목 7(컨틴전시 소진 현황과 재배정). v1.0 값은 Day2 워크북 §4 항목 6·§5.")
