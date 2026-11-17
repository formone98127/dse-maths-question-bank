#!/usr/bin/env python3
"""Put the HKEAA examiner-report notes under each question on the site.

Source: dse-question-bank / reports<year>[_en].json (tools/report_notes.py).

Each question entry in docs/data.js gets the note appended as a collapsible block:

    <details class="exam-note"><summary>考評報告這樣說</summary><p>…</p></details>

Keyed by (year, language, paper, question) — the paper MUST be part of the key, or a
Paper 1 note for Q5 lands on Paper 2 Q5 as well (that mistake put 934 boxes on the
site when only 590 notes exist). Only 題目 entries get the box, never 解答 pages.

  python scripts/inject_reports.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BANK = SITE.parent / "dse-question-bank"
DATA = SITE / "docs" / "data.js"

INLINE = re.compile(r"【考生表現】\s*(.*?)\s*(?=【題目內容】|$)", re.S)


def bank_reports() -> dict[tuple[str, str, int, int], str]:
    out: dict[tuple[str, str, int, int], str] = {}
    for f in BANK.glob("reports*.json"):
        m = re.match(r"reports(\d{4})(_en)?\.json", f.name)
        if not m:
            continue
        year, lang = m.group(1), ("en" if m.group(2) else "zh")
        d = json.loads(f.read_text(encoding="utf-8"))
        for k, v in d["paper"]["p1"].items():
            mm = re.match(r"\s*(\d{1,2})", k)
            if not (mm and v.strip()):
                continue
            key = (year, lang, 1, int(mm.group(1)))
            letters = re.findall(r"\(([a-c])\)", k)
            txt = f"（{letters[0]}）{v.strip()}" if len(letters) == 1 else v.strip()
            out[key] = (out[key] + "\n\n" + txt) if key in out else txt
        for k, v in d["paper"]["p2"].items():
            if k.isdigit() and v.strip():
                out[(year, lang, 2, int(k))] = v.strip()
    return out


def note_html(note: str) -> str:
    """One <p> per paragraph, so （a）/（b） sit on separate lines on the site."""
    def esc(x: str) -> str:
        return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    paras = [p.strip() for p in str(note).split("\n\n") if p.strip()]
    body = "".join(f"<p>{esc(x)}</p>" for x in paras)
    return ('<details class="exam-note"><summary>考評報告這樣說</summary>'
            f'{body}</details>')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    notes = bank_reports()
    s = DATA.read_text(encoding="utf-8")
    head, body = s.split("=", 1)
    d = json.loads(body.strip().rstrip(";"))

    n = 0
    for q in d["questions"]:
        if q.get("subject") != "數學" or str(q.get("type")) != "題目":
            continue
        year = str(q.get("year"))
        lang = "en" if "英文" in str(q.get("file", "")) else "zh"
        paper = 1 if str(q.get("paper")) == "Paper 1" else 2
        try:
            qno = int(q.get("qno"))
        except (TypeError, ValueError):
            continue
        note = notes.get((year, lang, paper, qno))
        if not note:
            continue
        for field in ("text", "html"):
            v = q.get(field) or ""
            if "【考生表現】" in v:
                q[field] = INLINE.sub("", v)
        # an older box (e.g. the pre-fix text) must be replaced, not stacked
        html = q.get("html") or ""
        html = re.sub(r'(?:<p>)?<details class="exam-note">.*?</details>(?:</p>)?', "", html, flags=re.S)
        box = note_html(note)
        q["html"] = html + "<p>" + box + "</p>"
        q["report"] = note
        n += 1

    print("entries updated:", n)
    if a.write:
        DATA.write_text(head + "=" + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";",
                        encoding="utf-8")
        print("wrote", DATA.name, round(DATA.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
