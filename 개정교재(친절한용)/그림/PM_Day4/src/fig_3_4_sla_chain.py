from mplcommon import *
import numpy as np
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.9), gridspec_kw={"width_ratios": [3.2, 1.9]})
# 좌: 항목 ② 사슬
rows = [("초안 — 데스크 응답 15 + OLA 착수 30 + 원인 분리 30 + 수행사 UC 복구 240 (착수 1h·복구 4h)", [15, 30, 30, 240], RUST, "= 315분 > 120 — 불가(산술)"),
        ("재협상 — 15 + 30 + 30 + UC 복구 90 (착수 30분·복구 90분, 연 +0.6억)", [15, 30, 30, 90], NAVY, "= 165분 — 직렬로는 여전히 불가"),
        ("재협상 + 병렬 착수 — 15 + 병렬 착수 30 + 원인 분리·복구 75 (데스크 접수 중 인프라·개발운영 동시 착수)", [15, 30, 75], TEAL, "≤ 120 성립")]
cols = [GREY, "#8FA9C8", NAVY, None]
for i, (name, segs, c, verdict) in enumerate(rows):
    y = 2 - i; left = 0
    for j, sg in enumerate(segs):
        ax.barh(y, sg, left=left, height=0.5, color=c if j == len(segs) - 1 else cols[j], alpha=0.9 if j == len(segs) - 1 else 0.7, edgecolor="white")
        ax.text(left + sg / 2, y, f"{sg}", ha="center", va="center", fontsize=7.4, color="white")
        left += sg
    ax.text(left + 4, y, verdict, va="center", fontsize=8.6, fontweight="bold", color=c)
    ax.text(0, y + 0.36, name, fontsize=7.4, color=c, va="bottom")
ax.axvline(120, color=RUST, lw=1.8)
ax.text(122, 2.62, "SLA ② P1 복구 2시간 = 120분", fontsize=8, color=RUST, fontweight="bold")
ax.set_xlim(0, 420); ax.set_ylim(-0.55, 3.0); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlabel("P1 인시던트 복구 사슬 (분) — 가장 긴 경로")
ax.set_title("항목 ② — 3층의 합이 SLA를 넘으면 협상이 아니라 산술로 불가", fontsize=9.6, color=NAVY)
# 우: 항목 ⑥ 3층 공백
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
layers = [(7.6, "SLA (현업 ↔ IT본부)", "⑥ 출고 확정 D+1 06:00\n(B-08 리드타임 12h의 운영 전제)", NAVY, True),
          (4.6, "OLA (서비스운영팀 ↔ 인프라·개발운영)", "— 비어 있음 —\nIT본부 안에 출고 확정 작업이 없다", GREY, False),
          (1.6, "UC (외부 계약)", "3PL 대성로지스 UC 없음\n(물류본부 계약 · 준실시간 거부 · 2027-06 재협상)", RUST, False)]
for y, h, t, c, solid in layers:
    ax2.add_patch(plt.Rectangle((0.4, y - 1.2), 9.2, 2.4, fill=True, facecolor=(c if solid else "white"), edgecolor=c, lw=1.6, ls="-" if solid else "--", alpha=0.9 if solid else 1))
    ax2.text(0.7, y + 0.75, h, fontsize=7.6, color="white" if solid else c, fontweight="bold", va="center")
    ax2.text(5.0, y - 0.25, t, fontsize=7.2, color="white" if solid else c, ha="center", va="center")
ax2.annotate("", xy=(5, 6.5), xytext=(5, 5.9), arrowprops=dict(arrowstyle="-", color=RUST, lw=1.5))
ax2.text(5, 9.4, "항목 ⑥ — 한 층이 비면 SLA는 구조적으로 불가", fontsize=8.6, color=NAVY, ha="center", fontweight="bold")
ax2.text(5, -0.4, "→ \"최선 노력\"으로 강등, 3PL 재협상 후 재상정\n(⑱ 이관 4번, 한동석, 06-30)", fontsize=7.4, color=RUST, ha="center", va="top")
fig.suptitle("SLA/OLA/UC 3층 — 약속은 받치는 약속의 합보다 강할 수 없다 (서명 2027-05-14: SLA 1 · OLA 3 · UC 5)", fontsize=10.5, color=NAVY, y=0.995)
fig.tight_layout()
save(fig, "fig_3_4_sla_chain", "Day4 워크북 ⑰ 항목 4(SLA/OLA/UC 3층 매핑표 ①~⑦ — ② 초안 315 > 120 · 재협상 165 → 병렬 착수 ≤ 120, ⑥ UC 부재 → 최선 노력 강등)·항목 9. 재협상 연 +0.6억은 [추가 설정].")
