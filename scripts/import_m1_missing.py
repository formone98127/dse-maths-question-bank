#!/usr/bin/env python3
"""把 M1 評卷參考分題 md 匯入 data.js（只補缺，不覆蓋）。用法：python3 import_m1_missing.py 2014 2014_MS_split.md"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DATA = REPO / "docs/data.js"


def main():
    year, fname = sys.argv[1], sys.argv[2]
    src = pathlib.Path(fname)
    md = src.read_text(encoding="utf-8")
    s = DATA.read_text(encoding="utf-8")
    d = json.loads(s[s.index("{"): s.rindex("}") + 1])
    have = {int(q["qno"]) for q in d["questions"]
            if q["paper"] == "Paper 1M" and str(q["year"]) == year and q["type"] == "解答"}
    blocks = re.split(r"(?m)^## 第 (\d+) 題\s*$", md)
    added = []
    for i in range(1, len(blocks), 2):
        qno = int(blocks[i])
        body = blocks[i + 1].strip()
        if qno in have or len(body) < 30:
            continue
        html = "\n".join("<p>" + x.replace("\n", " ") + "</p>" for x in body.split("\n\n") if x.strip())
        d["questions"].append({"subject": "數學", "year": year, "paper": "Paper 1M", "type": "解答",
                               "qno": qno, "title": f"第 {qno} 題（評卷參考）", "section": "M1",
                               "tags": ["M1"], "text": body, "html": html, "file": src.name})
        added.append(qno)
    d["count"] = len(d["questions"])
    DATA.write_text("window.QB =" + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print(f"{year}: 補 {added}｜總數 {d['count']}")


if __name__ == "__main__":
    main()
