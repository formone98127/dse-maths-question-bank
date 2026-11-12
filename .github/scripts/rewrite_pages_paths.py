#!/usr/bin/env python3
"""Copy docs/ to gh-pages-dist/ and prefix root-absolute paths for project Pages."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

SRC = Path("docs")
DST = Path("gh-pages-dist")
PREFIX = "/dse-maths-question-bank"
BANK_OLD = 'const BANK_URL = "https://hkdse.exampaper.cloud/";'
BANK_NEW = 'const BANK_URL = "https://formone98127.github.io/dse-maths-question-bank/";'
TEXT_EXT = {".html", ".js", ".css", ".json", ".webmanifest", ".txt", ".svg"}
SKIP_DIRS = {"mathjax"}
SKIP_NAMES = {"sitemap.xml", "CNAME"}

ATTR = re.compile(
    r"""((?:href|src|content|action|srcset|data-src|poster)=["'])/(?!/|dse-maths-question-bank(?:/|["']))""",
    re.I,
)
CSS_URL = re.compile(
    r"""(url\((['"]?))/(?!/|dse-maths-question-bank/)""",
    re.I,
)


def rewrite(text: str) -> str:
    text = ATTR.sub(rf"\1{PREFIX}/", text)
    text = CSS_URL.sub(rf"\1{PREFIX}/", text)
    text = text.replace(BANK_OLD, BANK_NEW)
    return text


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns(".git", "CNAME"))
    for path in DST.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_NAMES:
            # Keep official sitemap URLs; drop CNAME so github.io does not redirect.
            if path.name == "CNAME":
                path.unlink()
            continue
        if path.suffix.lower() not in TEXT_EXT:
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = rewrite(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")

    (DST / "404.html").write_text(
        """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>頁面不存在｜DSE Hub</title>
</head>
<body>
<p>找不到此頁。<a href="{prefix}/hub/">返回 DSE Hub</a></p>
</body>
</html>
""".format(prefix=PREFIX),
        encoding="utf-8",
    )
    (DST / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
