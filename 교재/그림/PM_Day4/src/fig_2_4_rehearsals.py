from mplcommon import *
import numpy as np
# 리허설 3회 + 본 컷오버 소요 시간과 검증 6종 결과
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.6, 6.2), gridspec_kw={"height_ratios": [3, 1.6]}, sharex=True)
labels = ["리허설 1회차\n2026-11-23", "리허설 2회차\n2027-01-08", "리허설 3회차\n2027-01-22", "본 컷오버\n2027-02-26~28"]
hours = [41 + 20/60, 33 + 10/60, 31 + 40/60, 34 - (2 + 20/60) + (1 + 10/60)]   # 본 컷오버 = 계획 34h - 여유 2h20m + 소진 1h10m = 32h50m
vol = ["7.4TB 전체\n(CR-11 확정 전)", "5.1TB\n(5년 필터)", "5.1TB\n+ 롤백 리허설 7h50m 병행", "5.1TB · 창 34h\n여유 소진 1h10m / 2h20m"]
cols = [RUST, NAVY, NAVY, TEAL]
x = np.arange(4)
bars = ax.bar(x, hours, color=cols, width=0.55, alpha=0.9)
ax.axhline(34, color=RUST, lw=1.6, ls="--"); ax.text(0.32, 35.4, "컷오버 창 34h (헌장 §7, 허용범위 0)", ha="left", fontsize=7.6, color=RUST)
for xi, h, v in zip(x, hours, vol):
    hh, mm = int(h), int(round((h - int(h)) * 60))
    ax.text(xi, h + 0.5, f"{hh}h {mm:02d}m", ha="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(xi, 2, v, ha="center", va="bottom", fontsize=7.4, color="white")
ax.annotate("창 초과 +7h20m —\n실패를 보기 위한 1회차", xy=(0, 41.3), xytext=(0.75, 44), fontsize=8, color=RUST, ha="center",
            arrowprops=dict(arrowstyle="->", color=RUST))
ax.annotate("본 컷오버 = 31h40m + 편차 순합\n(+38 +30 -25 +10 = +53분 상당)", xy=(3, 32.8), xytext=(2.2, 40), fontsize=7.6, color=TEAL, ha="center",
            arrowprops=dict(arrowstyle="->", color=TEAL))
ax.set_ylim(0, 47); ax.set_ylabel("소요 시간 (h)")
ax.set_title("리허설 3회와 본 컷오버 — 결과가 나빠야 좋은 리허설", fontsize=10.5, color=NAVY, pad=8)
# 검증 6종 격자
checks = ["① 건수", "② 금액 합계", "③ 키 유일성", "④ 참조 정합성", "⑤ 코드 매핑", "⑥ 표본 대조"]
res = [[0, -41200, 1204, 412, 96, 18], [0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]]
txt = [["0", "-41,200원\n규칙 정정", "1,204\n브랜드 간 중복", "412\n고아", "96\n미매핑", "18"], ["0", "0", "0", "0", "0", "3\n시간대·통화"], ["0"] * 6, ["0", "0", "0", "0", "0", "1 → 재실행 → 0\nVAT 반올림"]]
for xi in range(4):
    for j, c in enumerate(checks):
        yy = 5 - j
        v = res[xi][j]
        col = TEAL if v == 0 else (RUST if xi == 0 else "#E0A040")
        ax2.scatter(xi - 0.33 + j * 0.13, yy * 0 + 0.5, s=0)  # placeholder
        ax2.add_patch(plt.Rectangle((xi - 0.36 + j * 0.12, 0.15), 0.11, 0.7, color=col, alpha=0.85 if v else 0.35))
        if v != 0:
            ax2.text(xi - 0.305 + j * 0.12, 0.92 + (0.5 * (j % 3) if xi == 0 else 0), txt[xi][j], ha="center", va="bottom", fontsize=6.2, color=col, rotation=0)
ax2.text(-0.62, 0.5, "검증 6종\n(초록 = 통과)", va="center", ha="center", fontsize=7.5, color=GREY)
for j, c in enumerate(checks):
    ax2.text(-0.36 + j * 0.12 + 0.055, 0.05, c[0], ha="center", va="top", fontsize=6.5, color=GREY)
ax2.text(1.5, -0.22, "① 건수 ② 금액 합계 ③ 키 유일성 ④ 참조 정합성 ⑤ 코드 매핑 커버리지(4,318) ⑥ 표본 필드 대조(2,000/5,000행)  —  1회차 미통과 3종은 G2 정본 정제(11-27)로 해소, 본 컷오버 표본 1건은 2월 가격 개정분 12건의 변환 규칙", ha="center", va="top", fontsize=6.8, color=GREY)
ax2.set_ylim(-0.6, 2.8); ax2.set_yticks([]); ax2.spines["left"].set_visible(False); ax2.spines["bottom"].set_visible(False)
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8.5)
fig.tight_layout()
save(fig, "fig_2_4_rehearsals", "Day4 워크북 ⑯ 항목 1(리허설 3회 소요)·6(검증 6종 결과 표)·10(편차). 본 컷오버 소요는 계획 34h - 여유 2h20m + 소진 1h10m = 32h50m 상당으로 환산.")
