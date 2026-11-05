from mplcommon import *
import numpy as np
axes = ["Size (인원)\n소규모 팀 ↔ 대규모", "Criticality (결함 시 피해)\n편의 손실 ↔ 생명·막대한 자금 손실", "Dynamism (요구사항 변화율)\n월 50% ↔ 월 1%", "Personnel (팀 숙련도)\n고숙련 비율 높음 ↔ 저숙련 비율 높음", "Culture (조직 문화)\n자율로 번성 ↔ 질서로 번성"]
inner = ["소규모 팀", "편의 손실", "월 50% 변화", "고숙련 비율 높음", "자율로 번성"]
outer = ["대규모", "생명·막대한 자금 손실", "월 1% 변화", "저숙련 비율 높음", "질서로 번성"]
# P1 위치(교재 2.6절의 정성 판단을 0=중심(애자일)~1=바깥(규율)로 표현한 개념값)
p1 = [0.85, 0.7, 0.5, np.nan, 0.8]   # Personnel: 사례에 없음 → 가정(미표시)
srs = [0.85, 0.3, 0.25, np.nan, 0.8]  # 매장 화면·가맹 포털 (dynamism 높음, criticality 낮음)
syrs = [0.85, 0.9, 0.8, np.nan, 0.8]  # 인터페이스·데이터·결제 (criticality 높음, dynamism 낮음)
N = len(axes); ang = np.linspace(0, 2*np.pi, N, endpoint=False)
fig = plt.figure(figsize=(9.2, 7.6)); ax = fig.add_subplot(111, polar=True)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_ylim(0, 1.15); ax.set_yticks([0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels([]); ax.grid(color="#cccccc", lw=0.8)
ax.set_xticks(ang); ax.set_xticklabels(axes, fontsize=9, color=NAVY)
ax.tick_params(axis="x", pad=8)
ax.fill(np.linspace(0,2*np.pi,200), [0.3]*200, color=TEAL, alpha=0.08)
ax.text(np.pi/2+0.35, 0.16, "애자일 쪽\n(중심)", ha="center", va="center", fontsize=8.5, color=TEAL)
ax.text(np.deg2rad(324), 0.93, "규율 쪽\n(바깥)", ha="center", va="center", fontsize=8.5, color=GREY, bbox=dict(fc="white", ec="none", pad=1))
def plot(vals, color, label, ls="-", lw=2):
    v = np.array(vals, dtype=float); a = ang.copy()
    m = ~np.isnan(v)
    aa = np.concatenate([a[m], a[m][:1]]); vv = np.concatenate([v[m], v[m][:1]])
    ax.plot(aa, vv, color=color, lw=lw, ls=ls, label=label); ax.scatter(a[m], v[m], color=color, s=36, zorder=5)
plot(p1, NAVY, "P1 전체 (교재 2.6절 정성 판단)")
plot(srs, TEAL, "SRS 570건 — 매장 화면·가맹 포털 → 더 애자일하게", ls="--", lw=1.6)
plot(syrs, RUST, "SyRS 396건 — 인터페이스·데이터·결제 → 더 규율 있게", ls="--", lw=1.6)
# Personnel 미확정 표시
ax.scatter([ang[3]], [0.5], facecolors="white", edgecolors=GREY, s=90, zorder=6, lw=1.5)
ax.text(ang[3], 0.62, "?", ha="center", va="center", fontsize=12, color=GREY, fontweight="bold")
ax.text(ang[3]+0.12, 0.78, "사례에 없음 →\n워크북에서 가정", ha="left", va="center", fontsize=8, color=GREY)
# 안/밖 라벨
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), frameon=False, fontsize=8.5)
fig.text(0.5, 0.055, "다섯 점이 한 방향을 가리키지 않는다 → 처방은 '한 방법 고르기'가 아니라 시스템 분할(SRS/SyRS)이다.", ha="center", fontsize=9.5, color=NAVY)
fig.subplots_adjust(top=0.94, bottom=0.24)
save(fig, "fig_2_6_boehm_turner", "Boehm & Turner (2003), Balancing Agility and Discipline, Addison-Wesley의 5축 극좌표를 바탕으로 재구성. 위치는 정성 개념값이며 측정치가 아니다.")
