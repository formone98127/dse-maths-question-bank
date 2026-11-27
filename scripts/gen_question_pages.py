#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate per-question static SEO pages at /questions/math/<year>/paper-<N>/q<qno>/.

Reverse-engineered from commit 648d811 (the 2019–2025 pages) so 2012–2018 can be
produced with the SAME structure (title / meta description / self-canonical /
JSON-LD QAPage + BreadcrumbList / H1 / breadcrumb / zh+en question / MS image /
考評報告 / 相關課題 / prev-next nav).

Data sources:
  - docs/data.js             (window.QB)  -> zh/en question text+html, tags, report
  - docs/topics/_mapping.json              -> tag name -> topic slug
  - docs/ms/<year>P<n>/Q<NN>.png           -> marking scheme image (checked on disk)

Usage:
  python3 scripts/gen_question_pages.py --year 2012 --paper 1            # dry run
  python3 scripts/gen_question_pages.py --year 2012 --paper 1 --write    # write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://hkdse.exampaper.cloud"
GTAG_ID = "G-LTB27V0RGW"

CSS = (
    ":root{--fg:#111;--mut:#555;--line:#ddd;--bg:#fafafa;--acc:#0b5}\n"
    "*{box-sizing:border-box}\n"
    "body{margin:0;font:16px/1.7 -apple-system,BlinkMacSystemFont,\"Segoe UI\",\"Noto Sans TC\",sans-serif;color:var(--fg);background:var(--bg)}\n"
    "header.site{background:#fff;border-bottom:1px solid var(--line)}\n"
    ".wrap{max-width:860px;margin:0 auto;padding:0 16px}\n"
    ".bc{font-size:14px;color:var(--mut);padding:12px 0}\n"
    ".bc a{color:var(--mut)}\n"
    "main{padding:8px 0 40px}\n"
    "h1{font-size:24px;line-height:1.35;margin:8px 0 16px}\n"
    "h2{font-size:17px;margin:0 0 10px;color:#111}\n"
    ".card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px;margin:0 0 14px}\n"
    ".qh p{margin:.4em 0}\n"
    ".qh li{margin:.2em 0}\n"
    ".ans .big{font-size:34px;font-weight:700;color:var(--acc);margin:4px 0}\n"
    ".pct{color:var(--mut);font-size:14px;margin:6px 0 0}\n"
    ".ms{overflow-x:auto}\n"
    ".ms table{border-collapse:collapse;width:100%;font-size:15px}\n"
    ".ms td,.ms th{border:1px solid var(--line);padding:6px 8px;vertical-align:top}\n"
    ".ms img{max-width:100%;height:auto}\n"
    ".qh img{max-width:100%;height:auto}\n"
    ".tag{display:inline-block;margin:0 8px 8px 0;padding:4px 10px;background:#eef7f1;border:1px solid #cfe8da;border-radius:999px;font-size:14px;text-decoration:none;color:#065f46}\n"
    "nav.pn{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}\n"
    "nav.pn a{padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;text-decoration:none}\n"
    "details.card summary{cursor:pointer;font-weight:600}\n"
    "footer{border-top:1px solid var(--line);color:var(--mut);font-size:13px;padding:18px 0 40px;background:#fff}\n"
    "@media(max-width:600px){h1{font-size:20px}.ans .big{font-size:28px}}"
)

MATHJAX = (
    '<script>window.MathJax = {tex: {inlineMath: [["$","$"],["\\(","\\)"]], '
    'displayMath: [["$$","$$"],["\\[","\\]"]]}, options: {enableMenu: false}};</script>\n'
    '<script defer="defer" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
)

GTAG = (
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>\n'
    '<script>\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    '  function gtag(){dataLayer.push(arguments);}\n'
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GTAG_ID}');\n"
    '</script>'
)


def strip_latex_delims(s: str) -> str:
    """去掉 $ / \\( \\) / \\[ \\] 分隔符，保留內文（供 JSON-LD 純文字）。"""
    for d in ("$", "\\(", "\\)", "\\[", "\\]"):
        s = s.replace(d, "")
    return s


