# -*- coding: utf-8 -*-
"""그림 2-2. 47건 — 저자별 공수 × 3분류, 차원별 분포"""
from mplcommon import *
from day8_enterprise import REQ, P, C, R, AUTHOR_MM, DIM_MM, DIM_N
authors=list(AUTHOR_MM.keys()); cls=[(P,TEAL),(C,NAVY),(R,RUST)]
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), gridspec_kw=dict(width_ratios=[1.25,1]))
ax=axes[0]; bottom=[0]*len(authors)
for k,col in cls:
    vals=[sum(r[4] for r in REQ if r[2]==a and r[6]==k) for a in authors]
    ax.bar(range(len(authors)),vals,bottom=bottom,color=col,width=0.6,label=k,zorder=2)
    for i,v in enumerate(vals):
        if v>=3: ax.text(i,bottom[i]+v/2,str(v),ha="center",va="center",fontsize=8,color="white")
    bottom=[b+v for b,v in zip(bottom,vals)]
for i,a in enumerate(authors): ax.text(i,bottom[i]+1.2,f"{bottom[i]} mm\n{sum(1 for r in REQ if r[2]==a)}건",ha="center",fontsize=8,color=NAVY)
ax.set_xticks(range(len(authors))); ax.set_xticklabels([f"{a}\n{ {'나영선':'품질안전','한동석':'물류','박세연':'IT','오정근':'영업','최영주':'준법'}[a]}" for a in authors],fontsize=8.5)
ax.set_ylim(0,75); ax.set_ylabel("공수(mm)"); ax.legend(fontsize=8,frameon=False,loc="upper right")
ax.set_title("저자별 공수 → 3분류: 제품화 27 / 유상 59 / 거절 52 mm", fontsize=9.5, loc="left")
ax=axes[1]; dims=["①","②","③","④","⑤","—"]
ax.bar(range(6),[DIM_MM[d] for d in dims],color=[NAVY]*5+[GREY],width=0.6,zorder=2)
for i,d in enumerate(dims): ax.text(i,DIM_MM[d]+1,f"{DIM_MM[d]} mm\n{DIM_N[d]}건",ha="center",fontsize=8,color=NAVY)
ax.set_xticks(range(6)); ax.set_xticklabels(["① 라벨","② 식별자","③ 단위","④ 규격","⑤ 흐름","5차원 밖"],fontsize=8); ax.set_ylim(0,55)
ax.set_title("차원별 — 거절 52 중 ②가 25", fontsize=9.5, loc="left")
fig.subplots_adjust(wspace=0.22,bottom=0.16)
save(fig,"fig_2_2_requests","day8_enterprise.py REQ [추가 설정] · 저자별 건수·공수는 정본 §4.12·E-10")
