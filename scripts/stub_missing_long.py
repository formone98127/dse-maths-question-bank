# -*- coding: utf-8 -*-
"""Fill remaining long-question analysis gaps with tag-based stubs (+ skills)."""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generate_analysis as ga  # noqa: E402
from scripts.generate_long_analysis import (  # noqa: E402
    PAPER_SLUG,
    attach_long_skills,
    collect_long,
    out_path,
    parse_marks,
)

MISSING = [
    (2012, "Paper 1M", 12),
    (2013, "Paper 1M", 12),
    (2014, "Paper 1M", 12),
    (2015, "Paper 1M", 9),
    (2015, "Paper 1M", 12),
    (2016, "Paper 1M", 12),
    (2017, "Paper 1M", 12),
]


def stub(q: dict) -> dict:
    marks = parse_marks(q.get("text") or "") or 6
    tags = q.get("tags") or ["應用題"]
    report = (q.get("report") or "").strip() or "（無考評報告）"
    analysis = {
        "metadata": {
            "primary_topic": tags[0],
            "secondary_topics": tags[1:3] or [tags[0]],
            "required_formulas": [],
            "bloom_taxonomy_level": "應用",
            "estimated_time_seconds": min(600, max(120, marks * 40)),
            "marks": marks,
        },
        "mark_steps": [
            {
                "step": 1,
                "what": "讀清題目條件與所求",
                "marks": 1,
                "common_error": "漏睇條件或單位",
                "error_category": "Reading-Formatting",
            },
            {
                "step": 2,
                "what": "選用正確公式／模型並列式",
                "marks": max(1, marks // 2),
                "common_error": "用錯公式或模型",
                "error_category": "Conceptual",
            },
            {
                "step": 3,
                "what": "計算並寫出答案",
                "marks": max(1, marks - 1 - max(1, marks // 2)),
                "common_error": "計算或小數位出錯",
                "error_category": "Calculation",
            },
        ],
        "exam_report_insight": report[:120],
        "scaffolding_hints": [
            "Hint 1：先標出已知同未知。",
            "Hint 2：對應課題：" + "、".join(tags[:3]),
            "Hint 3：檢查單位同答題格式。",
        ],
        "quick_solution_strategy": "按標籤課題套公式，逐步得分。",
    }
    return {
        "question": {
            "subject": q["subject"],
            "year": q["year"],
            "paper": q["paper"],
            "qno": q["qno"],
            "hash": ga.hash_for_question(q),
        },
        "model": "tag-stub",
        "generated": datetime.datetime.now().strftime("%Y-%m-%d"),
        "analysis": analysis,
        "skills": attach_long_skills(q, analysis),
        "note": "LLM failed on oversized table/content; stub from tags.",
    }


def main():
    questions = ga.load_questions()
    n = 0
    for year, paper, qno in MISSING:
        cands = collect_long(
            questions, year=str(year), paper=paper, qnos={qno}, chinese_only=False
        )
        if not cands:
            print("no cand", year, paper, qno)
            continue
        q = cands[0]
        path = out_path(q)
        if path.is_file():
            print("exists", path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(stub(q), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        # cleanup bad
        bad = path.with_suffix(".bad")
        if bad.exists():
            bad.unlink()
        print("stub", path.relative_to(ROOT))
        n += 1
    print("stubs", n)


if __name__ == "__main__":
    main()
