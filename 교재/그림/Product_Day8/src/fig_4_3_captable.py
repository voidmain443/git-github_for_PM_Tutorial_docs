# -*- coding: utf-8 -*-
"""그림 4-3. 캡테이블 T2 → T3 A안 / B안"""
from mplcommon import *
from day8_enterprise import PCT2, PCT3A, PCT3B, FD2, FD_A, FD_B, PRICE_A, PRICE_B
order=["강민수","오세진","윤하경","옵션풀","노들","SAFE","한강","코너스톤"]
colors={"강민수":NAVY,"오세진":"#3B5B8C","윤하경":"#6D86AE","옵션풀":SAND,"노들":TEAL,"SAFE":"#7FBBA6","한강":RUST,"코너스톤":"#E39A86"}
cols=[("T2 (SAFE 후)\nFD 1,305,556",PCT2),(f"A안 한강\nFD {FD_A:,} · {PRICE_A:,}원",PCT3A),(f"B안 코너스톤\nFD {FD_B:,} · {PRICE_B:,}원",PCT3B)]
fig, ax = plt.subplots(figsize=(7.6, 4.4))
for i,(lab,d) in enumerate(cols):
    bottom=0
    for k in order:
        if k not in d: continue
        v=d[k]; ax.bar(i,v,bottom=bottom,color=colors[k],width=0.56,edgecolor="white",lw=0.6,zorder=2)
        if v>=3: ax.text(i,bottom+v/2,f"{k} {v:.2f}",ha="center",va="center",fontsize=7.6,color="white" if k not in ("옵션풀","SAFE") else "#222")
        bottom+=v
ax.set_xticks(range(3)); ax.set_xticklabels([c[0] for c in cols],fontsize=8.5); ax.set_ylim(0,110); ax.set_ylabel("지분(%)")
ax.annotate("풀 +112,745주(15% pre → 실질 12.00)",xy=(1,PCT3A["강민수"]+PCT3A["오세진"]+PCT3A["윤하경"]+PCT3A["옵션풀"]/2),xytext=(1,104),fontsize=7.6,ha="center",color="#555",arrowprops=dict(arrowstyle="->",color=GREY,lw=0.8))
ax.set_title("같은 80억 — A안 20.00% / B안 21.62%. 강민수 25.38 / 27.01", fontsize=10.5, loc="left")
fig.subplots_adjust(bottom=0.16)
save(fig,"fig_4_3_captable","정본 K-03·04·05 · day8_enterprise.py")
