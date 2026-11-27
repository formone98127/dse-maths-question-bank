#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate full-paper MC practice pages with Quiz structured data.

For each MC paper that has per-question pages (docs/math/<year>/paper-2*/q*/),
extract question text, options and answers from each q page's QAPage JSON-LD
and build a one-page practice view with a Quiz node (Google Practice Problems).

Generates:
  - docs/math/2012/paper-2/quiz/index.html
  - docs/math/2012/paper-2-en/quiz/index.html
Adds a "全卷操練" link on each paper index page and registers the quiz URLs
in docs/sitemap.xml.

Usage:  python scripts/build_quiz_pages.py
Idempotent: safe to re-run.
"""
import json
import re
from pathlib import Path

from build_meta import ver

VER = ver()

ROOT = Path(__file__).resolve().parent.parent
MATH_DIR = ROOT / "docs" / "math"
SITEMAP = ROOT / "docs" / "sitemap.xml"
SITE = "https://hkdse.exampaper.cloud"
TODAY = "2026-11-18"
GTAG_ID = "G-LTB27V0RGW"

KEYWORDS = ("DSE, 香港中學文憑, 歷屆試題, past paper, DSE 數學, 數學卷二, "
            "MC, 選擇題, 答案, 操卷, 免費題庫")

# (year, folder, lang_label, title, desc, quiz_nav_label)
PAPERS = [
    {
        "year": "2012",
        "folder": "paper-2",
        "lang": "zh-Hant-HK",
        "label": "卷二（中文）",
        "title": "2012 DSE 數學卷二全卷操練｜45 題 MC 連答案｜DSE 數學題庫",
        "desc": ("一頁操晒 2012 DSE 數學卷二全部 45 題 MC：題目、選項同答案逐題列出，"
                 "附逐題深度分析連結，適合計時操卷同考後對卷。"),
        "nav": "全卷操練（45 題連答案）",
    },
    {
        "year": "2012",
        "folder": "paper-2-en",
        "lang": "zh-Hant-HK",
        "label": "卷二（英文）",
        "title": "2012 DSE Maths Paper 2 操練｜45 MC 連答案｜DSE 數學題庫",
        "desc": ("2012 DSE Maths Paper 2 full practice: all 45 MC questions with answers "
                 "on one page, linked to per-question deep analysis. Timed mock ready."),
        "nav": "全卷操練（45 題連答案）",
    },
]

LD_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def extract_questions(paper_dir):
    """Return list of dicts {n, stem, options, answer} from q*/index.html pages."""
    out = []
    warnings = []
    qdirs = sorted(
        (d for d in paper_dir.iterdir()
         if d.is_dir() and re.fullmatch(r"q\d+", d.name)),
        key=lambda d: int(d.name[1:]),
    )
    for d in qdirs:
        n = int(d.name[1:])
        html = (d / "index.html").read_text(encoding="utf-8")
        m = LD_RE.search(html)
        if not m:
            warnings.append(f"q{n}: no ld+json block")
            continue
        try:
            graph = json.loads(m.group(1))["@graph"]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            warnings.append(f"q{n}: ld+json parse failed: {e}")
            continue
        qa = next((x for x in graph if x.get("@type") == "QAPage"), None)
        if not qa or not qa.get("mainEntity"):
            warnings.append(f"q{n}: no QAPage mainEntity")
            continue
        q = qa["mainEntity"]
        text = q.get("text", "")
        acc = q.get("acceptedAnswer", {}).get("text", "")
        sugg = [a.get("text", "") for a in q.get("suggestedAnswer", [])]

        stem = text.split(" - A.")[0].strip() if " - A." in text else text.strip()
        answer = re.sub(r"^([A-D])\.\s*", r"\1. ", acc.split("。速解策略")[0].rstrip("。").strip())
        options = [re.sub(r"^([A-D])\.\s*", r"\1. ", s.strip()) for s in sugg]

        if not stem or not answer or len(options) < 2:
            warnings.append(f"q{n}: incomplete data (stem={bool(stem)}, ans={bool(answer)}, opts={len(options)})")

        ans_letter = re.match(r"^([A-D])\.", answer)
        wrong = [o for o in options
                 if not (ans_letter and o.startswith(ans_letter.group(1) + "."))]
        out.append({"n": n, "stem": stem, "options": options,
                    "answer": answer, "wrong": wrong})
    return out, warnings


def render_quiz_page(meta, questions):
    year = meta["year"]
    folder = meta["folder"]
    url = f"{SITE}/math/{year}/{folder}/quiz/"
    paper_url = f"{SITE}/math/{year}/{folder}/"
    q_url_base = f"/math/{year}/{folder}/q"

    blocks = []
    has_part = []
    for q in questions:
        n = q["n"]
        stem_html = q["stem"]
        opts_html = "\n".join(f"<li>{o}</li>" for o in q["options"])
        ans_html = q["answer"]
        blocks.append(
            f'<section class="quiz-q" id="q{n}">\n'
            f'  <h2>第 {n} 題<a class="quiz-qlink" href="{q_url_base}{n}/">逐題深度分析 ↗</a></h2>\n'
            f'  <div class="q-embed"><p>{stem_html}</p>\n<ul>\n{opts_html}\n</ul></div>\n'
            f'  <p class="quiz-ans">答案：{ans_html}</p>\n'
            f'</section>'
        )
        has_part.append({
            "@type": "Question",
            "position": n,
            "eduQuestionType": "Multiple choice",
            "name": f"{year} DSE 數學卷二 第 {n} 題",
            "text": q["stem"],
            "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
            "suggestedAnswer": [{"@type": "Answer", "text": w} for w in q["wrong"]],
        })

    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "DSE 數學題庫", "item": SITE + "/hub/"},
                {"@type": "ListItem", "position": 2, "name": "數學", "item": SITE + "/math/"},
                {"@type": "ListItem", "position": 3, "name": year, "item": f"{SITE}/math/{year}/"},
                {"@type": "ListItem", "position": 4, "name": meta["label"], "item": paper_url},
                {"@type": "ListItem", "position": 5, "name": "全卷操練", "item": url},
            ],
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "name": meta["title"],
            "description": meta["desc"],
            "url": url,
            "inLanguage": meta["lang"],
            "isPartOf": {"@id": SITE + "/hub/#website"},
            "about": {"@id": url + "#quiz"},
        },
        {
            "@type": "Quiz",
            "@id": url + "#quiz",
            "name": meta["title"],
            "description": meta["desc"],
            "url": url,
            "inLanguage": meta["lang"],
            "isAccessibleForFree": True,
            "dateModified": TODAY,
            "educationalAlignment": {
                "@type": "AlignmentObject",
                "alignmentType": "educationalSubject",
                "targetName": "HKDSE Mathematics Compulsory Part",
                "targetUrl": "https://www.hkeaa.edu.hk/",
            },
            "about": {
                "@type": "LearningResource",
                "name": "DSE 數學（必修部分）",
                "teaches": "Mathematics",
                "educationalLevel": "Secondary 4–6（HKDSE）",
                "inLanguage": meta["lang"],
            },
            "hasPart": has_part,
        },
    ]
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                        ensure_ascii=False, indent=2)

    blocks_html = "\n".join(blocks)
    return f"""<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
