#!/usr/bin/env python3
"""在 Hub 主頁 (/hub/) 加「按課題」可爬靜態內鏈，連去全部 /topics/<slug>/ 頁。

目的（SEO，Kin 2026-11-19）：/hub/ 係最強嘅已收錄頁，但原本靜態連結全部係
/#YYYYPnQm 呢種 hash（Google 唔會當成連去獨立 URL），而且 0 條連去 /topics/。
喺度補一條 hub → topics → questions 嘅可爬鏈，等 Google 由已收錄嘅 hub 爬去
143 課題頁、再落 448 題目頁。

冪等：用 HUB-TOPIC-INDEX:START/END 標記，重跑只會替換中間內容。
用法：python3 scripts/inject_hub_topic_links.py [--write]
"""
from __future__ import annotations
import re, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB = os.path.join(ROOT, "docs", "hub", "index.html")
START = "<!-- HUB-TOPIC-INDEX:START -->"
END = "<!-- HUB-TOPIC-INDEX:END -->"


def collect():
    rows = []
    for f in glob.glob(os.path.join(ROOT, "docs", "topics", "*", "index.html")):
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
    lis = "".join(
        f'<li><a href="/topics/{slug}/">{name}<span class="n">{cnt}</span></a></li>'
        for slug, name, cnt in rows
    )
    n = len(rows)
    return (
        f'{START}\n'
        f'<section class="hub-topic-index" aria-label="按課題瀏覽歷屆試題">\n'
        f'  <h2>按課題瀏覽（{n} 個 DSE 數學課題）</h2>\n'
        f'  <p class="hti-sub">每個課題頁收錄歷屆相關題目、答案、題解同答對率，可直接跳去逐題閱讀。</p>\n'
        f'  <ul class="hti-list">{lis}</ul>\n'
        f'</section>\n'
        f'{END}'
    )


def main():
    write = "--write" in sys.argv
    rows = collect()
    block = build(rows)
    html = open(HUB, encoding="utf-8").read()
    if START in html and END in html:
        html2 = re.sub(re.escape(START) + r".*?" + re.escape(END), block, html, flags=re.S)
    else:
        anchor = '<section class="seo-faq"'
        i = html.find(anchor)
        if i == -1:
            sys.exit("anchor <section class=\"seo-faq\"> not found")
        html2 = html[:i] + block + "\n" + html[i:]
    changed = html2 != html
    print(f"topics={len(rows)} changed={changed} write={write}")
    if write and changed:
        open(HUB, "w", encoding="utf-8").write(html2)


if __name__ == "__main__":
    main()
