#!/usr/bin/env python3
"""Generate the missing maths year pages (2024, 2025) from the 2023 templates
and refresh the year navigation on every maths page.

Templates are copied from an existing year so the layout, SEO tags and styling
stay identical; only the year, paper list and question index change.

  python scripts/gen_math_pages.py            # dry run
  python scripts/gen_math_pages.py --write
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATH = ROOT / "docs" / "math"

# year -> [(slug, 卷別 label, 語言 label, 題數)]
YEARS = {
    2024: [("paper-2-en", "卷二", "英文", 45), ("paper-2-zh", "卷二", "中文", 45)],
    2025: [("paper-2-en", "卷二", "英文", 45)],
}
NAV_YEARS = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012]


def year_nav(active: int | None) -> str:
    rows = []
    for y in NAV_YEARS:
        cls = ' class="on"' if y == active else ""
        rows.append(f'        <a href="/math/{y}/"{cls}>{y}</a>')
    return "\n".join(rows)


def replace_year_nav(html: str, active: int | None) -> str:
    pat = re.compile(r'(<nav class="strand-nav" aria-label="年份">)(.*?)(</nav>)', re.S)
    return pat.sub(lambda m: m.group(1) + "\n" + year_nav(active) + "\n        " + m.group(3), html, count=1)


def retitle(html: str, old: str, new: str) -> str:
    return html.replace(old, new)


def build_year_page(year: int, tpl: str) -> str:
    base_year = 2023
    h = replace_year_nav(tpl, year)
    h = h.replace(f"/math/{base_year}/", f"/math/{year}/")
    h = h.replace(f"數學 {base_year}", f"數學 {year}")
    h = h.replace(f"{base_year} 年", f"{year} 年")
    h = h.replace(f"{base_year} 至", f"{year} 至")
    h = h.replace(f"{base_year}）", f"{year}）")
    h = re.sub(r'lang=year&amp;year=\d{4}', f"lang=year&amp;year={year}", h)
    h = re.sub(r'class="on">\d{4}</a>', f'class="on">{year}</a>', h)

    rows = []
    for slug, cat, lang, nq in YEARS[year]:
        rows.append(f"""    <article class="paper-row">
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
    </article>""")
    h = re.sub(r'(<div class="paper-list">)(.*?)(\s*</div>\s*</section>)',
               lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n  " + m.group(3), h, count=1, flags=re.S)
    nq = YEARS[year][0][3]
    h = re.sub(r'<h2>\d{4} 年各卷</h2>', f"<h2>{year} 年各卷</h2>", h)
    # 課題計數來自舊年份，新頁唔可以照抄 → 改成連去課題總覽
    h = re.sub(r'(<section class="strand-index".*?</section>)',
               '<section class="strand-index" aria-label="本年相關課題">\n  <h2>本年相關課題</h2>\n'
               '  <nav class="strand-nav" aria-label="本年課題">\n'
               f'        <a href="/math/">返回數學科目頁，按課題篩選</a>\n'
               '  </nav>\n</section>', h, flags=re.S, count=1)
    h = re.sub(r'資料庫有 \d+ 卷、\d+ 題索引', f"資料庫有 {len(YEARS[year])} 卷、{nq} 題索引", h)
    return h


def build_paper_page(year: int, slug: str, cat: str, lang: str, nq: int, tpl: str) -> str:
    h = replace_year_nav(tpl, year)
    h = h.replace("/math/2023/paper-2-en/", f"/math/{year}/{slug}/")
    h = h.replace("/math/2023/paper-2-en", f"/math/{year}/{slug}")
    h = h.replace("/math/2023/", f"/math/{year}/")
    h = h.replace("數學 2023 卷二（英文）", f"數學 {year} {cat}（{lang}）")
    h = h.replace("2023 年卷二（英文）", f"{year} 年{cat}（{lang}）")
    h = h.replace("2023 卷二", f"{year} {cat}")
    h = h.replace("#2023P2Q", f"#{year}P2Q").replace("year=2023", f"year={year}")
    h = re.sub(r'卷二（英文）', f'{cat}（{lang}）', h)
    h = re.sub(r'class="on">2023</a>', f'class="on">{year}</a>', h)
    # 題目索引重寫
    items = "\n".join(
        f'    <li><a href="https://hkdse.exampaper.cloud/?subject=%E6%95%B8%E5%AD%B8#{year}P2Q{i}">'
        f'<span class="q-meta">數學 {year} {cat} Q{i}</span> — 第 {i} 題</a></li>'
        for i in range(1, nq + 1))
    h = re.sub(r'(<ul class="q-index">)(.*?)(\s*</ul>)',
               lambda m: m.group(1) + "\n" + items + "\n  " + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'<h2>題目索引（\d+ 題）</h2>', f"<h2>題目索引（{nq} 題）</h2>", h)
    return h


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    year_tpl = (MATH / "2023" / "index.html").read_text(encoding="utf-8")
    paper_tpl = (MATH / "2023" / "paper-2-en" / "index.html").read_text(encoding="utf-8")

    for y, papers in YEARS.items():
        ydir = MATH / str(y)
        page = build_year_page(y, year_tpl)
        print(f"{'write' if a.write else 'dry'} /math/{y}/index.html ({len(page)} bytes)")
        if a.write:
            ydir.mkdir(parents=True, exist_ok=True)
            (ydir / "index.html").write_text(page, encoding="utf-8")
        for slug, cat, lang, nq in papers:
            pp = build_paper_page(y, slug, cat, lang, nq, paper_tpl)
            print(f"{'write' if a.write else 'dry'} /math/{y}/{slug}/index.html ({len(pp)} bytes)")
            if a.write:
                (ydir / slug).mkdir(parents=True, exist_ok=True)
                (ydir / slug / "index.html").write_text(pp, encoding="utf-8")

    # 所有現存年份頁同卷頁：更新年份導覽（加 2024/2025）
    for f in sorted(MATH.glob("*/index.html")) + sorted(MATH.glob("*/*/index.html")):
        rel = f.relative_to(MATH)
        m = re.match(r"(\d{4})", str(rel))
        if not m:
            continue
        html = f.read_text(encoding="utf-8")
        if 'href="/math/2025/"' in html:
            continue
        new = replace_year_nav(html, int(m.group(1)))
        print(f"nav+ {rel}")
        if a.write:
            f.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
