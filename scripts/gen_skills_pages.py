#!/usr/bin/env python3
"""生成 /skills/ 技能索引頁，以及把 maps/*.md 轉成 /skills/<year>/paper-<n>/ 頁。"""
import json
import pathlib
import re

REPO = pathlib.Path("/home/one/hub_repo")
DOCS = REPO / "docs"
SK = DOCS / "skills"
SITE = "https://hkdse.exampaper.cloud"

CSS = """
:root{--fg:#111;--mut:#666;--line:#e3e3e3;--bg:#fafafa;--acc:#0b5}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang HK","Microsoft JhengHei",sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
header.site{background:#fff;border-bottom:1px solid var(--line);padding:10px 0;font-size:14px;color:var(--mut)}
h1{font-size:25px;margin:20px 0 8px}
h2{font-size:18px;margin:26px 0 10px}
p.lead{color:var(--mut);margin:0 0 16px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:15px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left}
th{background:#f4f6f5;font-size:13px;color:#444}
td.num{text-align:right;font-variant-numeric:tabular-nums}
a{color:#0a58ca}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px;margin:0 0 14px}
footer{margin:34px 0 50px;color:var(--mut);font-size:13px}
"""


def md_to_html(md):
    out, in_table = [], False
    rows = []
    for line in md.splitlines():
        s = line.rstrip()
        if s.startswith("|"):
            if re.match(r"^\|?[\s:|-]+\|?$", s):
                continue
            rows.append([c.strip() for c in s.strip("|").split("|")])
            in_table = True
            continue
        if in_table:
            if rows:
                head, body = rows[0], rows[1:]
                out.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"
                           + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body)
                           + "</tbody></table>")
            rows, in_table = [], False
        m = re.match(r"^(#{1,3})\s+(.*)", s)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
        elif s.strip().startswith("- "):
            out.append(f"<p>• {s.strip()[2:]}</p>")
        elif s.strip():
            out.append(f"<p>{s.strip()}</p>")
    if rows:
        head, body = rows[0], rows[1:]
        out.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"
                   + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body)
                   + "</tbody></table>")
    return "\n".join(out)


def main():
    book = json.loads((SK / "math_skill_book.json").read_text(encoding="utf-8"))
    cards = json.loads((SK / "math_question_cards.json").read_text(encoding="utf-8"))["cards"]
    counts = {}
    for c in cards:
        p = c.get("primary_hub_topic") or {}
        if p.get("topic_name"):
            counts[p["topic_name"]] = counts.get(p["topic_name"], 0) + 1

    rows = "".join(
        f'<tr><td>{t["name"]}</td><td>{t.get("group","")}</td>'
        f'<td class="num">{len(t.get("knowledge_points") or [])}</td>'
        f'<td class="num">{counts.get(t["name"], 0)}</td></tr>'
        for t in sorted(book["topics"], key=lambda x: -counts.get(x["name"], 0))
    )

    maps = sorted((SK / "maps").glob("*.md"))
    map_items = "".join(
        f'<li><a href="/skills/{m.stem.split("-")[1]}/paper-{m.stem.split("-")[3]}/">{m.stem}</a></li>'
        for m in maps
    ) or "<li>暫未有（試點：2012 卷二）</li>"

    html = f"""<!DOCTYPE html><html lang="zh-Hant-HK"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSE 數學技能地圖｜20 大課題·知識點·常見陷阱｜DSE Hub</title>
<meta name="description" content="DSE 數學技能地圖：20 大課題、知識點、公式、能力與錯選項陷阱分析，逐題對應，幫你知邊個概念最易失分。">
<link rel="canonical" href="{SITE}/skills/">
<style>{CSS}</style></head><body>
<header class="site"><div class="wrap"><a href="/hub/">← DSE Hub</a> ｜ <a href="/questions/">題目目錄</a> ｜ <a href="/stats/">答對率統計</a></div></header>
<main class="wrap">
<h1>DSE 數學技能地圖</h1>
<p class="lead">把每條題目拆成「課題 → 知識點 → 公式 → 能力 → 陷阱」。總共 {len(cards)} 張題卡，覆蓋必修同 M1。</p>
<div class="card">
<h2>技能地圖（逐卷）</h2>
<ul>{map_items}</ul>
</div>
<h2>20 大課題</h2>
<table><thead><tr><th>課題</th><th>範疇</th><th class="num">知識點</th><th class="num">題目（主課題）</th></tr></thead>
<tbody>{rows}</tbody></table>
<h2>點用呢個地圖</h2>
<p>每條題目頁底部都有「技能分析」：主課題、相關課題、知識點、用到嘅能力，以及每個錯選項對應嘅陷阱。溫習時唔止知答案，仲知自己係「概念錯」定「計算錯」。</p>
<footer>題目版權屬香港考試及評核局。技能分類為本站整理，非官方。<br>
<a href="/hub/">DSE Hub</a> ｜ <a href="/questions/">全部題目</a> ｜ <a href="/topics/">按課題</a></footer>
</main></body></html>
"""
    out = SK / "index.html"
    out.write_text(html, encoding="utf-8")
    print("wrote /skills/ index, topics:", len(book["topics"]), "maps:", len(maps))

    for m in maps:
        parts = m.stem.split("-")          # math-2012-paper-2
        year, paper = parts[1], parts[3]
        body = md_to_html(m.read_text(encoding="utf-8"))
        page = f"""<!DOCTYPE html><html lang="zh-Hant-HK"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{year} DSE 數學卷二 技能地圖｜陷阱與知識點分析｜DSE Hub</title>
<meta name="description" content="{year} DSE 數學 Paper {paper} 技能地圖：逐題課題、知識點、能力、錯選項陷阱分佈。">
<link rel="canonical" href="{SITE}/skills/{year}/paper-{paper}/">
<style>{CSS}</style></head><body>
<header class="site"><div class="wrap"><a href="/hub/">← DSE Hub</a> ｜ <a href="/skills/">技能地圖</a></div></header>
<main class="wrap">{body}
<footer>題目版權屬香港考試及評核局；技能分類為本站整理。<br><a href="/skills/">返回技能地圖</a></footer>
</main></body></html>
"""
        d = SK / year / f"paper-{paper}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        print("wrote", d.relative_to(DOCS))


if __name__ == "__main__":
    main()
