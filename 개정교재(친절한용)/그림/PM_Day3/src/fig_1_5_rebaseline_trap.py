from mplcommon import *
import numpy as np
# 개념도 — 곡선 형태는 온담 PV(BL-01)를 쓰되, 오른쪽 재기준선 시나리오는 가상이다
months = ["26-01","26-03","26-05","26-07","26-09","26-11","27-01","27-03","27-05","27-07"]
x = np.arange(1, 18)
PVc = np.array([3.06,6.12,19.14,36.83,45.72,54.61,62.69,71.74,77.83,84.12,91.81,103.00,119.20,129.19,136.77,142.02,145.80])
EVc = np.array([1.81,4.87,17.18,28.86,39.83,48.10,57.28,65.51,73.43])
fig, (a, b) = plt.subplots(1, 2, figsize=(11.6, 5.0), sharey=True)
# ---- 왼쪽: 편차를 보이게 두기
a.plot(x, PVc, color=NAVY, lw=2.4, label="PV — BL-01 고정 (G1 2026-04-30)")
pv2 = PVc.copy(); pv2[11:] += 0.33; pv2[12:] += 0.69
a.plot(x[10:], pv2[10:], color=NAVY, lw=1.6, ls="--", label="BL-02 (10-23): 승인 변경 +1.02만 편입 → 146.82")
a.plot(x[:9], EVc, color=TEAL, lw=2.4, marker="s", ms=3.5, label="EV 실적 (9개월)")
a.fill_between(x[:9], EVc, PVc[:9], color=RUST, alpha=0.18)
a.annotate("SV -4.40 (BL-01 대비)\n편차가 문서에 보인다", xy=(9, 75.6), xytext=(3.2, 100), fontsize=8.2, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
a.annotate("A10 착수 -10영업일 — 기준선에 넣지 않고\n편차로 남김 → EX-01 예외 보고", xy=(9, 73.43), xytext=(8.5, 40), fontsize=7.8, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9))
a.annotate("+1.02 계단 (CR-08·09·11 등, +185 FP)\n— 범위가 늘었으니 PV도 는다", xy=(13, pv2[12]), xytext=(2.0, 118), fontsize=7.6, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
a.set_title("편차를 보이게 두기 — 기준선 갱신(BL-02)", fontsize=10, color=NAVY)
a.legend(loc="upper left", fontsize=7.4, frameon=False, bbox_to_anchor=(0, 0.98))
# ---- 오른쪽: 계획을 고쳐 편차 없애기 (가상)
b.plot(x, PVc, color=GREY, lw=1.2, ls=":", label="최초 PV (BL-01) — 회색 점선으로만 남음")
# 실적: 점점 늦어지는 EV (가상) — 20개월에 종료
xe = np.arange(1, 21); ev_slow = np.interp(xe * 17/20, x, PVc) ; ev_slow[-1] = 145.8
b.plot(xe, ev_slow, color=TEAL, lw=2.4, label="EV 실적 (가상: 17개월 계획이 20개월)")
# 분기마다 재기준선: PV를 EV에 맞춤
cols = [NAVY, "#3E6FA0", "#7FA3CC", "#B8CCE4"]
for k, (start, lab) in enumerate([(4, "BL-02"), (7, "BL-03"), (10, "BL-04"), (13, "BL-05")]):
    xs = np.arange(start, 21); base = ev_slow[start-1]
    # 재기준선: 현 EV에서 남은 기간을 다시 배분해 종료 = 17 + 지연
    end = 17 + (start-1)*3/20 + 0.6*k + 0.4
    xx = np.linspace(start, 21, 30); yy = base + (145.8-base) * np.clip((xx-start)/(end-start), 0, 1)**1.15
    b.plot(xx, yy, color=cols[k], lw=1.4, ls="--")
    b.text(start, base - 9, lab, fontsize=7.5, color=cols[k], ha="center")
    b.plot([start], [base], marker="o", color=cols[k], ms=5)
b.annotate("마지막 기준선(BL-05) 대비 편차 0\n— 그러나 최초 계획 대비 +3개월은\n어느 문서에도 없다", xy=(20, 145.8), xytext=(11.5, 30), fontsize=8.2, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=0.9))
b.annotate("", xy=(20, 152), xytext=(17, 152), arrowprops=dict(arrowstyle="<->", color=RUST, lw=1.2)); b.text(18.5, 154, "누적 지연 +3개월 (은폐됨)", fontsize=7.6, color=RUST, ha="center")
b.set_title("계획을 고쳐 편차 없애기 — 분기마다 재기준선 (가상 시나리오)", fontsize=10, color=NAVY)
b.legend(loc="upper left", fontsize=7.4, frameon=False, bbox_to_anchor=(0, 0.98))
for ax_ in (a, b):
    ax_.axhline(145.8, color=GREY, lw=0.7); ax_.set_ylim(0, 165); ax_.set_xlim(0.5, 21)
    ax_.set_xticks(np.arange(1, 22, 2)); ax_.set_xticklabels(["26-01","26-03","26-05","26-07","26-09","26-11","27-01","27-03","27-05","27-07","27-09"], fontsize=7.2, rotation=45)
a.set_ylabel("누적 (억 원)")
fig.suptitle("재기준선은 편차를 없애는 것이 아니라 보이지 않게 하는 것", fontsize=11, color=NAVY, y=0.99)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "fig_1_5_rebaseline_trap", "왼쪽 PV·EV = Day3 워크북 ⑫ 항목 3·⑪ 항목 9(BL-02 +0.33·+0.69). 오른쪽은 개념도이며 실측이 아니다 — 재기준선 반복 시나리오는 가상.")
