# -*- coding: utf-8 -*-
"""그림 4-3. 5.8에서 1.12까지 — 가정을 하나씩 바꾸면"""
from mplcommon import *
from day7_pmf import ACV_CONTRACT, ACV_SAAS, GM_IR, GM_CHECK, LIFE_IR_YEARS, LIFE_CHECK_YEARS, CAC, CAC_PAID
steps=[("IR 덱\n계약 ACV·GM 61%\n수명 3.75년·CAC 620",ACV_CONTRACT*GM_IR*LIFE_IR_YEARS/CAC["blended"]),
       ("ACV → 순 SaaS\n1,226",ACV_SAAS*GM_IR*LIFE_IR_YEARS/CAC["blended"]),
       ("GM → 49.8%",ACV_SAAS*GM_CHECK*LIFE_IR_YEARS/CAC["blended"]),
       ("수명 → 코호트\n1.93년",ACV_SAAS*GM_CHECK*LIFE_CHECK_YEARS/CAC["blended"]),
       ("CAC → 유료 획득\n1,051",ACV_SAAS*GM_CHECK*LIFE_CHECK_YEARS/CAC_PAID)]
fig, ax = plt.subplots(figsize=(7.8, 4.0))
cols=[GREY,"#6B8FB5","#4F6D8F",NAVY,RUST]
for i,((lab,v),c) in enumerate(zip(steps,cols)):
    ax.bar(i,v,color=c,width=0.6,zorder=3); ax.text(i,v+0.12,f"{v:.2f}" if i else f"{v:.1f}",ha="center",fontsize=10,fontweight="bold")
    if i: ax.text(i,-0.55,f"×{v/steps[i-1][1]:.2f}",ha="center",fontsize=8,color=RUST)
ax.set_xticks(range(5)); ax.set_xticklabels([s[0] for s in steps],fontsize=7.8); ax.set_ylim(-0.9,6.8); ax.set_ylabel("LTV : CAC")
ax.axhline(3,ls="--",color=GREY,lw=0.9); ax.text(4.3,3.1,"3:1(벤치마크)",fontsize=7.5,color=GREY,ha="right")
ax.text(-0.3,6.4,"가장 큰 계단은 수명(×0.52) — 그 데이터(코호트)는 이미 ㉛에 있었다",fontsize=8,color=NAVY)
fig.subplots_adjust(bottom=0.22)
ax.set_title("같은 데이터의 세 답 — 5.8 / 1.9 / 1.12", fontsize=10.5, loc="left")
save(fig,"fig_4_3_ltv_ladder","정본 §3.3 LTV:CAC 5.8 / 1.9 / 1.12 · 가정 값은 워크북 ㉝ 항목 4 [추가 설정] · day7_pmf.py")
