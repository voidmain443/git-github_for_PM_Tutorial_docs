# -*- coding: utf-8 -*-
"""그림 5-3. 옵션풀의 위치 — pre면 주당가가 내려가고 기존 주주만 희석된다"""
from mplcommon import *
from day6_seed import PCT1, inv_post, fnd_post, inv_pre, fnd_pre, price_pre, PRICE
cases=[("실제 K-02\n추가 풀 없음",[("창업 3인",PCT1["강민수"]+PCT1["오세진"]+PCT1["윤하경"]),("옵션풀",PCT1["옵션풀"]),("노들",PCT1["노들투자파트너스(RCPS)"])],f"주당 {PRICE:,.0f}원"),
       ("풀 10% 요구 — post 기준\n(라운드 후 전체가 희석)",[("창업 3인",fnd_post),("옵션풀",0.10),("노들",inv_post)],f"주당 {PRICE:,.0f}원"),
       ("풀 10% 요구 — pre 기준\n(기존 주주만 희석)",[("창업 3인",fnd_pre),("옵션풀",0.10),("노들",inv_pre)],f"주당 {price_pre:,.0f}원")]
cols={"창업 3인":NAVY,"옵션풀":SAND,"노들":TEAL}
fig, ax = plt.subplots(figsize=(7.6, 4.2))
for i,(lab,segs,pp) in enumerate(cases):
    y=0
    for n,v in segs:
        ax.bar(i,v*100,bottom=y*100,color=cols[n],edgecolor="white",width=0.55,zorder=3)
        ax.text(i,(y+v/2)*100,f"{n} {v:.2%}",ha="center",va="center",fontsize=8.2,color="white" if n!="옵션풀" else "#333"); y+=v
    ax.text(i,102,pp,ha="center",fontsize=8.5,color="#333")
ax.set_xticks(range(3)); ax.set_xticklabels([c[0] for c in cases],fontsize=8.5); ax.set_ylim(0,112); ax.set_ylabel("지분 (FD, %)")
ax.set_ylim(0,124); ax.set_yticks([0,20,40,60,80,100])
ax.text(-0.45,118,f"가운데와 오른쪽의 창업자 차이 {(fnd_post-fnd_pre)*100:.2f}%p - 시리즈A 15% pre는 1.29%p(K-04). 딥게이지 계약에는 이 위치를 정하는 조항이 없다(D+186) - 없는 조항은 다음 리드가 정한다.",fontsize=7.4,color=RUST)
ax.set_title("옵션풀의 위치 — 금액이 아니라 선례가 값이다", fontsize=10.5, loc="left")
save(fig,"fig_5_3_pool_position","정본 §7.5 K-02 · §4.2 조항 부재 · 가상 비교(풀 합계 10%)는 day6_seed.py [추가 설정]")
