# -*- coding: utf-8 -*-
"""그림 4-2. 유닛이코노믹스 v1 — 표준 공장과 헤비 고객, 같은 매출 135만"""
from mplcommon import *
from day6_seed import UE, UE_OUT
fig, ax = plt.subplots(figsize=(6.8, 4.2))
for i,(k,d) in enumerate(UE.items()):
    o=UE_OUT[k]; segs=[("추론비",o["infer"],NAVY),("STT",d["stt"],TEAL),("저장·전송",d["store"],SAND)]
    y=0
    for n,v,c in segs:
        ax.bar(i,v,bottom=y,color=c,edgecolor="white",width=0.55,zorder=3)
        if v>=6: ax.text(i,y+v/2,f"{n} {v:.1f}",ha="center",va="center",fontsize=8,color="white" if c!=SAND else "#333")
        y+=v
    ax.bar(i,o["rev"]-y,bottom=y,color="white",edgecolor=NAVY,width=0.55,zorder=3,hatch="")
    ax.text(i,y+(o["rev"]-y)/2,f"공헌이익\n{o['rev']-o['var']:.1f}만 ({o['cm']:.1%})",ha="center",va="center",fontsize=9,color=NAVY,fontweight="bold")
    ax.text(i,o["rev"]+3,f"매출 135만 = 라인 3.0 × 45만\n사진 {d['photos']:,}장 · 변동원가 {o['var']:.1f}만 ({o['var_rate']:.1%})",ha="center",fontsize=8)
ax.set_xticks([0,1]); ax.set_xticklabels(["표준 공장","헤비 고객(동보프레스)"]); ax.set_ylim(0,178); ax.set_ylabel("만 원 / 월")
ax.text(-0.3,172,"STT 3.8 · 저장·전송 1.2/3.6은 표시 생략. 공헌이익 0의 사진 수 ≈ (135 - 3.8 - 3.6)만 ÷ 32원 ≈ 39,900장 — 헤비의 두 배",fontsize=8,color=GREY)
ax.set_title("같은 가격, 사진 4.7배, 공헌이익률 38%p 차이", fontsize=10.5, loc="left")
save(fig,"fig_4_2_ue_two","정본 §3.2 프라이싱 v1 유닛이코노믹스 표 · day6_seed.py 검산")
