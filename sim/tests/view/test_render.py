"""Smoke tests for the drawing layer. Headless via SDL_VIDEODRIVER=dummy.

These are deliberately shallow: render.py is kept thin enough to be obviously
correct, and everything worth asserting lives in camera.py and scene.py.
"""

import os

import numpy as np
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from sim.orbit import circular_speed, integrate
from sim.star import Kell
from sim.units import LENGTH, LUMINOSITY, MASS, TIME, VELOCITY, Quantity
from sim.view import (
    Camera,
    Disc,
    ScaleBand,
    Scene,
)
from sim.view.render import (
    OrbitTrace,
    PlanetDisc,
    ScaleBar,
    StarDisc,
)


@pytest.fixture(scope="module")
def surface() -> pygame.Surface:
    pygame.init()
    return pygame.Surface((400, 300))


@pytest.fixture(scope="module")
def trajectory():  # type: ignore[no-untyped-def]
    star = Quantity(1.0, MASS)
    v = circular_speed(star, Quantity(1.0, LENGTH)).scalar(VELOCITY)
    return integrate(
        mass=star,
        position=Quantity(np.array([1.0, 0.0]), LENGTH),
        velocity=Quantity(np.array([0.0, v * 1.05]), VELOCITY),
        timestep=Quantity(1e-3, TIME),
        steps=8_000,
    )


PLANET = Disc(centre_x=1.0, centre_y=0.0, circumference=6.3e-3)
KELL = Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))


class TestDrawablesRunWithoutError:
    def test_whole_scene_draws_at_every_band(self, surface, trajectory) -> None:  # type: ignore[no-untyped-def]
        scene = Scene()
        scene.add(StarDisc(KELL))
        scene.add(OrbitTrace(trajectory))
        scene.add(PlanetDisc(PLANET))
        scene.add(ScaleBar())
        for scale in (1e2, 1e5, 1e8, 1e11):
            camera = Camera(
                focus_x=1.0, focus_y=0.0, scale=scale, width=400, height=300,
                reference_length=PLANET.circumference,
            )
            surface.fill((0, 0, 0))
            scene.draw(camera, surface)

    def test_something_is_actually_painted(self, surface, trajectory) -> None:  # type: ignore[no-untyped-def]
        # A viewer whose tests all pass while drawing nothing is the obvious
        # failure mode here, so assert at least one pixel changed.
        surface.fill((0, 0, 0))
        camera = Camera(
            focus_x=0.0, focus_y=0.0, scale=150.0, width=400, height=300,
            reference_length=PLANET.circumference,
        )
        scene = Scene()
        scene.add(StarDisc(KELL))
        scene.add(OrbitTrace(trajectory))
        scene.draw(camera, surface)
        assert pygame.surfarray.array3d(surface).any()


class TestBandDeclarations:
    def test_every_drawable_declares_at_least_one_band(self, trajectory) -> None:  # type: ignore[no-untyped-def]
        for drawable in (StarDisc(KELL), OrbitTrace(trajectory), PlanetDisc(PLANET), ScaleBar()):
            assert drawable.bands
            assert all(isinstance(b, ScaleBand) for b in drawable.bands)
