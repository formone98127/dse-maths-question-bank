# -*- coding: utf-8 -*-
"""Build skill maps for every math paper in docs/data.js.

Strategy:
  1. Prefer Chinese 題目 rows; dedupe by (year, paper, qno).
  2. Map tags → topic via math_tag_crosswalk.json.
  3. Heuristic knowledge points / formulas from tag + question text keywords.
  4. If docs/analysis/.../qN.json has skills, use that (richer; includes option_faults).
  5. Write per-paper maps + INDEX under docs/skills/maps/.

Paper 1 long questions get topic/KP maps (no option_faults).
Paper 2 without LLM analysis get tag-based skills (source=tag).
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BOOK = json.loads((DOCS / "skills/math_skill_book.json").read_text(encoding="utf-8"))
CROSS = json.loads((DOCS / "skills/math_tag_crosswalk.json").read_text(encoding="utf-8"))["map"]
ANALYSIS = DOCS / "analysis" / "math"
OUT_DIR = DOCS / "skills" / "maps"

PAPER_CODE = {
    "Paper 1": "paper-1",
    "Paper 2": "paper-2",
    "Paper 1M": "paper-1m",
    "卷一": "paper-1",
    "卷二": "paper-2",
}

topics = {t["id"]: t for t in BOOK["topics"]}
topic_name = {t["id"]: t["name"] for t in BOOK["topics"]}
kps = {k["id"]: {**k, "tid": t["id"]} for t in BOOK["topics"] for k in t["knowledge_points"]}
formulas = {f["id"]: {**f, "tid": t["id"]} for t in BOOK["topics"] for f in t["formulas"]}
abilities = {a["id"]: a["name"] for a in BOOK["abilities"]}
CAT_ZH = {
    "Conceptual": "概念",
    "Calculation": "計算",
    "Reading-Formatting": "睇題",
    "Methodological": "方法",
}

# keyword → knowledge_point_id (checked against question text + tags)
KP_KEYWORDS: list[tuple[str, str]] = [
    ("指數", "K-EXP-01"),
    ("對數", "K-EXP-05"),
    ("百分", "K-PCT-01"),
    ("利息", "K-PCT-03"),
    ("比例", "K-RAT-04"),
    ("比、率", "K-RAT-01"),
    ("多項式", "K-POL-01"),
    ("因式", "K-POL-03"),
    ("餘式", "K-POL-04"),
    ("餘數", "K-POL-04"),
    ("展開", "K-POL-01"),
    ("方程", "K-EQN-01"),
    ("不等式", "K-EQN-05"),
    ("二次", "K-EQN-03"),
    ("判別", "K-EQN-04"),
    ("函數", "K-FUN-01"),
    ("頂點", "K-FUN-03"),
    ("平移", "K-FUN-04"),
    ("圖像", "K-FUN-05"),
    ("等差", "K-SEQ-02"),
    ("等比", "K-SEQ-03"),
    ("數列", "K-SEQ-01"),
    ("變分", "K-VAR-01"),
    ("正變", "K-VAR-01"),
    ("反變", "K-VAR-02"),
    ("三角", "K-TRI-01"),
    ("正弦", "K-TRI-04"),
    ("餘弦", "K-TRI-04"),
    ("弧度", "K-TRI-01"),
    ("面積", "K-MEN-01"),
    ("體積", "K-MEN-04"),
    ("扇形", "K-MEN-02"),
    ("弧長", "K-MEN-02"),
    ("斜率", "K-LIN-02"),
    ("直線", "K-LIN-03"),
    ("距離", "K-LIN-01"),
    ("圓", "K-CIR-01"),
    ("圓周角", "K-GEO-01"),
    ("切線", "K-GEO-02"),
    ("軌跡", "K-LOC-01"),
    ("旋轉", "K-TRF-03"),
    ("反射", "K-TRF-02"),
    ("極坐標", "K-TRF-04"),
    ("平均", "K-STA-01"),
    ("中位", "K-STA-02"),
    ("標準差", "K-STA-05"),
    ("方差", "K-STA-05"),
    ("概率", "K-PROB-01"),
    ("排列", "K-COM-02"),
    ("組合", "K-COM-03"),
    ("複數", "K-NUM-06"),
    ("有效數字", "K-NUM-04"),
    ("誤差", "K-NUM-05"),
    ("H.C.F", "K-NUM-02"),
    ("L.C.M", "K-NUM-02"),
    ("進位", "K-NUM-03"),
]


def load_questions():
    text = (DOCS / "data.js").read_text(encoding="utf-8")
    assign = text.index("=")
    data, _ = json.JSONDecoder().raw_decode(text[assign + 1 :].lstrip())
    return data["questions"]


def is_chinese_row(q: dict) -> bool:
    f = str(q.get("file") or "")
    if "英文" in f or "_en" in f.lower() or "English" in f:
        return False
    # prefer 中文 in filename; otherwise keep if text has CJK
    if "中文" in f:
        return True
    t = q.get("text") or ""
    return bool(re.search(r"[\u4e00-\u9fff]", t))


def paper_slug(paper: str) -> str:
    return PAPER_CODE.get(str(paper).strip(), re.sub(r"\W+", "-", str(paper).strip().lower()))


def analysis_path(year, paper, qno) -> Path:
    return ANALYSIS / str(year) / paper_slug(paper) / f"q{qno}.json"


def load_analysis_skills(year, paper, qno):
    p = analysis_path(year, paper, qno)
    if not p.is_file():
        return None, None
    doc = json.loads(p.read_text(encoding="utf-8"))
    return doc.get("skills"), doc.get("analysis")


def topic_from_tags(tags: list[str]) -> str | None:
    votes = Counter()
    for tag in tags or []:
        hit = CROSS.get(tag)
        if hit:
            votes[hit["topic_id"]] += 1
    if not votes:
        return None
    return votes.most_common(1)[0][0]


def infer_kps(topic_id: str | None, tags: list[str], text: str) -> list[str]:
    blob = " ".join(tags or []) + "\n" + (text or "")
    found = []
    for kw, kid in KP_KEYWORDS:
        if kw in blob and kid in kps:
            if topic_id is None or kps[kid]["tid"] == topic_id or True:
                # allow cross-topic KP if keyword hits
                if kid not in found:
                    found.append(kid)
    if topic_id and not found:
        # fallback: first 1–2 KPs of topic
        t = topics.get(topic_id)
        if t:
            found = [k["id"] for k in t["knowledge_points"][:2]]
    # prefer KPs in primary topic, then others; cap 3
    if topic_id:
        primary = [k for k in found if kps[k]["tid"] == topic_id]
        other = [k for k in found if kps[k]["tid"] != topic_id]
        found = (primary + other)[:3]
    else:
        found = found[:3]
    return found


def infer_formulas(kp_ids: list[str]) -> list[str]:
    out = []
    for f in BOOK["topics"]:
        for form in f["formulas"]:
            if form["knowledge_point_id"] in kp_ids and form["id"] not in out:
                out.append(form["id"])
    return out[:4]


def infer_abilities(topic_id: str | None, text: str) -> list[str]:
    ab = ["A-ALG"]
    t = text or ""
    if any(x in t for x in ["圖", "圖像", "斜", "頂點", "幹葉", "框線"]):
        ab.append("A-GRAPH")
    if any(x in t for x in ["求", "計算", "化簡", "解"]):
        ab.append("A-CALC")
    if any(x in t for x in ["若", "當", "非零", "正", "單位"]):
        ab.append("A-COND")
    # uniq preserve
    seen = []
    for a in ab:
        if a not in seen:
            seen.append(a)
    return seen[:3]


def bar(n, total, width=14):
    if not total:
        return "░" * width
    filled = round(width * n / total)
    return "█" * filled + "░" * (width - filled)


def collect_unique_math_questions(questions):
    """Return list of unique (year, paper, qno) question dicts; Chinese preferred."""
    best = {}
    for q in questions:
        if q.get("subject") != "數學" or q.get("type") != "題目":
            continue
        year, paper, qno = str(q.get("year")), str(q.get("paper")), str(q.get("qno"))
        key = (year, paper, qno)
        zh = is_chinese_row(q)
        if key not in best:
            best[key] = (zh, q)
        else:
            old_zh, _ = best[key]
            if zh and not old_zh:
                best[key] = (zh, q)
    rows = [q for _, q in best.values()]
    rows.sort(
        key=lambda q: (
            str(q.get("year")),
            str(q.get("paper")),
            int(re.sub(r"\D", "", str(q.get("qno"))) or 0),
        )
    )
    return rows


def skills_for_question(q: dict) -> dict:
    year, paper, qno = q["year"], q["paper"], q["qno"]
    rich, analysis = load_analysis_skills(year, paper, qno)
    if rich:
        return {
            "source": "analysis",
            "skills": rich,
            "analysis": analysis,
            "bloom": (analysis or {}).get("metadata", {}).get("bloom_taxonomy_level"),
            "secs": (analysis or {}).get("metadata", {}).get("estimated_time_seconds"),
        }
    tags = q.get("tags") or []
    tid = topic_from_tags(tags)
    kplist = infer_kps(tid, tags, q.get("text") or "")
    if not tid and kplist:
        tid = kps[kplist[0]]["tid"]
    if not tid:
        tid = "T-EQN"  # last resort bucket
        kplist = infer_kps(tid, tags, q.get("text") or "") or ["K-EQN-01"]
    skills = {
        "topic_id": tid,
        "knowledge_point_ids": kplist,
        "formula_ids": infer_formulas(kplist),
        "ability_ids": infer_abilities(tid, q.get("text") or ""),
        "option_faults": {},
    }
    return {"source": "tag", "skills": skills, "analysis": None, "bloom": None, "secs": None}


def write_paper_map(year: str, paper: str, items: list[dict]) -> Path:
    n = len(items)
    topic_c = Counter(topic_name[it["skills"]["topic_id"]] for it in items)
    kp_c = Counter(
        kps[kid]["name"] for it in items for kid in it["skills"]["knowledge_point_ids"]
    )
    f_c = Counter(
        formulas[fid]["name"] for it in items for fid in it["skills"]["formula_ids"]
    )
    ab_c = Counter(
        abilities[aid] for it in items for aid in it["skills"]["ability_ids"]
    )
    fault_ab = Counter()
    fault_kp = Counter()
    err_c = Counter()
    rich_n = sum(1 for it in items if it["source"] == "analysis")
    for it in items:
        faults = it["skills"].get("option_faults") or {}
        oa = ((it.get("analysis") or {}).get("options_analysis")) or {}
        for opt, f in faults.items():
            fault_ab[abilities[f["ability_id"]]] += 1
            if f.get("knowledge_point_id"):
                fault_kp[kps[f["knowledge_point_id"]]["name"]] += 1
            if opt in oa and oa[opt].get("error_category"):
                err_c[CAT_ZH.get(oa[opt]["error_category"], oa[opt]["error_category"])] += 1

    slug = paper_slug(paper)
    path = OUT_DIR / f"math-{year}-{slug}.md"
    lines = []
    a = lines.append
    a(f"# {year} 數學 {paper} · 技能地圖")
    a("")
    a(f"- 題數：**{n}**")
    a(f"- 深度分析掛鉤（含錯選項原因）：**{rich_n}**")
    a(f"- 標籤推斷掛鉤：**{n - rich_n}**")
    a("")
    if rich_n == 0:
        a("> 本卷暫時以題庫課題標籤對照技能冊。錯選項陷阱細節會隨 LLM 分析補上。")
        a("")
    a("## 課題分佈")
    a("")
    a("| 題數 | 課題 | |")
    a("|---:|---|---|")
    top = topic_c.most_common(1)[0][1] if topic_c else 1
    for name, c in topic_c.most_common():
        a(f"| {c} | {name} | `{bar(c, top)}` |")
    a("")
    a("## 知識點（Top 15）")
    a("")
    a("| 題數提及 | 知識點 |")
    a("|---:|---|")
    for name, c in kp_c.most_common(15):
        a(f"| {c} | {name} |")
    a("")
    a("## 公式（Top 12）")
    a("")
    a("| 題數提及 | 公式 |")
    a("|---:|---|")
    for name, c in f_c.most_common(12):
        a(f"| {c} | {name} |")
    a("")
    a("## 能力（成題標明）")
    a("")
    a("| 題數提及 | 能力 |")
    a("|---:|---|")
    for name, c in ab_c.most_common():
        a(f"| {c} | {name} |")
    a("")
    if fault_ab:
        a("## 錯選項陷阱（僅深度分析題）")
        a("")
        a("| 次數 | 能力 |")
        a("|---:|---|")
        for name, c in fault_ab.most_common():
            a(f"| {c} | {name} |")
        a("")
        if fault_kp:
            a("| 次數 | 知識點 |")
            a("|---:|---|")
            for name, c in fault_kp.most_common(12):
                a(f"| {c} | {name} |")
            a("")
        if err_c:
            a("| 次數 | 錯誤類型 |")
            a("|---:|---|")
            for name, c in err_c.most_common():
                a(f"| {c} | {name} |")
            a("")
    a("## 逐題")
    a("")
    a("| 題 | 來源 | 課題 | 知識點 | 能力 |")
    a("|---:|---|---|---|---|")
    for it in items:
        s = it["skills"]
        src = "分析" if it["source"] == "analysis" else "標籤"
        kp = "、".join(kps[x]["name"] for x in s["knowledge_point_ids"])
        ab = "、".join(abilities[x] for x in s["ability_ids"])
        a(f"| {it['qno']} | {src} | {topic_name[s['topic_id']]} | {kp} | {ab} |")
    a("")
    a("---")
    a("")
    a("產生：`python scripts/build_all_math_skill_maps.py`")
    a("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_index(papers: list[dict], all_items: list[dict]):
    topic_c = Counter(topic_name[it["skills"]["topic_id"]] for it in all_items)
    kp_c = Counter(
        kps[kid]["name"] for it in all_items for kid in it["skills"]["knowledge_point_ids"]
    )
    rich = sum(1 for it in all_items if it["source"] == "analysis")
    lines = []
    a = lines.append
    a("# 數學技能地圖總目錄")
    a("")
    a(f"- 卷數：**{len(papers)}**")
    a(f"- 題數（去重中文優先）：**{len(all_items)}**")
    a(f"- 已有深度分析 skills：**{rich}**")
    a(f"- 標籤推斷：**{len(all_items) - rich}**")
    a("")
    a("## 各卷")
    a("")
    a("| 年份 | 卷 | 題數 | 深度分析 | 地圖 |")
    a("|---|---|---:|---:|---|")
    for p in papers:
        link = f"[打開](./{p['file']})"
        a(f"| {p['year']} | {p['paper']} | {p['n']} | {p['rich']} | {link} |")
    a("")
    a("## 全庫課題分佈")
    a("")
    a("| 題數 | 課題 |")
    a("|---:|---|")
    for name, c in topic_c.most_common():
        a(f"| {c} | {name} |")
    a("")
    a("## 全庫知識點 Top 20")
    a("")
    a("| 題數提及 | 知識點 |")
    a("|---:|---|")
    for name, c in kp_c.most_common(20):
        a(f"| {c} | {name} |")
    a("")
    a("---")
    a("")
    a("產生：`python scripts/build_all_math_skill_maps.py`")
    a("")
    (OUT_DIR / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    # machine-readable summary
    summary = {
        "version": 1,
        "papers": papers,
        "totals": {
            "questions": len(all_items),
            "rich_analysis": rich,
            "tag_inferred": len(all_items) - rich,
        },
        "topics": topic_c.most_common(),
        "knowledge_points": kp_c.most_common(50),
    }
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    questions = load_questions()
    uniq = collect_unique_math_questions(questions)
    by_paper: dict[tuple[str, str], list] = defaultdict(list)
    all_items = []
    for q in uniq:
        packed = skills_for_question(q)
        item = {
            "year": str(q["year"]),
            "paper": str(q["paper"]),
            "qno": str(q["qno"]),
            **packed,
        }
        by_paper[(item["year"], item["paper"])].append(item)
        all_items.append(item)

    papers_meta = []
    for (year, paper), items in sorted(by_paper.items(), key=lambda x: (x[0][0], x[0][1])):
        items.sort(key=lambda it: int(re.sub(r"\D", "", it["qno"]) or 0))
        path = write_paper_map(year, paper, items)
        rich = sum(1 for it in items if it["source"] == "analysis")
        papers_meta.append(
            {
                "year": year,
                "paper": paper,
                "n": len(items),
                "rich": rich,
                "file": path.name,
            }
        )
        print(f"wrote {path.relative_to(ROOT)} ({len(items)} q, rich={rich})")

    write_index(papers_meta, all_items)
    print(f"wrote { (OUT_DIR / 'INDEX.md').relative_to(ROOT) }")
    print(f"papers={len(papers_meta)} questions={len(all_items)}")


if __name__ == "__main__":
    main()
