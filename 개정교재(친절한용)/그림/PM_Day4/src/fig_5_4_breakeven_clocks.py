from mplcommon import *
import numpy as np
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.6, 5.2), gridspec_kw={"width_ratios": [1.0, 1.15]})
# 좌: NPV 곡선 (할인율 8%, 2026~2031) — 산식은 day4_closing.py §5; 여기서는 점 값을 선형 보간
r = np.linspace(40, 110, 200)
npv_bc = -58.3 + (124.4 + 58.3) / 50 * (r - 50)    # 50% -58.3 → 100% +124.4 (선형: 편익은 실현률에 비례)
npv_ac = npv_bc + (138.3 - 124.4)                 # AC 반영: 구축비 168 → 151.95 만큼 평행 이동
ax.plot(r, npv_bc, color=NAVY, lw=2.2, label="BC v1.0 (구축비 168.0): 손익분기 66.0%")
ax.plot(r, npv_ac, color=TEAL, lw=1.8, ls="--", label="최종 AC 151.95 반영: 손익분기 62.1%")
ax.axhline(0, color=GREY, lw=1)
for rr, v, c, t, dy in [(50, -58.3, NAVY, "50%: -58.3", -12), (66, 0, NAVY, "  66.0%: 0", 6), (70, 14.8, NAVY, "70%: +14.8", 10), (100, 124.4, NAVY, "100%: +124.4", 8), (62.1, 0, TEAL, "62.1%  ", -11), (100, 138.3, TEAL, "+138.3", 8)]:
    ax.plot(rr, v, "o", color=c, ms=6); ax.text(rr, v + dy, t, ha="left" if t.startswith("  ") else ("right" if t.endswith("  ") else "center"), fontsize=7.4, color=c)
ax.axvline(95, color=RUST, lw=1.2, ls=":"); ax.text(95, 150, "판정선 95%\n(미만 → 경고)", ha="center", fontsize=7.2, color=RUST)
ax.axvline(66, color=RUST, lw=1.2, ls=":"); ax.text(65, -62, "66% 미만 →\n후속 투자 판단", ha="right", fontsize=7.2, color=RUST)
ax.axvline(78, color="#E0A040", lw=1.4, ls="-."); ax.text(78, -40, "온담 귀속 99.6 기준\n요구 실현률 78%\n(= 77.8 ÷ 99.6)", ha="center", fontsize=7.2, color="#E0A040")
ax.set_xlim(45, 108); ax.set_ylim(-75, 168)
ax.set_xlabel("편익 실현률 (직접 편익 118억/년 대비, %)"); ax.set_ylabel("NPV (억 원, 할인율 8%, 2026~2031)")
ax.legend(fontsize=7.2, loc="lower right", frameon=False)
ax.set_title("손익분기 실현률 — 66.0% (BC 재확인) / 62.1% (AC 반영)", fontsize=9.6, color=NAVY)
# 우: 두 시계 — x = 2027-01 기준 경과 월
def m(y, mo): return (y - 2027) * 12 + (mo - 1)
ax2.set_xlim(-4, 31); ax2.set_ylim(0, 10); ax2.axis("off")
ax2.plot([-4, 30], [7.3, 7.3], color=NAVY, lw=2); ax2.plot([m(2027, 5), 30], [3.0, 3.0], color=TEAL, lw=2)
ax2.plot([-4, -3.2], [7.3, 7.3], color="white", lw=4)   # 축 절단 표시
ax2.text(-4, 8.7, "프로그램 시계 (M+n, 착수 2026-01 = M0, 13개월 전 ←)", fontsize=8, color=NAVY, fontweight="bold")
ax2.text(m(2027, 5), 4.4, "운영 시계 (이관 2027-05 = +0)", fontsize=8, color=TEAL, fontweight="bold")
for x, t, dy, ha in [(m(2027, 5), "G4 05-28\n(M+17)", 0.35, "center"), (m(2028, 1), "M+24 2028-01\n(BC §4 목표 시점)", -0.4, "center"), (m(2028, 3), "G5 2028-03-31 (M+26)\n전 항목 판정 · 정미란 · 프로그램 이사회(김선호)\n손익분기 66% · 허용범위 -5%p", 0.35, "left")]:
    ax2.plot(x, 7.3, "o", color=NAVY, ms=6)
    ax2.text(x + (0.3 if ha == "left" else 0), 7.3 + dy, t, ha=ha, va="bottom" if dy > 0 else "top", fontsize=6.8, color=NAVY)
for x, t in [(m(2027, 5), "+0\n원장 v1.0 05-21"), (m(2028, 5), "+12 2028-05\n원장 v2 · B 목표 설정 · 유지 판정\n(재무본부 · P5 · 운영위)"), (m(2029, 5), "+24 2029-05\n원장 v3 · 유지 판정\n종결 또는 상시 KPI")]:
    ax2.plot(x, 3.0, "o", color=TEAL, ms=6); ax2.text(x, 2.55, t, ha="center", va="top", fontsize=6.8, color=TEAL)
for i, (x, t) in enumerate([(m(2027, 4), "04 B-08 13.6h"), (m(2027, 6), "06 B-04·02·03"), (m(2027, 9), "09 B-05·07"), (m(2027, 11), "11 B-03 산정식")]):
    ax2.plot(x, 5.0, "v", color=RUST, ms=6); ax2.text(x, 5.25 + (0.55 if i % 2 else 0), t, ha="center", va="bottom", fontsize=6.4, color=RUST)
ax2.text(m(2027, 4) - 0.4, 5.0, "첫 측정", ha="right", fontsize=6.6, color=RUST, va="center")
ax2.axvspan(m(2028, 1), m(2028, 3), ymin=0.70, ymax=0.76, color=NAVY, alpha=0.15)
ax2.text(13, 0.25, "두 시계가 어긋나는 곳: BC §4의 M+24(2028-01)는 프로그램 시계, 운영 조직의 +12(2028-05)는 이관 기준.\n원장은 두 시점을 모두 적고 판정자를 각각 둔다 (G5 재무본부 / 운영 +12·+24 운영위)", ha="center", fontsize=6.9, color=GREY)
ax2.set_title("편익 리뷰의 두 시계 — G5 M+26 / 운영 +12 · +24", fontsize=9.6, color=NAVY)
fig.suptitle("손익분기 66.0% / 62.1% / 78%와 편익 리뷰의 두 시계 (온담 P1 편익 실현 원장 v1.0, 2027-05-21)", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_5_4_breakeven_clocks", "Day4 워크북 ⑳ 항목 3(손익분기·실현 곡선)·항목 4(편익 리뷰 계획 — 두 시계), src/day4_closing.py §5 (NPV 100% +124.4 / 70% +14.8 / 50% -58.3 / AC 반영 +138.3). 곡선은 점 사이 선형 보간.")
