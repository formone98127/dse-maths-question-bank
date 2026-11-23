#!/usr/bin/env python3
"""把 M1 掃描成品（Jensen 的 *_P1_題目英文卷.md）匯入 docs/data.js。

用法：python3 scripts/import_m1.py <md_dir> [year ...]
預設年份：2012–2018、2021（data.js 未有的年份）
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DATA = REPO / "docs/data.js"

TAG_MAP = {
    "probability": "概率", "statistics": "統計", "differentiation": "微分法",
    "integration": "積分法", "limits": "極限", "binomial": "二項式定理",
    "exponential & log": "指數與對數", "trigonometry": "三角學",
    "normal distribution": "正態分佈", "poisson": "泊松分佈",
    "confidence interval": "置信區間", "trapezoidal rule": "梯形法",
    "area": "面積", "rate of change": "變化率", "tangent": "切線",
    "conditional probability": "條件概率", "sampling": "抽樣分佈",
    "hypothesis testing": "假設檢驗", "random variable": "隨機變量",
    "expectation": "期望值", "variance": "方差",
}


def tags_cn(raw):
    out = []
    for t in re.split(r"[,，、/]", raw):
        t = t.strip()
        if not t:
            continue
        out.append(TAG_MAP.get(t.lower(), t))
    return out[:4]


def to_html(text):
    lines = [l.rstrip() for l in text.splitlines()]
    blocks, cur, table = [], [], []

    def flush_table():
        nonlocal table
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table
                if not re.match(r"^\|?[\s:|-]+\|?$", r)]
        if rows:
            head = rows[0]
            body = rows[1:]
            h = "<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body:
                h += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
            blocks.append(h + "</tbody></table>")
        table = []

    for line in lines:
        if line.strip().startswith("|"):
            table.append(line)
            continue
        flush_table()
        if not line.strip():
            if cur:
                blocks.append("<p>" + " ".join(cur) + "</p>")
                cur = []
            continue
        img = re.match(r"!\[[^\]]*\]\(([^)]+)\)", line.strip())
        if img:
            blocks.append(f'<p><img src="{img.group(1)}" alt="" /></p>')
            continue
        cur.append(line.strip())
    flush_table()
    if cur:
        blocks.append("<p>" + " ".join(cur) + "</p>")
    html = "\n".join(blocks)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    return html


def plain(text):
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"^\s*\|.*\|\s*$", "", t, flags=re.M)
    t = re.sub(r"\n{2,}", "\n\n", t)
    return t.strip()


def parse_md(path):
    raw = path.read_text(encoding="utf-8")
    parts = re.split(r"\n## 第 (\d+) 題\n", raw)
    out = []
    for i in range(1, len(parts), 2):
        qno = parts[i]
        body = parts[i + 1]
        m = re.search(r"\*\*Tags:\*\*\s*(.+)", body)
        tags = tags_cn(m.group(1)) if m else ["M1"]
        body = re.sub(r"\*\*Tags:\*\*.*\n", "", body)
        body = body.strip()
        out.append({
            "subject": "數學", "year": path.name[:4], "paper": "Paper 1M",
            "type": "題目", "qno": qno, "title": f"第 {qno} 題",
            "section": "M1", "tags": tags,
            "text": plain(body), "html": to_html(body),
            "file": path.name,
        })
    return out


def main():
    md_dir = pathlib.Path(sys.argv[1])
    years = sys.argv[2:] or ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2021"]

    src = DATA.read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    have = {(q["year"], str(q["paper"]), str(q["qno"])) for q in data["questions"]}

    added = 0
    for y in years:
        p = md_dir / f"{y}_P1_題目英文卷.md"
        if not p.exists():
            print(f"skip {y}: 冇 {p.name}")
            continue
        for e in parse_md(p):
            key = (e["year"], e["paper"], e["qno"])
            if key in have:
                continue
            data["questions"].append(e)
            have.add(key)
            added += 1
        print(f"{y}: 累計新增 {added}")

    data["count"] = len(data["questions"])
    DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print("total questions:", data["count"], "added:", added)


if __name__ == "__main__":
    main()
