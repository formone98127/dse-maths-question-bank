# -*- coding: utf-8 -*-
"""把某年某卷 PDF 渲染成逐頁 PNG（供影像轉寫）。
用法: python _render_pages.py <year> <p1|p2> [dpi]
輸出: <year><p1|p2>_pages/pp00.png ...
"""
import io
import sys
from pathlib import Path

import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).parent
CN = ROOT / "dse真题数学" / "DSE (中)"


def render(year: str, paper: str, dpi: int = 150) -> Path:
    src = CN / year / f"{paper}.pdf"
    out = ROOT / f"{year}{paper}_pages"
    out.mkdir(exist_ok=True)
    doc = fitz.open(src)
    z = dpi / 72
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(z, z))
        pix.save(out / f"pp{i:02d}.png")
    n = len(doc)
    doc.close()
    print(f"{year} {paper}: {n} pages -> {out}")
    return out


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 150)
