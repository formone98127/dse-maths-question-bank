"""
Scene 01 — Intro (~60s)
Chaos → order: scattered glyphs coalesce into three DSE pillars.
Silent guide rail leads every beat.
"""

from __future__ import annotations

from manim import *

from config import (
    ALGEBRA_BLUE,
    DATA_ORANGE,
    GEOMETRY_GREEN,
    GOLD,
    HIGHLIGHT,
)
from utils import (
    GuideRail,
    MarkedMovingCameraScene,
    aha,
    cjk,
    formula,
    marked_play,
    marked_wait,
    pillar_node,
    random_particles,
    title_label,
)


class IntroChaosToOrder(MarkedMovingCameraScene):
    scene_key = "01_intro"

    def construct(self):
        guide = GuideRail(self, color=HIGHLIGHT)

        # --- chaos --------------------------------------------------------
        guide.show("從混亂開始", color=HIGHLIGHT)
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
        marked_wait(self, 1.2)

        guide.show("先找出秩序", color=GOLD)
        marked_play(
            self,
            particles.animate.arrange_in_grid(8, 8, buff=0.35).move_to(ORIGIN).set_opacity(0.55),
            run_time=3.0,
            event="chaos_grid_hint",
        )
        marked_wait(self, 1.0)

        # --- glyphs -------------------------------------------------------
        guide.show("數學符號登場", color=HIGHLIGHT)
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
        aha(self, 2.2, note="glyphs_settle")

        # --- three pillars ------------------------------------------------
        guide.show("歸入三大範疇", color=GOLD)
        left = pillar_node("數與代數", ALGEBRA_BLUE).move_to(LEFT * 4.2)
        mid = pillar_node("圖形空間", GEOMETRY_GREEN).move_to(ORIGIN)
        right = pillar_node("數據處理", DATA_ORANGE).move_to(RIGHT * 4.2)

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
        aha(self, 2.2, note="three_pillars")

        # Name each pillar with guide
        for node, phrase, col, key in (
            (left, "① 數與代數", ALGEBRA_BLUE, "algebra"),
            (mid, "② 圖形與空間", GEOMETRY_GREEN, "geometry"),
            (right, "③ 數據處理", DATA_ORANGE, "data"),
        ):
            guide.show(phrase, color=col)
            marked_play(
                self,
                Indicate(node[2], color=GOLD, scale_factor=1.2),
                run_time=0.9,
                event=f"pillar_pulse_{key}",
                intensity="med",
            )
            marked_wait(self, 0.55)

        # --- title --------------------------------------------------------
        guide.show("DSE 數學總覽", color=HIGHLIGHT)
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
        aha(self, 2.4, note="title_hold")

        guide.show("課題彼此相連", color=GOLD)
        link_lm = Line(left.get_center(), mid.get_center(), color=HIGHLIGHT, stroke_opacity=0.35)
        link_mr = Line(mid.get_center(), right.get_center(), color=HIGHLIGHT, stroke_opacity=0.35)
        marked_play(
            self,
            Create(link_lm),
            Create(link_mr),
            run_time=2.0,
            event="preview_links",
        )
        marked_wait(self, 2.2, event="intro_end_hold")

        guide.show("先看數與代數", color=ALGEBRA_BLUE)
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
        marked_wait(self, 0.8)
        guide.clear()
