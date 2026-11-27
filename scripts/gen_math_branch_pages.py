#!/usr/bin/env python3
"""生成 /math/、/math/core/、/math/m1/、/math/m2/ 四個分支入口頁。

設計原則（Kin 2026-11-26 定案 A）：
- 只做入口頁，唔搬任何已收錄 URL（/hub/math/**、/m1/**、/m2/** 全部不動）。
- 版面共用 docs/m1/index.html 同一套 header（hero + crumb + brand + tagline + strand-nav），
  唔可以另建一套設計。
- 年份／題數一律由檔案系統同 docs/data.js 即場計，唔准手寫。

用法：
    python3 scripts/gen_math_branch_pages.py           # dry run
    python3 scripts/gen_math_branch_pages.py --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BASE = "https://hkdse.exampaper.cloud"

HEAD = """<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="DSE Hub">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DSE Hub">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/og-image.png">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/hub/style.css?v=202611191400">
<style>
.year-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(132px,1fr)); gap:10px; margin:12px 0 4px; }}
.year-grid a {{ display:block; padding:12px 10px; border:1px solid var(--line); border-radius:12px; background:var(--card); color:var(--ink); text-decoration:none; font-weight:700; text-align:center; }}
.year-grid a span {{ display:block; font-size:12px; font-weight:500; color:var(--muted); margin-top:4px; }}
.unit-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:14px; margin:14px 0; }}
.unit-grid a {{ display:block; padding:16px; border:1px solid var(--line); border-radius:14px; background:var(--card); color:var(--ink); text-decoration:none; }}
.unit-grid a h3 {{ margin:0 0 6px; font-size:17px; }}
.unit-grid a p {{ margin:0; font-size:14px; color:var(--muted); }}
</style>
</head>
"""

HERO = """<body class="subj-page">
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <nav class="crumb" aria-label="麵包屑">
      <a href="/hub/">DSE Hub</a>
      <span aria-hidden="true">／</span>
      {crumbs}
    </nav>
    <a class="brand" href="/hub/" title="返 DSE Hub 主頁">DSE Hub</a>
    <h1>{h1}</h1>
    <p class="tagline">{tagline}</p>
    <nav class="strand-nav" aria-label="數學各單元">
      <a href="/math/">數學總覽</a>
      <a href="/math/core/">必修單元</a>
      <a href="/math/m1/">延伸單元一</a>
      <a href="/math/m2/">延伸單元二</a>
    </nav>
  </div>
