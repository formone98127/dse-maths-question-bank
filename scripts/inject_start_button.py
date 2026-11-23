#!/usr/bin/env python3
"""喺每個數學卷目錄頁加「▶ 開始做題（第 1 題）」掣，跳去 reader 深連結。

原因：刪走 .htaccess 嗰條「卷頁 301 → reader」規則後，卷頁要自己提供入口，
保住原本「一撳即做題」嘅 UX（同時保留卷頁畀 SEO 爬）。

用法：python3 scripts/inject_start_button.py [--write]（冪等）
"""
from __future__ import annotations
import re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATH = os.path.join(ROOT, "docs", "math")
MARK = "start-cta"


def main():
    write = "--write" in sys.argv
    changed = 0
    for f in sorted(glob.glob(os.path.join(MATH, "*", "*", "index.html"))):
        rel = os.path.relpath(f, MATH).split(os.sep)  # [year, paper, index.html]
        if len(rel) != 3:
            continue
        year, paper = rel[0], rel[1]
        if not (year.isdigit() and paper.startswith("paper-")):
            continue
        pm = re.search(r"paper-([12])", paper)
        if not pm:
            continue
        p = pm.group(1)
        href = f"/#{year}P{p}Q1"
        html = open(f, encoding="utf-8").read()
        if MARK in html:
            continue
        btn = (
            f'<p class="{MARK}"><a href="{href}" '
            f'style="display:inline-flex;gap:8px;align-items:center;background:#0a84ff;color:#fff;'
            f'font-weight:700;text-decoration:none;padding:10px 18px;border-radius:999px;font-size:15px">'
            f'▶ 開始做題（第 1 題）</a></p>'
        )
        # 插喺 <main...> 之後
        m = re.search(r"<main[^>]*>", html)
        if not m:
            continue
        new = html[: m.end()] + "\n" + btn + html[m.end():]
        if new != html:
            changed += 1
            if write:
                open(f, "w", encoding="utf-8").write(new)
    print(f"changed={changed} write={write}")


if __name__ == "__main__":
    main()
