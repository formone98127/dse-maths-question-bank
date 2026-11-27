"""
Scene 05 — Unification (~80s)
Three pillars reconnect; cross-domain bridges light up.
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
    formula,
    glow_dot,
    hold,
    marked_play,
    marked_wait,
    micro,
    pillar_node,
    title_label,
)


class UnificationArc(MarkedMovingCameraScene):
    scene_key = "05_unification"

    def construct(self):
        self.camera.frame.set_height(9).move_to(ORIGIN)
        guide = GuideRail(self, color=GOLD)

        guide.show("三線重新相遇", color=GOLD)
        left = pillar_node("數與代數", ALGEBRA_BLUE).move_to(LEFT * 4.4 + UP * 0.4)
        mid = pillar_node("圖形空間", GEOMETRY_GREEN).move_to(UP * 0.4)
        right = pillar_node("數據處理", DATA_ORANGE).move_to(RIGHT * 4.4 + UP * 0.4)

        marked_play(
            self,
            LaggedStart(
                GrowFromCenter(left),
                GrowFromCenter(mid),
                GrowFromCenter(right),
                lag_ratio=0.25,
            ),
            run_time=2.4,
            event="pillars_return",
            intensity="high",
        )
        aha(self, 1.6, note="pillars_back")

        # Algebra ↔ Geometry
        guide.show("代數 × 圖形", color=ALGEBRA_BLUE)
        bridge_ag = Line(
            left[3].get_center(),
            mid[3].get_center(),
            color=HIGHLIGHT,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        marked_play(self, Create(bridge_ag), run_time=1.2, event="bridge_ag")
        tag_ag = VGroup(
            micro("坐標", color=GOLD),
            formula(r"(x,y)", color=HIGHLIGHT).scale(0.7),
        ).arrange(DOWN, buff=0.12)
        tag_ag.next_to(bridge_ag, UP, buff=0.25)
        marked_play(self, FadeIn(tag_ag, shift=UP * 0.1), run_time=0.9, event="tag_coord")
        guide.show("橋樑就是坐標", color=GOLD)
        mini = Axes(
            x_range=[-1, 1, 1],
            y_range=[-1, 1, 1],
            x_length=1.4,
            y_length=1.4,
            axis_config={"color": ALGEBRA_BLUE, "stroke_width": 2, "tip_length": 0.1},
        ).move_to(bridge_ag.get_center() + DOWN * 1.1)
        marked_play(self, FadeIn(mini, scale=0.5), run_time=0.9, event="mini_axes")
        aha(self, 1.8, note="alg_geo_link")

        # Geometry ↔ Data
        guide.show("圖形 × 數據", color=GEOMETRY_GREEN)
        bridge_gd = Line(
            mid[3].get_center(),
            right[3].get_center(),
            color=HIGHLIGHT,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        marked_play(self, Create(bridge_gd), run_time=1.2, event="bridge_gd")
        tag_gd = VGroup(
            micro("面積", color=GOLD),
            formula(r"\int", color=HIGHLIGHT).scale(0.9),
        ).arrange(DOWN, buff=0.1)
        tag_gd.next_to(bridge_gd, UP, buff=0.25)
        marked_play(self, FadeIn(tag_gd), run_time=0.8, event="tag_area")
        guide.show("面積代表頻數", color=GOLD)
        aha(self, 1.6, note="geo_data_link")

        # Algebra ↔ Data
        guide.show("代數 × 數據", color=DATA_ORANGE)
        bridge_ad = ArcBetweenPoints(
            left[3].get_center() + DOWN * 0.15,
            right[3].get_center() + DOWN * 0.15,
            angle=-PI / 2.8,
            color=GOLD,
            stroke_width=2.5,
        )
        marked_play(self, Create(bridge_ad), run_time=1.5, event="bridge_ad", intensity="high")
        tag_ad = VGroup(
            micro("模型", color=GOLD),
            formula(r"y=mx+c", color=HIGHLIGHT).scale(0.65),
        ).arrange(DOWN, buff=0.1)
        tag_ad.next_to(bridge_ad, DOWN, buff=0.35)
        marked_play(self, FadeIn(tag_ad), run_time=0.9, event="tag_model")
        guide.show("模型解釋數據", color=GOLD)
        aha(self, 1.8, note="alg_data_link")

        # Nexus
        guide.show("原來本是一體", color=HIGHLIGHT)
        marked_play(self, FadeOut(mini), run_time=0.5)
        nexus = glow_dot(DOWN * 0.2, color=GOLD, radius=0.16, glow_radius=0.75, glow_opacity=0.4)
        centre = (left[3].get_center() + mid[3].get_center() + right[3].get_center()) / 3
        nexus.move_to(centre)
        spokes = VGroup(
            Line(left[3].get_center(), centre, color=GOLD, stroke_opacity=0.45, stroke_width=2),
            Line(mid[3].get_center(), centre, color=GOLD, stroke_opacity=0.45, stroke_width=2),
            Line(right[3].get_center(), centre, color=GOLD, stroke_opacity=0.45, stroke_width=2),
        )
        marked_play(
            self,
            Create(spokes),
            GrowFromCenter(nexus),
            run_time=1.8,
            event="nexus_form",
            intensity="high",
        )
        one = title_label("一體", color=HIGHLIGHT).scale(0.85)
        one.next_to(nexus, DOWN, buff=1.35)
        marked_play(self, FadeIn(one, shift=UP * 0.15), run_time=1.0, event="unity_word")
        hold(self, 2.4, note="unity_hold")

        guide.show("拉開看全圖", color=GOLD)
        marked_play(
            self,
            self.camera.frame.animate.set_height(12).move_to(ORIGIN),
            run_time=2.5,
            event="pullback",
            intensity="high",
        )
        marked_wait(self, 1.2, event="map_settle")
        guide.clear()
