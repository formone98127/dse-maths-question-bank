#!/usr/bin/env python3
"""喺數學「卷目錄頁」加逐題靜態連結（SEO 內鏈）。

問題：docs/math/<year>/<paper>/ 嘅「題目索引」原本只連去閱讀器 hash
（/?subject=…#YYYYPnQm），Google 唔會當連去獨立 URL，所以 448 個靜態題目頁
（/questions/...）幾乎只靠 sitemap 被發現 → 收錄慢。

做法：對每個「非英文」卷頁，解析 #YYYYPnQm，若對應靜態頁存在就喺該 <li> 補一條
<a class="q-static" href="/questions/math/<y>/paper-<p>/q<q>/">題解</a>。
跳過 -en 卷（避免中文卷連到英文題目頁的語言錯配）；靜態頁未存在就唔加（免死鏈）。
冪等：檔案已含 q-static 就跳過。

用法：python3 scripts/inject_paper_q_links.py [--write]
"""
from __future__ import annotations
import re, os, glob, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATH = os.path.join(ROOT, "docs", "math")
QS = os.path.join(ROOT, "docs", "questions", "math")

LI_RE = re.compile(r'(<li><a href="[^"]*#(\d{4})P(\d)Q(\d+)">.*?</a>)(</li>)')
QSTATIC = 'q-static'

# 只連去「已 commit（已部署）」嘅靜態題目頁，避免連去未入 git／未部署嘅頁變死鏈
_TRACKED = None


def _tracked():
    global _TRACKED
    if _TRACKED is None:
        out = subprocess.run(["git", "-C", ROOT, "ls-files", "docs/questions"],
                             capture_output=True, text=True).stdout
        _TRACKED = {os.path.join(ROOT, p) for p in out.splitlines() if p}
    return _TRACKED


def static_exists(y, p, q):
    return os.path.join(QS, y, f"paper-{p}", f"q{q}", "index.html") in _tracked()


def main():
    write = "--write" in sys.argv
    changed = scanned = 0
    for f in sorted(glob.glob(os.path.join(MATH, "*", "*", "index.html"))):
        if f.endswith(f"-en{os.sep}index.html"):
            continue
        html = open(f, encoding="utf-8").read()
        if QSTATIC in html:
            continue
        scanned += 1

        def repl(m):
            whole, y, p, q, close = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            if not static_exists(y, p, q):
                return m.group(0)
            href = f"/questions/math/{y}/paper-{p}/q{q}/"
            return whole + f' · <a class="{QSTATIC}" href="{href}">題解</a>' + close

        new = LI_RE.sub(repl, html)
        if new != html:
            changed += 1
            if write:
                open(f, "w", encoding="utf-8").write(new)
    print(f"scanned={scanned} changed={changed} write={write}")


if __name__ == "__main__":
    main()
