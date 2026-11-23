#!/usr/bin/env python3
"""M1 評卷參考（解答 md，表格形式）→ data.js 每題一條 type=解答 entry。

用法：python3 scripts/import_m1_ms.py <md_dir> [years...]
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DATA = REPO / "docs/data.js"


def split_rows(md_text):
    rows = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r"^\|?\s*[-:| ]+\|?\s*$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in ("Solution", "Marks", "Remarks") or cells[1] == "Marks":
            continue
        rows.append(cells[:3])
    return rows


def group_by_qno(rows):
    groups = {}
    cur = None
    for sol, marks, rem in rows:
        m = re.match(r"^(\d{1,2})\s*[\.\)]", sol)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 20:
                cur = n
                groups.setdefault(cur, [])
        if cur is None:
            continue
        groups[cur].append((sol, marks, rem))
    return groups


def build_html(rows):
    body = "".join(
        f"<tr><td>{sol}</td><td>{marks}</td><td>{rem}</td></tr>" for sol, marks, rem in rows
    )
    return ("<table><thead><tr><th>Solution</th><th>Marks</th><th>Remarks</th></tr></thead>"
            f"<tbody>{body}</tbody></table>")


def main():
    md_dir = pathlib.Path(sys.argv[1])
    years = sys.argv[2:] or [str(y) for y in range(2012, 2026)]

    src = DATA.read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    have = {(str(q["year"]), q["paper"], str(q["qno"]), q["type"]) for q in data["questions"]}

    added = 0
    for y in years:
        p = md_dir / f"{y}_P1_解答英文卷.md"
        if not p.exists():
            print(f"skip {y}: 冇 {p.name}")
            continue
        rows = split_rows(p.read_text(encoding="utf-8"))
        groups = group_by_qno(rows)
        n = 0
        for qno, rws in sorted(groups.items()):
            key = (y, "Paper 1M", str(qno), "解答")
            if key in have:
                continue
            text = "\n".join(f"{a} | {b} | {c}" for a, b, c in rws)
            data["questions"].append({
                "subject": "數學", "year": y, "paper": "Paper 1M", "type": "解答",
                "qno": qno, "title": f"第 {qno} 題 評卷參考", "section": "M1",
                "tags": ["評卷參考"],
                "text": text, "html": build_html(rws), "file": p.name,
            })
            have.add(key)
            added += 1
            n += 1
        print(f"{y}: 解答 {n} 題（表格 rows={len(rows)}）")

    data["count"] = len(data["questions"])
    DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print("total:", data["count"], "added 解答:", added)


if __name__ == "__main__":
    main()
