# -*- coding: utf-8 -*-
from __future__ import annotations

import html
import json
from typing import Iterable

BANK = "https://hkdse.exampaper.cloud"
GA = "G-LTB27V0RGW"
CSS_VER = "20261115b"
TUTOR = "https://dsemaths.canonlessons.com/"

AF_INDEX = "https://www.hkeaa.edu.hk/tc/hkdse/assessment/assessment_framework/"
CAT_A = "https://www.hkeaa.edu.hk/tc/hkdse/assessment/subject_information/category_a_subjects/"
CAT_B = "https://www.hkeaa.edu.hk/tc/hkdse/assessment/subject_information/category_b_subjects/"
CAT_C = "https://www.hkeaa.edu.hk/tc/HKDSE/assessment/subject_information/category_c_subjects/index.html"
PUB = "https://www.hkeaa.edu.hk/tc/resources/publications/list_of_publications/hkdse_erqp_pub/"
EDB_TEXT = "https://www.edb.gov.hk/tc/curriculum-development/kla/chi-edu/nss-lang/settext-text.html"
EDB_SET_INDEX = "https://www.edb.gov.hk/tc/curriculum-development/kla/chi-edu/nss-lang/settext-index.html"
SI = "https://www.hkeaa.edu.hk/DocLibrary/HKDSE/Subject_Information"

# Verified 2027 assessment-framework PDFs (HTTP 200, actual %PDF).
# Chinese Literature and Literature in English: no stable direct PDF path found; use AF_INDEX.
AF_PDF = {
    "chi": f"{SI}/chi_lang/2027hkdse-c-clang.pdf",
    "eng": f"{SI}/eng_lang/2027hkdse-e-elang.pdf",
    "math": f"{SI}/math/2027hkdse-c-math.pdf",
    "m1": f"{SI}/math/2027hkdse-c-math.pdf",
    "m2": f"{SI}/math/2027hkdse-c-math.pdf",
    "csd": f"{SI}/cs/2027hkdse-c-cs.pdf",
    "phys": f"{SI}/phy/2027hkdse-c-phy.pdf",
    "bio": f"{SI}/bio/2027hkdse-c-bio.pdf",
    "chem": f"{SI}/chem/2027hkdse-c-chem.pdf",
    "econ": f"{SI}/econ/2027hkdse-c-econ.pdf",
    "bafs": f"{SI}/bafs/2027hkdse-c-bafs.pdf",
    "ict": f"{SI}/ict/2027hkdse-c-ict.pdf",
    "geog": f"{SI}/geog/2027hkdse-c-geog.pdf",
    "hist": f"{SI}/hist/2027hkdse-c-hist.pdf",
    "chist": f"{SI}/chist/2027hkdse-c-chist.pdf",
    "ths": f"{SI}/ths/2027hkdse-c-ths.pdf",
    "hmsc": f"{SI}/hmsc/2027hkdse-c-hmsc.pdf",
    "dat": f"{SI}/dat/2027hkdse-c-dat.pdf",
    "tl": f"{SI}/tnl/2027hkdse-c-tl.pdf",
    "music": f"{SI}/music/2027hkdse-c-music.pdf",
    "va": f"{SI}/va/2027hkdse-c-va.pdf",
    "pe": f"{SI}/pe/2027hkdse-c-pe.pdf",
    "ers": f"{SI}/ers/2027hkdse-c-ers.pdf",
}

