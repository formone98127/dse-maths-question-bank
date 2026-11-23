# -*- coding: utf-8 -*-
"""Enrich math Paper 2 analyses (LLM + skills) year by year, then rebuild maps.

Usage:
  python scripts/enrich_paper2_analyses.py
  python scripts/enrich_paper2_analyses.py --years 2013,2014
  python scripts/enrich_paper2_analyses.py --years 2013 --range 1-5
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YEARS = list(range(2013, 2026))  # 2012 already enriched


def run(cmd: list[str]) -> int:
    print("\n>>>", " ".join(cmd), flush=True)
    p = subprocess.run(cmd, cwd=ROOT)
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="", help="comma years, e.g. 2013,2014")
    ap.add_argument("--range", dest="qrange", default="", help="optional qno range for every year")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--model", default="")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--skip-maps", action="store_true")
    args = ap.parse_args()

    years = (
        [int(x.strip()) for x in args.years.split(",") if x.strip()]
        if args.years.strip()
        else DEFAULT_YEARS
    )

    py = sys.executable
    for year in years:
        cmd = [
            py,
            "generate_analysis.py",
            "--subject",
            "數學",
            "--year",
            str(year),
            "--paper",
            "Paper 2",
            "--max-tokens",
            str(args.max_tokens),
        ]
        if args.qrange:
            cmd += ["--range", args.qrange]
        if args.force:
            cmd.append("--force")
        if args.model:
            cmd += ["--model", args.model]
        code = run(cmd)
        if code != 0:
            print(f"year {year} exited {code}; continuing", flush=True)
        if not args.skip_maps:
            run([py, "scripts/build_all_math_skill_maps.py"])

    print("ALL YEARS DONE", flush=True)


if __name__ == "__main__":
    main()
