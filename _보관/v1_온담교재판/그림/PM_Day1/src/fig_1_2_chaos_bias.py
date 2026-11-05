from mplcommon import *
import numpy as np
orgs = ["Landmark Graphics\n(약간 과소추정 경향)", "Landmark의 편향 방향을\n뒤집은 가상 조직", "Organization X\n(추정을 10~100배 부풀림)"]
succ = [6, 94, 70]
fig, ax = plt.subplots(figsize=(8.2, 4.2))
bars = ax.bar(orgs, succ, color=[RUST, TEAL, NAVY], width=0.55)
for b, v in zip(bars, succ):
    ax.text(b.get_x() + b.get_width()/2, v + 2, f"{v}%", ha="center", va="bottom", fontsize=13, fontweight="bold", color=b.get_facecolor())
ax.set_ylim(0, 108); ax.set_ylabel("CHAOS 정의에 따른 '성공' 비율 (%)")
ax.set_title("같은 정의, 같은 관리 품질 — 추정 편향의 방향만 바꾸면 '성공률'이 뒤집힌다", fontsize=11, color=NAVY, pad=12)
ax.axhline(16, color=GREY, ls="--", lw=1); ax.text(2.42, 18, "1994 CHAOS 성공 16%", fontsize=8, color=GREY, ha="right")
ax.annotate("", xy=(1, 88), xytext=(0, 12), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2, connectionstyle="arc3,rad=-0.25"))
ax.text(0.42, 58, "편향 방향만 반전\n(데이터·관리는 동일)", ha="center", fontsize=9, color=GREY, bbox=dict(fc="white", ec="none", pad=2))
ax.text(0.5, -30, "CHAOS 성공 정의: 최초 추정한 시간·비용·기능 안에 완료 → 지표가 측정하는 것은 관리 품질이 아니라 추정 편향의 방향",
        ha="center", fontsize=8.5, color=GREY, transform=ax.transData, clip_on=False)
fig.subplots_adjust(bottom=0.3)
save(fig, "fig_1_2_chaos_bias", "Eveleens & Verhoef (2010), The Rise and Fall of the Chaos Report Figures, IEEE Software 27(1)를 바탕으로 재구성. 1,211개 프로젝트·5,457개 추정치.")
