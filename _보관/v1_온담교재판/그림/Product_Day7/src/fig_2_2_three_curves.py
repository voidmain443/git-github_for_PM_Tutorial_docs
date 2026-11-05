# -*- coding: utf-8 -*-
"""그림 2-2. 27Q1 코호트 — 익명 A 인쇄, 익명 A 재계산, 익명 B, 자사"""
from mplcommon import *
from day7_pmf import COHORTS
ms=list(range(7))
def curve(name,q="27Q1"):
    r=COHORTS[name][q]; return [x/r[0]*100 for x in r[1:] if x is not None]
fig, ax = plt.subplots(figsize=(7.6, 4.0))
for name,lab,col,ls in [("Ret-A 인쇄","익명 A 인쇄(분모 15 = 활성 계정)",RUST,"--"),("Ret-A 재계산","익명 A 재계산(분모 20 = 총 계약)",RUST,"-"),("Ret-C 자사","자사(분모 14)",NAVY,"-"),("Ret-B","익명 B(분모 22)",GREY,"-")]:
    y=curve(name); ax.plot(ms[:len(y)],y,ls=ls,color=col,lw=2.2 if name!="Ret-B" else 1.6,marker="o",ms=4,label=lab)
    ax.text(6.15,y[-1],f"{y[-1]:.0f}%",fontsize=8.5,color=col,va="center")
ya=curve("Ret-A 인쇄"); yb=curve("Ret-A 재계산")
ax.fill_between(ms,yb,ya,color=RUST,alpha=0.10); ax.text(3.2,82,"'분모 정의' 한 줄의 값",fontsize=8.5,color=RUST,ha="center")
ax.set_xlim(-0.2,6.9); ax.set_ylim(40,105); ax.set_xlabel("개월(M)"); ax.set_ylabel("잔존율(%)"); ax.set_xticks(ms)
ax.legend(loc="lower left",fontsize=8,frameon=False)
fig.subplots_adjust(bottom=0.18)
ax.set_title("27Q1 코호트 — 같은 회사가 두 곡선이 된다", fontsize=10.5, loc="left")
save(fig,"fig_2_2_three_curves","정본 §7.2 (Ret-A 인쇄 15 → 14 · 재계산 20 → 14 · Ret-C 14 → 10 · Ret-B 22 → 13)")
