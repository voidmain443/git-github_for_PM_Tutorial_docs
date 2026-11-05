# -*- coding: utf-8 -*-
"""그림 1-3. 같은 21억의 네 비율 — 4.906 / 37.0 / 24.1 / 82.1"""
from mplcommon import *
import math
from day8_enterprise import ONDAM_SHARE_428, CONC_IR, CONC_CHECK, CONC_STRICT, TOTAL_MM, ANNUAL_MM
vals=[ONDAM_SHARE_428*100, CONC_IR*100, CONC_CHECK*100, TOTAL_MM/ANNUAL_MM*100]
labels=["온담에게\n21 / 428억","딥게이지 IR 기재\n7.0 / 18.9억","딥게이지 검산\n3.78 / 15.68억","개발 용량 잠식\n138 / 168 mm"]
colors=[GREY, RUST, TEAL, NAVY]
fig, ax = plt.subplots(figsize=(7.8, 4.1))
bars=ax.bar(range(4), vals, color=colors, width=0.58, zorder=2)
for i,(b,v) in enumerate(zip(bars,vals)):
    ax.text(b.get_x()+b.get_width()/2, v+1.5, f"{v:.1f}%" if i else f"{math.floor(v*1000)/1000:.3f}%", ha="center", fontsize=11, fontweight="bold", color=colors[i])
ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(0,100); ax.set_ylabel("%")
ax.axvline(0.5, color=GREY, lw=0.8, ls="--"); ax.text(0.5, 92, "상대의 시선 | 우리 안의 세 표기", ha="center", fontsize=8.5, color=GREY)
ax.text(1, 52, "과대 — 분자에\n구축·운영 포함", ha="center", fontsize=8, color=RUST)
ax.text(2, 40, f"적정\n(순SaaS 분모 {CONC_STRICT*100:.1f}%)", ha="center", fontsize=8, color=TEAL)
ax.text(3, 96, "IR 덱에 없다 — 계약이\n'성사되는' 리스크", ha="center", fontsize=8, color=NAVY, va="top")
ax.set_title("같은 21억 — 온담에게 4.9%, 딥게이지에게 37 / 24.1 / 82%", fontsize=10.5, loc="left")
fig.subplots_adjust(bottom=0.2)
save(fig,"fig_1_3_asymmetry","정본 §5.6 · E-07~11 · day8_enterprise.py")
