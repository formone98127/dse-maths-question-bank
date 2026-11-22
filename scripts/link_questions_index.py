#!/usr/bin/env python3
"""把 /questions/ 加入 sitemap 及 hub 首頁連結（冪等）。"""
import pathlib
import re

REPO = pathlib.Path("/home/one/hub_repo")
URL = "https://hkdse.exampaper.cloud/questions/"

sm = REPO / "docs/sitemap.xml"
s = sm.read_text(encoding="utf-8")
if URL not in s:
    s = s.replace(
        "</urlset>",
        f"  <url><loc>{URL}</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>\n</urlset>",
    )
    sm.write_text(s, encoding="utf-8")
    print("sitemap: added")
else:
    print("sitemap: already present")

hub = REPO / "docs/hub/index.html"
t = hub.read_text(encoding="utf-8")
if 'href="/questions/"' in t:
    print("hub: already linked")
else:
    new, n = re.subn(
        r'(<a href="/topics/">按課題瀏覽</a>)',
        r'\1 · <a href="/questions/">全部題目目錄（448）</a>',
        t,
        count=1,
    )
    if n:
        hub.write_text(new, encoding="utf-8")
        print("hub: link added")
    else:
        print("hub: anchor not found — skipped (manual check needed)")
