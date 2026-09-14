from mplcommon import *
import numpy as np
# 롤백 트리거 임계값 vs 관측값 — 임계값=100%로 정규화
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6), gridspec_kw={"width_ratios": [4, 1.6]})
ax = axes[0]
items = [("RB-1 마스터 검증\n재실행 횟수", 2, 1, "2회", "1회", "박세연", "전체 롤백 (PoNR 전, 손실 0)"),
         ("RB-2 이력 적재\n완료 시각", 15, 12.58, "11:00 (T0+15h)", "08:35 (T0+12h35m)", "P1 PM → 정미란", "손실 있는 롤백 vs 오픈 연기"),
         ("RB-3 배포 실패\n매장 수", 31, 9, "31점 (5%)", "9점", "오정근·박세연", "매장 갈래 부분 롤백"),
         ("RB-3′ 배포 실패\n직영 매장", 10, 2, "10점", "2점", "오정근·박세연", "(같은 트리거의 둘째 조건)"),
         ("RB-4 스모크\n실패율", 1.0, 0.0, "1.0% (성공 <99.0%)", "0% (36/36)", "정미란", "오픈 연기 → 부분 운영"),
         ("RB-4′ PG 승인\n실패 본수", 1, 0, "1본/7", "0본", "정미란", "(같은 트리거의 둘째 조건)")]
y = np.arange(len(items))[::-1]
for yi, (name, thr, obs, ts, os_, judge, act) in zip(y, items):
    ax.barh(yi, 100, color=SAND, height=0.55)
    r = obs / thr * 100
    ax.barh(yi, r, color=TEAL if r < 100 else RUST, height=0.55)
    ax.text(101.5, yi, f"임계 {ts}", va="center", fontsize=7.6, color=RUST)
    if r > 60: ax.text(r - 1.5, yi + 0.02, f"관측 {os_} ({r:.0f}%)", va="center", ha="right", fontsize=7.6, color="white", fontweight="bold")
    else: ax.text(max(r, 0) + 1.5, yi + 0.02, f"관측 {os_} ({r:.0f}%)", va="center", fontsize=7.6, color=TEAL if r < 100 else RUST, fontweight="bold")
    ax.text(-2, yi, name, va="center", ha="right", fontsize=8.2, color=NAVY)
    ax.text(146, yi, f"{judge}\n→ {act}", va="center", fontsize=7, color=GREY)
ax.axvline(100, color=RUST, lw=1.5)
ax.text(100, len(items) - 0.35, "임계값 = 100%", ha="center", fontsize=7.6, color=RUST)
ax.set_xlim(0, 195); ax.set_ylim(-0.7, len(items) - 0.2)
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("관측값 ÷ 임계값 (%)")
ax.set_title("1차 컷오버 02-26~28 — 트리거 4개 발동 0", fontsize=10, color=NAVY)
# 2차
ax = axes[1]
items2 = [("RB-A 센터 재고\n대사 불일치율", 0.5, 0.03, "%", "한동석"), ("RB-B 설비 IF\n수신 실패", 1, 0, "본", "박세연")]
y2 = np.arange(len(items2))[::-1]
for yi, (name, thr, obs, unit, judge) in zip(y2, items2):
    ax.barh(yi, 100, color=SAND, height=0.5)
    r = obs / thr * 100
    ax.barh(yi, r, color=TEAL, height=0.5)
    ax.text(r + 2, yi, f"관측 {obs:g}{unit} ({r:.0f}%)", va="center", fontsize=7.8, color=TEAL, fontweight="bold")
    ax.text(-3, yi, name, va="center", ha="right", fontsize=8, color=NAVY)
    ax.text(50, yi - 0.42, f"임계 {thr:g}{unit} · {judge}", ha="center", fontsize=7, color=GREY)
ax.axvline(100, color=RUST, lw=1.5)
ax.set_xlim(0, 125); ax.set_ylim(-0.9, 1.9); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xticks([0, 50, 100]); ax.set_xlabel("관측 ÷ 임계 (%)")
ax.set_title("2차 컷오버 03-27~28 — 발동 0", fontsize=10, color=NAVY)
fig.suptitle("롤백 트리거의 임계값과 관측값 — 발동하지 않은 트리거의 관측값은 다음 컷오버의 임계값 근거", fontsize=10.5, color=NAVY, y=1.0)
fig.tight_layout()
save(fig, "fig_2_3_rollback_triggers", "Day4 워크북 ⑯ 항목 5(RB-1~4 임계값·판정자·관측값)·항목 7(2차 RB-A·B). RB-2는 T0(02-26 20:00) 기준 경과 시간으로 비율 환산(12h35m ÷ 15h = 84%).")
