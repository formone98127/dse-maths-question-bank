#!/usr/bin/env python3
"""Re-apply every year of maths content from the question bank onto docs/data.js.

`docs/data.js` is a single-line JSON blob that another machine also writes, so
any rebase conflicts on it. The fix is never to merge the text: take the upstream
file, then replay our imports — they are idempotent because each tool replaces
entries by `file` name.

  python scripts/resync_from_bank.py            # dry run
  python scripts/resync_from_bank.py --write
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB = Path(r"C:\Users\Administrator\projects\dse-question-bank")
PY = sys.executable


def years_with(pattern: str, min_q: int = 15) -> list[int]:
    out = []
    for p in sorted(QB.glob(pattern)):
        name = p.name
        try:
            year = int(name[:4])
        except ValueError:
            continue
        n = p.read_text(encoding="utf-8").count("## 第") if "P1" in name else p.read_text(encoding="utf-8").count("**")
        if "P1" in name and n >= min_q:
            out.append(year)
        elif "P2" in name and n >= min_q:
            out.append(year)
    return sorted(set(out))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    flag = ["--write"] if a.write else []

    p1_zh = years_with("*_P1_題目中文卷.md")
    p1_en = years_with("*_P1_題目英文卷.md")
    p2_zh = years_with("*_P2_題目中文卷.md")
    p2_en = years_with("*_P2_題目英文卷.md")
    print("P1 zh", p1_zh, "| P1 en", p1_en)
    print("P2 zh", p2_zh, "| P2 en", p2_en)
    if not a.write:
        return
    for y in p1_zh:
        subprocess.run([PY, "scripts/add_paper1_year.py", str(y), "--lang", "zh", "--write"], cwd=ROOT, check=False)
    for y in p1_en:
        subprocess.run([PY, "scripts/add_paper1_year.py", str(y), "--lang", "en", "--write"], cwd=ROOT, check=False)
    for y in p2_zh:
        subprocess.run([PY, "scripts/add_paper_year.py", str(y), "--lang", "zh", "--write"], cwd=ROOT, check=False)
    for y in p2_en:
        subprocess.run([PY, "scripts/add_paper_year.py", str(y), "--lang", "en", "--write"], cwd=ROOT, check=False)
    for script in ("inject_answers.py", "inject_tags.py"):
        subprocess.run([PY, f"scripts/{script}", "--write"], cwd=ROOT, check=False)
    # 上游同一個年份可能用唔同檔名（2012_P2_questions_EN.md vs 2012_P2_題目英文卷.md）
    # → 用 (year, paper, qno, type, lang) 去重，優先保留我們新造的「題目…卷.md」
    import re as _re
    raw_path = ROOT / "docs" / "data.js"
    raw = raw_path.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    blob = json.loads(body[body.find("{"):].rstrip().rstrip(";"))

    def lang_of(e):
        f = str(e.get("file", ""))
        if _re.search(r"_ZH|中文", f, _re.I):
            return "zh"
        if _re.search(r"_EN|英文|questions_EN", f, _re.I):
            return "en"
        return "zh" if len(_re.findall(r"[\u4e00-\u9fff]", e.get("text", ""))) > 8 else "en"

    # 後出現者勝（我們在檔尾 append，所以會覆蓋上游同名題目）
    merged, dropped = {}, 0
    for e in blob["questions"]:
        key = (e.get("subject"), str(e.get("year")), e.get("paper"), e.get("type"), str(e.get("qno")), lang_of(e))
        if key in merged:
            dropped += 1
        merged[key] = e
    keep = list(merged.values())
    blob["questions"] = keep
    blob["count"] = len(keep)
    raw_path.write_text(head + "window.QB = " + json.dumps(blob, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("dedupe: dropped", dropped, "-> count", blob["count"])

    raw = raw_path.read_text(encoding="utf-8")
    qb = json.loads(raw[raw.find("{"):].rstrip().rstrip(";"))
    print("final:", qb["count"], "entries")


if __name__ == "__main__":
    main()
