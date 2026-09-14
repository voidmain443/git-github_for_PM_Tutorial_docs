from mplcommon import *
import numpy as np
rng = np.random.default_rng(11)
N = 60000
# 워크북 §5 완성 예시본(= 교재 5.7절 표) 대응 후 잔여 리스크 13건 (잔여 P, 영향 억) — 합 6.78. 상관: 한동석 축(R-01·R-03·R-12), 박세연 축(R-05·R-06·R-10) [추가 설정]
risks = {"R-01":(0.60,2.0),"R-02":(0.30,2.0),"R-03":(0.40,1.2),"R-04":(0.40,2.5),"R-05":(0.40,1.5),"R-06":(0.20,1.5),"R-07":(0.40,1.0),
         "R-08":(0.30,2.0),"R-09":(0.20,1.5),"R-10":(0.10,3.8),"R-11":(0.20,2.0),"R-12":(0.25,0.8),"R-13":(0.15,2.1)}
emv = sum(p*i for p, i in risks.values())
axisH = rng.random(N); axisP = rng.random(N)   # 공통 원인 잠재 변수
def occur(rid, p):
    if rid in ("R-01","R-03","R-12"): return axisH < p
    if rid in ("R-05","R-06","R-10"): return axisP < p
    return rng.random(N) < p
tot = np.zeros(N)
for rid, (p, i) in risks.items():
    tot += occur(rid, p) * i * rng.triangular(0.7, 1.0, 1.8, N)   # 영향 자체의 불확실성 (오른쪽 꼬리)
# 결합 꼬리: 세 사건(1차연도 삭감+3PL 결렬+P2 지연)이 겹치면 영향이 곱에 가깝다 — 프리모템 F3 [개념]
tail = (axisH < 0.12) & (rng.random(N) < 0.35)
tot += tail * rng.triangular(6, 12, 30, N)
# 교재 5.3절·5.7절의 예시 P-값(P50 ≈ 6.4 / P80 ≈ 10.1 / P90 ≈ 12.7, 컨틴전시 10.2 ≈ P80)에 맞춰 분위수 사상 [추가 설정]
q = np.percentile(tot, [0, 50, 80, 90, 99.5, 100])
tot = np.interp(tot, q, [0, 6.4, 10.1, 12.7, 21.0, 30.0])
p50, p80, p90 = np.percentile(tot, [50, 80, 90])
pc = (tot <= 10.2).mean()*100
fig, ax = plt.subplots(figsize=(9, 4.8))
bins = np.arange(0, 32, 1)
ax.hist(tot, bins=bins, density=True, color=NAVY, alpha=0.55)
ymax = ax.get_ylim()[1]*1.28; ax.set_ylim(0, ymax)
for x, lab, c, y in [(emv, f"잔여 EMV 합 {emv:.2f} (평균)", GREY, 0.90), (p50, f"P50 ≈ {p50:.1f}", NAVY, 0.82), (10.2, "컨틴전시 10.2 ≈ P80", TEAL, 0.74), (p80, f"P80 ≈ {p80:.1f}", RUST, 0.66), (p90, f"P90 ≈ {p90:.1f}", RUST, 0.58)]:
    ax.axvline(x, color=c, ls="--", lw=1.4); ax.text(x + 0.45, ymax*y, lab, color=c, fontsize=8.5, bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
ax.axvspan(0, 10.2, color=TEAL, alpha=0.08); ax.text(5.0, ymax*0.40, "몸통 — 컨틴전시가 덮는다\n(다섯 중 넷은 충분)", ha="center", fontsize=8.5, color=TEAL)
ax.axvspan(10.2, 22.2, color=RUST, alpha=0.06); ax.text(15.6, ymax*0.24, "컨틴전시 너머 — 관리예비비 12.0\n(스폰서 결재, 기준선 갱신)", ha="center", fontsize=8, color=RUST)
ax.annotate("멱함수형 꼬리 — 프리모템 F3\n(1차연도 삭감 + 3PL 결렬 + P2 지연 결합)\n어떤 유한한 컨틴전시도 덮지 못한다\n→ 구조가 자른다: 분리 컷오버·폴백·선행 릴리스,\n그 너머는 이사회의 중단 결정(헌장 §14)", xy=(22.5, ymax*0.02), xytext=(18.6, ymax*0.50), fontsize=8, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=1))
ax.set_xlabel("P1 잔여 리스크 노출 — 실현될 원가 영향의 합 (억 원)"); ax.set_ylabel("확률 밀도"); ax.set_xlim(0, 31)
ax.set_title("리스크 노출의 분포 — EMV 합·P50·P80과 컨틴전시 10.2의 위치, 그리고 꼬리는 구조가 자른다", fontsize=10.5, color=NAVY, pad=10)
ax.text(0.99, 0.985, "개념 시뮬레이션 [추가 설정] — 분포의 형태만 의미가 있다", transform=ax.transAxes, fontsize=7.5, color=GREY, va="top", ha="right")
fig.subplots_adjust(bottom=0.15)
save(fig, "fig_5_3_exposure_dist", "워크북 §5 완성 예시본 등록부(= 교재 5.7절 표)의 대응 후 잔여 EMV 합 6.78과 교재 5.3절의 예시 P-값(P50 약 6.4·P80 약 10.1·P90 약 12.7, 컨틴전시 10.2 ≈ P80),\n        Flyvbjerg et al. (2022) IT 프로젝트 원가 초과의 멱함수 분포 논의를 개념도로 재구성.")
