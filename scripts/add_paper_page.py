#!/usr/bin/env python3
"""Create one paper page under /math/<year>/<slug>/ and list it on the year page.

Existing year pages are edited in place (one `paper-row` inserted, year nav
untouched) instead of being regenerated, so hand-tuned topic counts on the older
years survive.

  python scripts/add_paper_page.py 2015 paper-1 卷一 中文 19 --write
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATH = ROOT / "docs" / "math"
TPL = MATH / "2023" / "paper-2-en" / "index.html"


def paper_html(year: int, slug: str, cat: str, lang: str, nq: int) -> str:
    h = TPL.read_text(encoding="utf-8")
    h = h.replace("/math/2023/paper-2-en/", f"/math/{year}/{slug}/")
    h = h.replace("/math/2023/paper-2-en", f"/math/{year}/{slug}")
    h = h.replace("/math/2023/", f"/math/{year}/")
    h = h.replace("數學 2023 卷二（英文）", f"數學 {year} {cat}（{lang}）")
    h = h.replace("2023 年卷二（英文）", f"{year} 年{cat}（{lang}）")
    h = h.replace("2023 卷二", f"{year} {cat}")
    pcode = "P1" if "1" in slug else "P2"
    h = h.replace("#2023P2Q", f"#{year}{pcode}Q").replace("year=2023", f"year={year}")
    h = h.replace("year%3D2023", f"year%3D{year}")
    h = h.replace("卷二（英文）", f"{cat}（{lang}）")
    h = re.sub(r'class="on">2023</a>', f'class="on">{year}</a>', h)
    items = "\n".join(
        f'    <li><a href="https://hkdse.exampaper.cloud/?subject=%E6%95%B8%E5%AD%B8#{year}{("P1" if "1" in slug else "P2")}Q{i}">'
        f'<span class="q-meta">數學 {year} {cat} Q{i}</span> — 第 {i} 題</a></li>' for i in range(1, nq + 1))
    h = re.sub(r'(<ul class="q-index">)(.*?)(\s*</ul>)', lambda m: m.group(1) + "\n" + items + "\n  " + m.group(3),
               h, count=1, flags=re.S)
    h = re.sub(r"<h2>題目索引（\d+ 題）</h2>", f"<h2>題目索引（{nq} 題）</h2>", h)
    h = re.sub(r"資料庫有 \d+ 題索引", f"資料庫有 {nq} 題索引", h)
    return h


def row(year: int, slug: str, cat: str, lang: str, nq: int) -> str:
    return f'''    <article class="paper-row">
      <a class="paper-main" href="/math/{year}/{slug}/" title="開啟卷頁">
        <div class="paper-year">{year}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">數學</span>
            <span class="tag cat">{cat}</span>
            <span class="tag lang">{lang}</span>
          </div>
          <div class="paper-title">文憑試 DSE 數學 {year} · {cat}（{lang}）</div>
          <div class="paper-sub">數學（必修部分） · {nq} 題索引</div>
        </div>
      </a>
    </article>
'''


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int)
    ap.add_argument("slug")
    ap.add_argument("cat")
    ap.add_argument("lang")
    ap.add_argument("nq", type=int)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    ydir = MATH / str(a.year)
    ypage = ydir / "index.html"
    if not ypage.exists():
        raise SystemExit(f"missing {ypage}; generate the year page first")
    h = ypage.read_text(encoding="utf-8")
    if f"/math/{a.year}/{a.slug}/" not in h:
        block = row(a.year, a.slug, a.cat, a.lang, a.nq)
        h = re.sub(r'(<div class="paper-list">)', r"\1\n" + block.replace("\\", "\\\\"), h, count=1)
        print(f"row added to {ypage.relative_to(ROOT)}")
        if a.write:
            ypage.write_text(h, encoding="utf-8")
    else:
        print("row already present")
    target = ydir / a.slug / "index.html"
    print(f"{'write' if a.write else 'dry'} {target.relative_to(ROOT)} ({len(paper_html(a.year, a.slug, a.cat, a.lang, a.nq))} bytes)")
    if a.write:
        (ydir / a.slug).mkdir(parents=True, exist_ok=True)
        target.write_text(paper_html(a.year, a.slug, a.cat, a.lang, a.nq), encoding="utf-8")


if __name__ == "__main__":
    main()
