"""生成 M1 卷頁：/m1/<year>/paper-1-en/（列出 12 題，連去 reader 深連結）。"""
from __future__ import annotations

import json
import pathlib

SITE = pathlib.Path(r"C:/Users/Administrator/projects/dse-maths-question-bank")
YEARS = ["2019", "2020", "2022", "2023", "2024", "2025"]

TPL = """<!doctype html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSE 數學延伸部分 M1 {year} Paper 1（英文）｜{n} 題｜DSE Hub</title>
<meta name="description" content="HKDSE 數學延伸部分（單元一 M1）{year} 年 Paper 1 英文卷，共 {n} 題，逐題可開來做，附課題標籤。">
<link rel="canonical" href="https://hkdse.exampaper.cloud/m1/{year}/paper-1-en/">
<style>
:root{{--bg:#0f1420;--card:#1a2130;--line:#2b3446;--fg:#e8edf6;--mut:#9aa8bf;--gold:#ffd166}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:"Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif}}
header{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line)}}
header a{{color:var(--fg);text-decoration:none;font-weight:700}}
main{{max-width:860px;margin:0 auto;padding:22px 18px 60px}}
h1{{font-size:22px;margin:6px 0 4px}}
.sub{{color:var(--mut);font-size:14px;margin-bottom:18px}}
ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}
li a{{display:flex;justify-content:space-between;align-items:center;background:var(--card);border:1px solid var(--line);
  border-radius:10px;padding:13px 15px;color:var(--fg);text-decoration:none;font-size:15px}}
li a:hover{{border-color:var(--gold)}}
.tag{{color:var(--mut);font-size:13px}}
footer{{color:var(--mut);font-size:12px;padding:26px 0 0}}
</style>
</head>
<body>
<header><a href="/hub/">DSE Hub</a><span class="tag">數學延伸部分 M1</span></header>
<main>
  <h1>M1 {year} · Paper 1（英文卷）</h1>
  <div class="sub">{n} 題 · 按題意改寫示範，非重現試題</div>
  <ul>
{items}  </ul>
  <footer>試題版權屬香港考試及評核局所有。本頁只提供題目索引與解題示範連結。</footer>
</main>
</body>
</html>
"""


def main(write: bool) -> int:
    raw = (SITE / "docs" / "data.js").read_text(encoding="utf-8")
    obj = json.loads(raw[len("window.QB ="):].rstrip().rstrip(";"))
    by_year: dict[str, list] = {}
    for e in obj["questions"]:
        if e.get("paper") == "Paper 1M":
            by_year.setdefault(str(e["year"]), []).append(e)
    for y in YEARS:
        qs = sorted(by_year.get(y, []), key=lambda e: int(e["qno"]))
        if not qs:
            print(f"{y}: 冇題目，跳過")
            continue
        items = "".join(
            f'    <li><a href="/#{y}P1MQ{q["qno"]}"><span>第 {q["qno"]} 題</span>'
            f'<span class="tag">{"、".join(q.get("tags") or []) or "—"}</span></a></li>\n'
            for q in qs
        )
        html = TPL.format(year=y, n=len(qs), items=items)
        out = SITE / "docs" / "m1" / y / "paper-1-en" / "index.html"
        if write:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
        print(f"{y}: {len(qs)} 題 → {out.relative_to(SITE)} {'OK' if write else 'dry'}")
    return 0


if __name__ == "__main__":
    import sys

    main("--write" in sys.argv)
