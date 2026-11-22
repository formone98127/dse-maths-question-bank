#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build docs/trap/cards.js from trap_cards.md (MC 伏位快問卡組源檔).

Format per card in trap_cards.md:

    ## id | 課題 tag | trap|true | 難度 1–3 | source_ref(可選)
    <statement body, LaTeX $…$ / $$…$$>
    hint: <一句廣東話提示>

Validates ids, topic tags (must be in TOPICS.math), hint length, trap ratio,
and source_ref against docs/data.js QB. Idempotent.

Usage:  PYTHONIOENCODING=utf-8 python scripts/build_trap_cards.py
"""
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows console cp1252 guard（同 build_index.py）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "trap_cards.md"
OUT_DIR = ROOT / "docs" / "trap"
OUT = OUT_DIR / "cards.js"

HINT_MAX = 60          # 提示上限（字）；過長只警告唔阻 build
TRAP_RATIO = (0.30, 0.75)  # trap 卡佔比超出範圍只警告（樣例階段會偏）
SOURCE_RE = re.compile(r"^(\d{4})P([12])Q(\d+)$")


def load_math_topics():
    """docs/hub/data.js TOPICS.math → {strand: [tags]}（同 build_seo.parse_topics 手法）。"""
    text = (ROOT / "docs" / "hub" / "data.js").read_text(encoding="utf-8")
    start = text.index("const TOPICS = ")
    blob = text[start:text.index("const PDF_LINKS", start)]
    m = re.search(r"math:\s*\{(.*?)\n  \},", blob, re.S)
    if not m:
        raise SystemExit("TOPICS.math not found in hub/data.js")
    topics = {}
    for name, arr in re.findall(r'"([^"]+)":\s*\[(.*?)\]', m.group(1), re.S):
        topics[name] = re.findall(r'"([^"]+)"', arr)
    return topics


def load_qb_index():
    """docs/data.js QB → set of (year, paper_no, qno)（source_ref 對照用）。"""
    text = (ROOT / "docs" / "data.js").read_text(encoding="utf-8")
    data, _ = json.JSONDecoder().raw_decode(text[text.index("=") + 1:].lstrip())
    idx = set()
    for q in data.get("questions", []):
        pm = re.search(r"(\d+)", str(q.get("paper", "")))
        if not pm:
            continue
        try:
            idx.add((str(q.get("year")), pm.group(1).upper(), int(q.get("qno"))))
        except (TypeError, ValueError):
            continue
    return idx


def parse_cards():
    text = SRC.read_text(encoding="utf-8")
    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    cards, errors, warnings = [], [], []
    for blk in blocks:
        lines = blk.strip().splitlines()
        head = lines[0].strip()
        parts = [p.strip() for p in head.split("|")]
        if not (4 <= len(parts) <= 5):
            errors.append(f"{head!r}: header 要 4–5 欄（id | 課題 | trap|true | 難度 | source_ref?）")
            continue
        cid, topic, flag, diff = parts[0], parts[1], parts[2].lower(), parts[3]
        src = parts[4] if len(parts) == 5 else ""
        body, hint = [], None
        for ln in lines[1:]:
            hm = re.match(r"^hint:\s*(.+)$", ln.strip())
            if hm:
                hint = hm.group(1).strip()
                break
            body.append(ln)
        statement = "\n".join(body).strip()
        if not statement or hint is None:
            errors.append(f"{cid}: 缺 statement 或 hint: 行")
            continue
        cards.append({
            "id": cid, "topic": topic, "flag": flag, "diff": diff,
            "src": src, "statement": statement, "hint": hint,
        })
    return cards, errors, warnings


def main():
    topics = load_math_topics()
    tag_to_strand = {t: s for s, ts in topics.items() for t in ts}
    qb = load_qb_index()
    cards, errors, warnings = parse_cards()

    seen = set()
    for c in cards:
        cid = c["id"]
        if cid in seen:
            errors.append(f"{cid}: id 重複")
        seen.add(cid)
        if c["topic"] not in tag_to_strand:
            errors.append(f"{cid}: 課題 {c['topic']!r} 唔喺 TOPICS.math 20 個 tag 入面")
        if c["flag"] not in ("trap", "true"):
            errors.append(f"{cid}: 第三欄只可以係 trap 或 true")
        if c["diff"] not in ("1", "2", "3"):
            errors.append(f"{cid}: 難度要 1–3")
        if len(c["hint"]) > HINT_MAX:
            warnings.append(f"{cid}: hint {len(c['hint'])} 字 > {HINT_MAX}")
        if c["src"]:
            m = SOURCE_RE.match(c["src"])
            if not m:
                errors.append(f"{cid}: source_ref {c['src']!r} 唔符 YYYY P1/P2 Qn 格式")
            elif (m.group(1), m.group(2), int(m.group(3))) not in qb:
                errors.append(f"{cid}: source_ref {c['src']} 喺 data.js QB 搵唔到")

    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(f"{len(errors)} 個錯，唔產生 cards.js")

    n_trap = sum(1 for c in cards if c["flag"] == "trap")
    ratio = n_trap / len(cards) if cards else 0
    if cards and not (TRAP_RATIO[0] <= ratio <= TRAP_RATIO[1]):
        warnings.append(f"trap 佔比 {ratio:.0%} 唔喺 {TRAP_RATIO[0]:.0%}–{TRAP_RATIO[1]:.0%}")

    out = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "deck_version": "trap-v1",
        "count": len(cards),
        "strands": topics,
        "cards": [
            {
                "id": c["id"],
                "topic": c["topic"],
                "strand": tag_to_strand[c["topic"]],
                "statement": c["statement"],
                "is_trap": c["flag"] == "trap",
                "hint": c["hint"],
                **({"source_ref": c["src"]} if c["src"] else {}),
                "difficulty": int(c["diff"]),
            }
            for c in cards
        ],
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "/* 由 scripts/build_trap_cards.py 產生；源檔 trap_cards.md；唔好手改 */\n"
        "window.TRAP_CARDS = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )

    per_topic = {}
    for c in cards:
        per_topic[c["topic"]] = per_topic.get(c["topic"], 0) + 1
    print(f"trap cards: {len(cards)} 張（trap {n_trap} / true {len(cards) - n_trap}）")
    for t, n in sorted(per_topic.items(), key=lambda x: -x[1]):
        print(f"  {t}: {n}")
    for w in warnings:
        print("WARN", w)
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
