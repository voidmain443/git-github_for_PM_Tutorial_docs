# -*- coding: utf-8 -*-
"""그림 2-3. 손실 7.0의 분해 — 퇴사가 원인인 것과 그 전에 새어 나간 것"""
from mplcommon import *
from day6_seed import LOSS, CAP_V10, CAP_V11
labels=["가용 24\n(v1.0)"]+["조현우 잔여\n2.17개월","태산정밀 커스텀\n(계획 외)","인수인계·채용","WIP 폐기","B-02 조도\n재작업 초과"]+["가용 17\n(v1.1)"]
vals=[l[1] for l in LOSS]; due=[True,False,True,True,False]   # 퇴사가 원인인가
fig, ax = plt.subplots(figsize=(8.0, 4.2))
ax.bar(0,CAP_V10,color=NAVY,width=0.6,zorder=3); ax.text(0,CAP_V10+0.3,"24.0",ha="center",fontsize=9.5,fontweight="bold")
top=CAP_V10
for i,(v,d) in enumerate(zip(vals,due),1):
    ax.bar(i,v,bottom=top-v,color=NAVY if d else RUST,alpha=0.85 if d else 0.75,width=0.6,zorder=3)
    ax.text(i,top+0.3,f"-{v:.1f}",ha="center",fontsize=9,color=NAVY if d else RUST); ax.plot([i-0.3,i+0.7],[top-v]*2,color=GREY,lw=0.6,ls=":")
    top-=v
ax.bar(6,CAP_V11,color=TEAL,width=0.6,zorder=3); ax.text(6,CAP_V11+0.3,"17.0",ha="center",fontsize=9.5,fontweight="bold")
ax.set_xticks(range(7)); ax.set_xticklabels(labels,fontsize=8); ax.set_ylim(0,27); ax.set_ylabel("man-month")
ax.text(0.6,4.5,"짙은 계단(2.2 + 1.0 + 0.7 = 3.9) — 퇴사가 원인\n붉은 계단(2.2 + 0.9 = 3.1) — 퇴사 전에 새어 나간 것",fontsize=8.5,color="#333",bbox=dict(boxstyle="round",fc="white",ec=GREY,lw=0.6))
ax.set_title("24 → 17 — 손실 7.0의 다섯 계단", fontsize=10.5, loc="left")
save(fig,"fig_2_3_capacity_loss","day6_seed.py LOSS [추가 설정 — G-37 24 → 17] · 정본 §4.3 조현우 퇴사 사유 '커스터마이징 요청만 하다가 끝난다' = 두 번째 계단")
