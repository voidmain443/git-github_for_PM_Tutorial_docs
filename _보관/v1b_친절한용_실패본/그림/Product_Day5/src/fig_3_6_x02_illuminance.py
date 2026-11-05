# -*- coding: utf-8 -*-
"""그림 3-6. X-02 OCR 벤치 — 조도 3조건의 정확도와 합격선"""
from mplcommon import *
fig, ax = plt.subplots(figsize=(7.2, 4.2))
conds = ["오전", "오후 3시 이후", "야간 조명"]; vals = [93.1, 84.7, 88.2]; avg = 88.7
cols = [TEAL, RUST, GREY]
bars = ax.bar(conds, vals, color=cols, width=0.55, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.6, f"{v:.1f}%", ha="center", fontsize=10, fontweight="bold")
ax.axhline(90, color=NAVY, ls="--", lw=1.4, zorder=2); ax.text(2.42, 90.3, "합격선 90% (사전등록)", ha="right", fontsize=8.5, color=NAVY)
ax.axhline(avg, color=RUST, lw=2.0, zorder=2); ax.text(1.5, avg + 0.3, f"평균 {avg}% → 실패", ha="center", fontsize=9, color=RUST, fontweight="bold")
ax.annotate("편차 8.4%p → 조도를 독립 변수로 등재\nI-11 \"오후엔 잘 안 보여요\"가 숫자가 된 지점", xy=(1, 84.7), xytext=(0.5, -0.24), textcoords="axes fraction", fontsize=8.2, color=RUST, ha="center",
            arrowprops=dict(arrowstyle="-", color=RUST, lw=0.8))
fig.subplots_adjust(bottom=0.3)
ax.set_ylim(75, 96); ax.set_ylabel("치수 OCR 정확도(항목 단위, %)", fontsize=9)
ax.set_title("X-02 OCR 벤치 — 도면·실물 300장 × 조도 3조건 (사진 900장, 검사항목 2,700개), D+55~68", fontsize=9.5, loc="left")
save(fig, "fig_3_6_x02_illuminance", "Day5 워크북 §4.5 카드 ② [추가 설정] · 검산 day5_discovery.py. D+300 eval v1 OCR 91.4%(V-01)는 6개월 뒤의 값.")