def load_questions() -> dict:
    raw = (DOCS / "data.js").read_text(encoding="utf-8")
    raw = raw[raw.index("{"):raw.rindex("}") + 1]
    data = json.loads(raw)
    out = {}
    for q in data["questions"]:
        if q.get("type") != "題目":
            continue
        try:
            year = int(q["year"])
        except (ValueError, TypeError):
            continue
        paper = q.get("paper") or ""
        pn = 2 if re.search(r"2|卷二", paper) else 1
        qno = str(q.get("qno"))
        key = (year, pn, qno)
        lang = "en" if re.search(r"英文|_EN|(EN)", q.get("file") or "") else "zh"
        rec = out.setdefault(key, {})
        rec[lang] = q
    return out


def load_topic_map() -> dict:
    m = json.loads((DOCS / "topics" / "_mapping.json").read_text(encoding="utf-8"))
    rev = {}
    for slug, info in m.get("slugs", {}).items():
        rev[info.get("name", "")] = slug
    return rev


def ms_img_path(year: int, paper: int, qno: int) -> str | None:
    """回傳 docs/ms 內 MS 圖相對路徑（由 q 頁指向），無圖回 None。"""
    rel = DOCS / "ms" / f"{year}P{paper}" / f"Q{qno:02d}.png"
    if rel.exists():
        return f"../../../../../ms/{year}P{paper}/Q{qno:02d}.png"
    return None


def render_page(year: int, paper: int, qno: int, zh, en, topic_map: dict,
                n_total: int, pct=None) -> str:
    tags = zh.get("tags") or []
    first_tag = tags[0] if tags else "數學"
    slug = f"paper-{paper}"
    qurl = f"{SITE}/questions/math/{year}/{slug}/q{qno}/"
    _tail = f"｜答對率 {round(float(pct))}%" if pct is not None else ""
    title = f"{year} DSE 數學 P{paper} Q{qno} 答案＋詳解{_tail}｜DSE Hub"
    h1 = f"{year} DSE 數學 P{paper} Q{qno} 答案＋詳解{_tail}"
    desc = f"{year} Paper {paper} 第 {qno} 題（{first_tag}）長題目：官方評卷參考、題解、考評報告。"

    zh_html = zh.get("html") or f"<p>{zh.get('text', '')}</p>"
    en_html = en.get("html") if en else ""
    report = (zh.get("report") or "").strip()
    ms_img = ms_img_path(year, paper, qno)

    # JSON-LD QAPage
    qa_text = strip_latex_delims(zh.get("text") or "")
    accepted = "官方題解：官方評卷參考表格見頁內（圖片）。　考評報告：" + strip_latex_delims(report)
    qa = {
        "@context": "https://schema.org", "@type": "QAPage",
        "mainEntity": {
            "@type": "Question", "name": h1, "text": qa_text, "answerCount": 1,
            "acceptedAnswer": {"@type": "Answer", "text": accepted, "upvoteCount": 1},
        },
    }
    bc = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首頁", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "數學", "item": f"{SITE}/math/"},
            {"@type": "ListItem", "position": 3, "name": str(year), "item": f"{SITE}/math/{year}/"},
            {"@type": "ListItem", "position": 4, "name": f"Paper {paper}", "item": f"{SITE}/math/{year}/{slug}/"},
            {"@type": "ListItem", "position": 5, "name": f"第 {qno} 題", "item": qurl},
        ],
    }

    # 麵包屑（可見）
    crumb = (
        f'<nav class="bc" aria-label="麵包屑">'
        f'<a href="../../../../../index.html">首頁</a> <span>›</span> '
        f'<a href="../../../../../math/index.html">數學</a> <span>›</span> '
        f'<a href="../../../../../math/{year}/">{year}</a> <span>›</span> '
        f'<a href="../../../../../math/{year}/{slug}">Paper {paper}</a> <span>›</span> '
        f'<span aria-current="page">第 {qno} 題</span></nav>'
    )

    # 相關課題
    topic_links = ""
    for t in tags:
        sl = topic_map.get(t)
        if sl:
            topic_links += f'<a class="tag" href="../../../../../topics/{sl}/">{t}</a>'
    if not topic_links:
        topic_links = '<span class="tag" style="color:#555">（待整理）</span>'

    # 上一題 / 下一題
    nav_parts = []
    if qno > 1:
        nav_parts.append(f'<a rel="prev" href="../q{qno - 1}/">← 上一題（第 {qno - 1} 題）</a>')
    if qno < n_total:
        nav_parts.append(f'<a rel="next" href="../q{qno + 1}/">下一題（第 {qno + 1} 題）→</a>')
    nav_parts += [
        f'<a href="../../../../../math/{year}/{slug}">返回該卷目錄</a>',
        f'<a href="../../../../../index.html#{year}P{paper}Q{qno}">互動作答版</a>',
        f'<a href="../../../../../index.html#{year}P{paper}Q{qno}A">互動版（展開題解）</a>',
    ]
    nav = '<nav class="pn" aria-label="題目導覽">' + "".join(nav_parts) + '</nav>'

    # MS 區
    if ms_img:
        ms_section = f'<div class="ms"><p><img src="{ms_img}" alt="MS Q{qno}" /></p></div>'
    else:
        ms_section = '<p>評卷參考整理中。</p>'

    # 英文版
    if en_html:
        en_section = f'<details class="card" id="en"><summary>English version（英文卷題目）</summary><div class="qh">{en_html}</div></details>\n'
    else:
        en_section = ""

    # 考評報告
    if report:
        report_section = f'<section class="card" id="report"><h2>考評報告</h2><p>{report}</p></section>\n'
    else:
        report_section = ""

    page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{qurl}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{qurl}" />
