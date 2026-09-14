from mplcommon import *
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
axes_ = ["범위\n(FP · 누적)", "일정\n(TF 전 → 후)", "원가\n(금액 · 자금원)", "품질\n(TC · 커버리지)", "리스크\n(잔여 EMV Δ)", "계약 · 편익\n(대가 · 타 프로젝트)"]
crs = ["CR-08 파일럿 임시 연동\n(범위 추가, 정미란)", "CR-09 발주 마감 22:00\n(요구 변경, 서정필)", "CR-10 원가 허용범위 정의\n(거버넌스, P1 PM)", "CR-11 전환 5년 한정\n(범위 축소, 박세연·재경)"]
cells = [
 ["FP +90 (68+22)\n누적 +210 (56%)\n헌장 §5 문언 변경", "A12 20 → 25일\nTF 10 → 5\n임계경로 불변", "+0.495\n컨틴전시 미배정 풀", "TC +12\nStRS 214 → 215\n컷오버 후 폐기 TC 2", "R-19 0.60 신규(원인)\nR-13·R-06 유지\n합 7.26 (여유 0.74)", "대가 +0.495 (6호)\nP3 협의 완료\n편익 영향 없음"],
 ["FP +35\n누적 +245\nSRS 4건 수정", "A10 +1영업일\n(임계, 이미 -10)\n회복 계획 전제", "+0.19\n컨틴전시 미배정 풀\n(야간조 0.9/년은 P1 밖)", "TC +8, 3건 재작성\nUAT-FRN-039 수정", "R-16 0.24 → 0.36\nR-02 0.60 → 0.53\n순증 +0.05 → 7.31", "대가 +0.19 (6호)\n물류본부·3PL 야간조\n→ 운영위 · B-08 12h 유지"],
 ["FP 0\nWBS·RTM 영향 없음", "없음", "금액 이동 0\n허용범위 10.08 → 10.20\n예외 트리거 EAC > 156.0", "없음", "없음\n(EMV ≠ 컨틴전시 각주)", "계약 영향 없음\n윤태호 감사 답변 단일화\n헌장 §12 문언 → CCB + 스폰서"],
 ["FP -60\n누적 +185 (+1.5%)\nSRS 570 → 569", "A09 150 → 140일\nTF 5 → 15 (개선)\nA13 회당 -6h", "SI -0.33 감액\n용역 -2.0 (BL-01 기반영)\n복귀 조건 해제", "TC -9 +2\n표본 대사 7.4 → 4.8TB", "변동 없음\nR-10 동결 규칙에 포함", "감액 서면 2건\n(SI 6호, DT-01)\n편익 무관 · P5 운영 문서"],
]
# 무게 (0~3) — 교재 3.2절 판단: 어느 축이 '무거운가'
w = np.array([[3,2,2,1,2,1],[1,2,1,1,2,3],[0,0,3,0,0,3],[2,1,2,1,0,2]])
cmap = LinearSegmentedColormap.from_list("nv", ["#F1F1F1", "#DCE6F2", "#8FA9C9", "#1F3A5F"])
fig, ax = plt.subplots(figsize=(12.2, 6.6))
ax.imshow(w, cmap=cmap, vmin=0, vmax=3, aspect="auto")
for i in range(4):
    for j in range(6):
        ax.text(j, i, cells[i][j], ha="center", va="center", fontsize=6.9, color="white" if w[i, j] >= 2 else "#222222", linespacing=1.3)
ax.set_xticks(range(6)); ax.set_xticklabels(axes_, fontsize=8.4, color=NAVY); ax.xaxis.tick_top()
ax.set_yticks(range(4)); ax.set_yticklabels(crs, fontsize=8, color=NAVY)
ax.set_xticks(np.arange(-0.5, 6, 1), minor=True); ax.set_yticks(np.arange(-0.5, 4, 1), minor=True); ax.grid(which="minor", color="white", lw=2)
ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
# 오른쪽 경로 열
paths = ["변경협의체 09-30 → CCB 10-15\n승인 (조건 4) — 규칙 ②", "변경협의체 → CCB + 운영위 10-08\n조건부 승인 — 규칙 ②+④\n한동석 반대의견 기재", "CCB + 스폰서 확인\n승인 — 규칙 ② (§12 문언)", "변경협의체 → CCB\n승인, 계약 서면 2건 — 규칙 ②"]
for i, p in enumerate(paths): ax.text(5.62, i, p, fontsize=7.0, color=RUST, va="center", ha="left")
ax.text(5.62, -0.72, "처리 경로", fontsize=8.4, color=RUST, ha="left", fontweight="bold")
ax.set_xlim(-0.5, 7.4)
fig.text(0.5, 0.045, "FP 하나로는 CR-10이 0이고 CR-09가 가장 작다 — 6축으로 돌리면 CR-10은 PM의 권한(예외 트리거)을, CR-09는 다른 본부의 야간 작업 창을 바꾼다. 둘 다 CCB.   음영 = 그 축이 그 변경에서 무거운 정도(판단).",
         ha="center", fontsize=8.2, color=NAVY)
fig.suptitle("변경 4건의 6축 영향 분석 — 2026-10-15 CCB 제10차 상정분 (워크북 ⑪ 항목 4~7)", fontsize=10.5, color=NAVY, y=0.985)
fig.tight_layout(rect=(0, 0.06, 1, 0.94))
save(fig, "fig_3_2_six_axis_radar", "Day3 워크북 ⑪ 완성 예시본 CR-08·09·10·11 항목 4~7(6축 영향·허용범위 판정·처리 경로)·항목 8 CCB 의결서. 음영의 무게는 교재 3.2절의 판단이며 계산값이 아니다.")
