# -*- coding: utf-8 -*-
"""交貨前格式閘門：粗體強調詞、合併格表格、填空底線轉義。

用法：
  python qa_md_format.py 題庫/經濟/2015_P1_QU(ENG).md
  python qa_md_format.py 題庫/經濟/*.md

退出碼：0 = 無嫌疑；1 = 有嫌疑要對頁覆核（唔等於一定錯，但唔准跳過）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# DSE 英文卷常見全大楷強調（原卷多數粗體）
EMPHASIS = (
    "INCONSISTENT", "CONSISTENT", "LEAST", "MOST", "EXCEPT",
    "WITHOUT", "INCORRECT", "CORRECT", "ALWAYS", "NEVER",
    "ONLY", "ALL", "NONE", "NOT", "TRUE", "FALSE",
)

EMP_RE = re.compile(
    r"(?<!\*\*)\b(" + "|".join(EMPHASIS) + r")\b(?!\*\*)"
)
# 已包喺 **…** 入面嘅唔計
BOLD_CHUNK = re.compile(r"\*\*[^*]+\*\*")
# 未轉義底線：Markdown 會當粗斜體食咗，網頁只剩好短嘅 _
RAW_BLANK = re.compile(r"(?<!\\)_{3,}")

Q_SPLIT = re.compile(r"\n## 第 (\d+) 題\n")
TABLE_BLOCK = re.compile(r"(?:^\|.+\|\s*\n)+", re.M)


def strip_bold(text: str) -> str:
    return BOLD_CHUNK.sub(" ", text)


def check_emphasis(qno: int, body: str, hits: list) -> None:
    content = body.split("【題目內容】", 1)
    text = content[1] if len(content) > 1 else body
    # 唔檢查 HTML／已粗體段
    plain = strip_bold(text)
    plain = re.sub(r"<[^>]+>", " ", plain)
    for m in EMP_RE.finditer(plain):
        w = m.group(1)
        # NOT／ALL／ONLY 好境多；仍標嫌疑，人工對頁
        hits.append((qno, "粗體嫌疑", w,
                     "題幹有全大楷強調詞但 MD 無 **…**；請對頁確認是否粗體"))
    for m in RAW_BLANK.finditer(text):
        hits.append((
            qno, "底線轉義", m.group(0)[:20],
            "未轉義 ___ 會被 Markdown 食成短 _；改用 \\_\\_\\_… 照原卷長度",
        ))


def check_tables(qno: int, body: str, hits: list) -> None:
    content = body.split("【題目內容】", 1)
    text = content[1] if len(content) > 1 else body
    # 已用 HTML colspan → OK
    if re.search(r"colspan\s*=\s*[\"']?\d+", text, re.I):
        return
    for block in TABLE_BLOCK.findall(text):
        rows = [r.strip() for r in block.strip().splitlines() if r.strip().startswith("|")]
        if len(rows) < 2:
            continue
        # 跳過分隔行 |---|
        data_rows = [r for r in rows if not re.match(r"^\|[\s\-:|]+\|$", r)]
        if len(data_rows) < 2:
            continue
        cells0 = [c.strip() for c in data_rows[0].strip("|").split("|")]
        cells1 = [c.strip() for c in data_rows[1].strip("|").split("|")]
        # 真跨欄嫌疑：表頭列首格空＋長字，下一列都係「子表頭」（首格亦空），
        # 即 Year 1/Year 2、Good X/Good Y 呢類——唔係「空角＋單欄數據表頭」
        if not (cells0 and cells0[0] == "" and len(cells0) >= 2 and len(cells0[1]) >= 12):
            continue
        if not (cells1 and cells1[0] == ""):
            continue
        non_empty_sub = [c for c in cells1[1:] if c]
        if len(non_empty_sub) >= 2 or len(cells0) >= 3:
            hits.append((
                qno, "合併格嫌疑", cells0[1][:60],
                "表頭下有多個子欄；原卷跨欄要用 HTML <th colspan=\"N\">",
            ))


def scan_file(path: Path) -> list:
    raw = path.read_text(encoding="utf-8")
    parts = Q_SPLIT.split(raw)
    hits = []
    for i in range(1, len(parts) - 1, 2):
        qno, body = int(parts[i]), parts[i + 1]
        check_emphasis(qno, body, hits)
        check_tables(qno, body, hits)
    return hits


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("用法: python qa_md_format.py <QU.md> [更多.md]")
        return 2
    paths: list[Path] = []
    for a in argv[1:]:
        p = Path(a)
        if any(ch in a for ch in "*?["):
            paths.extend(sorted(Path().glob(a)))
        elif p.is_file():
            paths.append(p)
        else:
            print("找不到:", a)
            return 2
    total = 0
    for path in paths:
        hits = scan_file(path)
        print(f"== {path} ==")
        if not hits:
            print("  OK（無粗體／合併格嫌疑）")
            continue
        total += len(hits)
        for qno, kind, token, tip in hits:
            print(f"  Q{qno} [{kind}] {token!r}")
            print(f"         → {tip}")
    if total:
        print(f"\n共 {total} 項嫌疑：對頁覆核後先交貨（§7 閘門）。")
        return 1
    print("\n全部通過格式閘門。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
