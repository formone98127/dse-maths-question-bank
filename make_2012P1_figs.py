# -*- coding: utf-8 -*-
"""2012 DSE P1 中文卷 — 6 張題目插圖 1:1 電子重繪 (SVG + PNG)
重跑: python make_2012P1_figs.py   輸出到 2012_P1_figs_svg/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Ellipse, Polygon

plt.rcParams.update({
    "font.family": ["Microsoft JhengHei", "DejaVu Sans"],
    "font.size": 13,
    "svg.fonttype": "path",
})
OUT = "2012_P1_figs_svg"
os.makedirs(OUT, exist_ok=True)

DASH = (0, (5, 3))
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

# ---------------------------------------------------------------- Q7 框線圖
fig, ax = newfig(8.6, 1.9)
A, T1, T2, B, T3 = 0.0, 1.7, 2.75, 5.7, 10.3
Y = 1.0
ax.plot([-0.7, 11.9], [0, 0], "k-", lw=1.3)                       # 軸
ax.plot([A, T1], [Y, Y], "k-", lw=1.4)                            # 左鬚
ax.plot([B, T3], [Y, Y], "k-", lw=1.4)                            # 右鬚
ax.add_patch(Polygon([(T1, .62), (B, .62), (B, 1.38), (T1, 1.38)],
                     closed=True, fill=False, lw=1.5, ec="k"))    # 箱
ax.plot([T2, T2], [.62, 1.38], "k-", lw=1.5)                      # 中位數
ax.plot([A, A], [0, Y], "k:", lw=1.2)                             # 虛垂線
ax.plot([T3, T3], [0, Y], "k:", lw=1.2)
for x, s, it in [(A, "$a$", True), (T1, "12.1", False), (T2, "13.2", False),
                 (B, "$b$", True), (T3, "18.1", False)]:
    ax.text(x, -0.28, s, ha="center", va="top", fontsize=13)
ax.text(12.0, 0.12, "時間 (s)", ha="left", va="center", fontsize=12)
ax.set_xlim(-1.0, 14.2); ax.set_ylim(-0.75, 1.75)
save(fig, "2012P1_Q7")

# ---------------------------------------------------------------- Q8 圓內接四邊形
fig, ax = newfig(5.6, 5.2)
s = 1.0
A = np.array([-5.796, 1.553]) * s
B = np.array([0.0, 8.0]) * s
D = np.array([0.0, -15.0]) * s
C = np.array([19.318, -5.176]) * s
ctr = np.array([6.308, -3.5]); R = 13.116
ax.add_patch(Ellipse(ctr, 2 * R, 2 * R, fill=False, lw=1.4, ec="k"))
for P, Q in [(A, B), (B, C), (C, D), (D, A), (A, C), (B, D)]:
    ax.plot(*zip(P, Q), "k-", lw=1.3)
for P, sname, dx, dy in [(A, "$A$", -1.5, .1), (B, "$B$", 0, .95),
                         (C, "$C$", 1.35, -.15), (D, "$D$", -.3, -1.15),
                         ((0, 0), "$E$", .55, -.95)]:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
ax.set_xlim(-9.5, 22.5); ax.set_ylim(-19.5, 11.5)
caption(ax, 6.3, -20.6, "圖 1")
save(fig, "2012P1_Q8")

# ---------------------------------------------------------------- Q9 直立角柱體
fig, ax = newfig(6.2, 5.4)
Bp = np.array([0.0, 0.0]); Cp = np.array([2.3, 0.0])
Dp = np.array([5.6, 1.05]); Ap = np.array([1.7, 1.6])
v = np.array([0.4, 2.3])
G, H, E, F = [P + v for P in (Bp, Cp, Dp, Ap)]
for P, Q in [(Bp, Ap), (Ap, Dp), (Ap, F)]:                        # 隱藏線
    ax.plot(*zip(P, Q), "k:", lw=1.2)
for P, Q in [(Bp, Cp), (Cp, Dp), (Cp, H), (Bp, G), (Dp, E),       # 可見線
             (F, G), (G, H), (H, E), (E, F)]:
    ax.plot(*zip(P, Q), "k-", lw=1.3)
lab = [(Ap, "$A$", .45, -.1), (Bp, "$B$", -.25, -.5), (Cp, "$C$", .1, -.5),
       (Dp, "$D$", .5, -.35), (F, "$F$", -.15, .4), (G, "$G$", -.55, 0),
       (H, "$H$", -.15, .4), (E, "$E$", .5, .25)]
for P, sname, dx, dy in lab:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
ax.set_xlim(-1.4, 7.6); ax.set_ylim(-1.4, 5.0)
caption(ax, 3.1, -1.7, "圖 2")
save(fig, "2012P1_Q9")

# ---------------------------------------------------------------- Q12 圓錐 + 半球
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.9))
for a in axes:
    a.set_aspect("equal"); a.axis("off")
ax = axes[0]
apex = np.array([0, 8.2]); bc = np.array([0, 0])
rx, ry = 4.0, 1.05
ax.add_patch(Arc(bc, 2 * rx, 2 * ry, theta1=0, theta2=180, lw=1.3, ls=DASH))
ax.add_patch(Arc(bc, 2 * rx, 2 * ry, theta1=180, theta2=360, lw=1.3))
ax.plot([apex[0], bc[0] - rx], [apex[1], 0], "k-", lw=1.3)
ax.plot([apex[0], bc[0] + rx], [apex[1], 0], "k-", lw=1.3)
ax.plot([apex[0], 0], [apex[1], 0], "k--", dashes=(5, 3), lw=1.1)
ax.plot([0, rx], [0, 0], "k--", dashes=(5, 3), lw=1.1)
ax.plot([0, .38], [0, 0], "k-", lw=1.1); ax.plot([.38, .38], [0, .38], "k-", lw=1.1)
ax.text(-0.5, 4.3, "96 cm", rotation=90, ha="right", va="center", fontsize=12)
ax.text(2.0, -0.55, "48 cm", ha="center", va="top", fontsize=12)
caption(ax, 0, -2.6, "圖 3(a)")
ax.set_xlim(-5.4, 5.4); ax.set_ylim(-4.4, 9.6)

ax = axes[1]
rc, R2 = np.array([0, 0]), 5.0                     # 碗
ax.add_patch(Arc(rc, 2 * R2, 2 * R2 * 0.88, theta1=180, theta2=360, lw=1.3))
ax.add_patch(Ellipse(rc, 2 * R2, 2 * R2 * 0.225, fill=False, lw=1.3, ec="k"))
cbx, cby, crx, cry = 0.3, -1.45, 2.45, 0.52        # 圓錐底
apx = 0.3, 6.9
ax.add_patch(Ellipse((cbx, cby), 2 * crx, 2 * cry, fill=False, lw=1.1, ec="k", ls=DASH))
ax.plot([apx[0], cbx - crx], [apx[1], cby], "k-", lw=1.3)
ax.plot([apx[0], cbx + crx], [apx[1], cby], "k-", lw=1.3)
caption(ax, 0.3, -5.6, "圖 3(b)")
ax.set_xlim(-6.2, 6.8); ax.set_ylim(-6.6, 8.0)
save(fig, "2012P1_Q12")

# ---------------------------------------------------------------- Q13 拋物線
fig, ax = newfig(6.0, 5.8)
xs = np.linspace(-0.85, 5.05, 200)
ys = 0.9 * (xs - 2.1) ** 2 + 1.15
ax.plot(xs, ys, "k-", lw=1.5)
ax.annotate("", xy=(0, 9.3), xytext=(0, -1.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3))
ax.annotate("", xy=(6.1, 0), xytext=(-1.0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3))
ax.text(-0.28, 9.25, "$y$", fontsize=15, ha="right")
ax.text(6.15, -0.05, "$x$", fontsize=15, va="center")
ax.text(-0.25, -0.42, "$O$", fontsize=14, ha="center", style="italic")
Q = np.array([1.15, 0.9 * (1.15 - 2.1) ** 2 + 1.15])
P = np.array([1.15, 0.0]); R = np.array([0.0, Q[1]])
ax.plot([R[0], Q[0]], [R[1], Q[1]], "k--", dashes=(4, 2.5), lw=1.1)
ax.plot([Q[0], P[0]], [Q[1], P[1]], "k--", dashes=(4, 2.5), lw=1.1)
ax.add_patch(Ellipse((0.17, Q[1] - 0.17), 0.34, 0.34, fill=False, lw=1.0, ec="k", ls=DOT))
ax.add_patch(Ellipse((P[0] - 0.17, 0.17), 0.34, 0.34, fill=False, lw=1.0, ec="k", ls=DOT))
ax.text(Q[0] + 0.28, Q[1] + 0.22, "$Q$", fontsize=15, style="italic")
ax.text(R[0] - 0.35, R[1], "$R$", fontsize=15, ha="right", va="center", style="italic")
ax.text(P[0] + 0.05, -0.45, "$P$", fontsize=15, ha="center", style="italic")
ax.text(4.35, 8.0, "$y = 15x^2 - 63x + 72$", fontsize=14, ha="center")
ax.set_xlim(-1.3, 6.6); ax.set_ylim(-1.6, 9.8)
caption(ax, 2.55, -1.75, "圖 4")
save(fig, "2012P1_Q13")

# ---------------------------------------------------------------- Q18 角錐體
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2))
for a in axes:
    a.set_aspect("equal"); a.axis("off")
A = np.array([0, 0]); Bp = np.array([3.4, -0.55])
C = np.array([5.1, 0.8]); D = np.array([1.7, 1.35])
V = np.array([2.4, 4.9])

ax = axes[0]
for P, Q in [(V, D), (D, A), (D, C)]:
    ax.plot(*zip(P, Q), "k--", dashes=(5, 3), lw=1.15)
for P, Q in [(V, A), (V, Bp), (V, C), (A, Bp), (Bp, C)]:
    ax.plot(*zip(P, Q), "k-", lw=1.3)
for P, sname, dx, dy in [(A, "$A$", -.35, -.4), (Bp, "$B$", .15, -.45),
                         (C, "$C$", .45, 0), (D, "$D$", 0, -.5), (V, "$V$", .1, .4)]:
    ax.text(P[0] + dx, P[1] + dy, sname, fontsize=15, ha="center", style="italic")
caption(ax, 2.55, -1.7, "圖 5(a)")
ax.set_xlim(-1.1, 6.4); ax.set_ylim(-1.9, 5.7)

ax = axes[1]
t = 0.45
P = V + t * (A - V); Q = V + t * (D - V)
for Pp, Qq in [(V, Bp), (V, C), (V, P), (V, Q)]:                  # 切走部分
    ax.plot(*zip(Pp, Qq), "k:", lw=1.2)
for Pp, Qq in [(D, A), (D, C)]:                                   # 隱藏底邊
    ax.plot(*zip(Pp, Qq), "k--", dashes=(5, 3), lw=1.15)
for Pp, Qq in [(A, Bp), (Bp, C), (A, P), (P, Bp), (P, Q),         # 模型實邊
               (Q, C), (D, Q)]:
    ax.plot(*zip(Pp, Qq), "k-", lw=1.3)
for Pp, sname, dx, dy in [(A, "$A$", -.35, -.4), (Bp, "$B$", .15, -.45),
                          (C, "$C$", .45, 0), (D, "$D$", -.1, -.5),
                          (V, "$V$", .1, .4), (P, "$P$", -.45, .05),
                          (Q, "$Q$", .05, .4)]:
    ax.text(Pp[0] + dx, Pp[1] + dy, sname, fontsize=15, ha="center", style="italic")
caption(ax, 2.55, -1.7, "圖 5(b)")
ax.set_xlim(-1.1, 6.4); ax.set_ylim(-1.9, 5.7)
save(fig, "2012P1_Q18")

print("all done ->", OUT)
