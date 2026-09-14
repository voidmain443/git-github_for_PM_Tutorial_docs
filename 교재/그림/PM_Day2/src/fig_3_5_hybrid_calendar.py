from mplcommon import *
import numpy as np
from datetime import date, timedelta
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
S0 = date(2026, 1, 5)
sprints = [(i+1, S0 + timedelta(14*i), S0 + timedelta(14*i+13)) for i in range(36)]
def typ(i): return "설계" if i <= 6 else ("구현" if i <= 26 else "통합·시험")
col = {"설계": NAVY, "구현": TEAL, "통합·시험": RUST}
fig, ax = plt.subplots(figsize=(12.5, 6.2))
# --- 행 좌표
Y_SP, Y_REL, Y_GATE, Y_EXT, Y_PEAK, Y_FZ = 5.0, 3.9, 3.0, 1.85, 0.75, 4.5
# 성수기·배포 금지 창 (배경)
peaks = [(date(2026,2,3), date(2026,2,16), "설 전 2주"), (date(2026,7,1), date(2026,8,31), "여름 성수기 7~8월"),
         (date(2026,9,11), date(2026,9,24), "추석 전 2주"), (date(2026,12,1), date(2026,12,31), "연말 성수기 12월"),
         (date(2027,1,25), date(2027,2,5), "설 전 2주")]
for a, b, lab in peaks:
    ax.axvspan(a, b + timedelta(1), ymin=0.02, ymax=0.985, color=RUST, alpha=0.07, lw=0)
    ax.add_patch(Rectangle((mdates.date2num(a), Y_PEAK-0.25), mdates.date2num(b+timedelta(1))-mdates.date2num(a), 0.5, color=RUST, alpha=0.35, lw=0))
    ax.text(a + (b-a)/2, Y_PEAK, lab, ha="center", va="center", fontsize=7, color=RUST)
# 스프린트
for i, a, b in sprints:
    ax.add_patch(Rectangle((mdates.date2num(a), Y_SP-0.28), 13.6, 0.56, facecolor=col[typ(i)], alpha=0.75 if i % 2 else 0.5, lw=0))
    if i % 2 == 1 or i in (36,): ax.text(a + timedelta(7), Y_SP, f"S{i}", ha="center", va="center", fontsize=6.2, color="white")
# 동결 12회 (매월 마지막 수요일) — 워크북 FZ-01~12
fz = [date(2026,1,28), date(2026,2,25), date(2026,3,25), date(2026,4,29), date(2026,5,27), date(2026,6,24), date(2026,7,29), date(2026,8,26), date(2026,9,30), date(2026,10,28), date(2026,11,25), date(2026,12,30)]
for d in fz: ax.plot([d, d], [Y_FZ-0.1, Y_FZ+0.1], color=GREY, lw=1)
ax.text(date(2026,1,6), Y_FZ-0.14, "| = 요구사항 동결 12회 (매월 마지막 수요일, FZ-01~12)", fontsize=7, color=GREY, va="top")
# 릴리스 (워크북 §3 캘린더의 6개 릴리스)
rels = [("R0 설계 베이스라인", date(2026,1,5), date(2026,3,29), NAVY), ("R1 기반·포털 프로토타입", date(2026,3,30), date(2026,6,21), TEAL),
        ("R2 재고 원장·POS 코어·규제", date(2026,6,22), date(2026,9,13), TEAL), ("R3 포털 선행·주문허브", date(2026,9,14), date(2026,12,6), TEAL),
        ("R4 잔여 Must·통합시험 → 컷오버", date(2026,12,7), date(2027,2,28), RUST), ("R5 안정화·이연 기능·이관", date(2027,3,1), date(2027,5,23), GREY)]
for lab, a, b, c in rels:
    ax.add_patch(Rectangle((mdates.date2num(a), Y_REL-0.22), mdates.date2num(b)-mdates.date2num(a), 0.44, facecolor=c, alpha=0.18, edgecolor=c, lw=1))
    ax.text(a + (b-a)/2, Y_REL, lab, ha="center", va="center", fontsize=7, color=c)
