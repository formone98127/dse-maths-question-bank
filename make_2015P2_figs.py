# -*- coding: utf-8 -*-
"""2015 DSE P2 中文卷 — 14 張題目插圖 1:1 電子重繪 (SVG + PNG)
重跑: python make_2015P2_figs.py   輸出到 2015P2_figs_svg/

幾何／數據來源（非目測，跟 2014P1 慣例「由條件反算」）：
  Q15 — 解方程組：C(0,0) B(16,0) A(16,12)；N=AC 上一點、DN⊥AC、DN=6、EN=5、DC=10、EA=13
        → N(6.4,4.8) D(2.8,9.6) E(3.4,8.8)（面積 96 cm² 自洽）
  Q17 — 平行四邊形 A(0,0) B(10,0) C(12,4) D(2,4)，E 為 CD 上 DE:EC=2:3 → E(6,4)；
        F=AD延線∩BE延線=(10/3,20/3)，G=AE延線∩BC延線=(15,10)
  Q18 — ∠BAC=90°(A)、∠ADC=90°(D)：A(0,0) B(6,0) C(0,4) D(2,2)（AD⊥DC 自洽）
  Q40 — 圓心 O(0,0) r=3，直徑 BD 水平；A(3,6)，切線 AB=6、AC=6，AC 延線交 BD 延線於 E(-5,0)
        → C(-1.8,2.4)（AC=6、CE=4、AE=10 自洽）
  Q20 — 圓半徑 5，AD 水平直徑；∠BAD=58° → B(-2.19,4.49)；C 使 BC=CD（上右）、E（下右）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, Wedge, FancyArrowPatch

plt.rcParams.update({
    "font.family": ["Microsoft JhengHei", "DejaVu Sans"],
    "font.size": 13,
    "svg.fonttype": "path",
})
OUT = "2015P2_figs_svg"
os.makedirs(OUT, exist_ok=True)

LW = 1.4
GRAY = "0.55"


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


def lbl(ax, x, y, s, fs=14, dx=0, dy=0, ha="center", va="center"):
    ax.text(x + dx, y + dy, s, fontsize=fs, ha=ha, va=va)


def rightangle(ax, p, d1, d2, size=0.5):
    """直角標記：p 為頂點，d1/d2 為兩條正交方向（單位向量）。"""
    a = p + d1 * size
    b = p + d1 * size + d2 * size
    c = p + d2 * size
    ax.plot([a[0], b[0], c[0]], [a[1], b[1], c[1]], "k-", lw=0.9, solid_capstyle="round")


# ============================================================ Q8 拋物線
fig, ax = plt.subplots(figsize=(4.4, 3.6))
ax.set_aspect("auto"); ax.axis("off")
x = np.linspace(-5, 2.2, 200)
y = (x + 2.0) ** 2
ax.plot(x, y, "k-", lw=1.6)
ax.annotate("", xy=(2.6, 0), xytext=(-5.4, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 17.2), xytext=(0, -0.8),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.plot([-2.0], [0], "ko", ms=3.5)
lbl(ax, 0, -1.6, "O")
lbl(ax, 2.9, 0, "$x$")
lbl(ax, 0.25, 17.5, "$y$")
lbl(ax, -2.0, -1.5, "$-b$", va="top")
ax.set_xlim(-5.6, 3.0); ax.set_ylim(-2.2, 18.0)
save(fig, "2015P2_Q8")

# ============================================================ Q13 點陣
fig, ax = newfig(7.6, 2.4)
ax.set_xlim(0, 18); ax.set_ylim(0, 5)


def cross(cx, cy, arm, s=0.16):
    """十字點陣：中心 1 粒 + 四臂各 arm 粒。"""
    ax.plot([cx], [cy], "ko", ms=s * 60)
    for k in range(1, arm + 1):
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)):
            ax.plot([cx + dx * 0.7], [cy + dy * 0.7], "ko", ms=s * 60)


cross(2.2, 2.5, 1)
cross(6.2, 2.5, 2)
cross(10.2, 2.5, 3)
lbl(ax, 14.2, 2.5, "$\\cdots$", fs=20)
save(fig, "2015P2_Q13")

# ============================================================ Q15 三角形
C = np.array([0.0, 0.0]); B = np.array([16.0, 0.0]); A = np.array([16.0, 12.0])
N = np.array([6.4, 4.8]); D = np.array([2.8, 9.6]); E = np.array([3.4, 8.8])
fig, ax = newfig(5.6, 4.4)
for P, Q in [(A, B), (B, C), (C, A), (D, N), (A, E), (C, D)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "k-", lw=LW)
# 直角標記：B（BA 向右、BC 向左），N（NA/NC 沿 AC、ND 垂直）
rightangle(ax, B, np.array([-1., 0.]), np.array([0., 1.]), 0.7)
rightangle(ax, N, (A - N) / np.linalg.norm(A - N), (D - N) / np.linalg.norm(D - N), 0.7)
lbl(ax, 0, -1.1, "$C$")
lbl(ax, 16, -1.1, "$B$")
lbl(ax, 16, 13.0, "$A$")
lbl(ax, 2.8, 10.7, "$D$")
lbl(ax, 3.4, 7.7, "$E$", dy=-0.55)
lbl(ax, 6.4, 3.6, "$N$", dy=-0.7)
ax.set_xlim(-3.5, 19); ax.set_ylim(-2.5, 15)
save(fig, "2015P2_Q15")

# ============================================================ Q16 平截頭體（圓錐切頂）
fig, ax = newfig(4.2, 3.6)
# 全圓錐高 12、底半徑 9；切去高 4 之頂錐 → 平截頭高 8、頂半徑 3
h_top, r_bot, r_top, h_frust = 4.0, 9.0, 3.0, 8.0
y0 = 0.0
# 全錐兩側虛線（被切去之頂部）
ax.plot([0, r_top], [y0 + h_frust, y0 + h_frust + h_top], "k--", lw=1.0, dashes=(3, 3))
ax.plot([0, -r_top], [y0 + h_frust, y0 + h_frust + h_top], "k--", lw=1.0, dashes=(3, 3))
ax.plot([-r_top, r_top], [y0 + h_frust + h_top, y0 + h_frust + h_top], "k--", lw=1.0, dashes=(3, 3))
# 平截頭實線
ax.plot([0, r_bot], [y0, y0 + h_frust], "k-", lw=LW)
ax.plot([0, -r_bot], [y0, y0 + h_frust], "k-", lw=LW)
ax.plot([-r_bot, r_bot], [y0, y0], "k-", lw=LW)
ax.plot([-r_top, r_top], [y0 + h_frust, y0 + h_frust], "k-", lw=LW)
# 虛線底圓（透視）
ax.plot([-r_bot, r_bot], [y0, y0], "k-", lw=LW)
ax.plot([-r_bot, 0, r_bot], [y0, y0 - 1.2, y0], "k--", lw=0.9, dashes=(2.5, 2.5))
ax.set_xlim(-11, 11); ax.set_ylim(-2.5, 14)
save(fig, "2015P2_Q16")

# ============================================================ Q17 平行四邊形
A = np.array([0.0, 0.0]); B = np.array([10.0, 0.0]); C = np.array([12.0, 4.0]); D = np.array([2.0, 4.0])
E = np.array([6.0, 4.0]); F = np.array([10 / 3, 20 / 3]); G = np.array([15.0, 10.0])
fig, ax = newfig(5.8, 4.2)
for P, Q in [(A, B), (B, C), (C, D), (D, A), (B, E), (E, F), (A, E), (E, G)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "k-", lw=LW)
# 延線（虛線）：D→F、C→G
ax.plot([D[0], F[0]], [D[1], F[1]], "k--", lw=0.9, dashes=(3, 3))
ax.plot([C[0], G[0]], [C[1], G[1]], "k--", lw=0.9, dashes=(3, 3))
for P, s, (dx, dy) in [(A, "$A$", (-0.6, -0.7)), (B, "$B$", (0.5, -0.7)), (C, "$C$", (0.5, 0.35)),
                        (D, "$D$", (-0.7, 0.35)), (E, "$E$", (0, 0.7)), (F, "$F$", (0.5, 0.35)),
                        (G, "$G$", (0.4, 0.3))]:
    lbl(ax, P[0], P[1], s, dx=dx, dy=dy)
ax.set_xlim(-2.5, 17); ax.set_ylim(-1.6, 12)
save(fig, "2015P2_Q17")

# ============================================================ Q18 直角三角形
A = np.array([0.0, 0.0]); B = np.array([6.0, 0.0]); C = np.array([0.0, 4.0]); D = np.array([2.0, 2.0])
fig, ax = newfig(4.6, 3.6)
for P, Q in [(A, B), (A, C), (A, D), (C, D)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "k-", lw=LW)
rightangle(ax, A, np.array([1., 0.]), np.array([0., 1.]), 0.5)
rightangle(ax, D, (A - D) / np.linalg.norm(A - D), (C - D) / np.linalg.norm(C - D), 0.5)
lbl(ax, 0, -0.7, "$A$")
lbl(ax, 6, -0.7, "$B$")
lbl(ax, -0.35, 4.2, "$C$", ha="center")
lbl(ax, 2, 1.55, "$D$", dy=-0.55)
# α = ∠CAD（A 處 CA 與 DA 之間）
ax.text(1.15, 0.55, "$\\alpha$", fontsize=13)
# β = ∠ABC（B 處 BA 與 BC 之間）
ax.text(4.9, 0.6, "$\\beta$", fontsize=13)
ax.set_xlim(-1.6, 7.4); ax.set_ylim(-1.7, 5.2)
save(fig, "2015P2_Q18")

# ============================================================ Q20 圓
r = 5.0
A = np.array([-r, 0.0]); Dp = np.array([r, 0.0])
ang = np.deg2rad(58)
u = np.array([np.cos(ang), np.sin(ang)])
t = 10 * np.cos(ang)
B = A + t * u
# C 使 BC=CD（上右）：B 與 D 之中垂線交圓
mid = (B + Dp) / 2
dirv = Dp - B
perp = np.array([-dirv[1], dirv[0]])
perp = perp / np.linalg.norm(perp)
# C 在圓上且在中垂線上：|mid + s·perp| = r → 選 +（上右）
s = -np.dot(mid, perp) + np.sqrt(r ** 2 - np.dot(mid, mid) + np.dot(mid, perp) ** 2)
C = mid + s * perp
# E（下右）
angE = np.deg2rad(-55)
E = np.array([r * np.cos(angE), r * np.sin(angE)])
fig, ax = newfig(4.6, 4.2)
ax.add_patch(Circle((0, 0), r, fill=False, ec="k", lw=LW))
ax.plot([A[0], Dp[0]], [A[1], Dp[1]], "k-", lw=LW)
for P, Q in [(A, B), (B, C), (C, Dp), (Dp, E), (E, A), (C, E)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "k-", lw=LW)
lbl(ax, -r, -0.7, "$A$")
lbl(ax, r, -0.7, "$D$")
lbl(ax, B[0], B[1] + 0.5, "$B$")
lbl(ax, C[0], C[1] + 0.5, "$C$")
lbl(ax, E[0], E[1] - 0.55, "$E$")
ax.set_xlim(-6.6, 6.6); ax.set_ylim(-6.6, 6.6)
save(fig, "2015P2_Q20")

# ============================================================ Q25 兩直線
fig, ax = plt.subplots(figsize=(4.2, 3.6))
ax.set_aspect("auto"); ax.axis("off")
# L1: x = -2（鉛垂，x 截距負）；L2: y = x + 1（x 截距 -1、y 截距 1）；交於 (-2,-1)
ax.plot([-2, -2], [-2.6, 3.2], "k-", lw=LW)
ax.plot([-3.4, 2.4], [-2.4, 3.4], "k-", lw=LW)
ax.annotate("", xy=(2.6, 0), xytext=(-3.6, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 3.6), xytext=(0, -2.9),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
lbl(ax, 0, -3.3, "O")
lbl(ax, 2.95, 0, "$x$")
lbl(ax, 0.25, 3.8, "$y$")
lbl(ax, -2, 3.3, "$L_1$", va="bottom")
lbl(ax, 2.15, 3.4, "$L_2$")
ax.set_xlim(-3.7, 3.0); ax.set_ylim(-3.4, 4.0)
save(fig, "2015P2_Q25")

# ============================================================ Q28 棒形圖
fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("auto"); ax.axis("off")
keys = [1, 2, 3, 4, 5]
cnts = [12, 16, 8, 4, 4]
ax.bar(keys, cnts, width=0.55, color="white", edgecolor="k", linewidth=1.1)
ax.annotate("", xy=(6.0, 0), xytext=(0.2, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 18.4), xytext=(0, -0.4),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
for k, c in zip(keys, cnts):
    lbl(ax, k, c + 0.7, str(c), fs=11, va="bottom")
lbl(ax, 3.0, -2.2, "鑰匙的數目", fs=12)
ax.text(-1.35, 9.0, "學生人數", fontsize=12, rotation=90, ha="center", va="center")
for k in keys:
    lbl(ax, k, -1.2, str(k), fs=11)
ax.set_xlim(0, 6.2); ax.set_ylim(-3.2, 20)
save(fig, "2015P2_Q28")

# ============================================================ Q29 框線圖
fig, ax = plt.subplots(figsize=(6.4, 2.2))
ax.set_aspect("auto"); ax.axis("off")
y = 0.0
box = 1.0
ax.annotate("", xy=(72, 0), xytext=(8, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
# 鬚
ax.plot([15, 25], [y, y], "k-", lw=1.2)
ax.plot([45, 60], [y, y], "k-", lw=1.2)
ax.plot([15, 15], [y - box * 0.18, y + box * 0.18], "k-", lw=1.2)
ax.plot([60, 60], [y - box * 0.18, y + box * 0.18], "k-", lw=1.2)
# 盒
ax.add_patch(plt.Rectangle((25, y - box / 2), 20, box, fill=False, ec="k", lw=1.2))
# 中位數線
ax.plot([40, 40], [y - box / 2, y + box / 2], "k-", lw=1.6)
# 刻度
for xv in range(10, 71, 5):
    ax.plot([xv, xv], [y - box, y - box * 0.6], "k-", lw=0.8)
    lbl(ax, xv, y - box - 0.45, str(xv), fs=10)
lbl(ax, 40, y - box - 1.5, "閱書數目", fs=12)
ax.set_xlim(8, 73); ax.set_ylim(-4.5, 3.0)
save(fig, "2015P2_Q29")

# ============================================================ Q32 log 直線
fig, ax = plt.subplots(figsize=(4.4, 3.4))
ax.set_aspect("auto"); ax.axis("off")
# 直線過 (0,2) 及 (3,0)，斜率 -2/3
ax.plot([-0.6, 3.6], [2.4, -0.4], "k-", lw=1.6)
ax.annotate("", xy=(3.9, 0), xytext=(-0.9, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 3.1), xytext=(0, -0.5),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.plot([3], [0], "ko", ms=3.5)
lbl(ax, 0, -0.65, "O")
lbl(ax, 3, -0.6, "3")
lbl(ax, -0.3, 2, "2", ha="right")
lbl(ax, 4.2, 0, "$\\log_3 x$")
lbl(ax, 0.25, 3.3, "$\\log_3 y$")
ax.set_xlim(-1.0, 4.5); ax.set_ylim(-1.0, 3.4)
save(fig, "2015P2_Q32")

# ============================================================ Q36 陰影三角形
fig, ax = plt.subplots(figsize=(4.6, 4.0))
ax.set_aspect("auto"); ax.axis("off")
# 三線：y=x+5、x+2y=10、x=4；三角形頂點 (0,5)(4,3)(4,9)
tri = Polygon([(0, 5), (4, 3), (4, 9)], closed=True, facecolor="0.8", edgecolor="k", lw=1.0, zorder=1)
ax.add_patch(tri)
xx = np.linspace(-0.5, 4, 100)
ax.plot(xx, xx + 5, "k-", lw=1.3, zorder=2)
ax.plot(xx, (10 - xx) / 2, "k-", lw=1.3, zorder=2)
ax.plot([4, 4], [2.5, 9.5], "k-", lw=1.3, zorder=2)
ax.annotate("", xy=(5.2, 0), xytext=(-0.8, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 10.2), xytext=(0, -0.8),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
lbl(ax, 0, -1.1, "O")
lbl(ax, 5.5, 0, "$x$")
lbl(ax, 0.25, 10.6, "$y$")
lbl(ax, 4, -1.0, "4")
lbl(ax, -0.25, 5, "5", ha="right")
ax.set_xlim(-1.0, 5.8); ax.set_ylim(-1.8, 11.0)
save(fig, "2015P2_Q36")

# ============================================================ Q39 正弦波
fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.set_aspect("auto"); ax.axis("off")
xx = np.linspace(-40, 180, 500)
yy = np.sin(np.deg2rad(2 * xx + 30))
ax.plot(xx, yy, "k-", lw=1.5)
ax.annotate("", xy=(192, 0), xytext=(-48, 0),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 1.35), xytext=(0, -1.35),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
ax.plot([75, 165], [0, 0], "ko", ms=3.5)
lbl(ax, 75, -0.45, "75", va="top")
lbl(ax, 165, -0.45, "165", va="top")
lbl(ax, 0, -0.45, "O", va="top")
lbl(ax, 205, 0, "$x$")
lbl(ax, 4, 1.42, "$y$")
ax.set_xlim(-50, 210); ax.set_ylim(-1.55, 1.5)
save(fig, "2015P2_Q39")

# ============================================================ Q40 圓切線
O = np.array([0.0, 0.0]); r = 3.0
B = np.array([3.0, 0.0]); D = np.array([-3.0, 0.0]); A = np.array([3.0, 6.0])
C = np.array([-1.8, 2.4]); E = np.array([-5.0, 0.0])
fig, ax = newfig(4.8, 3.8)
ax.add_patch(Circle(O, r, fill=False, ec="k", lw=LW))
ax.plot([B[0], D[0]], [B[1], D[1]], "k-", lw=LW)
for P, Q in [(A, B), (A, C), (A, E), (C, E)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "k-", lw=LW)
lbl(ax, 3, -0.65, "$B$")
lbl(ax, -3, -0.65, "$D$")
lbl(ax, 3, 6.5, "$A$")
lbl(ax, -1.8, 3.05, "$C$")
lbl(ax, -5, -0.65, "$E$")
ax.set_xlim(-6.4, 6.4); ax.set_ylim(-2.0, 8.0)
save(fig, "2015P2_Q40")

print("ALL DONE")
