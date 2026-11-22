"""年份頁的 M1 入口（獨立一段，不與必修卷混在一起）。"""
from __future__ import annotations

import json
import pathlib

SITE = pathlib.Path(r"C:/Users/Administrator/projects/dse-maths-question-bank")
YEARS = ["2019", "2020", "2022", "2023", "2024", "2025"]

CARD = """    <article class="paper-row">
      <a class="paper-main" href="/#__HASH__" title="開啟 M1 題目">
        <div class="paper-year">{year}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">數學</span>
            <span class="tag cat">延伸部分 M1</span>
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


def strip_old(s: str, year: str) -> str:
    token = f"{year}P1MQ1"
    i = s.find(token)
    while i != -1:
        start = s.rfind("<article", 0, i)
        end = s.find("</article>", i)
        if start == -1 or end == -1:
            break
        end += len("</article>")
        s = s[:start] + s[end:]
        i = s.find(token)
    return s


def main(write: bool) -> int:
    cnt = counts()
    for y in YEARS:
        page = SITE / "docs" / "math" / y / "index.html"
        if not page.exists():
            print(f"{y}: 無年份頁")
            continue
        s = page.read_text(encoding="utf-8")
        s = strip_old(s, y)
        card = CARD.replace("__HASH__", f"{y}P1MQ1").format(year=y, n=cnt.get(y, 0))
        sect = (f'<section class="year-group">\n  <h2>{y} 年延伸部分 M1</h2>\n'
                f'  <div class="paper-list">\n{card}  </div>\n</section>\n')
        idx = s.find("</main>")
        if idx == -1:
            print(f"{y}: 找不到 </main>")
            continue
        s = s[:idx] + sect + s[idx:]
        if write:
            page.write_text(s, encoding="utf-8")
        print(f"{y}: 獨立 M1 段（{cnt.get(y,0)} 題）{'OK' if write else 'dry'}")
    return 0


if __name__ == "__main__":
    import sys

    main("--write" in sys.argv)
