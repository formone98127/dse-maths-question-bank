#!/usr/bin/env python3
"""把技能卡（docs/skills/math_question_cards.json）注入逐題頁，並生成 /skills/ 索引。

用法：python3 scripts/inject_skill_cards.py [--write]
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DOCS = REPO / "docs"
SK = DOCS / "skills"
START = "<!-- SKILL-CARD:START -->"
END = "<!-- SKILL-CARD:END -->"

CSS = """<style>
.skill-card{margin:18px 0;border:1px solid #d9e6df;background:#f6fbf8;border-radius:10px;padding:14px 16px}
.skill-card h2{font-size:15px;margin:0 0 8px;color:#1d6b45}
.skill-card dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:0;font-size:14px}
.skill-card dt{color:#5b6b63;white-space:nowrap}
.skill-card dd{margin:0}
.skill-card .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.skill-card .tag{background:#e3f2ea;border:1px solid #c3e0d0;border-radius:999px;padding:3px 9px;font-size:13px;color:#1d6b45}
.skill-card table{border-collapse:collapse;margin-top:10px;font-size:13px;width:100%}
.skill-card td,.skill-card th{border:1px solid #d9e6df;padding:5px 8px;text-align:left}
</style>"""


def build_maps():
    book = json.loads((SK / "math_skill_book.json").read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in book["topics"]}
    kp = {}
    formula = {}
    for t in book["topics"]:
        for k in t.get("knowledge_points", []):
            kp[k["id"]] = k["name"]
        for f in t.get("formulas", []):
            formula[f["id"]] = f.get("name", f["id"])
    abilities = {a["id"]: a["name"] for a in book["abilities"]}
    return topics, kp, formula, abilities


def card_html(card, topics, kp, formula, abilities, err_tags):
    parts = []
    prim = card.get("primary_hub_topic") or {}
    if prim:
        parts.append(f"<dt>主課題</dt><dd>{prim.get('topic_name','')}</dd>")
    ht = [t["topic_name"] for t in card.get("hub_topics") or []]
    if len(ht) > 1:
        parts.append("<dt>相關課題</dt><dd>" + "、".join(ht) + "</dd>")
    if card.get("answer_pct") is not None:
        parts.append(f"<dt>全港答對率</dt><dd>{card['answer_pct']}%</dd>")
    if card.get("answer"):
        parts.append(f"<dt>官方答案</dt><dd>{card['answer']}</dd>")

    sk = card.get("skills") or {}
    kps = [kp.get(x, x) for x in sk.get("knowledge_point_ids") or []]
    fs = [formula.get(x, x) for x in sk.get("formula_ids") or []]
    ab = [abilities.get(x, x) for x in sk.get("ability_ids") or []]
    if kps:
        parts.append("<dt>知識點</dt><dd>" + "、".join(kps) + "</dd>")
    if fs:
        parts.append("<dt>公式</dt><dd>" + "、".join(fs) + "</dd>")
    if ab:
        parts.append("<dt>用到能力</dt><dd>" + "、".join(ab) + "</dd>")

    rows = []
    for opt, fault in (sk.get("option_faults") or {}).items():
        r = []
        if fault.get("ability_id"):
            r.append(abilities.get(fault["ability_id"], fault["ability_id"]))
        if fault.get("knowledge_point_id"):
            r.append(kp.get(fault["knowledge_point_id"], fault["knowledge_point_id"]))
        if fault.get("formula_id"):
            r.append(formula.get(fault["formula_id"], fault["formula_id"]))
        if r:
            rows.append((opt, "／".join(r)))
    table = ""
    if rows:
        body = "".join(f"<tr><td>{o}</td><td>{d}</td></tr>" for o, d in rows)
        table = ("<table><thead><tr><th>錯選項</th><th>陷阱（能力／知識點）</th></tr></thead>"
                 f"<tbody>{body}</tbody></table>")

    tags = [x for x in (card.get("bank_tags") or []) if x]
    taghtml = ""
    if tags:
        taghtml = '<div class="tags">' + "".join(f'<span class="tag">{t}</span>' for t in tags[:8]) + "</div>"

    return (f"{START}{CSS}<section class=\"skill-card\"><h2>技能分析（呢題考咩、陷阱喺邊）</h2>"
            f"<dl>{''.join(parts)}</dl>{taghtml}{table}</section>{END}")


def main():
    write = "--write" in sys.argv
    topics, kp, formula, abilities = build_maps()
    err_tags = {}
    p = SK / "math_error_tags.json"
    if p.exists():
        raw = json.loads(p.read_text(encoding="utf-8"))
        err_tags = raw if isinstance(raw, dict) else {}
    cards = {c["id"]: c for c in json.loads((SK / "math_question_cards.json").read_text(encoding="utf-8"))["cards"]}

    n = 0
    for page in sorted((DOCS / "questions/math").rglob("q*/index.html")):
        parts = page.parts
        try:
            i = parts.index("math")
            year, paper_slug, qslug = parts[i + 1], parts[i + 2], parts[i + 3]
        except (ValueError, IndexError):
            continue
        paper = paper_slug.replace("paper-", "")
        cid = f"math-{year}-p{paper}-q{qslug[1:]}"
        card = cards.get(cid)
        if not card:
            continue
        block = card_html(card, topics, kp, formula, abilities, err_tags)
        html = page.read_text(encoding="utf-8")
        if START in html:
            html = re.sub(re.escape(START) + r".*?" + re.escape(END), block, html, flags=re.S)
        else:
            html = html.replace("</main>", block + "\n</main>", 1)
        if write:
            page.write_text(html, encoding="utf-8")
        n += 1
    print(f"{'[dry]' if not write else ''} skill cards injected: {n}")


if __name__ == "__main__":
    main()
