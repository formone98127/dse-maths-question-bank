#!/usr/bin/env python3
"""由 data.js 自動生成 Hub 嘅「數學延伸部分 M1／M2」入口區塊（唔准手改）。"""
import json
import pathlib
import re

REPO = pathlib.Path("/home/one/hub_repo")
DOCS = REPO / "docs"
HUB = DOCS / "hub/index.html"
START = "<!-- EXT-INDEX:START -->"
END = "<!-- EXT-INDEX:END -->"


def main():
    s = (DOCS / "data.js").read_text(encoding="utf-8")
    data = json.loads(s[s.index("{"): s.rindex("}") + 1])
    groups = {"Paper 1M": ("M1", "微積分與統計"), "Paper 2M": ("M2", "代數與微積分")}
    blocks = {}
    for paper, (code, name) in groups.items():
        years = {}
        for q in data["questions"]:
            if q["paper"] == paper and q["type"] == "題目":
                years[str(q["year"])] = years.get(str(q["year"]), 0) + 1
        years = {y: n for y, n in years.items() if (DOCS / code.lower() / y / "paper-1-en/index.html").exists()}
        if not years:
            continue
        total = sum(years.values())
        items = "".join(
            f'<li><a href="/{code.lower()}/{y}/paper-1-en/">{y}</a></li>'
            for y in sorted(years, reverse=True)
        )
        blocks[paper] = (f'    <div class="ext-group">\n'
                         f'      <span class="ext-label">{code}（{name}）<em>{len(years)} 年 · {total} 題</em></span>\n'
                         f'      <ul class="ext-list">{items}</ul>\n'
                         f'    </div>\n')

    html = (START + '\n  <section class="ext-index" aria-label="數學延伸部分 M1／M2">\n'
            '    <h2>數學延伸部分（M1／M2）逐題題庫</h2>\n'
            + blocks.get("Paper 2M", "") + blocks.get("Paper 1M", "") +
            '  </section>\n' + END)

    tpl = HUB.read_text(encoding="utf-8")
    if START in tpl and END in tpl:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), html, tpl, flags=re.S)
    else:
        old = re.search(r'\n  <section class="ext-index".*?</section>\n', tpl, flags=re.S)
        if not old:
            raise SystemExit("找不到 ext-index 區塊")
        new = tpl[: old.start()] + "\n" + html + tpl[old.end():]
    HUB.write_text(new, encoding="utf-8")
    print("ext-index 已自動更新：",
          {k: len(re.findall(r"paper-1-en/", v)) for k, v in blocks.items()})


if __name__ == "__main__":
    main()
