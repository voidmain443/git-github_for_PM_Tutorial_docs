# -*- coding: utf-8 -*-
"""그림 2-4. 최소 표본 — 효과 크기가 작아질수록 제곱으로 는다 (X-07 조도 경고)"""
from mplcommon import *
from day6_seed import n_two_prop
import numpy as np
p1=0.18; targets=np.arange(0.04,0.161,0.005); ns=[n_two_prop(p1,p) for p in targets]
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(targets*100,ns,color=NAVY,lw=2)
for p,lab,off in [(0.08,"X-07 목표 8% → 177",(10,-24)),(0.12,"12% → 약 500",(-78,6)),(0.14,"14% → 약 1,100",(-92,4))]:
    n=n_two_prop(p1,p); ax.plot(p*100,n,"o",color=RUST); ax.annotate(f"{lab}",xy=(p*100,n),xytext=off,textcoords="offset points",fontsize=8.5,color=RUST)
ax.axhline(250,ls="--",color=GREY,lw=1); ax.text(4.2,275,"2주 동안 오후 라인에서 얻는 사진 ≈ 250 (arm당)",fontsize=8,color=GREY)
ax.set_xlabel("목표 재촬영률 (%) — 기준 18%에서"); ax.set_ylabel("최소 표본 (arm당)"); ax.set_ylim(0,1500); ax.set_xlim(4,16.5)
fig.subplots_adjust(bottom=0.2)
ax.text(4.2,1380,"두 비율 검정 · a .05 양측(z 1.96) · 검정력 .8(z 0.84)\nn = [1.96·sqrt(2·pbar·qbar) + 0.84·sqrt(p1·q1 + p2·q2)]^2 / (p1 - p2)^2",fontsize=8,color="#333")
ax.set_title("최소 표본은 효과 크기의 제곱에 반비례한다", fontsize=10.5, loc="left")
save(fig,"fig_2_4_sample_size","day6_seed.py n_two_prop · 워크북 ㉙ 항목 4 X-07 [추가 설정] · Kohavi 외(2020) 표본 계산")
