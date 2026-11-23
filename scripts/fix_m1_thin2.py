#!/usr/bin/env python3
"""改進版：2018／2021 M1 切題（頁為單位，容許題號缺失時自動遞進），驗證 12 題後寫入 data.js。"""
import json
import pathlib
import re

REPO = pathlib.Path("/home/one/hub_repo")
TXT = pathlib.Path("/home/one/m1_fix/txt")
DATA = REPO / "docs/data.js"
FOOT = "Answers written in the margins will not be marked."


def clean(t):
    lines = [l.rstrip() for l in t.splitlines() if l.strip() and l.strip() != FOOT]
    return "\n".join(lines).replace("\\$", "$").strip()


def split_page(text, expected):
    """回傳 [(qno, chunk)]；若頁首冇題號，用 expected 並遞進。"""
    parts = re.split(r"(?m)^\s*(\d{1,2})\.\s", text)
    out = []
    if len(parts) == 1:
        if text:
            out.append((expected, text))
        return out
    # parts[0] 係第一個題號前嘅殘留（多數空）
    prefix = parts[0].strip()
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        body = parts[i + 1].strip()
        if prefix:
            body = prefix + "\n" + body
            prefix = ""
        out.append((n, f"{n}. {body}" if not body.startswith(f"{n}.") else body))
    return out


def build(year):
    qs = {}
    expected = 1
    for p in sorted(TXT.glob(f"{year}_p*.md")):
        text = clean(p.read_text(encoding="utf-8"))
        if not text:
            continue
        low = text.lower()
        if "question-answer book" in low or "instructions" in low or "module 1 (calculus" in low:
            continue  # 封面／指示頁
        if not re.search(r"(?m)^\s*\d{1,2}\.\s", text) and re.search(r"(?i)marks|总分|總分", text) and len(text) < 120:
            continue
        segs = split_page(text, expected)
        for n, chunk in segs:
            if n in qs:
                qs[n] += "\n" + chunk
            else:
                qs[n] = chunk
            expected = max(expected, n + 1)
    return qs


def to_html(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if p:
            out.append("<p>" + p.replace("\n", " ") + "</p>")
    return "\n".join(out)


def main():
    src = DATA.read_text(encoding="utf-8")
    data = json.loads(src[src.index("{"): src.rindex("}") + 1])
    total_changed = 0
    for year in ["2018", "2021"]:
        qs = build(year)
        counts = {k: len(v) for k, v in qs.items()}
        print(f"{year}: {len(qs)} 題 | 最少 {min(counts.values())} 字 | 平均 {round(sum(counts.values())/len(counts))}")
        if len(qs) != 12 or min(counts.values()) < 120:
            print(f"  !! {year} 驗證失敗（需 12 題、每題 ≥120 字），跳過")
            continue
        n_upd = 0
        for n, text in qs.items():
            ent = next((q for q in data["questions"]
                        if q["year"] == year and q["paper"] == "Paper 1M"
                        and str(q["qno"]) == str(n) and q["type"] == "題目"), None)
            if not ent:
                continue
            if len(text) > len(ent.get("text") or ""):
                ent["text"] = text
                ent["html"] = to_html(text)
                n_upd += 1
        print(f"  {year}: 更新 {n_upd} 題")
        total_changed += n_upd
    if total_changed:
        data["count"] = len(data["questions"])
        DATA.write_text("window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    print("total updated:", total_changed)


if __name__ == "__main__":
    main()
