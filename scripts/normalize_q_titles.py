#!/usr/bin/env python3
"""統一 448（＋2012）題目頁嘅 title / og:title / h1 / meta description 格式。

新格式：`{year} DSE 數學 P{paper} Q{qno} 答案＋詳解｜答對率 {pct}%｜DSE 數學題庫`
（P1 冇官方答對率就省略該段）

用法：python3 scripts/normalize_q_titles.py [--dry]
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
QDIR = REPO / "docs/questions"
IDX = QDIR / "_index.json"


def load_pct():
    data = json.loads(IDX.read_text(encoding="utf-8"))
    out = {}
    for q in data:
        key = (str(q["year"]), str(q["paper"]), str(q["qno"]).strip("qQ"))
        pc = q.get("answer_pct")
        if pc is None:
            continue
        try:
            out[key] = int(round(float(pc)))
        except (TypeError, ValueError):
            continue
    return out


def build(year, paper, qno, pct):
    head = f"{year} DSE 數學 P{paper} Q{qno} 答案＋詳解"
    if pct is not None:
        head += f"｜答對率 {pct}%"
    return head + "｜DSE 數學題庫"


def main():
    dry = "--dry" in sys.argv
    pct_map = load_pct()
    changed = 0
    for page in sorted(QDIR.rglob("index.html")):
        parts = page.parts
        try:
            i = parts.index("math")
            year, paper, qslug = parts[i + 1], parts[i + 2], parts[i + 3]
        except (ValueError, IndexError):
            continue
        if not qslug.startswith("q"):
            continue
        paper_no = paper.replace("paper-", "")
        qno = qslug[1:]
        pct = pct_map.get((year, paper_no, qno))
        new_title = build(year, paper_no, qno, pct)

        html = page.read_text(encoding="utf-8")
        orig = html
        html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1)
        html = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + new_title + m.group(2), html, count=1)
        html = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + new_title + m.group(2), html, count=1)
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{new_title.replace('｜DSE 數學題庫', '')}</h1>", html, count=1)

        # meta description：確保有「年份＋卷＋題號」前綴
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        if m:
            desc = m.group(1)
            prefix = f"【{year} DSE 數學 Paper {paper_no} 第 {qno} 題】"
            if not desc.startswith("【"):
                desc = prefix + desc
            if len(desc) > 165:
                desc = desc[:162].rstrip("，。、 ") + "…"
            html = html.replace(m.group(0), f'<meta name="description" content="{desc}"', 1)
            html = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
                          lambda mm: mm.group(1) + desc + mm.group(2), html, count=1)

        if html != orig:
            changed += 1
            if not dry:
                page.write_text(html, encoding="utf-8")
    print(f"{'[dry] ' if dry else ''}updated {changed} pages")


if __name__ == "__main__":
    main()
