# -*- coding: utf-8 -*-
"""그림 2-3. 용량 잠식 4 시나리오"""
from mplcommon import *
from day8_enterprise import CAPACITY, DEV, ANNUAL_MM, EPILOGUE_MM
names=list(CAPACITY.keys()); mm=[CAPACITY[n][0] for n in names]; mon=[CAPACITY[n][1] for n in names]; pct=[CAPACITY[n][2] for n in names]
fig, ax = plt.subplots(figsize=(8.2, 4.0))
cols=[RUST,NAVY,TEAL,GREY]
bars=ax.barh(range(4),mm,color=cols,height=0.55,zorder=2)
for i,(m,mo,p) in enumerate(zip(mm,mon,pct)):
    ax.text(m+2,i,f"{m} mm = {DEV}명 × {mo}개월 = 연간 용량의 {p}%" if m else "0 mm — 대한기공 2.4억, 커스텀 0",va="center",fontsize=8.5,color=cols[i])
ax.set_yticks(range(4)); ax.set_yticklabels(["47건 전부 수용","분류 후\n(제품화 27 + 유상 59)","유상 커스텀만(59)","딜 거절 → 대한기공"],fontsize=8.5)
ax.axvline(ANNUAL_MM,color=GREY,lw=1,ls="--"); ax.text(ANNUAL_MM+2,2.5,f"연간 용량 {ANNUAL_MM} mm\n(14명 × 12)",fontsize=7.8,color=GREY,va="center")
ax.axvline(72,color=TEAL,lw=1.2,ls=":"); ax.text(72-1.5,3.45,"상한 6 FTE\n= 연 72 mm",fontsize=7.8,color=TEAL,va="center",ha="right")
ax.axvline(EPILOGUE_MM,color=RUST,lw=1.2,ls=":"); ax.text(EPILOGUE_MM+2,-0.62,"에필로그 14명 × 7개월 = 98 mm (§7 봉인)",fontsize=7.8,color=RUST,va="center")
ax.set_xlim(0,230); ax.set_ylim(3.8,-0.9); ax.set_xlabel("공수(man-month)")
ax.set_title("돈을 받아도 시간은 돌아오지 않는다 — 분류 후에도 절반(51.2%)", fontsize=10.5, loc="left")
fig.subplots_adjust(left=0.2,bottom=0.16)
save(fig,"fig_2_3_capacity","E-10·11 · day8_enterprise.py CAPACITY [추가 설정]")
