"""把動畫 GIF／MP4 掛到某一題的解答 entry（data.js 的 anim 欄）。"""
from __future__ import annotations
import argparse, json, pathlib, re

SITE = pathlib.Path(__file__).resolve().parents[1]
DATA = SITE / "docs" / "data.js"


def load():
    raw = DATA.read_text(encoding="utf-8")
    head, body = raw.split("window.QB =", 1)
    return head, json.loads(body.rstrip().rstrip(";"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--paper", required=True)
    ap.add_argument("--qno", required=True)
    ap.add_argument("--anim", required=True, help="例如 /media/solutions/2012P2Q41.gif")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    head, obj = load()
    hit = 0
    for e in obj["questions"]:
        if (e.get("year") == a.year and e.get("paper") == a.paper
                and str(e.get("qno")) == str(a.qno) and e.get("type") == "解答"):
            e["anim"] = a.anim
            hit += 1
    print(f"{a.year} {a.paper} Q{a.qno}: 掛上 {a.anim} → {hit} 條 entry")
    if a.write and hit:
        DATA.write_text(head + "window.QB =" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";",
                        encoding="utf-8")
        print("已寫入 docs/data.js")


if __name__ == "__main__":
    main()
