#!/usr/bin/env python3
"""匯入 Jensen 的 <year>_MS_split.md（分題評卷參考）→ data.js type=解答（覆蓋舊版）。"""
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
        p = p.replace("\n", "<br>")
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## 第 (\d+) 題.*$", raw)
    out = {}
    for i in range(1, len(parts), 2):
        qno = parts[i]
        body = re.sub(r"(?m)^<!--.*?-->\s*$", "", parts[i + 1]).strip()
        if body:
            out[qno] = body
    return out


def main():
    src_dir = pathlib.Path(sys.argv[1])
    src = DATA.read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    idx = {(q["year"], q["paper"], str(q["qno"]), q["type"]): i for i, q in enumerate(data["questions"])}

    added = updated = 0
    for f in sorted(src_dir.glob("*_MS_split.md")):
        year = f.name[:4]
        qs = parse(f)
        for qno, body in qs.items():
            key = (year, "Paper 1M", qno, "解答")
            entry = {
                "subject": "數學", "year": year, "paper": "Paper 1M", "type": "解答",
                "qno": int(qno), "title": f"第 {qno} 題 評卷參考", "section": "M1",
                "tags": ["評卷參考"], "text": body, "html": to_html(body), "file": f.name,
            }
            if key in idx:
                data["questions"][idx[key]] = entry
                updated += 1
            else:
                data["questions"].append(entry)
                added += 1
        print(f"{year}: {len(qs)} 題")

    data["count"] = len(data["questions"])
    DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print(f"added {added}, updated {updated}, total {data['count']}")


if __name__ == "__main__":
    main()
