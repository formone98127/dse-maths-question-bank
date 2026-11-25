"""
Shared Manim helpers: glow nodes, labels, camera moves, marked play/wait.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from manim import (
    BLUE,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Animation,
    AnimationGroup,
    Circle,
    Dot,
    MathTex,
    MovingCameraScene,
    Text,
    VGroup,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    ReplacementTransform,
    Transform,
    Write,
    always_redraw,
    interpolate_color,
    np,
)

from config import (
    AHA_WAIT,
    ALGEBRA_BLUE,
    BEAT_WAIT,
    CJK_FONT,
    DATA_ORANGE,
    GEOMETRY_GREEN,
    GOLD,
    GUIDE_SIZE,
    HIGHLIGHT,
    HOLD_WAIT,
    LABEL_SIZE,
    MICRO_SIZE,
    SFX,
    TITLE_SIZE,
)


# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
def cjk(
    text: str,
    *,
    font_size: int = LABEL_SIZE,
    color=HIGHLIGHT,
    weight: str = "MEDIUM",
    **kwargs,
) -> Text:
    """Short Traditional Chinese label (2–6 chars preferred)."""
    return Text(
        text,
        font=CJK_FONT,
        font_size=font_size,
        color=color,
        weight=weight,
        **kwargs,
    )


def micro(text: str, color=HIGHLIGHT) -> Text:
    return cjk(text, font_size=MICRO_SIZE, color=color)


def title_label(text: str, color=HIGHLIGHT) -> Text:
    return cjk(text, font_size=TITLE_SIZE, color=color, weight="BOLD")


def formula(tex: str, color=HIGHLIGHT, scale: float = 1.0) -> MathTex:
    m = MathTex(tex, color=color)
    m.scale(scale)
    return m


def guide_text(text: str, color=HIGHLIGHT) -> Text:
    """Silent-narration line: short guiding phrase (ideally ≤10 chars)."""
    return cjk(text, font_size=GUIDE_SIZE, color=color, weight="MEDIUM")


class GuideRail:
    """
    Persistent bottom caption that morphs beat-by-beat.
    Sticks to the camera frame so zoom/pan keeps it readable.
    """

    def __init__(self, scene: MovingCameraScene, *, color=HIGHLIGHT):
        self.scene = scene
        self.color = color
        self.current: Text | None = None
        self._base_height: float | None = None

    def _attach(self, mob: Text) -> None:
        frame = self.scene.camera.frame
        if self._base_height is None:
            self._base_height = float(frame.height)

        def _stick(m, _dt=0):
            # Keep roughly constant on-screen size & pin near bottom centre
            scale = frame.height / self._base_height
            target_h = 0.42 * scale
            if m.height > 1e-6:
                m.set_height(target_h)
            m.move_to(frame.get_bottom() + UP * (0.55 * scale))

        mob.add_updater(_stick)
        _stick(mob)

    def show(
        self,
        text: str,
        *,
        color=None,
        run_time: float = 0.9,
        event: str | None = "guide",
    ) -> Text:
        col = color if color is not None else self.color
        nxt = guide_text(text, color=col)
        frame = self.scene.camera.frame
        if self._base_height is None:
            self._base_height = float(frame.height)
        # Park at bottom centre before animating (no updater yet)
        scale = frame.height / self._base_height
        nxt.move_to(frame.get_bottom() + UP * (0.55 * scale))

        if self.current is None:
            marked_play(
                self.scene,
                FadeIn(nxt, shift=UP * 0.15),
                run_time=run_time,
                event=event,
                note=text,
                intensity="soft",
            )
        else:
            self.current.clear_updaters()
            nxt.move_to(self.current.get_center())
            marked_play(
                self.scene,
                ReplacementTransform(self.current, nxt),
                run_time=run_time,
                event=event,
                note=text,
                intensity="soft",
            )
        self._attach(nxt)
        self.current = nxt
        return nxt

    def clear(self, *, run_time: float = 0.6) -> None:
        if self.current is None:
            return
        self.current.clear_updaters()
        marked_play(
            self.scene,
            FadeOut(self.current),
            run_time=run_time,
            event="guide_clear",
        )
        self.current = None


# ---------------------------------------------------------------------------
# Glow / nodes
# ---------------------------------------------------------------------------
def glow_dot(
    point=ORIGIN,
    *,
    color=HIGHLIGHT,
    radius: float = 0.12,
    glow_radius: float = 0.45,
    glow_opacity: float = 0.35,
) -> VGroup:
    core = Dot(point=point, radius=radius, color=color)
    aura = Circle(radius=glow_radius, color=color, stroke_width=0).move_to(point)
    aura.set_fill(color, opacity=glow_opacity)
    return VGroup(aura, core)


def pillar_node(
    label: str,
    color,
    *,
    radius: float = 0.55,
) -> VGroup:
    """Category node: glowing disc + micro CJK label underneath."""
    ring = Circle(radius=radius, color=color, stroke_width=3)
    fill = Circle(radius=radius * 0.92, color=color, stroke_width=0)
    fill.set_fill(color, opacity=0.18)
    core = Dot(radius=0.14, color=color)
    aura = Circle(radius=radius * 1.35, color=color, stroke_width=0)
    aura.set_fill(color, opacity=0.12)
    txt = micro(label, color=color)
    txt.next_to(ring, DOWN, buff=0.28)
    return VGroup(aura, fill, ring, core, txt)


def soft_pulse(mobject, color=GOLD, scale_factor: float = 1.15) -> Indicate:
    return Indicate(mobject, color=color, scale_factor=scale_factor)


# ---------------------------------------------------------------------------
# Camera helpers (Infinite Canvas feel)
# ---------------------------------------------------------------------------
def camera_frame(scene: MovingCameraScene):
    return scene.camera.frame


def smooth_zoom(
    scene: MovingCameraScene,
    target,
    *,
    scale: float | None = None,
    run_time: float = 2.0,
    event: str | None = None,
) -> None:
    frame = camera_frame(scene)
    anims = [frame.animate.move_to(target)]
    if scale is not None:
        anims.append(frame.animate.set_height(scale))
    marked_play(scene, *anims, run_time=run_time, event=event or "camera_zoom")


def smooth_pan(
    scene: MovingCameraScene,
    target,
    *,
    run_time: float = 1.8,
    event: str | None = None,
) -> None:
    frame = camera_frame(scene)
    marked_play(
        scene,
        frame.animate.move_to(target),
        run_time=run_time,
        event=event or "camera_pan",
    )


# ---------------------------------------------------------------------------
# Marked play / wait (feeds SFX timeline)
# ---------------------------------------------------------------------------
def _infer_run_time(anims: Sequence, kwargs: dict) -> float:
    if "run_time" in kwargs and kwargs["run_time"] is not None:
        return float(kwargs["run_time"])
    times: list[float] = []
    for a in anims:
        if isinstance(a, Animation):
            times.append(float(getattr(a, "run_time", 1.0) or 1.0))
        elif isinstance(a, AnimationGroup):
            times.append(float(getattr(a, "run_time", 1.0) or 1.0))
    return max(times) if times else 1.0


def marked_play(
    scene,
    *anims,
    event: str | None = None,
    note: str = "",
    intensity: str = "med",
    **kwargs,
) -> None:
    rt = _infer_run_time(anims, kwargs)
    kwargs.setdefault("run_time", rt)
    scene.play(*anims, **kwargs)
    SFX.advance(float(kwargs["run_time"]))
    if event:
        SFX.mark(event, note=note, intensity=intensity)


def marked_wait(
    scene,
    duration: float = BEAT_WAIT,
    *,
    event: str | None = None,
    note: str = "",
) -> None:
    scene.wait(duration)
    SFX.advance(duration)
    if event:
        SFX.mark(event, note=note, intensity="soft")


def aha(scene, duration: float = AHA_WAIT, *, note: str = "aha") -> None:
    marked_wait(scene, duration, event="aha_hold", note=note)


def hold(scene, duration: float = HOLD_WAIT, *, note: str = "hold") -> None:
    marked_wait(scene, duration, event="hold", note=note)


# ---------------------------------------------------------------------------
# Morph utilities
# ---------------------------------------------------------------------------
def morph(scene, source, target, *, run_time: float = 1.6, event: str = "morph") -> None:
    marked_play(
        scene,
        ReplacementTransform(source, target),
        run_time=run_time,
        event=event,
        intensity="high",
    )


def flash_intersection(scene, point, color=GOLD) -> None:
    spark = glow_dot(point, color=color, radius=0.08, glow_radius=0.55, glow_opacity=0.55)
    marked_play(
        scene,
        GrowFromCenter(spark),
        run_time=0.45,
        event="intersection_flash",
        intensity="high",
    )
    marked_play(scene, FadeOut(spark), run_time=0.4)


# ---------------------------------------------------------------------------
# Particle cloud → ordered structure
# ---------------------------------------------------------------------------
def random_particles(
    n: int = 48,
    *,
    colors: Iterable | None = None,
    spread: float = 5.5,
    seed: int = 42,
) -> VGroup:
    rng = np.random.default_rng(seed)
    palette = list(colors) if colors else [ALGEBRA_BLUE, GEOMETRY_GREEN, DATA_ORANGE, HIGHLIGHT]
    dots = VGroup()
    for i in range(n):
        p = rng.uniform(-spread, spread, size=2)
        c = palette[i % len(palette)]
        dots.add(Dot(point=[p[0], p[1], 0], radius=0.05, color=c))
    return dots


class MarkedMovingCameraScene(MovingCameraScene):
    """MovingCameraScene that auto-starts/ends SFX scene blocks."""

    scene_key: str = "unnamed"

    def setup(self):
        super().setup()
        SFX.begin_scene(self.scene_key)

    def tear_down(self):
        SFX.end_scene(self.scene_key)
        SFX.dump()
        super().tear_down()
