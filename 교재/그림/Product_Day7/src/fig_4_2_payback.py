# -*- coding: utf-8 -*-
"""그림 4-2. 채널별 payback — 매출 기준·GM 61%·GM 49.8%"""
from mplcommon import *
from day7_pmf import CAC, CANON_PAYBACK, CAC_PAID, PAYBACK
import numpy as np
chs=list(CAC.keys()); x=np.arange(len(chs)); w=0.26
vals=[[CANON_PAYBACK[c][0] for c in chs],[CANON_PAYBACK[c][1] for c in chs],[CANON_PAYBACK[c][2] for c in chs]]
fig, ax = plt.subplots(figsize=(7.8, 4.0))
for i,(v,lab,col) in enumerate(zip(vals,["IR 기재 — 매출 기준(GM 미반영)","GM 61%(계약 분모)","GM 49.8%(순 SaaS 분모)"],[GREY,"#6B8FB5",NAVY])):
    b=ax.bar(x+(i-1)*w,v,w,color=col,label=lab,zorder=3)
    for bb,vv in zip(b,v): ax.text(bb.get_x()+bb.get_width()/2,vv+0.4,f"{vv:.1f}",ha="center",fontsize=7.5)
ax.axhline(12,ls="--",color=RUST,lw=1); ax.text(-0.45,12.5,"12개월 — 벤치마크",fontsize=7.5,color=RUST,ha="left")
ax.set_xticks(x); ax.set_xticklabels([f"{c}\nCAC {CAC[c]:,}만" for c in chs],fontsize=8.5); ax.set_ylabel("payback(개월)"); ax.set_ylim(0,33)
ax.legend(loc="upper left",fontsize=8,frameon=False)
ax.text(2.55,26,f"오가닉 41% 제외 → 유료 획득 CAC {CAC_PAID:,.0f}만\n→ payback 약 20.7개월(GM 49.8%)",fontsize=8,color=NAVY,ha="left",bbox=dict(boxstyle="round",fc="white",ec=NAVY,lw=0.6))
fig.subplots_adjust(bottom=0.2)
ax.set_title("아웃바운드 28.9개월이 열 달 보이지 않은 이유 — IR의 10.9", fontsize=10.5, loc="left")
save(fig,"fig_4_2_payback","정본 §3.3 CAC·payback 표 · G-21~24·G-41 · day7_pmf.py")
