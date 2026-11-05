from mplcommon import *
import numpy as np
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.9), gridspec_kw={"width_ratios": [1.15, 1.6]})
# 좌: 219.2분 분할 도넛
tot = 43830 * 0.005
unplanned, release = tot * 0.6, tot * 0.4
wedges, _ = ax.pie([unplanned, release], colors=[RUST, NAVY], startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.38, edgecolor="white"))
# 3월 실측 57분 (비계획 유보 안)
ax.pie([57, tot - 57], colors=["#7A3A2A", "none"], startangle=90, counterclock=False, radius=0.62, wedgeprops=dict(width=0.14, edgecolor="none"))
ax.text(0, 0.12, "99.5% / 월", ha="center", fontsize=9, color=NAVY, fontweight="bold")
ax.text(0, -0.08, f"= {tot:.1f}분\n= 3h 39m", ha="center", va="top", fontsize=8.5, color=NAVY)
ax.text(0.95, -0.95, f"비계획 유보 60%\n{unplanned:.1f}분", fontsize=8, color=RUST, ha="center")
ax.text(-1.05, 0.55, f"릴리스 몫 40%\n{release:.1f}분", fontsize=8, color=NAVY, ha="center")
ax.text(1.02, 0.78, "3월 실측 57분 (안쪽 호)\n유보의 43% · 예산 소진 26%\n4월 0분 · 8주 99.927%", fontsize=7, color="#7A3A2A", ha="center")
ax.set_title("월 허용 다운 = 30.4375일 × 1,440분 × 0.5%\n(28일 202 / 30일 216 / 31일 223분 · 계획 정지 제외)", fontsize=8.6, color=NAVY)
# 우: 릴리스당 기대 다운 → 월 릴리스 횟수
cases = [("DORA 실측 2026-09\nCFR 12% × MTTR 240분", 28.8, 3.0, RUST), ("중간 목표 (하자보수기)\nCFR 10% × MTTR 90분", 9.0, 9.7, NAVY), ("ELS 목표\nCFR 10% × MTTR 45분", 4.5, 19.5, TEAL)]
x = np.arange(3)
for xi, (n, d, r, c) in zip(x, cases):
    ax2.bar(xi - 0.2, d, width=0.38, color=c, alpha=0.5)
    ax2.text(xi - 0.2, d + 0.5, f"{d}분\n/릴리스", ha="center", fontsize=7.8, color=c)
ax3 = ax2.twinx()
for xi, (n, d, r, c) in zip(x, cases):
    ax3.bar(xi + 0.2, r, width=0.38, color=c)
    ax3.text(xi + 0.2, r + 0.4, f"월 {r}회\n(주 {r/4.33:.1f})", ha="center", fontsize=8, color=c, fontweight="bold")
ax2.set_xticks(x); ax2.set_xticklabels([c[0] for c in cases], fontsize=7.6)
ax2.set_ylabel("릴리스당 기대 다운 (분) — 옅은 막대", fontsize=8); ax3.set_ylabel("월 릴리스 횟수 = 87.7 ÷ 기대 다운 — 짙은 막대", fontsize=8)
ax2.set_ylim(0, 36); ax3.set_ylim(0, 24); ax3.spines["top"].set_visible(False)
ax2.text(1.0, 33.5, "릴리스 속도는 배포 도구의 문제가 아니라 복구 시간(MTTR)의 문제다\n— 복구 45분 = KEDB 우회 + 회귀 자동화 + 롤백 스크립트", ha="center", fontsize=7.6, color=NAVY)
ax2.text(0, 25.5, "이 상태로는\n주 1회 릴리스 불가", ha="center", fontsize=7.4, color=RUST)
ax2.set_title("릴리스 몫 87.7분 → 릴리스 속도로 환전", fontsize=9.6, color=NAVY)
fig.suptitle("Error budget의 환전 — 99.5% → 219.2분 → 릴리스 몫 87.7분 → 월 3.0 / 9.7 / 19.5회 (온담 SLA ①, 결정자 박준영)", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_3_5_error_budget", "Day4 워크북 ⑰ 항목 3(error budget 표)·src/day4_closing.py §1·§6. DORA 실측은 Day3 ⑫ [추가 설정]. 소진 규칙: 유보 131.5분 초과 시 표준 릴리스 동결, 릴리스 몫 소진 시 CAB 승인 릴리스만.")
