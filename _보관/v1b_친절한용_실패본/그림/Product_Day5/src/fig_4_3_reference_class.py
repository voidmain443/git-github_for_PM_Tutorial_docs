# -*- coding: utf-8 -*-
"""그림 4-3. 레퍼런스 클래스 12건 — 첫 유료까지 · ARR 1억까지, 딥게이지 계획"""
from mplcommon import *
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from day5_discovery import RC, PLAN_first_paid, PLAN_arr1, med
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
for ax, idx, title, plan in [(axes[0], 1, "첫 유료까지 (개월)", PLAN_first_paid), (axes[1], 2, "ARR 1억까지 (개월)", PLAN_arr1)]:
    vals = sorted(r[idx] for r in RC)
    ax.barh(range(len(vals)), vals, color=NAVY, alpha=0.75, height=0.6)
    for i, v in enumerate(vals): ax.text(v + 0.25, i, str(v), va="center", fontsize=8)
    m = med(vals); ax.axvline(m, color=GREY, ls="--", lw=1.2); ax.text(m + 0.2, len(vals) - 0.4, f"중앙값 {m:g}", fontsize=8.5, color=GREY)
    ax.axvline(plan, color=RUST, lw=2.2); ax.text(plan + 0.3, -1.0, f"딥게이지 계획 {plan}", fontsize=9, color=RUST, fontweight="bold", ha="left")
    ax.set_yticks([]); ax.set_title(title, fontsize=10, loc="left"); ax.set_xlim(0, max(vals) + 4); ax.set_ylim(-3.2, len(vals))
axes[0].text(0.3, -2.7, "12건 중 6건이 계획보다 빠르다 — 중앙값 근처", fontsize=8, color=TEAL)
axes[1].text(0.3, -2.7, "12건 중 1건만 계획보다 빠르다 — 상위 1/12", fontsize=8, color=RUST)
fig.suptitle("레퍼런스 클래스 원장 v0 — 유사 버티컬 SaaS 12건(사례 설정, 실명 아님)", fontsize=10, x=0.02, ha="left")
save(fig, "fig_4_3_reference_class", "Day5 워크북 §5.5 항목 5 [추가 설정]. 계획이 틀렸다는 뜻이 아니다 — 낙관을 알고 시드 IR을 쓰라는 뜻.")
