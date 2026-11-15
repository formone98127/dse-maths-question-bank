#!/usr/bin/env python3
"""Fill `tags` on maths Paper 2 entries in docs/data.js from the question bank.

The practice UI filters by topic in the site data, so a year whose cleaned JSON
has tags but whose data.js entry does not is invisible in 「按課題」. Tags are
copied per question number; the sibling language is used as a fallback because
both editions ask the same questions.

  python scripts/inject_tags.py            # dry run
  python scripts/inject_tags.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data.js"
QB = Path(r"C:\Users\Administrator\projects\dse-question-bank")


def load_tags() -> dict:
    out: dict = {}
    for d in QB.glob("cleaned*_p2*"):
        m = re.match(r"cleaned(\d{4})_p2(_zh)?", d.name)
        if not m:
            continue
        key = (int(m.group(1)), "zh" if m.group(2) else "en")
        tags = {}
        for f in d.glob("q*.json"):
            q = json.loads(f.read_text(encoding="utf-8"))
            if q.get("tags"):
                tags[int(q["number"])] = q["tags"]
        if tags:
            out[key] = tags
    return out


def lang_of(entry: dict) -> str:
    f = str(entry.get("file", ""))
    if re.search(r"_(ZH|CHI)|中文", f, re.I):
        return "zh"
    if re.search(r"_(EN|ENG)|英文", f, re.I):
        return "en"
    return "zh" if len(re.findall(r"[\u4e00-\u9fff]", entry.get("text", ""))) > 8 else "en"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    bank = load_tags()
    raw = DATA.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    qb = json.loads(body[body.find("{"):].rstrip().rstrip(";"))

    filled = still = 0
    empty = set()
    for q in qb["questions"]:
        if q.get("subject") != "數學" or q.get("paper") != "Paper 2" or q.get("type") != "題目":
            continue
        key = (int(q["year"]), lang_of(q))
        tags = bank.get(key, {}).get(int(q["qno"]))
        if not tags:
            other = (key[0], "en" if key[1] == "zh" else "zh")
            tags = bank.get(other, {}).get(int(q["qno"]))
        if tags:
            if q.get("tags") != tags:
                q["tags"] = tags
                filled += 1
        else:
            still += 1
            empty.add(f"{key[0]}-{key[1]}")

    print(f"tagged entries updated: {filled}; still without tags: {still}", sorted(empty))
    if a.write and filled:
        DATA.write_text(head + "window.QB = " + json.dumps(qb, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
        print("wrote", DATA, round(DATA.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
