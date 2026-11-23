#!/usr/bin/env python3
"""修正 data.js 內 404 圖片引用（用 JSON 解析，唔靠 regex 猜轉義）。"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/one/hub_repo")
DOCS = REPO / "docs"
SRC = DOCS / "hub" / "data.js"


def main():
    apply = "--apply" in sys.argv
    raw = SRC.read_text(encoding="utf-8")
    body = raw[raw.index("{"): raw.rindex("}") + 1]
    data = json.loads(body)

    by_name = {}
    for p in DOCS.rglob("*.png"):
        by_name.setdefault(p.name.lower(), []).append(p)

    refs = set()
    for q in data["questions"]:
        for key in ("html", "text"):
            for m in re.findall(r'<img[^>]+src="([^"]+)"', q.get(key) or ""):
                refs.add(m)
    missing = sorted(r for r in refs if not (DOCS / r).exists())
    print(f"img refs={len(refs)} missing={len(missing)}")

    fixes = {}
    drops = set()
    for r in missing:
        cands = by_name.get(pathlib.Path(r).name.lower(), [])
        if len(cands) == 1:
            new = cands[0].relative_to(DOCS).as_posix()
            fixes[r] = new
            print(f"  FIX {r} -> {new}")
        else:
            drops.add(r)
            print(f"  DROP {r} (同名檔 {len(cands)} 個)")

    if apply:
        for q in data["questions"]:
            for key in ("html", "text"):
                v = q.get(key)
                if not v:
                    continue
                for old, new in fixes.items():
                    v = v.replace(f'src="{old}"', f'src="{new}"').replace(f"]({old})", f"]({new})")
                for old in drops:
                    v = re.sub(r'<img[^>]+src="' + re.escape(old) + r'"[^>]*>', "", v)
                    v = v.replace(f"![Figure]({old})", "").replace(f"]({old})", "](about:blank)")
                q[key] = v
        out = "window.QB =" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"
        SRC.write_text(out, encoding="utf-8")
        print(f"applied: fixed={len(fixes)} dropped={len(drops)}")


if __name__ == "__main__":
    main()
