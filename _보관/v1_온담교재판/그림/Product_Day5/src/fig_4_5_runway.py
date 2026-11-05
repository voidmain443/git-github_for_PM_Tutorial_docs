# -*- coding: utf-8 -*-
"""그림 4-5. 딥게이지 현금 곡선 D+0~180 — 채용 후 급락과 선투자의 자리"""
from mplcommon import *
import numpy as np, sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from day5_discovery import cash0, burn, burn_after
days = np.arange(0, 200)
def cash(d, hire=True):
    # 원장(day5_discovery.py)과 같은 월 단위 관행: D+75까지 3명(2,300/월), 이후 5명(3,230/월). 30일 = 1개월
    if not hire or d <= 75: return cash0 - burn * d / 30
    return cash0 - burn * 75 / 30 - burn_after * (d - 75) / 30
c_hire = [cash(d) for d in days]; c_no = [cash(d, False) for d in days]
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.plot(days, c_no, color=GREY, ls="--", lw=1.4, label="3명 유지 (월 2,300만) — 런웨이 7개월")
ax.plot(days, c_hire, color=NAVY, lw=2.2, label="D+45·D+70 채용 (월 3,230만)")
ax.axhline(0, color="black", lw=0.8)
zero = next(d for d, c in zip(days, c_hire) if c <= 0)
ax.axvline(zero, color=RUST, ls=":", lw=1.4); ax.text(zero - 2, 12000, f"소진 D+{zero}", color=RUST, fontsize=9, ha="right", fontweight="bold")
ax.axvline(180, color=TEAL, ls="--", lw=1.4); ax.text(181, 12000, "시드 12억\nD+180", color=TEAL, fontsize=9)
ax.axvline(150, color=TEAL, lw=2.0); ax.text(149, 6000, "노들 선투자 2억\nD+150", color=TEAL, fontsize=9, ha="right")
ax.scatter([90], [cash(90)], color=NAVY, zorder=4); ax.annotate(f"D+90 잔액 {cash(90):,.0f}만\n(5명 기준 2.7개월)", (90, cash(90)), textcoords="offset points", xytext=(-6, -38), fontsize=8.5, ha="center")
ax.set_xlim(0, 200); ax.set_ylim(-1500, 17500); ax.set_xlabel("D+n (2026-03-02 = D+0)", fontsize=9); ax.set_ylabel("현금 잔액 (만 원)", fontsize=9)
ax.legend(fontsize=8.5, loc="upper right", frameon=False)
ax.set_title("딥게이지 현금 곡선 — 채용 두 명이 런웨이를 7개월에서 2.7개월로", fontsize=10, loc="left")
save(fig, "fig_4_5_runway", "G-15(현금 1.6억·월 2,300만) + Day5 워크북 §1.5 항목 8 [추가 설정]. 검산 day5_discovery.py.")
print("zero day", zero, "D+90", round(cash(90)))
