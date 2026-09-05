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
from typing import Final, cast

import numpy as np
import pygame
from numpy.typing import NDArray

from sim.orbit import Trajectory
from sim.star import Kell
from sim.surface import Terrain
from sim.view.bands import ScaleBand
from sim.view.camera import Camera
from sim.view.geometry import Disc

__all__ = ["OrbitTrace", "PlanetDisc", "ScaleBar", "StarDisc", "TerrainTrace"]

_INK: Final = (232, 236, 228)
_DIM: Final = (96, 108, 100)
_GOLD: Final = (198, 160, 70)
_TEAL: Final = (74, 176, 158)

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
    """Kell, drawn at least a pixel across however far out you are."""

    bands: Final = frozenset(ScaleBand)

    def __init__(self, star: Kell, radius_world: float = 0.02) -> None:
        self._star = star
        self._radius = radius_world

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        centre = _point(camera.world_to_screen(0.0, 0.0))
        radius = max(2, int(self._radius * camera.scale))
        pygame.draw.circle(surface, _GOLD, centre, radius)


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

    The surface curve is drawn as a polyline sampled in surface coordinates and
    composed hierarchically, so it stays exact at ground zoom -- the same path a
    terrain layer will take.
    """

    bands: Final = frozenset(ScaleBand)

    def __init__(self, planet: Disc, samples: int = 512) -> None:
        self._planet = planet
        self._samples = samples

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        planet = self._planet
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

    def __init__(self, terrain: Terrain | None = None) -> None:
        self._terrain = terrain

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        mpp = camera.metres_per_pixel
        # A round number of world units close to 200 px wide.
        raw = 200.0 * mpp
        exponent = np.floor(np.log10(raw))
        span = float(10.0**exponent)
        pixels = int(span / mpp)

        y = camera.height - 28
        pygame.draw.line(surface, _INK, (20, y), (20 + pixels, y), 1)
        pygame.draw.line(surface, _INK, (20, y - 4), (20, y + 4), 1)
        pygame.draw.line(surface, _INK, (20 + pixels, y - 4), (20 + pixels, y + 4), 1)

        if pygame.font.get_init():
            font = pygame.font.Font(None, 18)
            label = f"{span:.0e} world units   |   {camera.band.value}"
            if camera.is_clamped:
                label += "   [zoom limit]"
            if self._terrain is not None and self._terrain.is_clamped_at(mpp):
                label += "   [below terrain detail]"
            surface.blit(font.render(label, True, _INK), (20, y + 8))


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

    def __init__(self, planet: Disc, terrain: Terrain, samples: int = 900) -> None:
        self._planet = planet
        self._terrain = terrain
        self._samples = samples

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

    def draw(self, camera: Camera, target: object) -> None:
        surface = cast(pygame.Surface, target)
        arc = self.visible_arc(camera)
        heights = self.sample_heights(camera)
        xs, ys = camera.surface_to_screen(self._planet, arc, heights)
        points = [
            _point((x, y))
            for x, y in zip(np.asarray(xs), np.asarray(ys), strict=True)
        ]
        if len(points) > 1:
            pygame.draw.aalines(surface, _TEAL, False, points)
