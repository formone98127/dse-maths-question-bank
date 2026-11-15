# -*- coding: utf-8 -*-
"""Generate resource pages, sitemap entries, hub patches, and resources.js."""
from __future__ import annotations

import re
from pathlib import Path

from .pages_electives import all_pages as elective_pages
from .pages_index_chi import all_pages as index_chi_pages
from .pages_lang_csd import all_pages as lang_csd_pages
from .pages_stem import all_pages as stem_pages

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
LASTMOD = "2026-11-15"
CACHE = "20261115r"


def all_pages():
    pages = []
    for fn in (index_chi_pages, lang_csd_pages, stem_pages, elective_pages):
        pages.extend(fn())
    # unique by path, first wins
    seen = {}
    for path, html in pages:
        if path in seen:
            raise SystemExit(f"duplicate path {path}")
        seen[path] = html
    return list(seen.items())


def write_pages(pages):
    written = []
    for path, html in pages:
        rel = path.strip("/")
        dest = DOCS / rel / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        written.append(path)
    return written


def insert_after(text, anchor, insertion, label):
    if insertion.strip() in text:
        return text  # already patched
    if text.count(anchor) != 1:
        raise SystemExit(f"patch {label}: anchor count {text.count(anchor)}")
    return text.replace(anchor, anchor + insertion, 1)


def patch_landings():
    # Math CTA + resource block
    math = DOCS / "math" / "index.html"
    t = math.read_text(encoding="utf-8")
    t = insert_after(
        t,
        ' · <a href="/math/calculator/">Casio 計算機程式</a></p>',
        ' · <a href="/math/formulas/">公式同應試技巧</a>',
        "math cta",
    )
    t = insert_after(
        t,
        '<main class="subj-main">\n',
        """<section class="strand-index" aria-label="溫習資源">
  <h2>免費溫習資源</h2>
  <nav class="strand-nav">
    <a href="/math/formulas/">公式同應試技巧</a>
    <a href="/math/calculator/">Casio 計算機程式</a>
    <a href="/m1/">數學延伸單元一</a>
    <a href="/m2/">數學延伸單元二</a>
    <a href="/resources/">全科溫習資源</a>
  </nav>
</section>
""",
        "math main",
    )
    math.write_text(t, encoding="utf-8")

    chem = DOCS / "chem" / "index.html"
    t = chem.read_text(encoding="utf-8")
    t = insert_after(
        t,
        '<p class="page-cta"><a href="/hub/?subject=chem&amp;mode=topic">按課題篩選化學題目</a> · <a href="/hub/?subject=chem&amp;mode=year">按年份睇卷</a></p>',
        ' · <a href="/chem/formulas/">公式、離子同答題框架</a>',
        "chem cta",
    )
    t = insert_after(
        t,
        '<main class="subj-main">\n',
        """<section class="strand-index" aria-label="溫習資源">
  <h2>免費溫習資源</h2>
  <nav class="strand-nav">
    <a href="/chem/formulas/">公式、離子同答題框架</a>
    <a href="/resources/">全科溫習資源</a>
  </nav>
</section>
""",
        "chem main",
    )
    chem.write_text(t, encoding="utf-8")

    econ = DOCS / "econ" / "index.html"
    t = econ.read_text(encoding="utf-8")
    t = insert_after(
        t,
        '<p class="page-cta"><a href="/hub/?subject=econ&amp;mode=topic">按課題篩選經濟題目</a> · <a href="/hub/?subject=econ&amp;mode=year">按年份睇卷</a></p>',
        ' · <a href="/econ/exam-skills/">資料回應同長題框架</a>',
        "econ cta",
    )
    t = insert_after(
        t,
        '<main class="subj-main">\n',
        """<section class="strand-index" aria-label="溫習資源">
  <h2>免費溫習資源</h2>
  <nav class="strand-nav">
    <a href="/econ/exam-skills/">資料回應同長題框架</a>
    <a href="/resources/">全科溫習資源</a>
  </nav>
</section>
""",
        "econ main",
    )
    econ.write_text(t, encoding="utf-8")

    phys = DOCS / "phys" / "index.html"
    t = phys.read_text(encoding="utf-8")
    t = insert_after(
        t,
        '<p class="page-cta"><a href="/hub/?subject=phys&amp;mode=topic">按課題篩選物理題目</a> · <a href="/hub/?subject=phys&amp;mode=year">按年份睇卷</a></p>',
        ' · <a href="/phys/formulas/">公式同課題筆記</a>',
        "phys cta",
    )
    t = insert_after(
        t,
        '<main class="subj-main">\n',
        """<section class="strand-index" aria-label="溫習資源">
  <h2>免費溫習資源</h2>
  <nav class="strand-nav">
    <a href="/phys/formulas/">公式溫習表</a>
    <a href="/phys/mechanics/">力學</a>
    <a href="/phys/heat/">熱與氣體</a>
    <a href="/phys/waves/">波動</a>
    <a href="/phys/electricity-magnetism/">電與磁</a>
    <a href="/phys/radioactivity/">放射與核能</a>
    <a href="/phys/energy/">能量</a>
    <a href="/resources/">全科溫習資源</a>
  </nav>
</section>
""",
        "phys main",
    )
    phys.write_text(t, encoding="utf-8")

    bio = DOCS / "bio" / "index.html"
    t = bio.read_text(encoding="utf-8")
    t = insert_after(
        t,
        '<p class="page-cta"><a href="/hub/?subject=bio&amp;mode=topic">按課題篩選生物題目</a> · <a href="/hub/?subject=bio&amp;mode=year">按年份睇卷</a></p>',
        ' · <a href="/bio/exam-skills/">課題筆記同應試技巧</a>',
        "bio cta",
    )
    t = insert_after(
        t,
        '<main class="subj-main">\n',
        """<section class="strand-index" aria-label="溫習資源">
  <h2>免費溫習資源</h2>
  <nav class="strand-nav">
    <a href="/bio/exam-skills/">應試技巧</a>
    <a href="/bio/cells/">細胞</a>
    <a href="/bio/genetics/">遺傳</a>
    <a href="/bio/human-physiology/">人體生理</a>
    <a href="/bio/ecology/">生態</a>
    <a href="/bio/evolution/">演化</a>
    <a href="/bio/biotechnology/">生物科技</a>
    <a href="/resources/">全科溫習資源</a>
  </nav>
</section>
""",
        "bio main",
    )
    bio.write_text(t, encoding="utf-8")


