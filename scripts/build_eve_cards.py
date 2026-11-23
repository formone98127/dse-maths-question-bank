#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build docs/eve/cards.js from eve_cards.md (開考倒數卡組源檔).

Format per card in eve_cards.md:

    ## id | kind | speaker | [trap|true] | [min_days] | [belief_of]
    <dialogue body, LaTeX $…$>
    left: <label> | brain:N,time:N,score:N,mood:N
    right: <label> | brain:N,time:N,score:N,mood:N
    correct: <一句正確講法>          # belief / exam
    exam: <EXAM-id>                   # belief → 對應考試局卡
    timeout: time:-2                  # urgent 唔滑

Usage:  PYTHONIOENCODING=utf-8 python scripts/build_eve_cards.py
"""
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "eve_cards.md"
OUT_DIR = ROOT / "docs" / "eve"
OUT = OUT_DIR / "cards.js"

KINDS = {"life", "urgent", "belief", "exam"}
SPEAKERS = {"self", "parents", "classmate", "tutor", "exam"}
SPEAKER_LABEL = {
    "self": "自己",
    "parents": "爸媽",
    "classmate": "同學",
    "tutor": "補習老師",
    "exam": "考試局",
}
STAT_KEYS = ("brain", "time", "score", "mood")
STAT_RE = re.compile(r"^(brain|time|score|mood):([+-]?\d+)$")
CHOICE_RE = re.compile(r"^(left|right):\s*(.+?)\s*\|\s*(.+)$")
META_RE = re.compile(r"^(correct|exam|timeout):\s*(.+)$")


def parse_effects(s):
    out = {k: 0 for k in STAT_KEYS}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        m = STAT_RE.match(part)
        if not m:
            raise ValueError(f"唔識橫條加減 {part!r}")
        out[m.group(1)] = int(m.group(2))
    return out


def parse_cards():
    text = SRC.read_text(encoding="utf-8")
    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    cards, errors = [], []
    for blk in blocks:
        lines = blk.strip().splitlines()
        head = lines[0].strip()
        parts = [p.strip() for p in head.split("|")]
        while len(parts) < 6:
            parts.append("")
        cid, kind, speaker, flag, min_days, belief_of = parts[:6]
        kind, speaker, flag = kind.lower(), speaker.lower(), flag.lower()
        body, left, right, correct, exam, timeout = [], None, None, None, None, None
        for ln in lines[1:]:
            s = ln.strip()
            if not s:
                if body and body[-1] != "":
                    body.append("")
                continue
            cm = CHOICE_RE.match(s)
            if cm:
                side, label, eff = cm.group(1), cm.group(2).strip(), cm.group(3).strip()
                try:
                    choice = {"label": label, "effects": parse_effects(eff)}
                except ValueError as e:
                    errors.append(f"{cid}: {e}")
                    continue
                if side == "left":
                    left = choice
                else:
                    right = choice
                continue
            mm = META_RE.match(s)
            if mm:
                key, val = mm.group(1), mm.group(2).strip()
                if key == "correct":
                    correct = val
                elif key == "exam":
                    exam = val
                else:
                    try:
                        timeout = parse_effects(val)
                    except ValueError as e:
                        errors.append(f"{cid}: {e}")
                continue
            body.append(ln)
        statement = "\n".join(body).strip()
        cards.append({
            "id": cid,
            "kind": kind,
            "speaker": speaker,
            "flag": flag,
            "min_days": min_days,
            "belief_of": belief_of,
            "statement": statement,
            "left": left,
            "right": right,
            "correct": correct,
            "exam": exam,
            "timeout": timeout,
        })
    return cards, errors


def main():
    cards, errors = parse_cards()
    by_id = {c["id"]: c for c in cards}
    seen = set()

    for c in cards:
        cid = c["id"]
        if cid in seen:
            errors.append(f"{cid}: id 重複")
        seen.add(cid)
        if c["kind"] not in KINDS:
            errors.append(f"{cid}: kind 要係 {KINDS}")
        if c["speaker"] not in SPEAKERS:
            errors.append(f"{cid}: speaker 要係 {SPEAKERS}")
        if not c["statement"]:
            errors.append(f"{cid}: 缺對白")
        if not c["left"] or not c["right"]:
            errors.append(f"{cid}: 要有 left: 同 right:")
        if c["kind"] == "belief":
            if c["flag"] not in ("trap", "true"):
                errors.append(f"{cid}: belief 卡要 trap 或 true")
            if not c["correct"]:
                errors.append(f"{cid}: belief 卡要 correct:")
            if not c["exam"]:
                errors.append(f"{cid}: belief 卡要 exam:")
            elif c["exam"] not in by_id:
                errors.append(f"{cid}: exam {c['exam']} 唔存在")
        if c["kind"] == "exam":
            if not c["belief_of"]:
                errors.append(f"{cid}: exam 卡要 belief_of")
            elif c["belief_of"] not in by_id:
                errors.append(f"{cid}: belief_of {c['belief_of']} 唔存在")
            if not c["correct"]:
                errors.append(f"{cid}: exam 卡要 correct:")
        if c["kind"] == "urgent" and not c["timeout"]:
            errors.append(f"{cid}: urgent 卡要 timeout:")
        if c["min_days"]:
            if not c["min_days"].isdigit():
                errors.append(f"{cid}: min_days 要係數字")
            else:
                c["min_days"] = int(c["min_days"])
        else:
            c["min_days"] = None

    # 雙向對應：belief.exam ↔ exam.belief_of
    for c in cards:
        if c["kind"] == "belief" and c["exam"] in by_id:
            ex = by_id[c["exam"]]
            if ex["belief_of"] and ex["belief_of"] != c["id"]:
                errors.append(f"{c['id']}: exam {c['exam']} 指向 {ex['belief_of']}，唔係自己")
            if not ex["belief_of"]:
                ex["belief_of"] = c["id"]

    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(f"{len(errors)} 個錯，唔產生 cards.js")

    out_cards = []
    for c in cards:
        item = {
            "id": c["id"],
            "kind": c["kind"],
            "speaker": c["speaker"],
            "speaker_label": SPEAKER_LABEL[c["speaker"]],
            "statement": c["statement"],
            "left": c["left"],
            "right": c["right"],
        }
        if c["kind"] == "belief":
            item["is_trap"] = c["flag"] == "trap"
            item["correct"] = c["correct"]
            item["exam"] = c["exam"]
        if c["kind"] == "exam":
            item["belief_of"] = c["belief_of"]
            item["correct"] = c["correct"]
        if c["kind"] == "urgent":
            item["timeout"] = c["timeout"]
        if c["min_days"] is not None:
            item["min_days"] = c["min_days"]
        out_cards.append(item)

    out = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "deck_version": "eve-v1",
        "count": len(out_cards),
        "cards": out_cards,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "/* 由 scripts/build_eve_cards.py 產生；源檔 eve_cards.md；唔好手改 */\n"
        "window.EVE_CARDS = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )

    by_kind = {}
    for c in out_cards:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    print(f"eve cards: {len(out_cards)} 張")
    for k, n in sorted(by_kind.items()):
        print(f"  {k}: {n}")
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
