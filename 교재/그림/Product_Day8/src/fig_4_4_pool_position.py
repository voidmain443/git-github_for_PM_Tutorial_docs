# -*- coding: utf-8 -*-
"""그림 4-4. 옵션풀의 위치 — pre vs post, 1.29%p"""
from mplcommon import *
from day8_enterprise import PCT3A, PCT3POST, PRICE_A, PRICE_POST, SH_A, SH_POST, POOL_SHIFT, POOL_VALUE_A, POOL_NEW_A
names=["강민수","오세진","윤하경","노들","SAFE","옵션풀","한강"]
fig, ax = plt.subplots(figsize=(7.8, 4.0))
x=range(len(names)); w=0.36
a=[PCT3A[n] for n in names]; b=[PCT3POST[n] for n in names]
ax.bar([i-w/2 for i in x],a,width=w,color=RUST,label=f"풀 pre-money(한강 제안) — 주당 {PRICE_A:,} · 한강 {SH_A:,}주",zorder=2)
ax.bar([i+w/2 for i in x],b,width=w,color=TEAL,label=f"같은 풀 post-money — 주당 {PRICE_POST:,} · 한강 {SH_POST:,}주",zorder=2)
for i,(p,q) in enumerate(zip(a,b)):
    ax.text(i-w/2,p+0.4,f"{p:.2f}",ha="center",fontsize=7.6,color=RUST); ax.text(i+w/2,q+0.4,f"{q:.2f}",ha="center",fontsize=7.6,color=TEAL)
    d=q-p; ax.text(i,max(p,q)+2.6,f"{d:+.2f}%p",ha="center",fontsize=8,fontweight="bold",color=NAVY if d>=0 else RUST)
ax.set_xticks(list(x)); ax.set_xticklabels(names,fontsize=9); ax.set_ylim(0,32); ax.set_ylabel("지분(%)")
ax.legend(fontsize=7.6,frameon=False,loc="upper right")
ax.text(3,24.5,f"같은 {POOL_NEW_A:,}주를 pre에 두면 주당가가 {PRICE_POST:,} → {PRICE_A:,}으로 내려가고\n한강이 같은 80억으로 {SH_A-SH_POST:,}주를 더 받는다 = {POOL_SHIFT:.2f}%p = 풀 가치 {POOL_VALUE_A:.1f}억\n(시드 0.43%p의 시리즈A 판 — 풀 4배 · 밸류 6.7배)",ha="center",fontsize=7.8,color="#333")
ax.set_title("옵션풀의 위치 — '표준 문구예요'의 값은 1.29%p", fontsize=10.5, loc="left")
fig.subplots_adjust(bottom=0.14)
save(fig,"fig_4_4_pool_position","정본 K-04 · post 방식 정의는 day8_enterprise.py (정본 §7.5와 같은 정의)")