def patch_sitemap(paths):
    sm = DOCS / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    existing = set(re.findall(r"<loc>(.*?)</loc>", text))
    new_entries = []
    for path in paths:
        loc = f"https://hkdse.exampaper.cloud{path}"
        if loc in existing:
            continue
        # subject landings slightly higher priority
        parts = [p for p in path.split("/") if p]
        pri = "0.9" if len(parts) == 1 else "0.75"
        new_entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            f"    <priority>{pri}</priority>\n"
            "  </url>"
        )
    if not new_entries:
        return
    if not text.rstrip().endswith("</urlset>"):
        raise SystemExit("sitemap missing urlset close")
    text = text.rstrip()
    # keep closing tag
    if text.endswith("</urlset>"):
        text = text[: -len("</urlset>")].rstrip() + "\n" + "\n".join(new_entries) + "\n</urlset>\n"
    sm.write_text(text, encoding="utf-8")
    # verify
    locs = re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8"))
    for loc in locs:
        if loc.rstrip("/") == "https://hkdse.exampaper.cloud":
            raise SystemExit("sitemap contains domain root")
        if loc.lower().endswith(".pdf"):
            raise SystemExit(f"sitemap contains pdf {loc}")
        rel = loc.replace("https://hkdse.exampaper.cloud", "")
        dest = DOCS / rel.strip("/") / "index.html"
        if not dest.is_file():
            raise SystemExit(f"sitemap loc has no file: {loc} -> {dest}")


