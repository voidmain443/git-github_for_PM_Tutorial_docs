from mplcommon import *
import numpy as np
fig = plt.figure(figsize=(10.6, 6.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1.0], height_ratios=[3.3, 1.0], wspace=0.08, hspace=0.05)
ax = fig.add_subplot(gs[0, 0])
groups = ["가맹 점주 (388점·331명)\n포털 발주 전환", "가맹 점주\n마감 20:00 준수", "직영 매장 (227점)\n반품 신규 절차", "서비스데스크 (11명)\n1차 해결률", "물류센터 (246명, 2차 후)\n센터 재고 조회 사용"]
stages = ["A\n인식", "D\n욕구", "K\n지식", "A\n능력", "R\n강화"]
# 장벽 위치 (행, 열): 가맹 K/A, 가맹 마감 R, 직영 R, 데스크 K, 물류 A/D
bar = {(0, 2), (0, 3), (1, 4), (2, 4), (3, 2), (4, 0), (4, 1)}
note = {(0, 2): "구형 단말 9점 · 60대 이상 점주 27%", (1, 4): "마감 놓치면 다음날 출고 불가 — 경험이 강화", (2, 4): "절차는 알지만 바쁜 시간대 생략",
        (3, 2): "FAQ 부족 → 20건 · KEDB 우회 공유", (4, 0): "노조(김미르) '처리량 목표와 인력' 우려", (4, 1): "→ 한동석 서면 04-12: 평가에 쓰지 않음"}
for i in range(5):
    for j in range(5):
        c = RUST if (i, j) in bar else TEAL
        ax.add_patch(plt.Rectangle((j, 4 - i), 1, 1, facecolor=c, alpha=0.75 if (i, j) in bar else 0.18, edgecolor="white", lw=2))
        if (i, j) in bar:
            ax.text(j + 0.5, 4 - i + 0.5, "장벽", ha="center", va="center", fontsize=8, color="white", fontweight="bold")
for i, g in enumerate(groups):
    ax.text(-0.1, 4 - i + 0.5, g, ha="right", va="center", fontsize=7.8, color=NAVY)
for j, s in enumerate(stages):
    ax.text(j + 0.5, 5.12, s, ha="center", va="bottom", fontsize=8.5, color=NAVY, fontweight="bold")
# 주석 (행 우측)
rn = {0: "K/A — 구형 단말 9점 · 60대 이상 27%\n→ P3 방문 교육 2회차 · '간편 재발주'(R5 05-07)", 1: "R — 다음날 출고 불가 경험이 강화\n→ 마감 30분 전 알림", 2: "R — 알지만 바쁜 시간대 생략\n→ POS 강제 확인 단계(03-12)", 3: "K — FAQ 부족\n→ FAQ 20건 · KEDB 우회 공유", 4: "A/D — 노조 우려가 사용 저항으로\n→ 평가 불사용 서면(04-12)"}
for i, t in rn.items():
    ax.text(5.1, 4 - i + 0.5, t, ha="left", va="center", fontsize=6.9, color=GREY)
ax.set_xlim(-3.1, 9.4); ax.set_ylim(-0.1, 5.9); ax.axis("off")
ax.set_title("집단 5 × ADKAR 5단계 — 장벽의 위치가 다르면 조치가 다르다", fontsize=9.6, color=NAVY, x=0.55, pad=12)
# 우: 지표 곡선
axn = fig.add_subplot(gs[1, 0]); axn.axis("off")
axn.text(0.02, 0.85, "Kotter 단기 성과 — 04-05 협의회 공문 \"가맹 발주 리드타임 38h → 13.6h\"(4월 1주 평균; 목표 12h는 M+12 판정, ⑳ B-08 첫 측정)\nBridges 끝냄 — 03-19 OD-POS 2.1 종료 세션(박세연, 2011년 원 설계자 주관): \"없어진 시스템\"이 아니라 \"임무를 마친 시스템\"\nFord·Ford·D'Amelio — 물류센터의 저항은 정보였다: 시스템이 아니라 '리포트가 평가에 쓰이는가'가 쟁점 → 서면으로 분리", fontsize=7.4, color=NAVY, va="top", ha="left", transform=axn.transAxes, linespacing=1.7)
ax2 = fig.add_subplot(gs[:, 1])
wk = [2, 4, 8]
series = [("가맹 전화·팩스·엑셀 발주 비율 (39% →) 목표 ≤15%", [24, 16, 11], RUST, 15),
          ("가맹 포털 마감 준수율 → 95%", [81, 90, 96], NAVY, 95),
          ("직영 반품 절차 준수율 → 95%", [78, 88, 94], "#8FA9C8", 95),
          ("데스크 1차 해결률 → 70%", [52, 64, 73], TEAL, 70)]
for n, v, c, tgt in series:
    ax2.plot(wk, v, marker="o", color=c, lw=2, label=n)
    ax2.axhline(tgt, color=c, lw=0.8, ls=":", alpha=0.7)
    for x, y in zip(wk, v): ax2.text(x, y + (1.6 if c != "#8FA9C8" else -4.2), f"{y}%", ha="center", fontsize=7, color=c)
ax2.plot([4], [87], marker="s", color=GREY); ax2.text(4.15, 84.5, "물류센터 사용률 87% (2차 후 4주, 목표 90%)", fontsize=6.8, color=GREY)
ax2.set_xticks(wk); ax2.set_xticklabels(["2주", "4주", "8주"]); ax2.set_xlim(1.3, 8.9); ax2.set_ylim(0, 105)
ax2.set_ylabel("%"); ax2.legend(fontsize=6.6, loc="center right", frameon=False, bbox_to_anchor=(1.0, 0.42))
ax2.set_title("채택 지표 2·4·8주 (점선 = 목표)", fontsize=9.6, color=NAVY)
fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.08)
save(fig, "fig_3_7_adkar", "Day4 워크북 ⑰ 항목 8(사용자 채택·ADKAR 장벽 진단 표 — 집단 5, 2·4·8주 지표, 장벽, 조치, 단기 성과 공지, 끝냄 처리). 데이터 P3 교육 대장·포털 로그 [추가 설정].")
