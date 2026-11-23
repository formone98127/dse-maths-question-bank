# -*- coding: utf-8 -*-
"""Export human-readable Markdown from math skill book + tag crosswalk."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "docs" / "skills"


def export_book() -> Path:
    book = json.loads((SKILLS / "math_skill_book.json").read_text(encoding="utf-8"))
    lines = [
        "# 數學技能冊（必修部分）",
        "",
        "所有題目分析只准用本冊編號。唔准自由另起課題／公式名。",
        "",
        f"版本：{book.get('version', 1)}　"
        f"課題 {len(book['topics'])}　"
        f"知識點 {sum(len(t['knowledge_points']) for t in book['topics'])}　"
        f"公式 {sum(len(t['formulas']) for t in book['topics'])}　"
        f"能力 {len(book['abilities'])}",
        "",
        "## 能力（全科共用 8 種）",
        "",
    ]
    for a in book["abilities"]:
        lines.append(f"- `{a['id']}` **{a['name']}** — {a.get('desc', '')}")
    lines += ["", "## 課題／知識點／公式", ""]
    for t in book["topics"]:
        lines.append(f"### `{t['id']}` {t['name']}（{t.get('group', '')}）")
        lines.append("")
        lines.append("**知識點**")
        lines.append("")
        for k in t["knowledge_points"]:
            pr = ", ".join(f"`{p}`" for p in (k.get("prereqs") or [])) or "—"
            lines.append(f"- `{k['id']}` {k['name']}（先備：{pr}）")
        lines.append("")
        lines.append("**公式**")
        lines.append("")
        for f in t["formulas"]:
            lines.append(
                f"- `{f['id']}` {f['name']}：`${f['latex']}$"
                f"（知識點 `{f['knowledge_point_id']}`）"
            )
        lines.append("")
    out = SKILLS / "math_skill_book.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def export_crosswalk() -> Path:
    cw = json.loads((SKILLS / "math_tag_crosswalk.json").read_text(encoding="utf-8"))
    lines = [
        "# 題庫標籤 → 技能冊課題對照",
        "",
        cw.get("note") or "題庫 tags 對照到技能冊 20 課題；不改網站既有 tag 字串。",
        "",
        f"共 {len(cw.get('map') or {})} 條。",
        "",
        "| 題庫 tag（網站不變） | 技能冊課題 | topic_id |",
        "|---|---|---|",
    ]
    for tag, hit in sorted((cw.get("map") or {}).items(), key=lambda x: (x[1].get("topic_id", ""), x[0])):
        lines.append(
            f"| {tag} | {hit.get('topic_name', '')} | `{hit.get('topic_id', '')}` |"
        )
    lines.append("")
    out = SKILLS / "math_tag_crosswalk.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main():
    b = export_book()
    c = export_crosswalk()
    print(f"wrote {b.relative_to(ROOT)}")
    print(f"wrote {c.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
