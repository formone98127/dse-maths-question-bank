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


TAGS = {
 "2019": {1:["概率分佈","期望與方差"],2:["概率","條件概率"],3:["二項分佈","概率"],
          4:["概率"],5:["微分法","函數與圖像"],6:["二項式定理","指數級數"],
          7:["微分法","切線"],8:["對數","積分法"],9:["泊松分佈","正態分佈"],
          10:["正態分佈","置信區間"],11:["梯形法","定積分"],12:["微分方程","積分法"]},
 "2020": {1:["概率分佈"],2:["二項分佈"],3:["概率","條件概率"],4:["置信區間"],
          5:["二項式定理","指數級數"],6:["微分法","極值"],7:["微分法","求積法"],
          8:["積分法"],9:["正態分佈","概率"],10:["概率","泊松分佈"],
          11:["梯形法","積分法"],12:["對數","微分法"]},
 "2022": {1:["概率分佈","中央極限定理"],2:["期望與方差"],3:["概率","條件概率"],
          4:["置信區間"],5:["指數級數","對數"],6:["微分法","切線"],
          7:["微分法"],8:["微分法","極值"],9:["正態分佈","泊松分佈"],
          10:["正態分佈","二項分佈"],11:["梯形法","積分法"],12:["微分方程","微分法"]},
 "2023": {1:["概率分佈"],2:["泊松分佈","中央極限定理"],3:["概率","條件概率"],
          4:["概率"],5:["二項式定理","指數級數"],6:["對數","直線方程"],
          7:["定積分","面積"],8:["微分法","梯形法"],9:["正態分佈","置信區間"],
          10:["泊松分佈","概率"],11:["微分法","極值"],12:["積分法","微分方程"]},
 "2024": {1:["概率分佈","獨立事件"],2:["概率","條件概率"],3:["二項分佈"],
          4:["置信區間","標準差"],5:["二項式定理","指數級數"],6:["對數","微分法"],
          7:["微分法","變化率"],8:["正態分佈","積分法"],9:["正態分佈","期望與方差"],
          10:["泊松分佈","條件概率"],11:["對數","梯形法","積分法"],12:["微分方程"]},
 "PP":   {1:["指數級數","對數"],2:["對數","微分法"],3:["微分法","變化率"],
          4:["微分法","切線"],5:["定積分","面積"],6:["正態分佈","置信區間"],
          7:["概率","條件概率"],8:["二項分佈"],9:["概率"],
          10:["梯形法","積分法"],11:["對數","微分方程"],12:["泊松分佈","置信區間"],
          13:["正態分佈","概率"]},
}

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
                "tags": TAGS.get(year, {}).get(int(qno), []),
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