</header>
<main class="subj-main">
"""

FOOT = """</main>
<footer><a href="/hub/">返回 DSE Hub 主頁</a> · 相關：<a href="/hub/math/">數學研究站</a> · <a href="https://dsemaths.canonlessons.com/" rel="noopener">免費 DSE 數學視覺教程</a></footer>
</body>
</html>
"""


def year_dirs(path: Path) -> list[str]:
    if not path.is_dir():
        return []
    out = [p.name for p in path.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}", p.name)]
    return sorted(out)


def topic_names() -> dict[str, str]:
    f = DOCS / "topics" / "_mapping.json"
    if not f.exists():
        return {}
    m = json.loads(f.read_text(encoding="utf-8"))
    return {k: (v.get("name") or k) for k, v in m.items() if isinstance(v, dict)}


def jsonld(name, url, desc):
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": name,
        "url": url,
        "description": desc,
        "inLanguage": "zh-Hant-HK",
        "isPartOf": {"@type": "WebSite", "name": "DSE Hub", "url": BASE + "/"},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": BASE + "/hub/"},
                {"@type": "ListItem", "position": 2, "name": "數學", "item": BASE + "/math/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url},
            ],
        },
    }
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(data, ensure_ascii=False, indent=None)


def build_math_index() -> str:
    url = BASE + "/math/"
    title = "DSE 數學科總覽：必修單元、M1、M2 歷屆試題｜DSE Hub"
    desc = "DSE 數學科三個部分的入口：必修單元（Core）、延伸單元一（M1）、延伸單元二（M2）。逐年逐題電子題庫，免費查閱。"
    core_years = year_dirs(DOCS / "hub" / "math")
    m1_years = year_dirs(DOCS / "m1")
    m2_years = year_dirs(DOCS / "m2")
    units = [
        ("/math/core/", "數學必修單元（Core）", "Paper 1 同 Paper 2，%d 個年度，另設樣本試卷同練習卷。" % len([y for y in core_years if y.isdigit()])),
        ("/math/m1/", "數學延伸單元一（M1）", "微積分與統計，%d 個年度。" % len(m1_years)),
        ("/math/m2/", "數學延伸單元二（M2）", "代數與微積分，%d 個年度。" % len(m2_years)),
    ]
    body = HERO.format(
        crumbs='<span>/math/</span>',
        h1="DSE 數學科：三個單元",
        tagline="必修單元（Core）、延伸單元一（M1）、延伸單元二（M2）各自有獨立試卷同題目庫。先揀你要溫嘅單元。",
    )
    body += '<section class="res-sec">\n  <h2>揀單元</h2>\n  <div class="unit-grid">\n'
    for u, n, d in units:
        body += '<a href="%s"><h3>%s</h3><p>%s</p></a>\n' % (u, n, d)
    body += "  </div>\n</section>\n"
    body += (
        '<section class="res-sec">\n  <h2>單元關係</h2>\n'
        "<p>必修部分係所有考生的基礎；延伸單元一以微積分同統計為主，延伸單元二以代數同微積分為主。"
        "考生只可以報考其中一個延伸單元，而且必須同時報考必修部分。所以三個單元分開收錄，各自有逐年試題頁。</p>\n"
        "</section>\n"
    )
    body += FOOT
    return HEAD.format(title=title, desc=desc, url=url, base=BASE) + jsonld("DSE 數學科", url, desc) + body


def build_core() -> str:
    url = BASE + "/math/core/"
    title = "DSE 數學必修單元（Core）歷屆試題索引｜DSE Hub"
    desc = "DSE 數學必修部分（Core）逐年試卷同逐題電子版索引：Paper 1、Paper 2、樣本試卷同練習卷，另附課題分類。"
    years = [y for y in year_dirs(DOCS / "hub" / "math") if y.isdigit()]
    others = [y for y in year_dirs(DOCS / "hub" / "math") if not y.isdigit()]
    slugs = {p.name for p in (DOCS / "hub" / "math").iterdir() if p.is_dir()}
    names = topic_names()
    topics = sorted([(names.get(s, s), s) for s in slugs if s in names], key=lambda t: t[0])
    body = HERO.format(
        crumbs='<a href="/math/">數學</a> <span aria-hidden="true">／</span> <span>/math/core/</span>',
        h1="DSE 數學必修單元（Core）歷屆試題",
        tagline="必修部分每屆設 Paper 1（長題目）同 Paper 2（多項選擇）。以下逐年入題目庫，逐題連評卷參考。",
    )
    body += '<section class="res-sec">\n  <h2>逐年試卷（%d 個年度）</h2>\n  <div class="year-grid">\n' % len(years)
    for y in years:
        body += '<a href="/hub/math/%s/paper-1-en/">%s<span>Paper 1 · Paper 2</span></a>\n' % (y, y)
    for y in others:
        label = {"PP": "樣本試卷", "SP": "練習卷"}.get(y, y)
        body += '<a href="/hub/math/%s/">%s<span>%s</span></a>\n' % (y, y, label)
    body += "  </div>\n</section>\n"
    if topics:
        body += '<section class="res-sec">\n  <h2>按課題（%d 個）</h2>\n  <p>' % len(topics)
        body += " · ".join('<a href="/hub/math/%s/">%s</a>' % (s, n) for n, s in topics)
        body += "</p>\n</section>\n"
    body += (
        '<section class="res-sec">\n  <h2>必修部分範圍</h2>\n'
        "<p>必修部分分三大範疇：數與代數、度量圖形與空間、數據處理。Paper 1 以長題目考推導同解釋，"
        "Paper 2 以多項選擇考速度同概念辨析。實際題型同分數分佈以考評局當年評核大綱為準。</p>\n</section>\n"
    )
    body += (
        '<section class="res-sec" aria-label="相關資源">\n  <h2>相關</h2>\n  <ul>\n'
        '    <li><a href="/hub/math/formulas/">必修公式表</a></li>\n'
        '    <li><a href="/math/m1/">數學延伸單元一（M1）</a></li>\n'
        '    <li><a href="/math/m2/">數學延伸單元二（M2）</a></li>\n'
        '    <li><a href="/topics/">全部課題索引</a></li>\n'
        "  </ul>\n</section>\n"
    )
    body += FOOT
    return HEAD.format(title=title, desc=desc, url=url, base=BASE) + jsonld("DSE 數學必修單元", url, desc) + body


def build_unit(unit: str) -> str:
    if unit == "m1":
        url = BASE + "/math/m1/"
        title = "DSE 數學延伸單元一（M1）歷屆試題索引｜DSE Hub"
        desc = "DSE 數學延伸單元一（微積分與統計）逐年試卷同逐題電子版索引，另附單元公式表同課題筆記。"
        h1 = "DSE 數學延伸單元一（M1）歷屆試題"
        tagline = "單元一考微積分同統計。以下逐年入題目庫，逐題連評卷參考。"
        src = DOCS / "m1"
        extra = '<li><a href="/m1/formulas/">單元一公式溫習表</a></li>\n    <li><a href="/m1/notes/">單元一課題筆記</a></li>\n'
        scope = (
            "<p>單元一以微積分（極限、導數、積分）同統計（概率分布、二項及常態分布、置信區間）為主，"
            "全部屬傳統長題。考生必須同時報考必修部分，並且只可以選一個延伸單元。</p>\n"
        )
    else:
        url = BASE + "/math/m2/"
        title = "DSE 數學延伸單元二（M2）歷屆試題索引｜DSE Hub"
        desc = "DSE 數學延伸單元二（代數與微積分）逐年試卷同逐題電子版索引，另附單元公式表同課題筆記。"
        h1 = "DSE 數學延伸單元二（M2）歷屆試題"
        tagline = "單元二考代數同微積分。以下逐年入題目庫，逐題連評卷參考。"
        src = DOCS / "m2"
        extra = '<li><a href="/m2/formulas/">單元二公式溫習表</a></li>\n    <li><a href="/m2/notes/">單元二課題筆記</a></li>\n'
        scope = (
            "<p>單元二以矩陣、向量、三角學、代數方程同微積分為主，計法較重推導同嚴謹表達。"
            "考生必須同時報考必修部分，並且只可以選一個延伸單元。</p>\n"
        )
    years = year_dirs(src)
    body = HERO.format(
        crumbs='<a href="/math/">數學</a> <span aria-hidden="true">／</span> <span>/math/%s/</span>' % unit,
        h1=h1,
        tagline=tagline,
    )
    body += '<section class="res-sec">\n  <h2>逐年試卷（%d 個年度）</h2>\n  <div class="year-grid">\n' % len(years)
    for y in years:
        body += '<a href="/%s/%s/paper-1-en/">%s<span>%s</span></a>\n' % (unit, y, y, "Paper 1")
    body += "  </div>\n</section>\n"
    body += '<section class="res-sec">\n  <h2>考核範圍</h2>\n  ' + scope + "</section>\n"
    body += '<section class="res-sec" aria-label="相關資源">\n  <h2>相關</h2>\n  <ul>\n    ' + extra + (
        '<li><a href="/math/core/">數學必修單元（Core）</a></li>\n'
        '    <li><a href="/math/%s/">數學%s</a></li>\n' % (("m2", "延伸單元二（M2）") if unit == "m1" else ("m1", "延伸單元一（M1）"))
    ) + "  </ul>\n</section>\n"
    body += FOOT
    name = "DSE 數學延伸單元一" if unit == "m1" else "DSE 數學延伸單元二"
    return HEAD.format(title=title, desc=desc, url=url, base=BASE) + jsonld(name, url, desc) + body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    pages = {
        DOCS / "math" / "index.html": build_math_index(),
        DOCS / "math" / "core" / "index.html": build_core(),
        DOCS / "math" / "m1" / "index.html": build_unit("m1"),
        DOCS / "math" / "m2" / "index.html": build_unit("m2"),
    }
    for p, html in pages.items():
        print("%-40s %6d bytes" % (p.relative_to(ROOT), len(html)))
        if a.write:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(html, encoding="utf-8")
    if not a.write:
        print("\n(dry run — 加 --write 才寫入)")


if __name__ == "__main__":
    main()
