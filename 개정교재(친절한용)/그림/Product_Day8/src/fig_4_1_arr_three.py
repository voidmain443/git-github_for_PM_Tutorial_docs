# -*- coding: utf-8 -*-
"""그림 4-1. ARR 세 값과 집중 리스크 3표기"""
from mplcommon import *
from day8_enterprise import ARR_IR, ARR_CHECK, LIC_YEAR, BILL_YEAR, CONC_IR, CONC_CHECK, TOTAL_MM, ANNUAL_MM
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), gridspec_kw=dict(width_ratios=[1.2,1]))
ax=axes[0]
labs=["IR 기재\n(온담 연 청구 전액)","검산\n(라이선스만)","온담 제외"]
base=[11.9,11.9,11.9]; add=[BILL_YEAR,LIC_YEAR,0]
ax.bar(range(3),base,color=NAVY,width=0.55,zorder=2,label="자동차 58사 계약 ARR 11.9")
ax.bar(range(3),add,bottom=base,color=[RUST,TEAL,"white"],width=0.55,zorder=2)
for i,(b,a) in enumerate(zip(base,add)):
    ax.text(i,b+a+0.3,f"{b+a:.2f}억" if i==1 else f"{b+a:.1f}억",ha="center",fontsize=10,fontweight="bold",color=[RUST,TEAL,NAVY][i])
    if a: ax.text(i,b+a/2,f"온담 {a:.2f}",ha="center",va="center",fontsize=8.5,color="white")
ax.text(0,6,"11.9",ha="center",color="white",fontsize=8.5); ax.text(1,6,"11.9",ha="center",color="white",fontsize=8.5); ax.text(2,6,"11.9",ha="center",color="white",fontsize=8.5)
ax.set_xticks(range(3)); ax.set_xticklabels(labs,fontsize=8.5); ax.set_ylim(0,22); ax.set_ylabel("ARR(억)")
ax.text(2,20.3,"18.9에는 구축 3.0 +\n운영 2.22가 들어 있다",ha="center",fontsize=7.6,color=RUST,va="top")
ax.set_title("ARR 세 값 — 18.9 / 15.68 / 11.9", fontsize=9.5, loc="left")
ax=axes[1]
vals=[CONC_IR*100,CONC_CHECK*100,TOTAL_MM/ANNUAL_MM*100]; cols=[RUST,TEAL,NAVY]
ax.bar(range(3),vals,color=cols,width=0.55,zorder=2)
for i,v in enumerate(vals): ax.text(i,v+1.5,f"{v:.1f}%",ha="center",fontsize=10,fontweight="bold",color=cols[i])
ax.set_xticks(range(3)); ax.set_xticklabels(["ARR 비중\nIR 기재\n7.0/18.9","ARR 비중\n검산\n3.78/15.68","개발 용량\n잠식\n138/168"],fontsize=8.2); ax.set_ylim(0,100)
ax.text(0,52,"과대",ha="center",fontsize=8,color=RUST); ax.text(1,38,"적정",ha="center",fontsize=8,color=TEAL); ax.text(2,95,"IR 덱에 없다",ha="center",fontsize=8,color=NAVY,va="top")
ax.set_title("집중 리스크 3표기 — 세 번째를 우리가 먼저", fontsize=9.5, loc="left")
fig.subplots_adjust(wspace=0.28,bottom=0.22)
save(fig,"fig_4_1_arr_three","정본 §3.4 · E-04·07·08·11")
