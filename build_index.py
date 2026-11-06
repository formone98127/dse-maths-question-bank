# -*- coding: utf-8 -*-
"""題庫檢索 index 產生器
parse 三份成品 MD → docs/data.js（內嵌 JSON），供 docs/index.html 檢索網頁使用。
重跑: python build_index.py
"""
import io
import json
import re
import shutil
import sys
import time
from pathlib import Path

import markdown

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MD_EXT = ["tables"]


def md2html(text: str) -> str:
    return markdown.markdown(text, extensions=MD_EXT)


def strip_tail_matter(raw: str) -> str:
    """移除檔尾製作說明：--- 後嘅 > blockquote、「全卷完／試卷完」行（新年份 MD 都照跟呢個格式）"""
    for _ in range(3):
        new = re.sub(r"\n---\s*\n+(> .*\n?)+\s*$", "\n", raw)
        new = re.sub(r"\n+> (本題目庫|備份|製作|制作).*$", "\n", new, flags=re.S)
        new = re.sub(r"\n+\*?[—\s]*(全卷完|試卷完)[^\n]*\*?\s*$", "\n", new)
        new = re.sub(r"\n---\s*$", "\n", new)
        if new == raw:
            break
        raw = new
    return raw

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# (檔名, 年份, 卷別, 類型, 科目)
SOURCES = [
    ("2012_P1_題目中文卷.md", 2012, "Paper 1", "題目", "數學"),
    ("2012_P1_解答.md",      2012, "Paper 1", "解答", "數學"),
    ("2013_P1_QU(CHI).md",   2013, "Paper 1", "題目", "數學"),
    ("2014_P1_QU(CHI).md",   2014, "Paper 1", "題目", "數學"),
    ("2015_P2_QU(CHI).md",   2015, "Paper 2", "題目", "數學"),
    ("2012_II_解答.md",      2012, "Paper 2", "解答", "數學"),
    ("2013_II_解答.md",      2013, "Paper 2", "解答", "數學"),
    ("題庫/經濟/2015_P1_QU(ENG).md", 2015, "Paper 1", "題目", "經濟"),
    ("題庫/經濟/2017_P1_QU(ENG).md", 2017, "Paper 1", "題目", "經濟"),
    ("題庫/經濟/2020_P1_QU(ENG).md", 2020, "Paper 1", "題目", "經濟"),
    # 理科第 2 層（原卷截圖；先 push 後校對）
    ("化學/2024_P1A_QU(CHI).md", 2024, "Paper 1A", "題目", "化學"),
    ("化學/2024_P1B_QU(CHI).md", 2024, "Paper 1B", "題目", "化學"),
    ("化學/2024_P2_QU(CHI).md",  2024, "Paper 2",  "題目", "化學"),
    ("化學/2023_P1A_QU(CHI).md", 2023, "Paper 1A", "題目", "化學"),
    ("化學/2023_P1B_QU(CHI).md", 2023, "Paper 1B", "題目", "化學"),
    ("化學/2023_P2_QU(CHI).md",  2023, "Paper 2",  "題目", "化學"),
    ("化學/2022_P1A_QU(CHI).md", 2022, "Paper 1A", "題目", "化學"),
    ("化學/2022_P1B_QU(CHI).md", 2022, "Paper 1B", "題目", "化學"),
    ("化學/2022_P2_QU(CHI).md",  2022, "Paper 2",  "題目", "化學"),
    ("化學/2021_P1A_QU(CHI).md", 2021, "Paper 1A", "題目", "化學"),
    ("化學/2021_P1B_QU(CHI).md", 2021, "Paper 1B", "題目", "化學"),
    ("化學/2021_P2_QU(CHI).md",  2021, "Paper 2",  "題目", "化學"),
    ("化學/2020_P1A_QU(CHI).md", 2020, "Paper 1A", "題目", "化學"),
    ("化學/2020_P1B_QU(CHI).md", 2020, "Paper 1B", "題目", "化學"),
    ("化學/2020_P2_QU(CHI).md",  2020, "Paper 2",  "題目", "化學"),
    ("化學/2019_P1A_QU(CHI).md", 2019, "Paper 1A", "題目", "化學"),
    ("化學/2019_P1B_QU(CHI).md", 2019, "Paper 1B", "題目", "化學"),
    ("化學/2019_P2_QU(CHI).md",  2019, "Paper 2",  "題目", "化學"),
    ("化學/2018_P1A_QU(CHI).md", 2018, "Paper 1A", "題目", "化學"),
    ("化學/2018_P1B_QU(CHI).md", 2018, "Paper 1B", "題目", "化學"),
    ("化學/2018_P2_QU(CHI).md",  2018, "Paper 2",  "題目", "化學"),
    ("化學/2017_P1A_QU(CHI).md", 2017, "Paper 1A", "題目", "化學"),
    ("化學/2017_P1B_QU(CHI).md", 2017, "Paper 1B", "題目", "化學"),
    ("化學/2017_P2_QU(CHI).md",  2017, "Paper 2",  "題目", "化學"),
    ("生物/2023_P1_QU(CHI).md",  2023, "Paper 1",  "題目", "生物"),
    ("生物/2023_P2_QU(CHI).md",  2023, "Paper 2",  "題目", "生物"),
    ("物理/2024_P1_QU(CHI).md",  2024, "Paper 1",  "題目", "物理"),
    ("物理/2024_P2_QU(CHI).md",  2024, "Paper 2",  "題目", "物理"),
]

