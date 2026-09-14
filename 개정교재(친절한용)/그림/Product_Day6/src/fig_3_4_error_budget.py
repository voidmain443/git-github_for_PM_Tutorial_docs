# -*- coding: utf-8 -*-
"""그림 3-4. 오류 예산 — 라인별 월 FN 신호와 예산선, 소진 시 자동 조치 (가상의 한 라인, 한 달)"""
from mplcommon import *
import numpy as np
days=np.arange(1,31)
rev=np.cumsum([5]*30)                                                   # 초안 '양품' 판정 누적(하루 5건, 가상)
fn=np.cumsum([0,0,1,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0])   # 검사원이 '불량'으로 뒤집은 누적(가상 - 예산 초과 시나리오)
rate=fn/np.maximum(rev,1)
fig, ax = plt.subplots(figsize=(7.6, 3.9))
ax.plot(days,rate*100,color=NAVY,lw=2,label="누적 FN 신호율 = 뒤집힌 '양품' ÷ 초안 '양품'")
ax.axhline(8.0,color=RUST,ls="--",lw=1.2); ax.text(1.2,8.4,"월 FN 예산 8.0%(라인별)",color=RUST,fontsize=8.5)
over=np.argmax(rate*100>8.0) if (rate*100>8.0).any() else None
if over is not None:
    d0=days[over]; ax.axvspan(d0,d0+6,color=GREY,alpha=0.18); ax.text(d0+0.3,1.2,f"D{d0}: 예산 소진 → 초안 표시 OFF(자동)\n→ 원인 분석 48h → 재학습 → 재측정 합격 후 ON",fontsize=7.8,color="#333")
    ax.plot(days[over:over+6],rate[over:over+6]*100,color=GREY,lw=2)
ax.set_xlabel("일(가상의 한 라인, 한 달)"); ax.set_ylabel("%"); ax.set_ylim(0,16); ax.set_xlim(1,30)
fig.subplots_adjust(bottom=0.2)
ax.legend(loc="upper left",fontsize=8,frameon=False)
ax.text(17,13.6,"검사원도 놓친 FN은 이 그림에 없다\n— 클레임으로 잡힌다(㉘ 항목 6, 책임 한계 162만)",fontsize=8,color=RUST,bbox=dict(boxstyle="round",fc="white",ec=RUST,lw=0.6))
ax.set_title("오류 예산 정책 — 측정 원천은 HITL 수정 로그", fontsize=10.5, loc="left")
save(fig,"fig_3_4_error_budget","워크북 ㉗ 항목 5 [추가 설정] · 값은 가상의 시나리오(예산 초과 예시) — 정본 수치 아님 · SRE error budget policy 형식")
