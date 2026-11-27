#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate DSE Hub Marking Scheme landing pages.

Builds:
  - docs/ms/index.html          (MS hub page)
  - docs/ms/<folder>/index.html (one page per MS image folder, e.g. 2012P1, 2012P1zh)

then registers every new URL in docs/sitemap.xml and bumps lastmod for /hub/ and /math/.

Usage:  python scripts/build_ms_pages.py
Idempotent: safe to re-run after adding new MS folders or images.
"""
import json
import re
from pathlib import Path

from build_meta import ver

VER = ver()

ROOT = Path(__file__).resolve().parent.parent
MS_DIR = ROOT / "docs" / "ms"
SITEMAP = ROOT / "docs" / "sitemap.xml"
SITE = "https://hkdse.exampaper.cloud"
TODAY = "2026-11-18"
GTAG_ID = "G-LTB27V0RGW"

KEYWORDS = ("DSE, 香港中學文憑, 歷屆試題, past paper, DSE 數學, "
            "marking scheme, 評卷參考, 評分準則, 對卷, 免費題庫")


def collect():
    """Return [{folder, year, zh, imgs}] sorted by folder name."""
    out = []
    for d in sorted(p for p in MS_DIR.iterdir() if p.is_dir()):
        m = re.fullmatch(r"(20\d{2})P1(zh)?", d.name)
        if not m:
            continue
        out.append({
            "folder": d.name,
            "year": m.group(1),
            "zh": bool(m.group(2)),
            "imgs": sorted(x.name for x in d.glob("Q*.png")),
        })
    return out


def labels(p):
    n = len(p["imgs"])
    if p["zh"]:
        return {
            "lang": "zh-Hant-HK", "hl": "zh-Hant-HK",
            "h1": f"{p['year']} DSE 數學卷一 Marking Scheme（中文版）",
            "title": f"{p['year']} DSE 數學卷一 Marking Scheme（中文版）｜評卷參考下載｜DSE Hub",
            "desc": (f"免費查閱 {p['year']} DSE 數學卷一 Marking Scheme（中文版）評卷參考，"
                     f"共 {n} 題逐題列出評分準則，適合考後對卷、學寫步驟攞分位。"),
            "crumb": f"{p['year']} 卷一（中文版）",
            "nav": f"{p['year']} 中",
        }
    return {
        "lang": "en-HK", "hl": "en-HK",
        "h1": f"{p['year']} DSE Maths Paper 1 Marking Scheme",
        "title": f"{p['year']} DSE Maths Paper 1 Marking Scheme｜評卷參考下載｜DSE Hub",
        "desc": (f"免費查閱 {p['year']} DSE Maths Paper 1 Marking Scheme 評卷參考，"
                 f"共 {n} 題逐題列出評分準則，適合考後對卷、學寫步驟攞分位。"),
        "crumb": f"{p['year']} Paper 1 (EN)",
        "nav": f"{p['year']} 英",
    }


def hreflang_block(p, all_pages):
    hl = "zh-Hant-HK" if p["zh"] else "en-HK"
    url = f"{SITE}/ms/{p['folder']}/"
    lines = [f'<link rel="alternate" hreflang="{hl}" href="{url}">']
    for q in all_pages:
        if q["year"] == p["year"] and q["zh"] != p["zh"]:
            qhl = "zh-Hant-HK" if q["zh"] else "en-HK"
            lines.append(f'<link rel="alternate" hreflang="{qhl}" href="{SITE}/ms/{q["folder"]}/">')
    en = next((q for q in all_pages if q["year"] == p["year"] and not q["zh"]), p)
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/ms/{en["folder"]}/">')
    return "\n".join(lines)


def year_nav(p, all_pages):
    links = []
    for q in all_pages:
        cls = ' class="on"' if q["folder"] == p["folder"] else ""
        lang = "中" if q["zh"] else "英"
        links.append(f'<a href="/ms/{q["folder"]}/"{cls}>{q["year"]} {lang}</a>')
    return "\n".join(links)


def figures(p):
    out = []
    for img in p["imgs"]:
        num = re.sub(r"^0+", "", img.replace("Q", "").replace(".png", ""))
        lang = "（中文版）" if p["zh"] else ""
        alt = f"{p['year']} DSE 數學卷一 Marking Scheme{lang} 第 {num} 題評卷參考"
        out.append(
            f'<figure class="ms-fig"><a href="{img}" target="_blank" rel="noopener">'
            f'<img src="{img}" alt="{alt}" loading="lazy"></a>'
            f'<figcaption class="ms-cap">第 {num} 題</figcaption></figure>'
        )
    return "\n".join(out)


def page_jsonld(p, lab, url):
    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": SITE + "/hub/"},
                {"@type": "ListItem", "position": 2, "name": "數學", "item": SITE + "/math/"},
                {"@type": "ListItem", "position": 3, "name": "Marking Scheme", "item": SITE + "/ms/"},
                {"@type": "ListItem", "position": 4, "name": lab["crumb"], "item": url},
            ],
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "name": lab["title"],
            "description": lab["desc"],
            "url": url,
            "inLanguage": lab["hl"],
            "isPartOf": {"@id": SITE + "/hub/#website"},
            "about": {"@type": "Thing", "name": "DSE 數學（必修部分）Marking Scheme 評卷參考"},
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)


def render_page(p, all_pages):
    lab = labels(p)
    url = f"{SITE}/ms/{p['folder']}/"
    tagline = (f'{lab["desc"]} 配合 <a href="/math/{p["year"]}/">{p["year"]} DSE 數學試題</a>'
               f" 一齊用，考後對卷效率更高。")
    return f"""<!DOCTYPE html>
