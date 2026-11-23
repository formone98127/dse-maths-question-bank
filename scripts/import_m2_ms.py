#!/usr/bin/env python3
"""匯入 M2 評卷參考（<year>_MS_split.md）→ docs/data.js（type=解答、paper=Paper 2M）。"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DATA = REPO / "docs/data.js"


def to_html(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if not p:
            continue
        if p.startswith("Subtotals:") or p.startswith("Marks:"):
            out.append(f'<p class="ms-meta">{p}</p>')
        else:
            out.append("<p>" + p.replace("\n", " ") + "</p>")
    return "\n".join(out)


def main():
    src = pathlib.Path(sys.argv[1])
    year = sys.argv[2] if len(sys.argv) > 2 else (re.match(r"(\d{4})", src.name).group(1) if re.match(r"(\d{4})", src.name) else "2025")
    md = src.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^## 第 (\d+) 題[^\n]*$", md)
    src_json = DATA.read_text(encoding="utf-8")
    data = json.loads(src_json[src_json.index("{"): src_json.rindex("}") + 1])
    idx = {(str(q["year"]), q["paper"], str(q["qno"]), q["type"]): i for i, q in enumerate(data["questions"])}

    added = upd = 0
    for i in range(1, len(blocks), 2):
        qno = int(blocks[i])
        body = blocks[i + 1].strip()
        body = re.sub(r"(?m)^\s*##\s*第\s+\d+\s*題.*$", "", body).strip()
        if len(body) < 40:
            continue
        key = (year, "Paper 2M", str(qno), "解答")
        entry = {
            "subject": "數學", "year": year, "paper": "Paper 2M", "type": "解答",
            "qno": qno, "title": f"第 {qno} 題（評卷參考）", "section": "M2",
            "tags": ["M2"], "text": body, "html": to_html(body), "file": src.name,
        }
        if key in idx:
            data["questions"][idx[key]] = entry
            upd += 1
        else:
            data["questions"].append(entry)
            added += 1
    data["count"] = len(data["questions"])
    DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print(f"{year}: 新增 {added}、更新 {upd}、總數 {data['count']}")


if __name__ == "__main__":
    main()
