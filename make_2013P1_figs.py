# -*- coding: utf-8 -*-
"""2013 DSE P1 中文卷 — 4 張題目插圖 1:1 電子重繪 (SVG + PNG)
重跑: python make_2013P1_figs.py   輸出到 2013P1_figs_svg/

幾何座標數學反算（非目測擺位）：
  Q7 圖1  — E 為原點，相交弦定理 AE·CE = BE·DE 配合 BE = CE
            → AE = DE，四點精確共圓（保證 ∠BAC = ∠BDC 成立）
  Q18 圖3(a) — 直角三角 AB=28, BC=21, AC=35 (3-4-5)，放 C=(0,0), A=(35,0)
            正弦定理：∠BCM=53.130°，∠BMC=75° → CM = 21·sin(51.870°)/sin(75°) = 17.100
            → M=(17.100, 0)；覆驗 ∠BMC = 75.0° ✓
  Q18 圖3(b) — 摺後 3D：A=(28,0,0), B=(0,0,0) 貼地；|MB|=17.393, |MA|=17.9, |MC|=17.1
            解 4 方程組（三距離 + ∠AMC=107°）得 M=(13.679, 6.128, 8.817),
            C=(7.734, 19.524, 0)；AC 水平距離 = 28.14（即 (b)(i) 答案量級）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.rcParams.update({
    "font.family": ["Microsoft JhengHei", "DejaVu Sans"],
    "font.size": 13,
    "svg.fonttype": "path",
})
OUT = "2013P1_figs_svg"
os.makedirs(OUT, exist_ok=True)

DASHDOT = (0, (6, 2, 1, 2))
DOT = (0, (1.5, 2.2))
LW = 1.4

def newfig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax

def save(fig, name, pad=0.05):
    fig.savefig(f"{OUT}/{name}.svg", bbox_inches="tight", pad_inches=pad)
    fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    print(name, "ok")

def caption(ax, x, y, s):
    ax.text(x, y, s, ha="center", va="top", fontsize=13)

# ---------------------------------------------------------------- Q10 幹葉圖（B 委員會委員年歲）
fig, ax = plt.subplots(figsize=(5.2, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
rows = [
    ("幹（十位）", "葉（個位）"),
    ("2", "$a$  5  6  7"),
    ("3", "3  3  8"),
    ("4", "3"),
    ("5", "1  2  9"),
    ("6", "7  $b$"),
]
xh, xv = 3.4, 4.0                                   # header 直線與分隔直線位置
for i, (stem, leaf) in enumerate(rows):
    y = 5.2 - i * 0.85
    if i == 0:
        ax.text(xh - 0.35, y, stem, fontsize=14, ha="right", va="center")
        ax.text(xv + 0.3, y, leaf, fontsize=14, ha="left", va="center")
        ax.plot([xh - 4.2, xh + 4.6], [y - 0.42, y - 0.42], "k-", lw=1.1)  # header 底線
    else:
        ax.text(xh - 0.35, y, stem, fontsize=14.5, ha="right", va="center")
        ax.text(xv + 0.3, y, leaf, fontsize=14.5, ha="left", va="center")
ax.plot([xv, xv], [0.25, 5.62], "k-", lw=1.2)       # 幹/葉分隔直線
fig.savefig(f"{OUT}/2013P1_Q10.svg", bbox_inches="tight", pad_inches=0.05)
fig.savefig(f"{OUT}/2013P1_Q10.png", dpi=200, bbox_inches="tight", pad_inches=0.05)
plt.close(fig)
print("2013P1_Q10 ok")

# ---------------------------------------------------------------- Q9 棒形圖（僱員家庭成員人數）
# 讀數：1人→4, 2人→16, 3人→20, 4人→16, 5人→8, 6人→4, 7人→4
fig, ax = plt.subplots(figsize=(7.6, 2.9))
freqs = {1: 4, 2: 16, 3: 20, 4: 16, 5: 8, 6: 4, 7: 4}
ax.bar(list(freqs), list(freqs.values()), width=0.62,
       facecolor="white", edgecolor="k", lw=1.2, hatch="////", zorder=3)
ax.set_xticks(range(1, 8))
ax.set_yticks(range(0, 25, 4))
ax.set_xlabel("家庭成員人數", fontsize=12.5, labelpad=6)
ax.set_ylabel("僱員人數", fontsize=12.5, labelpad=6)
ax.set_title("$D$ 公司僱員的家庭成員人數的分佈", fontsize=13, pad=10)
ax.grid(axis="y", linestyle=":", lw=0.8, zorder=0)
for s in ax.spines.values():
    s.set_visible(True); s.set_linewidth(1.2)
ax.tick_params(labelsize=12)
ax.set_ylim(0, 24)
ax.set_aspect("auto")
fig.savefig(f"{OUT}/2013P1_Q9.svg", bbox_inches="tight", pad_inches=0.05)
fig.savefig(f"{OUT}/2013P1_Q9.png", dpi=200, bbox_inches="tight", pad_inches=0.05)
plt.close(fig)
print("2013P1_Q9 ok")

# ---------------------------------------------------------------- Q7 圖1 四邊形 ABCD
# 座標反算：E=(0,0)；EA 方向 147°、EB 方向 213°（兩對角線）
# AE·CE = BE·DE 且 BE=CE → AE=DE=a、BE=CE=b；取 a=2.2, b=1.9
a, b = 2.2, 1.9
dEA = np.radians(147.0)                                  # EA 方向角
A = a * np.array([np.cos(dEA), np.sin(dEA)])             # (-1.845, 1.198)
C = b * np.array([np.cos(np.radians(-33)), np.sin(np.radians(-33))])  # (1.594,-1.035)
B = b * np.array([np.cos(np.radians(213)), np.sin(np.radians(213))])  # (-1.594,-1.035)
D = a * np.array([np.cos(np.radians(33)), np.sin(np.radians(33))])    # (1.845, 1.198)
E = np.array([0.0, 0.0])
# 覆驗共圓：AE·CE == BE·DE
assert abs(np.linalg.norm(A - E) * np.linalg.norm(C - E)
           - np.linalg.norm(B - E) * np.linalg.norm(D - E)) < 1e-9

fig, ax = newfig(6.0, 4.6)
for P, Q in [(A, B), (B, C), (C, D), (D, A), (A, C), (B, D)]:
    ax.plot(*zip(P, Q), "k-", lw=1.3)
for P, sname, dx, dy in [(A, "$A$", -.5, .35), (D, "$D$", .5, .35),
                         (B, "$B$", -.35, -.55), (C, "$C$", .4, -.55),
                         (E, "$E$", .42, .3)]:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.6, 2.5)
caption(ax, 0, -3.1, "圖 1")
save(fig, "2013P1_Q7")

# ---------------------------------------------------------------- Q15 框線圖
# 讀數：min=25, Q1=45, 中位數=55, Q3=70, max=90
# 數學覆驗：素珊最高 90 → z=3；志諺 65 → z=0.5 ⇒ μ=60, σ=10 自洽 ✓
A_, Q1, MED, Q3, B_ = 25.0, 45.0, 55.0, 70.0, 90.0
Y = 12.0                                            # y 系統放大，令長寬比貼近原卷 (~3.5:1)
fig, ax = newfig(7.2, 2.4)
ax.plot([18.5, 101.5], [0, 0], "k-", lw=1.3)                       # 軸
for g in range(20, 101, 5):                                        # dotted 網格線
    ax.plot([g, g], [0, 21], "k:", lw=0.8)
    if g % 10 == 0:
        ax.plot([g, g], [-0.5, 0], "k-", lw=1.2)
        ax.text(g, -2.8, str(g), ha="center", va="top", fontsize=12.5)
ax.plot([A_, Q1], [Y, Y], "k-", lw=1.5)                            # 左鬚
ax.plot([Q3, B_], [Y, Y], "k-", lw=1.5)                            # 右鬚
ax.add_patch(Polygon([(Q1, 6), (Q3, 6), (Q3, 18), (Q1, 18)],
                     closed=True, fill=False, lw=1.6, ec="k"))     # 箱
ax.plot([MED, MED], [6, 18], "k-", lw=1.6)                         # 中位數線
ax.text(103.5, 8, "得分（分）", ha="left", va="center", fontsize=12.5)
ax.set_xlim(17, 119); ax.set_ylim(-6.5, 23)
save(fig, "2013P1_Q15")

# ---------------------------------------------------------------- Q17 圖2 長方形禁區
W, H = 2.35, 1.0
xd = 1.0                                    # 分隔線位置（闊度約 43%）
fig, ax = newfig(6.4, 3.2)
ax.add_patch(Polygon([(0, 0), (W, 0), (W, H), (0, H)],
                     closed=True, fill=False, lw=1.4, ec="k"))
ax.plot([xd, xd], [0, H], "k-", lw=1.4)                            # 分隔線
xa = xd + 0.14
ax.annotate("", xy=(xa, H), xytext=(xa, 0),
            arrowprops=dict(arrowstyle="<|-|>", color="k", lw=1.2))
ax.text(xa + 0.1, H / 2, "$x$ m", fontsize=14, ha="left", va="center")
ax.set_xlim(-0.15, 2.8); ax.set_ylim(-0.68, 1.08)
caption(ax, 1.3, -0.32, "圖 2")
save(fig, "2013P1_Q17")

# ---------------------------------------------------------------- Q18 圖3(a) — 平面三角（獨立一圖）
# 座標 1:1 量度自原卷 crop（試卷附圖不一定依比例繪成；正規化 430px = 35 單位，B 為 y 基準）
fig, ax = newfig(6.4, 4.0)
Cp = np.array([0.0, 0.0]); Mp = np.array([19.1, 0.81])
Ap = np.array([35.0, 0.81]); Bp = np.array([15.05, -25.6])
ax.plot(*zip(Cp, Ap), "k-", lw=1.35)
ax.plot(*zip(Cp, Bp), "k-", lw=1.35)
ax.plot(*zip(Ap, Bp), "k-", lw=1.35)
ax.plot(*zip(Bp, Mp), "k--", dashes=(5, 3), lw=1.15)                # 摺痕 BM
for P, sname, dx, dy in [(Cp, "$C$", -.55, .6), (Mp, "$M$", .0, .9),
                         (Ap, "$A$", .55, .6), (Bp, "$B$", 0, -1.6)]:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
ax.set_xlim(-4.5, 39.5); ax.set_ylim(-29.5, 4.0)
caption(ax, 17.5, -31.5, "圖 3(a)")
save(fig, "2013P1_Q18a")

# ---------------------------------------------------------------- Q18 圖3(b) — 摺起 3D（獨立一圖）
# 3D 反算座標（見檔頭說明）
B3 = np.array([0.0, 0.0, 0.0])
A3 = np.array([28.0, 0.0, 0.0])
C3 = np.array([7.734, 19.524, 0.0])
M3 = np.array([13.679, 6.128, 8.817])
# 覆驗四約束
def d3(P, Q): return np.linalg.norm(P - Q)
assert abs(d3(B3, M3) - 17.393) < 0.01          # BM
assert abs(d3(A3, M3) - 17.9) < 0.01            # AM
assert abs(d3(C3, M3) - 17.1) < 0.01            # CM
cosAMC = np.dot(A3 - M3, C3 - M3) / (d3(A3, M3) * d3(C3, M3))
assert abs(np.degrees(np.arccos(cosAMC)) - 107.0) < 0.1

# 匹配投影 T：解 T·v_i = w_i，令 3D 真實座標投影後精確重現原卷四點布局
# v = B→A / B→C / B→M (3D, 反算座標)；w = 原卷圖中 B→A / B→C / B→M (2D, 量自 crop, 縮 1/12, y 已翻上)
V = np.column_stack([A3 - B3, C3 - B3, M3 - B3])
W = np.column_stack([np.array([21.7, 23.3]),         # B→A
                     np.array([-20.0, 13.75]),       # B→C
                     np.array([3.58, 37.7])])        # B→M
Tmat = W @ np.linalg.inv(V)                          # 2x3 線性投影
def P2(P3):
    return Tmat @ (np.asarray(P3, dtype=float) - B3)
A2, B2, C2, M2 = P2(A3), P2(B3), P2(C3), P2(M3)

fig, ax = newfig(7.0, 4.6)
# 地面 dash-dot 平行四邊形：頂邊兩角 1:1 量度自原卷 4x zoom crop，底邊由平行四邊形約束
# （左右邊等長平行、上下底水平）對稱修正 — 原卷為規則平行四邊形
tl = np.array([-30.4, 28.3]); tr = np.array([48.7, 28.3])
v = np.array([21.25, 33.25])                       # 左/右邊向量（向左下）
pc = [tl, tr, tr - v, tl - v]
ax.add_patch(Polygon(pc, closed=True, fill=False, lw=1.15, ec="k", ls=DASHDOT))
# 三角 BCM 與 ABM（摺起）；AC 點線輔助
for P, Q in [(B2, C2), (C2, M2), (M2, B2), (A2, B2), (A2, M2)]:
    ax.plot(*zip(P, Q), "k-", lw=1.3)
ax.plot(*zip(C2, A2), "k:", lw=1.2)
for P, sname, dx, dy in [(M2, "$M$", -5.2, 1.4), (A2, "$A$", 2.3, 0),
                         (C2, "$C$", -2.5, 0), (B2, "$B$", 0.3, -2.6)]:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
ax.set_xlim(-53, 53); ax.set_ylim(-17, 50)
caption(ax, 0, -19.5, "圖 3(b)")
save(fig, "2013P1_Q18b")

print("all done ->", OUT)
