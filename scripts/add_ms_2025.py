#!/usr/bin/env python3
"""把題庫的 2025_MS.md（MinerU 抽出的評卷參考）寫入網站 data.js 的「解答」entry。

MinerU 出兩種格式：page 3–12 係 HTML <table>，page 13 之後係 Markdown pipe table。
兩種都要處理，否則 Q19 會漏。每題輸出一張乾淨表格（Solution | Marks | Remarks），
掉走題號格、掉走全空行同尾部空 cell，避免 Q18 那種幾百行空白。
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

SITE = pathlib.Path(r"C:\Users\Administrator\projects\dse-maths-question-bank")
MS = pathlib.Path(r"C:\Users\Administrator\projects\dse-question-bank\2025_MS.md")

TAB = re.compile(r"<table>(.*?)</table>", re.S)
ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL = re.compile(r"<td([^>]*)>(.*?)</td>", re.S)
QHEAD = re.compile(r"^\s*(\d{1,2})\.")


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()


def qnum(text: str) -> int | None:
    m = QHEAD.match(strip_tags(text))
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 19 else None


def trim_cells(cells: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out = list(cells)
    while out and not strip_tags(out[-1][1]):
        out.pop()
    return out


def collect(src: str) -> dict[int, list[str]]:
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
                    cells = trim_cells(cells)
                    if not cells:
                        continue
                    body = "".join(f"<td{a}>{c}</td>" for a, c in cells)
                    per_q.setdefault(cur, []).append(f"<tr>{body}</tr>")
        elif re.search(r"^\|\s*Solution", seg, re.M):
            for line in seg.splitlines():
                line = line.strip()
                if not line.startswith("|") or set(line) <= {"|", "-", " "}:
                    continue
                cols = [c.strip() for c in line.strip("|").split("|")]
                if cols and cols[0].lower().startswith("solution"):
                    continue
                n = qnum(cols[0]) if cols else None
                if n is not None:
                    cur = n
                    # pipe table 的題號同解答同一個 cell（"19. (a) Since …"），
                    # 只剝走前綴，唔可以整格掉走，否則第一行解答會唔見。
                    cols = [re.sub(r"^\s*\d{1,2}\.\s*", "", cols[0])] + cols[1:]
                if cur is None:
                    continue
                while cols and not cols[-1]:
                    cols.pop()
                if not cols:
                    continue
                body = "".join(f"<td>{c}</td>" for c in cols)
                per_q.setdefault(cur, []).append(f"<tr>{body}</tr>")
    return per_q


def main() -> int:
    src = MS.read_text(encoding="utf-8").replace("\r", "")
    per_q = collect(src)
    missing = [n for n in range(1, 20) if not per_q.get(n)]
    print("題數:", len([n for n in per_q if per_q[n]]), "缺:", missing or "無")
    for n in range(1, 20):
        rows = per_q.get(n, [])
        print(f"  Q{n}: {len(rows)} 行, {len(''.join(rows))} 字")

    if "--write" in sys.argv:
        path = SITE / "docs" / "data.js"
        raw = path.read_text(encoding="utf-8")
        head = raw[: raw.index("{")]
        d = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
        before = len(d["questions"])
        d["questions"] = [q for q in d["questions"]
                          if not (q.get("type") == "解答" and str(q.get("year")) == "2025")]
        added = 0
        for n, rows in sorted(per_q.items()):
            if not rows:
                continue
            html = ('<table class="ms-table"><tr><th>Solution</th><th>Marks</th>'
                    '<th>Remarks</th></tr>' + "".join(rows) + "</table>")
            d["questions"].append({
                "subject": "數學", "year": "2025", "paper": "Paper 1",
                "type": "解答", "qno": str(n),
                "title": f"2025 卷一 第 {n} 題 評卷參考",
                "section": "", "tags": [], "text": "", "html": html,
                "file": "2025_MS.md",
            })
            added += 1
        path.write_text(head + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";\n",
                        encoding="utf-8")
        print(f"解答 entry 新增 {added} 條；entries {before} -> {len(d['questions'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
