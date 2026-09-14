from mplcommon import *
import numpy as np
from matplotlib.patches import Rectangle
# 워크북 ⑭ 항목 2 주차별 표 (34주, 2026-02-02 ~ 09-27)
D = [18,26,31,34,29,33,24,15] + [0]*26
T = [0]*8 + [14,22,31,38,36,41,40,47,33,52,46,50,48,44,39,46,44,38,12,9,11,27,44,52,38,28]
C = [4,15,22,30,31,33,30,26,18,20,26,33,34,38,37,42,34,44,35,43,40,41,36,39,37,35,17,10,11,19,33,41,39,31]
w = np.arange(1, 35); found = np.cumsum(np.array(D)+np.array(T)); closed = np.cumsum(C); backlog = found - closed
tc = np.array([0]*8 + [210]*18 + [95,95,95] + [230]*5)  # 주당 실행 TC [추가 설정]
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(11.2, 7.6), sharex=True, gridspec_kw=dict(height_ratios=[2.0, 1.0]))
ax.fill_between(w, 0, backlog, color=RUST, alpha=0.18, label="미해결 backlog (발견 - 해소)")
ax.plot(w, found, color=NAVY, lw=2.4, label="누적 발견 (설계 검토 210 + 스프린트 시험 930 = 1,140)")
ax.plot(w, closed, color=TEAL, lw=2.2, ls="--", label="누적 해소 (1,024)")
ax.plot(w, backlog, color=RUST, lw=1.6)
for (x0, x1, lab) in [(1, 8, "① 설계 검토\n수렴형 평탄\n(S3–S6)"), (9, 26, "② 스프린트 시험 상승 (S7–S15)\n주 210 TC · 6월 밀도 0.16 최고"), (27, 29, ""), (30, 34, "④ 9월 재상승\n(S17–S18)")]:
    ax.axvspan(x0-0.5, x1+0.5, color=NAVY if lab else RUST, alpha=0.05 if lab else 0.0)
    if lab: ax.text((x0+x1)/2, 1250, lab, fontsize=7.6, color=NAVY, ha="center", va="top")
ax.add_patch(Rectangle((26.5, 0), 3, 1330, fill=False, ec=RUST, lw=1.6, ls="--"))
ax.text(28, 1250, "③ 8월 평탄\n12·9·11\n= 시험 정지형", fontsize=7.6, color=RUST, ha="center", va="top", fontweight="bold")
ax.annotate("backlog 116 (최고)\n심각도 1: 0 / 2: 7 / 3: 58 / 4: 51", xy=(34, 116), xytext=(27.5, 380), fontsize=7.8, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax.annotate("backlog 96 → 90: 해소도 함께 줄었다\n— 곡선만 보면 '개선'", xy=(28, 90), xytext=(18.5, 300), fontsize=7.6, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.8))
ax.annotate("6월부터 해소가 발견을 따라가지 못함\n(개발자 R3 설계·규제 항목 병행)", xy=(20, 65), xytext=(9.5, 500), fontsize=7.6, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
ax.set_ylim(0, 1330); ax.set_ylabel("건 (누적)"); ax.legend(loc="center left", fontsize=7.8, frameon=False, bbox_to_anchor=(0.0, 0.62))
ax.set_title("온담 P1 34주 결함 누적곡선 (2026-02-02 ~ 09-27) — 평탄의 두 의미", fontsize=10.5, color=NAVY)
# 아래: 시험 노력 + 밀도
ax2.bar(w, tc, color=NAVY, alpha=0.35, width=0.8, label="주당 실행 TC (시험 노력) [추가 설정]")
ax2.text(28, 104, "-55% : 시험 인력 6명 중 4명\n규제 검증 A07으로 이동", fontsize=6.8, color=RUST, ha="center", va="bottom", fontweight="bold")
ax2.set_ylim(0, 300); ax2.set_ylabel("TC / 주", color=NAVY); ax2.set_xlabel("주 (1 = 2026-02-02 주, 34 = 09-21 주)")
ax3 = ax2.twinx(); ax3.spines["right"].set_visible(True)
mx = [12.5, 17, 21.5, 26, 30.5, 34]; dens = [0.085, 0.130, 0.162, 0.157, 0.129, 0.132]
ax3.plot(mx, dens, color=RUST, lw=2.0, marker="o", ms=5, label="월별 누적 밀도 (시험 결함 ÷ 인수 FP)")
for xm_, d_, m_ in zip(mx, dens, ["4월","5월","6월","7월","8월","9월"]):
    ax3.text(xm_, d_ + 0.008, f"{m_} {d_:.3f}", fontsize=7.2, color=RUST, ha="center", va="bottom")
ax3.axhline(0.13, color=RUST, lw=1.0, ls="--"); ax3.text(0.6, 0.133, "허용범위 0.13건/FP\n(작업패키지 계층, 수행사 PM)", fontsize=7.2, color=RUST, va="bottom")
ax3.annotate("8월 0.129 = 착시\n(시험 정지)", xy=(30.5, 0.129), xytext=(22.5, 0.182), fontsize=7.4, color=RUST, ha="center", arrowprops=dict(arrowstyle="->", color=RUST, lw=0.8))
ax3.annotate("09-28 1단계\n에스컬레이션\n(0.132 > 0.13)", xy=(34, 0.132), xytext=(33.0, 0.178), fontsize=7.2, color=RUST, ha="center", arrowprops=dict(arrowstyle="->", color=RUST, lw=0.8))
ax3.set_ylim(0, 0.21); ax3.set_ylabel("건/FP", color=RUST)
h1, l1 = ax2.get_legend_handles_labels(); h2, l2 = ax3.get_legend_handles_labels(); ax2.legend(h1+h2, l1+l2, loc="upper left", fontsize=7.6, frameon=False)
ax2.set_xlim(0.3, 37.5); ax2.set_xticks([1,5,9,13,17,21,25,29,33]); ax2.set_xticklabels(["02-02","03-02","03-30","04-27","05-25","06-22","07-20","08-17","09-14"], fontsize=7.5)
fig.tight_layout(h_pad=1.0)
save(fig, "fig_4_2_defect_curves", "Day3 워크북 ⑭ 완성 예시본 항목 2(주차별 발견·해소·미해결·밀도)·항목 3(구간 ①~④)·항목 4(월별 누적 밀도). 검산 스크립트 src/day3_defects.py. 주당 실행 TC는 [추가 설정].")
