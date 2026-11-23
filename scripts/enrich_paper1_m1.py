# -*- coding: utf-8 -*-
"""Enrich all math Paper 1 + Paper 1M analyses, rebuild maps after each year."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YEARS = [str(y) for y in range(2012, 2026)] + ["PP", "SP"]
PAPERS = ["Paper 1", "Paper 1M"]


def run(cmd: list[str]) -> int:
    print("\n>>>", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="")
    ap.add_argument("--papers", default="Paper 1,Paper 1M")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-maps", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=4096)
    args = ap.parse_args()
    years = [y.strip() for y in args.years.split(",") if y.strip()] or YEARS
    papers = [p.strip() for p in args.papers.split(",") if p.strip()] or PAPERS
    py = sys.executable

    for year in years:
        for paper in papers:
            if year == "SP" and paper == "Paper 1M":
                continue  # no SP M1 in bank typically
            cmd = [
                py,
                "scripts/generate_long_analysis.py",
                "--year",
                year,
                "--paper",
                paper,
                "--max-tokens",
                str(args.max_tokens),
            ]
            if args.force:
                cmd.append("--force")
            # English-only fallback for papers with 0 Chinese
            code = run(cmd)
            if code != 0:
                print(f"retry with --all-langs {year} {paper}", flush=True)
                run(cmd + ["--all-langs"])
        if not args.skip_maps:
            run([py, "scripts/build_all_math_skill_maps.py"])
    print("ALL LONG DONE", flush=True)


if __name__ == "__main__":
    main()
