"""
Scene 06 — Outro (~40s)
Full map freeze + channel end card. Zero narration, micro-typography only.
"""

from __future__ import annotations

from manim import *

from config import (
    ALGEBRA_BLUE,
    DATA_ORANGE,
    GEOMETRY_GREEN,
    GOLD,
    HIGHLIGHT,
    SFX,
)
from utils import (
    MarkedMovingCameraScene,
    aha,
    cjk,
    glow_dot,
    hold,
    marked_play,
    marked_wait,
    micro,
    pillar_node,
    title_label,
)


class OutroFinale(MarkedMovingCameraScene):
    scene_key = "06_outro"

    def construct(self):
        self.camera.frame.set_height(11).move_to(ORIGIN)

        # ================================================================
        # A. Reconstruct final knowledge map (~15s)
        # ================================================================
        left = pillar_node("數與代數", ALGEBRA_BLUE).move_to(LEFT * 4.4 + UP * 0.6)
        mid = pillar_node("圖形空間", GEOMETRY_GREEN).move_to(UP * 0.6)
        right = pillar_node("數據處理", DATA_ORANGE).move_to(RIGHT * 4.4 + UP * 0.6)

        centre = (left[3].get_center() + mid[3].get_center() + right[3].get_center()) / 3
        links = VGroup(
            Line(left[3].get_center(), mid[3].get_center(), color=HIGHLIGHT, stroke_opacity=0.5),
            Line(mid[3].get_center(), right[3].get_center(), color=HIGHLIGHT, stroke_opacity=0.5),
            ArcBetweenPoints(
                left[3].get_center(),
                right[3].get_center(),
                angle=-PI / 2.6,
                color=GOLD,
                stroke_opacity=0.55,
            ),
            Line(left[3].get_center(), centre, color=GOLD, stroke_opacity=0.35),
            Line(mid[3].get_center(), centre, color=GOLD, stroke_opacity=0.35),
            Line(right[3].get_center(), centre, color=GOLD, stroke_opacity=0.35),
        )
        nexus = glow_dot(centre, color=GOLD, radius=0.14, glow_radius=0.7)

        map_group = VGroup(links, left, mid, right, nexus)
        marked_play(
            self,
            FadeIn(map_group, scale=0.92),
            run_time=2.0,
            event="final_map_in",
            intensity="high",
        )
        aha(self, 2.0, note="map_freeze")

        # Soft pulse cascade
        for node, key in ((left, "a"), (mid, "g"), (right, "d")):
            marked_play(
                self,
                Indicate(node[2], color=GOLD, scale_factor=1.12),
                run_time=0.55,
                event=f"final_pulse_{key}",
            )

        # ================================================================
        # B. Brand lockup (~15s)
        # ================================================================
        brand = title_label("DSE 數學", color=HIGHLIGHT)
        brand.move_to(UP * 3.2)
        tag = cjk("看見結構", font_size=34, color=GOLD)
        tag.next_to(brand, DOWN, buff=0.22)

        marked_play(
            self,
            map_group.animate.scale(0.82).shift(DOWN * 0.55),
            FadeIn(brand, shift=DOWN * 0.15),
            run_time=1.8,
            event="brand_lock",
            intensity="high",
        )
        marked_play(self, FadeIn(tag), run_time=0.9, event="tagline")
        hold(self, 2.5, note="brand_hold")

        # ================================================================
        # C. End card (~10s)
        # ================================================================
        # Morph tagline → subscribe cue (micro only)
        end = cjk("下集見", font_size=40, color=HIGHLIGHT)
        end.move_to(tag.get_center())
        marked_play(
            self,
            ReplacementTransform(tag, end),
            run_time=1.4,
            event="end_card",
            intensity="high",
        )
        # Fade map softly, leave brand
        marked_play(
            self,
            FadeOut(map_group),
            brand.animate.move_to(UP * 0.4),
            end.animate.next_to(ORIGIN, DOWN, buff=0.55),
            run_time=2.0,
            event="end_simplify",
        )
        hold(self, 2.8, note="outro_hold")

        # Final fade to void
        marked_play(
            self,
            FadeOut(brand),
            FadeOut(end),
            run_time=1.6,
            event="fade_void",
            intensity="soft",
        )
        marked_wait(self, 0.8, event="black")

        # Ensure cue sheet written (tear_down also dumps)
        SFX.dump()
