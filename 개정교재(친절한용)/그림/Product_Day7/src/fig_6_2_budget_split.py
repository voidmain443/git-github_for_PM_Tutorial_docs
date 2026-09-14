# -*- coding: utf-8 -*-
"""그림 6-2. 예산 3분리 — 사고 전 습관과 사고 후 분기"""
from mplcommon import *
from day7_pmf import BUDGET_SPLIT, QUARTER_MM, RESERVE
before=[("차별화",65,NAVY),("위생",35,"#6B8FB5"),("신뢰 복구",0,RUST)]
after=[(n,p,{"차별화":NAVY,"위생":"#6B8FB5","신뢰 복구":RUST}[n]) for n,p,_ in BUDGET_SPLIT]
fig, ax = plt.subplots(figsize=(7.0, 3.9))
for i,(lab,segs) in enumerate([("사고 전 습관\n(가상)",before),("2027-Q4\n사고 후 분기",after)]):
    y=0
    for n,p,c in segs:
        if p==0: continue
        ax.bar(i,p,bottom=y,color=c,edgecolor="white",width=0.5,zorder=3); ax.text(i,y+p/2,f"{n} {p}%",ha="center",va="center",fontsize=9,color="white"); y+=p
ax.set_xticks([0,1]); ax.set_xticklabels(["사고 전 습관(가상)","2027-Q4 — 사고 후 분기"]); ax.set_ylim(0,112); ax.set_ylabel("배분 비율(%)")
alloc=QUARTER_MM*(1-RESERVE)
ax.text(-0.35,106,f"개발 11명 × 3개월 = {QUARTER_MM} mm · 예비 25% = {QUARTER_MM*RESERVE:.2f} · 배분 {alloc:.2f} mm — 신뢰 복구 35% = {alloc*0.35:.1f} mm(재발 방지 6건 ≈ 8 mm)",fontsize=7.8,color=GREY)
ax.set_title("사고 후 분기 — 차별화가 처음으로 과반이 아니다", fontsize=10.5, loc="left")
save(fig,"fig_6_2_budget_split","워크북 ㉟ 항목 3 [추가 설정] · SRE error budget policy의 제품판")
