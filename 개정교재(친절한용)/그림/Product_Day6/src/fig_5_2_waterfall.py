# -*- coding: utf-8 -*-
"""그림 5-2. 매각가 3구간 — 참가적 1x와 비참가적, 투자자 몫"""
from mplcommon import *
from day6_seed import payout, EXITS
import numpy as np
ex=np.linspace(15,320,200); npart=[payout(e,0.20,False)[0] for e in ex]; part=[payout(e,0.20,True)[0] for e in ex]
fig, ax = plt.subplots(figsize=(7.6, 4.2))
ax.plot(ex,npart,color=NAVY,lw=2,label="비참가적 1x — max(12, 20% × 매각가)"); ax.plot(ex,part,color=RUST,lw=2,label="참가적 1x — 12 + 20% × (매각가 - 12)")
ax.fill_between(ex,npart,part,color=RUST,alpha=0.12)
for e in EXITS:
    a=payout(e,0.20,False)[0]; b=payout(e,0.20,True)[0]
    ax.plot([e,e],[a,b],color=GREY,lw=0.8,ls=":"); ax.text(e+3,(a+b)/2,f"{b-a:.1f}억",fontsize=8.5,color=RUST,va="center")
    ax.plot(e,a,"o",color=NAVY,ms=4); ax.plot(e,b,"o",color=RUST,ms=4)
ax.axvline(60,color=GREY,lw=0.6,ls="--"); ax.text(62,38,"60억 — 비참가적이 전환하는 점",fontsize=7.5,color=GREY)
ax.set_xlabel("매각가 (억 원)"); ax.set_ylabel("투자자 몫 (억 원)"); ax.set_xlim(15,320); ax.set_ylim(0,75)
ax.legend(loc="upper left",fontsize=8,frameon=False)
rows=[("30억","12.6"),("100억","61.6"),("300억","201.6")]
ax.text(200,10,"창업자 3인 합계(참가적·풀 pre 70%)\n"+"\n".join(f"{a}: {b}" for a,b in rows),fontsize=8,color="#333",bbox=dict(boxstyle="round",fc="white",ec=GREY,lw=0.6))
ax.set_title('"참가적" 한 단어의 값 — 100억에서 9.6억', fontsize=10.5, loc="left")
save(fig,"fig_5_2_waterfall","정본 §3.2 참가적 1x · 워크북 ㉚ 항목 3 [추가 설정 — 매각가 30/100/300] · day6_seed.py payout()")
