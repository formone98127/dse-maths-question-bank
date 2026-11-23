#!/usr/bin/env python3
"""喺 hub 加「最新題目」5 條靜態連結（冪等，包 marker）。"""
import json
import pathlib

REPO = pathlib.Path("/home/one/hub_repo")
IDX = REPO / "docs/questions/_index.json"
HUB = REPO / "docs/hub/index.html"
START = "<!-- HUB-LATEST-Q:START -->"
END = "<!-- HUB-LATEST-Q:END -->"

CSS = """<style>
.hub-latest{margin:22px 0 8px}
.hub-latest h2{font-size:1rem;margin:0 0 6px}
.hub-latest p.sub{color:var(--dim,#8a8f98);font-size:.85rem;margin:0 0 10px}
.hub-latest ul{list-style:none;padding:0;margin:0;display:grid;gap:6px}
.hub-latest li a{display:flex;justify-content:space-between;gap:10px;padding:9px 12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:9px;text-decoration:none;color:inherit;font-size:.92rem}
.hub-latest li a:hover{border-color:#58c4dd}
.hub-latest .p{color:#8a8f98;font-size:.82rem;white-space:nowrap}
</style>"""


def main():
    data = json.loads(IDX.read_text(encoding="utf-8"))
    items = sorted(data, key=lambda q: (int(q["year"]) if str(q["year"]).isdigit() else 0,
                                        int(str(q["paper"])), -int(str(q["qno"]).strip("qQ"))),
                   reverse=True)[:5]
    lis = []
    for q in items:
        pct = q.get("answer_pct")
        tail = f"答對率 {round(float(pct))}%" if pct is not None else "官方詳解"
        lis.append(
            f'<li><a href="{q["url"]}"><span>{q["year"]} P{q["paper"]} Q{q["qno"]}</span>'
            f'<span class="p">{tail}</span></a></li>'
        )
    block = (f"{START}\n<section class=\"hub-latest\" aria-label=\"最新題目\">\n{CSS}\n"
             "<h2>最新題目（逐題答案＋詳解）</h2>\n"
             "<p class=\"sub\">啱啱更新嘅題目頁，附官方評卷參考同答對率。</p>\n"
             f"<ul>{''.join(lis)}</ul>\n"
             "<p class=\"sub\"><a href=\"/questions/\">睇全部 448 題 →</a></p>\n"
             f"</section>\n{END}")

    html = HUB.read_text(encoding="utf-8")
    if START in html and END in html:
        head, rest = html.split(START, 1)
        _, tail = rest.split(END, 1)
        html = head + block + tail
    else:
        html = html.replace("<!-- HUB-TOPIC-INDEX:START -->", block + "\n<!-- HUB-TOPIC-INDEX:START -->", 1)
    HUB.write_text(html, encoding="utf-8")
    print("hub latest-5 added:", [f'{q["year"]}P{q["paper"]}Q{q["qno"]}' for q in items])


if __name__ == "__main__":
    main()
