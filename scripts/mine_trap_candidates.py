#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mine MC trap candidates from docs/analysis for the trap deck (content pass helper).

Walks docs/analysis/math/*/paper-2*/q*.json, aggregates distractor error_tag
frequency per primary_topic, and prints a ranked candidate list per topic to
stdout for hand-curation into trap_cards.md. Read-only; no docs/ output.

Usage:  PYTHONIOENCODING=utf-8 python scripts/mine_trap_candidates.py [--top 5]
"""
import argparse
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "docs" / "analysis"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=5, help="每課題印幾多個候選伏位")
    args = ap.parse_args()

    by_topic = defaultdict(Counter)   # topic → error_tag → 次數
    examples = defaultdict(list)      # (topic, tag) → [(來源題, thought)] 最初 3 個
    files = sorted(ANALYSIS.glob("math/*/paper-2*/q*.json"))
    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("skip", fp.name, e, file=sys.stderr)
            continue
        analysis = data.get("analysis") or {}
        meta = analysis.get("metadata") or {}
        topic = meta.get("primary_topic") or "（未知課題）"
        # 來源標籤：2012 paper-2 Q5（紙本頁對照用）
        ref = f"{fp.parts[-3]} {fp.parts[-2]} Q{re.sub(r'[^0-9]', '', fp.stem)}"
        for opt in (analysis.get("options_analysis") or {}).values():
            tag = (opt or {}).get("error_tag")
            if not tag:
                continue
            by_topic[topic][tag] += 1
            key = (topic, tag)
            if len(examples[key]) < 3:
                thought = (opt.get("student_thought_process") or "").strip()
                examples[key].append((ref, thought))

    if not by_topic:
        raise SystemExit(f"no analysis json under {ANALYSIS}")

    total = sum(sum(c.values()) for c in by_topic.values())
    print(f"伏位候選（分析檔 {len(files)} 個 · 錯誤標籤 {total} 次）")
    print("手動篩選後寫入 trap_cards.md，再跑 build_trap_cards.py。\n")
    for topic, counter in sorted(by_topic.items(), key=lambda x: -sum(x[1].values())):
        print(f"## {topic}（{sum(counter.values())} 次）")
        for tag, n in counter.most_common(args.top):
            print(f"  {n:>3} × {tag}")
            for ref, thought in examples[(topic, tag)]:
                t = (thought[:60] + "…") if len(thought) > 60 else thought
                print(f"        - {ref}: {t}")
        print()


if __name__ == "__main__":
    main()
