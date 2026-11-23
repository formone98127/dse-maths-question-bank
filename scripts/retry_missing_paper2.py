# -*- coding: utf-8 -*-
"""Retry missing Paper 2 analysis questions, then rebuild maps."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
MISSING = {
    2014: [1, 14, 16, 27],
    2015: [26, 44],
    2016: [36],
    2017: [26, 33],
    2018: [15, 27],
    2019: [16],
    2020: [4, 32, 38],
    2021: [28],
    2023: [4, 5, 27],
    2024: [5],
    2025: [7, 8, 21],
}


def run(cmd):
    print(">>>", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    # Full 2022 English-only paper
    run([
        PY, "generate_analysis.py", "--subject", "數學", "--year", "2022",
        "--paper", "Paper 2", "--all-langs", "--max-tokens", "4096",
    ])
    for year, qnos in MISSING.items():
        cmd = [
            PY, "generate_analysis.py", "--subject", "數學", "--year", str(year),
            "--paper", "Paper 2", "--max-tokens", "4096",
        ]
        for q in qnos:
            cmd += ["--question", str(q)]
        run(cmd)
    run([PY, "scripts/build_all_math_skill_maps.py"])
    print("RETRY DONE", flush=True)


if __name__ == "__main__":
    main()
