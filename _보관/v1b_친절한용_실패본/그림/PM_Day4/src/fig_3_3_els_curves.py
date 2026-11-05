from mplcommon import *
import numpy as np
# ELS 8주 지표 곡선 4개 + 종료 기준선
wk = np.arange(1, 9)
err = [2.4, 1.3, 0.9, 0.7, 0.8, 0.5, 0.4, 0.4]
calls = [1840, 1120, 780, 610, 690, 540, 470, 450]
p2 = [3, 2, 1, 0, 2, 1, 0, 0]
p1 = [2, 0, 0, 0, 0, 0, 0, 0]
staff = [20, 20, 15, 15, 18, 10, 10, 6]
fig, axes = plt.subplots(2, 2, figsize=(10.2, 6.4), sharex=True)
def shade(ax):
    ax.axvspan(4.5, 5.5, color=SAND, alpha=0.6)
    ax.axvspan(6.5, 8.5, color=TEAL, alpha=0.08)
ax = axes[0, 0]; shade(ax)
ax.plot(wk, err, marker="o", color=NAVY, lw=2)
ax.axhline(0.5, color=RUST, ls="--", lw=1.4); ax.text(4.0, 0.55, "종료 기준 ③ ≤ 0.5%", ha="center", fontsize=7.6, color=RUST)
ax.axhline(1.8, color=GREY, ls=":", lw=1); ax.text(8.45, 1.85, "구 시스템 기준값 1.8% (O-13)", ha="right", fontsize=7.2, color=GREY)
for x, y in zip(wk, err): ax.text(x, y + 0.08, f"{y}%", ha="center", fontsize=7.4, color=NAVY)
ax.set_ylim(0, 2.8); ax.set_title("매장 주문 오류율 (%)", fontsize=9.5, color=NAVY)
ax = axes[0, 1]; shade(ax)
ax.plot(wk, calls, marker="o", color=NAVY, lw=2)
ax.axhline(480, color=RUST, ls="--", lw=1.4); ax.text(2.6, 300, "종료 기준 ④ ≤ 480/주 (기준 400의 1.2배)", ha="left", fontsize=7.4, color=RUST)
for x, y in zip(wk, calls): ax.text(x, y + 45, f"{y:,}", ha="center", fontsize=7.4, color=NAVY)
ax.set_ylim(0, 2100); ax.set_title("서비스데스크 콜 (건/주)", fontsize=9.5, color=NAVY)
ax = axes[1, 0]; shade(ax)
ax.bar(wk - 0.18, p2, width=0.36, color=NAVY, label="P2")
ax.bar(wk + 0.18, p1, width=0.36, color=RUST, label="P1")
ax.axhline(2, color=RUST, ls="--", lw=1.4); ax.text(8.45, 3.3, "종료 기준 ② P2 ≤ 2/주 · ① P1 0 (2주 연속)", ha="right", fontsize=7.4, color=RUST)
ax.text(1, 2.15, "P1-01 03-03 재고 API 57분\nP1-02 03-05 포인트 이중차감", fontsize=6.8, color=RUST, ha="left", va="bottom")
ax.text(5, 2.15, "P2-07 03-29\n폴백 배치 84분", fontsize=6.8, color=NAVY, ha="center", va="bottom")
ax.set_ylim(0, 3.6); ax.set_yticks([0, 1, 2, 3]); ax.legend(loc="upper right", fontsize=7.5, frameon=False, bbox_to_anchor=(1.0, 0.85))
ax.set_title("인시던트 P1·P2 (건/주) — P3 41 · P4 88 별도", fontsize=9.5, color=NAVY); ax.set_xlabel("ELS 주차 (2027-03-01 ~ 04-23)")
ax = axes[1, 1]; shade(ax)
ax.step(wk, staff, where="mid", color=TEAL, lw=2.2); ax.plot(wk, staff, "o", color=TEAL)
for x, y in zip(wk, staff): ax.text(x, y + 0.7, f"{y}", ha="center", fontsize=7.4, color=TEAL)
ax.text(5, 20.6, "2차 컷오버 후 +3", fontsize=6.8, color=TEAL, ha="center", va="bottom")
ax.text(8.45, 3.8, "→ 04-26 하자보수 체제 4명(비상주)", ha="right", fontsize=7.2, color=GREY)
ax.set_ylim(0, 24); ax.set_title("수행사 상주 인력 (명) — 지표를 따라 줄인다", fontsize=9.5, color=NAVY); ax.set_xlabel("ELS 주차")
for ax in axes.flat:
    ax.set_xticks(wk); ax.set_xlim(0.5, 8.6)
axes[0, 0].text(5, 2.62, "5주차: 2차 컷오버 후\n기준 적용 유예", ha="center", va="top", fontsize=7, color=GREY)
axes[0, 0].text(7.5, 2.62, "7·8주 2주 연속 충족\n→ 04-23 종료 판정(박준영)", ha="center", va="top", fontsize=7, color=TEAL, fontweight="bold")
fig.suptitle("ELS 8주 — 종료 기준 5개(P1 0 · P2 ≤ 2 · 오류율 ≤ 0.5% · 콜 ≤ 480 · 심각도 2 backlog 0)를 2주 연속 충족해야 끝난다", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_3_3_els_curves", "Day4 워크북 ⑰ 항목 5(ELS 8주 계획·실적 표 — 상주·P1·P2·오류율·콜·핫픽스)·종료 기준 ①~⑤. 기준값 1.8%는 Day1 회사 정본 O-13.")
