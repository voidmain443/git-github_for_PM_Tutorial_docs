from mplcommon import *
import numpy as np
import matplotlib.dates as mdates
from datetime import date, timedelta
from matplotlib.patches import Rectangle
def d(s): return date.fromisoformat(s)
# 워크북 ⑫ 항목 8 — 기준선 / as-is / to-be (일자 [추가 설정], 작업일 → 일자 환산)
rows = [
 # (label, [(start,end,kind)...])  kind: base / asis / tobe
 ("A05 구현 R1 S7–S12",     [("2026-03-30","2026-06-19","base"), ("2026-03-30","2026-06-28","asis"), ("2026-03-30","2026-06-28","tobe")], "+5 (S10 3주, R-05)"),
 ("A06 구현 R2 S13–S18",    [("2026-06-22","2026-09-11","base"), ("2026-06-29","2026-09-25","asis"), ("2026-06-29","2026-09-25","tobe")], "+10 (S18 3주, 이월 420)"),
 ("A07 규제 검증 (FNLT 09-11)", [("2026-08-24","2026-09-11","base"), ("2026-08-24","2026-09-11","asis"), ("2026-08-24","2026-09-11","tobe")], "충족 142/142"),
 ("A10 구현 R3 S19–S24",    [("2026-09-14","2026-12-04","base"), ("2026-09-28","2026-12-18","asis"), ("2026-09-28","2026-12-18","tobe")], "착수 09-28 = 작업일 190, TF 0 → -10"),
 ("A11 정본 판정 → G2",      [("2026-10-26","2026-11-20","base"), ("2026-10-19","2026-11-13","asis"), ("2026-10-19","2026-11-13","tobe")], "TF 5 → 10, G2 11-27 정시"),
 ("A09 전환 매핑",           [("2026-03-30","2026-10-23","base"), ("2026-03-30","2026-10-16","asis"), ("2026-03-30","2026-10-16","tobe")], "CR-11 150 → 140일, TF 5 → 15"),
 ("A12 구현 R4 잔여 S25–S26", [("2026-12-07","2027-01-01","base"), ("2026-12-21","2027-01-15","asis"), ("2026-12-21","2027-01-29","tobe")], "CR-08 +5 · 이월 300 +5 → 30일, TF 10 → 0 (제2 임계)"),
 ("A13 리허설 1~3회차",      [("2026-11-23","2027-01-29","base"), ("2026-11-16","2027-01-22","asis"), ("2026-11-16","2027-01-22","tobe")], "01-22 종료, FNLT 01-29"),
 ("A14 통합·성능·보안 시험", [("2026-12-07","2027-01-15","base"), ("2026-12-21","2027-01-29","asis"), ("2026-12-21","2027-01-22","tobe")], "as-is 30 → to-be 25 (S24와 SS 겹침 -5)"),
 ("A16 UAT·리허설·롤백",     [("2027-01-18","2027-02-18","base"), ("2027-02-01","2027-03-04","asis"), ("2027-01-25","2027-02-18","tobe")], "as-is +10 → to-be UAT 1차 병행 -5, 02-18 유지"),
 ("A15 P2 I/F 시험 (2차 컷오버로 분리)", [("2027-02-08","2027-02-12","base"), ("2027-03-08","2027-03-12","asis"), ("2027-03-08","2027-03-12","tobe")], "G1 의결: MG3 선행 조건에서 제외, MC 03-05"),
]
fig, ax = plt.subplots(figsize=(12.4, 8.2))
cols = {"base": GREY, "asis": RUST, "tobe": TEAL}; off = {"base": 0.27, "asis": 0.0, "tobe": -0.27}
n = len(rows)
for i, (lab, bars, note) in enumerate(rows):
    y = n - 1 - i
    for (s0, e0, k) in bars:
        ax.barh(y + off[k], (d(e0) - d(s0)).days, left=mdates.date2num(d(s0)), height=0.24, color=cols[k], alpha=0.85 if k != "base" else 0.55)
    ax.text(mdates.date2num(d("2027-04-12")), y, note, fontsize=7.0, color="#333333", va="center")
