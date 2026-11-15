#!/usr/bin/env python3
"""Add a Paper 1 year (long questions) to docs/data.js from the question bank.

Paper 1 has a different Markdown shape than Paper 2 — `## 第 N 題` blocks with
【建議標籤】 (卷別/部分 + 課題) and 【題目內容】 — so it needs its own parser. The
entries keep the SOP section (甲部(1)/甲部(2)/乙部) and the topic tags, which is
what the site filters on. No `answer` field: Paper 1 ships without answers.

  python scripts/add_paper1_year.py 2015 --lang zh            # dry run
  python scripts/add_paper1_year.py 2015 --lang zh --write
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data.js"
QB = Path(r"C:\Users\Administrator\projects\dse-question-bank")


def parse(path: Path, year: int) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    figdir = re.search(r"!\[[^\]]*\]\(([^/)]+)/", raw)
    src_dir = figdir.group(1) if figdir else f"{year}_P1_zh_figs"
    out_dir = src_dir.replace("_P1_zh_figs", "P1_zh_figs").replace("_P1_figs", "P1_figs")
    raw = re.sub(r"(?m)^## Question\s+(\d+)\s*$", r"## 第 \1 題", raw)
    parts = re.split(r"(?m)^## 第 (\d+) 題\s*$", raw)
    entries = []
    for i in range(1, len(parts) - 1, 2):
        n = int(parts[i])
        body = parts[i + 1]
        sec = re.search(r"卷別/部分：Paper 1[　\s·]+([^\n]+)", body)
        section = f"Paper 1　{sec.group(1).strip()}" if sec else "Paper 1"
        topics = re.search(r"課題：([^\n]+)", body)
        tags = [t.strip("# ").strip() for t in topics.group(1).split("#") if t.strip()] if topics else []
        content = body.split("【題目內容】", 1)[-1].strip()
        content = re.sub(r"(?m)^\s*---\s*$", "", content).replace(f"{src_dir}/", f"{out_dir}/")
        entries.append({
            "subject": "數學",
            "year": str(year),
            "paper": "Paper 1",
            "type": "題目",
            "qno": str(n),
            "title": f"第 {n} 題",
            "section": section,
            "tags": tags,
            "text": content,
            "html": markdown.markdown(content, extensions=["tables"]),
            "file": path.name,
        })
    return entries


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int)
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    suffix = "中文卷" if a.lang == "zh" else "英文卷"
    md = QB / f"{a.year}_P1_題目{suffix}.md"
    if not md.exists():
        raise SystemExit(f"no {md.name}")
    entries = parse(md, a.year)
    if not entries:
        raise SystemExit(f"parsed 0 questions from {md.name} — 唔郁 data.js")
    print(f"{md.name}: {len(entries)} questions, tags {sum(1 for e in entries if e['tags'])}")

    src_figs = QB / (f"{a.year}_P1_zh_figs" if a.lang == "zh" else f"{a.year}_P1_figs")
    dst_figs = ROOT / "docs" / (f"{a.year}P1_zh_figs" if a.lang == "zh" else f"{a.year}P1_figs")
    if src_figs.exists():
        print(f"figures: {len(list(src_figs.glob('*.png')))} -> docs/{dst_figs.name}")
    if not a.write:
        return
    if src_figs.exists():
        dst_figs.mkdir(parents=True, exist_ok=True)
        for f in src_figs.glob("*.png"):
            shutil.copy2(f, dst_figs / f.name)
    shutil.copy2(md, ROOT / md.name)

    raw = DATA.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    qb = json.loads(body[body.find("{"):].rstrip().rstrip(";"))
    qs = [q for q in qb["questions"] if q.get("file") != md.name]
    qs.extend(entries)
    qs.sort(key=lambda q: (q.get("subject", ""), -int(q["year"]), q.get("paper", ""), int(q.get("qno") or 0)))
    qb["questions"] = qs
    qb["count"] = len(qs)
    import time
    qb["generated"] = time.strftime("%Y-%m-%d %H:%M")
    DATA.write_text(head + "window.QB = " + json.dumps(qb, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("data.js:", round(DATA.stat().st_size / 1e6, 2), "MB,", qb["count"], "entries")


if __name__ == "__main__":
    main()
