#!/usr/bin/env python3
"""把靜態題目頁（/questions/**）的「考生答對率」由純文字改成雙色 bar。

規則（Kin 2026-11-19 定案）：答對率一律用雙色 bar —— 左段綠＝答對比例(pct%)，
右段紅＝答錯比例(100-pct%)。現有題、以後新題都一樣。與閱讀器 pctGauge 一致
（綠 #33a852、紅 #e5533d、寬 90px、高 8px、圓角）。

用法：
  python3 scripts/inject_pct_bar.py            # dry run，印會改幾多檔
  python3 scripts/inject_pct_bar.py --write    # 實際寫入
冪等：已含 pct-bar 的頁會 skip，可重複執行。
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "docs" / "questions"

# 統一 markup：<p class="pct">歷年考生答對率：<strong>N%</strong>（官方統計）</p>
PCT_RE = re.compile(
    r'<p class="pct">歷年考生答對率：<strong>(\d+)%</strong>（官方統計）</p>'
)

BAR_CSS = (
    ".pct-bar{display:inline-flex;width:90px;height:8px;border-radius:999px;"
    "overflow:hidden;vertical-align:middle;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}"
    ".pct-bar i{display:block;height:100%}"
    ".pct-bar .g{background:#33a852}.pct-bar .r{background:#e5533d}"
)


def bar_html(pct: int) -> str:
    p = max(0, min(100, pct))
    return (
        f'<p class="pct">歷年考生答對率 '
        f'<span class="pct-bar" role="img" aria-label="考生答對率 {p}%">'
        f'<i class="g" style="width:{p}%"></i>'
        f'<i class="r" style="width:{100 - p}%"></i>'
        f'</span> '
        f'<strong>{p}%</strong>（官方統計）</p>'
    )


def ensure_css(html: str) -> str:
    if ".pct-bar{" in html:
        return html
    # 插在 .pct{...} 規則後面；否則插在 </style> 前面
    m = re.search(r"\.pct\{[^}]*\}\n", html)
    if m:
        return html[: m.end()] + BAR_CSS + "\n" + html[m.end():]
    return html.replace("</style>", BAR_CSS + "\n</style>", 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    changed = 0
    scanned = 0
    for f in sorted(QDIR.rglob("index.html")):
        html = f.read_text(encoding="utf-8")
        if "答對率" not in html:
            continue
        scanned += 1
        if "pct-bar" in html:      # 已處理
            continue
        m = PCT_RE.search(html)
        if not m:
            continue               # 非標準格式，跳過（人手跟進）
        pct = int(m.group(1))
        new = html[: m.start()] + bar_html(pct) + html[m.end():]
        new = ensure_css(new)
        changed += 1
        if args.write:
            f.write_text(new, encoding="utf-8")

    print(f"scanned={scanned} changed={changed} write={args.write}")


if __name__ == "__main__":
    main()
