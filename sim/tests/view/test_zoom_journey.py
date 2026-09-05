"""The test that should have existed before the viewer shipped.

The viewer PRP's validation step said to run the app and zoom by hand from the
whole orbit to a stretch of ground. That was not done -- headless smoke tests
were run instead, which drew each layer once at a few scales and asserted only
that pixels changed. Three defects survived that and were found in seconds by
someone actually looking at the screen:

1. The zoom limits were absolute constants, so the GROUND band was unreachable.
2. The star was drawn with an unculled radius, filling the viewport with gold
   at close zoom.
3. Following Vellum centred on the planet's centre, so zooming in put the
   camera inside the planet with the surface thousands of pixels off-screen.

This walks the whole zoom range the feature exists to provide and asserts the
view stays sane at every step. It is slower than a smoke test and it is the
only kind that could have caught any of these.
"""

import os

import numpy as np
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from sim.view import Camera, ScaleBand
from sim.view.app import _camera_for, _demo_world, _rebuild

WIDTH, HEIGHT = 640, 400
BACKGROUND = (14, 18, 16)


@pytest.fixture(scope="module")
def world():  # type: ignore[no-untyped-def]
    pygame.init()
    pygame.font.init()
    return _demo_world()


def journey(circumference: float) -> list[Camera]:
    """Cameras stepping from the whole system down to the deepest zoom."""
    widest = Camera(
        0.0, 0.0, WIDTH / 6.0, WIDTH, HEIGHT, reference_length=circumference
    )
    cameras = [widest]
    camera = widest
    for _ in range(200):
        zoomed = camera.zoomed(2.0)
        if zoomed.scale == camera.scale:
            break
        camera = zoomed
        cameras.append(camera)
    return cameras


class TestTheWholeRangeIsReachable:
    def test_every_band_is_visited(self, world) -> None:  # type: ignore[no-untyped-def]
        _, _, planet, _ = world
        bands = {c.band for c in journey(planet.circumference)}
        assert bands == set(ScaleBand), f"never reached {set(ScaleBand) - bands}"

    def test_ground_is_reachable(self, world) -> None:  # type: ignore[no-untyped-def]
        # The defect: zoom limits were absolute px-per-world-unit constants,
        # so on a world whose orbit is 1.0 the deepest zoom was still REGIONAL.
        _, _, planet, _ = world
        assert any(c.band is ScaleBand.GROUND for c in journey(planet.circumference))

    def test_zoom_can_go_below_the_terrain_floor(self, world) -> None:  # type: ignore[no-untyped-def]
        # Otherwise "below terrain detail" could never be reported, and the
        # honesty about the resolution floor would be untestable.
        _, _, planet, terrain = world
        assert any(
            terrain.is_clamped_at(c.metres_per_pixel)
            for c in journey(planet.circumference)
        )

    def test_terrain_has_detail_throughout_the_ground_band(self, world) -> None:  # type: ignore[no-untyped-def]
        _, _, planet, terrain = world
        entering_ground = next(
            c for c in journey(planet.circumference) if c.band is ScaleBand.GROUND
        )
        assert not terrain.is_clamped_at(entering_ground.metres_per_pixel), (
            "the GROUND band begins already below the terrain's resolution floor, "
            "so there is nothing to see there"
        )


class TestNothingSwallowsTheView:
    def test_no_frame_is_a_flat_wash_of_one_colour(self, world) -> None:  # type: ignore[no-untyped-def]
        """The gold-screen defect.

        An unculled circle of radius 2e7 px covers everything. Asserting that
        some background survives catches any drawable that paints the viewport
        edge to edge.
        """
        star, trajectory, planet, terrain = world
        surface = pygame.Surface((WIDTH, HEIGHT))
        for camera in journey(planet.circumference):
            focused = _camera_for(camera, planet, following=True, anchor=0.0)
            surface.fill(BACKGROUND)
            _rebuild(star, trajectory, planet, terrain).draw(focused, surface)
            pixels = pygame.surfarray.array3d(surface)
            is_background = np.all(pixels == np.array(BACKGROUND), axis=2)
            assert is_background.any(), (
                f"the whole viewport was painted over at {camera.band.value} "
                f"(scale {camera.scale:.3e})"
            )


class TestFollowingLandsOnTheGround:
    def test_the_surface_is_on_screen_once_the_planet_fills_the_view(self, world) -> None:  # type: ignore[no-untyped-def]
        """The inside-the-planet defect.

        Following centred on the planet's centre. Once the planet is larger
        than the viewport that puts the ground thousands of pixels away, so
        zooming in showed empty space where the world should be.
        """
        _, _, planet, _ = world
        for camera in journey(planet.circumference):
            if camera.span > planet.circumference:
                continue  # planet still fits; centring on it is right
            focused = _camera_for(camera, planet, following=True, anchor=0.0)
            sx, sy = focused.surface_to_screen(planet, 0.0, 0.0)
            assert 0 <= float(sx) <= WIDTH, f"ground off-screen at {camera.band.value}"
            assert 0 <= float(sy) <= HEIGHT, f"ground off-screen at {camera.band.value}"
