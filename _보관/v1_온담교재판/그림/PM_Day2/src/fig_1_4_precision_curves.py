from mplcommon import *
import numpy as np
fig, ax = plt.subplots(figsize=(9, 4.6))
t = np.linspace(0, 1, 400)
def sig(x, c, k): return 1/(1+np.exp(-k*(x-c)))
# 각 분야: 정밀도(0~1)가 급등하는 지점 — 개념도
curves = [
 ("SI (온담 P1)",  lambda x: 0.25+0.35*sig(x,0.22,30)+0.4*sig(x,0.62,35), NAVY, "-",  [(0.22,"G1 FP 확인서",(-62,8)),(0.62,"G2 정본 판정",(-70,-14)),(0.80,"G3 컷오버",(6,6))]),
 ("건설·EPC (P2)", lambda x: 0.15+0.75*sig(x,0.30,40)+0.10*sig(x,0.7,30), RUST, "-",  [(0.30,"T0 발주 확정 (LSTK)",(6,-4))]),
 ("제조 NPD",      lambda x: 0.10+0.25*sig(x,0.25,40)+0.30*sig(x,0.45,40)+0.35*sig(x,0.65,40), TEAL, "-", [(0.25,"Gate 3",(6,-12)),(0.45,"DVT·금형 발주",(6,-12)),(0.68,"PVT",(8,-4))]),
 ("제약 임상·규제", lambda x: 0.30+0.20*sig(x,0.35,30)+0.45*sig(x,0.75,45), GREY, "--", [(0.75,"규제 제출",(8,-6))]),
]
for name, f, c, ls, marks in curves:
    y = f(t); ax.plot(t, y, color=c, lw=2.2, ls=ls, label=name)
    for mx, ml, off in marks:
        my = f(np.array([mx]))[0]
        ax.plot(mx, my, "o", color=c, ms=5)
        ax.annotate(ml, (mx, my), xytext=off, textcoords="offset points", fontsize=7.5, color=c)
ax.set_xlim(0, 1); ax.set_ylim(0, 1.08)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1]); ax.set_xticklabels(["착수", "", "프로젝트 기간 (정규화)", "", "종료"])
ax.set_yticks([0.1, 0.5, 0.9]); ax.set_yticklabels(["굵게\n(계획 패키지)", "작업패키지", "활동 단위\n(CPM·동결)"])
ax.set_ylabel("범위·일정·원가 계획의 정밀도")
ax.axvspan(0.78, 0.83, color=NAVY, alpha=0.06)
ax.legend(loc="lower right", fontsize=8.5, frameon=False)
ax.set_title("되돌릴 수 없는 결정 앞에 게이트를 두고, 게이트까지는 상세히, 그 뒤는 굵게 — 분야별 급등 지점", fontsize=10.5, color=NAVY, pad=10)
ax.text(0.01, 1.02, "개념도 — 곡선의 형태와 상대 위치만 의미가 있으며 실측이 아니다", fontsize=7.5, color=GREY, va="bottom")
fig.subplots_adjust(bottom=0.16, left=0.15)
save(fig, "fig_1_4_precision_curves", "교재 1.4절 분야별 대조표(SI FP 기준선 / EPC AACE Class·LSTK / NPD EVT→DVT→PVT / 제약 규제 시계 역산)를 시간축 위에 개념도로 재구성.")
