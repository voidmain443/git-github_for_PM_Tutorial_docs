# -*- coding: utf-8 -*-
"""그림 5-1. 캡테이블 T0 → T1 — 주식수는 그대로, 지분은 × 0.8"""
from mplcommon import *
from day6_seed import T0, T1, FD0, FD1, PRICE
names=["강민수","오세진","윤하경","옵션풀","노들투자파트너스(RCPS)"]; cols=[NAVY,"#4F6D8F","#6B8FB5",SAND,TEAL]
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for i,(tab,fd,lab) in enumerate([(T0,FD0,"T0 설립 (K-01)\n1,000,000주"),(T1,FD1,f"T1 시드 후 (K-02)\n1,250,000주 · 주당 {PRICE:,.0f}원")]):
    y=0
    for n,c in zip(names,cols):
        v=tab.get(n,0)
        if v:
            ax.bar(i,v/1000,bottom=y/1000,color=c,edgecolor="white",width=0.55,zorder=3)
            ax.text(i,(y+v/2)/1000,f"{n} {v:,}\n{v/fd:.1%}",ha="center",va="center",fontsize=8,color="white" if c!=SAND else "#333"); y+=v
    ax.text(i,y/1000+25,lab,ha="center",fontsize=8.5)
ax.set_xticks([0,1]); ax.set_xticklabels(["",""]); ax.set_ylim(0,1420); ax.set_ylabel("천 주"); ax.set_xlim(-0.5,1.5)
ax.text(-0.45,1380,"창업 3인·옵션풀의 막대 높이(주식수)는 같다 — 전체가 커져 비율이 준다(× 0.8). 신주 250,000 = 12억 ÷ 4,800원.",fontsize=8,color=GREY)
ax.set_title("캡테이블 T0 → T1", fontsize=10.5, loc="left")
save(fig,"fig_5_1_captable","정본 §7.5 K-01·K-02 · day6_seed.py 검산")
