#!/usr/bin/env python3
"""Add a Paper 2 year to docs/data.js from the question-bank repo's Markdown.

The published site's own build_index.py only knows a handful of hand-listed
sources, so running it would delete every maths year it does not list. This tool
instead parses one finished Markdown file into the exact entry shape the search
app expects (subject/year/paper/type/qno/title/section/tags/text/html/file,
plus `answer` when the official key is present), copies its figure folder into
`docs/<year>P2_figs/`, and splices the entries in next to the same paper's
neighbouring years.

  python scripts/add_paper_year.py 2024            # dry run
  python scripts/add_paper_year.py 2024 --write
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


def parse_md(path: Path, year: int, lang_tag: str = 'zh') -> tuple[list[dict], str]:
    raw = path.read_text(encoding="utf-8")
    lang = "中文" if "中文卷" in path.name else "英文"
    figdir_src = re.search(r"!\[[^\]]*\]\(([^/)]+)/", raw)
    src_dir = figdir_src.group(1) if figdir_src else ""
    # 逐題切：**N.** … 直到下一個 **M.** 或 ## Answers
    blocks = re.split(r"(?m)^\*\*(\d{1,2})\.\*\*\s*", raw)
    entries = []
    section = "Paper 2"
    for i in range(1, len(blocks) - 1, 2):
        n = int(blocks[i])
        body = blocks[i + 1]
        if body.startswith("Answers") or "## Answers" in body[:40]:
            break
        body = body.split("## Answers")[0].strip()
        # 段落 heading
        heads = re.findall(r"(?m)^##\s+(Paper 2.*)$", body)
        if heads:
            section = heads[-1].strip()
        body = re.sub(r"(?m)^##\s+Paper 2.*$", "", body).strip()
        fig_out = f"{year}P2_zh_figs/" if lang_tag == "zh" else f"{year}P2_figs/"
        body = body.replace(f"{src_dir}/", fig_out)
        text = body
        html = markdown.markdown(body, extensions=["tables"])
        entries.append({
            "subject": "數學",
            "year": str(year),
            "paper": "Paper 2",
            "type": "題目",
            "qno": str(n),
            "title": f"第 {n} 題",
            "section": section,
            "tags": [],
            "text": text,
            "html": html,
            "file": path.name,
        })
    return entries, (src_dir if not src_dir else "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    a = ap.parse_args()
    y = a.year
    suffix = "中文卷" if a.lang == "zh" else "英文卷"
    cands = [p for p in QB.glob(f"{y}_P2_題目{suffix}.md")]
    if not cands:
        raise SystemExit(f"no markdown for {y} in {QB}")
    md = cands[0]
    entries, _ = parse_md(md, y, a.lang)

    # 答案（若 cleaned JSON 有）
    answers = {}
    cl = QB / f"cleaned{y}_p2_zh"
    if not cl.exists():
        cl = QB / f"cleaned{y}_p2"
    if cl.exists():
        for f in cl.glob("q*.json"):
            q = json.loads(f.read_text(encoding="utf-8"))
            if q.get("answer"):
                answers[str(q["number"])] = str(q["answer"]).upper()
    for e in entries:
        if e["qno"] in answers:
            e["answer"] = answers[e["qno"]]

    print(f"{md.name}: {len(entries)} questions, {sum(1 for e in entries if 'answer' in e)} with answers")

    # 圖搬去 docs/<year>P2_figs
    if a.lang == "zh":
        src_figs = QB / f"{y}_P2_zh_figs"
        dst_figs = ROOT / "docs" / f"{y}P2_zh_figs"
    else:
        src_figs = QB / f"{y}_P2_figs"
        dst_figs = ROOT / "docs" / f"{y}P2_figs"
    if src_figs.exists():
        print(f"figures: {len(list(src_figs.glob('*.png')))} from {src_figs.name} -> docs/{dst_figs.name}")
        if a.write:
            dst_figs.mkdir(parents=True, exist_ok=True)
            for f in src_figs.glob("*.png"):
                shutil.copy2(f, dst_figs / f.name)
    shutil.copy2(md, ROOT / md.name) if a.write else None

    if not a.write:
        return
    raw = DATA.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    qb = json.loads(body[body.find("{"):].rstrip().rstrip(";"))
    target_file = md.name
    qs = [q for q in qb["questions"] if q.get("file") != target_file]
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
