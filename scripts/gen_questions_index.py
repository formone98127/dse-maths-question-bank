#!/usr/bin/env python3
"""生成 /questions/ 總目錄（448 題靜態內鏈）— 解決題目頁「Google 無法辨識」孤兒問題。

用法：python3 scripts/gen_questions_index.py
輸出：docs/questions/index.html
"""
import json
import pathlib
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parent.parent
IDX = REPO / "docs/questions/_index.json"
OUT = REPO / "docs/questions/index.html"

CSS = """
:root{--bg:#0b0d10;--card:#14181d;--tx:#e8eaed;--dim:#9aa3ad;--ln:#232b34;--ac:#58c4dd}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 -apple-system,"PingFang HK","Microsoft JhengHei",system-ui,sans-serif}
header{padding:28px 20px 10px;max-width:980px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 8px}
p.lead{color:var(--dim);margin:0 0 4px}
main{max-width:980px;margin:0 auto;padding:0 20px 60px}
section{margin-top:26px}
h2{font-size:1.05rem;border-bottom:1px solid var(--ln);padding-bottom:8px}
ul{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:6px}
li a{display:block;padding:7px 9px;background:var(--card);border:1px solid var(--ln);border-radius:8px;color:var(--tx);text-decoration:none;font-size:.92rem}
li a:hover{border-color:var(--ac);color:var(--ac)}
.note{color:var(--dim);font-size:.9rem;margin-top:6px}
footer{max-width:980px;margin:0 auto;padding:20px;color:var(--dim);font-size:.85rem}
a{color:var(--ac)}
"""


def main():
    data = json.loads(IDX.read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for q in data:
        groups[(str(q["year"]), str(q["paper"]))].append(q)
    for k in groups:
        groups[k].sort(key=lambda q: int(str(q["qno"]).strip("qQ")))

    parts = []
    for (year, paper) in sorted(groups, key=lambda k: (-int(k[0]) if k[0].isdigit() else 0, k[1])):
        qs = groups[(year, paper)]
        links = "".join(
            f'<li><a href="{q["url"]}">Q{q["qno"]}</a></li>' for q in qs
        )
        label = f"{year} 年 Paper {paper}" if year.isdigit() else f"{year} Paper {paper}"
        parts.append(f'<section><h2>{label}（{len(qs)} 題）</h2><ul>{links}</ul></section>')

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSE 數學題目總目錄（{len(data)} 題逐題頁）｜DSE 數學題庫</title>
<meta name="description" content="DSE 數學 2019–2025 共 {len(data)} 條題目逐題頁目錄：官方評卷參考、答對率、課題標籤，一頁直達。">
<link rel="canonical" href="https://hkdse.exampaper.cloud/questions/">
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>DSE 數學題目總目錄</h1>
  <p class="lead">2019–2025 共 <strong>{len(data)}</strong> 條題目，逐題獨立頁（含官方評卷參考、答對率、課題標籤）。</p>
  <p class="note"><a href="/hub/">← 返回題庫首頁</a>　｜　<a href="/topics/">按課題瀏覽</a></p>
</header>
<main>
{''.join(parts)}
</main>
<footer>© DSE 數學題庫　｜　hkdse.exampaper.cloud</footer>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} — {len(data)} links, {len(groups)} groups")


if __name__ == "__main__":
    main()
