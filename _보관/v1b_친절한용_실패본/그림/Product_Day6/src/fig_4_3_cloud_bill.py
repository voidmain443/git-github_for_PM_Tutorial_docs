# -*- coding: utf-8 -*-
"""그림 4-3. 청구서 780만 — 서비스별로는 보이고, 원인은 보이지 않는다"""
from mplcommon import *
from day6_seed import BILL_EXPECTED, BILL_ACTUAL, BILL_BY_SERVICE, HEAVY_EXCESS, HEAVY_MULT, HYPOTHESES
fig=plt.figure(figsize=(8.6,4.4)); gs=fig.add_gridspec(1,2,width_ratios=[1,1.35],wspace=0.35)
ax=fig.add_subplot(gs[0]); ax2=fig.add_subplot(gs[1]); ax2.axis("off")
ax.bar(0,BILL_EXPECTED,color=GREY,width=0.55,zorder=3); ax.text(0,BILL_EXPECTED+15,"예상 210",ha="center",fontsize=9.5,fontweight="bold")
y=0; cols=[NAVY,TEAL,SAND,"#BFBFBF"]
for (n,v),c in zip(BILL_BY_SERVICE,cols):
    ax.bar(1,v,bottom=y,color=c,edgecolor="white",width=0.55,zorder=3)
    if v>200: ax.text(1,y+v/2,f"{n} {v}",ha="center",va="center",fontsize=7.8,color="white")
    y+=v
ax.text(1,y+15,"실제 780",ha="center",fontsize=9.5,fontweight="bold"); ax.text(0.68,690,"STT 41 · 저장 58\nGPU 69 (위 세 조각)",fontsize=7,color="#333",ha="right")
ax.annotate("",xy=(1.42,780),xytext=(1.42,210),arrowprops=dict(arrowstyle="<->",color=RUST,lw=1.2)); ax.text(1.47,495,f"초과 570\n동보프레스 {HEAVY_EXCESS}(78%)\n= 원가표 69.5의 {HEAVY_MULT:.2f}배",fontsize=8,color=RUST,va="center")
ax.set_xticks([0,1]); ax.set_xticklabels(["예상(G-08)","12월 청구서(G-39)"]); ax.set_ylim(0,880); ax.set_xlim(-0.5,2.3); ax.set_ylabel("만 원")
ax2.text(0,0.98,"가설 4 — D+284에 어느 것도 확인할 수 없다",fontsize=10,fontweight="bold",color=NAVY,va="top")
for i,(h,t,resp,meas) in enumerate(HYPOTHESES):
    yy=0.86-i*0.185
    ax2.add_patch(plt.Rectangle((0,yy-0.14),1,0.165,fc="#EFEFEF",ec=GREY,lw=0.6,transform=ax2.transAxes))
    ax2.text(0.015,yy,f"{h}  {t}",fontsize=8.2,va="top",color="#333",transform=ax2.transAxes)
    ax2.text(0.015,yy-0.075,f"대응: {resp}   ·   판별 계측: {meas}",fontsize=7.4,va="top",color=GREY,transform=ax2.transAxes)
ax2.text(0,-0.02,"계측 가능: 테넌트별 API 호출 합계  ·  불가능: 사진 단위 재촬영·재시도·배치 구분\n→ 첫 조치는 계측(D+300 이후 첫 백로그 항목). 조항·경고는 신규·갱신부터, 소급하지 않는다.",fontsize=7.8,color=RUST,va="bottom",transform=ax2.transAxes)
fig.suptitle("청구서는 금액과 고객을 말하고, 원인은 말하지 않는다", fontsize=10.5, x=0.01, ha="left")
save(fig,"fig_4_3_cloud_bill","정본 §4.4·G-39(210 → 780, 동보 444 = 78%) · F-09 6.39배 · 서비스별 내역·가설 4는 워크북 ㉘ 항목 4 [추가 설정]")
