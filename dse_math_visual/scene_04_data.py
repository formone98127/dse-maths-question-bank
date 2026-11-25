"""
Scene 04 — Data Handling (~120s)
Scatter → histogram → central tendency → probability → distribution.
"""

from __future__ import annotations

from manim import *
import numpy as np

from config import DATA_ORANGE, DATA_DIM, GOLD, HIGHLIGHT, ALGEBRA_BLUE
from utils import (
    MarkedMovingCameraScene,
    aha,
    cjk,
    formula,
    glow_dot,
    hold,
    marked_play,
    marked_wait,
    micro,
)


class DataArc(MarkedMovingCameraScene):
    scene_key = "04_data"

    def construct(self):
        self.camera.frame.set_height(8).move_to(ORIGIN)
        chapter = cjk("數據處理", font_size=40, color=DATA_ORANGE)
        chapter.to_edge(UL, buff=0.45)
        marked_play(self, FadeIn(chapter), run_time=0.9, event="chapter_label")

        # ================================================================
        # A. Scatter cloud (~20s)
        # ================================================================
        rng = np.random.default_rng(21)
        pts = []
        for _ in range(40):
            x = rng.normal(0, 1.6)
            y = 0.55 * x + rng.normal(0, 0.7)
            pts.append([x, y, 0])
        dots = VGroup(
            *[
                Dot(point=p, radius=0.06, color=DATA_ORANGE).set_opacity(0.85)
                for p in pts
            ]
        )
        marked_play(
            self,
            LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.02),
            run_time=2.2,
            event="scatter_in",
            intensity="soft",
        )
        scat_lab = micro("散點", color=DATA_ORANGE).next_to(dots, DOWN, buff=0.55)
        marked_play(self, FadeIn(scat_lab), run_time=0.5)
        aha(self, 1.6, note="scatter")

        # Trend line
        trend = Line(LEFT * 3.5 + DOWN * 1.9, RIGHT * 3.5 + UP * 1.9, color=GOLD, stroke_width=3)
        marked_play(self, Create(trend), run_time=1.4, event="trend_line", intensity="high")
        aha(self, 1.5, note="correlation")

        # ================================================================
        # B. Morph scatter → histogram (~25s)
        # ================================================================
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"color": HIGHLIGHT, "stroke_opacity": 0.35, "tip_length": 0.12},
        ).shift(DOWN * 0.2)
        heights = [3, 6, 9, 7, 4, 2]
        bars = VGroup()
        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.9,
                height=h * 0.42,
                stroke_width=0,
                fill_color=DATA_ORANGE,
                fill_opacity=0.75,
            )
            bar.move_to(axes.c2p(i + 0.5, 0), DOWN)
            bars.add(bar)

        hist_lab = micro("直方圖", color=DATA_ORANGE)
        marked_play(
            self,
            FadeOut(trend),
            FadeOut(scat_lab),
            ReplacementTransform(dots, bars),
            FadeIn(axes),
            run_time=2.6,
            event="scatter_to_hist",
            intensity="high",
        )
        hist_lab.next_to(axes, UP, buff=0.25)
        marked_play(self, FadeIn(hist_lab), run_time=0.5)
        aha(self, 1.8, note="histogram")

        # ================================================================
        # C. Mean / median (~25s)
        # ================================================================
        # Mean line through histogram
        mean_x = 2.6
        mean_line = DashedLine(
            axes.c2p(mean_x, 0),
            axes.c2p(mean_x, 9),
            color=GOLD,
            stroke_width=3,
        )
        mean_tex = formula(r"\bar{x}", color=GOLD).scale(0.9)
        mean_tex.next_to(mean_line, UP, buff=0.15)
        marked_play(
            self,
            Create(mean_line),
            FadeIn(mean_tex),
            run_time=1.3,
            event="mean_line",
            intensity="high",
        )
        mean_lab = micro("平均", color=GOLD).next_to(hist_lab, RIGHT, buff=0.4)
        marked_play(self, FadeIn(mean_lab), run_time=0.5)
        aha(self, 1.6, note="mean")

        # Median marker slightly offset
        med_x = 2.3
        med_dot = glow_dot(axes.c2p(med_x, 0.3), color=HIGHLIGHT, radius=0.08, glow_radius=0.3)
        med_lab = micro("中位", color=HIGHLIGHT).next_to(med_dot, DOWN, buff=0.25)
        marked_play(
            self,
            GrowFromCenter(med_dot),
            FadeIn(med_lab),
            run_time=1.0,
            event="median",
        )
        aha(self, 1.6, note="median")

        # ================================================================
        # D. Probability (~25s)
        # ================================================================
        marked_play(
            self,
            FadeOut(axes),
            FadeOut(bars),
            FadeOut(hist_lab),
            FadeOut(mean_line),
            FadeOut(mean_tex),
            FadeOut(mean_lab),
            FadeOut(med_dot),
            FadeOut(med_lab),
            FadeOut(chapter),
            run_time=1.0,
        )

        prob_lab = micro("機率", color=DATA_ORANGE).to_edge(UP, buff=0.55)
        marked_play(self, FadeIn(prob_lab), run_time=0.5)

        # Two-branch tree
        root = glow_dot(UP * 2.0, color=GOLD, radius=0.1, glow_radius=0.35)
        left_n = glow_dot(LEFT * 2.8 + DOWN * 0.3, color=DATA_ORANGE)
        right_n = glow_dot(RIGHT * 2.8 + DOWN * 0.3, color=DATA_ORANGE)
        e1 = Line(root.get_center(), left_n.get_center(), color=HIGHLIGHT, stroke_width=2.5)
        e2 = Line(root.get_center(), right_n.get_center(), color=HIGHLIGHT, stroke_width=2.5)
        pL = formula(r"\tfrac{1}{2}", color=HIGHLIGHT).scale(0.7).next_to(e1, UP, buff=0.05)
        pR = formula(r"\tfrac{1}{2}", color=HIGHLIGHT).scale(0.7).next_to(e2, UP, buff=0.05)

        marked_play(self, GrowFromCenter(root), run_time=0.6, event="prob_root")
        marked_play(
            self,
            Create(e1),
            Create(e2),
            GrowFromCenter(left_n),
            GrowFromCenter(right_n),
            FadeIn(pL),
            FadeIn(pR),
            run_time=1.6,
            event="prob_tree",
            intensity="high",
        )

        # Leaf outcomes
        leafL = formula(r"P(A)", color=DATA_ORANGE).scale(0.8).next_to(left_n, DOWN, buff=0.35)
        leafR = formula(r"P(B)", color=DATA_ORANGE).scale(0.8).next_to(right_n, DOWN, buff=0.35)
        marked_play(self, FadeIn(leafL), FadeIn(leafR), run_time=0.8)
        aha(self, 1.8, note="probability_tree")

        # Formula unify
        axiom = formula(r"0\le P\le 1", color=GOLD).scale(1.1)
        axiom.move_to(DOWN * 2.4)
        marked_play(self, Write(axiom), run_time=1.2, event="prob_axiom", intensity="high")
        aha(self, 1.8, note="prob_bound")

        # ================================================================
        # E. Distribution curve (~25s)
        # ================================================================
        marked_play(
            self,
            FadeOut(root),
            FadeOut(left_n),
            FadeOut(right_n),
            FadeOut(e1),
            FadeOut(e2),
            FadeOut(pL),
            FadeOut(pR),
            FadeOut(leafL),
            FadeOut(leafR),
            FadeOut(axiom),
            FadeOut(prob_lab),
            run_time=0.9,
        )

        axes2 = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.45, 0.1],
            x_length=9,
            y_length=4.2,
            axis_config={"color": HIGHLIGHT, "stroke_opacity": 0.35, "tip_length": 0.12},
        ).shift(DOWN * 0.35)

        def pdf(x):
            return float(np.exp(-0.5 * x * x) / np.sqrt(2 * np.pi))

        curve = axes2.plot(pdf, color=DATA_ORANGE, stroke_width=4)
        area = axes2.get_area(curve, x_range=[-1, 1], color=DATA_ORANGE, opacity=0.35)

        dist_lab = micro("分布", color=DATA_ORANGE).to_edge(UP, buff=0.5)
        marked_play(self, Create(axes2), FadeIn(dist_lab), run_time=1.2, event="dist_axes")
        marked_play(self, Create(curve), run_time=1.8, event="bell_curve", intensity="high")
        marked_play(self, FadeIn(area), run_time=1.0, event="area_shade")
        sigma = formula(r"P(|X-\mu|<\sigma)", color=GOLD).scale(0.85)
        sigma.next_to(dist_lab, DOWN, buff=0.25)
        marked_play(self, Write(sigma), run_time=1.3, event="one_sigma")
        hold(self, 2.2, note="data_close")

        # Soft dissolve toward unification space
        marked_play(
            self,
            FadeOut(axes2),
            FadeOut(curve),
            FadeOut(area),
            FadeOut(dist_lab),
            FadeOut(sigma),
            self.camera.frame.animate.set_height(10).move_to(ORIGIN),
            run_time=2.0,
            event="handoff_unify",
            intensity="high",
        )
        marked_wait(self, 0.4)
