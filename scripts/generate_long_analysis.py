# -*- coding: utf-8 -*-
"""Generate deep analysis for math long questions (Paper 1 / Paper 1M).

Writes docs/analysis/math/<year>/paper-1|paper-1m/q<n>.json with analysis + skills.
Skills use step_faults (no ABCD). Reuses generate_analysis LLM client + skill book.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generate_analysis as ga  # noqa: E402

DOCS = ROOT / "docs"
ANALYSIS = DOCS / "analysis" / "math"

PAPER_SLUG = {"Paper 1": "paper-1", "Paper 1M": "paper-1m", "卷一": "paper-1"}

SYSTEM = """你是一位擁有 20 年經驗的 DSE 數學卷一閱卷專家。請對輸入的長題進行解構。

輸出一個有效 JSON 物件（嚴禁 markdown fences），Schema：

{
  "metadata": {
    "primary_topic": "字串",
    "secondary_topics": ["1-3 個次考點"],
    "required_formulas": ["核心公式/定理，LaTeX"],
    "bloom_taxonomy_level": "記憶|理解|應用|分析|評鑑|創造",
    "estimated_time_seconds": 60-600 整數,
    "marks": 本題總分整數（由題幹括號分數推斷）
  },
  "mark_steps": [
    {
      "step": 1,
      "what": "這步要做什麼（30字內）",
      "marks": 分數整數,
      "common_error": "這步常見錯法（40字內，可空字串）",
      "error_category": null 或 "Conceptual"|"Calculation"|"Reading-Formatting"|"Methodological"
    }
  ],
  "exam_report_insight": "結合考評報告寫一句（若無報告則根據題目推測）",
  "scaffolding_hints": ["Hint1 啟發", "Hint2 知識", "Hint3 破題"],
  "quick_solution_strategy": "40字內速解切入"
}

