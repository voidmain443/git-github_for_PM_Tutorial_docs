from mplcommon import *
import numpy as np
# AACE 18R-97 (프로세스 산업) / 56R-08 (건축) 예시 정확도 범위 — Class는 정의도로 결정된다
classes = ["Class 5\n정의도 0~2%", "Class 4\n1~15%", "Class 3\n10~40%", "Class 2\n30~75%", "Class 1\n65~100%"]
x = np.arange(5)
r18 = {"lo_out": [-50, -30, -20, -15, -10], "lo_in": [-20, -15, -10, -5, -3], "hi_in": [30, 20, 10, 5, 3], "hi_out": [100, 50, 30, 20, 15]}
r56 = {"lo_out": [-30, -20, -15, -10, -5], "lo_in": [-20, -10, -10, -5, -3], "hi_in": [30, 20, 10, 5, 3], "hi_out": [50, 30, 20, 15, 10]}
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.fill_between(x, r18["lo_out"], r18["hi_out"], color=NAVY, alpha=0.10, label="18R-97 프로세스 산업 — 예시 범위의 바깥 경계")
ax.fill_between(x, r18["lo_in"], r18["hi_in"], color=NAVY, alpha=0.22, label="18R-97 — 안쪽 경계")
ax.plot(x, r56["lo_out"], color=RUST, lw=1.6, ls="--"); ax.plot(x, r56["hi_out"], color=RUST, lw=1.6, ls="--", label="56R-08 건축·일반 건설 — 바깥 경계")
ax.axhline(0, color=GREY, lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(classes, fontsize=8.5); ax.set_ylabel("추정 대비 실제의 예시 정확도 범위 (%)")
ax.set_ylim(-60, 110)
ax.set_yticks([-50, -20, 0, 20, 50, 100]); ax.set_yticklabels(["-50%", "-20%", "0", "+20%", "+50%", "+100%"])
# P1 위치
ax.annotate("입찰 시점 FP 12,400 (RFP 기준 개략 계수)\n→ 정의도로는 Class 4~3", xy=(1.5, 0), xytext=(0.15, 62), fontsize=8, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax.plot([1.5], [0], "o", color=TEAL, ms=7)
ax.annotate("G1 FP 기준선 확인서 (설계 스프린트 6회 후)\n→ Class 2에 가깝다. 그 사이 차이가 ±3% 재확인 조항의 이유", xy=(3, 0), xytext=(2.05, -45), fontsize=8, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax.plot([3], [0], "o", color=TEAL, ms=7)
ax.text(4.0, 95, "\"Class 3이면 ±20%\"는 규칙이 아니다.\n범위는 리스크 분석으로 산정하며, 컨틴전시가\n적정할 때 약 80%가 이 밴드에 든다는 경험적 관찰", ha="right", va="top", fontsize=8, color=RUST)
ax.legend(loc="upper right", fontsize=7.5, frameon=False, bbox_to_anchor=(1.0, 0.72))
ax.set_title("AACE 추정 분류 — Class는 정의도로 결정되고, 정확도 범위는 자동으로 따라오지 않는다", fontsize=10.5, color=NAVY, pad=10)
fig.subplots_adjust(bottom=0.17)
save(fig, "fig_4_1_aace_cone", "AACE International RP 18R-97 (Rev. 2020) 및 RP 56R-08 (Rev. 2020)의 Cost Estimate Classification 표를 바탕으로 재구성. 범위 숫자는 인쇄 전 원문 표 대조 필요. 건축용 문서는 56R-08이며 56R-11이 아니다.")
