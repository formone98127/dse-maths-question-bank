# -*- coding: utf-8 -*-
"""Generate docs/skills/maps/math-2012-paper-2.md from annotated analysis JSON."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = json.loads((ROOT / "docs/skills/math_skill_book.json").read_text(encoding="utf-8"))
ANALYSIS = ROOT / "docs/analysis/math/2012/paper-2"
OUT = ROOT / "docs/skills/maps/math-2012-paper-2.md"

topics = {t["id"]: t["name"] for t in BOOK["topics"]}
kps = {k["id"]: k["name"] for t in BOOK["topics"] for k in t["knowledge_points"]}
kps_topic = {
    k["id"]: t["name"] for t in BOOK["topics"] for k in t["knowledge_points"]
}
formulas = {f["id"]: f["name"] for t in BOOK["topics"] for f in t["formulas"]}
abilities = {a["id"]: a["name"] for a in BOOK["abilities"]}
CAT_ZH = {
    "Conceptual": "概念",
    "Calculation": "計算",
    "Reading-Formatting": "睇題",
    "Methodological": "方法",
}


def load_rows():
    rows = []
    for p in sorted(ANALYSIS.glob("q*.json"), key=lambda x: int(x.stem[1:])):
        d = json.loads(p.read_text(encoding="utf-8"))
        s = d["skills"]
        md = d["analysis"]["metadata"]
        oa = d["analysis"]["options_analysis"]
        correct = next(k for k, v in oa.items() if v.get("is_correct"))
        wrong = {k: v for k, v in oa.items() if not v.get("is_correct")}
        rows.append(
            {
                "q": int(p.stem[1:]),
                "correct": correct,
                "topic_id": s["topic_id"],
                "topic": topics[s["topic_id"]],
                "kps": s["knowledge_point_ids"],
                "formulas": s["formula_ids"],
                "abilities": s["ability_ids"],
                "faults": s["option_faults"],
                "wrong": wrong,
                "bloom": md.get("bloom_taxonomy_level"),
                "secs": md.get("estimated_time_seconds"),
                "primary": md.get("primary_topic"),
            }
        )
    return rows


def bar(n, total, width=16):
    filled = round(width * n / total) if total else 0
    return "█" * filled + "░" * (width - filled)


def main():
    rows = load_rows()
    n = len(rows)
    fault_n = sum(len(r["faults"]) for r in rows)
    secs = [r["secs"] for r in rows]

    topic_c = Counter(r["topic"] for r in rows)
    fault_ab = Counter(
        abilities[f["ability_id"]] for r in rows for f in r["faults"].values()
    )
    fault_kp = Counter(
        kps[f["knowledge_point_id"]]
        for r in rows
        for f in r["faults"].values()
        if f.get("knowledge_point_id")
    )
    fault_f = Counter(
        formulas[f["formula_id"]]
        for r in rows
        for f in r["faults"].values()
        if f.get("formula_id")
    )
    err_c = Counter(
        CAT_ZH.get(v["error_category"], v["error_category"])
        for r in rows
        for v in r["wrong"].values()
    )
    stack_c = Counter(len(r["kps"]) for r in rows)
    bloom_c = Counter(r["bloom"] for r in rows)
    q_ab = Counter(abilities[a] for r in rows for a in r["abilities"])

    lines = []
    a = lines.append

    a("# 2012 數學卷二 · 技能地圖")
    a("")
    a("由已掛好嘅 `skills` 編號統計。唔係學生答題紀錄——係「呢一卷出題人預埋嘅陷阱地圖」。")
    a("")
    a(f"- 題數：**{n}**")
    a(f"- 錯選項（陷阱）總數：**{fault_n}**（平均每題 {fault_n/n:.1f} 個）")
    a(f"- 預計作答時間：最短 {min(secs)} 秒 · 中位 {sorted(secs)[n//2]} 秒 · 最長 {max(secs)} 秒 · 平均 {sum(secs)/n:.0f} 秒")
    a("")
    a("## 一眼睇完")
    a("")
    a("1. **最多題嘅課題**：數系（5）、統計（4）、求積法（4）、圓形幾何（4）。")
    a("2. **錯選項最常指向嘅能力**：代數變形、計算仔細度、睇條件——合共佔大多數陷阱。")
    a("3. **錯選項最常踩中嘅知識點**：二次函數頂點與開口、平面圖形面積、展開與合併、不等式、弧長與扇形。")
    a("4. **錯誤類型**：概念 62、計算 50、睇題 15、方法 8（一個錯選項一個類型）。")
    a("5. **大多數題疊 2 個知識點**（29 題）；淨用 1 個嘅有 14 題；3 個嘅只有 2 題。")
    a("")
    a("## 課題分佈（成題主課題）")
    a("")
    a("| 題數 | 課題 | |")
    a("|---:|---|---|")
    for name, c in topic_c.most_common():
        a(f"| {c} | {name} | `{bar(c, topic_c.most_common(1)[0][1])}` |")
    missing = [t["name"] for t in BOOK["topics"] if t["name"] not in topic_c]
    if missing:
        a("")
        a("本卷**未出現**作主課題：" + "、".join(missing))
    a("")
    a("## 錯選項：學生跌倒時，最常係邊種能力")
    a("")
    a("每個錯選項只計一種能力。數字越大 = 卷內預設越多陷阱打呢一種。")
    a("")
    a("| 次數 | 能力 | |")
    a("|---:|---|---|")
    top_ab = fault_ab.most_common(1)[0][1]
    for name, c in fault_ab.most_common():
        a(f"| {c} | {name} | `{bar(c, top_ab)}` |")
    a("")
    a("成題標明「用到」嘅能力（一題可多於一種）：")
    a("")
    a("| 題數提及 | 能力 |")
    a("|---:|---|")
    for name, c in q_ab.most_common():
        a(f"| {c} | {name} |")
    a("")
    a("## 錯選項：最常踩中嘅知識點（Top 12）")
    a("")
    a("| 次數 | 知識點 |")
    a("|---:|---|")
    for name, c in fault_kp.most_common(12):
        a(f"| {c} | {name} |")
    a("")
    a("## 錯選項：最常踩中嘅公式（Top 12）")
    a("")
    a("| 次數 | 公式 |")
    a("|---:|---|")
    for name, c in fault_f.most_common(12):
        a(f"| {c} | {name} |")
    a("")
    a("## 錯誤類型分佈")
    a("")
    a("| 次數 | 類型 | 意思 |")
    a("|---:|---|---|")
    meaning = {
        "概念": "條概念／公式用錯",
        "計算": "步驟大致啱，計數或符號出錯",
        "睇題": "單位、條件、小數位等睇漏",
        "方法": "用咗低效或無效嘅切入",
    }
    top_e = err_c.most_common(1)[0][1]
    for name, c in err_c.most_common():
        a(f"| {c} | {name} | {meaning.get(name, '')} |")
    a("")
    a("## 知識點疊加（難度粗指標）")
    a("")
    a("| 一題知識點數 | 題數 |")
    a("|---:|---:|")
    for k in sorted(stack_c):
        a(f"| {k} | {stack_c[k]} |")
    a("")
    a("Bloom 層次：")
    a("")
    a("| 題數 | 層次 |")
    a("|---:|---|")
    for name, c in bloom_c.most_common():
        a(f"| {c} | {name} |")
    a("")
    a("## 逐題地圖")
    a("")
    a("| 題 | 答案 | 課題 | 層次 | 秒 | 知識點 | 能力 | 錯選項 → 能力／公式或知識點 |")
    a("|---:|:---:|---|---|---:|---|---|---|")
    for r in rows:
        kp = "、".join(kps[x] for x in r["kps"])
        ab = "、".join(abilities[x] for x in r["abilities"])
        bits = []
        for opt, f in sorted(r["faults"].items()):
            tag = abilities[f["ability_id"]]
            if f.get("formula_id"):
                tag += "／" + formulas[f["formula_id"]]
            elif f.get("knowledge_point_id"):
                tag += "／" + kps[f["knowledge_point_id"]]
            cat = CAT_ZH.get(r["wrong"][opt]["error_category"], "")
            bits.append(f"{opt}（{cat}）{tag}")
        a(
            f"| {r['q']} | {r['correct']} | {r['topic']} | {r['bloom']} | {r['secs']} | {kp} | {ab} | "
            + "；".join(bits)
            + " |"
        )
    a("")
    a("## 點用呢份地圖")
    a("")
    a("- **備題／補習**：先睇「錯選項最常踩中」嗰幾條，專出打呢幾點嘅易題。")
    a("- **之後個人報告**：學生揀咗邊個字母，就對呢張表嘅「錯選項 → …」一行，加 1 次弱點。")
    a("- **跨年擴展**：其他年份掛同一套編號後，呢張表可以加埋「邊啲陷阱年年出現」。")
    a("")
    a("---")
    a("")
    a("產生方式：`python scripts/map_2012_p2.py`")
    a("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({n} questions, {fault_n} traps)")


if __name__ == "__main__":
    main()
