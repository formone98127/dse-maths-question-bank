"""
Scene 01 — Intro (~60s)
Chaos → order: scattered glyphs coalesce into three DSE pillars.
"""

from __future__ import annotations

from manim import *
import numpy as np

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
    formula,
    glow_dot,
    marked_play,
    marked_wait,
    morph,
    pillar_node,
    random_particles,
    title_label,
)


class IntroChaosToOrder(MarkedMovingCameraScene):
    scene_key = "01_intro"

    def construct(self):
        # --- 0–8s: chaotic particle field ---------------------------------
        particles = random_particles(
            64,
            colors=[ALGEBRA_BLUE, GEOMETRY_GREEN, DATA_ORANGE, HIGHLIGHT, GOLD],
            spread=6.2,
            seed=7,
        )
        marked_play(
            self,
            LaggedStart(*[FadeIn(d, scale=0.3) for d in particles], lag_ratio=0.02),
            run_time=3.0,
            event="chaos_spawn",
            intensity="soft",
        )
        marked_wait(self, 1.5)

        # Drift chaos
        marked_play(
            self,
            particles.animate.arrange_in_grid(8, 8, buff=0.35).move_to(ORIGIN).set_opacity(0.55),
            run_time=3.0,
            event="chaos_grid_hint",
        )
        marked_wait(self, 1.2)

        # --- 8–22s: glyphs emerge from particles --------------------------
        glyphs = VGroup(
            formula(r"x", color=ALGEBRA_BLUE),
            formula(r"\triangle", color=GEOMETRY_GREEN),
            formula(r"\Sigma", color=DATA_ORANGE),
            formula(r"f", color=ALGEBRA_BLUE),
            formula(r"\pi", color=GEOMETRY_GREEN),
            formula(r"P", color=DATA_ORANGE),
            formula(r"a_n", color=ALGEBRA_BLUE),
            formula(r"\theta", color=GEOMETRY_GREEN),
            formula(r"\bar{x}", color=DATA_ORANGE),
        )
        glyphs.arrange_in_grid(3, 3, buff=0.85).scale(0.95)

        marked_play(
            self,
            ReplacementTransform(particles, glyphs),
            run_time=3.2,
            event="glyph_coalesce",
            intensity="high",
        )
        aha(self, 2.4, note="glyphs_settle")

        # --- 22–40s: three pillars crystallise ----------------------------
        left = pillar_node("數與代數", ALGEBRA_BLUE).move_to(LEFT * 4.2)
        mid = pillar_node("圖形空間", GEOMETRY_GREEN).move_to(ORIGIN)
        right = pillar_node("數據處理", DATA_ORANGE).move_to(RIGHT * 4.2)

        # Split glyphs into three colour groups → morph into pillars
        blue_g = VGroup(*[g for g in glyphs if g.color == ALGEBRA_BLUE])
        green_g = VGroup(*[g for g in glyphs if g.color == GEOMETRY_GREEN])
        orange_g = VGroup(*[g for g in glyphs if g.color == DATA_ORANGE])

        # Colour match may fail if MathTex color comparison is odd; fallback by index
        if len(blue_g) == 0:
            blue_g = VGroup(glyphs[0], glyphs[3], glyphs[6])
            green_g = VGroup(glyphs[1], glyphs[4], glyphs[7])
            orange_g = VGroup(glyphs[2], glyphs[5], glyphs[8])

        marked_play(
            self,
            blue_g.animate.arrange(DOWN, buff=0.2).move_to(LEFT * 4.2),
            green_g.animate.arrange(DOWN, buff=0.2).move_to(ORIGIN),
            orange_g.animate.arrange(DOWN, buff=0.2).move_to(RIGHT * 4.2),
            run_time=2.0,
            event="pillar_sort",
        )
        marked_wait(self, 0.5)

        marked_play(
            self,
            ReplacementTransform(blue_g, left),
            ReplacementTransform(green_g, mid),
            ReplacementTransform(orange_g, right),
            run_time=2.6,
            event="pillars_form",
            intensity="high",
        )
        aha(self, 2.5, note="three_pillars")

        # Pulse each pillar
        for node, name in ((left, "algebra"), (mid, "geometry"), (right, "data")):
            marked_play(
                self,
                Indicate(node[2], color=GOLD, scale_factor=1.2),
                run_time=0.9,
                event=f"pillar_pulse_{name}",
                intensity="med",
            )
            marked_wait(self, 0.45)

        # --- 40–60s: title crystallises -----------------------------------
        brand = title_label("DSE 數學", color=HIGHLIGHT)
        brand.move_to(UP * 2.6)
        sub = cjk("視覺總覽", font_size=32, color=GOLD)
        sub.next_to(brand, DOWN, buff=0.25)

        marked_play(
            self,
            FadeIn(brand, shift=UP * 0.2),
            run_time=1.4,
            event="title_in",
            intensity="high",
        )
        marked_play(self, FadeIn(sub, shift=UP * 0.1), run_time=0.9, event="subtitle_in")
        aha(self, 2.8, note="title_hold")

        # Soft link lines between pillars (preview of unification)
        link_lm = Line(left.get_center(), mid.get_center(), color=HIGHLIGHT, stroke_opacity=0.35)
        link_mr = Line(mid.get_center(), right.get_center(), color=HIGHLIGHT, stroke_opacity=0.35)
        marked_play(
            self,
            Create(link_lm),
            Create(link_mr),
            run_time=2.0,
            event="preview_links",
        )
        marked_wait(self, 2.5, event="intro_end_hold")

        # Camera ease into algebra pillar for chapter handoff
        marked_play(
            self,
            self.camera.frame.animate.move_to(left.get_center()).set_height(5.5),
            FadeOut(brand),
            FadeOut(sub),
            FadeOut(link_lm),
            FadeOut(link_mr),
            FadeOut(mid),
            FadeOut(right),
            run_time=2.4,
            event="handoff_algebra",
            intensity="high",
        )
        marked_wait(self, 0.6)