<style>
{CSS}
</style>
{MATHJAX}
<script type="application/ld+json">{json.dumps(qa, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>
{GTAG}
</head>
<body>
<header class="site"><div class="wrap">{crumb}</div></header>
<main class="wrap">
<h1>{h1}</h1>

<section class="card" id="q"><h2>題目（中文卷）</h2><div class="qh">{zh_html}</div></section>
{en_section}<section class="card" id="solution"><h2>官方評卷參考（Marking Scheme）</h2>{ms_section}</section>
{report_section}<section class="card" id="topics"><h2>相關課題</h2><p>{topic_links}</p></section>
{nav}
</main>
<footer><div class="wrap">DSE Hub｜{year} 數學 Paper {paper} 第 {qno} 題　
資料來源：香港考試及評核局歷屆試題及評卷參考（非官方整理，僅供學習）</div></footer>
<noscript><div class="wrap"><p>本頁內容為靜態文字，毋須 JavaScript 亦可完整閱讀；數學式若未經 MathJax 排版，會以 LaTeX（如 $x^2$）原樣顯示。</p></div></noscript>
</body>
</html>
"""
    return page


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--paper", type=int, required=True, choices=[1, 2])
    ap.add_argument("--qno", type=int, default=None)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    questions = load_questions()
    topic_map = load_topic_map()
    qnos = sorted(int(k[2]) for k in questions if k[0] == a.year and k[1] == a.paper)
    n_total = max(qnos) if qnos else 0
    if a.qno:
        qnos = [a.qno]

    written = []
    for qno in qnos:
        key = (a.year, a.paper, str(qno))
        rec = questions.get(key)
        if not rec:
            print(f"skip q{qno}: 無題目 record")
            continue
        zh = rec.get("zh")
        if not zh:
            print(f"skip q{qno}: 無中文題目")
            continue
        en = rec.get("en")
        html = render_page(a.year, a.paper, qno, zh, en, topic_map, n_total, pct=rec.get("answer_pct") or zh.get("answer_pct"))
        outdir = DOCS / "questions" / "math" / str(a.year) / f"paper-{a.paper}" / f"q{qno}"
        outfile = outdir / "index.html"
        if a.write:
            outdir.mkdir(parents=True, exist_ok=True)
            outfile.write_text(html, encoding="utf-8")
        written.append((str(outfile.relative_to(ROOT)), len(html.encode("utf-8"))))

    print(f"year={a.year} paper={a.paper} n={len(written)} write={a.write}")
    for path, nbytes in written:
        print(f"  {path}  {nbytes}B")


if __name__ == "__main__":
    main()