要求：繁體中文；數學用 $...$ / $$...$$；mark_steps 2-6 步；各 common_error 短；不要輸出 skills。"""


def is_chinese(q: dict) -> bool:
    return ga._is_chinese_question(q)


def year_ok(q_year, year) -> bool:
    return ga._year_matches(q_year, year)


def collect_long(questions, year=None, paper=None, qnos=None, chinese_only=True):
    out = []
    for q in questions:
        if q.get("type") != "題目" or q.get("subject") != "數學":
            continue
        if paper and q.get("paper") != paper:
            continue
        if q.get("paper") not in ("Paper 1", "Paper 1M"):
            continue
        if not year_ok(q.get("year"), year):
            continue
        qno_i = int(re.sub(r"\D", "", str(q.get("qno", ""))) or 0)
        if qnos and qno_i not in qnos:
            continue
        if chinese_only and not is_chinese(q):
            # keep English only if no Chinese twin later
            pass
        out.append(q)

    # dedupe: prefer Chinese
    best = {}
    for q in out:
        key = (str(q["year"]), str(q["paper"]), str(q["qno"]))
        zh = is_chinese(q)
        if key not in best or (zh and not is_chinese(best[key])):
            best[key] = q
    rows = list(best.values())
    if chinese_only:
        # drop English-only only when chinese_only and we have Chinese preference already applied
        rows = [q for q in rows if is_chinese(q) or True]
        # Prefer Chinese; if only English exists keep it
        filtered = []
        by = {}
        for q in rows:
            key = (str(q["year"]), str(q["paper"]), str(q["qno"]))
            by.setdefault(key, []).append(q)
        for key, group in by.items():
            zh = [g for g in group if is_chinese(g)]
            filtered.append(zh[0] if zh else group[0])
        rows = filtered
    rows.sort(
        key=lambda q: (
            str(q["year"]),
            str(q["paper"]),
            int(re.sub(r"\D", "", str(q["qno"])) or 0),
        )
    )
    return rows


def out_path(q: dict) -> Path:
    slug = PAPER_SLUG.get(str(q["paper"]), "paper-1")
    return ANALYSIS / str(q["year"]) / slug / f"q{q['qno']}.json"


def parse_marks(text: str) -> int | None:
    m = re.search(r"[（(]\s*(\d+)\s*分\s*[）)]", text or "")
    if m:
        return int(m.group(1))
    m = re.search(r"\((\d+)\s*marks?\)", text or "", re.I)
    return int(m.group(1)) if m else None


def validate_long(obj: dict) -> list[str]:
    errs = []
    md = obj.get("metadata")
    if not isinstance(md, dict):
        return ["缺 metadata"]
    for k in ("primary_topic", "secondary_topics", "required_formulas", "bloom_taxonomy_level", "estimated_time_seconds"):
        if k not in md:
            errs.append(f"metadata 缺 {k}")
    if md.get("bloom_taxonomy_level") not in ga.BLOOM_LEVELS:
        errs.append("bloom_taxonomy_level 無效")
    t = md.get("estimated_time_seconds")
    if not isinstance(t, int) or not (60 <= t <= 600):
        errs.append(f"estimated_time_seconds 須 60-600，得 {t!r}")
    steps = obj.get("mark_steps")
    if not isinstance(steps, list) or not (2 <= len(steps) <= 8):
        errs.append("mark_steps 須 2-8 步")
    else:
        for s in steps:
            if not isinstance(s, dict) or "step" not in s or not s.get("what"):
                errs.append("mark_steps 項目不完整")
                break
            cat = s.get("error_category")
            if cat is not None and cat not in ga.ERROR_CATEGORIES:
                errs.append(f"error_category 無效 {cat!r}")
    hints = obj.get("scaffolding_hints")
    if not isinstance(hints, list) or len(hints) != 3:
        errs.append("scaffolding_hints 須 3 個")
    if not obj.get("quick_solution_strategy"):
        errs.append("缺 quick_solution_strategy")
    return errs


def attach_long_skills(q: dict, analysis: dict) -> dict:
    base = ga.attach_skills_post(q, {**analysis, "options_analysis": {}})
    # map mark_steps → step_faults
    faults = {}
    for s in analysis.get("mark_steps") or []:
        if not isinstance(s, dict):
            continue
        step = str(s.get("step"))
        cat = s.get("error_category")
        if not cat and not (s.get("common_error") or "").strip():
            continue
        aid = ga.CAT_TO_ABILITY.get(cat, "A-ALG")
        kid = (base.get("knowledge_point_ids") or [None])[0]
        fid = (base.get("formula_ids") or [None])
        fid = fid[0] if fid else None
        faults[step] = {
            "knowledge_point_id": kid,
            "formula_id": fid,
            "ability_id": aid,
            "error_category": cat,
        }
    base["option_faults"] = {}
    base["step_faults"] = faults
    return base


def build_user_prompt(q: dict) -> str:
    marks = parse_marks(q.get("text") or "")
    lines = [
        f"科目：數學　年份：{q['year']}　卷別：{q['paper']}　第 {q['qno']} 題",
        f"標籤：{', '.join(q.get('tags') or []) or '（無）'}",
        f"題幹標示分數：{marks if marks is not None else '未知'}",
        "",
        "【題目】",
        (q.get("text") or "").strip(),
        "",
        "【考評報告】",
        (q.get("report") or "（無）").strip(),
    ]
    return "\n".join(lines)


def process_one(q: dict, cfg: dict, force=False) -> bool:
    path = out_path(q)
    if path.is_file() and not force:
        print(f"↷ skip {path.relative_to(ROOT)}")
        return False
    prompt = build_user_prompt(q)
    print(f"→ {q['year']} {q['paper']} Q{q['qno']} model={cfg['model']}")
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt},
    ]
    content = ""
    for attempt in range(1, 4):
        try:
            content = ga.call_llm(cfg, messages)
            obj = ga.parse_llm_json(content)
        except Exception as e:
            errs = [str(e)[:200]]
            print(f"  ✗ try {attempt}: {errs[0]}")
            continue
        obj.pop("skills", None)
        # fill marks if missing
        md = obj.get("metadata") if isinstance(obj, dict) else None
        if isinstance(md, dict) and "marks" not in md:
            m = parse_marks(q.get("text") or "")
            if m is not None:
                md["marks"] = m
        errs = validate_long(obj) if isinstance(obj, dict) else ["not object"]
        if not errs:
            skills = attach_long_skills(q, obj)
            payload = {
                "question": {
                    "subject": q["subject"],
                    "year": q["year"],
                    "paper": q["paper"],
                    "qno": q["qno"],
                    "hash": ga.hash_for_question(q),
                },
                "model": cfg["model"],
                "generated": datetime.datetime.now().strftime("%Y-%m-%d"),
                "analysis": obj,
                "skills": skills,
            }
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"  ✓ {path.relative_to(ROOT)}")
            return True
        print(f"  ✗ try {attempt}: {errs}")
        messages.append({"role": "assistant", "content": content})
        messages.append(
            {
                "role": "user",
                "content": "修正以下問題後重新輸出完整 JSON：\n- " + "\n- ".join(errs),
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.with_suffix(".bad").write_text(content or "", encoding="utf-8")
    print(f"  ✗ give up Q{q['qno']}")
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=str, help="year or PP/SP")
    ap.add_argument("--paper", choices=["Paper 1", "Paper 1M"], default="Paper 1")
    ap.add_argument("--question", type=int, action="append")
    ap.add_argument("--range", dest="qrange")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all-langs", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--temperature", type=float, default=0.3)
    args = ap.parse_args()

    questions = ga.load_questions()
    qnos = set(args.question or [])
    if args.qrange:
        qnos |= ga.parse_qno_spec(args.qrange)
    year = args.year
    # allow int years via string
    cands = collect_long(
        questions,
        year=year,
        paper=args.paper,
        qnos=qnos or None,
        chinese_only=not args.all_langs,
    )
    if args.list:
        for q in cands:
            print(f"{q['year']} {q['paper']} Q{q['qno']} tags={q.get('tags')} file={q.get('file')}")
        print(f"共 {len(cands)} 題")
        return
    if not cands:
        raise SystemExit("找不到題目")

    class A:
        provider = None
        base_url = None
        api_key = None
        model = args.model
        temperature = args.temperature
        max_tokens = args.max_tokens

    cfg = ga.resolve_config(A())
    ok = 0
    for q in cands:
        if process_one(q, cfg, force=args.force):
            ok += 1
    print(f"完成：{ok}/{len(cands)}")


if __name__ == "__main__":
    main()
