# -*- coding: utf-8 -*-
"""掃描各年試卷 PDF：頁數 + 文字層抽樣（判斷可否直接取文字轉寫）"""
import io
import sys
from pathlib import Path

import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).parent
CN = ROOT / "dse真题数学" / "DSE (中)"

targets = []
for y in range(2013, 2024):
    for p in ("p1", "p2"):
        f = CN / str(y) / f"{p}.pdf"
        if f.exists():
            targets.append((y, p, f))

for y, p, f in targets:
    doc = fitz.open(f)
    n = len(doc)
    txt = ""
    for i in range(n):
        txt += doc[i].get_text()
    chars = len(txt.strip())
    # 有效文字層：每頁平均 > 200 字元
    per = chars / max(n, 1)
    flag = "TEXT" if per > 200 else ("PARTIAL" if per > 30 else "SCAN")
    print(f"{y} {p}: pages={n} chars={chars} per_page={per:.0f} [{flag}]")
    if flag != "SCAN":
        # 樣本
        sample = txt.strip().replace("\n", " ")[:180]
        print(f"    sample: {sample}")
    doc.close()