PAGE_CSS = """
/* Page-scoped resource layout — do not add to the shared stylesheet. */
.res-sec { margin: 8px 0 24px; }
.res-sec > h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 10px;
  color: var(--ink);
}
.res-sec > h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 16px 0 8px;
  color: var(--ink);
}
.res-sec p, .res-sec li {
  font-size: 15px;
  line-height: 1.7;
  color: var(--ink-2);
}
.res-sec p { margin: 0 0 10px; }
.res-sec ul, .res-sec ol { margin: 0 0 10px; padding-left: 1.25em; }
.res-sec li { margin: 0 0 6px; }
.res-sec a { color: var(--acc-ink); }
.res-card {
  margin: 0 0 12px;
  border: 1px solid var(--hair);
  border-radius: var(--radius);
  background: var(--card);
  padding: 14px 16px 16px;
}
.res-card h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--ink);
}
.res-card p:last-child, .res-card ul:last-child, .res-card ol:last-child { margin-bottom: 0; }
.res-toc {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 8px 0 0;
}
.res-toc a {
  display: inline-block;
  border: 1px solid var(--hair);
  border-radius: var(--radius);
  background: var(--card);
  color: var(--acc-ink);
  text-decoration: none;
  font-size: 14px;
  padding: 7px 10px;
}
.res-toc a:hover { background: var(--card-hi); }
.res-note {
  border: 1px solid var(--hair);
  border-radius: var(--radius);
  background: var(--card);
  padding: 12px 14px;
  margin: 0 0 16px;
  color: var(--ink-2);
  font-size: 14px;
  line-height: 1.65;
}
.res-note strong { color: var(--ink); }
.res-grid {
  display: grid;
  gap: 8px;
}
.res-grid a.res-item {
  display: block;
  border: 1px solid var(--hair);
  border-radius: var(--radius);
  background: var(--card);
  padding: 14px 16px;
  text-decoration: none;
  color: inherit;
}
.res-grid a.res-item:hover { background: var(--card-hi); }
.res-grid a.res-item .kicker {
  margin: 0 0 4px;
  font-size: 12px;
  font-weight: 600;
  color: var(--acc-ink);
}
.res-grid a.res-item h3 {
  margin: 0 0 6px;
  font-size: 16px;
  font-weight: 700;
  color: var(--ink);
}
.res-grid a.res-item p {
  margin: 0;
  font-size: 14px;
  line-height: 1.65;
  color: var(--ink-2);
}
.res-table-wrap { overflow-x: auto; margin: 0 0 12px; }
.res-sec table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.res-sec th, .res-sec td {
  border-bottom: 1px solid var(--hair);
  text-align: left;
  vertical-align: top;
  padding: 8px 8px 8px 0;
  color: var(--ink-2);
}
.res-sec th { color: var(--ink); font-weight: 700; }
.res-kicker { margin: 0 0 6px; font-size: 13px; font-weight: 600; color: var(--acc-ink); }
"""


def _ld(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def official_links_html(slug: str, extra: Iterable[tuple[str, str]] | None = None) -> str:
    items = [
        ("考評局評核大綱一覽（2026–2029）", AF_INDEX),
        ("甲類高中科目資訊", CAT_A),
        ("考評局刊物（考試報告及試題專輯）", PUB),
    ]
    pdf = AF_PDF.get(slug)
    if pdf:
        items.insert(0, ("2027 年評核大綱（PDF）", pdf))
    if extra:
        items.extend(extra)
    lis = "\n".join(
        f'<li><a href="{html.escape(url, quote=True)}" rel="noopener">{html.escape(label)}</a></li>'
        for label, url in items
    )
    return f"""<section class="res-sec" aria-label="官方資料">
  <h2>官方資料（請以考評局／教育局為準）</h2>
  <p>以下係官方評核同刊物頁面。本站只提供原創溫習筆記同答題框架，唔會轉載官方試題、評卷參考、考試報告或指定篇章全文。</p>
  <ul>
    {lis}
  </ul>
</section>"""


def render_page(
    *,
    path: str,
    title: str,
    description: str,
    crumbs: list[tuple[str, str | None]],
    h1: str,
    tagline: str,
    body: str,
    schema_type: str = "Article",
    keywords: str | None = None,
    nav_html: str = "",
    cta_html: str = "",
    footer_back: tuple[str, str] = ("/hub/", "返回 DSE Hub 主頁"),
) -> str:
    """path like /chi/prescribed-texts/ (leading and trailing slash)."""
    assert path.startswith("/") and path.endswith("/"), path
    canon = BANK + path
    kw = keywords or "DSE, 香港中學文憑, 溫習資源, 課題筆記, 答題框架, 免費"
    crumb_ld = []
    crumb_html_parts = []
    for i, (name, url) in enumerate(crumbs, 1):
        if url:
            crumb_ld.append({
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": BANK + url if url.startswith("/") else url,
            })
            crumb_html_parts.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(name)}</a>')
        else:
            crumb_ld.append({
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": canon,
            })
            crumb_html_parts.append(f"<span>{html.escape(name)}</span>")
    crumb_html = '\n      <span aria-hidden="true">／</span>\n      '.join(crumb_html_parts)

    page_obj: dict = {
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": canon,
        "inLanguage": "zh-Hant-HK",
        "isPartOf": {"@id": f"{BANK}/#website"},
        "author": {"@type": "Organization", "name": "DSE Hub"},
    }
    if schema_type == "CollectionPage":
        page_obj["about"] = {"@type": "Thing", "name": h1}

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": crumb_ld,
            },
            page_obj,
        ],
    }

    etitle = html.escape(title)
    edesc = html.escape(description)
    ekw = html.escape(kw)
    eh1 = html.escape(h1)
    etag = html.escape(tagline)

    nav_block = nav_html or (
        '<nav class="strand-nav" aria-label="本站導覽">\n'
        '        <a href="/hub/">題庫主頁</a>\n'
        '        <a href="/resources/">全科溫習資源</a>\n'
        "        </nav>"
    )
    cta_block = cta_html or (
        '<p class="page-cta"><a href="/resources/">全科溫習資源</a> · '
        '<a href="/hub/">返回 DSE Hub 主頁</a></p>'
    )
    back_href, back_label = footer_back

    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{etitle}</title>