SUBJ_ORDER = ["數學", "經濟", "化學", "生物", "物理"]

# 第 2 層截圖：src 相對 repo → docs 內唯一名（避免化學／物理同名 2024_P2_crops 互蓋）
SCIENCE_CROP_MAP = [
    ("化學/2024_P1A_crops", "chem_2024_P1A_crops"),
    ("化學/2024_P1B_crops", "chem_2024_P1B_crops"),
    ("化學/2024_P2_crops", "chem_2024_P2_crops"),
    ("化學/2023_P1A_crops", "chem_2023_P1A_crops"),
    ("化學/2023_P1B_crops", "chem_2023_P1B_crops"),
    ("化學/2023_P2_crops", "chem_2023_P2_crops"),
    ("化學/2022_P1A_crops", "chem_2022_P1A_crops"),
    ("化學/2022_P1B_crops", "chem_2022_P1B_crops"),
    ("化學/2022_P2_crops", "chem_2022_P2_crops"),
    ("化學/2021_P1A_crops", "chem_2021_P1A_crops"),
    ("化學/2021_P1B_crops", "chem_2021_P1B_crops"),
    ("化學/2021_P2_crops", "chem_2021_P2_crops"),
    ("化學/2020_P1A_crops", "chem_2020_P1A_crops"),
    ("化學/2020_P1B_crops", "chem_2020_P1B_crops"),
    ("化學/2020_P2_crops", "chem_2020_P2_crops"),
    ("化學/2019_P1A_crops", "chem_2019_P1A_crops"),
    ("化學/2019_P1B_crops", "chem_2019_P1B_crops"),
    ("化學/2019_P2_crops", "chem_2019_P2_crops"),
    ("化學/2018_P1A_crops", "chem_2018_P1A_crops"),
    ("化學/2018_P1B_crops", "chem_2018_P1B_crops"),
    ("化學/2018_P2_crops", "chem_2018_P2_crops"),
    ("化學/2017_P1A_crops", "chem_2017_P1A_crops"),
    ("化學/2017_P1B_crops", "chem_2017_P1B_crops"),
    ("化學/2017_P2_crops", "chem_2017_P2_crops"),
    ("生物/2023_P1_crops", "bio_2023_P1_crops"),
    ("生物/2023_P2_crops", "bio_2023_P2_crops"),
    ("物理/2024_P1_crops", "phys_2024_P1_crops"),
    ("物理/2024_P2_crops", "phys_2024_P2_crops"),
]


