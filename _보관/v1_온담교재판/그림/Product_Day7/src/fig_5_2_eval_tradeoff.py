# -*- coding: utf-8 -*-
"""그림 5-2. eval v1 → v2 — FN이 내려가고 세 가지가 올라갔다"""
from mplcommon import *
from day7_pmf import R1, R2, V1, V2, AUTO_ON, AUTO_OFF, ADOPT
fig, axs = plt.subplots(1,4,figsize=(8.4,3.6))
items=[("FN(%)",R1["FN"]*100,R2["FN"]*100,"↓ 8.1 → 2.4"),("FP(%)",R1["FP"]*100,R2["FP"]*100,"↑ 14.6 → 21.3"),("단가(원)",V1["cost"],V2["cost"],"↑ ×2.1"),("지연(초)",V1["lat"],V2["lat"],"↑ ×2.4")]
for ax,(lab,a,b,note) in zip(axs,items):
    col=TEAL if b<a else RUST
    ax.bar([0,1],[a,b],color=[GREY,col],width=0.55,zorder=3)
    for i,v in enumerate([a,b]): ax.text(i,v*1.03,f"{v:.1f}",ha="center",fontsize=9,fontweight="bold")
    ax.set_xticks([0,1]); ax.set_xticklabels(["v1","v2"]); ax.set_title(lab,fontsize=9.5); ax.set_ylim(0,max(a,b)*1.3)
    ax.text(0.5,max(a,b)*1.2,note,ha="center",fontsize=8,color=col)
fig.text(0.5,0.07,f"자동판정 ON {AUTO_ON} / OFF {AUTO_OFF}  ·  채택률 ㉮ {ADOPT['a']:.0%}   ← 마지막 화살표(FP → 채택률)는 워크북 ㉞ 항목 5에서 여러분이 그린다",ha="center",fontsize=8.5,color=NAVY)
fig.subplots_adjust(bottom=0.3,wspace=0.4,top=0.82)
fig.suptitle("eval v1 → v2 — FN 하나가 내려가고 셋이 올라갔다", fontsize=10.5, x=0.01, ha="left")
save(fig,"fig_5_2_eval_tradeoff","정본 §7.3 V-03~05 · §8.1 · 분자는 day7_pmf.py [추가 설정]")
