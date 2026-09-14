from mplcommon import *
import numpy as np
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.6, 5.4), gridspec_kw={"width_ratios": [2.3, 1.0]})
steps = [("BL-02 편입\n(변경 대가 → PMB)", 1.02, NAVY, "CR-03·06·07·08·09·11"),
         ("리스크 배정 집행", 2.50, RUST, "R-07 0.15 · R-05 0.42 · R-03 0.50\nR-10 0.45 · R-19 0.60 · R-20 0.18 · R-13 0.20"),
         ("미배정 풀 집행", 0.77, RUST, "단말 0.30 · 아카이브 0.20\n부하 시나리오 0.20 · 보안 0.05 · 임시 라이선스 0.02"),
         ("편차 흡수\n(리스크 배정 없는 AC 초과)", 1.86, "#E0A040", "클라우드 실사용 0.76\n망분리·DR 0.50 · PMO 단가 0.60"),
         ("반납", 4.05, TEAL, "= 집행 한도 156.00 - AC 151.95\n프로그램 PMO장 06월")]
x = np.arange(len(steps)); base = 0
for xi, (n, v, c, d) in zip(x, steps):
    ax.bar(xi, v, bottom=base, width=0.6, color=c, alpha=0.85)
    ax.text(xi, base + v / 2, f"{v:.2f}", ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
    if xi < len(steps) - 1: ax.text(xi + 0.36, base + v / 2, d, ha="left", va="center", fontsize=6.6, color=GREY)
    else: ax.text(xi - 0.36, base + v / 2, d, ha="right", va="center", fontsize=6.6, color=GREY)
    if xi < len(steps) - 1: ax.plot([xi + 0.3, xi + 0.7], [base + v, base + v], color=GREY, lw=0.8, ls=":")
    base += v
ax.bar(len(steps), 10.20, width=0.6, color=NAVY, alpha=0.25); ax.text(len(steps), 10.2 + 0.12, "합계 10.20\n(BL-01 컨틴전시)", ha="center", va="bottom", fontsize=7.6, color=NAVY, fontweight="bold")
ax.plot([len(steps) - 0.7, len(steps) - 0.3], [10.2, 10.2], color=GREY, lw=0.8, ls=":")
ax.set_xticks(list(x) + [len(steps)]); ax.set_xticklabels([s[0] for s in steps] + ["합계"], fontsize=7.8)
ax.set_ylim(0, 13.2); ax.set_ylabel("억 원")
ax.text(0.0, 12.5, "집행 5.13 = 2.50 + 0.77 + 1.86 = VAC(-5.13)   ·   소진율(편입 제외) 5.13 ÷ (10.20 - 1.02) = 50.3%   ·   검산: 반납 4.05 = 집행 한도 여유 4.05", fontsize=7.6, color=NAVY)
ax.set_title("컨틴전시 10.20의 분해 — 편입 1.02 + 집행 5.13 + 반납 4.05", fontsize=9.8, color=NAVY)
# 우: 관리예비비 + 유보 3건
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
ax2.add_patch(plt.Rectangle((0.3, 7.0), 9.4, 2.6, facecolor="#DCE6F2", edgecolor=NAVY, lw=1.2))
ax2.text(5, 8.9, "관리예비비 12.0 (이사회 · 스폰서)", ha="center", fontsize=8.6, color=NAVY, fontweight="bold")
ax2.text(5, 7.9, "요청 0 · 집행 0 · 반납 12.0\n대상 R-01·R-14·R-17 미실현 (R-01은 분리 의결로 흡수)", ha="center", fontsize=7.2, color=NAVY)
ax2.text(5, 6.3, "Day2 조정표의 유보 3건 (8.0)", ha="center", fontsize=8.6, color=NAVY, fontweight="bold")
res = [("클라우드 3.0", "반납 — IS-10, 부하시험 후 사이징 확정\n(운영 사용량 월 0.42 → P5 운영비, 이관 8번)", TEAL),
       ("PMO 3.0", "승인 전 — 하자보수기 PMO 잔류 1명 1.05\n(이관 10번, 06-01 운영위)", RUST),
       ("전환 2.0", "감액 확정 — CR-11 5년 필터 (DT-01 10-23)", TEAL)]
for i, (n, d, c) in enumerate(res):
    y = 5.0 - i * 1.75
    ax2.add_patch(plt.Rectangle((0.3, y - 0.7), 9.4, 1.5, facecolor="white", edgecolor=c, lw=1.2))
    ax2.text(0.6, y + 0.35, n, fontsize=8, color=c, fontweight="bold", va="center")
    ax2.text(0.6, y - 0.28, d, fontsize=6.7, color=GREY, va="center")
ax2.text(5, -0.1, "승인 168.00 - 집행 한도 156.00 = 12.0 = 관리예비비\n→ 168 대비 16.05 미사용은 12.0 + 4.05, 절감 아님", ha="center", fontsize=7.2, color=NAVY, va="top")
fig.suptitle("컨틴전시 · 관리예비비 · 유보 3건 총괄 — 예비비는 \"남았다\"가 아니라 \"어디로 갔는가\"로 보고한다", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_4_2_contingency_breakdown", "Day4 워크북 ⑱ 항목 4(컨틴전시·관리예비비 집행 총괄 표), src/day4_closing.py §3. 유보 3건은 Day2 ⑨ §4.5 조정표.")
