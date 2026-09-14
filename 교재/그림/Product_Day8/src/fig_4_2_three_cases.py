# -*- coding: utf-8 -*-
"""그림 4-2. 재무모델 3케이스 — 24개월 ARR과 현금"""
from mplcommon import *
from day8_enterprise import CASES, FIN, CASH0, A_IN, PRE_CLOSE_BURN
fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.9))
cols={"Bear":RUST,"Base":NAVY,"Bull":TEAL}
ax=axes[0]
for k,c in CASES.items():
    arr0=58*2052/10000; pts=[(0,arr0),(12,FIN[k]["ARR12"]),(24,FIN[k]["ARR24"])]
    ax.plot([p[0] for p in pts],[p[1] for p in pts],marker="o",color=cols[k],lw=2,label=k)
    ax.text(24.4,FIN[k]["ARR24"],f"{FIN[k]['ARR24']:.1f}",fontsize=8.5,color=cols[k],va="center")
    ax.text(12.4,FIN[k]["ARR12"]+(1.3 if k=="Bull" else -1.4),f"{FIN[k]['ARR12']:.1f}",fontsize=8,color=cols[k],va="center")
ax.text(0.3,58*2052/10000-3.2,"11.9(온담 제외)",fontsize=7.8,color=GREY)
ax.set_xticks([0,12,24]); ax.set_xticklabels(["2028-05\n(D+800)","+12개월","+24개월"],fontsize=8.5); ax.set_ylabel("ARR 검산(억) — 온담 라이선스 3.78만 ARR"); ax.set_xlim(-1,28); ax.set_ylim(0,48)
ax.legend(fontsize=8,frameon=False,loc="upper left"); ax.set_title("ARR — Bear 온담 거절 / Base 3분류 수용 / Bull + 식품 3사", fontsize=9.2, loc="left")
ax=axes[1]
for k,c in CASES.items():
    cash=[CASH0]; 
    for m in range(1,25):
        b=PRE_CLOSE_BURN if m<=6 else c["burn"][(m-7)//6]
        v=cash[-1]-b+(A_IN if m==6 else 0); cash.append(v)
    ax.plot(range(25),cash,color=cols[k],lw=2,label=k)
    ax.text(24.4,cash[-1],f"{cash[-1]:.1f}억 / {FIN[k]['runway']}개월",fontsize=7.8,color=cols[k],va="center")
ax.annotate(f"클로징 직전 {CASH0-6*PRE_CLOSE_BURN:.1f}억 — 런웨이 8.9개월 안에\n클로징이 있어야 한다(코너스톤 D+930은 빠듯)",xy=(5.6,CASH0-6*PRE_CLOSE_BURN),xytext=(7.5,6),fontsize=7.6,color=RUST,arrowprops=dict(arrowstyle="->",color=RUST,lw=0.9))
ax.axvline(6,color=GREY,lw=0.8,ls=":"); ax.text(6.3,88,"시리즈A 80억 입금(D+1000)",fontsize=7.6,color=GREY)
ax.set_xticks([0,6,12,18,24]); ax.set_xlabel("개월"); ax.set_ylabel("현금(억)"); ax.set_xlim(-0.5,33); ax.set_ylim(0,95)
ax.set_title("현금 — 6개월차 바닥, 24개월 뒤 28.4 / 36.8 / 47.6", fontsize=9.2, loc="left")
fig.subplots_adjust(wspace=0.3,bottom=0.18)
save(fig,"fig_4_2_three_cases","day8_enterprise.py CASES·FIN [추가 설정] · G-15 7.52억")
