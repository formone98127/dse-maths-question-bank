# -*- coding: utf-8 -*-
"""量度 2014 P1 Q10 距離時間圖：汽車 B 平直段的起訖 x、右上交點 x，
配合 8:15 與 9:30 的刻度，反算拐點時間。"""
import io
import sys

import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

im = Image.open("2014p1_pages/pp07.png").convert("L")
a = np.array(im)
dark = a < 128

# 圖形繪圖區（粗略範圍，避開座標軸標籤）
Y0, Y1 = 330, 830
X0, X1 = 230, 1130
sub = dark[Y0:Y1, X0:X1]

# 座標軸：最長垂直線 / 水平線
colsum = sub.sum(axis=0)
rowsum = sub.sum(axis=1)
yaxis_x = int(np.argmax(colsum)) + X0
xaxis_y = int(np.argmax(rowsum)) + Y0
print(f"y-axis x={yaxis_x} (len {colsum.max()}), x-axis y={xaxis_y} (len {rowsum.max()})")

# 繪圖區內部（軸內側）
px0, px1 = yaxis_x + 6, X1 - 30
py0, py1 = Y0 + 30, xaxis_y - 6
print(f"plot area x {px0}..{px1}, y {py0}..{py1}")

# 找水平長直線（汽車 B 的平直段）
best = []
for y in range(py0, py1):
    row = dark[y, px0:px1]
    # 最長連續暗段
    run = best_run = 0
    start = bs = 0
    for i, v in enumerate(row):
        if v:
            if run == 0:
                start = i
            run += 1
            if run > best_run:
                best_run = run
                bs = start
        else:
            run = 0
    if best_run > 40:
        best.append((best_run, y, bs + px0, bs + best_run + px0))
best.sort(reverse=True)
print("\nlongest horizontal runs (len, y, x_start, x_end):")
for b in best[:8]:
    print("  ", b)

# 找垂直虛線（8:15 / 9:30 的點線）：繪圖區內暗像素數 8~60 且分佈稀疏
print("\nsparse vertical lines (candidate dotted ticks):")
for x in range(px0, px1):
    col = dark[py0:py1, x]
    n = col.sum()
    if 8 <= n <= 70:
        # 檢查是否分散（非實線）
        idx = np.where(col)[0]
        gaps = np.diff(idx)
        if len(gaps) and gaps.max() >= 4:
            print(f"   x={x} n={n}")
