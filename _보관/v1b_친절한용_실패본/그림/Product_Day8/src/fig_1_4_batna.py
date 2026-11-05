# -*- coding: utf-8 -*-
"""그림 1-4. 온담 vs 대한기공 — BATNA 비교"""
from mplcommon import *
from day8_enterprise import BILL_YEAR, LIC_YEAR, TOTAL_MM, CLS_MM, P, C, BATNA
rows=[("연 매출(억)",BILL_YEAR,BATNA["연"]),("실질 ARR 증분(억)",LIC_YEAR,BATNA["연"]),("공수 mm (분류 후)",CLS_MM[P]+CLS_MM[C],0),("공수 mm (전부)",TOTAL_MM,0)]
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), gridspec_kw=dict(width_ratios=[1.15,1]))
ax=axes[0]
y=range(len(rows))
ax.barh([i+0.18 for i in y],[r[1] for r in rows],height=0.34,color=RUST,label="온담 딜",zorder=2)
ax.barh([i-0.18 for i in y],[r[2] for r in rows],height=0.34,color=TEAL,label="대한기공",zorder=2)
for i,r in enumerate(rows):
    ax.text(r[1]+2,i+0.18,f"{r[1]:g}",va="center",fontsize=8.5,color=RUST); ax.text(r[2]+2,i-0.18,f"{r[2]:g}",va="center",fontsize=8.5,color=TEAL)
ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows],fontsize=8.5); ax.invert_yaxis(); ax.set_xlim(0,160); ax.legend(fontsize=8,loc="upper right",frameon=False)
ax.set_title("매출 3배 · ARR 1.6배 · 공수 무한대", fontsize=9.5, loc="left")
ax=axes[1]; ax.axis("off")
txt=[("도메인","확장 SAM(식품 —\n제조사 아님)","초기 SAM 안\n(1차 협력사)"),("클로징","47건 협상 + CFO 3주\n→ D+900 전후 · 2법인","표준계약 4주\n클라우드"),("커스텀","47건 / 138 mm\n(분류 후 86)","0건"),("텀시트 연동","코너스톤 선행 조건\n충족","온담 거절 = 코너스톤\n소멸 → 한강 단독"),("리스크","용량 · 법정 기준 · 배상\n100% · 판정자 · 미측정","ACV 낮음 · 채널\n의존(김도윤)")]
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.text(0.0,0.97,"기준",fontsize=8.5,fontweight="bold",color=NAVY,va="top"); ax.text(0.24,0.97,"온담 딜",fontsize=8.5,fontweight="bold",color=RUST,va="top"); ax.text(0.64,0.97,"대한기공",fontsize=8.5,fontweight="bold",color=TEAL,va="top")
for i,(k,a,b) in enumerate(txt):
    yy=0.86-i*0.185
    ax.text(0.0,yy,k,fontsize=7.8,color=NAVY,va="top"); ax.text(0.24,yy,a,fontsize=7.4,color="#333",va="top",linespacing=1.25); ax.text(0.64,yy,b,fontsize=7.4,color="#333",va="top",linespacing=1.25)
    ax.plot([0,1],[yy+0.025,yy+0.025],color="#ddd",lw=0.6)
ax.set_title("BATNA는 서명돼야 카드다 — 병행 체결", fontsize=9.5, loc="left")
fig.subplots_adjust(wspace=0.25,bottom=0.12)
save(fig,"fig_1_4_batna","정본 §5.8 · E-15 · ㊱ 항목 7 [추가 설정]")
