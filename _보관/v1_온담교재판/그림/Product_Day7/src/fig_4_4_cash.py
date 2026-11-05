# -*- coding: utf-8 -*-
"""그림 4-4. 현금 D+300 → D+600 — 열 달의 소진"""
from mplcommon import *
from day7_pmf import BURN_PATH, CASH_D300, CASH_D600, RUNWAY
months=[m for m,_,_ in BURN_PATH]; burns=[b for _,b,_ in BURN_PATH]
cash=[CASH_D300]; 
for b in burns: cash.append(cash[-1]-b)
fig, ax1 = plt.subplots(figsize=(7.8, 4.0)); ax2=ax1.twinx()
ax1.bar(range(len(burns)),[b/1000 for b in burns],color="#DCE6F2",edgecolor=NAVY,width=0.6,zorder=2,label="월 순소진(천만)")
for i,b in enumerate(burns): ax1.text(i,b/1000+0.15,f"{b/1000:.1f}",ha="center",fontsize=7.5,color=NAVY)
ax2.plot(range(-1,len(burns)),[c/10000 for c in cash],color=RUST,lw=2.2,marker="o",ms=4,zorder=3,label="현금 잔액(억)")
ax2.text(len(burns)-1-1.6,CASH_D600/10000+3.2,f"{CASH_D600/10000:.2f}억\n런웨이 {RUNWAY:.0f}개월",fontsize=8.5,color=RUST,va="center")
ax2.text(-0.9,CASH_D300/10000+0.4,"15.40억(D+300)",fontsize=8,color=RUST)
ax1.set_xticks(range(len(burns))); ax1.set_xticklabels([m for m in months],fontsize=8.5); ax1.set_ylim(0,13); ax2.set_ylim(0,18)
ax1.set_ylabel("월 순소진(천만 원)"); ax2.set_ylabel("현금(억 원)"); ax1.set_xlim(-1.2,len(burns)-0.3)
ax1.annotate("8월 — 사고 대응·2-pass 원가",xy=(7,9.9),xytext=(4.2,11.6),fontsize=7.8,color="#333",arrowprops=dict(arrowstyle="->",color=GREY,lw=0.8))
ax1.annotate("10월 — 아웃바운드 중단(D+590)",xy=(9,6.2),xytext=(6.3,2.2),fontsize=7.8,color="#333",arrowprops=dict(arrowstyle="->",color=GREY,lw=0.8))
fig.subplots_adjust(bottom=0.16)
ax1.set_title("현금 15.40 → 6.82억 — 시리즈A 클로징(D+900)에 닿지 않는다", fontsize=10.5, loc="left")
save(fig,"fig_4_4_cash","day7_pmf.py 월별 소진 [추가 설정 — G-15 6.82억/11개월·G-11 6,200에 맞춤]")
