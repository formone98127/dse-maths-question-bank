#!/usr/bin/env python3
"""匯入 M2 試卷（<year>_P1_題目英文卷.md）→ docs/data.js（paper=Paper 2M）。"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DATA = REPO / "docs/data.js"

TAG_RULES = [
    ("矩陣", [r"matrix", r"matrices", r"\bdeterminant\b", r"inverse of"]),
    ("向量", [r"\bvector", r"\bvec", r"\\mathbf\{i\}", r"cross product", r"dot product"]),
    ("積分法", [r"\\int", r"integral", r"integrate"]),
    ("微分法", [r"derivative", r"differentiate", r"\\frac\{d", r"rate of change"]),
    ("微分方程", [r"differential equation", r"\\frac\{dy\}\{dx\} ="]),
    ("極限", [r"\blimit\b", r"\\lim", r"tends to"]),
    ("二項式定理", [r"binomial", r"ascending powers"]),
    ("三角學", [r"\\sin", r"\\cos", r"\\tan", r"radian"]),
    ("對數與指數", [r"\\ln", r"e\^", r"logarithm"]),
    ("數列與級數", [r"sequence", r"series", r"sum to infinity"]),
]


def tags_for(text):
    low = text.lower()
    out = [name for name, pats in TAG_RULES if any(re.search(p, low) for p in pats)]
    return out[:3] or ["M2"]


def to_html(text):
    blocks = []
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if p:
            blocks.append("<p>" + p.replace("\n", " ") + "</p>")
    return "\n".join(blocks)


def parse(md):
    parts = re.split(r"(?m)^## 第 (\d+) 題\s*$", md)
    out = {}
    for i in range(1, len(parts), 2):
        qno = parts[i]
        body = parts[i + 1].strip()
        if body:
            out[qno] = body
    return out


def main():
    src_dir = pathlib.Path(sys.argv[1])
    years = sys.argv[2:] or ["2015", "2018", "2020", "2021", "2022", "2023", "2024", "2025"]
    src = DATA.read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    have = {(str(q["year"]), q["paper"], str(q["qno"]), q["type"]) for q in data["questions"]}

    added = 0
    for y in years:
        f = src_dir / f"{y}_P1_題目英文卷.md"
        if not f.exists():
            print(f"{y}: 冇檔"); continue
        qs = parse(f.read_text(encoding="utf-8"))
        n = 0
        for qno, body in qs.items():
            key = (y, "Paper 2M", qno, "題目")
            if key in have:
                continue
            data["questions"].append({
                "subject": "數學", "year": y, "paper": "Paper 2M", "type": "題目",
                "qno": int(qno), "title": f"第 {qno} 題", "section": "M2",
                "tags": tags_for(body), "text": body, "html": to_html(body),
                "file": f.name,
            })
            have.add(key)
            added += 1
            n += 1
        print(f"{y}: {n} 題")
    data["count"] = len(data["questions"])
    DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print("total", data["count"], "added", added)


if __name__ == "__main__":
    main()
