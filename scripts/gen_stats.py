#!/usr/bin/env python3
"""生成 /stats/ 答對率統計頁（由 docs/questions/_index.json）。"""
import json
import pathlib
import statistics
from collections import defaultdict

REPO = pathlib.Path("/home/one/hub_repo")
IDX = REPO / "docs/questions/_index.json"
OUT = REPO / "docs/stats/index.html"
SITE = "https://hkdse.exampaper.cloud"

CSS = """
:root{--fg:#111;--mut:#666;--line:#e3e3e3;--bg:#fafafa;--acc:#0b5;--hot:#d64545;--cool:#2f8f5b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang HK","Microsoft JhengHei",sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
header.site{background:#fff;border-bottom:1px solid var(--line);padding:12px 0;font-size:14px;color:var(--mut)}
h1{font-size:26px;margin:22px 0 8px}
h2{font-size:18px;margin:28px 0 10px}
p.lead{color:var(--mut);margin:0 0 18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px}
.card b{display:block;font-size:26px;line-height:1.2}
.card span{color:var(--mut);font-size:13px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:15px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left}
th{background:#f3f5f4;font-weight:600;font-size:13px;color:#444}
tr:last-child td{border-bottom:0}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.bar{display:inline-block;height:9px;border-radius:5px;vertical-align:middle}
.b-hot{background:var(--hot)}.b-cool{background:var(--cool)}
a{color:#0a58ca}
footer{margin:36px 0 50px;color:var(--mut);font-size:13px}
"""


def main():
    data = json.loads(IDX.read_text(encoding="utf-8"))
    mc = [q for q in data if q.get("answer_pct") is not None]
    pcts = [q["answer_pct"] for q in mc]
    avg = statistics.mean(pcts)
    med = statistics.median(pcts)
    hardest = sorted(mc, key=lambda q: q["answer_pct"])[:20]
    easiest = sorted(mc, key=lambda q: -q["answer_pct"])[:10]

    by_year = defaultdict(list)
    for q in mc:
        by_year[q["year"]].append(q["answer_pct"])
    year_rows = "".join(
        f'<tr><td>{y}</td><td class="num">{len(v)}</td><td class="num">{statistics.mean(v):.1f}%</td>'
        f'<td class="num">{min(v)}%</td><td class="num">{max(v)}%</td></tr>'
        for y, v in sorted(by_year.items())
    )

    by_topic = defaultdict(list)
    for q in mc:
        for t in (q.get("tags") or []):
            by_topic[t].append(q["answer_pct"])
    topic_rows = "".join(
        f'<tr><td>{t}</td><td class="num">{len(v)}</td><td class="num">{statistics.mean(v):.1f}%</td>'
        f'<td><span class="bar {"b-hot" if statistics.mean(v) < 50 else "b-cool"}" '
        f'style="width:{int(statistics.mean(v))}px"></span></td></tr>'
        for t, v in sorted(by_topic.items(), key=lambda kv: statistics.mean(kv[1]))
        if len(v) >= 6
    )

    hard_rows = "".join(
        f'<tr><td><a href="{q["url"]}">{q["year"]} P{q["paper"]} Q{q["qno"]}</a></td>'
        f'<td>{", ".join(q.get("tags") or [])[:24]}</td>'
        f'<td class="num" style="color:var(--hot);font-weight:600">{q["answer_pct"]}%</td></tr>'
        for q in hardest
    )

    easy_rows = "".join(
        f'<tr><td><a href="{q["url"]}">{q["year"]} P{q["paper"]} Q{q["qno"]}</a></td>'
        f'<td class="num">{q["answer_pct"]}%</td></tr>'
        for q in easiest
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSE 數學答對率統計（2012–2025）｜最難題目排行｜DSE Hub</title>
<meta name="description" content="DSE 數學歷屆 MC 答對率完整統計：{len(mc)} 題官方數據、每年平均答對率、最難 20 題逐題連結、各課題難度排行。">
<link rel="canonical" href="{SITE}/stats/">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LTB27V0RGW"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-LTB27V0RGW');</script>
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="wrap"><a href="/hub/">← DSE Hub</a> ｜ <a href="/questions/">全部題目目錄</a> ｜ <a href="/topics/">課題索引</a></div></header>
<main class="wrap">
<h1>DSE 數學答對率統計（2012–2025）</h1>
<p class="lead">數據來自香港考試及評核局歷屆考生表現報告。答對率＝該題全體考生答對百分比。</p>

<div class="cards">
  <div class="card"><b>{len(mc)}</b><span>有官方答對率嘅 MC 題</span></div>
  <div class="card"><b>{avg:.1f}%</b><span>平均答對率</span></div>
  <div class="card"><b>{med:.0f}%</b><span>中位數</span></div>
  <div class="card"><b>{min(pcts)}%</b><span>最難一題</span></div>
</div>

<h2>每年平均答對率</h2>
<table><thead><tr><th>年份</th><th class="num">題數</th><th class="num">平均</th><th class="num">最低</th><th class="num">最高</th></tr></thead>
<tbody>{year_rows}</tbody></table>

<h2>最難 20 題（全港答對率最低）</h2>
<table><thead><tr><th>題目</th><th>課題</th><th class="num">答對率</th></tr></thead>
<tbody>{hard_rows}</tbody></table>

<h2>最容易 10 題</h2>
<table><thead><tr><th>題目</th><th class="num">答對率</th></tr></thead>
<tbody>{easy_rows}</tbody></table>

<h2>課題難度排行（至少 6 題樣本）</h2>
<table><thead><tr><th>課題</th><th class="num">題數</th><th class="num">平均答對率</th><th></th></tr></thead>
<tbody>{topic_rows}</tbody></table>

<footer>
<p>資料來源：香港考試及評核局《考生表現》報告（2012–2025）。題目版權屬香港考試及評核局所有，本站只提供索引同統計分析。</p>
<p><a href="/hub/">返回 DSE Hub</a> ｜ <a href="/questions/">逐題目錄</a> ｜ <a href="/topics/">按課題</a></p>
</footer>
</main>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} — mc={len(mc)} avg={avg:.1f}")


if __name__ == "__main__":
    main()
