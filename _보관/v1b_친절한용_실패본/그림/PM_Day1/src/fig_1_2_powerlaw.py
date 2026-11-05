from mplcommon import *
import numpy as np
rng = np.random.default_rng(3)
x = np.linspace(0, 6, 800)
# 정규분포(평균 1.3, sd 0.3) vs 두꺼운 꼬리(로그노멀 근사, 멱함수 꼬리 형태) — 개념 도해용 형태
from math import gamma
norm = np.exp(-0.5*((x-1.3)/0.3)**2)/(0.3*np.sqrt(2*np.pi))
# Pareto-형 꼬리: x>=1 에서 alpha=1.6, 앞부분은 부드럽게
# 두꺼운 꼬리: 로그노멀(sigma 큼) — 멱함수 꼬리에 가까운 형태의 개념도
sg = 0.75; mu = np.log(1.05) + sg**2   # 최빈값 ≈ 1.05
xx = np.maximum(x, 1e-6)
heavy = np.exp(-0.5*((np.log(xx)-mu)/sg)**2)/(xx*sg*np.sqrt(2*np.pi))
fig, ax = plt.subplots(figsize=(8.2, 4.3))
ax.plot(x, norm, color=NAVY, lw=2, label="정규분포를 가정한 초과율 (관행)")
ax.plot(x, heavy, color=RUST, lw=2, label="멱함수(power-law) 꼬리 — IT 프로젝트 실측 (Flyvbjerg 2022)")
ax.fill_between(x, heavy, where=(x>2.2), color=RUST, alpha=0.18)
ax.axvline(1.3, color=NAVY, ls="--", lw=1)
ax.text(1.26, 1.38, "'평균 초과율'에\n맞춘 컨틴전시", color=NAVY, fontsize=9, va="top", ha="right")
ax.annotate("어떤 유한한 컨틴전지도\n꼬리를 덮지 못한다", xy=(3.3, 0.06), xytext=(3.6, 0.55), fontsize=9.5, color=RUST,
            arrowprops=dict(arrowstyle="->", color=RUST))
ax.set_xlim(0, 6); ax.set_ylim(0, 1.45)
ax.set_xlabel("최종 실적 ÷ 최초 승인 예산 (배)"); ax.set_ylabel("확률 밀도 (개념도)")
ax.set_xticks([0,1,2,3,4,5,6]); ax.set_xticklabels(["0","1.0\n(예산 내)","2.0","3.0","4.0","5.0","6.0"])
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.98), frameon=False, fontsize=9)
ax.set_title("평균은 위험을 심하게 과소평가한다 — 처방은 버퍼 증액이 아니라 전파 경로 차단(모듈화)", fontsize=10.5, color=NAVY, pad=10)
fig.text(0.5, 0.06, "※ 곡선은 분포의 형태를 보이기 위한 개념도이며 실측값을 그린 것이 아니다.", ha="center", fontsize=8, color=GREY)
fig.subplots_adjust(bottom=0.24)
save(fig, "fig_1_2_powerlaw", "Flyvbjerg et al. (2022), JMIS — IT 프로젝트 5,392건의 원가 초과가 멱함수 분포를 따른다는 실증을 바탕으로 재구성.")
