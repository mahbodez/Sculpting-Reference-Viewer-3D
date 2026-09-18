"""Moving, turning and scaling an object by taking hold of it in the view.

One gizmo for all three: the object's pivot with three arms along the axes,
each ending in a handle, and a ring at the centre.  Drag an arm's handle and
the gesture is held to that axis -- a move along it, a turn about it, a scale
along it; drag the centre and the gesture is free -- a move across the view,
a turn about the line of sight, a scale of the whole.  Which of the three a
drag does is the tool's *mode*, set in the Model panel.

The arms are a fixed length on screen, so the gizmo is the same size to the
hand at every zoom, and every gesture is worked out from where the drag began
rather than step by step, so that a hundred pixels of travel come out as one
exact change and not the sum of a hundred rounded ones.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ..core.linalg import normalize, rotation_matrix
from ..core.scene import Transform

MODES = ("move", "rotate", "scale")
MODE_LABELS = {"move": "Move", "rotate": "Rotate", "scale": "Scale"}

#: The arms' length on screen, in logical pixels, and how close a press has
#: to land to a handle to take hold of it.
ARM_PIXELS = 78.0
HANDLE_RADIUS = 7.0
CENTRE_RADIUS = 11.0
GRAB_SLACK = 5.0
#: A scale is never taken below this, since nothing comes back from nought.
MIN_SCALE = 1e-3


@dataclass(frozen=True)
class Gizmo:
    """Where the gizmo falls on screen this frame."""

    #: The pivot, in logical pixels.
    origin: tuple[float, float]
    #: For each of X, Y, Z: the handle's screen point, whether the arm points
    #: towards the viewer, and the world-space direction it runs along.
    arms: tuple[tuple[tuple[float, float], bool, np.ndarray], ...]
    #: The screen direction of each arm, unit length, for projecting a drag.
    screen_axes: tuple[np.ndarray, ...]


@dataclass
class _Grip:
    """What a drag began from."""

    handle: str
    mode: str
    x: float
    y: float
    world: np.ndarray
    parent: np.ndarray
    origin: np.ndarray
    origin_screen: tuple[float, float]
    axis: np.ndarray | None
    screen_axis: np.ndarray | None
    param: float | None
    plane_point: np.ndarray | None


class ObjectTool:
    """State of the transform gesture and the arithmetic behind it."""

    def __init__(self) -> None:
        self.active = False
        self.mode = "move"
        self.hover_handle: str | None = None
        self.grabbed: str | None = None
        self._grip: _Grip | None = None

    def set_active(self, active: bool) -> None:
        self.active = bool(active)
        if not self.active:
            self.cancel()

    def set_mode(self, mode: str) -> None:
        if mode in MODES:
            self.mode = mode

    def cancel(self) -> None:
        self.grabbed = None
        self._grip = None
        self.hover_handle = None

    @property
    def dragging(self) -> bool:
        return self._grip is not None

    # -- geometry -------------------------------------------------------

    def axes(self, world: np.ndarray) -> list[np.ndarray]:
        """The three directions the arms run along, in world space.

        A move and a turn are along and about the world's axes, which is
        what an artist placing one object beside another wants; a scale is
        along the object's own, because that is the only frame a scale of
        one axis means anything in.
        """
        if self.mode == "scale":
            linear = np.asarray(world, dtype=np.float64)[:3, :3]
            return [normalize(linear[:, index]) for index in range(3)]
        return [np.eye(3)[index] for index in range(3)]

    def gizmo(self, picker, world: np.ndarray) -> Gizmo | None:
        """Where the gizmo for an object at ``world`` falls on screen, or ``None`` if behind."""
        camera = picker.camera
        origin = np.asarray(world, dtype=np.float64)[:3, 3]
        depth = float(np.dot(origin - camera.eye, camera.forward))
        if depth <= 0.0:
            return None
        reach = picker.world_per_pixel(max(depth, 1e-6)) * ARM_PIXELS
        ox, oy, _ = camera.project(origin, picker.width, picker.height)
        arms = []
        screen_axes = []
        for axis in self.axes(world):
            tip = origin + axis * reach
            if float(np.dot(tip - camera.eye, camera.forward)) <= 0.0:
                tip = origin
            tx, ty, _ = camera.project(tip, picker.width, picker.height)
            towards = float(np.dot(axis, camera.forward)) < 0.0
            arms.append(((float(tx), float(ty)), towards, axis))
            direction = np.array([tx - ox, ty - oy], dtype=np.float64)
            length = float(np.linalg.norm(direction))
            screen_axes.append(direction / length if length > 1e-6 else np.array([1.0, 0.0]))
        return Gizmo((float(ox), float(oy)), tuple(arms), tuple(screen_axes))

    def handle_at(self, x: float, y: float, gizmo: Gizmo | None) -> str | None:
        """Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or none."""
        if gizmo is None:
            return None
        if math.hypot(x - gizmo.origin[0], y - gizmo.origin[1]) <= CENTRE_RADIUS + GRAB_SLACK:
            return "centre"
        nearest, best = None, HANDLE_RADIUS + GRAB_SLACK
        for name, (tip, _, _) in zip("xyz", gizmo.arms, strict=True):
            away = math.hypot(x - tip[0], y - tip[1])
            if away <= best:
                nearest, best = name, away
        return nearest

    # -- the gesture ----------------------------------------------------

    def begin(
        self,
        handle: str,
        x: float,
        y: float,
        picker,
        world: np.ndarray,
        parent: np.ndarray,
    ) -> bool:
        """Take hold of ``handle`` on an object standing at ``world`` under ``parent``."""
        gizmo = self.gizmo(picker, world)
        if gizmo is None:
            return False
        origin = np.asarray(world, dtype=np.float64)[:3, 3].copy()
        axis = screen_axis = None
        param = plane_point = None
        if handle in ("x", "y", "z"):
            index = "xyz".index(handle)
            axis = gizmo.arms[index][2]
            screen_axis = gizmo.screen_axes[index]
            if self.mode == "move":
                param = _axis_param(picker, x, y, origin, axis)
                if param is None:
                    return False
        elif self.mode == "move":
            plane_point = picker.plane_point(x, y, origin)
        self._grip = _Grip(
            handle,
            self.mode,
            x,
            y,
            np.asarray(world, dtype=np.float64).copy(),
            np.asarray(parent, dtype=np.float64).copy(),
            origin,
            gizmo.origin,
            axis,
            screen_axis,
            param,
            plane_point,
        )
        self.grabbed = handle
        return True

    def drag(
        self, x: float, y: float, picker, snap_deg: float = 0.0, uniform: bool = True
    ) -> Transform | None:
        """The object's new local transform for the cursor at ``(x, y)``, or ``None`` to hold."""
        grip = self._grip
        if grip is None:
            return None
        if grip.mode == "move":
            world = self._moved(grip, x, y, picker)
        elif grip.mode == "rotate":
            world = self._turned(grip, x, y, picker, snap_deg)
        else:
            world = self._scaled(grip, x, y, uniform)
        if world is None:
            return None
        local = np.linalg.inv(grip.parent) @ world
        return Transform.from_matrix(local)

    def end(self) -> None:
        self.grabbed = None
        self._grip = None

    # -- the three gestures ---------------------------------------------

    @staticmethod
    def _moved(grip: _Grip, x: float, y: float, picker) -> np.ndarray | None:
        if grip.axis is not None:
            param = _axis_param(picker, x, y, grip.origin, grip.axis)
            if param is None or grip.param is None:
                return None
            shift = grip.axis * (param - grip.param)
        else:
            now = picker.plane_point(x, y, grip.origin)
            shift = now - grip.plane_point
        world = grip.world.copy()
        world[:3, 3] += shift
        return world

    @staticmethod
    def _turned(grip: _Grip, x: float, y: float, picker, snap_deg: float) -> np.ndarray | None:
        ox, oy = grip.origin_screen
        start = math.atan2(-(grip.y - oy), grip.x - ox)
        now = math.atan2(-(y - oy), x - ox)
        if math.hypot(x - ox, y - oy) < 4.0 and math.hypot(grip.x - ox, grip.y - oy) < 4.0:
            return None
        turn = now - start  # counter-clockwise on screen is positive
        towards = -np.asarray(picker.camera.forward, dtype=np.float64)
        if grip.axis is None:
            axis = towards
        else:
            axis = grip.axis
            # An axis pointing away from the viewer turns the other way for
            # the same motion of the hand: the right-hand rule, seen from behind.
            if float(np.dot(axis, towards)) < 0.0:
                turn = -turn
        if snap_deg > 0.0:
            step = math.radians(snap_deg)
            turn = round(turn / step) * step
        rotation = np.eye(4)
        rotation[:3, :3] = rotation_matrix(axis, turn)
        to_origin = np.eye(4)
        to_origin[:3, 3] = -grip.origin
        back = np.eye(4)
        back[:3, 3] = grip.origin
        return back @ rotation @ to_origin @ grip.world

    @staticmethod
    def _scaled(grip: _Grip, x: float, y: float, uniform: bool) -> np.ndarray | None:
        ox, oy = grip.origin_screen
        if grip.screen_axis is not None and not uniform:
            was = float(np.dot((grip.x - ox, grip.y - oy), grip.screen_axis))
            now = float(np.dot((x - ox, y - oy), grip.screen_axis))
            if abs(was) < 1e-6:
                return None
            factor = now / was
            index = "xyz".index(grip.handle)
            factors = np.ones(3)
            factors[index] = factor
        else:
            if grip.screen_axis is not None:
                was = float(np.dot((grip.x - ox, grip.y - oy), grip.screen_axis))
                now = float(np.dot((x - ox, y - oy), grip.screen_axis))
            else:
                was = math.hypot(grip.x - ox, grip.y - oy)
                now = math.hypot(x - ox, y - oy)
            if abs(was) < 1e-6:
                return None
            factor = now / was
            factors = np.full(3, factor)
        # A scale of nought or a mirror is not something a drag should arrive
        # at by accident; the handle stops at the pivot instead.
        factors = np.maximum(factors, MIN_SCALE)
        scale = np.eye(4)
        scale[:3, :3] = np.diag(factors)
        return grip.world @ scale


def _axis_param(picker, x: float, y: float, origin: np.ndarray, axis: np.ndarray) -> float | None:
    """How far along ``axis`` from ``origin`` the point nearest the cursor's ray lies.

    The closest approach of two lines; ``None`` when the axis runs straight
    into the screen, where any answer would be a guess.
    """
    ray_origin, ray_direction = picker.camera.ray(x, y, picker.width, picker.height)
    axis = normalize(axis)
    direction = normalize(ray_direction)
    dot = float(np.dot(axis, direction))
    if abs(dot) > 0.9995:
        return None
    between = np.asarray(ray_origin, dtype=np.float64) - origin
    denominator = 1.0 - dot * dot
    return float((np.dot(between, axis) - dot * np.dot(between, direction)) / denominator)
