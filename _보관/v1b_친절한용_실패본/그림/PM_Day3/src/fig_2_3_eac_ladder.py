from mplcommon import *
# 워크북 ⑫ 항목 5 — EAC 4공식 + 조정형 2, TCPI 4
items = [
 ("EAC1 = BAC / CPI",               141.23, "현재 CPI 1.032가 끝까지 — 착시 포함, PMB보다 낮은 EAC는 고정가에서 불가능", GREY,  "기각"),
 ("EAC2 = AC + (BAC - EV)",         143.50, "잔여는 계획대로 — 라이선스 미발생 4.70·컨틴전시 잔여 집행 무시", GREY, "기각"),
 ("EAC3 = AC + (BAC - EV)/(CPI×SPI)",145.43, "원가·일정 효율 복합 (0.973)", GREY, "참고"),
 ("BAC = PMB",                      145.80, "계획 원가 (컨틴전시 제외)", NAVY, ""),
 ("EAC1' = BAC / CPI(조정 0.968)",  150.57, "발생주의 CPI 유지 — EAC4 검산", TEAL, "검산"),
 ("EAC4 = AC + 상향식 ETC 79.72",   150.86, "항목별 잔여 근거 — 공식 EAC", TEAL, "공식"),
 ("EAC3' = AC(조정) + 72.37/(0.968×0.943)", 155.04, "조정 CPI × SPI — 일정 회복 실패 시 도착지", RUST, "경고"),
 ("집행 한도 = BAC + 컨틴전시 10.20", 156.00, "예외 보고 기준 (헌장 §12, CR-10)", RUST, ""),
 ("승인 예산 = 집행 한도 + 관리예비비 12.0", 168.00, "이사회", GREY, ""),
]
fig, ax = plt.subplots(figsize=(9.6, 6.4))
y = list(range(len(items)))[::-1]
for yi, (name, val, note, col, tag) in zip(y, items):
    lw = 3.2 if tag in ("공식",) or val in (145.80, 156.00) else 1.8
    ax.plot([136, val], [yi, yi], color=col, lw=lw, solid_capstyle="butt", alpha=0.9 if col != GREY else 0.7)
    ax.plot([val], [yi], marker="o", color=col, ms=8 if lw > 3 else 6, zorder=4)
    ax.text(val + 0.4, yi, f"{val:.2f}", fontsize=9, color=col, va="center", fontweight="bold" if lw > 3 else "normal")
    ax.text(135.6, yi, name, fontsize=8.6, color=col, va="center", ha="right", fontweight="bold" if lw > 3 else "normal")
    ax.text(159.3 if val < 160 else val + 3.4, yi, note + (f"  [{tag}]" if tag else ""), fontsize=7.4, color=GREY, va="center")
ax.axvline(145.80, color=NAVY, lw=1.2, ls="--", alpha=0.7); ax.axvline(156.00, color=RUST, lw=1.4)
ax.axvspan(153.0, 156.0, color=RUST, alpha=0.08); ax.text(154.5, 8.55, "경고 대역\n153~156", fontsize=7.2, color=RUST, ha="center", va="top")
# 괄호: EAC4 ↔ EAC1'
ax.annotate("", xy=(152.6, 3.0), xytext=(152.6, 4.0), arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.0))
ax.text(152.9, 3.5, "0.29 안에서 만남 → 상향식과 조정 지수가 정합", fontsize=7.4, color=TEAL, va="center")
ax.annotate("", xy=(156.0, 1.5), xytext=(155.04, 1.5), arrowprops=dict(arrowstyle="<->", color=RUST, lw=1.2))
ax.text(156.3, 1.5, "여유 0.96 — 스폰서가 기억할 두 번째 숫자", fontsize=7.6, color=RUST, ha="left", va="center", fontweight="bold")
# VAC 표시
ax.text(136.2, -0.9, "VAC = BAC - EAC:  EAC1 +4.57 / EAC2 +2.30 / EAC3 +0.37 / EAC4 -5.06 / EAC3' -9.24      집행 한도 여유 = 156.00 - EAC:  14.77 / 12.50 / 10.57 / 5.14 / 0.96", fontsize=7.6, color=NAVY)
# TCPI 박스
txt = ("TCPI = (BAC - EV) / (기준 - AC) = 72.37 / (기준 - AC)\n"
       "  분모 BAC 145.80 (본값 AC 71.13)      → 0.969  본값 — 착시 포함, 의미 없음\n"
       "  분모 BAC 145.80 (조정 AC 75.83)      → 1.034  PMB 안에 끝내려면 3.4% 절감 — 고정가에서 비현실적 → PMB 초과 확정\n"
       "  분모 집행 한도 156.00                → 0.853  집행 한도 안은 가능 (컨틴전시 잔여 8.79가 완충)\n"
       "  분모 EAC4 150.86                     → 0.908  공식 EAC 달성에 필요한 효율")
ax.text(136.2, -1.65, txt, fontsize=7.6, color=NAVY, va="top",
        bbox=dict(boxstyle="round,pad=0.5", fc="#DCE6F2", ec="none"))
ax.set_xlim(135.5, 181); ax.set_ylim(-5.2, 9.0)
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlabel("원가 (억 원)")
ax.set_title("EAC 사다리 — 네 공식은 네 전제다 (2026-09-30, BAC 145.80 / 집행 한도 156.00)", fontsize=10.5, color=NAVY, pad=8)
fig.tight_layout()
save(fig, "fig_2_3_eac_ladder", "Day3 워크북 ⑫ 완성 예시본 항목 5(EAC1~4, EAC1'·EAC3', VAC, 집행 한도 여유, TCPI 4값). 상향식 ETC 79.72의 항목별 근거는 같은 항목의 표.")
