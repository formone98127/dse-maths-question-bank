# -*- coding: utf-8 -*-
"""2014 DSE P1 中文卷 — 10 張題目插圖 1:1 電子重繪 (SVG + PNG)
重跑: python make_2014P1_figs.py   輸出到 2014P1_figs_svg/

幾何／數據來源（非目測）：
  Q9  — 由相似三角形條件反算：AC=25, BC=20, BD=12 → DC=BC²/AC=16, AD=9,
        AB=15（15-20-25 直角三角形，∠ABC=90°），BD 為斜邊上的高
  Q10 — 原卷量度：x(7:30)=386px, x(8:15)=582px, x(9:30)=910px,
        y(0)=673px, y(44)=524px, y(80)=403px → 折點 x≈751px = 8:54
  Q14 — 相似三角形：底半徑 72 / 高 96 → r(h)=0.75h；切去下部後容器高 60
        （36→96），底半徑 27；水深 28 → 水面半徑 0.75×64 = 48
  Q17 — 解方程組：V=(x,5,z)（VB=VC=30 → y=5）；
        ∠VAB=∠VDC=110° → x=-0.342|AV|；VB²=900
        → 8.5486x²-36x-576=0 → x=-6.371, z=16.78
  Q18 — L1: 6x+7y=900；L2 過 (45,90) 與 x 截距 180 → 2x+3y=360
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse

plt.rcParams.update({
    "font.family": ["Microsoft JhengHei", "DejaVu Sans"],
    "font.size": 13,
    "svg.fonttype": "path",
})
OUT = "2014P1_figs_svg"
os.makedirs(OUT, exist_ok=True)

LW = 1.4
DOT = (0, (1.2, 2.4))


def newfig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name, pad=0.06):
    fig.savefig(f"{OUT}/{name}.svg", bbox_inches="tight", pad_inches=pad)
    fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    print(name, "ok")


def cap(ax, x, y, s, fs=13):
    ax.text(x, y, s, ha="center", va="top", fontsize=fs)


# ============================================================ Q9 圖 1
A = np.array([0.0, 0.0]); C = np.array([25.0, 0.0])
D = np.array([9.0, 0.0]); B = np.array([9.0, 12.0])
fig, ax = newfig(4.6, 3.4)
for P, Q in [(A, B), (B, C), (A, C), (B, D)]:
    ax.plot(*zip(P, Q), "k-", lw=LW)
ax.text(-1.4, -1.2, "$A$", fontsize=16, ha="center")
ax.text(26.4, -1.2, "$C$", fontsize=16, ha="center")
ax.text(9.0, -1.9, "$D$", fontsize=16, ha="center")
ax.text(9.0, 13.4, "$B$", fontsize=16, ha="center")
ax.set_xlim(-3, 28); ax.set_ylim(-4, 15)
cap(ax, 12.5, -5.4, "圖 1")
save(fig, "2014P1_Q9")

# ============================================================ Q10 圖 2 距離—時間圖
T0, T1 = 0.0, 2.0                      # 7:30 → 9:30（小時）
tA = np.array([T0, T1]); dA = np.array([0.0, 80.0])           # 汽車 A：恆速
tB = np.array([T0, 0.75, 1.400, T1])                          # 8:15 停車，8:54 再開
dB = np.array([0.0, 44.0, 44.0, 80.0])
fig, ax = plt.subplots(figsize=(7.0, 3.6))
ax.set_aspect("auto"); ax.axis("off")
ax.annotate("", xy=(2.42, 0), xytext=(-0.10, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 92), xytext=(0, -1.5),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
for yv in (44, 80):                      # 水平虛線
    ax.plot([0, 2.0], [yv, yv], "k--", lw=0.8, dashes=(1.5, 2.5))
for tv, lab in [(0.75, "8:15"), (2.0, "9:30")]:               # 垂直虛線
    ax.plot([tv, tv], [0, (80 if tv > 1 else 44)], "k--", lw=0.8, dashes=(1.5, 2.5))
ax.plot(tA, dA, "k-", lw=LW)
ax.plot(tB, dB, "k-", lw=LW)
ax.text(-0.05, -1.8, "$0$", fontsize=12.5, ha="right", va="top")
ax.text(0.06, -4.6, "7:30", fontsize=12.5, ha="center", va="top")
ax.text(0.75, -2.0, "8:15", fontsize=12.5, ha="center", va="top")
ax.text(2.0, -2.0, "9:30", fontsize=12.5, ha="center", va="top")
ax.text(-0.16, 44, "44", fontsize=12.5, ha="right", va="center")
ax.text(-0.16, 80, "80", fontsize=12.5, ha="right", va="center")
ax.text(-0.13, 2.2, "$X$", fontsize=14, ha="right", va="center")
ax.text(-0.14, 88, "$Y$", fontsize=14, ha="right", va="bottom")
ax.text(1.24, 0.42, "時間", fontsize=12.5, ha="left", va="bottom")
ax.text(-0.62, 66, "與 $X$ 城間之距離 (km)", fontsize=12.5,
        rotation=90, ha="center", va="center")
ax.text(0.60, 52, "汽車 $A$", fontsize=12.5, ha="left")
ax.text(1.42, 34.5, "汽車 $B$", fontsize=12.5, ha="left")
ax.text(1.05, -14, "圖 2", fontsize=13, ha="center", va="top")
ax.set_xlim(-1.05, 2.55); ax.set_ylim(-19, 95)
save(fig, "2014P1_Q10")

# ============================================================ Q11 框線圖
vals = [18, 42, 55, 63, 91]
fig, ax = plt.subplots(figsize=(7.0, 2.0))
ax.set_aspect("auto"); ax.axis("off")
y = 0.0
BOXH = 0.85
ax.plot([18, 42], [y, y], "k-", lw=LW)
ax.plot([63, 91], [y, y], "k-", lw=LW)
ax.add_patch(plt.Rectangle((42, -BOXH), 21, 2 * BOXH, fill=False, lw=LW))
ax.plot([55, 55], [-BOXH, BOXH], "k-", lw=LW)
for v in vals:
    ax.plot([v, v], [y - BOXH if 42 <= v <= 63 else y, -2.05], "k:", lw=0.9, dashes=(1.2, 2.2))
    ax.text(v, -2.2, str(v), fontsize=12.5, ha="center", va="top")
ax.annotate("", xy=(103, y), xytext=(91, y),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.text(105, y, "價錢（千元）", fontsize=12.5, ha="left", va="center")
ax.set_xlim(10, 150); ax.set_ylim(-3.4, 2.0)
save(fig, "2014P1_Q11")

# ============================================================ Q14 圖 3 平截頭體
R_TOP, H_TOP = 72.0, 96.0
r_of = lambda h: R_TOP * h / H_TOP
H_BOT = 36.0                    # 容器底：距錐頂 36 cm（＝96-60）
H_WAT = H_BOT + 28.0            # 水面：距錐頂 64 cm
RY = 0.24                       # 橢圓短軸比例（視角）

fig, ax = newfig(7.4, 5.0)
# 母線
ax.plot([-R_TOP, -r_of(H_BOT)], [H_TOP, H_BOT], "k-", lw=LW)
ax.plot([R_TOP, r_of(H_BOT)], [H_TOP, H_BOT], "k-", lw=LW)
ax.plot([-r_of(H_BOT), 0], [H_BOT, 0], "k--", lw=0.9, dashes=(4, 2.5))
ax.plot([r_of(H_BOT), 0], [H_BOT, 0], "k--", lw=0.9, dashes=(4, 2.5))
# 橢圓：前半（下方弧）實線、後半（上方弧）虛線
def rim(ax, h, all_dashed=False):
    r = r_of(h)
    th = np.linspace(np.pi, 2 * np.pi, 90)          # 前弧
    if all_dashed:
        ax.plot(r * np.cos(th), h + r * RY * np.sin(th), "k--", lw=1.0, dashes=(4, 2.5))
    else:
        ax.plot(r * np.cos(th), h + r * RY * np.sin(th), "k-", lw=LW)
    th = np.linspace(0, np.pi, 90)                  # 後弧（隱藏邊）
    ax.plot(r * np.cos(th), h + r * RY * np.sin(th), "k--", lw=1.0, dashes=(4, 2.5))
    return r
rim(ax, H_TOP)
rim(ax, H_BOT)
rim(ax, H_WAT, all_dashed=True)
# 尺寸線
def dim_v(ax, x, y0, y1, label, side=1):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color="k",
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    ax.plot([x - 6 * side, x + 6 * side], [y0, y0], "k-", lw=0.8)
    ax.plot([x - 6 * side, x + 6 * side], [y1, y1], "k-", lw=0.8)
    ax.text(x + 4 * side, (y0 + y1) / 2, label, fontsize=12,
            ha="left" if side > 0 else "right", va="center", rotation=90)
def dim_h(ax, y, x0, x1, label):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color="k",
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    ax.plot([x0, x0], [y - 7, y + 7], "k-", lw=0.8)
    ax.plot([x1, x1], [y - 7, y + 7], "k-", lw=0.8)
    ax.text((x0 + x1) / 2, y + 3, label, fontsize=12, ha="center", va="bottom")
dim_h(ax, H_TOP + 6, -R_TOP, R_TOP, "72 cm")
dim_v(ax, -R_TOP - 26, H_BOT, H_TOP, "60 cm", side=1)
dim_v(ax, R_TOP + 26, 0, H_TOP, "96 cm", side=1)
dim_v(ax, 0, H_BOT, H_WAT, "28 cm", side=1)
ax.set_xlim(-125, 128); ax.set_ylim(-16, 112)
cap(ax, 0, -18, "圖 3")
save(fig, "2014P1_Q14")

# ============================================================ Q15 圖 4 對數線性圖
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.set_aspect("equal"); ax.axis("off")
ax.annotate("", xy=(3.9, 0), xytext=(-0.6, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 2.6), xytext=(0, -0.5),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
xs = np.linspace(0.0, 3.0, 2)
ax.plot(xs, -(xs - 3.0) / 3.0, "k-", lw=LW)
ax.text(-0.10, -0.34, "$O$", fontsize=13, ha="right", va="top")
ax.text(3.0, -0.30, "$3$", fontsize=12.5, ha="center", va="top")
ax.text(3.95, -0.28, "log$_4\\,x$", fontsize=13, ha="left", va="center")
ax.text(0.12, 2.6, "log$_8\\,y$", fontsize=13, ha="left", va="center")
ax.text(1.05, -1.85, "圖 4", fontsize=13, ha="center", va="top")
ax.set_xlim(-0.95, 4.3); ax.set_ylim(-2.4, 2.9)
save(fig, "2014P1_Q15")

# ============================================================ Q16 圖 5 點子圖案
fig, ax = newfig(7.2, 1.5)
def pattern(ax, x0, n):
    """第 n 個圖案：上排 n 粒，下排 n+1 粒"""
    for i in range(n):
        ax.plot(x0 + i * 0.62, 0.55, "o", ms=7, mfc="white", mec="k", mew=1.2)
    for i in range(n + 1):
        ax.plot(x0 + i * 0.62 - 0.31, 0.0, "o", ms=7, mfc="white", mec="k", mew=1.2)
    return x0 + n * 0.62
x = 0.0
ends = []
for n in (1, 2, 3):
    ends.append((x - 0.4, pattern(ax, x + 0.35, n)))
    x = ends[-1][1] + 1.25
for a, b in ends:
    ax.annotate("", xy=(b + 0.05, 0.28), xytext=(a - 0.05, 0.28),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k",
                                shrinkA=0, shrinkB=0, mutation_scale=12))
ax.text(x - 0.3, 0.28, "$\\cdots$", fontsize=16, ha="left", va="center")
ax.text(2.6, -0.95, "圖 5", fontsize=13, ha="center", va="top")
ax.set_xlim(-1.0, x + 0.6); ax.set_ylim(-1.5, 1.2)
save(fig, "2014P1_Q16")

# ============================================================ Q17 圖 6(a)(b) 角錐體
CX, CY = 0.62, 0.44                    # 斜投影係數


def proj(p):
    x, y, z = p
    return np.array([x + CX * y, z + CY * y])


AB_, BC_ = 18.0, 10.0
Vx, Vz = -6.371, 16.78
V = np.array([Vx, 5.0, Vz])
A_ = np.array([0, 0, 0]); B_ = np.array([AB_, 0, 0])
C_ = np.array([AB_, BC_, 0]); D_ = np.array([0, BC_, 0])
P_ = (A_ + B_) / 2; Q_ = (C_ + D_) / 2
M_ = (V + B_) / 2; N_ = (V + C_) / 2


def draw_pyramid(ax, dx=0.0, cut=False, alpha_lbl=True):
    pa, pb, pc, pd = [proj(p) + [dx, 0] for p in (A_, B_, C_, D_)]
    pv = proj(V) + [dx, 0]
    for p, q, ls in [(pa, pb, "-"), (pb, pc, "-"), (pc, pd, "--"),
                     (pd, pa, "-"), (pv, pa, "-"), (pv, pb, "-"), (pv, pc, "-")]:
        ax.plot(*zip(p, q), "k-", lw=1.2, linestyle=ls if ls == "-" else (0, (4, 2.5)))
    ax.plot(*zip(pv, pd), "k-", lw=1.0, dashes=(4, 2.5))
    if cut:
        pp, pq = proj(P_) + [dx, 0], proj(Q_) + [dx, 0]
        pm, pn = proj(M_) + [dx, 0], proj(N_) + [dx, 0]
        ax.add_patch(Polygon([pp, pq, pn, pm], closed=True, fill=False, lw=1.6))
        for p, s, off in [(pp, "$P$", (-.9, -.9)), (pq, "$Q$", (.7, -.5)),
                          (pm, "$M$", (-1.0, .55)), (pn, "$N$", (.6, .8))]:
            ax.text(p[0] + off[0], p[1] + off[1], s, fontsize=14, ha="center")
    if alpha_lbl:
        for p, s, off in [(pa, "$A$", (-.8, -.9)), (pb, "$B$", (.6, -.9)),
                          (pc, "$C$", (.9, .2)), (pd, "$D$", (-.9, .5)),
                          (pv, "$V$", (-.4, .8))]:
            ax.text(p[0] + off[0], p[1] + off[1], s, fontsize=14, ha="center")
    return pa, pb, pc, pd, pv


fig, ax = newfig(6.4, 5.2)
draw_pyramid(ax, dx=0.0, cut=False)
ax.text(9.4, -5.4, "圖 6(a)", fontsize=13, ha="center", va="top")
ax.set_xlim(-9.5, 32); ax.set_ylim(-9.5, 22.5)
save(fig, "2014P1_Q17a")

fig, ax = newfig(8.6, 5.2)
draw_pyramid(ax, dx=0.0, cut=True)
# 切出部分（PBCQNM）向右移置
dx2 = 31.0
pp, pq = proj(P_) + [dx2, 0], proj(Q_) + [dx2, 0]
pm, pn = proj(M_) + [dx2, 0], proj(N_) + [dx2, 0]
pb3, pc3 = proj(B_) + [dx2, 0], proj(C_) + [dx2, 0]
for p, q, dash in [(pp, pb3, False), (pb3, pc3, False), (pc3, pq, True), (pq, pp, True),
                   (pm, pp, False), (pm, pb3, False), (pn, pc3, False), (pn, pq, True),
                   (pm, pn, False)]:
    ax.plot(*zip(p, q), "k-", lw=1.3, dashes=(4, 2.5) if dash else ())
for p, s, off in [(pp, "$P$", (-.9, -.9)), (pq, "$Q$", (.7, -.6)),
                  (pm, "$M$", (-1.0, .55)), (pn, "$N$", (.6, .8)),
                  (pb3, "$B$", (.5, -.9)), (pc3, "$C$", (.9, .1))]:
    ax.text(p[0] + off[0], p[1] + off[1], s, fontsize=14, ha="center")
ax.text(16.0, -5.4, "圖 6(b)", fontsize=13, ha="center", va="top")
ax.set_xlim(-9.5, 56); ax.set_ylim(-9.5, 22.5)
save(fig, "2014P1_Q17b")

# ============================================================ Q18 圖 7 線性規劃
fig, ax = plt.subplots(figsize=(5.4, 3.9))
ax.set_aspect("equal"); ax.axis("off")
XMAX = 205
ax.annotate("", xy=(XMAX, 0), xytext=(-14, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 152), xytext=(0, -14),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k", shrinkA=0, shrinkB=0))
L1y = lambda x: (900 - 6 * x) / 7.0
L2y = lambda x: (360 - 2 * x) / 3.0
xg = np.linspace(-6, 190, 2)
ax.plot(xg, L1y(xg), "k-", lw=LW)
ax.plot(xg, L2y(xg), "k-", lw=LW)
shade = Polygon([(0, 0), (0, 120), (45, 90), (150, 0)], closed=True,
                facecolor="0.78", edgecolor="k", lw=1.2, hatch="////", zorder=1)
ax.add_patch(shade)
ax.text(20, 142, "$L_1$", fontsize=14, ha="center")
ax.text(112, 84, "$L_2$", fontsize=14, ha="center")
ax.text(-9, -9, "$O$", fontsize=13, ha="right", va="top")
ax.text(XMAX - 4, -9, "$x$", fontsize=13, ha="right", va="top")
ax.text(-9, 150, "$y$", fontsize=13, ha="right", va="bottom")
ax.text(90, -26, "圖 7", fontsize=13, ha="center", va="top")
ax.set_xlim(-26, 218); ax.set_ylim(-40, 165)
save(fig, "2014P1_Q18")

# ============================================================ Q19 圖 8 八管裝置
fig, ax = newfig(7.4, 3.4)
W, GAP, HT = 1.0, 0.52, 4.6
for i in range(8):
    x0 = i * (W + GAP)
    ax.plot([x0, x0], [0, HT], "k-", lw=1.6)
    ax.plot([x0 + W, x0 + W], [0, HT], "k-", lw=1.6)
    ax.plot([x0, x0 + W], [0, 0], "k-", lw=1.6)
ax.text(4 * (W + GAP) - GAP / 2 - W / 2, -0.85, "圖 8", fontsize=13, ha="center", va="top")
ax.set_xlim(-1.2, 8 * (W + GAP) + 0.2); ax.set_ylim(-2.2, HT + 0.6)
save(fig, "2014P1_Q19")

print("done ->", OUT)
