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

from typing import Final, cast

import numpy as np
import pygame

from sim.orbit import Trajectory
from sim.star import Kell
from sim.view.bands import ScaleBand
from sim.view.camera import Camera
from sim.view.geometry import Disc

__all__ = ["OrbitTrace", "PlanetDisc", "ScaleBar", "StarDisc"]

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
    """A bar and a readout. Without it eleven decades of zoom disorient fast."""

    bands: Final = frozenset(ScaleBand)

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
            surface.blit(font.render(label, True, _INK), (20, y + 8))
