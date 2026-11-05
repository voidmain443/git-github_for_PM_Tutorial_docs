# -*- coding: utf-8 -*-
"""그림 4-4. 옵션풀의 위치 — pre-money vs post-money가 강민수 지분에 미치는 효과 (시드 12억, pre 48억 기준)"""
from mplcommon import *
FD0 = 1_000_000; kang = 450_000; pool0 = 100_000; pre = 48e8; inv = 12e8; inv_share = inv / (pre + inv)   # 20%
# 가정: 텀시트가 "라운드 후 옵션풀 = post FD의 10%"를 요구한다(추가 풀 신설). K-02 정본은 추가 풀 없이 8.0% — 이 그림은 요구받았을 때의 두 방식 비교.
# (A) post-money 기준 — 먼저 주당 4,800원(pre ÷ FD0)에 투자, 그 뒤 풀을 신설해 모두가 희석
N_post = inv / (pre / FD0)                      # 250,000주
fd1 = FD0 + N_post                              # 1,250,000
P_post = (0.10 * fd1 - pool0) / 0.90            # 풀 합계 = 10% of final FD
fd_post = fd1 + P_post; kang_post = kang / fd_post; inv_post = N_post / fd_post
# (B) pre-money 기준 — 풀을 pre FD에 넣어 주당가가 내려가고 기존 주주만 희석; 투자자는 정확히 20%
fd_pre_post = (FD0 - pool0) / (1 - inv_share - 0.10)   # 창업자 900,000주 = 70%
P_pre = 0.10 * fd_pre_post - pool0; N_pre = inv_share * fd_pre_post
kang_pre = kang / fd_pre_post; inv_pre = N_pre / fd_pre_post
fig, ax = plt.subplots(figsize=(7.4, 4.0))
labels = ["시드 전\n(K-01)", "추가 풀 post-money\n(우리 요구)", "추가 풀 pre-money\n(텀시트 표준 문구)"]
vals = [kang / FD0 * 100, kang_post * 100, kang_pre * 100]
bars = ax.bar(labels, vals, color=[GREY, TEAL, RUST], width=0.55, zorder=3)
for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width()/2, v + 0.4, f"{v:.2f}%", ha="center", fontsize=10.5, fontweight="bold")
ax.set_ylim(0, 56); ax.set_ylabel("강민수 지분(FD, %)", fontsize=9)
ax.annotate(f"차이 {vals[1]-vals[2]:.2f}%p — 같은 풀, 누가 희석을 지는가", xy=(2, vals[2]), xytext=(0.6, 41), fontsize=8.5, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
ax.set_title("옵션풀을 post FD의 10%로 요구받았을 때 창업자 지분 — 시드 12억 · pre 48억 (K-02 조건, 가상 비교)", fontsize=9.5, loc="left")
ax.text(1, vals[1]-6, f"투자자 {inv_post*100:.1f}%", ha="center", fontsize=8, color="white"); ax.text(2, vals[2]-6, f"투자자 {inv_pre*100:.1f}%", ha="center", fontsize=8, color="white")
ax.text(0.62, 50.5, "D+12 ㉑ 항목 3에 '추가 풀은 post-money 기준'을 적는 것이\nDay8 한강 텀시트(풀 15% pre, 1.29%p)를 반박하는 계산의 시작이다.", fontsize=7.8, color=GREY)
save(fig, "fig_4_4_option_pool", "검산 day5_discovery.py 기준 K-01·K-02. Day8 K-04의 15% pre 조항 효과 1.29%p는 정본 §7.5.")
print(f"post {kang_post:.4f} (inv {inv_post:.4f}) pre {kang_pre:.4f} (inv {inv_pre:.4f}) diff {(kang_post-kang_pre)*100:.2f}%p")
