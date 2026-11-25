"""
Batch-render all DSE Math Visual scenes, then merge with FFmpeg.

Usage:
  python render_all.py              # 1080p30 quality medium
  python render_all.py --ql         # low quality preview
  python render_all.py --merge-only # only concat existing mp4s
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SFX_PATH = ROOT / "sfx_markers.json"
CONCAT_LIST = ROOT / "concat_list.txt"
FINAL_OUT = ROOT / "DSE_Math_Visual_Overview.mp4"

SCENES = [
    ("scene_01_intro.py", "IntroChaosToOrder", "01_intro"),
    ("scene_02_algebra.py", "AlgebraArc", "02_algebra"),
    ("scene_03_geometry.py", "GeometryArc", "03_geometry"),
    ("scene_04_data.py", "DataArc", "04_data"),
    ("scene_05_unification.py", "UnificationArc", "05_unification"),
    ("scene_06_outro.py", "OutroFinale", "06_outro"),
]


def _find_mp4(scene_file: str, class_name: str, quality_flag: str) -> Path | None:
    """Locate Manim output mp4 for a scene class under media/videos/."""
    media = ROOT / "media" / "videos" / Path(scene_file).stem
    if not media.exists():
        return None
    # quality folders: 1080p30, 480p15, 720p30, etc.
    candidates: list[Path] = []
    for folder in media.rglob(f"{class_name}.mp4"):
        candidates.append(folder)
    if not candidates:
        return None
    # Prefer highest-res / newest
    candidates.sort(key=lambda p: (p.stat().st_mtime, p.stat().st_size), reverse=True)
    return candidates[0]


def render_scene(scene_file: str, class_name: str, quality: str) -> Path:
    cmd = [
        sys.executable,
        "-m",
        "manim",
        quality,
        str(ROOT / scene_file),
        class_name,
    ]
    print("\n>>>", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    out = _find_mp4(scene_file, class_name, quality)
    if out is None:
        raise FileNotFoundError(f"Rendered mp4 not found for {class_name}")
    print(f"    OK → {out}")
    return out


def merge_videos(clips: list[Path], output: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg not found on PATH — install FFmpeg to merge clips.")

    lines = []
    for c in clips:
        # ffmpeg concat demuxer wants forward slashes / escaped quotes
        path = c.resolve().as_posix().replace("'", r"'\''")
        lines.append(f"file '{path}'")
    CONCAT_LIST.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(CONCAT_LIST),
        "-c",
        "copy",
        str(output),
    ]
    print("\n>>>", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    print(f"\nFinal film → {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render & merge DSE Math Visual scenes")
    parser.add_argument("--ql", action="store_true", help="Low quality preview (-ql)")
    parser.add_argument("--qh", action="store_true", help="High quality (-qh)")
    parser.add_argument("--qk", action="store_true", help="4K (-qk)")
    parser.add_argument("--merge-only", action="store_true", help="Skip render, only concat")
    parser.add_argument(
        "--scenes",
        nargs="*",
        default=None,
        help="Optional subset of class names to render",
    )
    args = parser.parse_args()

    if args.qk:
        quality = "-qk"
    elif args.qh:
        quality = "-qh"
    elif args.ql:
        quality = "-ql"
    else:
        quality = "-qm"  # 1080p default medium

    selected = SCENES
    if args.scenes:
        wanted = set(args.scenes)
        selected = [s for s in SCENES if s[1] in wanted]
        if not selected:
            print("No matching scenes.", file=sys.stderr)
            return 1

    clips: list[Path] = []
    if args.merge_only:
        for scene_file, class_name, _key in selected:
            mp4 = _find_mp4(scene_file, class_name, quality)
            if mp4 is None:
                print(f"Missing clip for {class_name}", file=sys.stderr)
                return 1
            clips.append(mp4)
    else:
        for scene_file, class_name, _key in selected:
            clips.append(render_scene(scene_file, class_name, quality))

        # Stitch per-scene SFX sidecars into one film-length cue sheet
        try:
            from config import merge_sfx_sidecars

            keys = [s[2] for s in selected]
            merged = merge_sfx_sidecars(keys, SFX_PATH)
            data = json.loads(merged.read_text(encoding="utf-8"))
            print(
                f"SFX markers: {len(data.get('markers', []))} events, "
                f"{data.get('total_seconds')}s → {SFX_PATH}"
            )
        except Exception as exc:
            print(f"(SFX merge skipped: {exc})")

    merge_videos(clips, FINAL_OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
