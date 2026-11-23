#!/usr/bin/env python3
"""生成 M2 卷頁：/m2/<year>/paper-1-en/（列出該年題目，連 reader 深連結）。"""
import json
import pathlib

REPO = pathlib.Path("/home/one/hub_repo")
DOCS = REPO / "docs"
SITE = "https://hkdse.exampaper.cloud"

TPL = """<!doctype html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSE 數學延伸部分 M2 {year} Paper 1（英文）｜{n} 題｜DSE Hub</title>
<meta name="description" content="HKDSE 數學延伸單元二（M2，代數與微積分）{year} 年 Paper 1 英文卷，共 {n} 題，逐題可開來做，附課題標籤。">
<link rel="canonical" href="{site}/m2/{year}/paper-1-en/">
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
        items = "".join(
            f'<li><a href="/#{year}P2MQ{q["qno"]}"><span>第 {q["qno"]} 題</span>'
            f'<span class="tag">{"、".join(q.get("tags") or []) or "—"}</span></a></li>'
            for q in qs
        )
        html = TPL.format(year=year, n=len(qs), items=items, site=SITE)
        out = DOCS / "m2" / year / "paper-1-en" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        total += 1
        print(f"{year}: {len(qs)} 題 → {out.relative_to(DOCS)}")
    print("pages:", total)


if __name__ == "__main__":
    main()