def fix_img_paths(text: str, subject: str = "數學") -> str:
    """圖徑改成 docs 內唯一資料夾名（Pages 只發布 docs/）"""
    if subject == "化學":
        text = text.replace("2024_P1A_crops/", "chem_2024_P1A_crops/")
        text = text.replace("2024_P1B_crops/", "chem_2024_P1B_crops/")
        text = text.replace("2024_P2_crops/", "chem_2024_P2_crops/")
        text = text.replace("2023_P1A_crops/", "chem_2023_P1A_crops/")
        text = text.replace("2023_P1B_crops/", "chem_2023_P1B_crops/")
        text = text.replace("2023_P2_crops/", "chem_2023_P2_crops/")
        text = text.replace("2022_P1A_crops/", "chem_2022_P1A_crops/")
        text = text.replace("2022_P1B_crops/", "chem_2022_P1B_crops/")
        text = text.replace("2022_P2_crops/", "chem_2022_P2_crops/")
        text = text.replace("2021_P1A_crops/", "chem_2021_P1A_crops/")
        text = text.replace("2021_P1B_crops/", "chem_2021_P1B_crops/")
        text = text.replace("2021_P2_crops/", "chem_2021_P2_crops/")
        text = text.replace("2020_P1A_crops/", "chem_2020_P1A_crops/")
        text = text.replace("2020_P1B_crops/", "chem_2020_P1B_crops/")
        text = text.replace("2020_P2_crops/", "chem_2020_P2_crops/")
        text = text.replace("2019_P1A_crops/", "chem_2019_P1A_crops/")
        text = text.replace("2019_P1B_crops/", "chem_2019_P1B_crops/")
        text = text.replace("2019_P2_crops/", "chem_2019_P2_crops/")
        text = text.replace("2018_P1A_crops/", "chem_2018_P1A_crops/")
        text = text.replace("2018_P1B_crops/", "chem_2018_P1B_crops/")
        text = text.replace("2018_P2_crops/", "chem_2018_P2_crops/")
        text = text.replace("2017_P1A_crops/", "chem_2017_P1A_crops/")
        text = text.replace("2017_P1B_crops/", "chem_2017_P1B_crops/")
        text = text.replace("2017_P2_crops/", "chem_2017_P2_crops/")
    elif subject == "生物":
        text = text.replace("2023_P1_crops/", "bio_2023_P1_crops/")
        text = text.replace("2023_P2_crops/", "bio_2023_P2_crops/")
    elif subject == "物理":
        text = text.replace("2024_P1_crops/", "phys_2024_P1_crops/")
        text = text.replace("2024_P2_crops/", "phys_2024_P2_crops/")
    return text


def encode_qno(token: str) -> int:
    """支援「1.1」同「1」（結構式）→ 唯一整數（11／19）"""
    if "." in token:
        a, b = token.split(".", 1)
        return int(a) * 10 + int(b)
    return int(token) * 10 + 9


def parse_question_file(path: Path, year: int, paper: str, subject: str = "數學") -> list:
    """題目庫格式：## 第 N 題 →【建議標籤】→ - 卷別/部分 / - 課題 →【題目內容】
    亦支援物理卷二「## 第 1.1 題」「## 第 1 題（結構式）」"""
    raw = strip_tail_matter(path.read_text(encoding="utf-8"))
    blocks = re.split(r"\n## 第 (\d+(?:\.\d+)?) 題(?:（[^）\n]*）)?\n", raw)
    out = []
    phys_p2 = subject == "物理" and paper == "Paper 2"
    for i in range(1, len(blocks) - 1, 2):
        token, body = blocks[i], blocks[i + 1]
        if phys_p2 or "." in token:
            qno = encode_qno(token)
            label = f"第 {token} 題" if "." in token else f"第 {token} 題（結構式）"
        else:
            qno = int(token)
            label = f"第 {qno} 題"
        sec = re.search(r"卷別/部分：(.+)", body)
        tags_line = re.search(r"課題：(.+)", body)
        tags = re.findall(r"#([\w\-]+)", tags_line.group(1)) if tags_line else []
        sec_text = sec.group(1).strip() if sec else ""
        part_m = re.search(r"(甲部\(\d\)|乙部)", sec_text)
        title = f"{part_m.group(1)} {label}" if part_m else label
        content = body.split("【題目內容】", 1)
        text = content[1].strip() if len(content) > 1 else ""
        for _ in range(4):
            new = re.sub(r"\n---\s*$", "", text).rstrip()
            new = re.sub(r"\n?## (甲部|乙部|丙部|丁部|第一部分|第二部分)[^\n]*$", "", new).rstrip()
            if new == text:
                break
            text = new
        out.append({
            "subject": subject,
            "year": year, "paper": paper, "type": "題目", "qno": qno,
            "title": title,
            "section": sec.group(1).strip() if sec else "",
            "tags": tags,
            "text": text,
            "html": md2html(fix_img_paths(text, subject)),
            "file": path.name,
        })
    return out


