#!/usr/bin/env python3
"""重建 docs/questions/_index.json 及 docs/sitemap-questions.xml（掃描實際頁面）。"""
import json
import pathlib
import re
from datetime import date

REPO = pathlib.Path("/home/one/hub_repo")
QDIR = REPO / "docs/questions"
SITE = "https://hkdse.exampaper.cloud"


def topic_names():
    p = REPO / "docs/topics/_mapping.json"
    if not p.exists():
        return {}
    m = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for name, slug in (m.items() if isinstance(m, dict) else []):
        out[str(slug)] = name
    return out


def parse(page):
    html = page.read_text(encoding="utf-8")
    title = (re.search(r"<title>(.*?)</title>", html) or [None, ""])[1] if "<title>" in html else ""
    m = re.search(r"<title>(.*?)</title>", html)
    title = m.group(1) if m else ""
    pct = None
    pm = re.search(r"答對率\s*(\d+)%", title)
    if pm:
        pct = int(pm.group(1))
    tags = []
    for tm in re.finditer(r'class="tag" href="[^"]*/topics/([^/"]+)/"[^>]*>([^<]+)', html):
        tags.append((tm.group(1), tm.group(2).strip()))
    desc = ""
    dm = re.search(r'<meta name="description" content="([^"]*)"', html)
    if dm:
        desc = dm.group(1)
    ans = None
    am = re.search(r'<div class="big">([^<]{1,60})</div>', html)
    if am:
        ans = am.group(1).strip()
    return {
        "title": title,
        "pct": pct,
        "tags": tags,
        "desc_len": len(desc),
        "answer": ans,
        "has_ms": "/ms/" in html,
        "has_report": "考評報告" in html,
        "langs": [l for l in ("en", "zh") if f'id="{l}"' in html],
    }


def main():
    rows = []
    for page in sorted(QDIR.glob("math/*/paper-*/q*/index.html")):
        parts = page.parts
        i = parts.index("math")
        year, paper_slug, qslug = parts[i + 1], parts[i + 2], parts[i + 3]
        paper = paper_slug.replace("paper-", "")
        qno = qslug[1:]
        meta = parse(page)
        rows.append({
            "year": year,
            "paper": paper,
            "qno": qno,
            "url": f"/questions/math/{year}/paper-{paper}/q{qno}/",
            "file": str(page.relative_to(REPO)).replace("\\", "/"),
            "langs": meta["langs"] or ["zh"],
            "has_solution": meta["has_ms"],
            "has_report": meta["has_report"],
            "answer": meta["answer"],
            "answer_pct": meta["pct"],
            "tags": [t[1] for t in meta["tags"]],
            "title": meta["title"],
            "desc_len": meta["desc_len"],
        })

    rows.sort(key=lambda r: (r["year"], r["paper"], int(r["qno"])))
    (QDIR / "_index.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("index rows:", len(rows))

    urls = [SITE + r["url"] for r in rows]
    today = date.today().isoformat()
    body = "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq></url>\n" for u in urls)
    (REPO / "docs/sitemap-questions.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + "</urlset>\n", encoding="utf-8")
    print("sitemap-questions urls:", len(urls))


if __name__ == "__main__":
    main()
