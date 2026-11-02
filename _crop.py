# -*- coding: utf-8 -*-
"""裁切頁面局部並放大，供細讀核對。
用法: python _crop.py <page.png> <x0> <y0> <x1> <y1> <out.png> [scale]
座標以像素計（可先跑 python -c 讀 PIL size）。
"""
import io
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def crop(src, x0, y0, x1, y1, out, scale=2.0):
    im = Image.open(src)
    c = im.crop((int(x0), int(y0), int(x1), int(y1)))
    if scale != 1.0:
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(out)
    print(f"{out} {c.width}x{c.height} (from {im.width}x{im.height})")


if __name__ == "__main__":
    a = sys.argv
    crop(a[1], float(a[2]), float(a[3]), float(a[4]), float(a[5]), a[6],
         float(a[7]) if len(a) > 7 else 2.0)
