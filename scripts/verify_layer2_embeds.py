# -*- coding: utf-8 -*-
"""核對第 2 層 MD 嵌圖路徑同 crops PNG（慳 token 本機檢查）。

用法:
  python scripts/verify_layer2_embeds.py
  python scripts/verify_layer2_embeds.py 化學
  python scripts/verify_layer2_embeds.py 化學 生物
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


def check_md(md: Path) -> dict:
    text = md.read_text(encoding="utf-8")
    embeds = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    missing, empty, bad = [], [], []
    for rel in embeds:
        p = (md.parent / rel.replace("/", "\\")).resolve()
        if not p.exists():
            missing.append(rel)
            continue
        if p.stat().st_size == 0:
            empty.append(rel)
            continue
        if Image is not None:
            try:
                with Image.open(p) as im:
                    im.verify()
            except Exception as ex:  # noqa: BLE001
                bad.append(f"{rel}:{ex}")
    crops_dirs = sorted({(md.parent / Path(rel).parts[0]) for rel in embeds if "crops" in rel})
    png_count = sum(len(list(d.glob("*.png"))) for d in crops_dirs if d.is_dir())
    return {
        "md": str(md.relative_to(ROOT)),
        "q": len(re.findall(r"(?m)^## 第 ", text)),
        "embeds": len(embeds),
        "png": png_count,
        "pending": text.count("圖待補"),
        "qmark": text.count("[?]"),
        "missing": len(missing),
        "empty": len(empty),
        "bad": len(bad),
        "ok": not (missing or empty or bad),
    }


def main(subjects: list[str]) -> int:
    rows = []
    for subj in subjects:
        folder = ROOT / subj
        if not folder.is_dir():
            print(f"skip missing: {subj}")
            continue
        for md in sorted(folder.glob("*QU*.md")):
            rows.append(check_md(md))
    if not rows:
        print("no MD found")
        return 1
    print(f"{'MD':40} {'題':>4} {'嵌':>4} {'PNG':>4} {'待補':>4} {'[?]':>4} {'缺':>3} {'空':>3} 狀態")
    fail = 0
    for r in rows:
        st = "OK" if r["ok"] else "FAIL"
        if not r["ok"]:
            fail += 1
        print(
            f"{r['md']:40} {r['q']:4d} {r['embeds']:4d} {r['png']:4d} "
            f"{r['pending']:4d} {r['qmark']:4d} {r['missing']:3d} {r['empty']:3d} {st}"
        )
    print(f"total {len(rows)} files, fail {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    subs = sys.argv[1:] or ["化學", "生物", "物理"]
    raise SystemExit(main(subs))
