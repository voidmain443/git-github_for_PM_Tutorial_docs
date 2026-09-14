from mplcommon import *
import numpy as np
# 워크북 ⑮ 항목 3 수행사 성과 기록 (S7~S18)
S = ["S7","S8","S9","S10\n(3주)","S11","S12","S13","S14","S15","S16","S17","S18\n(3주)"]
acc = [620,620,600,480,470,560,560,600,620,620,640,630]
carry = [0,0,20,160,310,370,430,450,450,450,430,420]
sla = [100,92,83,58,75,88,90,92,95,94,91,91]
plan = [46,48,50,50,52,52,54,54,54,54,54,54]; act = [46,48,49,50,51,52,53,52,54,54,56,52]
x = np.arange(12)
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10.4, 6.8), sharex=True, gridspec_kw=dict(height_ratios=[1.35, 1]))
cols = [RUST if v < 560 else NAVY for v in acc]
ax.bar(x, acc, color=cols, alpha=0.85, width=0.62, label="인수 FP (스프린트 리뷰)")
ax.axhline(620, color=GREY, lw=1.0, ls="--"); ax.text(-0.45, 700, "계획 620 FP / 스프린트 (파선)", fontsize=7.8, color=GREY)
for i, v in enumerate(acc): ax.text(i, v + 8, str(v), ha="center", fontsize=7.6, color=cols[i])
axb = ax.twinx(); axb.spines["right"].set_visible(True)
axb.plot(x, carry, color=RUST, lw=2.0, marker="o", ms=4, label="이월 누적 FP (계획 - 인수)")
axb.annotate("S18 이월 420\n(R3 120 · A12 300 재배치)", xy=(11, 420), xytext=(9.0, 290), fontsize=7.2, color=RUST, va="top", ha="center", arrowprops=dict(arrowstyle="->", color=RUST, lw=0.7))
axb.text(7.0, 490, "450 (S14~S16)", fontsize=7.2, color=RUST, ha="center")
axb.set_ylim(0, 970); axb.set_ylabel("이월 FP", color=RUST)
ax.set_ylim(0, 920); ax.set_ylabel("인수 FP")
h1,l1 = ax.get_legend_handles_labels(); h2,l2 = axb.get_legend_handles_labels(); ax.legend(h1+h2, l1+l2, loc="upper left", fontsize=7.8, frameon=False, bbox_to_anchor=(0, 1.0))
ax.set_title("수행사 성과 — 인수 FP·이월 (12회 7,020 / 7,440 = 94.4%, velocity 평균 585)", fontsize=10, color=NAVY)
# 아래: SLA + 인력
ax2.plot(x, sla, color=TEAL, lw=2.2, marker="s", ms=4.5, label="발주사 결정 SLA 준수율 (5영업일 내 응답, %)")
for i, v in enumerate(sla): ax2.text(i + (0.28 if i == 3 else 0), v + 2, f"{v}%", ha="left" if i == 3 else "center", fontsize=7.4, color=TEAL, fontweight="bold" if i == 3 else "normal")
ax2.set_ylim(25, 132); ax2.set_ylabel("SLA %", color=TEAL)
axc = ax2.twinx(); axc.spines["right"].set_visible(True)
axc.plot(x, plan, color=GREY, lw=1.2, ls=":", marker="_", ms=9, label="수행 인력 계획 (명)")
axc.plot(x, act, color=NAVY, lw=1.2, marker="o", ms=3.5, label="수행 인력 실 (명, 평균 52.3)")
axc.set_ylim(36, 76); axc.set_ylabel("인력 (명)", color=NAVY)
h1,l1 = ax2.get_legend_handles_labels(); h2,l2 = axc.get_legend_handles_labels(); ax2.legend(h1+h2, l1+l2, loc="upper right", fontsize=7.6, frameon=False, ncol=3)
ax2.set_xticks(x); ax2.set_xticklabels(S, fontsize=8)
# 대조 세로선
for ax_ in (ax, ax2):
    ax_.axvline(3, color=RUST, lw=1.2, ls="--", alpha=0.7); ax_.axvline(10, color=NAVY, lw=1.2, ls="--", alpha=0.7)
ax2.text(3.25, 27, "S10: 인수 480 · SLA 58%\n(POS 화면 승인 대기 12영업일)\n→ 5월 지연은 발주사 원인 (IS-02, 7일 귀책 0.42)", fontsize=7.4, color=RUST, ha="left", va="bottom")
ax2.text(9.75, 27, "S17: 인수 640 · SLA 91%\n→ 9월 이후 지연은\n수행사 원인의 근거", fontsize=7.4, color=NAVY, ha="right", va="bottom")
ax2.set_title("발주사 결정 SLA 준수율과 인력 — 같은 축에 두는 양방향 기록 (총 87건 중 76건 87%)", fontsize=10, color=NAVY)
fig.tight_layout(h_pad=1.4)
save(fig, "fig_5_4_supplier_performance", "Day3 워크북 ⑮ 완성 예시본 항목 3(스프린트별 계획·인수·이월·인력·SLA). 5월 귀책 판정은 ⑬ IS-02·⑮ 항목 6.")
