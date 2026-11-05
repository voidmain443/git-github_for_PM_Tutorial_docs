from mplcommon import *
import numpy as np
from datetime import date, timedelta
rng = np.random.default_rng(7)
N = 40000
# 개념 시뮬레이션 [추가 설정]: 컷오버 완료일 = 기준 2027-02-26 + 지연(영업일)
# (1) 독립 가정: 활동별 3점 추정을 독립으로 합산 → 큰 수의 법칙으로 분산이 줄어 P80이 P50에 붙는다
ind = sum(rng.triangular(-2, 0, 5, N) for _ in range(6)) / 2.4
ind -= np.percentile(ind, 50)
# (2) 상관 반영(risk driver): 공통 원인(R-01 P2 지연, R-10 정본 후 변경, R-05 인력)이 여러 활동을 동시에 늦춤 → 오른쪽 긴 꼬리
drv = rng.random(N) < 0.45                     # 공통 원인 발생 (약 45%)
common = rng.exponential(1.0, N)
base = rng.triangular(-2, 0, 4, N)
def mk(k):
    c = base + drv * (2 + k * common)
    return c - np.percentile(c, 50)
k = 10.0
for _ in range(60):
    c = mk(k); p80 = np.percentile(c, 80); k *= (15.0 / p80) ** 0.5
cor = mk(k)
fig, ax = plt.subplots(figsize=(9, 4.8))
bins = np.arange(-8, 41, 1)
ax.hist(ind, bins=bins, density=True, color=GREY, alpha=0.35, label="상관 무시 — 활동별 독립 3점 추정 (착시)")
ax.hist(cor, bins=bins, density=True, color=NAVY, alpha=0.55, label="상관 반영 — risk driver (R-01·R-10·R-05가 여러 활동에 동시 매핑)")
p50, p80, p90 = np.percentile(cor, [50, 80, 90]); i80 = np.percentile(ind, 80)
d0 = date(2027, 2, 26)
def bd(d):
    cur, n = d0, int(round(d))
    while n > 0:
        cur += timedelta(1)
        if cur.weekday() < 5: n -= 1
    return cur.strftime("%m-%d")
ymax = ax.get_ylim()[1] * 1.25; ax.set_ylim(0, ymax)
ax.axvspan(0, 15, color=TEAL, alpha=0.10)
ax.text(7.5, ymax*0.60, "프로그램 합류 버퍼\n15영업일 (→ 03-12)\n≈ P70 근처까지 덮는다", ha="center", va="center", fontsize=8.5, color=TEAL)
for x, lab, c, y in [(p50, f"P50 = {bd(p50)} (목표)", NAVY, 0.88), (p80, f"P80 ≈ {bd(p80)} (버퍼 크기의 근거)", RUST, 0.80), (p90, f"P90 ≈ {bd(p90)}", RUST, 0.72)]:
    ax.axvline(x, color=c, ls="--", lw=1.2); ax.text(x + 0.5, ymax*y, lab, color=c, fontsize=8.5)
ax.axvline(i80, color=GREY, ls=":", lw=1.2); ax.text(i80 + 0.5, ymax*0.38, f"독립 가정의 P80 ≈ {bd(i80)}\n— P50에 붙는다", color=GREY, fontsize=8)
ax.set_xlabel("컷오버 완료일의 기준(2027-02-26) 대비 지연 (영업일)"); ax.set_ylabel("확률 밀도"); ax.set_xlim(-8, 40)
ax.legend(loc="upper right", fontsize=8, frameon=False, bbox_to_anchor=(1.0, 0.62))
ax.set_title("몬테카를로 일정 분포 — 상관을 무시하면 P80이 P50에 붙고, 버퍼는 충분해 보인다", fontsize=10.5, color=NAVY, pad=10)
ax.text(0.01, 0.985, "개념 시뮬레이션 [추가 설정] — 분포의 형태만 의미가 있다. 목표는 P50, 버퍼가 P50~P80을 덮는다. P80을 팀의 목표로 주지 않는다", transform=ax.transAxes, fontsize=7.5, color=GREY, va="top")
fig.subplots_adjust(bottom=0.15)
save(fig, "fig_3_4_monte_carlo", "Hulett, D. (2009) Practical Schedule Risk Analysis의 risk driver 방법과 병합 편향 논의를 교재 3.4절 P1 예시(P50 02-26·P80 03-19·합류 버퍼 15영업일)에 맞춰 개념도로 재구성.")
