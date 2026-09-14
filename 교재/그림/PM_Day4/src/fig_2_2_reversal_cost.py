from mplcommon import *
import numpy as np
# 되돌리는 비용의 계단 — 컷오버 진행 시각(T0=02-26 20:00 기준 h)에 대한 롤백 비용(개념 척도 + 실제 관측값 주석)
fig, ax = plt.subplots(figsize=(10.2, 5.6))
# 구간: [시작h, 끝h, 비용 수준, 라벨]
segs = [
 (-24, -0.5, 0.0, "게이트 1 이전\n비용 0 — 착수하지 않으면 됨"),
 (-0.5, 5.67, 1.0, "게이트 1~PoNR\n시간만 잃음: 구 시스템 재기동 2h, 손실 0"),
 (5.67, 16.0, 2.4, "PoNR 01:40 이후\n이중 원장 대사 2영업일 · 3PL 출고 취소 협의\n(03:00 배치 출고 지시 1,200건+)"),
 (16.0, 20.0, 3.4, "게이트 3 이후(배포 시작)\n매장 부분 롤백: 방문 6영업일 · 2.1억"),
 (20.0, 34.0, 4.6, "16:00 이후 — 롤백 불가\n선택지는 오픈 연기(최대 10:00, 매장 수기)뿐"),
]
cols = [TEAL, TEAL, RUST, RUST, GREY]
for (a, b, c, lab), col in zip(segs, cols):
    ax.plot([a, b], [c, c], color=col, lw=4, solid_capstyle="butt")
    ax.fill_between([a, b], 0, c, color=col, alpha=0.08)
    ax.text((a + b) / 2, c + 0.12, lab, ha="center", va="bottom", fontsize=7.6, color=col)
for i in range(1, len(segs)):
    ax.plot([segs[i][0]] * 2, [segs[i-1][2], segs[i][2]], color=GREY, lw=1, ls=":")
# 결정권자 띠
bands = [(-24, 5.67, "롤백 결정권: P1 PM (게이트 1·2 판정 권한 범위)", NAVY),
         (5.67, 20.0, "정미란 (부재 시 김선호) — 헌장 §14 중단 조건과 같은 층", RUST),
         (20.0, 34.0, "롤백 없음 · 오픈 연기 결정만 정미란", GREY)]
for a, b, t, c in bands:
    ax.axvspan(a, b, ymin=0.0, ymax=0.06, color=c, alpha=0.18)
    ax.text((a + b) / 2, -0.32, t, ha="center", va="center", fontsize=7.2, color=c)
# 게이트 마커
marks = [(-0.5, "게이트 1\n19:30 → 19:35", NAVY, 5.55, "center"), (5.0, "게이트 2\n01:00 → 01:38", NAVY, 6.1, "right"), (5.67, "PoNR 01:40", RUST, 5.55, "left"),
         (16.0, "게이트 3\n12:00 → 12:30", NAVY, 6.1, "right"), (20.0, "기술적 롤백\n최종 시한 16:00", RUST, 5.55, "left"), (32.5, "오픈 판정 04:30", TEAL, 6.1, "right"), (34.0, "오픈 06:00", TEAL, 5.55, "left")]
for x, t, c, yy, ha in marks:
    ax.axvline(x, color=c, lw=1.0, ls="--", alpha=0.7)
    ax.text(x + (0.15 if ha == "left" else -0.15 if ha == "right" else 0), yy, t, ha=ha, va="bottom", fontsize=7.4, color=c, fontweight="bold")
# 롤백 트리거 위치
trig = [(5.0, 1.0, "RB-1 재실행 2회 후 미통과 → 전체 롤백 (관측 1/2)", "center"),
        (15.0, 2.4, "RB-2 이력 적재 11:00 미완 → 손실 있는 롤백 vs 연기 (관측 08:35)", "center"),
        (24.0, 4.6, "RB-3 20:00 집계: 실패 31점·직영 10 초과\n→ 매장 부분 롤백 (관측 9·2)", "left"),
        (32.5, 4.6, "\n\nRB-4 04:30: 스모크 <99.0%·PG 실패\n→ 오픈 연기 (관측 100%·0)", "right")]
for x, y, t, ha in trig:
    ax.plot(x, y, marker="v", color=NAVY, ms=7, zorder=5)
    ax.text(x + (0.3 if ha == "left" else -0.3 if ha == "right" else 0), y - 0.22, t, ha=ha, va="top", fontsize=6.9, color=NAVY)
ax.set_xlim(-24, 35); ax.set_ylim(-0.6, 7.0)
ax.set_xticks([-24, -12, 0, 5.67, 12, 16, 20, 24, 34])
ax.set_xticklabels(["T-24h\n02-25 20:00", "T-12h", "T0\n02-26 20:00", "01:40", "08:00", "12:00", "16:00", "20:00", "T+34h\n02-28 06:00"], fontsize=7.6)
ax.set_yticks([0, 1.0, 2.4, 3.4, 4.6]); ax.set_yticklabels(["0", "시간", "시간+손실", "+매장 방문", "불가"], fontsize=7.8)
ax.set_ylabel("되돌리는 비용 (개념 척도)"); ax.set_xlabel("컷오버 진행 시각")
ax.set_title("되돌리는 비용의 계단 — 게이트는 비용이 달라지는 곳에 놓는다 (온담 1차 컷오버)", fontsize=10.5, color=NAVY, pad=8)
fig.tight_layout()
save(fig, "fig_2_2_reversal_cost", "Day4 워크북 ⑯ 항목 3(게이트)·4(PoNR — 이후 롤백이 잃는 것·최종 시한 산식 8h+2h+4h)·5(트리거 4). 세로축은 개념 척도이며 금액(2.1억)·일수는 워크북 값.")
