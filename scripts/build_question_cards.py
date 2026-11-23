# -*- coding: utf-8 -*-
"""Build unified math question cards + short error-tag catalog.

Sources (read-only merge):
  - docs/data.js                 (題目正文、tags、answer、answer_pct、report)
  - docs/questions/_index.json   (逐題頁 URL、langs、has_solution/report)
  - docs/questions/math/**/q*/index.html  (錯項分析、考評報告 HTML)
  - docs/analysis/math/**/q*.json (error_tag、skills、公式／時間)
  - docs/skills/math_tag_crosswalk.json
  - docs/skills/math_skill_book.json

Outputs:
  - docs/skills/math_question_cards.json
  - docs/skills/math_error_tags.json
  - docs/skills/math_cards_index.json

Usage:
  python scripts/build_question_cards.py
  python scripts/build_question_cards.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "docs" / "skills"
DATA_JS = ROOT / "docs" / "data.js"
INDEX_JSON = ROOT / "docs" / "questions" / "_index.json"
QUESTIONS_DIR = ROOT / "docs" / "questions" / "math"
ANALYSIS_DIR = ROOT / "docs" / "analysis" / "math"
CROSSWALK_PATH = SKILLS / "math_tag_crosswalk.json"
BOOK_PATH = SKILLS / "math_skill_book.json"

# ---------------------------------------------------------------------------
# Controlled short error tags (Chinese labels students can search)
# Each rule: (regex, tag). First matches win; multiple rules may fire.
# ---------------------------------------------------------------------------
ERROR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"負號|丟掉.*負|負.*丟|當成\s*\+|把\s*-?\s*當"), "負號丟掉"),
    (re.compile(r"符號.*反|取反|正負搞|方向搞反|不等號方向|方向錯誤"), "符號顛倒"),
    (re.compile(r"指數.*加|加指數|指數相加|相加.*指數|當成.*相加"), "指數加減混淆"),
    (re.compile(r"指數.*乘|相乘.*指數|冪的冪|外層冪|指數定律"), "指數相乘誤用"),
    (re.compile(r"係數"), "係數運算錯誤"),
    (re.compile(r"單利|複利|再生息|期數與|利率.*錯|每期利率"), "單複利混淆"),
    (re.compile(r"比例.*倒|順序倒|倒轉|次序"), "比例次序倒轉"),
    (re.compile(r"漏掉?條件|忽略|未考慮|漏讀|誤讀題|條件.*錯"), "條件漏讀"),
    (re.compile(r"單位"), "單位未統一"),
    (re.compile(r"未代|代錯|代入.*錯|直接把.+當答案|沒有化成"), "代入錯誤"),
    (re.compile(r"計算|口算|算成|偏大|偏小|粗心|算錯"), "計算粗心"),
    (re.compile(r"公式|誤用.*定理|定理|法則誤"), "公式／定理誤用"),
    (re.compile(r"讀圖|圖像|斜率|截距|頂點|平移"), "讀圖／圖像錯誤"),
    (re.compile(r"放回|不放回"), "放回條件混淆"),
    (re.compile(r"至少|補集"), "至少／補集誤用"),
    (re.compile(r"百分|基數|折扣|利潤率"), "百分基數錯"),
    (re.compile(r"定義混淆|混淆|誤認|誤判|誤當|誤以"), "定義／概念混淆"),
    (re.compile(r"漏情況|漏驗|外來根|定義域|非零"), "漏驗根／定義域"),
    (re.compile(r"圓周角|圓心角|切線|相似|全等|幾何"), "幾何關係誤用"),
    (re.compile(r"排列|組合|P\^|C\^|方法數"), "排列組合誤用"),
    (re.compile(r"只作用|漏乘|漏了|當成\s*3\^1|外層.*漏"), "指數作用範圍錯"),
]

TAG_IDS = {
    "負號丟掉": "E-SIGN-DROP",
    "符號顛倒": "E-SIGN-FLIP",
    "指數加減混淆": "E-INDEX-ADD",
    "指數相乘誤用": "E-INDEX-MUL",
    "係數運算錯誤": "E-COEFF",
    "單複利混淆": "E-INTEREST",
    "比例次序倒轉": "E-ORDER",
    "條件漏讀": "E-COND",
    "單位未統一": "E-UNIT",
    "代入錯誤": "E-SUB",
    "計算粗心": "E-CALC",
    "公式／定理誤用": "E-FORMULA",
    "讀圖／圖像錯誤": "E-GRAPH",
    "放回條件混淆": "E-REPLACE",
    "至少／補集誤用": "E-COMPLEMENT",
    "百分基數錯": "E-PCT-BASE",
    "定義／概念混淆": "E-DEF",
    "漏驗根／定義域": "E-DOMAIN",
    "幾何關係誤用": "E-GEOM",
    "排列組合誤用": "E-PERM",
    "指數作用範圍錯": "E-INDEX-SCOPE",
    "其他": "E-OTHER",
}


def load_qb() -> list[dict]:
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.QB\s*=\s*(\{.*\})", text, re.S)
    if not m:
        raise SystemExit(f"cannot parse {DATA_JS}")
    return json.loads(m.group(1))["questions"]


def paper_key(paper: str) -> str:
    """Paper 2 → 2；Paper 1M → 1m。"""
    s = str(paper).strip()
    m = re.search(r"(\d+[A-Za-z]?)", s)
    return (m.group(1) if m else s).lower()


def card_id(year, paper, qno) -> str:
    return f"math-{year}-p{paper_key(paper)}-q{qno}"


def is_chinese_entry(q: dict) -> bool:
    f = str(q.get("file") or "")
    return "中文" in f or "CHI" in f.upper() or "zh" in f.lower()


def strip_html(s: str) -> str:
    s = unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tag_error_text(text: str) -> list[str]:
    if not text:
        return []
    hits = []
    for rx, tag in ERROR_RULES:
        if rx.search(text):
            hits.append(tag)
    if not hits:
        hits.append("其他")
    # stable unique, keep rule order
    seen = set()
    out = []
    for t in hits:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def normalize_analysis_tag(raw: str | None) -> list[str]:
    if not raw:
        return []
    tagged = tag_error_text(raw)
    if tagged != ["其他"]:
        return tagged
    # keep a short cleaned original as searchable label
    clean = re.sub(r"\s+", "", raw)
    clean = re.sub(r"[（(].*?[）)]", "", clean)
    if len(clean) > 16:
        clean = clean[:16]
    return [clean or "其他"]


def parse_distractors_from_html(html: str) -> list[dict]:
    """Parse <b>A.</b> … bullets under 錯項分析."""
    m = re.search(r"錯項分析[:：]</b></p>\s*<ul>(.*?)</ul>", html, re.S)
    if not m:
        m = re.search(r"<p><b>錯項分析[:：]</b></p>\s*<ul>(.*?)</ul>", html, re.S)
    if not m:
        # JSON-LD fallback: 錯項分析： A. … B. …
        m2 = re.search(r"錯項分析[:：]\s*(.+?)(?:\"\s*,\s*\"upvoteCount|/p>)", html, re.S)
        if not m2:
            return []
        blob = strip_html(m2.group(1))
        parts = re.split(r"(?=[A-D]\.\s)", blob)
        out = []
        for part in parts:
            mm = re.match(r"([A-D])\.\s*(.+)", part.strip(), re.S)
            if not mm:
                continue
            detail = mm.group(2).strip()
            out.append(
                {
                    "option": mm.group(1),
                    "error_tags": tag_error_text(detail),
                    "detail": detail,
                    "source": "html-jsonld",
                }
            )
        return out

    out = []
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
        plain = strip_html(li)
        mm = re.match(r"([A-D])\.\s*(.+)", plain, re.S)
        if not mm:
            continue
        detail = mm.group(2).strip()
        out.append(
            {
                "option": mm.group(1),
                "error_tags": tag_error_text(detail),
                "detail": detail,
                "source": "html",
            }
        )
    return out


def parse_report_from_html(html: str) -> str | None:
    m = re.search(r'<section[^>]*id="report"[^>]*>.*?<h2[^>]*>.*?</h2>\s*(.*?)</section>', html, re.S)
    if not m:
        return None
    text = strip_html(m.group(1))
    return text or None


def report_error_tags(report: str | None) -> list[dict]:
    if not report:
        return []
    items = []
    # 「誤以 X 作為答案」「錯誤地…」「誤把…」
    for m in re.finditer(r"(誤以|錯誤地|誤把|誤用|誤認)([^。；;]{2,80})", report):
        detail = (m.group(1) + m.group(2)).strip()
        items.append(
            {
                "error_tags": tag_error_text(detail),
                "detail": detail,
                "source": "report",
            }
        )
    if not items and any(k in report for k in ("誤", "錯", "少数", "少數", "weak", "wrong")):
        items.append(
            {
                "error_tags": tag_error_text(report),
                "detail": report[:160],
                "source": "report",
            }
        )
    return items


def load_index() -> dict[tuple[str, str, str], dict]:
    if not INDEX_JSON.is_file():
        return {}
    rows = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    out = {}
    for r in rows:
        key = (str(r["year"]), paper_key(f"Paper {r['paper']}"), str(r["qno"]))
        out[key] = r
    return out


def load_analysis() -> dict[tuple[str, str, str], dict]:
    out = {}
    if not ANALYSIS_DIR.is_dir():
        return out
    for fp in ANALYSIS_DIR.rglob("q*.json"):
        # .../math/2012/paper-2/q1.json
        try:
            year = fp.parts[-3]
            paper = fp.parts[-2]  # paper-2
            qno = re.sub(r"\D", "", fp.stem)
            doc = json.loads(fp.read_text(encoding="utf-8"))
            pk = paper.replace("paper-", "")
            out[(str(year), pk, str(int(qno)))] = doc
        except (OSError, ValueError, IndexError, json.JSONDecodeError):
            continue
    return out


def html_path_for(year: str, paper: str, qno: str) -> Path | None:
    # prefer paper-2 / paper-1 under questions/math
    p = QUESTIONS_DIR / str(year) / f"paper-{paper_key(paper)}" / f"q{qno}" / "index.html"
    if p.is_file():
        return p
    return None


def merge_bank_entries(entries: list[dict]) -> dict:
    """Merge zh+en 題目 rows for one (year, paper, qno). Prefer Chinese fields."""
    zh = [e for e in entries if is_chinese_entry(e)]
    primary = (zh or entries)[0]
    tags: list[str] = []
    seen = set()
    answer = primary.get("answer")
    pct = primary.get("answer_pct")
    report = primary.get("report")
    text = primary.get("text")
    for e in zh + [e for e in entries if e not in zh]:
        for t in e.get("tags") or []:
            if t not in seen:
                seen.add(t)
                tags.append(t)
        if answer is None and e.get("answer"):
            answer = e.get("answer")
        if pct is None and e.get("answer_pct") is not None:
            pct = e.get("answer_pct")
        if not report and e.get("report"):
            report = e.get("report")
        if not text and e.get("text"):
            text = e.get("text")
    return {
        "year": str(primary["year"]),
        "paper": str(primary["paper"]),
        "qno": str(primary["qno"]),
        "section": primary.get("section") or "",
        "bank_tags": tags,
        "answer": answer,
        "answer_pct": pct,
        "report": report,
        "stem": text,
    }


def map_hub_topics(tags: list[str], crosswalk: dict) -> tuple[list[dict], dict | None, list[str]]:
    cmap = crosswalk.get("map") or {}
    hubs = []
    seen = set()
    unmapped = []
    for t in tags:
        hit = cmap.get(t)
        if not hit:
            unmapped.append(t)
            continue
        tid = hit["topic_id"]
        if tid in seen:
            continue
        seen.add(tid)
        hubs.append({"topic_id": tid, "topic_name": hit["topic_name"]})
    primary = hubs[0] if hubs else None
    return hubs, primary, unmapped


def build_cards() -> tuple[list[dict], dict, dict, dict]:
    crosswalk = json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))
    book = json.loads(BOOK_PATH.read_text(encoding="utf-8")) if BOOK_PATH.is_file() else {}
    topic_names = {t["id"]: t["name"] for t in book.get("topics") or []}

    qb = [q for q in load_qb() if q.get("subject") == "數學" and q.get("type") == "題目"]
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for q in qb:
        key = (str(q["year"]), paper_key(q["paper"]), str(q["qno"]))
        groups[key].append(q)

    index = load_index()
    analysis = load_analysis()

    cards = []
    unmapped_tag_counter = Counter()
    error_counter = Counter()
    error_examples: dict[str, list[str]] = defaultdict(list)

    for key in sorted(groups.keys(), key=lambda k: (k[0], k[1], int(re.sub(r"\D", "", k[2]) or 0))):
        year, pk, qno = key
        merged = merge_bank_entries(groups[key])
        hubs, primary, unmapped = map_hub_topics(merged["bank_tags"], crosswalk)
        for t in unmapped:
            unmapped_tag_counter[t] += 1

        idx = index.get(key)
        url = idx.get("url") if idx else None
        langs = idx.get("langs") if idx else None
        has_solution = bool(idx.get("has_solution")) if idx else False
        has_report = bool(idx.get("has_report")) if idx else bool(merged.get("report"))

        # prefer index answer/pct when present
        answer = merged["answer"]
        pct = merged["answer_pct"]
        if idx:
            if idx.get("answer"):
                answer = idx["answer"]
            if idx.get("answer_pct") is not None:
                pct = idx["answer_pct"]
            if idx.get("tags"):
                # keep bank_tags from merge; index tags already subset
                pass

        option_errors: list[dict] = []
        report_text = merged.get("report")
        html_p = html_path_for(year, pk, qno)
        if html_p:
            html = html_p.read_text(encoding="utf-8")
            option_errors = parse_distractors_from_html(html)
            html_report = parse_report_from_html(html)
            if html_report:
                report_text = html_report
                has_report = True
            if "mc-sol" in html or "官方題解" in html:
                has_solution = True

        an = analysis.get(key)
        skills = None
        formulas = None
        estimated_time = None
        if an:
            skills = an.get("skills")
            meta = (an.get("analysis") or {}).get("metadata") or {}
            formulas = meta.get("required_formulas")
            estimated_time = meta.get("estimated_time_seconds")
            oa = (an.get("analysis") or {}).get("options_analysis") or {}
            if not option_errors:
                for opt, payload in oa.items():
                    if not isinstance(payload, dict) or payload.get("is_correct"):
                        continue
                    raw_tag = payload.get("error_tag")
                    detail = payload.get("student_thought_process") or raw_tag or ""
                    if isinstance(detail, str) and len(detail) > 220:
                        detail = detail[:220] + "…"
                    option_errors.append(
                        {
                            "option": opt,
                            "error_tags": normalize_analysis_tag(raw_tag),
                            "detail": detail,
                            "source": "analysis",
                            "error_category": payload.get("error_category"),
                        }
                    )

        report_errors = report_error_tags(report_text)

        cid = card_id(year, f"Paper {pk}", qno)
        for oe in option_errors:
            for t in oe.get("error_tags") or []:
                error_counter[t] += 1
                if cid not in error_examples[t] and len(error_examples[t]) < 5:
                    error_examples[t].append(cid)
        for re_item in report_errors:
            for t in re_item.get("error_tags") or []:
                error_counter[t] += 1
                if cid not in error_examples[t] and len(error_examples[t]) < 5:
                    error_examples[t].append(cid)

        # resolve primary hub name from book if needed
        if primary and primary["topic_id"] in topic_names:
            primary = {
                "topic_id": primary["topic_id"],
                "topic_name": topic_names[primary["topic_id"]],
            }

        stream = "m1" if pk in ("1m", "1M") else "compulsory"
        card = {
            "id": card_id(year, f"Paper {pk}", qno),
            "subject": "math",
            "stream": stream,
            "year": year,
            "paper": pk,
            "qno": qno,
            "section": merged.get("section") or None,
            "url": url,
            "langs": langs,
            "stem": merged.get("stem"),
            "answer": answer,
            "answer_pct": pct,
            "bank_tags": merged["bank_tags"],
            "hub_topics": hubs,
            "primary_hub_topic": primary,
            "unmapped_tags": unmapped or None,
            "has_solution": has_solution,
            "has_report": has_report,
            "report": report_text,
            "option_errors": option_errors or None,
            "report_errors": report_errors or None,
            "required_formulas": formulas,
            "estimated_time_seconds": estimated_time,
            "skills": skills,
        }
        # drop null-ish noise for smaller file? keep explicit nulls for schema clarity — strip only empty unmapped
        if card["unmapped_tags"] is None:
            del card["unmapped_tags"]
        cards.append(card)

    catalog = {
        "version": 1,
        "generated": str(date.today()),
        "note": "錯法短標籤目錄；由 distractor／analysis／report 文字規則對上。",
        "tags": [
            {
                "id": TAG_IDS.get(name, "E-OTHER"),
                "name": name,
                "count": error_counter[name],
                "examples": error_examples.get(name, []),
            }
            for name in sorted(error_counter.keys(), key=lambda n: (-error_counter[n], n))
        ],
    }

    by_topic: dict[str, list[str]] = defaultdict(list)
    by_error: dict[str, list[str]] = defaultdict(list)
    by_pct_bucket: dict[str, list[str]] = defaultdict(list)
    for c in cards:
        for h in c.get("hub_topics") or []:
            by_topic[h["topic_id"]].append(c["id"])
        for oe in c.get("option_errors") or []:
            for t in oe.get("error_tags") or []:
                by_error[t].append(c["id"])
        for re_item in c.get("report_errors") or []:
            for t in re_item.get("error_tags") or []:
                by_error[t].append(c["id"])
        pct = c.get("answer_pct")
        if isinstance(pct, (int, float)):
            if pct >= 80:
                by_pct_bucket["easy_ge_80"].append(c["id"])
            elif pct >= 50:
                by_pct_bucket["mid_50_79"].append(c["id"])
            else:
                by_pct_bucket["hard_lt_50"].append(c["id"])

    # unique preserve order
    def uniq(seq):
        seen = set()
        out = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    index_out = {
        "version": 1,
        "generated": str(date.today()),
        "by_hub_topic": {k: uniq(v) for k, v in sorted(by_topic.items())},
        "by_error_tag": {k: uniq(v) for k, v in sorted(by_error.items(), key=lambda kv: -len(kv[1]))},
        "by_answer_pct_bucket": {k: uniq(v) for k, v in by_pct_bucket.items()},
        "stats": {
            "cards": len(cards),
            "compulsory": sum(1 for c in cards if c.get("stream") == "compulsory"),
            "m1": sum(1 for c in cards if c.get("stream") == "m1"),
            "with_url": sum(1 for c in cards if c.get("url")),
            "with_answer": sum(1 for c in cards if c.get("answer")),
            "with_answer_pct": sum(1 for c in cards if c.get("answer_pct") is not None),
            "with_option_errors": sum(1 for c in cards if c.get("option_errors")),
            "with_report_errors": sum(1 for c in cards if c.get("report_errors")),
            "with_hub_topic": sum(1 for c in cards if c.get("hub_topics")),
            "compulsory_with_hub": sum(
                1 for c in cards if c.get("stream") == "compulsory" and c.get("hub_topics")
            ),
            "with_skills": sum(1 for c in cards if c.get("skills")),
            "unmapped_tag_counts": dict(unmapped_tag_counter.most_common()),
        },
    }

    bundle = {
        "version": 1,
        "generated": str(date.today()),
        "note": "統一題卡：bank_tags 保留原字；hub_topics 經 crosswalk 歸入 20 大課題；option_errors.error_tags 為短標籤。",
        "cards": cards,
    }
    return cards, catalog, index_out, bundle


def write_outputs(catalog, index_out, bundle) -> None:
    SKILLS.mkdir(parents=True, exist_ok=True)
    cards_path = SKILLS / "math_question_cards.json"
    tags_path = SKILLS / "math_error_tags.json"
    idx_path = SKILLS / "math_cards_index.json"
    cards_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tags_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    idx_path.write_text(json.dumps(index_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {cards_path.relative_to(ROOT)} ({len(bundle['cards'])} cards)")
    print(f"wrote {tags_path.relative_to(ROOT)} ({len(catalog['tags'])} error tags)")
    print(f"wrote {idx_path.relative_to(ROOT)}")
    stats = index_out["stats"]
    for k, v in stats.items():
        if k == "unmapped_tag_counts":
            continue
        print(f"  {k}: {v}")
    if stats["unmapped_tag_counts"]:
        print("  unmapped tags:", stats["unmapped_tag_counts"])


def check_only() -> int:
    cards_path = SKILLS / "math_question_cards.json"
    idx_path = SKILLS / "math_cards_index.json"
    cw_path = CROSSWALK_PATH
    if not cards_path.is_file() or not idx_path.is_file() or not cw_path.is_file():
        print("missing outputs; run without --check first", file=sys.stderr)
        return 2
    bundle = json.loads(cards_path.read_text(encoding="utf-8"))
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    cw = json.loads(cw_path.read_text(encoding="utf-8"))
    cards = bundle["cards"]
    errs = []
    if not cards:
        errs.append("no cards")
    # 必修卷必須有 hub；M1 延伸部分嘅 tag 暫未入 20 課題，容許空
    no_hub_comp = [
        c["id"] for c in cards if c.get("stream") == "compulsory" and not c.get("hub_topics")
    ]
    if no_hub_comp:
        errs.append(f"compulsory cards without hub_topics: {len(no_hub_comp)} e.g. {no_hub_comp[:5]}")
    m1_unmapped = {
        k: v
        for k, v in (idx["stats"].get("unmapped_tag_counts") or {}).items()
        if k
        not in {
            # known M1-only labels — warn but do not fail
            "微分法",
            "積分法",
            "定積分",
            "正態分佈",
            "泊松分佈",
            "置信區間",
            "指數級數",
            "梯形法",
            "概率分佈",
            "二項分佈",
            "微分方程",
            "極值",
            "期望與方差",
            "二項式定理",
            "中央極限定理",
            "變化率",
            "Kinematics",
        }
    }
    if m1_unmapped:
        print("WARN non-M1 unmapped tags:", m1_unmapped)
    elif idx["stats"].get("unmapped_tag_counts"):
        print("note: remaining unmapped tags are M1-only:", idx["stats"]["unmapped_tag_counts"])
    valid_ids = {v["topic_id"] for v in cw["map"].values()}
    for c in cards:
        for h in c.get("hub_topics") or []:
            if h["topic_id"] not in valid_ids:
                errs.append(f"{c['id']} unknown topic {h['topic_id']}")
    if errs:
        print("FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print(
        f"ok cards={len(cards)} compulsory_hub={idx['stats'].get('compulsory_with_hub')} "
        f"option_errors={idx['stats']['with_option_errors']} "
        f"error_tags={len(json.loads((SKILLS / 'math_error_tags.json').read_text(encoding='utf-8'))['tags'])}"
    )
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="只驗證已產生檔，不重建")
    args = ap.parse_args()
    if args.check:
        sys.exit(check_only())
    if not CROSSWALK_PATH.is_file():
        print(f"缺 crosswalk：先跑 python scripts/build_math_skill_foundation.py", file=sys.stderr)
        sys.exit(2)
    _cards, catalog, index_out, bundle = build_cards()
    write_outputs(catalog, index_out, bundle)


if __name__ == "__main__":
    main()
