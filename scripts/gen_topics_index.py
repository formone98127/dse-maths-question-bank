#!/usr/bin/env python3
"""生成 /topics/ 課題總匯頁（之前 404，但所有課題頁 header 都連去 /topics/）。

由 docs/topics/*/index.html 抽 slug＋中文名＋題數，出 docs/topics/index.html。
冪等，可重跑（新課題會自動加入）。
用法：python3 scripts/gen_topics_index.py [--write]
"""
from __future__ import annotations
import re, glob, os, sys, json, html as H

from build_meta import ver

VER = ver()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(ROOT, "docs", "topics")
OUT = os.path.join(TDIR, "index.html")


def collect():
    rows = []
    for f in glob.glob(os.path.join(TDIR, "*", "index.html")):
        slug = os.path.basename(os.path.dirname(f))
        h = open(f, encoding="utf-8").read()
        m = re.search(r"<h1>DSE 數學：(.+?) 歷屆試題總覽</h1>", h)
        name = m.group(1) if m else slug
        t = re.search(r"<title>[^<]*?（(\d+) 題", h)
        cnt = int(t.group(1)) if t else 0
        rows.append((slug, name, cnt))
    rows.sort(key=lambda r: (-r[2], r[1]))
    return rows


def build(rows):
    lis = "\n".join(
        f'      <li><a href="/topics/{slug}/">{H.escape(name)}<span class="n">{cnt} 題</span></a></li>'
        for slug, name, cnt in rows
    )
    items = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"url":"https://hkdse.exampaper.cloud/topics/{slug}/","name":"{H.escape(name)}"}}'
        for i, (slug, name, cnt) in enumerate(rows[:20])
    )
    n = len(rows)
    title = f"DSE 數學課題總匯（{n} 個課題）｜歷屆試題＋答案｜DSE Hub"
    desc = f"按課題瀏覽 DSE 數學歷屆試題：{n} 個課題頁，收錄相關題目、答案、題解同考生答對率。"
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://hkdse.exampaper.cloud/topics/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b1220">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","url":"https://hkdse.exampaper.cloud/topics/","inLanguage":"zh-Hant-HK","mainEntity":{{"@type":"ItemList","numberOfItems":{n},"itemListElement":[{items}]}}}}</script>
<style>
.main{{max-width:760px;margin:0 auto;padding:18px 16px 40px;color:var(--ink,#fff)}}
.main h1{{font-size:20px;margin:0 0 6px}}
.main .sub{{color:var(--ink-2,rgba(235,235,245,.64));font-size:13.5px;margin-bottom:16px}}
.topic-grid{{list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 16px}}
.topic-grid li a{{display:flex;justify-content:space-between;gap:8px;padding:7px 0;color:#409cff;text-decoration:none;border-bottom:1px solid rgba(84,84,88,.48);font-size:14px}}
.topic-grid li a:hover{{text-decoration:underline}}
.topic-grid .n{{color:rgba(235,235,245,.42);font-variant-numeric:tabular-nums;font-size:12.5px}}
.bc{{font-size:13px;margin-bottom:10px}}
.bc a{{color:#409cff;text-decoration:none}}
@media(max-width:420px){{.topic-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="top" style="max-width:760px;margin:0 auto;padding:14px 16px 4px">
  <p class="bc"><a href="/hub/">DSE Hub</a> › <a href="/math/">數學</a> › 課題</p>
</header>
<main class="main">
  <h1>DSE 數學課題總匯（{n} 個課題）</h1>
  <p class="sub">每個課題頁收錄歷屆相關題目、答案、題解同考生答對率，按題數排列。</p>
  <ul class="topic-grid">
{lis}
  </ul>
</main>
<footer style="max-width:760px;margin:0 auto;padding:16px;color:rgba(235,235,245,.5);font-size:12.5px">
  站內只放索引、連結同課題標籤 · <a href="/hub/" style="color:#409cff">返回 DSE Hub</a> · <a href="/privacy/" style="color:#409cff">私隱政策</a>
</footer>
</body>
</html>
"""


def main():
    rows = collect()
    out = build(rows)
    if "--write" in sys.argv:
        open(OUT, "w", encoding="utf-8").write(out)
        print("wrote", OUT, "topics:", len(rows))
    else:
        print("dry-run topics:", len(rows), "-> (add --write)")


if __name__ == "__main__":
    main()