<html lang="{lab['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{lab['title']}</title>
<meta name="description" content="{lab['desc']}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
<meta name="author" content="DSE Hub">
<link rel="canonical" href="{url}">
{hreflang_block(p, all_pages)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="DSE Hub">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{lab['title']}">
<meta property="og:description" content="{lab['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DSE Hub 香港中學文憑歷屆試題資料庫">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{lab['title']}">
<meta name="twitter:description" content="{lab['desc']}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
<style>
.ms-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }}
.ms-fig {{ background:var(--card); border:1px solid var(--hair); border-radius:var(--radius); overflow:hidden; }}
.ms-fig a {{ display:block; text-decoration:none; }}
.ms-fig img {{ display:block; width:100%; height:auto; background:#fff; }}
.ms-cap {{ padding:8px 12px; font-size:13px; color:var(--ink-2); }}
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
{page_jsonld(p, lab, url)}
</script>
</head>
<body class="subj-page">
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <nav class="crumb" aria-label="麵包屑">
      <a href="/hub/">DSE Hub</a><span aria-hidden="true">／</span><a href="/math/">數學</a><span aria-hidden="true">／</span><a href="/ms/">Marking Scheme</a><span aria-hidden="true">／</span><span>{lab['crumb']}</span>
    </nav>
    <p class="brand">DSE Hub</p>
    <h1>{lab['h1']}</h1>
    <p class="tagline">{tagline}</p>
    <nav class="strand-nav" aria-label="年份">{year_nav(p, all_pages)}</nav>
  </div>
</header>
<main class="subj-main">
  <section aria-label="逐題評卷參考">
    <div class="ms-grid">
{figures(p)}
    </div>
  </section>
</main>
<footer><a href="/hub/">DSE Hub 主頁</a> · <a href="/math/">DSE 數學 Past Paper</a> · <a href="/ms/">Marking Scheme 總覽</a> · 內容僅供學習用途，版權屬香港考試及評核局（HKEAA）</footer>
</body>
</html>
"""


def render_hub(all_pages):
    title = "DSE Maths Marking Scheme 下載｜數學評卷參考（2012–2024）｜DSE Hub"
    desc = ("免費查閱 2012–2024 DSE 數學卷一 Marking Scheme 評卷參考，中英文版齊全，"
            "逐題列出評分準則，適合考後對卷、學評分標準同操卷。")
    url = SITE + "/ms/"
    items = []
    nav = []
    for i, p in enumerate(all_pages, 1):
        lang = "中文版" if p["zh"] else "英文版"
        name = f"{p['year']} DSE 數學卷一 Marking Scheme（{lang}）"
        items.append({"@type": "ListItem", "position": i, "name": name,
                      "url": f"{SITE}/ms/{p['folder']}/"})
        nav.append(f'<a href="/ms/{p["folder"]}/">{p["year"]} {lang}</a>')
    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": SITE + "/hub/"},
                {"@type": "ListItem", "position": 2, "name": "數學", "item": SITE + "/math/"},
                {"@type": "ListItem", "position": 3, "name": "Marking Scheme", "item": url},
            ],
        },
        {
            "@type": "CollectionPage",
            "@id": url + "#page",
            "name": title,
            "description": desc,
            "url": url,
            "inLanguage": "zh-Hant-HK",
            "isPartOf": {"@id": SITE + "/hub/#website"},
            "about": {"@type": "Thing", "name": "DSE 數學（必修部分）Marking Scheme 評卷參考"},
            "mainEntity": {
                "@type": "ItemList",
                "name": "DSE 數學 Marking Scheme 評卷參考",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        },
    ]
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                        ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
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
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DSE Hub 香港中學文憑歷屆試題資料庫">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
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
      <a href="/hub/">DSE Hub</a><span aria-hidden="true">／</span><a href="/math/">數學</a><span aria-hidden="true">／</span><span>Marking Scheme</span>
    </nav>
    <p class="brand">DSE Hub</p>
    <h1>DSE 數學 Marking Scheme 評卷參考</h1>
    <p class="tagline">考後對卷必備：2012–2024 數學卷一 Marking Scheme，逐題列出評分準則。中英文版齊全（部分年份只有英文版），配合 <a href="/math/">DSE 數學試題</a> 一齊用，對卷效率最高。</p>
    <nav class="subj-nav" aria-label="科目">
      <a href="/math/">數學 Past Paper</a>
      <a href="/ms/" class="on">Marking Scheme</a>
    </nav>
  </div>
</header>
<main class="subj-main">
  <section class="strand-index" aria-label="Marking Scheme 年份">
    <h2>按年份揀 Marking Scheme</h2>
    <nav class="strand-nav" aria-label="年份">
{chr(10).join(nav)}
    </nav>
  </section>
</main>
<footer><a href="/hub/">DSE Hub 主頁</a> · <a href="/math/">DSE 數學 Past Paper</a> · 內容僅供學習用途，版權屬香港考試及評核局（HKEAA）</footer>
</body>
</html>
"""


def patch_sitemap(all_pages):
    xml = SITEMAP.read_text(encoding="utf-8")
    for loc in (SITE + "/hub/", SITE + "/math/"):
        xml = re.sub(
            r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)",
            r"\g<1>" + TODAY + r"\g<2>", xml, count=1)
    new_urls = [(SITE + "/ms/", "0.6")]
    new_urls += [(f"{SITE}/ms/{p['folder']}/", "0.5") for p in all_pages]
    added = []
    for loc, prio in new_urls:
        if loc + "</loc>" in xml:
            continue
        added.append(loc)
        block = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>")
        xml = xml.replace("</urlset>", block + "\n</urlset>")
    SITEMAP.write_text(xml, encoding="utf-8")
    return added


def main():
    pages = collect()
    if not pages:
        print("No MS folders found — aborting.")
        return
    for p in pages:
        out = MS_DIR / p["folder"] / "index.html"
        out.write_text(render_page(p, pages), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({len(p['imgs'])} images)")
    hub = MS_DIR / "index.html"
    hub.write_text(render_hub(pages), encoding="utf-8")
    print(f"wrote {hub.relative_to(ROOT)}")
    added = patch_sitemap(pages)
    print(f"sitemap: {len(added)} new URLs added, /hub/ + /math/ lastmod bumped to {TODAY}")
    print(f"total MS pages: {len(pages) + 1}")


if __name__ == "__main__":
    main()
