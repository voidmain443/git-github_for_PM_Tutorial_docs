# -*- coding: utf-8 -*-
"""그림 2-3. 동일 연령 M4 비교 — 네 곡선의 방향"""
from mplcommon import *
from day7_pmf import M4
fig, ax = plt.subplots(figsize=(6.8, 3.9))
x=[0,1,2]; labs=["26Q4","27Q1","27Q2"]
for name,lab,col,ls in [("Ret-C 자사","자사",NAVY,"-"),("Ret-B","익명 B",GREY,"-"),("Ret-A 재계산","익명 A 재계산",RUST,"-"),("Ret-A 인쇄","익명 A 인쇄(분모 효과)",RUST,":")]:
    y=M4[name]; ax.plot(x,y,ls=ls,color=col,lw=2.2,marker="o",ms=5,label=lab)
    for xi,yi in zip(x,y): ax.text(xi,yi+1.8,f"{yi}",fontsize=8,color=col,ha="center")
ax.set_xticks(x); ax.set_xticklabels(labs); ax.set_ylim(50,108); ax.set_ylabel("M4 잔존율(%)"); ax.set_xlabel("코호트")
ax.legend(loc="lower right",fontsize=8,frameon=False)
ax.text(-0.1,104,"방향이 높이보다 많은 것을 말한다 — 자사·B는 개선, A는 느린 개선, A 인쇄는 분모",fontsize=7.8,color=GREY)
fig.subplots_adjust(bottom=0.18)
ax.set_title("동일 연령 M4 — 코호트가 개선되는가", fontsize=10.5, loc="left")
save(fig,"fig_2_3_same_age","정본 §7.2 동일 연령(M4) 비교 · day7_pmf.py")
