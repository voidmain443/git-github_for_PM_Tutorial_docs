# -*- coding: utf-8 -*-
"""그림 2-4. 이탈 7건 — 유형과 시점"""
from mplcommon import *
from day7_pmf import CHURN
types=["미온보딩","챔피언 이탈","가치 미실현","가격","경쟁·대체"]
fig, ax = plt.subplots(figsize=(7.2, 3.8))
seen={}
for i,(q,m,cust,t,why) in enumerate(CHURN):
    y=types.index(t); x=int(m[1:]); k=(x,y); n=seen.get(k,0); seen[k]=n+1; x=x+0.32*n; y=y+0.0; col={"미온보딩":RUST,"가치 미실현":NAVY}.get(t,GREY)
    ax.plot(x,y,"o",color=col,ms=11,zorder=3); ax.text(x+0.13,y+0.12+0.3*n,f"{cust}({q})",fontsize=7.6,color="#333")
ax.set_yticks(range(5)); ax.set_yticklabels(types); ax.set_xlim(1.4,6.2); ax.set_ylim(-0.7,4.7); ax.set_xlabel("이탈 시점(M)"); ax.set_xticks([2,3,4,5])
ax.axvspan(1.5,2.5,color=RUST,alpha=0.06); ax.axvspan(3.5,5.5,color=NAVY,alpha=0.06)
ax.text(2.0,4.45,"M2 — 온보딩",fontsize=8,color=RUST,ha="center"); ax.text(4.5,4.45,"M4~M5 — 가치",fontsize=8,color=NAVY,ha="center")
ax.invert_yaxis()
fig.subplots_adjust(left=0.2,bottom=0.18)
ax.set_title("이탈 7건 — 시점이 유형을 가른다. 가격은 하나뿐이다", fontsize=10.5, loc="left")
save(fig,"fig_2_4_churn_types","워크북 ㉛ 항목 5 [추가 설정] — 정본 §3.3 이탈 7")
