# -*- coding: utf-8 -*-
"""그림 2-1. 자사 삼각행렬 — 가로·세로·대각선 세 방향"""
from mplcommon import *
from day7_pmf import COHORTS
import numpy as np
C=COHORTS["Ret-C 자사"]; qs=["26Q4","27Q1","27Q2"]
fig, ax = plt.subplots(figsize=(8.0, 3.9)); ax.axis("off")
ax.set_xlim(0,11.6); ax.set_ylim(-0.6,4.2)
ax.text(0.2,3.75,"코호트",fontsize=9,fontweight="bold"); ax.text(1.55,3.75,"분모",fontsize=9,fontweight="bold")
for m in range(7): ax.text(2.6+m*1.0+0.45,3.75,f"M{m}",fontsize=9,fontweight="bold",ha="center")
for i,q in enumerate(qs):
    row=C[q]; y=3.0-i*0.95
    ax.text(0.2,y,q,fontsize=9.5); ax.text(1.6,y,str(row[0]),fontsize=9.5,ha="center")
    for m in range(7):
        v=row[m+1]; x=2.6+m*1.0
        if v is None:
            ax.add_patch(plt.Rectangle((x,y-0.35),0.92,0.8,fc="#EFEFEF",ec="white",hatch="///")); ax.text(x+0.46,y,"▨",fontsize=9,ha="center",color=GREY)
        else:
            p=v/row[0]; col=plt.cm.Blues(0.25+0.6*p)
            ax.add_patch(plt.Rectangle((x,y-0.35),0.92,0.8,fc=col,ec="white"))
            ax.text(x+0.46,y+0.1,f"{v}",fontsize=9.5,ha="center",color="white" if p>0.75 else "#222",fontweight="bold")
            ax.text(x+0.46,y-0.2,f"{p:.0%}",fontsize=7.5,ha="center",color="white" if p>0.75 else "#333")
# 가로: 27Q1 평탄
ax.annotate("",xy=(9.5,2.05),xytext=(7.7,2.05),arrowprops=dict(arrowstyle="->",color=RUST,lw=1.4,alpha=0.8))
ax.text(9.65,2.05,"가로 — M5→M6\n71% 평탄",fontsize=7.5,color=RUST,va="center")
# 세로: M4
ax.annotate("",xy=(7.06,0.35),xytext=(7.06,3.0),arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.4))
ax.text(7.15,-0.2,"세로 — M4: 67 → 79 → 83 개선",fontsize=7.5,color=TEAL,ha="left")
ax.text(9.65,1.1,"가장 젊고\n가장 높다",fontsize=7,color=GREY,va="center")
ax.text(0.2,-0.45,"27Q3 신규 9는 격자 밖(M0~M1) · 유료 31 = 2 + 10 + 10 + 9",fontsize=7.5,color=GREY)
ax.set_title("자사 삼각행렬 Ret-C — 분자와 %를 함께", fontsize=10.5, loc="left")
save(fig,"fig_2_1_triangle","정본 §7.2 Ret-C · day7_pmf.py 검산")
