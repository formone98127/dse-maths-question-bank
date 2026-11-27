"""
Scene 03 — Measures, Shape & Space (~150s)
Point → line → triangle → circle → similarity → coordinates → trig.
"""

from __future__ import annotations

from manim import *
import numpy as np

from config import GEOMETRY_GREEN, GOLD, HIGHLIGHT, ALGEBRA_BLUE, DATA_ORANGE
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


class GeometryArc(MarkedMovingCameraScene):
    scene_key = "03_geometry"

    def construct(self):
        self.camera.frame.set_height(8).move_to(ORIGIN)
        guide = GuideRail(self, color=GEOMETRY_GREEN)

        chapter = cjk("圖形空間", font_size=40, color=GEOMETRY_GREEN)
        chapter.to_edge(UL, buff=0.45)
        guide.show("第二章・圖形空間", color=GEOMETRY_GREEN)
        marked_play(self, FadeIn(chapter), run_time=0.9, event="chapter_label")

        # A. Point → Line → Triangle
        guide.show("由一點開始", color=HIGHLIGHT)
        p1 = glow_dot(LEFT * 2.8 + DOWN * 1.2, color=GEOMETRY_GREEN)
        marked_play(self, GrowFromCenter(p1), run_time=0.7, event="point")
        p2 = glow_dot(RIGHT * 2.8 + DOWN * 1.2, color=GEOMETRY_GREEN)
        marked_play(self, GrowFromCenter(p2), run_time=0.5, event="point2")
        guide.show("兩點成線", color=GEOMETRY_GREEN)
        seg = Line(p1[1].get_center(), p2[1].get_center(), color=GEOMETRY_GREEN, stroke_width=4)
        marked_play(self, Create(seg), run_time=1.0, event="segment")
        marked_wait(self, 0.6)

        guide.show("三點成面", color=GOLD)
        p3 = glow_dot(UP * 2.0, color=GOLD)
        marked_play(self, GrowFromCenter(p3), run_time=0.6, event="apex")
        tri = Polygon(
            p1[1].get_center(),
            p2[1].get_center(),
            p3[1].get_center(),
            color=GEOMETRY_GREEN,
            stroke_width=4,
        )
        tri.set_fill(GEOMETRY_GREEN, opacity=0.12)
        marked_play(
            self,
            FadeOut(seg),
            FadeOut(p1),
            FadeOut(p2),
            FadeOut(p3),
            Create(tri),
            run_time=1.6,
            event="triangle_form",
            intensity="high",
        )
        tri_lab = micro("三角形", color=GEOMETRY_GREEN).next_to(tri, DOWN, buff=0.4)
        marked_play(self, FadeIn(tri_lab), run_time=0.6)
        aha(self, 1.8, note="triangle")

        # B. Angle sum
        guide.show("三角之內角和", color=GOLD)
        verts = tri.get_vertices()
        line_ab = Line(verts[0], verts[1], color=GEOMETRY_GREEN)
        line_bc = Line(verts[1], verts[2], color=GEOMETRY_GREEN)
        line_ca = Line(verts[2], verts[0], color=GEOMETRY_GREEN)
        a0 = Angle(line_ca, line_ab, radius=0.4, color=GOLD)
        a1 = Angle(line_ab, line_bc, radius=0.4, color=GOLD)
        a2 = Angle(line_bc, line_ca, radius=0.4, color=GOLD)
        marked_play(
            self,
            Create(a0),
            Create(a1),
            Create(a2),
            run_time=1.4,
            event="angles_mark",
        )
        sum_tex = formula(r"A+B+C=180^\circ", color=GOLD).scale(0.95)
        sum_tex.next_to(tri_lab, DOWN, buff=0.35)
        marked_play(self, Write(sum_tex), run_time=1.4, event="angle_sum", intensity="high")
        aha(self, 2.0, note="angle_sum")

        # C. Similarity
        guide.show("放大縮小・仍相似", color=GOLD)
        marked_play(
            self,
            FadeOut(a0),
            FadeOut(a1),
            FadeOut(a2),
            FadeOut(sum_tex),
            FadeOut(tri_lab),
            run_time=0.7,
        )
        small = tri.copy().scale(0.5).move_to(LEFT * 3.3)
        large = tri.copy().scale(1.05).move_to(RIGHT * 2.5)
        marked_play(
            self,
            Transform(tri, small),
            FadeIn(large),
            run_time=2.0,
            event="similarity_split",
            intensity="high",
        )
        sim_lab = micro("相似", color=GOLD).move_to(UP * 2.8)
        marked_play(self, FadeIn(sim_lab), run_time=0.6)
        guide.show("對應邊成比例", color=HIGHLIGHT)
        ratio = formula(r"\dfrac{a}{a'}=\dfrac{b}{b'}", color=HIGHLIGHT).scale(0.9)
        ratio.next_to(sim_lab, DOWN, buff=0.3)
        marked_play(self, Write(ratio), run_time=1.5, event="sim_ratio", intensity="high")
        aha(self, 2.0, note="similarity")

        # D. Circle
        guide.show("進入圓的世界", color=GEOMETRY_GREEN)
        marked_play(
            self,
            FadeOut(tri),
            FadeOut(large),
            FadeOut(sim_lab),
            FadeOut(ratio),
            run_time=0.8,
        )
        circle = Circle(radius=2.2, color=GEOMETRY_GREEN, stroke_width=4)
        center = glow_dot(ORIGIN, color=GOLD, radius=0.08, glow_radius=0.3)
        marked_play(
            self,
            Create(circle),
            GrowFromCenter(center),
            run_time=1.5,
            event="circle_in",
        )
        circ_lab = micro("圓", color=GEOMETRY_GREEN).next_to(circle, DOWN, buff=0.45)
        marked_play(self, FadeIn(circ_lab), run_time=0.5)

        guide.show("直徑對直角", color=GOLD)
        A = circle.point_at_angle(PI)
        B = circle.point_at_angle(0)
        C = circle.point_at_angle(PI / 2.4)
        diam = Line(A, B, color=GOLD, stroke_width=3)
        chord1 = Line(A, C, color=HIGHLIGHT, stroke_width=2.5)
        chord2 = Line(B, C, color=HIGHLIGHT, stroke_width=2.5)
        marked_play(self, Create(diam), run_time=1.0, event="diameter")
        marked_play(self, Create(chord1), Create(chord2), run_time=1.2, event="inscribed")
        right = RightAngle(chord1, chord2, length=0.28, color=GOLD)
        marked_play(self, Create(right), run_time=0.8, event="angle_in_semicircle", intensity="high")
        thm = formula(r"90^\circ", color=GOLD).scale(0.9)
        thm.next_to(C, UP, buff=0.25)
        marked_play(self, FadeIn(thm), run_time=0.6)
        aha(self, 2.2, note="semicircle_theorem")

        # E. Coordinates
        guide.show("圖形遇上代數", color=ALGEBRA_BLUE)
        marked_play(
            self,
            FadeOut(circle),
            FadeOut(center),
            FadeOut(circ_lab),
            FadeOut(diam),
            FadeOut(chord1),
            FadeOut(chord2),
            FadeOut(right),
            FadeOut(thm),
            FadeOut(chapter),
            run_time=1.0,
        )
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=9,
            y_length=6,
            axis_config={"color": HIGHLIGHT, "stroke_opacity": 0.4, "tip_length": 0.15},
        )
        coord_lab = micro("坐標", color=ALGEBRA_BLUE).to_edge(UP, buff=0.5)
        marked_play(
            self,
            Create(axes),
            FadeIn(coord_lab),
            run_time=1.6,
            event="coord_plane",
            intensity="high",
        )

        guide.show("用坐標量距離", color=HIGHLIGHT)
        pts = [axes.c2p(-2, -1), axes.c2p(3, -1), axes.c2p(1, 2)]
        dots = VGroup(*[glow_dot(p, color=GEOMETRY_GREEN, radius=0.07, glow_radius=0.28) for p in pts])
        poly = Polygon(*pts, color=GEOMETRY_GREEN, stroke_width=3).set_fill(GEOMETRY_GREEN, opacity=0.1)
        marked_play(
            self,
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15),
            run_time=1.2,
            event="coord_points",
        )
        marked_play(self, Create(poly), run_time=1.2, event="coord_triangle")
        dist = formula(r"d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}", color=HIGHLIGHT).scale(0.75)
        dist.next_to(coord_lab, DOWN, buff=0.25)
        marked_play(self, Write(dist), run_time=1.8, event="distance_formula", intensity="high")
        aha(self, 2.0, note="analytic_geometry")

        # F. Trig
        guide.show("三角函數登場", color=GEOMETRY_GREEN)
        marked_play(
            self,
            FadeOut(axes),
            FadeOut(dots),
            FadeOut(poly),
            FadeOut(dist),
            FadeOut(coord_lab),
            run_time=0.9,
        )
        uc = Circle(radius=2.0, color=GEOMETRY_GREEN, stroke_width=3)
        theta = 40 * DEGREES
        tip = np.array([2 * np.cos(theta), 2 * np.sin(theta), 0.0])
        radius_line = Line(ORIGIN, tip, color=GOLD, stroke_width=3)
        drop = DashedLine(tip, [tip[0], 0, 0], color=HIGHLIGHT, stroke_width=2)
        base = Line(ORIGIN, [tip[0], 0, 0], color=HIGHLIGHT, stroke_width=2)
        marked_play(self, Create(uc), run_time=1.2, event="unit_circle")
        marked_play(
            self,
            Create(radius_line),
            Create(base),
            Create(drop),
            run_time=1.4,
            event="trig_triangle",
        )
        trig = formula(r"\sin\theta,\ \cos\theta,\ \tan\theta", color=GOLD).scale(0.9)
        trig.to_edge(UP, buff=0.55)
        trig_lab = micro("三角", color=GEOMETRY_GREEN).next_to(trig, DOWN, buff=0.2)
        marked_play(self, Write(trig), FadeIn(trig_lab), run_time=1.6, event="trig_labels", intensity="high")
        aha(self, 2.2, note="trigonometry")

        guide.show("邊長比就是角", color=GOLD)
        soh = VGroup(
            formula(r"\sin=\dfrac{opp}{hyp}", color=HIGHLIGHT).scale(0.65),
            formula(r"\cos=\dfrac{adj}{hyp}", color=HIGHLIGHT).scale(0.65),
            formula(r"\tan=\dfrac{opp}{adj}", color=HIGHLIGHT).scale(0.65),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        soh.to_edge(RIGHT, buff=0.6)
        marked_play(
            self,
            LaggedStart(*[FadeIn(s, shift=LEFT * 0.2) for s in soh], lag_ratio=0.2),
            run_time=1.8,
            event="sohcahtoa",
        )
        hold(self, 2.0, note="geometry_close")

        guide.show("下一站・數據處理", color=DATA_ORANGE)
        portal = glow_dot(RIGHT * 5.8 + DOWN * 0.5, color=DATA_ORANGE, radius=0.2, glow_radius=0.85)
        marked_play(
            self,
            FadeOut(uc),
            FadeOut(radius_line),
            FadeOut(base),
            FadeOut(drop),
            FadeOut(trig),
            FadeOut(trig_lab),
            FadeOut(soh),
            GrowFromCenter(portal),
            self.camera.frame.animate.move_to(portal.get_center()).set_height(4.2),
            run_time=2.2,
            event="handoff_data",
            intensity="high",
        )
        marked_wait(self, 0.5)
        guide.clear()
