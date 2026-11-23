#!/usr/bin/env python3
"""Inject the official Paper 2 answers into docs/data.js.

Each maths Paper 2 question entry gains `answer` (and an `answer_pct` only when
the marking scheme prints one), read from the question-bank repo's
cleaned<year>_p2[_zh]/qNN.json — the same values that were extracted from the
marking-scheme table model, not from an LLM free-read. The practice UI in
docs/index.html already keys off `curQ.answer`, so this alone turns on
"撳選項即核對" for every year that has an official key.

  python scripts/inject_answers.py            # dry run
  python scripts/inject_answers.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data.js"
QB = Path(r"C:\Users\Administrator\projects\dse-question-bank")


def load_bank() -> dict:
    """{(year, 'zh'|'en'): {qno: answer}}"""
    out: dict = {}
    for d in QB.glob("cleaned*_p2*"):
        m = re.match(r"cleaned(\d{4})_p2(_zh)?", d.name)
        if not m:
            continue
        key = (int(m.group(1)), "zh" if m.group(2) else "en")
        ans = {}
        for f in d.glob("q*.json"):
            q = json.loads(f.read_text(encoding="utf-8"))
            if q.get("answer"):
                ans[int(q["number"])] = str(q["answer"]).upper()
        if ans:
            out[key] = ans
    # 再由 {year}_P2_答案.md 補（中英共用同一份官方答案鍵）
    for md in QB.glob("*_P2_答案.md"):
        m = re.match(r"(\d{4})_P2_答案", md.name)
        if not m:
            continue
        year = int(m.group(1))
        rows = re.findall(r"\|\s*(\d{1,2})\s*\|\s*([A-D])\s*\|", md.read_text(encoding="utf-8"))
        if not rows:
            continue
        ans = {int(n): a for n, a in rows}
        for lang in ("zh", "en"):
            k = (year, lang)
            merged = dict(ans)
            merged.update(out.get(k, {}))   # cleaned 目錄優先
            out[k] = merged
    return out


def lang_of(entry: dict) -> str:
    f = str(entry.get("file", ""))
    if re.search(r"_(ZH|CHI)|中文", f, re.I):
        return "zh"
    if re.search(r"_(EN|ENG)|英文", f, re.I):
        return "en"
    # 檔名冇語言標記：中文題目會有大量 CJK
    return "zh" if len(re.findall(r"[\u4e00-\u9fff]", entry.get("text", ""))) > 8 else "en"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    bank = load_bank()
    raw = DATA.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    json_txt = body[body.find("{"):].rstrip().rstrip(";")
    qb = json.loads(json_txt)

    filled = miss = 0
    missing_years = set()
    for q in qb["questions"]:
        if q.get("subject") != "數學" or q.get("paper") != "Paper 2" or q.get("type") != "題目":
            continue
        key = (int(q["year"]), lang_of(q))
        ans = bank.get(key, {}).get(int(q["qno"]))
        if not ans:
            # 同一年的中英卷共用同一份官方答案；語言目錄命名不一致時退回另一語言
            other = (key[0], "en" if key[1] == "zh" else "zh")
            ans = bank.get(other, {}).get(int(q["qno"]))
        if ans:
            if q.get("answer") != ans:
                q["answer"] = ans
                filled += 1
        else:
            miss += 1
            missing_years.add(f"{key[0]}-{key[1]}")

    print(f"entries updated: {filled}; still missing: {miss}")
    if missing_years:
        print("no official key for:", sorted(missing_years))
    if a.write and filled:
        out = "window.QB = " + json.dumps(qb, ensure_ascii=False, separators=(",", ":")) + ";\n"
        DATA.write_text(head + out, encoding="utf-8")
        print("wrote", DATA, round(DATA.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
