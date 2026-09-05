"""Drawing onto a pygame surface.

Kept deliberately thin. Everything worth asserting lives in sim.view.camera,
sim.view.geometry and sim.view.scene, all of which are pure; this module is
small enough to be obviously correct by reading.

Nothing here computes physics. It draws what the simulation produced -- see
architecture rule 7 in CLAUDE.md. In particular the star's appearance rests on
Kell's stubbed luminosity, so nothing drawn here is evidence about stellar
physics.

Axioms used: none.
Abstracts: nothing directly; see sim.star for what the star's values rest on.

Depends on: pygame, sim.view.*
Used by: sim.view.app
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Final, cast

import numpy as np
import pygame
from numpy.typing import NDArray

from sim.orbit import Trajectory
from sim.rotation import Spin, is_lit
from sim.star import Kell
from sim.surface import Terrain
from sim.units import LENGTH, Quantity
from sim.view.bands import ScaleBand
from sim.view.camera import Camera
from sim.view.geometry import Disc, contiguous_runs
from sim.view.sidebar import PANEL_WIDTH, ROW_HEIGHT, TOP, Target

__all__ = [
    "OrbitTrace",
    "PlanetDisc",
    "ScaleBar",
    "Sidebar",
    "StarDisc",
    "TerrainTrace",
]

_INK: Final = (232, 236, 228)
_DIM: Final = (96, 108, 100)
_GOLD: Final = (198, 160, 70)
_TEAL: Final = (74, 176, 158)
_DAY: Final = (214, 196, 142)
_NIGHT: Final = (44, 62, 60)
_RULE: Final = (52, 66, 62)
#: Vellum's own marker colour. Distinct from the orbit trace so a test can
#: tell whether the planet was drawn or merely overlapped by its own path.
VELLUM: Final = (126, 214, 200)
_MIN_PLANET_PIXELS: Final = 3

#: Pixel coordinates handed to SDL are clipped to this box. SDL takes C ints,
#: so a coordinate far outside the viewport must never reach it -- see the
#: precision note in sim.view.camera.
_CLIP: Final = 1 << 15


def _point(value: tuple[object, object]) -> tuple[int, int]:
    x = float(cast(float, value[0]))
    y = float(cast(float, value[1]))
    return (
        int(max(-_CLIP, min(_CLIP, x))),
        int(max(-_CLIP, min(_CLIP, y))),
    )


class StarDisc:
    """Kell, drawn at least a pixel across however far out you are.

    Culled when it does not intersect the viewport. Without that, zooming to
    the ground drew a circle of radius 2e7 pixels centred a world unit away and
    filled the screen with gold -- the star is only 0.02 world units across,
    but at 1e9 pixels per unit that is still twenty million pixels.
    """

    bands: Final = frozenset(ScaleBand)

    def __init__(self, star: Kell, radius_world: float = 0.02) -> None:
        self._star = star
        self._radius = radius_world

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        cx = float(cast(float, camera.world_to_screen(0.0, 0.0)[0]))
        cy = float(cast(float, camera.world_to_screen(0.0, 0.0)[1]))
        radius = self._radius * camera.scale

        # Nothing to draw if the disc misses the viewport entirely...
        nearest_x = min(max(cx, 0.0), float(camera.width))
        nearest_y = min(max(cy, 0.0), float(camera.height))
        if math.hypot(cx - nearest_x, cy - nearest_y) > radius:
            return
        # ...and nothing sensible to draw if we are inside it. Being inside the
        # star is not a view; it means the camera is somewhere it should not be,
        # and painting the viewport gold hides that rather than showing it.
        corners = [(0.0, 0.0), (camera.width, 0.0), (0.0, camera.height),
                   (camera.width, camera.height)]
        if all(math.hypot(cx - x, cy - y) < radius for x, y in corners):
            return

        pygame.draw.circle(surface, _GOLD, (int(cx), int(cy)), max(2, int(radius)))


class OrbitTrace:
    """The rosette. Visible until the ground fills the view."""

    bands: Final = frozenset(
        {ScaleBand.SYSTEM, ScaleBand.PLANETARY, ScaleBand.REGIONAL}
    )

    def __init__(self, trajectory: Trajectory, stride: int = 8) -> None:
        self._positions = trajectory.positions[::stride]

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        xs, ys = camera.world_to_screen(self._positions[:, 0], self._positions[:, 1])
        points = [
            _point((x, y))
            for x, y in zip(np.asarray(xs), np.asarray(ys), strict=True)
        ]
        if len(points) > 1:
            pygame.draw.aalines(surface, _DIM, False, points)


class PlanetDisc:
    """Vellum. A bare disc until the surface layer exists.

    Drawn only where the whole disc is meaningful. Closer in, TerrainTrace
    draws the real profile and this would just be a duplicate circle through
    the middle of it.
    """

    bands: Final = frozenset({ScaleBand.SYSTEM, ScaleBand.PLANETARY})

    def __init__(self, planet: Disc, samples: int = 512) -> None:
        self._planet = planet
        self._samples = samples

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        planet = self._planet

        # Below a few pixels the outline has nothing to draw -- at the opening
        # view Vellum's radius is 0.0013 px -- so mark it instead. StarDisc has
        # always had this floor; the planet did not, and simply was not drawn.
        radius_px = planet.radius * camera.scale
        if radius_px < _MIN_PLANET_PIXELS:
            centre = _point(camera.world_to_screen(planet.centre_x, planet.centre_y))
            pygame.draw.circle(surface, VELLUM, centre, _MIN_PLANET_PIXELS)
            return

        # Sample the arc the viewport actually covers, so ground zoom spends its
        # samples where they are visible rather than around the whole world.
        half_arc = min(
            planet.circumference * 0.5,
            camera.width * camera.metres_per_pixel,
        )
        centre_s = 0.0
        s = np.linspace(centre_s - half_arc, centre_s + half_arc, self._samples)
        xs, ys = camera.surface_to_screen(planet, s, np.zeros_like(s))
        points = [
            _point((x, y))
            for x, y in zip(np.asarray(xs), np.asarray(ys), strict=True)
        ]
        if len(points) > 1:
            pygame.draw.aalines(surface, _TEAL, False, points)


class ScaleBar:
    """A bar and a readout. Without it eleven decades of zoom disorient fast.

    It also says when the zoom has passed the terrain's resolution floor. Below
    that there is no more detail, and the ground drawn is the finest the field
    contains rather than something invented -- the viewer should say so instead
    of showing convincing smoothness.
    """

    bands: Final = frozenset(ScaleBand)

    def __init__(self, terrain: Terrain | None = None, spin: Spin | None = None) -> None:
        self._terrain = terrain
        self._spin = spin
        #: Simulation time and whether it is advancing. Set by the caller each
        #: frame. Shown because a world that starts moving on its own is
        #: alarming when nothing on screen says it is running.
        self.time = 0.0
        self.clock_running = True

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        mpp = camera.metres_per_pixel
        # A round number of world units close to 200 px wide.
        raw = 200.0 * mpp
        exponent = np.floor(np.log10(raw))
        span = float(10.0**exponent)
        pixels = int(span / mpp)

        y = camera.height - 28
        left = PANEL_WIDTH + 20
        pygame.draw.line(surface, _INK, (left, y), (left + pixels, y), 1)
        pygame.draw.line(surface, _INK, (left, y - 4), (left, y + 4), 1)
        pygame.draw.line(surface, _INK, (left + pixels, y - 4), (left + pixels, y + 4), 1)

        if pygame.font.get_init():
            font = pygame.font.Font(None, 18)
            label = f"{span:.0e} world units   |   {camera.band.value}"
            if camera.is_clamped:
                label += "   [zoom limit]"
            if self._terrain is not None and self._terrain.is_clamped_at(mpp):
                label += "   [below terrain detail]"
            surface.blit(font.render(label, True, _INK), (left, y + 8))

            state = "running" if self.clock_running else "paused"
            clock = f"t = {self.time:.4f}   [{state} — space]"
            if self._spin is not None and self._spin.sidereal_day > 0.0:
                days = self.time / self._spin.sidereal_day
                clock = f"day {days:.2f}   " + clock
            surface.blit(font.render(clock, True, _DIM), (left, y + 24))


class TerrainTrace:
    """Vellum's ground, sampled at roughly screen resolution.

    Samples only the arc the viewport covers, at about one sample per pixel, so
    the cost is set by the window rather than by the world. Terrain is queried
    at the zoom's own resolution -- a whole-world profile does not pay for metre
    detail, and a metre of ground gets it, down to the terrain's floor.

    Positions reach the screen through ``camera.surface_to_screen``, which
    composes them from the planet centre rather than as absolute world
    coordinates. That is what keeps ground detail from being quantised by the
    planet's distance from Kell.
    """

    bands: Final = frozenset(
        {ScaleBand.GROUND, ScaleBand.REGIONAL, ScaleBand.PLANETARY}
    )

    def __init__(
        self,
        planet: Disc,
        terrain: Terrain,
        samples: int = 900,
        spin: Spin | None = None,
    ) -> None:
        self._planet = planet
        self._terrain = terrain
        self._samples = samples
        self._spin = spin
        #: Simulation time, set by the caller each frame. Only used to decide
        #: which part of the ground is in daylight.
        self.time = 0.0

    def visible_arc(self, camera: Camera) -> NDArray[np.float64]:
        """Return the surface positions this camera can see."""
        planet = self._planet
        # The arc subtended by the viewport, capped at the whole world.
        half = min(
            planet.circumference * 0.5,
            camera.span * 0.75,
        )
        centre = math.atan2(
            camera.focus_y - planet.centre_y, camera.focus_x - planet.centre_x
        ) * planet.circumference / (2.0 * math.pi)
        return np.linspace(centre - half, centre + half, self._samples)

    def sample_heights(self, camera: Camera) -> NDArray[np.float64]:
        """Return terrain heights across the visible arc, at screen resolution."""
        arc = self.visible_arc(camera)
        resolution = max(
            self._terrain.resolution_floor,
            float(abs(arc[-1] - arc[0])) / max(1, self._samples),
        )
        return self._terrain.height(arc, resolution=resolution)

    def lit_mask(self, camera: Camera) -> NDArray[np.bool_]:
        """Return which sampled points are in daylight.

        All of them when the world does not turn -- which, before the rotation
        layer existed, was the whole surface all the time.
        """
        arc = self.visible_arc(camera)
        if self._spin is None:
            return np.ones(arc.shape, dtype=bool)
        planet = self._planet
        # Kell sits at the origin, so the star lies this way from the planet.
        star_angle = math.atan2(-planet.centre_y, -planet.centre_x)
        distance = Quantity(math.hypot(planet.centre_x, planet.centre_y), LENGTH)
        return np.asarray(
            is_lit(self._spin, arc, self.time, star_angle, distance), dtype=bool
        )

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        arc = self.visible_arc(camera)
        heights = self.sample_heights(camera)
        xs, ys = camera.surface_to_screen(self._planet, arc, heights)
        points = [
            _point((x, y))
            for x, y in zip(np.asarray(xs), np.asarray(ys), strict=True)
        ]
        if len(points) < 2:
            return
        if self._spin is None:
            pygame.draw.aalines(surface, _TEAL, False, points)
            return
        # Split into runs of day and night and draw each in its own colour, so
        # the terminator is visible as the boundary between them. Each run
        # reaches one point into the next so the segments join up.
        lit = self.lit_mask(camera)
        for start, stop, is_day in contiguous_runs(lit):
            segment = points[start : min(stop + 1, len(points))]
            if len(segment) < 2:
                # A run of one sample at the very end of the arc. Nothing to
                # draw through a single point, and a polyline call with one
                # point raises.
                continue
            pygame.draw.aalines(surface, _DAY if is_day else _NIGHT, False, segment)


class Sidebar:
    """A list of what is in the system, and which of it you are watching.

    Vellum crosses the window in seconds at system scale and is three pixels
    across there, so catching it with the pointer is not a realistic way in.
    Selecting it from a list is.

    Drawn in screen space at every zoom, because knowing what you are looking
    at matters most when the view gives no clue.
    """

    bands: Final = frozenset(ScaleBand)

    def __init__(self, targets: Sequence[Target], selected: int | None = None) -> None:
        self._targets = list(targets)
        self._selected = selected

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        panel = pygame.Surface((PANEL_WIDTH, camera.height), pygame.SRCALPHA)
        panel.fill((10, 14, 13, 215))
        surface.blit(panel, (0, 0))
        pygame.draw.line(
            surface, _RULE, (PANEL_WIDTH, 0), (PANEL_WIDTH, camera.height), 1
        )
        if not pygame.font.get_init():
            return

        heading = pygame.font.Font(None, 20)
        surface.blit(heading.render("THE SYSTEM OF KELL", True, _DIM), (16, 22))

        font = pygame.font.Font(None, 22)
        for index, item in enumerate(self._targets):
            top = TOP + index * ROW_HEIGHT
            chosen = index == self._selected
            if chosen:
                pygame.draw.rect(
                    surface, (26, 40, 38), pygame.Rect(0, top, PANEL_WIDTH, ROW_HEIGHT)
                )
                pygame.draw.rect(
                    surface, _TEAL, pygame.Rect(0, top, 3, ROW_HEIGHT)
                )
            colour = _INK if chosen else _DIM
            surface.blit(font.render(item.name, True, colour), (16, top + 7))
            if item.has_ground:
                surface.blit(
                    pygame.font.Font(None, 17).render("ground", True, _DIM),
                    (PANEL_WIDTH - 58, top + 10),
                )
