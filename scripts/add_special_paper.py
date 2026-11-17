#!/usr/bin/env python3
"""把「樣本試卷 / 練習卷」（SP / PP）整合入主網 data.js。

題庫的 md 格式同其他年份一樣（`## 第 N 題` 或 `## Question N`），
但 year 唔係四位數字，所以:

  year = "PP" / "SP"   paper = "Paper 1"

圖由 `PP_P1_figs_svg/` 之類複製到 `docs/PPP1_zh_figs/`（英文 → `PPP1_figs/`）。

  python scripts/add_special_paper.py PP --lang zh          # dry run
  python scripts/add_special_paper.py PP --lang zh --write
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


def parse(path: Path, tag: str, lang: str) -> list[dict]:
    raw = path.read_text(encoding="utf-8").replace("\r", "")
    blocks = re.split(r"(?m)^##\s+(?:第\s*(\d+)\s*題|Question\s*(\d+))\s*$", raw)
    src_fig = re.search(r"!\[[^\]]*\]\(([^/)]+)/", raw)
    src_dir = src_fig.group(1) if src_fig else ""
    out_dir = f"{tag}P1_zh_figs" if lang == "zh" else f"{tag}P1_figs"

    entries = []
    for i in range(1, len(blocks) - 1, 3):
        n = blocks[i] or blocks[i + 1]
        body = blocks[i + 2].strip()
        m_sec = re.search(r"卷別/部分：\s*(.+)", body)
        section = m_sec.group(1).strip() if m_sec else f"Paper 1"
        m_tag = re.search(r"課題：\s*(.+)", body)
        # 「#Algebra #Laws of Indices」→ 以 # 分段，唔可以按空白切（會把 Laws of Indices 拆散）
        tags = [t.strip() for t in m_tag.group(1).split("#") if t.strip()] if m_tag else []
        body = body.split("【題目內容】", 1)[-1].strip()
        body = re.sub(r"(?m)^---\s*$", "", body).strip()
        if src_dir:
            body = body.replace(f"{src_dir}/", f"{out_dir}/")
        html = markdown.markdown(body, extensions=["tables"])
        entries.append({
            "subject": "數學",
            "year": tag,
            "paper": "Paper 1",
            "type": "題目",
            "qno": str(int(n)),
            "title": f"第 {int(n)} 題",
            "section": section,
            "tags": tags,
            "text": body,
            "html": html,
            "file": path.name,
        })
    return entries, src_dir, out_dir


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", choices=["PP", "SP"])
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    name = f"{a.tag}_P1_題目{'中文卷' if a.lang == 'zh' else '英文卷'}.md"
    path = QB / name
    entries, src_dir, out_dir = parse(path, a.tag, a.lang)
    print(f"{name}: {len(entries)} 題；圖 {src_dir or '無'} → docs/{out_dir}")
    for e in entries[:3]:
        print("  Q", e["qno"], "|", e["section"], "|", e["tags"], "|", e["text"][:50])

    if not a.write:
        return 0

    raw = DATA.read_text(encoding="utf-8")
    head = raw[: raw.index("{")]
    d = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    before = len(d["questions"])
    d["questions"] = [q for q in d["questions"]
                      if not (q.get("year") == a.tag and q.get("paper") == "Paper 1"
                              and q.get("file") == name)]
    d["questions"].extend(entries)

    DATA.write_text(head + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";\n",
                    encoding="utf-8")

    if src_dir:
        src = QB / src_dir
        dst = ROOT / "docs" / out_dir
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in src.iterdir():
            if f.suffix.lower() == ".png":
                shutil.copy2(f, dst / f.name)
                n += 1
        print(f"圖複製 {n} 個 → docs/{out_dir}")
    print(f"entries {before} -> {len(d['questions'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
