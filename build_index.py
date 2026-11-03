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

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# (檔名, 年份, 卷別, 類型)
SOURCES = [
    ("2012_P1_題目中文卷.md", 2012, "Paper 1", "題目"),
    ("2013_P1_QU(CHI).md",   2013, "Paper 1", "題目"),
    ("2014_P1_QU(CHI).md",   2014, "Paper 1", "題目"),
    ("2012_II_解答.md",      2012, "Paper 2", "解答"),
    ("2013_II_解答.md",      2013, "Paper 2", "解答"),
]


def fix_img_paths(text: str) -> str:
    """圖徑保持 docs 內相對（build 時 figs_svg 會複製入 docs/）"""
    return text


def parse_question_file(path: Path, year: int, paper: str) -> list:
    """題目庫格式：## 第 N 題 →【建議標籤】→ - 卷別/部分 / - 課題 →【題目內容】"""
    raw = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n## 第 (\d+) 題\n", raw)
    out = []
    for i in range(1, len(blocks) - 1, 2):
        qno, body = int(blocks[i]), blocks[i + 1]
        sec = re.search(r"卷別/部分：(.+)", body)
        tags_line = re.search(r"課題：(.+)", body)
        tags = re.findall(r"#([\w\-]+)", tags_line.group(1)) if tags_line else []
        content = body.split("【題目內容】", 1)
        text = content[1].strip() if len(content) > 1 else ""
        text = re.sub(r"\n---\s*$", "", text).strip()
        text = re.sub(r"\n?## (甲部|乙部)[^\n]*$", "", text).strip()  # 移除混入嘅部分標題
        out.append({
            "year": year, "paper": paper, "type": "題目", "qno": qno,
            "title": f"第 {qno} 題",
            "section": sec.group(1).strip() if sec else "",
            "tags": tags,
            "text": text,
            "html": md2html(fix_img_paths(text)),
            "file": path.name,
        })
    return out


def parse_solution_file(path: Path, year: int, paper: str) -> list:
    """解答庫格式：## QN　課題名 → 內容至下一個 ## 或檔尾"""
    raw = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n## Q(\d+)　(.+)\n", raw)
    out = []
    for i in range(1, len(blocks) - 2, 3):
        qno, title, body = int(blocks[i]), blocks[i + 1].strip(), blocks[i + 2]
        text = re.sub(r"\n---\s*$", "", body).strip()
        out.append({
            "year": year, "paper": paper, "type": "解答", "qno": qno,
            "title": f"Q{qno}　{title}",
            "section": f"Paper 2　{'Section A' if qno <= 30 else 'Section B'}",
            "tags": [title],
            "text": text,
            "html": md2html(fix_img_paths(text)),
            "file": path.name,
        })
    return out


def main():
    qs = []
    for fname, year, paper, typ in SOURCES:
        p = ROOT / fname
        if not p.exists():
            print("skip (missing):", fname)
            continue
        got = (parse_question_file(p, year, paper) if typ == "題目"
               else parse_solution_file(p, year, paper))
        qs.extend(got)
        print(f"{fname}: {len(got)} 題")

    qs.sort(key=lambda q: (q["year"], q["paper"], q["type"] != "題目", q["qno"]))
    payload = {"generated": time.strftime("%Y-%m-%d %H:%M"), "count": len(qs), "questions": qs}
    js = "window.QB = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    (DOCS / "data.js").write_text(js, encoding="utf-8")
    print(f"total {len(qs)} 題 -> docs/data.js ({len(js)//1024} KB)")

    # figs_svg 複製入 docs/（Pages /docs 模式只發布 docs 資料夾）
    for figs in sorted(ROOT.glob("*_figs_svg")):
        shutil.copytree(figs, DOCS / figs.name, dirs_exist_ok=True)
        print(f"copied {figs.name} -> docs/{figs.name}")


if __name__ == "__main__":
    main()