def patch_hub():
    p = DOCS / "hub" / "index.html"
    t = p.read_text(encoding="utf-8")

    # stylesheet token must remain 20261112r
    if 'href="/hub/style.css?v=20261112r"' not in t:
        raise SystemExit("hub stylesheet token changed unexpectedly")

    # page-scoped CSS: add related-resources styles into existing <style> block
    css_add = """
/* Topic-mode related resources — page-scoped only. */
.hub-related {
  margin: 22px 0 8px;
  padding-top: 8px;
}
.hub-related h2 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 12px;
  color: var(--ink);
}
.hub-related-grid {
  display: grid;
  gap: 8px;
}
a.hub-related-card {
  display: block;
  border: 1px solid var(--hair);
  border-radius: var(--radius);
  background: var(--card);
  padding: 14px 16px;
  text-decoration: none;
  color: inherit;
}
a.hub-related-card:hover {
  background: var(--card-hi);
}
.hub-related-kicker {
  margin: 0 0 4px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--acc-ink);
}
.hub-related-card h3 {
  margin: 0 0 6px;
  font-size: 16px;
  font-weight: 700;
  color: var(--ink);
}
.hub-related-card p {
  margin: 0;
  font-size: 14px;
  line-height: 1.65;
  color: var(--ink-2);
}
"""
    if ".hub-related {" not in t:
        if "</style>" not in t:
            raise SystemExit("hub missing style close")
        t = t.replace("</style>", css_add + "</style>", 1)

    # meta description — mention all-subject resources, keep past-paper identity
    old_desc = "免費查閱香港中學文憑試（DSE）數學、經濟、化學、生物、物理歷屆試題，按年份或課題溫習，支援中英文卷。唔使報名，即時喺 DSE Hub 開卷。"
    new_desc = "免費查閱香港中學文憑試（DSE）數學、經濟、化學、生物、物理歷屆試題，按年份或課題溫習；亦為甲類各科提供原創筆記同答題框架。唔使報名，即時喺 DSE Hub 開卷。"
    if old_desc in t:
        t = t.replace(old_desc, new_desc)

    old_title = "免費 DSE 歷屆試題｜數學經濟化學生物物理 Past Paper｜DSE Hub"
    new_title = "免費 DSE 歷屆試題同全科溫習資源｜數學經濟化學生物物理 Past Paper｜DSE Hub"
    if old_title in t:
        t = t.replace(old_title, new_title)

    # schema about + FAQ + ItemList
    faq_old = "而家有數學（必修部分）、經濟、化學、生物同物理。每科已上線嘅年份同卷別，以資料庫實際內容為準。"
    faq_new = "題庫而家有數學（必修部分）、經濟、化學、生物同物理嘅歷屆試題。另外已為現行甲類全部科目提供原創溫習資源，可到全科資源頁查閱。已上線嘅年份同卷別，以資料庫實際內容為準。"
    if faq_old in t:
        t = t.replace(faq_old, faq_new)

    faq_html_old = "而家有數學（必修部分）、經濟、化學、生物同物理。每科已上線嘅年份同卷別，以資料庫實際內容為準，科目頁會列出全部已有卷。"
    faq_html_new = "題庫而家有數學（必修部分）、經濟、化學、生物同物理嘅歷屆試題。另外已為現行甲類全部科目提供原創溫習資源，可到<a href=\"/resources/\">全科溫習資源</a>查閱。已上線嘅年份同卷別，以資料庫實際內容為準，科目頁會列出全部已有卷。"
    if faq_html_old in t:
        t = t.replace(faq_html_old, faq_html_new)

    # ItemList: keep 5 paper subjects, append resources as 6th
    old_list = '"numberOfItems": 5,'
    # only the papers list should change — be specific
    old_item5 = """        {
          "@type": "ListItem",
          "position": 5,
          "name": "物理",
          "url": "https://hkdse.exampaper.cloud/phys/"
        }
      ]
    },"""
    new_item5 = """        {
          "@type": "ListItem",
          "position": 5,
          "name": "物理",
          "url": "https://hkdse.exampaper.cloud/phys/"
        },
        {
          "@type": "ListItem",
          "position": 6,
          "name": "全科溫習資源",
          "url": "https://hkdse.exampaper.cloud/resources/"
        }
      ]
    },"""
    if old_item5 in t:
        t = t.replace(old_item5, new_item5, 1)
        t = t.replace(old_list, '"numberOfItems": 6,', 1)

    about_old = """        {
          "@type": "Thing",
          "name": "物理"
        }
      ],"""
    about_new = """        {
          "@type": "Thing",
          "name": "物理"
        },
        {
          "@type": "Thing",
          "name": "全科溫習資源"
        }
      ],"""
    if about_old in t:
        t = t.replace(about_old, about_new, 1)

    # extras cards — keep existing three, add new ones
    extras_end = """    <a class="hub-extras-card" href="/math/">
      <p class="hub-extras-kicker">溫習教程</p>
      <h3>數學課題筆記</h3>
      <p class="hub-extras-desc">按課題睇重點同常見題型，再連去相關歷屆題目。</p>
    </a>
  </div>
</section>"""
    extras_new = """    <a class="hub-extras-card" href="/math/">
      <p class="hub-extras-kicker">溫習教程</p>
      <h3>數學課題筆記</h3>
      <p class="hub-extras-desc">按課題睇重點同常見題型，再連去相關歷屆題目。</p>
    </a>
    <a class="hub-extras-card" href="/resources/">
      <p class="hub-extras-kicker">全科資源</p>
      <h3>甲類各科溫習資源</h3>
      <p class="hub-extras-desc">為現行文憑試甲類全部科目提供原創筆記、公式表同答題框架。</p>
    </a>
    <a class="hub-extras-card" href="/chi/prescribed-texts/">
      <p class="hub-extras-kicker">溫習教程</p>
      <h3>中文指定篇章指引</h3>
      <p class="hub-extras-desc">按教育局現行十二篇名單整理主題、手法同比較角度，不含全文。</p>
    </a>
    <a class="hub-extras-card" href="/eng/writing/">
      <p class="hub-extras-kicker">溫習教程</p>
      <h3>英文寫作框架</h3>
      <p class="hub-extras-desc">article、書信、建議書同演講等任務寫作步驟，配合說話討論技巧。</p>
    </a>
  </div>
</section>"""
    if extras_end in t and 'href="/resources/"' not in t.split("hub-extras")[-1][:2000] or True:
        if 'href="/resources/">' not in t or "甲類各科溫習資源" not in t:
            if extras_end not in t:
                raise SystemExit("hub extras block not found")
            t = t.replace(extras_end, extras_new, 1)

    # footer subject links
    footer_old = '科目：<a href="/math/">數學</a> · <a href="/econ/">經濟</a> · <a href="/chem/">化學</a> · <a href="/bio/">生物</a> · <a href="/phys/">物理</a><br>'
    footer_new = '科目：<a href="/math/">數學</a> · <a href="/econ/">經濟</a> · <a href="/chem/">化學</a> · <a href="/bio/">生物</a> · <a href="/phys/">物理</a> · <a href="/chi/">中國語文</a> · <a href="/eng/">英國語文</a> · <a href="/csd/">公民與社會發展</a> · <a href="/resources/">全科溫習資源</a><br>'
    if footer_old in t:
        t = t.replace(footer_old, footer_new, 1)

    # tagline
    tag_old = "即時睇題目／題解，自選按課題操卷——完全免費，真正方便用家既 Past Paper 收集平台。"
    tag_new = "即時睇題目／題解，自選按課題操卷；亦提供甲類各科原創溫習資源。完全免費，真正方便用家既 Past Paper 收集平台。"
    if tag_old in t:
        t = t.replace(tag_old, tag_new, 1)

    # scripts: add resources.js and cache-bust app.js
    old_scripts = """<script src="/data.js?v=202611150459"></script>
<script src="/hub/data.js?v=202611150459"></script>
<script src="/hub/app.js?v=20261112r"></script>"""
    new_scripts = f"""<script src="/data.js?v=202611150459"></script>
<script src="/hub/data.js?v=202611150459"></script>
<script src="/hub/resources.js?v={CACHE}"></script>
<script src="/hub/app.js?v={CACHE}"></script>"""
    if old_scripts in t:
        t = t.replace(old_scripts, new_scripts, 1)
    elif f"/hub/resources.js?v={CACHE}" not in t:
        raise SystemExit("hub script tags not found for cache-bust")

    p.write_text(t, encoding="utf-8")
    # final guards
    t2 = p.read_text(encoding="utf-8")
    if 'href="/hub/style.css?v=20261112r"' not in t2:
        raise SystemExit("hub stylesheet token lost")
    if "id=\"result\"" not in t2 and "id=result" not in t2:
        # result may be id="result"
        if 'id="result"' not in t2:
            raise SystemExit("hub #result missing")
    if "/hub/app.js?v=20261115r" not in t2:
        raise SystemExit("app.js cache token not updated")


def main():
    from .catalog import write_resources_js
    pages = all_pages()
    written = write_pages(pages)
    patch_landings()
    patch_sitemap(written)
    patch_hub()
    js, n = write_resources_js()
    print(f"wrote {len(written)} pages")
    print(f"wrote {js} ({n} resources)")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
