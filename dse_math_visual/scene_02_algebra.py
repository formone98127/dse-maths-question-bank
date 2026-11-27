"""
Scene 02 — Number & Algebra (~150s)
Linear → quadratic → functions → sequences → inequalities.
Silent guide rail leads every beat.
"""

from __future__ import annotations

from manim import *
import numpy as np

from config import ALGEBRA_BLUE, GEOMETRY_GREEN, GOLD, HIGHLIGHT
from utils import (
    GuideRail,
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


class AlgebraArc(MarkedMovingCameraScene):
    scene_key = "02_algebra"

    def construct(self):
        self.camera.frame.set_height(8)
        guide = GuideRail(self, color=ALGEBRA_BLUE)

        chapter = cjk("數與代數", font_size=40, color=ALGEBRA_BLUE)
        chapter.to_edge(UL, buff=0.45)
        guide.show("第一章・數與代數", color=ALGEBRA_BLUE)
        marked_play(self, FadeIn(chapter), run_time=1.0, event="chapter_label")

        # A. Numbers → variables
        guide.show("由數字開始", color=HIGHLIGHT)
        nums = VGroup(
            *[formula(str(n), color=ALGEBRA_BLUE) for n in (1, 2, 3, 5, 8)]
        ).arrange(RIGHT, buff=0.55)
        marked_play(
            self,
            LaggedStart(*[Write(n) for n in nums], lag_ratio=0.15),
            run_time=2.0,
            event="numbers_in",
        )
        marked_wait(self, 0.8)

        guide.show("變成未知數", color=GOLD)
        vars_ = VGroup(
            formula("a", color=ALGEBRA_BLUE),
            formula("b", color=ALGEBRA_BLUE),
            formula("x", color=GOLD),
            formula("y", color=ALGEBRA_BLUE),
            formula("n", color=ALGEBRA_BLUE),
        ).arrange(RIGHT, buff=0.55)
        marked_play(
            self,
            ReplacementTransform(nums, vars_),
            run_time=2.0,
            event="num_to_var",
            intensity="high",
        )
        tag = micro("變數", color=ALGEBRA_BLUE).next_to(vars_, DOWN, buff=0.45)
        marked_play(self, FadeIn(tag), run_time=0.7, event="label_var")
        aha(self, 1.8, note="variables")

        # B. Linear equation
        guide.show("用方程找答案", color=ALGEBRA_BLUE)
        marked_play(self, FadeOut(tag), run_time=0.4)
        eq1 = formula(r"2x+1=7", color=HIGHLIGHT).scale(1.35)
        marked_play(
            self,
            ReplacementTransform(vars_, eq1),
            run_time=1.8,
            event="linear_eq",
            intensity="high",
        )
        micro_eq = micro("方程", color=ALGEBRA_BLUE).next_to(eq1, DOWN, buff=0.4)
        marked_play(self, FadeIn(micro_eq), run_time=0.6)
        aha(self, 1.5, note="equation")

        guide.show("逐步化簡", color=HIGHLIGHT)
        eq2 = formula(r"2x=6", color=HIGHLIGHT).scale(1.35)
        marked_play(
            self,
            ReplacementTransform(eq1, eq2),
            FadeOut(micro_eq),
            run_time=1.5,
            event="eq_simplify",
        )
        marked_wait(self, 0.8)

        guide.show("解出來了", color=GOLD)
        eq3 = formula(r"x=3", color=GOLD).scale(1.5)
        marked_play(
            self,
            ReplacementTransform(eq2, eq3),
            run_time=1.4,
            event="eq_solve",
            intensity="high",
        )
        flash = glow_dot(eq3.get_center(), color=GOLD, radius=0.1, glow_radius=0.7)
        marked_play(self, GrowFromCenter(flash), run_time=0.4, event="solve_flash", intensity="high")
        marked_play(self, FadeOut(flash), run_time=0.35)
        aha(self, 1.8, note="solved")

        # C. Graphs
        guide.show("放到坐標上看", color=ALGEBRA_BLUE)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 8, 1],
            x_length=8,
            y_length=5.5,
            axis_config={"color": HIGHLIGHT, "stroke_opacity": 0.35, "tip_length": 0.15},
        ).shift(DOWN * 0.15)

        marked_play(
            self,
            ReplacementTransform(eq3, axes),
            run_time=2.0,
            event="axes_appear",
        )

        guide.show("一次函數・直線", color=ALGEBRA_BLUE)
        line = axes.plot(lambda x: 0.8 * x + 1.5, color=ALGEBRA_BLUE, stroke_width=4)
        line_lab = micro("直線", color=ALGEBRA_BLUE).next_to(axes, UP, buff=0.2)
        marked_play(self, Create(line), FadeIn(line_lab), run_time=1.8, event="linear_graph")
        aha(self, 1.5, note="linear_line")

        guide.show("二次函數・拋物線", color=GOLD)
        para = axes.plot(lambda x: 0.45 * x**2 - 0.2, color=ALGEBRA_BLUE, stroke_width=4)
        para_lab = micro("拋物線", color=GOLD).next_to(axes, UP, buff=0.2)
        marked_play(
            self,
            ReplacementTransform(line, para),
            ReplacementTransform(line_lab, para_lab),
            run_time=2.4,
            event="line_to_parabola",
            intensity="high",
        )
        aha(self, 2.0, note="quadratic")

        guide.show("根在這裏", color=GOLD)
        r = float(np.sqrt(0.2 / 0.45))
        root_dots = VGroup(
            glow_dot(axes.c2p(-r, 0), color=GOLD, radius=0.08, glow_radius=0.35),
            glow_dot(axes.c2p(r, 0), color=GOLD, radius=0.08, glow_radius=0.35),
        )
        marked_play(
            self,
            LaggedStart(*[GrowFromCenter(d) for d in root_dots], lag_ratio=0.2),
            run_time=1.2,
            event="roots_flash",
            intensity="high",
        )
        root_tex = formula(r"x=\pm\sqrt{\dfrac{b}{a}}", color=GOLD).scale(0.7)
        root_tex.next_to(axes, DOWN, buff=0.25)
        marked_play(self, Write(root_tex), run_time=1.4, event="root_formula")
        aha(self, 2.0, note="roots")

        # D. Functions
        guide.show("寫成函數形式", color=ALGEBRA_BLUE)
        marked_play(
            self,
            FadeOut(root_dots),
            FadeOut(root_tex),
            FadeOut(para_lab),
            run_time=0.6,
        )
        f_tex = formula(r"f(x)=x^{2}", color=HIGHLIGHT).scale(1.3)
        f_tex.move_to(UP * 2.6)
        marked_play(self, Write(f_tex), run_time=1.2, event="function_notation")
        fn_lab = micro("函數", color=ALGEBRA_BLUE).next_to(f_tex, RIGHT, buff=0.35)
        marked_play(self, FadeIn(fn_lab), run_time=0.6)
        aha(self, 1.6, note="function")

        guide.show("改變式子・圖形變", color=GOLD)
        f2 = formula(r"f(x)=x^{2}-2x-3", color=HIGHLIGHT).scale(1.05)
        f2.move_to(f_tex)
        new_para = axes.plot(
            lambda x: x**2 - 2 * x - 3, x_range=[-2.2, 4.2], color=ALGEBRA_BLUE, stroke_width=4
        )
        marked_play(
            self,
            ReplacementTransform(f_tex, f2),
            ReplacementTransform(para, new_para),
            FadeOut(fn_lab),
            run_time=2.2,
            event="function_shift",
            intensity="high",
        )
        guide.show("頂點在最低處", color=GOLD)
        vertex = glow_dot(axes.c2p(1, -4), color=GOLD, radius=0.09, glow_radius=0.4)
        marked_play(self, GrowFromCenter(vertex), run_time=0.7, event="vertex_flash", intensity="high")
        aha(self, 1.8, note="vertex")

        # E. Sequences
        marked_play(
            self,
            FadeOut(axes),
            FadeOut(new_para),
            FadeOut(vertex),
            FadeOut(f2),
            FadeOut(chapter),
            run_time=1.0,
        )
        self.camera.frame.move_to(ORIGIN)

        guide.show("數列・找規律", color=ALGEBRA_BLUE)
        seq_label = micro("數列", color=ALGEBRA_BLUE).to_edge(UP, buff=0.55)
        marked_play(self, FadeIn(seq_label), run_time=0.6)

        terms = VGroup(
            *[formula(str(t), color=ALGEBRA_BLUE) for t in (2, 5, 8, 11, 14)]
        ).arrange(RIGHT, buff=0.7)
        marked_play(
            self,
            LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in terms], lag_ratio=0.12),
            run_time=1.8,
            event="arith_seq",
        )
        guide.show("等差・每次加固定", color=GOLD)
        diffs = VGroup()
        for i in range(4):
            brace = MathTex("+3", color=GOLD).scale(0.55)
            brace.next_to(VGroup(terms[i], terms[i + 1]), UP, buff=0.15)
            diffs.add(brace)
        marked_play(
            self,
            LaggedStart(*[FadeIn(d) for d in diffs], lag_ratio=0.1),
            run_time=1.2,
            event="common_diff",
        )
        aha(self, 1.5, note="AP")

        guide.show("通項公式", color=HIGHLIGHT)
        general = formula(r"a_n=a_1+(n-1)d", color=HIGHLIGHT).scale(1.1)
        general.next_to(terms, DOWN, buff=0.9)
        marked_play(
            self,
            FadeOut(diffs),
            Write(general),
            run_time=1.8,
            event="AP_formula",
            intensity="high",
        )
        aha(self, 2.0, note="AP_formula")

        guide.show("等比・每次乘固定", color=GOLD)
        geo_terms = VGroup(
            *[formula(str(t), color=ALGEBRA_BLUE) for t in (3, 6, 12, 24, 48)]
        ).arrange(RIGHT, buff=0.7)
        geo_gen = formula(r"a_n=a_1\,r^{n-1}", color=HIGHLIGHT).scale(1.1)
        geo_gen.move_to(general)
        geo_lab = micro("等比", color=GOLD).to_edge(UP, buff=0.55)
        marked_play(
            self,
            ReplacementTransform(terms, geo_terms),
            ReplacementTransform(general, geo_gen),
            ReplacementTransform(seq_label, geo_lab),
            run_time=2.2,
            event="AP_to_GP",
            intensity="high",
        )
        aha(self, 2.2, note="GP")

        # F. Inequality
        marked_play(
            self,
            FadeOut(geo_terms),
            FadeOut(geo_gen),
            FadeOut(geo_lab),
            run_time=0.8,
        )

        guide.show("不等式・一條射線", color=ALGEBRA_BLUE)
        ineq = formula(r"x>2", color=HIGHLIGHT).scale(1.4)
        marked_play(self, Write(ineq), run_time=1.0, event="ineq_tex")
        number_line = NumberLine(
            x_range=[-1, 6, 1],
            length=10,
            color=HIGHLIGHT,
            include_numbers=True,
            font_size=28,
        ).shift(DOWN * 1.2)
        marked_play(
            self,
            ineq.animate.next_to(number_line, UP, buff=0.8),
            Create(number_line),
            run_time=1.6,
            event="number_line",
        )

        open_dot = Circle(radius=0.12, color=GOLD, stroke_width=4).move_to(number_line.n2p(2))
        ray = Arrow(
            number_line.n2p(2.15),
            number_line.n2p(5.8),
            buff=0,
            color=ALGEBRA_BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.08,
        )
        marked_play(
            self,
            Create(open_dot),
            GrowArrow(ray),
            run_time=1.5,
            event="ineq_ray",
            intensity="high",
        )
        ray_lab = micro("不等式", color=ALGEBRA_BLUE).next_to(ineq, RIGHT, buff=0.4)
        marked_play(self, FadeIn(ray_lab), run_time=0.6)
        hold(self, 2.2, note="algebra_close")

        guide.show("下一站・圖形空間", color=GEOMETRY_GREEN)
        portal = glow_dot(RIGHT * 5.5, color=GEOMETRY_GREEN, radius=0.2, glow_radius=0.9)
        marked_play(
            self,
            FadeOut(ineq),
            FadeOut(ray_lab),
            FadeOut(number_line),
            FadeOut(open_dot),
            FadeOut(ray),
            GrowFromCenter(portal),
            self.camera.frame.animate.move_to(RIGHT * 5.5).set_height(4),
            run_time=2.2,
            event="handoff_geometry",
            intensity="high",
        )
        marked_wait(self, 0.5)
        guide.clear()
