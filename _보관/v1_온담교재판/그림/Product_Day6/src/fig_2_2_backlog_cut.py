# -*- coding: utf-8 -*-
"""그림 2-2. 백로그 41 mm의 두 절단 — 41 → 24 → 17"""
from mplcommon import *
from day6_seed import MOSCOW, reserve_v10, done_mm, WIP_KEPT, reserve_used, rem_must, rem_should, rem_res
fig, ax = plt.subplots(figsize=(7.6, 4.3))
bars=[("백로그 견적\n41.0",[("Must",MOSCOW["Must"],NAVY),("Should",MOSCOW["Should"],TEAL),("Could",MOSCOW["Could"],SAND),("Won't",MOSCOW["Won't"],"#BFBFBF")]),
      ("v1.0 가용 24\n(D+130)",[("Must",MOSCOW["Must"],NAVY),("Should",MOSCOW["Should"],TEAL),("예비",reserve_v10,"#DCE6F2")]),
      ("v1.1 가용 17\n(D+235)",[("완료 Must",done_mm,NAVY),("WIP",sum(WIP_KEPT.values()),"#4F6D8F"),("예비 사용",reserve_used,"#DCE6F2"),("남은 Must",rem_must,"#6B8FB5"),("남은 Should",rem_should,TEAL),("남은 예비",rem_res,"#DDF0E8")])]
for i,(lab,segs) in enumerate(bars):
    y=0
    for name,v,c in segs:
        ax.bar(i,v,bottom=y,color=c,edgecolor="white",width=0.58,zorder=3)
        if v>=1.2: ax.text(i,y+v/2,f"{name} {v:g}",ha="center",va="center",fontsize=8,color="white" if c in (NAVY,TEAL,"#4F6D8F","#6B8FB5") else "#333")
        y+=v
    ax.text(i,y+0.6,f"{y:g} mm",ha="center",fontsize=9.5,fontweight="bold")
ax.plot([0.7,1.3],[24*0.6]*2,ls="--",color=GREY,lw=1); ax.text(1.32,24*0.6,"Must 60% = 14.4",fontsize=7.5,color=GREY,va="center")
ax.text(2.32,13.6,"작은 조각(위에서): 남은 Should 1.5 · 남은 Must 1.1\n예비 사용 0.8 · WIP 0.7",fontsize=7.2,color="#333",va="center")
ax.plot([1.7,2.3],[17*0.6]*2,ls="--",color=GREY,lw=1); ax.text(2.32,17*0.6,"60% = 10.2\n(완료 10.0이 이미 여기)",fontsize=7.5,color=GREY,va="center")
ax.set_xticks(range(3)); ax.set_xticklabels([b[0] for b in bars]); ax.set_ylim(0,46); ax.set_ylabel("man-month")
ax.text(-0.45,44,"41 - 18 = 23이 백로그 밖(Could 12 · Won't 11) — 예비 6은 항목이 아니다. 17에서는 이미 쓴 10.7이 되돌아오지 않는다 → 남은 5.5로 나눈다.",fontsize=7.6,color=GREY)
ax.set_title("백로그 41 mm의 두 절단", fontsize=10.5, loc="left")
save(fig,"fig_2_2_backlog_cut","day6_seed.py 백로그 29건 [추가 설정 — G-37·G-38] · 워크북 ㉖ 항목 2·3")