def parse_solution_file(path: Path, year: int, paper: str, subject: str = "數學") -> list:
    """解答庫格式：## QN　課題名 → 內容至下一個 ## 或檔尾"""
    raw = strip_tail_matter(path.read_text(encoding="utf-8"))
    blocks = re.split(r"\n## Q(\d+)　(.+)\n", raw)
    out = []
    for i in range(1, len(blocks) - 2, 3):
        qno, title, body = int(blocks[i]), blocks[i + 1].strip(), blocks[i + 2]
        text = re.sub(r"\n---\s*$", "", body).strip()
        out.append({
            "subject": subject,
            "year": year, "paper": paper, "type": "解答", "qno": qno,
            "title": f"Q{qno}　{title}",
            "section": (f"Paper 2　{'Section A' if qno <= 30 else 'Section B'}"
                        if paper == "Paper 2"
                        else f"Paper 1　{'甲部(1)' if qno <= 9 else '甲部(2)' if qno <= 14 else '乙部'}"),
            "tags": [title],
            "text": text,
            "html": md2html(fix_img_paths(text, subject)),
            "file": path.name,
        })
    return out


def main():
    qs = []
    for fname, year, paper, typ, subject in SOURCES:
        p = ROOT / fname
        if not p.exists():
            print("skip (missing):", fname)
            continue
        got = (parse_question_file(p, year, paper, subject) if typ == "題目"
               else parse_solution_file(p, year, paper, subject))
        qs.extend(got)
        print(f"{fname}: {len(got)} 題")

    qs.sort(key=lambda q: (SUBJ_ORDER.index(q["subject"]) if q["subject"] in SUBJ_ORDER else 99,
                           q["year"], q["paper"], q["type"] != "題目", q["qno"]))
    payload = {"generated": time.strftime("%Y-%m-%d %H:%M"), "count": len(qs), "questions": qs}
    js = "window.QB = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    (DOCS / "data.js").write_text(js, encoding="utf-8")
    print(f"total {len(qs)} 題 -> docs/data.js ({len(js)//1024} KB)")

    # figs_svg 複製入 docs/（Pages /docs 模式只發布 docs 資料夾）
    for figs in sorted(ROOT.glob("*_figs_svg")):
        shutil.copytree(figs, DOCS / figs.name, dirs_exist_ok=True)
        print(f"copied {figs.name} -> docs/{figs.name}")

    # 經濟圖檔：只複製已列入 SOURCES 嘅年份（未收貨年份唔上公開 repo）
    econ_years = sorted({y for _, y, _, t, s in SOURCES if s == "經濟" and t == "題目"})
    for y in econ_years:
        src = ROOT / "題庫" / "經濟" / f"{y}_P1_images"
        if src.is_dir():
            shutil.copytree(src, DOCS / src.name, dirs_exist_ok=True)
            print(f"copied {src.name} -> docs/{src.name}")

    # 理科第 2 層 crops → docs 唯一名（MD 路徑喺 fix_img_paths 改寫）
    for rel, dest_name in SCIENCE_CROP_MAP:
        src = ROOT / rel
        if src.is_dir():
            shutil.copytree(src, DOCS / dest_name, dirs_exist_ok=True)
            n = len(list(src.glob("*.png")))
            print(f"copied {rel} ({n} png) -> docs/{dest_name}")


if __name__ == "__main__":
    main()
