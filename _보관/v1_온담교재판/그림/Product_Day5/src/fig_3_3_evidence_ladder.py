# -*- coding: utf-8 -*-
"""그림 3-3. 실험의 종류 — 증거의 강도 × 비용·기간"""
from mplcommon import *
fig, ax = plt.subplots(figsize=(8.4, 4.6))
items = [("인터뷰\n(자기 보고)", 1, 1), ("랜딩·설문\n(의향)", 2, 1.7), ("위저드오브오즈\n(행동, 사람이 뒤에서)", 3.2, 3.2), ("프로토타입\n(행동, 제품으로)", 4.6, 4.2), ("유료 파일럿\n(지불)", 6.2, 5.2), ("실사용 데이터\n(리텐션)", 8.0, 6.0)]
for name, x, y in items:
    ax.scatter(x, y, s=260, color=NAVY, zorder=3)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, 14), ha="center", fontsize=8.5)
ax.plot([i[1] for i in items], [i[2] for i in items], color=NAVY, lw=1.2, alpha=0.5, zorder=2)
# 딥게이지 실험
dg = [("X-01 WoZ\n검사원 5·2주·60만", 3.2, 3.2, TEAL), ("X-03 LOI\n4개사·30만\n(지불 의사 ≠ 지불)", 5.4, 4.6, TEAL), ("X-02 OCR 벤치\n900장·42만\n(기술 실험 — 별도 축)", 1.8, 4.9, RUST)]
for name, x, y, c in dg:
    ax.scatter(x, y, s=420, facecolors="none", edgecolors=c, linewidths=2.2, zorder=4)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, -34), ha="center", fontsize=8, color=c)
ax.set_xlim(0, 9.2); ax.set_ylim(0, 7.2)
ax.set_xlabel("비용·기간 →  (프리시드 90일 · 현금 1.6억의 범위 안에서)", fontsize=9)
ax.set_ylabel("증거의 강도 →", fontsize=9)
ax.set_xticks([]); ax.set_yticks([])
ax.axvspan(0, 4.0, color=SAND, alpha=0.35, zorder=1)
ax.text(2.0, 6.7, "프리시드에서 할 수 있는 것", ha="center", fontsize=8.5, color=GREY)
ax.text(6.6, 0.4, "가정의 중요도에 맞는 강도를 고른다 — A-05(수용)는 인터뷰로는\n검증되지 않고(자기 보고), 유료 파일럿은 6개월이 걸린다. WoZ가 그 사이.", fontsize=7.8, color=GREY, ha="center")
save(fig, "fig_3_3_evidence_ladder", "Ries(2011)·Bland & Osterwalder(2019). 딥게이지 X-01~03은 Day5 워크북 §4.5.")
