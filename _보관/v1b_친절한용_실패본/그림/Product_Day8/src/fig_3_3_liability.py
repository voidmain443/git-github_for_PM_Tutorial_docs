# -*- coding: utf-8 -*-
"""그림 3-3. 배상 4구간 vs 3년 공헌·현금 — 물리적 하한"""
from mplcommon import *
from day8_enterprise import LIAB_TIERS, LIAB_TABLE, CONTRIB_3Y, CASH, YEAR1_CASH, SETUP_ACTUAL_TOTAL
tiers=[t for t,_ in LIAB_TIERS]; amts=[a for _,a,_,_ in LIAB_TABLE]
conds=["일반 SLA 위반\n(크레딧)","이관 6종 미통과\noutput 미달","보안 사고\n(유출·로그 훼손)","고의·중과실만\nAI 판정·법정 판정 제외"]
fig, ax = plt.subplots(figsize=(7.8, 4.2))
cols=[TEAL,NAVY,"#8A6D3B",RUST]
bars=ax.bar(range(4),amts,color=cols,width=0.55,zorder=2)
for i,(a,row) in enumerate(zip(amts,LIAB_TABLE)):
    ax.text(i,a+0.15,f"{a:.2f}억\n공헌의 {row[2]}% · 현금의 {row[3]}%",ha="center",fontsize=8,color=cols[i])
ax.axhline(CONTRIB_3Y,color=NAVY,lw=1.2,ls="--"); ax.text(3.35,CONTRIB_3Y+0.12,f"3년 공헌 {CONTRIB_3Y:.2f}억\n(21 − 6.12 − 6.66 − 2.70)",fontsize=7.8,color=NAVY,ha="right",va="bottom")
ax.axhline(CASH/10000,color=GREY,lw=1.2,ls=":"); ax.text(-0.35,CASH/10000+0.12,f"현금 {CASH/10000:.2f}억(D+800)",fontsize=7.8,color=GREY,va="bottom")
ax.set_xticks(range(4)); ax.set_xticklabels([f"{int(t*100)}%\n{c}" for t,c in zip(tiers,conds)],fontsize=8)
ax.set_ylim(0,9.6); ax.set_ylabel("배상액(억) — 연 청구 7.0억 기준")
ax.text(1.5,9.3,f"물리적 하한은 구축 실소요 {SETUP_ACTUAL_TOTAL}억으로(F-14): 1년차 현금 {YEAR1_CASH:.2f}억 — 3.00으로 계산하면 7억이 '감당 가능해 보인다'",ha="center",fontsize=7.8,color=RUST,va="top")
ax.set_title("배상 상한 4구간 — 금액이 아니라 조건으로 가른다", fontsize=10.5, loc="left")
fig.subplots_adjust(bottom=0.2)
save(fig,"fig_3_3_liability","E-13 · ㊲ 항목 5 · day8_enterprise.py LIAB_TABLE [추가 설정]")
