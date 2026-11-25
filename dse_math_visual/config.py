"""
DSE Math Visual — shared colours, fonts, styles, and SFX cue sheet.
Manim Community Edition v0.18+
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from manim import ManimColor, config as manim_config

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
SFX_PATH = ROOT / "sfx_markers.json"
OUTPUT_DIR = ROOT / "media" / "videos"

# ---------------------------------------------------------------------------
# Colour palette (strict)
# ---------------------------------------------------------------------------
BG = ManimColor("#0D1117")
ALGEBRA_BLUE = ManimColor("#38BDF8")
GEOMETRY_GREEN = ManimColor("#34D399")
DATA_ORANGE = ManimColor("#FB923C")
HIGHLIGHT = ManimColor("#F8FAFC")
GOLD = ManimColor("#FACC15")

# Soft variants for fills / glows
ALGEBRA_DIM = ManimColor("#0EA5E9")
GEOMETRY_DIM = ManimColor("#10B981")
DATA_DIM = ManimColor("#F97316")

# ---------------------------------------------------------------------------
# Manim global look
# ---------------------------------------------------------------------------
manim_config.background_color = BG
manim_config.frame_rate = 30
manim_config.pixel_height = 1080
manim_config.pixel_width = 1920

# ---------------------------------------------------------------------------
# CJK font (Traditional Chinese / Hong Kong glyphs)
# Prefer Noto CJK HK → Microsoft JhengHei → common fallbacks
# ---------------------------------------------------------------------------
_CJK_CANDIDATES = [
    "Noto Sans HK",
    "Noto Sans TC",
    "Noto Sans CJK HK",
    "Noto Sans CJK TC",
    "Microsoft JhengHei",
    "Microsoft JhengHei UI",
    "微軟正黑體",
    "MingLiU_HKSCS",
    "Microsoft YaHei",
    "PingFang HK",
    "Source Han Sans HC",
]


def _resolve_cjk_font() -> str:
    env = os.environ.get("DSE_MATH_CJK_FONT")
    if env:
        return env
    available: set[str] = set()
    try:
        import manimpango

        available = {f.strip() for f in manimpango.list_fonts()}
    except Exception:
        available = set()

    for name in _CJK_CANDIDATES:
        if not available or name in available:
            # Prefer exact match when we have a font list
            if available and name not in available:
                continue
            return name
    return "Microsoft JhengHei"


CJK_FONT = _resolve_cjk_font()

# Typography defaults
LABEL_SIZE = 36
TITLE_SIZE = 56
MICRO_SIZE = 28
FORMULA_SCALE = 1.0

# Breathing / pacing (tuned for ~10 min film across 6 scenes)
AHA_WAIT = 2.4
BEAT_WAIT = 1.8
HOLD_WAIT = 3.0

# ---------------------------------------------------------------------------
# SFX cue sheet recorder
# ---------------------------------------------------------------------------
class SFXRecorder:
    """Accumulate timed visual events → sfx_markers.json for post audio."""

    def __init__(self) -> None:
        self._t = 0.0
        self._markers: list[dict[str, Any]] = []
        self._scene: str | None = None

    def begin_scene(self, name: str) -> None:
        self._scene = name
        self.mark("scene_start", note=name)

    def end_scene(self, name: str | None = None) -> None:
        self.mark("scene_end", note=name or self._scene or "")
        self._scene = None

    def advance(self, dt: float) -> None:
        if dt and dt > 0:
            self._t += float(dt)

    @property
    def time(self) -> float:
        return self._t

    def mark(self, event: str, *, note: str = "", intensity: str = "med") -> None:
        self._markers.append(
            {
                "t": round(self._t, 3),
                "event": event,
                "scene": self._scene,
                "note": note,
                "intensity": intensity,
            }
        )

    def dump(self, path: Path | str | None = None) -> Path:
        """Write this process's markers. Also mirrors a per-scene sidecar file."""
        out = Path(path) if path else SFX_PATH
        payload = {
            "total_seconds": round(self._t, 3),
            "markers": self._markers,
        }
        out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if self._scene:
            side = ROOT / f"sfx_{self._scene}.json"
            side.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return out

    def reset(self) -> None:
        self._t = 0.0
        self._markers.clear()
        self._scene = None


def merge_sfx_sidecars(scene_keys: list[str], out: Path | None = None) -> Path:
    """Concatenate per-scene sfx_*.json files with cumulative time offsets."""
    offset = 0.0
    merged: list[dict[str, Any]] = []
    for key in scene_keys:
        side = ROOT / f"sfx_{key}.json"
        if not side.exists():
            continue
        data = json.loads(side.read_text(encoding="utf-8"))
        for m in data.get("markers", []):
            item = dict(m)
            item["t"] = round(float(m["t"]) + offset, 3)
            item["local_t"] = m["t"]
            merged.append(item)
        offset += float(data.get("total_seconds", 0.0))
    target = out or SFX_PATH
    target.write_text(
        json.dumps(
            {"total_seconds": round(offset, 3), "markers": merged},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return target


SFX = SFXRecorder()
