from mplcommon import *
import numpy as np
months = ["26-01","26-02","26-03","26-04","26-05","26-06","26-07","26-08","26-09","26-10","26-11","26-12","27-01","27-02","27-03","27-04","27-05"]
# 워크북 §4 완성 예시본 항목 5 — 월별 PV (억 원). 누적은 원값 기준(월 값 합과 ±0.01 차이 가능)
mpv = np.array([3.06,3.06,13.02,17.69,8.89,8.89,8.09,9.05,6.09,6.29,7.69,11.19,16.20,9.98,7.59,5.24,3.78])
cum = np.array([3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83,84.12,91.81,103.00,119.20,129.19,136.77,142.02,145.80])
x = np.arange(len(months))
fig, ax = plt.subplots(figsize=(9.2, 5.0))
ax2 = ax.twinx()
bars = ax2.bar(x, mpv, color=NAVY, alpha=0.18, width=0.6, label="월 PV (억, 오른쪽 축)")
for i, v in enumerate(mpv):
    if v >= 11: ax2.text(i, v * 0.45, f"{v:.2f}", ha="center", va="center", fontsize=7.5, color=NAVY)
ax2.set_ylim(0, 100); ax2.set_ylabel("월 PV (억 원)", color=GREY); ax2.tick_params(axis="y", colors=GREY); ax2.spines["right"].set_visible(True); ax2.spines["top"].set_visible(False)
ax.plot(x, cum, color=NAVY, lw=2.6, marker="o", ms=4, label="누적 PV — 워크북 §4 완성 예시본 항목 5 (작업 시점 기준)\n(SI 68.2 / 상용SW 19.4 / 인프라 20.9 / 단말 8.6 / 전환 9.4 / 시험·감리 9.7 / PMO 9.6)")
for i, off in [(3, (-10, 6)), (11, (-8, 8)), (13, (-8, 8)), (16, (-6, -32))]:
    ax.annotate(f"{cum[i]:.2f}\n({cum[i]/145.8*100:.1f}%)", (i, cum[i]), xytext=off, textcoords="offset points", fontsize=7.5, color=NAVY, ha="right")
for gx, gl in [(3, "G1 04-30"), (10, "G2 11-27"), (13, "G3 02-19 · 컷오버 02-26"), (16, "G4 05-29")]:
    ax.axvline(gx, color=GREY, lw=0.7, ls=":"); ax.text(gx, 150, gl, fontsize=7.5, color=GREY, ha="center", va="bottom")
ax.axvspan(1.6, 3.4, color=RUST, alpha=0.07); ax.text(2.2, 66, "봉우리 ① 라이선스 14.0(3~4월)\n+ 클라우드 선약정 6.0 — R-04\n(1차연도 삭감)의 첫 이연 후보", fontsize=7.5, color=RUST, ha="center")
ax.axvspan(10.6, 13.4, color=RUST, alpha=0.07); ax.annotate("봉우리 ② 단말 8.6·DR 4.2·\n부하시험·보안진단·감리·컷오버", xy=(11.4, 30), xytext=(8.0, 36), fontsize=7.5, color=RUST, ha="center", arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax.axhline(145.8, color=GREY, lw=0.8); ax.text(0, 141, "계획 원가 145.8 (BAC 156.0은 컨틴전시 10.2를 더한 값 — PV 곡선에는 없다)", fontsize=7.5, color=GREY)
ax.text(13.6, 62, "2026년 누적 103.00 (70.6%) / 2027년 42.80\nBC 연차 집행 계획 2026 102.0과 차이 1.0 —\nPV(작업 예정) vs 현금(검수 후 지급)의 시점 차이, 정합", fontsize=7.5, color=NAVY, ha="center")
ax.set_xticks(x); ax.set_xticklabels(months, fontsize=7.5, rotation=45); ax.set_ylabel("누적 PV (억 원)"); ax.set_ylim(0, 165); ax.set_xlim(-0.6, 16.6)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=6.8, frameon=True, framealpha=0.92, edgecolor="none", bbox_to_anchor=(0.0, 0.84))
ax.set_title("온담 P1 계획 원가 145.8의 월별 PV S-curve — 봉우리는 사실이다 (작업 시점 기준, 지급 시점이 아니다)", fontsize=10.5, color=NAVY, pad=10)
fig.subplots_adjust(bottom=0.16, right=0.92)
save(fig, "fig_4_5_pv_scurve", "워크북 §4 완성 예시본 항목 5 '월별 PV 곡선' 표 = 교재 4.5절 표 [추가 설정 — 배분 규칙: SI 스프린트 시작 월 가중 0.7/1.1/1.2, 라이선스 인도 시점 2026-03~05, 단말 2026-12~2027-02, 감리 게이트별, PMO 월 0.56].")
