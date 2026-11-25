"""生成 M1 卷頁：/m1/<year>/paper-1-en/（列出 12 題；有深度分析頁就直連，否則 reader 深連結）。"""
from __future__ import annotations

import json
import pathlib
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SITE))

from build_seo import (  # noqa: E402
    ROOT,
    SITE as SITE_URL,
    ld_json,
    seo_head,
)

YEARS = [str(y) for y in range(2012, 2026)] + ["PP", "SP"]
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
.sub{{color:var(--mut);font-size:14px;margin-bottom:18px}}
ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}
li a{{display:flex;justify-content:space-between;align-items:center;background:var(--card);border:1px solid var(--line);
  border-radius:10px;padding:13px 15px;color:var(--fg);text-decoration:none;font-size:15px}}
li a:hover{{border-color:var(--gold)}}
li a .deep{{color:var(--gold);font-size:12px;margin-left:8px}}
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


def q_href(year: str, qno) -> str:
    """有深度分析頁（/math/<year>/paper-1m-en/qN/）就直連，否則返 reader 深連結。"""
    if (ANALYSIS_DIR / year / "paper-1m" / f"q{qno}.json").is_file():
        return f"/math/{year}/paper-1m-en/q{qno}/"
    return f"/#{year}P1MQ{qno}"


def main(write: bool) -> int:
    raw = (SITE / "docs" / "data.js").read_text(encoding="utf-8")
    obj = json.loads(raw[len("window.QB ="):].rstrip().rstrip(";"))
    by_year: dict[str, list] = {}
    for e in obj["questions"]:
        if e.get("paper") == "Paper 1M" and e.get("type") == "題目":
            by_year.setdefault(str(e["year"]), []).append(e)
    for y in YEARS:
        qs = sorted(by_year.get(y, []), key=lambda e: int(e["qno"]))
        if not qs:
            print(f"{y}: 冇題目，跳過")
            continue
        rows = []
        for q in qs:
            qno = q["qno"]
            has_deep = (ANALYSIS_DIR / y / "paper-1m" / f"q{qno}.json").is_file()
            badge = '<span class="deep">深度分析</span>' if has_deep else ""
            tags = "、".join(q.get("tags") or []) or "—"
            rows.append(
                f'    <li><a href="{q_href(y, qno)}"><span>第 {qno} 題</span>'
                f'<span class="tag">{tags}{badge}</span></a></li>\n'
            )
        items = "".join(rows)
        canonical = f"{SITE_URL}/m1/{y}/paper-1-en/"
        title = f"DSE 數學延伸部分 M1 {y} Paper 1（英文）｜{len(qs)} 題｜DSE Hub"
        desc = f"HKDSE 數學延伸部分（單元一 M1）{y} 年 Paper 1 英文卷，共 {len(qs)} 題，逐題可開來做，附課題標籤同深度分析。"
        head = seo_head(title, desc, canonical)
        ld = ld_json(
            {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": f"{SITE_URL}/hub/"},
                            {"@type": "ListItem", "position": 2, "name": "數學延伸 M1", "item": canonical},
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
        html = TPL.format(year=y, n=len(qs), items=items, head=head, ld=ld)
        out = SITE / "docs" / "m1" / y / "paper-1-en" / "index.html"
        if write:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
        print(f"{y}: {len(qs)} 題 → {out.relative_to(SITE)} {'OK' if write else 'dry'}")
    return 0


if __name__ == "__main__":
    main("--write" in sys.argv)
