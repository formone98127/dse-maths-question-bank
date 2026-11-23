# -*- coding: utf-8 -*-
"""Validate analysis JSON skills hooks against docs/skills/math_skill_book.json."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "docs" / "skills" / "math_skill_book.json"
DEFAULT_ROOT = ROOT / "docs" / "analysis" / "math"


def load_book(path: Path = BOOK_PATH):
    book = json.loads(path.read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in book["topics"]}
    kps, formulas = {}, {}
    for t in book["topics"]:
        for k in t["knowledge_points"]:
            kps[k["id"]] = k
        for f in t["formulas"]:
            formulas[f["id"]] = f
    abilities = {a["id"]: a for a in book["abilities"]}
    return book, (topics, kps, formulas, abilities)


def wrong_options(doc: dict) -> set[str]:
    oa = (doc.get("analysis") or {}).get("options_analysis") or {}
    return {k for k, v in oa.items() if isinstance(v, dict) and not v.get("is_correct")}


def validate_skills(skills, idx, wrong: set[str]) -> list[str]:
    topics, kps, formulas, abilities = idx
    errs = []
    if not isinstance(skills, dict):
        return ["skills 不是物件"]
    if skills.get("topic_id") not in topics:
        errs.append(f"未知 topic_id {skills.get('topic_id')!r}")
    for kid in skills.get("knowledge_point_ids") or []:
        if kid not in kps:
            errs.append(f"未知 knowledge_point_id {kid!r}")
    for fid in skills.get("formula_ids") or []:
        if fid not in formulas:
            errs.append(f"未知 formula_id {fid!r}")
    for aid in skills.get("ability_ids") or []:
        if aid not in abilities:
            errs.append(f"未知 ability_id {aid!r}")
    faults = skills.get("option_faults")
    if faults is None:
        faults = {}
    if not isinstance(faults, dict):
        errs.append("option_faults 須為物件")
        return errs
    for opt in faults:
        if wrong and opt not in wrong:
            errs.append(f"option_faults 含非錯選項 {opt}")
    for opt in wrong:
        if opt not in faults:
            errs.append(f"錯選項 {opt} 缺 option_faults")
            continue
        f = faults[opt]
        kid, fid, aid = f.get("knowledge_point_id"), f.get("formula_id"), f.get("ability_id")
        if aid not in abilities:
            errs.append(f"{opt} 未知 ability_id {aid!r}")
        if kid is None and fid is None:
            errs.append(f"{opt} 須有 knowledge_point_id 或 formula_id")
        if kid is not None and kid not in kps:
            errs.append(f"{opt} 未知 knowledge_point_id {kid!r}")
        if fid is not None and fid not in formulas:
            errs.append(f"{opt} 未知 formula_id {fid!r}")
    # long-question step_faults (optional)
    for step, f in (skills.get("step_faults") or {}).items():
        if not isinstance(f, dict):
            errs.append(f"step_faults.{step} 不是物件")
            continue
        aid = f.get("ability_id")
        if aid not in abilities:
            errs.append(f"step {step} 未知 ability_id {aid!r}")
        kid, fid = f.get("knowledge_point_id"), f.get("formula_id")
        if kid is None and fid is None:
            errs.append(f"step {step} 須有 knowledge_point_id 或 formula_id")
        if kid is not None and kid not in kps:
            errs.append(f"step {step} 未知 knowledge_point_id {kid!r}")
        if fid is not None and fid not in formulas:
            errs.append(f"step {step} 未知 formula_id {fid!r}")
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_ROOT, help="analysis 目錄或單一 json")
    ap.add_argument("--require-skills", action="store_true", help="沒有 skills 亦當錯誤")
    args = ap.parse_args()
    if not BOOK_PATH.is_file():
        print(f"缺技能冊: {BOOK_PATH}", file=sys.stderr)
        sys.exit(2)
    _, idx = load_book()
    target = args.path
    files = [target] if target.is_file() else sorted(target.rglob("q*.json"))
    ok = bad = skip = 0
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        skills = doc.get("skills")
        if not skills:
            if args.require_skills:
                print(f"FAIL {path.relative_to(ROOT)}: 缺 skills")
                bad += 1
            else:
                skip += 1
            continue
        errs = validate_skills(skills, idx, wrong_options(doc))
        if errs:
            print(f"FAIL {path.relative_to(ROOT)}:")
            for e in errs:
                print(f"  - {e}")
            bad += 1
        else:
            ok += 1
    print(f"ok={ok} fail={bad} skip_no_skills={skip}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
