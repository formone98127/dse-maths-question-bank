"""把 M1 題目（題庫 md）匯入網站 docs/data.js。

用法：python scripts/add_m1_year.py 2019 --write
      python scripts/add_m1_year.py --all --write

規則：
- 只讀 `M1_<year>_P1_EN.md`（`## 第 N 題` 分塊）
- paper 用 "Paper 1M"（pno → "1M"，唔會同 Paper 1 撞）
- type = 題目；section = "M1"；lang 由檔名推（_EN / _ZH）
- 以 (year, paper, qno, type) 取代舊 entry，可重跑
"""
from __future__ import annotations

import argparse
import json
import re
import pathlib

BANK = pathlib.Path(r"C:/Users/Administrator/projects/dse-question-bank")
SITE = pathlib.Path(r"C:/Users/Administrator/projects/dse-maths-question-bank")


def md_to_html(block: str) -> str:
    out = []
    for para in re.split(r"\n\s*\n", block.strip()):
        p = para.strip()
        if not p:
            continue
        if p.startswith("|"):                      # 表格
            rows = [r for r in p.split("\n") if r.strip().startswith("|")]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if len(cells) >= 2:
                head = "".join(f"<th>{c}</th>" for c in cells[0])
                body = "".join(
                    "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                    for r in cells[2:]
                )
                out.append(f'<table class="m1-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
            continue
        if p.startswith("!["):                      # 圖：略過，留文字
            continue
        if p.startswith("$$"):
            out.append(f"<p>{p}</p>")
        else:
            out.append(f"<p>{p}</p>")
    return "\n".join(out)


def parse(path: pathlib.Path):
    txt = path.read_text(encoding="utf-8")
    parts = re.split(r"^## 第 (\d+) 題\s*$", txt, flags=re.M)
    out = []
    for i in range(1, len(parts) - 1, 2):
        qno = parts[i]
        body = parts[i + 1].strip()
        body = re.sub(r"^\*試卷完.*$", "", body, flags=re.M).strip()
        out.append((qno, body))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("year", nargs="?", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    files = sorted(BANK.glob("M1_*_P1_EN.md")) if a.all else sorted(
        BANK.glob(f"M1_{a.year}_P1_EN.md"))
    if not files:
        print("找不到 M1 md")
        return 2

    data_js = SITE / "docs" / "data.js"
    raw = data_js.read_text(encoding="utf-8")
    obj = json.loads(raw[len("window.QB ="):].rstrip().rstrip(";"))

    added = 0
    for f in files:
        m = re.match(r"M1_(\w+)_P1_EN\.md", f.name)
        if not m:
            continue
        year = m.group(1)
        items = parse(f)
        keys = {(year, "Paper 1M", q) for q, _ in items}
        obj["questions"] = [
            e for e in obj["questions"]
            if not (str(e.get("year")) == year and e.get("paper") == "Paper 1M" and e.get("type") == "題目")
        ]
        for qno, body in items:
            obj["questions"].append({
                "subject": "數學",
                "year": year,
                "paper": "Paper 1M",
                "type": "題目",
                "qno": qno,
                "title": f"第 {qno} 題",
                "section": "M1",
                "tags": [],
                "text": re.sub(r"\s+", " ", body)[:1200],
                "html": md_to_html(body),
                "file": f.name,
            })
            added += 1
        print(f"{year}: {len(items)} 題")

    obj["count"] = len(obj["questions"])
    if a.write:
        data_js.write_text("window.QB =" + json.dumps(obj, ensure_ascii=False) + ";", encoding="utf-8")
        print(f"寫入 docs/data.js，count={obj['count']}，新增 {added}")
    else:
        print(f"[dry-run] count 會變 {obj['count']}，新增 {added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