<meta name="description" content="{edesc}">
<meta name="keywords" content="{ekw}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
<meta name="author" content="DSE Hub">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DSE Hub">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{etitle}">
<meta property="og:description" content="{edesc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BANK}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DSE Hub 香港中學文憑歷屆試題資料庫">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{etitle}">
<meta name="twitter:description" content="{edesc}">
<meta name="twitter:image" content="{BANK}/og-image.png">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="DSE Hub">
<meta name="application-name" content="DSE Hub">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/hub/style.css?v={CSS_VER}">
<style>
{PAGE_CSS}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA}');
</script>
<script type="application/ld+json">
{_ld(ld)}
</script>
</head>
<body class="subj-page">
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <nav class="crumb" aria-label="麵包屑">
      {crumb_html}
      </nav>
    <p class="brand">DSE Hub</p>
    <h1>{eh1}</h1>
    <p class="tagline">{etag}</p>
        {nav_block}
    {cta_block}
  </div>
</header>
<main class="subj-main">
{body}
</main>
<footer><a href="{html.escape(back_href, quote=True)}">{html.escape(back_label)}</a> · <a href="/hub/">DSE Hub 主頁</a> · 相關：<a href="{TUTOR}" rel="noopener">免費 DSE 數學視覺教程</a></footer>
</body>
</html>
"""


def card_link(href: str, kicker: str, title: str, desc: str) -> str:
    return (
        f'<a class="res-item" href="{html.escape(href, quote=True)}">'
        f'<p class="kicker">{html.escape(kicker)}</p>'
        f"<h3>{html.escape(title)}</h3>"
        f"<p>{html.escape(desc)}</p></a>"
    )


def toc(items: Iterable[tuple[str, str]]) -> str:
    links = "\n".join(
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        for href, label in items
    )
    return f'<nav class="res-toc" aria-label="本頁章節">{links}</nav>'


def note(text_html: str) -> str:
    return f'<p class="res-note">{text_html}</p>'


COPYRIGHT_NOTE = (
    '<p class="res-note"><strong>版權同使用說明：</strong>'
    "呢啲筆記用自己嘅措辭整理公開課程常見概念同應試方法，方便溫習。"
    "正式考試請同時核對考評局當年評核大綱，以及試卷提供嘅公式或資料。"
    "本站唔會轉載官方試題、評卷參考、考試報告、課程指引原文，亦唔會刊登指定文言篇章全文。"
    "需要原文或官方樣本時，請行下面官方連結。</p>"
)