ax.set_yticks(range(n)); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8)
# 마일스톤
ms = [("MG3 기준선 02-19 (FNLT)", "2027-02-19", NAVY, 0.985), ("as-is MG3 03-05", "2027-03-05", RUST, 0.945), ("컷오버 1차 창 02-26~28 (SNET)", "2027-02-26", NAVY, 0.905), ("2차 창 03-12~14 (합류 버퍼 15 전부 소진)", "2027-03-12", RUST, 0.865), ("물류 2차 컷오버 03-27 (R-01 분리)", "2027-03-27", TEAL, 0.825)]
for lab, dt, c, ypos in ms:
    ax.axvline(mdates.date2num(d(dt)), color=c, lw=1.1, ls="--" if c != NAVY else "-", alpha=0.8)
    ax.text(mdates.date2num(d("2027-02-19")) - 2.5, n - 0.3 - (0.985 - ypos) * 14, lab + "  " + dt[5:] if False else lab, fontsize=7.0, color=c, rotation=0, va="center", ha="right")
ax.axvline(mdates.date2num(d("2026-11-27")), color=GREY, lw=0.8, ls=":"); ax.text(mdates.date2num(d("2026-11-27")) + 1.2, -0.75, "G2 11-27", fontsize=7.2, color=GREY)
ax.axvline(mdates.date2num(d("2026-09-30")), color=GREY, lw=0.8, ls=":"); ax.text(mdates.date2num(d("2026-09-30")) - 1.2, -0.75, "데이터 일자 09-30", fontsize=7.2, color=GREY, ha="right")
ax.axvline(mdates.date2num(d("2026-10-02")), color=RUST, lw=0.9, ls=":"); ax.text(mdates.date2num(d("2026-10-02")) + 1.0, -1.3, "EX-01 제출 10-02", fontsize=7.0, color=RUST)
ax.axvline(mdates.date2num(d("2026-10-16")), color=RUST, lw=0.9, ls=":"); ax.text(mdates.date2num(d("2026-10-16")) + 1.0, -0.75, "결정 시한 10-16", fontsize=7.0, color=RUST)
# 버퍼 막대 (하단)
by = -1.6
for (s0, e0, lab, c, alpha) in [("2027-02-19","2027-03-12","합류 버퍼 15영업일 (프로그램 PMO장) — as-is 전부 소진 / to-be 0", NAVY, 0.25),
                                  ("2026-08-12","2026-09-11","규제 버퍼 22 — 종료(0 소비)", TEAL, 0.3)]:
    ax.barh(by, (d(e0) - d(s0)).days, left=mdates.date2num(d(s0)), height=0.4, color=c, alpha=alpha)
    ax.text(mdates.date2num(d(s0)) - (2.5 if c == NAVY else 0), by - 0.45, lab, fontsize=6.9, color=c, va="top", ha="right" if c == NAVY else "left")
# 범례
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GREY, alpha=0.55, label="기준선 BL-01 (일정 v1.0)"), Patch(color=RUST, label="as-is 전망 (회복 없음) — MG3 03-05, G4 06-11"), Patch(color=TEAL, label="to-be 회복 계획 (EX-01 대안 1) — MG3 02-19, 여유 0, A12 TF 0")],
          loc="upper center", fontsize=7.6, frameon=True, edgecolor="none", framealpha=0.95, bbox_to_anchor=(0.5, 1.0), ncol=1)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
ax.set_xlim(mdates.date2num(d("2026-03-15")), mdates.date2num(d("2027-07-15"))); ax.set_ylim(-2.7, n + 1.4)
ax.grid(axis="x", color="#EEEEEE", lw=0.6)
ax.set_title("온담 P1 임계경로 구간 A05~A17 — 기준선 / as-is / to-be (2026-09-30, 워크북 ⑫ 항목 8)", fontsize=10.5, color=NAVY)
fig.tight_layout()
save(fig, "fig_2_8_cpm_asis_tobe", "Day3 워크북 ⑫ 완성 예시본 항목 8(활동별 기준선·실제·전망·TF, 마일스톤 표, 버퍼 표, 회복 계획 EX-01). 작업일 → 일자 환산은 [추가 설정]. Day2 그림 3-6의 A05~A17 구간.")
