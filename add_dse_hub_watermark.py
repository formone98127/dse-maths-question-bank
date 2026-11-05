#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add locked 'DSE Hub' watermark to delivery SVG/PNG after §9.4 pass.

Usage:
  python add_dse_hub_watermark.py fig.svg
  python add_dse_hub_watermark.py fig.png
  python add_dse_hub_watermark.py folder_of_figs --recursive

Idempotent: skips files that already contain the watermark marker.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WM_TEXT = "DSE Hub"
WM_MARKER = 'id="dse-hub-wm"'
WM_FILL = "#3d8bfd"
WM_OPACITY = 0.28


def _svg_viewbox(svg: str) -> tuple[float, float]:
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg, re.I)
    if m:
        parts = m.group(1).replace(",", " ").split()
        if len(parts) >= 4:
            return float(parts[2]), float(parts[3])
    wm = re.search(r'\bwidth\s*=\s*"([0-9.]+)', svg, re.I)
    hm = re.search(r'\bheight\s*=\s*"([0-9.]+)', svg, re.I)
    if wm and hm:
        return float(wm.group(1)), float(hm.group(1))
    return 400.0, 300.0


def watermark_svg(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if WM_MARKER in raw or f">{WM_TEXT}</text>" in raw and "dse-hub-wm" in raw:
        return False
    w, h = _svg_viewbox(raw)
    fs = max(10.0, min(w, h) * 0.045)
    x = w - max(6.0, w * 0.02)
    y = h - max(6.0, h * 0.02)
    block = (
        f'\n <g {WM_MARKER} pointer-events="none" aria-hidden="true">\n'
        f'  <text x="{x:.3f}" y="{y:.3f}" text-anchor="end" '
        f'font-family="Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif" '
        f'font-size="{fs:.3f}" font-weight="700" fill="{WM_FILL}" '
        f'fill-opacity="{WM_OPACITY}">{WM_TEXT}</text>\n'
        f" </g>\n"
    )
    if "</svg>" not in raw:
        raise ValueError(f"no </svg> in {path}")
    path.write_text(raw.rsplit("</svg>", 1)[0] + block + "</svg>\n", encoding="utf-8")
    return True


def watermark_png(path: Path) -> bool:
    from PIL import Image, ImageDraw, ImageFont

    im = Image.open(path).convert("RGBA")
    # skip if bottom-right already looks watermarked (simple marker file sidecar)
    marker = path.with_suffix(path.suffix + ".dsehubwm")
    if marker.exists():
        return False
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    target = max(14, int(min(im.size) * 0.045))
    font = None
    for name in (
        "C:/Windows/Fonts/msjhbd.ttc",
        "C:/Windows/Fonts/msjh.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        try:
            font = ImageFont.truetype(name, target)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), WM_TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = im.width - tw - max(8, im.width // 50)
    y = im.height - th - max(8, im.height // 50)
    # #3d8bfd at ~28% alpha
    draw.text((x, y), WM_TEXT, font=font, fill=(61, 139, 253, int(255 * WM_OPACITY)))
    out = Image.alpha_composite(im, overlay)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        out = out.convert("RGB")
    out.save(path)
    marker.write_text("DSE Hub\n", encoding="utf-8")
    return True


def process(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".svg":
        return "added" if watermark_svg(path) else "skip"
    if suf in {".png", ".jpg", ".jpeg", ".webp"}:
        return "added" if watermark_png(path) else "skip"
    return "ignore"


def main() -> int:
    ap = argparse.ArgumentParser(description="Add DSE Hub watermark to delivery figures")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("-r", "--recursive", action="store_true")
    args = ap.parse_args()
    files: list[Path] = []
    for p in args.paths:
        if p.is_dir():
            globber = p.rglob if args.recursive else p.glob
            files.extend(sorted(globber("*.svg")))
            files.extend(sorted(globber("*.png")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"missing: {p}", file=sys.stderr)
            return 1
    counts = {"added": 0, "skip": 0, "ignore": 0}
    for f in files:
        status = process(f)
        counts[status] = counts.get(status, 0) + 1
        if status == "added":
            print(f"OK  {f}")
        elif status == "skip":
            print(f"--  {f} (already)")
    print(f"done: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
