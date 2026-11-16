#!/usr/bin/env python3
"""Rebuild the maths lines of the hub catalog from docs/data.js.

`docs/hub/data.js` (the home-page catalog) is written by hand, so it drifts: the
search index can hold 41 maths papers while the catalog lists 21, and the home
page then looks half-empty. This regenerates one line per (year, paper, language)
that actually has questions, keeps every non-maths entry untouched, and fixes the
「N 卷」counters on the pages.

  python scripts/rebuild_catalog.py            # dry run
  python scripts/rebuild_catalog.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "data.js"
HUB = DOCS / "hub" / "data.js"


def lang_of(entry: dict) -> str:
    f = str(entry.get("file", ""))
    if re.search(r"_ZH|中文", f, re.I):
        return "中文"
    if re.search(r"_EN|英文|QU\(ENG\)|questions_EN", f, re.I):
        return "英文"
    return "中文" if len(re.findall(r"[\u4e00-\u9fff]", entry.get("text", ""))) > 8 else "英文"


def paper_label(p: str) -> str:
    return "卷一" if p.endswith("1") else "卷二"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    raw = DATA.read_text(encoding="utf-8")
    blob = json.loads(raw[raw.find("{"):].rstrip().rstrip(";"))

    seen = {}
    for q in blob["questions"]:
        if q.get("subject") != "數學" or q.get("type") != "題目":
            continue
        key = (int(q["year"]), q["paper"], lang_of(q))
        seen.setdefault(key, 0)
        seen[key] += 1

    lines = []
    for (year, paper, lang) in sorted(seen, key=lambda k: (-k[0], k[1], k[2])):
        code = "P1" if paper.endswith("1") else "P2"
        lines.append(f'  {{ id: "math", name: "數學（必修部分）", year: {year}, paper: "{paper_label(paper)}", '
                     f'lang: "{lang}", hash: "#{year}{code}Q1" }},')
    print(f"catalog maths papers: {len(lines)}  (from {len(seen)} year/paper/language sets)")

    hub = HUB.read_text(encoding="utf-8")
    start = hub.find("const CATALOG = [")
    end = hub.find("];", start)
    head, body, tail = hub[:start], hub[start:end], hub[end:]
    kept = [l for l in body.splitlines() if '{ id: "math"' not in l and "const CATALOG" not in l]
    merged = "\n".join(kept + lines)
    new_hub = head + "const CATALOG = [\n" + merged.lstrip("\n") + "\n" + tail

    if a.write:
        HUB.write_text(new_hub, encoding="utf-8")
        # 頁面上的「數學 N 卷」
        n = len(lines)
        touched = 0
        for p in DOCS.rglob("*.html"):
            t = p.read_text(encoding="utf-8")
            t2 = re.sub(r'(<a href="/math/"[^>]*>數學<span class="n">)\d+( 卷</span>)', rf"\g<1>{n}\g<2>", t)
            if t2 != t:
                p.write_text(t2, encoding="utf-8")
                touched += 1
        print(f"wrote catalog ({n} maths papers), updated counters on {touched} page(s)")


if __name__ == "__main__":
    main()
