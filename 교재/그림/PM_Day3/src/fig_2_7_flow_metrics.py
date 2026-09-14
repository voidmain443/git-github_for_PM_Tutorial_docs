from mplcommon import *
import numpy as np
from matplotlib.patches import FancyBboxPatch
S = ["S7","S8","S9","S10","S11","S12","S13","S14","S15","S16","S17","S18"]
thr = [620,620,600,480,470,560,560,600,620,620,640,630]
wip = [22,24,26,41,38,31,28,27,25,24,26,29]
age = [6,7,9,12,10,8,7,7,6,8,9,11]
ct  = [14,15,16,21,22,18,17,16,15,15,16,17]
x = np.arange(12)
fig = plt.figure(figsize=(11.2, 8.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.3, 1.0], hspace=0.28)
ax = fig.add_subplot(gs[0])
ax.bar(x, thr, color=[RUST if v < 500 else NAVY for v in thr], alpha=0.8, width=0.6, label="throughput — 인수 FP / 스프린트")
for i, v in enumerate(thr): ax.text(i, v + 8, str(v), ha="center", fontsize=7.4, color=NAVY if v >= 500 else RUST)
ax.axhline(620, color=GREY, lw=0.9, ls="--", label="계획 620 FP / 스프린트")
ax.set_ylim(0, 1000); ax.set_ylabel("인수 FP"); ax.set_xticks(x); ax.set_xticklabels(S)
ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
ax2.plot(x, wip, color=TEAL, lw=2.2, marker="o", ms=4.5, label="WIP — 진행 중 StRS 항목 수")
ax2.plot(x, age, color=RUST, lw=1.8, marker="D", ms=4, ls="--", label="work item age 최장 (영업일)")
ax2.plot(x, ct, color=GREY, lw=1.4, marker="s", ms=3.5, ls=":", label="cycle time 중앙값 (StRS 승인 → 인수, 영업일)")
for i in (3,): ax2.text(i, wip[i] + 1.5, f"WIP {wip[i]}", fontsize=7.6, color=TEAL, ha="center", fontweight="bold"); ax2.text(i + 0.55, age[i] - 0.5, f"age {age[i]}", fontsize=7.6, color=RUST, fontweight="bold")
ax2.set_ylim(0, 55); ax2.set_ylabel("항목 수 / 영업일")
ax2.annotate("S10 (05-11~29): WIP 41·age 12(POS 화면 정의서)·cycle 21\n— SI EV 하락(5월 3.41, 6월 3.26)과 R-05 실현(IS-02)의 2주 전 신호\n트리거였던 '참석률 70% 미만 2주'보다 age가 먼저 움직였다",
             xy=(3, 41), xytext=(4.2, 47.5), fontsize=7.6, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9))
ax2.annotate("S18: age 11 재상승 — 규제 해석(09-01) + 결함 마무리\n→ 3주 연장·이월 420", xy=(11, 11), xytext=(7.4, 41.5), fontsize=7.4, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.8))
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=7.4, frameon=False, ncol=1, bbox_to_anchor=(0, 1.0))
ax.set_title("온담 S7~S18 흐름 지표 (Vacanti 4지표) — 완료(throughput) 옆에 진행 중(WIP·age)을 둔다", fontsize=10.2, color=NAVY, pad=14)
# ---- 아래: 지표의 층위
bx = fig.add_subplot(gs[1]); bx.set_xlim(0, 100); bx.set_ylim(0, 40); bx.axis("off")
def box(x0, y0, w, h, title, body, fc, ec, tc="white"):
    bx.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=1.2))
    bx.text(x0 + w/2, y0 + h - 2.6, title, ha="center", va="top", fontsize=8.6, color=tc, fontweight="bold")
    bx.text(x0 + 1.5, y0 + h - 7.5, body, ha="left", va="top", fontsize=7.1, color=tc, linespacing=1.35)
box(1, 18, 30, 21, "EVM · ES · CPM — \"어디에 있는가\"", "SPI 0.943 / SPI(t) 0.920 / CPI 1.032\nA10 TF -10 · MG3 as-is 03-05\n단위: 억 원·영업일 · 주기: 월\n수신: 스폰서·CCB·운영위\n완료된 것(인수 FP)만 잰다", NAVY, NAVY)
box(35, 18, 30, 21, "흐름 지표 (Vacanti) — \"왜 그런가\"", "throughput 480 · WIP 41 · age 12 · cycle 21\n단위: 항목·영업일 · 주기: 스프린트(2주)\n수신: 이재현·P1 PMO·주간 PM 회의\n진행 중인 것의 나이를 잰다\n→ SPI가 떨어지기 전에 움직인다", TEAL, TEAL)
box(69, 18, 30, 21, "DORA 4지표 — \"파이프라인이 감당하는가\"", "배포 주 2회 · 리드타임 3.1일\n변경 실패율 12% (목표 ≤10%, 12월)\n복구 4시간 [추가 설정]\n단위: 회·일·% · 주기: 월\n회복 계획 ①(회귀 자동화)의 효과 지표", "#555555", GREY)
bx.annotate("", xy=(35, 28.5), xytext=(31, 28.5), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
bx.annotate("", xy=(69, 28.5), xytext=(65, 28.5), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
bx.add_patch(FancyBboxPatch((1, 0.3), 98, 15.0, boxstyle="round,pad=0.4,rounding_size=1.2", fc="#F6E0DA", ec=RUST, lw=1.2))
bx.text(50, 14.6, "같은 병리 — \"완료된 것만 재는 지표\"", ha="center", va="top", fontsize=8.6, color=RUST, fontweight="bold")
bx.text(2.5, 11.4, "flow debt: 완료 항목의 cycle time은 정상인데 오래 멈춘 항목(age)이 쌓인다 → 어느 날 한꺼번에 늦은 완료가 나온다 (S10 age 12 → S11 470)\n"
                  "SPI 수렴: 누적 EV가 커질수록 SPI가 1로 돌아가 후반부 지연이 보이지 않는다 (8월 0.913 → 9월 0.943, SPI(t)는 0.920)\n"
                  "결함 backlog: 발견 곡선의 평탄이 수렴인지 시험 정지인지 곡선만으로는 모른다 (8월 12·9·11, TC 210 → 95)",
        ha="left", va="top", fontsize=7.2, color="#222222", linespacing=1.4)
bx.text(2.5, 1.2, "처방 (한 줄): 완료 지표 옆에 진행 중 항목의 나이를 병기한다 — throughput 옆 work item age / SPI 옆 SPI(t)·ES / 결함 발견 곡선 옆 시험 노력·결함 나이", ha="left", va="bottom", fontsize=7.6, color=RUST, fontweight="bold")
save(fig, "fig_2_7_flow_metrics", "Day3 워크북 ⑫ 완성 예시본 항목 9(스프린트별 throughput·WIP·age·cycle time 표, DORA 4지표 [추가 설정]), 교재 2.7절. Vacanti(2015) 4지표·DORA(2018) 4지표 개념.")