<meta name="author" content="DSE 數學題庫">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DSE 數學題庫">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DSE 數學題庫 香港中學文憑歷屆試題資料庫">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta['title']}">
<meta name="twitter:description" content="{meta['desc']}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
<script>MathJax = {{tex: {{inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['$$','$$']]}}}};</script>
<script src="/mathjax/tex-chtml.js" async></script>
<style>
.quiz-q {{ background:var(--card); border:1px solid var(--hair); border-radius:var(--radius); padding:16px; margin:0 0 14px; }}
.quiz-q h2 {{ font-size:1.05rem; margin-bottom:10px; }}
.quiz-q .q-embed {{ margin:0; }}
.quiz-ans {{ color:var(--acc-ink); font-weight:600; margin-top:12px; }}
.quiz-qlink {{ font-size:.8rem; font-weight:400; color:var(--ink-3); margin-left:10px; text-decoration:none; }}
.quiz-qlink:hover {{ color:var(--acc-ink); }}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GTAG_ID}');
</script>
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body class="subj-page">
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <nav class="crumb" aria-label="麵包屑">
      <a href="/hub/">DSE 數學題庫</a><span aria-hidden="true">／</span><a href="/math/">數學</a><span aria-hidden="true">／</span><a href="/math/{year}/">{year}</a><span aria-hidden="true">／</span><a href="/math/{year}/{folder}/">{meta['label']}</a><span aria-hidden="true">／</span><span>全卷操練</span>
    </nav>
    <p class="brand">DSE 數學題庫</p>
    <h1>{meta['title']}</h1>
    <p class="tagline">一頁操晒 {year} DSE 數學{meta['label']}全部 {len(questions)} 題 MC，題目、選項同答案逐題列出，每題附「逐題深度分析」連結。適合計時模擬操卷同考後對卷。</p>
    <nav class="strand-nav" aria-label="同年試卷">
      <a href="/math/{year}/paper-1/">卷一（中文）</a>
      <a href="/math/{year}/paper-2/">卷二（中文）</a>
      <a href="/math/{year}/paper-2-en/">卷二（英文）</a>
      <a href="/math/{year}/{folder}/quiz/" class="on">全卷操練</a>
    </nav>
  </div>
