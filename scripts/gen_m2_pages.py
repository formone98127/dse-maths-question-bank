#!/usr/bin/env python3
"""生成 M2 卷頁：/m2/<year>/paper-1-en/（列出該年題目；有深度分析頁就直連，否則 reader 深連結）。"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO))

from build_seo import (  # noqa: E402
    ROOT,
    SITE as SITE_URL,
    ld_json,
    seo_head,
)

ANALYSIS_DIR = ROOT / "analysis" / "math"

TPL = """<!doctype html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
{head}
<script type="application/ld+json">{ld}</script>
<style>
:root{{--bg:#0f1420;--card:#1a2130;--line:#2b3446;--fg:#e8edf6;--mut:#9aa8bf;--gold:#ffd166}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:"Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif}}
header{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line)}}
header a{{color:var(--fg);text-decoration:none;font-weight:700}}
main{{max-width:860px;margin:0 auto;padding:22px 18px 60px}}
h1{{font-size:22px;margin:6px 0 4px}}
p.sub{{color:var(--mut);margin:0 0 18px;font-size:14px}}
ul.qs{{list-style:none;padding:0;margin:0;display:grid;gap:8px}}
ul.qs a{{display:flex;justify-content:space-between;gap:10px;align-items:center;background:var(--card);
border:1px solid var(--line);border-radius:10px;padding:11px 14px;text-decoration:none;color:var(--fg)}}
ul.qs a:hover{{border-color:var(--gold);color:var(--gold)}}
.tag{{font-size:12px;color:var(--mut)}}
.deep{{color:var(--gold);font-size:12px;margin-left:8px}}
footer{{color:var(--mut);font-size:13px;border-top:1px solid var(--line);padding:16px 18px;margin-top:26px}}
</style>
</head>
<body>
<header><a href="/hub/">← DSE Hub</a> <span style="color:var(--mut)">｜ 數學延伸部分 M2</span></header>
<main>
<h1>M2 {year} · Paper 1（英文卷）</h1>
<p class="sub">共 {n} 題 · 官方評卷參考逐題對應</p>
<ul class="qs">{items}</ul>
</main>
<footer>題目版權屬香港考試及評核局。本站提供索引、課題標籤與解答整理。<br>
<a href="/hub/" style="color:var(--gold)">返回 DSE Hub</a> ｜ <a href="/questions/" style="color:var(--gold)">題目目錄</a></footer>
</body>
</html>
"""


def q_href(year: str, qno) -> str:
    """有深度分析頁（/math/<year>/paper-2m-en/qN/）就直連，否則返 reader 深連結。"""
    if (ANALYSIS_DIR / year / "paper-2m" / f"q{qno}.json").is_file():
        return f"/math/{year}/paper-2m-en/q{qno}/"
    return f"/#{year}P2MQ{qno}"


def main():
    src = (DOCS / "data.js").read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    by_year = {}
    for q in data["questions"]:
        if q["paper"] == "Paper 2M" and q["type"] == "題目":
            by_year.setdefault(str(q["year"]), []).append(q)

    total = 0
    for year, qs in sorted(by_year.items()):
        qs.sort(key=lambda q: int(q["qno"]))
        rows = []
        for q in qs:
            qno = q["qno"]
            has_deep = (ANALYSIS_DIR / year / "paper-2m" / f"q{qno}.json").is_file()
            badge = '<span class="deep">深度分析</span>' if has_deep else ""
            tags = "、".join(q.get("tags") or []) or "—"
            rows.append(
                f'<li><a href="{q_href(year, qno)}"><span>第 {qno} 題</span>'
                f'<span class="tag">{tags}{badge}</span></a></li>'
            )
        items = "".join(rows)
        canonical = f"{SITE_URL}/m2/{year}/paper-1-en/"
        title = f"DSE 數學延伸部分 M2 {year} Paper 1（英文）｜{len(qs)} 題｜DSE Hub"
        desc = f"HKDSE 數學延伸單元二（M2，代數與微積分）{year} 年 Paper 1 英文卷，共 {len(qs)} 題，逐題可開來做，附課題標籤同深度分析。"
        head = seo_head(title, desc, canonical)
        ld = ld_json(
            {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": f"{SITE_URL}/hub/"},
                            {"@type": "ListItem", "position": 2, "name": "數學延伸 M2", "item": canonical},
                        ],
                    },
                    {
                        "@type": "CollectionPage",
                        "name": title,
                        "url": canonical,
                        "inLanguage": "zh-Hant-HK",
                        "numberOfItems": len(qs),
                    },
                ],
            }
        )
        html = TPL.format(year=year, n=len(qs), items=items, site=SITE_URL, head=head, ld=ld)
        out = DOCS / "m2" / year / "paper-1-en" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        total += 1
        print(f"{year}: {len(qs)} 題 → {out.relative_to(REPO)}")
    print("pages:", total)


if __name__ == "__main__":
    main()
