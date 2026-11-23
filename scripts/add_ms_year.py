#!/usr/bin/env python3
"""把任一年份的評卷參考（MinerU 抽出的 md）寫入網站 data.js 的「解答」entry。

同 add_ms_2025.py 同一套邏輯，但參數化：

  python scripts/add_ms_year.py --year 2019 --lang en --md ../../dse_scan/work_all/ms_out/ms2019_en.md --dry
  python scripts/add_ms_year.py --year 2019 --lang en --md ... --write

處理兩種 MinerU 輸出：HTML <table> 與 Markdown pipe table（後者常見於末頁）。
遇到「Paper 2 / 試卷二」標題即停止（只取卷一）。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

SITE = pathlib.Path(r"C:\Users\Administrator\projects\dse-maths-question-bank")
TAB = re.compile(r"<table>(.*?)</table>", re.S)
ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL = re.compile(r"<td([^>]*)>(.*?)</td>", re.S)
QHEAD = re.compile(r"^\s*(\d{1,2})\.")
P2HEAD = re.compile(r"(?m)^#*\s*(Paper\s*2|試卷二|卷二)\s*$")


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()


def qnum(text: str) -> int | None:
    m = QHEAD.match(strip_tags(text))
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 19 else None


def trim(cells: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out = list(cells)
    while out and not strip_tags(out[-1][1]):
        out.pop()
    return out


def collect(src: str) -> dict[int, list[str]]:
    cut = P2HEAD.search(src)
    if cut:
        src = src[: cut.start()]
    per_q: dict[int, list[str]] = {}
    cur: int | None = None

    for seg in re.split(r"<!-- page \d+[^>]*-->", src):
        if "<table>" in seg:
            for table in TAB.findall(seg):
                for row in ROW.findall(table):
                    cells = [(a, c) for a, c in CELL.findall(row)]
                    if not cells:
                        continue
                    n = qnum(cells[0][1])
                    if n is not None:
                        cur = n
                        cells = cells[1:]
                    if cur is None:
                        continue
                    cells = trim(cells)
                    if not cells:
                        continue
                    per_q.setdefault(cur, []).append(
                        "<tr>" + "".join(f"<td{a}>{c}</td>" for a, c in cells) + "</tr>")
        elif re.search(r"^\|\s*(Solution|解答|解题)", seg, re.M | re.I):
            for line in seg.splitlines():
                line = line.strip()
                if not line.startswith("|") or set(line) <= {"|", "-", " "}:
                    continue
                cols = [c.strip() for c in line.strip("|").split("|")]
                if cols and re.match(r"(?i)solution|解答", cols[0]):
                    continue
                n = qnum(cols[0]) if cols else None
                if n is not None:
                    cur = n
                    cols = [re.sub(r"^\s*\d{1,2}\.\s*", "", cols[0])] + cols[1:]
                if cur is None:
                    continue
                while cols and not cols[-1]:
                    cols.pop()
                if not cols:
                    continue
                per_q.setdefault(cur, []).append(
                    "<tr>" + "".join(f"<td>{c}</td>" for c in cols) + "</tr>")
    return per_q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", required=True)
    ap.add_argument("--lang", choices=["en", "zh"], required=True)
    ap.add_argument("--md", required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = pathlib.Path(a.md).read_text(encoding="utf-8", errors="replace").replace("\r", "")
    per_q = collect(src)
    got = sorted(n for n in per_q if per_q[n])
    print(f"{a.year}/{a.lang}: {len(got)} 題 → {got}")
    if not got:
        print("無內容，跳過")
        return 1

    if not a.write:
        return 0

    path = SITE / "docs" / "data.js"
    raw = path.read_text(encoding="utf-8")
    head = raw[: raw.index("{")]
    d = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    before = len(d["questions"])
    fname = f"{a.year}_MS_{a.lang}.md"
    # 只換走「今次抽得到」的那幾題；其餘題目保留舊的圖版本，
    # 令該年仍然是 19/19，唔會因為 MinerU 漏一頁而少一題。
    keep_q = {str(n) for n in got}
    d["questions"] = [q for q in d["questions"] if not (
        q.get("type") == "解答"
        and str(q.get("year")) == a.year
        and str(q.get("paper")) == "Paper 1"
        and str(q.get("qno")) in keep_q)]
    added = 0
    for n in got:
        rows = per_q[n]
        html = ('<table class="ms-table"><tr><th>Solution</th><th>Marks</th><th>Remarks</th></tr>'
                + "".join(rows) + "</table>")
        d["questions"].append({
            "subject": "數學", "year": str(a.year), "paper": "Paper 1",
            "type": "解答", "qno": str(n), "title": f"{a.year} 卷一 第 {n} 題 評卷參考",
            "section": "", "tags": [], "text": "", "html": html,
            "file": fname, "lang": a.lang,
        })
        added += 1
    path.write_text(head + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";\n",
                    encoding="utf-8")
    print(f"寫入 {added} 條；entries {before} -> {len(d['questions'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
