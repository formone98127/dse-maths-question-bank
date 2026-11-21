"""在年份頁加 M1 入口，並寫入 hub 目錄。

用法：python scripts/add_m1_entry.py --write
"""
from __future__ import annotations

import json
import pathlib
import re

SITE = pathlib.Path(r"C:/Users/Administrator/projects/dse-maths-question-bank")
YEARS = ["2019", "2020", "2022", "2023", "2024", "2025"]

ROW = """    <article class="paper-row">
      <a class="paper-main" href="/?subject=%E6%95%B8%E5%AD%B8#__HASH__" title="開啟 M1 題目">
        <div class="paper-year">{year}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">數學</span>
            <span class="tag cat">M1 延伸部分</span>
            <span class="tag lang">英文</span>
          </div>
          <div class="paper-title">文憑試 DSE 數學延伸部分 M1 {year} · 題目（英文）</div>
          <div class="paper-sub">單元一（微積分與統計） · {n} 題</div>
        </div>
      </a>
    </article>
"""


def counts() -> dict[str, int]:
    raw = (SITE / "docs" / "data.js").read_text(encoding="utf-8")
    obj = json.loads(raw[len("window.QB ="):].rstrip().rstrip(";"))
    out: dict[str, int] = {}
    for e in obj["questions"]:
        if e.get("paper") == "Paper 1M":
            out[str(e["year"])] = out.get(str(e["year"]), 0) + 1
    return out


def main(write: bool) -> int:
    cnt = counts()
    for y in YEARS:
        page = SITE / "docs" / "math" / y / "index.html"
        if not page.exists():
            print(f"{y}: 無年份頁，跳過")
            continue
        s = page.read_text(encoding="utf-8")
        if f"#__HASH__" not in s and f'#{{y}}P1MQ1' in s:
            print(f"{y}: 已有 M1 入口")
            continue
        if f"{y}P1MQ1" in s:
            print(f"{y}: 已有 M1 入口")
            continue
        row = ROW.replace("__HASH__", f"{y}P1MQ1").format(year=y, n=cnt.get(y, 0))
        # 插在第一個 </article> 之後
        idx = s.find("</article>")
        if idx == -1:
            print(f"{y}: 找不到插入點")
            continue
        s = s[: idx + len("</article>")] + "\n\n" + row + s[idx + len("</article>"):]
        if write:
            page.write_text(s, encoding="utf-8")
        print(f"{y}: 加 M1 入口（{cnt.get(y,0)} 題）{'✓' if write else '（dry）'}")

    # hub 目錄
    hub = SITE / "docs" / "hub" / "data.js"
    hs = hub.read_text(encoding="utf-8")
    rows = []
    for y in YEARS:
        if f'"#P{y}P1MQ1"' in hs or f'#{"P"}{y}P1MQ1' in hs or f"#{y}P1MQ1" in hs:
            continue
        rows.append(
            '  { id: "math", name: "數學（延伸部分 M1）", year: %s, paper: "M1", lang: "英文", hash: "#%sP1MQ1" },'
            % (y if y.isdigit() else '"%s"' % y, y)
        )
    if rows:
        marker = "const CATALOG = ["
        i = hs.find(marker)
        j = hs.find("\n", i)
        hs = hs[: j + 1] + "\n".join(rows) + "\n" + hs[j + 1:]
        if write:
            hub.write_text(hs, encoding="utf-8")
        print(f"hub 加 {len(rows)} 行{'（dry）' if not write else ''}")
    else:
        print("hub 已有 M1 行")
    return 0


if __name__ == "__main__":
    import sys

    main("--write" in sys.argv)
