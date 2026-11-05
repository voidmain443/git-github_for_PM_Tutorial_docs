"""공통 matplotlib 설정 — PM Day4 교재 그림"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["Apple SD Gothic Neo", "Hiragino Sans"]   # ㉛~㊵는 Hiragino로 폴백
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42   # Type42 임베딩 — 폴백 글꼴의 glyph name 문제 회피
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
NAVY, TEAL, RUST, GREY, SAND = "#1F3A5F", "#2A7F62", "#C8553D", "#7A7A7A", "#E8E1D5"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def save(fig, name, source):
    fig.text(0.01, 0.005, "출처: " + source, fontsize=7.5, color=GREY, ha="left", va="bottom")
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=200, bbox_inches="tight")
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight")
