# -*- coding: utf-8 -*-
"""그림 1-2. 현금 흐름 D+120 → D+300 — 세 시계(런웨이·클로징·TIPS)"""
from mplcommon import *
from day6_seed import PATH, CASH_D300, RUNWAY_D300, CASH_MIN
xs=[d for d,_,_ in PATH]; ys=[c/10000 for _,c,_ in PATH]
fig, ax = plt.subplots(figsize=(8.0, 4.0))
ax.step(xs, ys, where="post", color=NAVY, lw=2, zorder=3)
ax.fill_between(xs, ys, step="post", color=NAVY, alpha=0.08)
ax.axhline(0, color=GREY, lw=0.8)
marks=[(149,CASH_MIN/10000,"D+149 잔액 1,505만\n(7월 급여 후 · 런웨이 0.4개월)",RUST,(-58,26)),(150,2.15,"선투자 2억 D+150",TEAL,(14,8)),(179,13.15,"시드 잔여 10억 D+179\n(클로징)",TEAL,(-60,14)),
       (217,17.18,"TIPS 1차년도 5억 D+217",TEAL,(8,-34)),(300,CASH_D300/10000,f"D+300 {CASH_D300/10000:.1f}억 / 런웨이 {RUNWAY_D300:.0f}개월 (G-15)",NAVY,(-190,-30))]
for x,y,t,c,off in marks:
    ax.plot(x,y,"o",color=c,zorder=4); ax.annotate(t,xy=(x,y),xytext=off,textcoords="offset points",fontsize=8,color=c,arrowprops=dict(arrowstyle="-",color=c,lw=0.6))
ax.set_xlim(115,305); ax.set_ylim(-0.5,19.5); ax.set_xlabel("D+n (2026-06-30 = D+120, 12-27 = D+300)"); ax.set_ylabel("현금 잔액 (억 원)")
ax.set_xticks([120,150,180,210,240,270,300])
fig.subplots_adjust(bottom=0.2)
ax.text(121,18.6,"소진: 7월 3,900 → 12월 6,900만(+청구서 초과 570)  ·  유료 3사 SaaS 매출은 월 405만 — 이 그림에서 보이지 않는다",fontsize=8,color=GREY)
ax.set_title("현금 흐름 D+120 → D+300 — 세 계단과 한 바닥", fontsize=10.5, loc="left")
save(fig,"fig_1_2_cash_path","day6_seed.py 현금 흐름 [추가 설정 — G-15 D+300 15.4억/22개월에 맞춤] · 정본 §3.2 선투자 2억·RCPS 12억·TIPS 8억")