</header>
<main class="subj-main">
{blocks_html}
</main>
<footer><a href="/math/{year}/{folder}/">返回 {year} {meta['label']}</a> · <a href="/math/">DSE 數學 Past Paper</a> · <a href="/hub/">DSE 數學題庫 主頁</a> · 站內只放索引、連結同課題標籤，只顯示資料庫已有內容</footer>
</body>
</html>
"""


def patch_paper_index(meta):
    idx = MATH_DIR / meta["year"] / meta["folder"] / "index.html"
    html = idx.read_text(encoding="utf-8")
    on_link = f'<a href="/math/{meta["year"]}/{meta["folder"]}/" class="on">{meta["label"]}</a>'
    new_link = f'<a href="/math/{meta["year"]}/{meta["folder"]}/quiz/">全卷操練（45 題連答案）</a>'
    if meta["nav"] not in html and "quiz/" not in html:
        html = html.replace(on_link, on_link + "\n        " + new_link)
        idx.write_text(html, encoding="utf-8")
        return True
    return False


def patch_sitemap(metas):
    xml = SITEMAP.read_text(encoding="utf-8")
    added = []
    for meta in metas:
        loc = f"{SITE}/math/{meta['year']}/{meta['folder']}/quiz/"
        if loc + "</loc>" in xml:
            continue
        added.append(loc)
        block = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>")
        xml = xml.replace("</urlset>", block + "\n</urlset>")
    SITEMAP.write_text(xml, encoding="utf-8")
    return added


def main():
    for meta in PAPERS:
        paper_dir = MATH_DIR / meta["year"] / meta["folder"]
        if not paper_dir.is_dir():
            print(f"skip {meta['folder']}: no folder")
            continue
        questions, warnings = extract_questions(paper_dir)
        if not questions:
            print(f"skip {meta['folder']}: no questions extracted")
            continue
        out = paper_dir / "quiz" / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(render_quiz_page(meta, questions), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({len(questions)} questions)")
        for w in warnings:
            print(f"  WARN {w}")
        linked = patch_paper_index(meta)
        print(f"  paper index link added: {linked}")
    added = patch_sitemap(PAPERS)
    print(f"sitemap: {len(added)} new quiz URLs added")


if __name__ == "__main__":
    main()