# 사용자에게 가는 릴리스 3개 (교재 1.2절)
for d, lab in [(date(2026,11,25), "① 가맹 포털 선행 릴리스\n(12월 성수기 회피 → 11월 말)"), (date(2027,2,26), "② 컷오버 릴리스"), (date(2027,4,16), "③ 컷오버 후 릴리스\n(옴니채널 고도화·BI)")]:
    ax.plot(d, Y_REL+0.36, marker="v", color=NAVY, ms=6); ax.text(d, Y_REL+0.48, lab, ha="center", va="bottom", fontsize=6.5, color=NAVY)
# 게이트 (다이아몬드)
gates = [(date(2026,1,5), "G0 착수"), (date(2026,4,30), "G1 기준선 확정"), (date(2026,11,27), "G2 정본 판정\n(S24 첫 주 금요일)"), (date(2027,2,19), "G3 컷오버 승인"), (date(2027,5,28), "G4 운영 이관")]
for d, lab in gates:
    ax.plot(d, Y_GATE, marker="D", color=NAVY, ms=8); ax.plot([d, d], [Y_GATE, Y_SP+0.28], color=NAVY, lw=0.8, ls=":")
    ax.text(d, Y_GATE-0.3, lab, ha="center", va="top", fontsize=7, color=NAVY)
# 외부 고정일·제약 (역삼각형)
ext = [(date(2026,4,24), "P2 T0 04-24\n규격 전달 (FNLT)", RUST, 0), (date(2026,8,12), "규제① 내부 목표 08-12\n(22영업일 버퍼)", GREY, 0), (date(2026,9,11), "규제① 09-11", RUST, 1),
       (date(2027,1,29), "리허설 3회차·\n전자금융 신청 01-29", GREY, 0), (date(2027,2,12), "P2 MC 02-12\n(SNET)", RUST, 1), (date(2027,2,26), "컷오버\n02-26~28", RUST, 0), (date(2027,3,12), "버퍼 종료\n03-12", GREY, 1), (date(2027,3,31), "규제② 03-31", RUST, 0)]
for d, lab, c, lv in ext:
    ax.plot(d, Y_EXT, marker="^", color=c, ms=7); ax.text(d, Y_EXT-0.26-0.42*lv, lab, ha="center", va="top", fontsize=6.5, color=c)
ax.plot([date(2027,2,19), date(2027,3,12)], [Y_EXT+0.36]*2, color=GREY, lw=4, alpha=0.5); ax.text(date(2027,3,1), Y_EXT+0.42, "합류 버퍼 15영업일 (프로그램)", fontsize=6.5, color=GREY, ha="center", va="bottom")
# 축
ax.set_xlim(date(2025,12,20), date(2027,6,20)); ax.set_ylim(0.2, 5.75)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
ax.tick_params(axis="x", labelsize=7.5); ax.set_yticks([Y_SP, Y_REL, Y_GATE, Y_EXT, Y_PEAK]); ax.set_yticklabels(["스프린트 36회\n(2주 고정)", "릴리스", "게이트", "외부 고정일·\n제약 일자", "성수기·\n배포 금지 창"], fontsize=8)
ax.spines["left"].set_visible(False)
for lab, c in col.items(): ax.plot([], [], color=c, lw=6, alpha=0.7, label=f"{lab} 스프린트")
ax.legend(loc="upper right", fontsize=7.5, frameon=False, ncol=3, bbox_to_anchor=(1.0, 1.06))
ax.set_title("온담 P1 하이브리드 달력 — 36 스프린트 위에 게이트·외부 고정일·성수기 창·릴리스를 겹친 한 장", fontsize=11, color=NAVY, pad=14, loc="left")
fig.subplots_adjust(left=0.08, right=0.99, bottom=0.10, top=0.9)
save(fig, "fig_3_5_hybrid_calendar", "사례 문서 §5.4(스프린트 36회·게이트 G0~G5·외부 고정일)와 헌장 §7·§9, 워크북 §3 완성 예시본의 스프린트×게이트 캘린더(릴리스 6개·동결 12회)를 재구성. 스프린트·성수기 창 날짜는 [추가 설정].")
