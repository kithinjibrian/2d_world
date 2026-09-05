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

from sim.view import Camera, Disc, ScaleBand
from sim.view.app import _camera_for, _demo_world, _rebuild
from sim.view.render import VELLUM

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
        _, _, planet, _, _ = world
        bands = {c.band for c in journey(planet.circumference)}
        assert bands == set(ScaleBand), f"never reached {set(ScaleBand) - bands}"

    def test_ground_is_reachable(self, world) -> None:  # type: ignore[no-untyped-def]
        # The defect: zoom limits were absolute px-per-world-unit constants,
        # so on a world whose orbit is 1.0 the deepest zoom was still REGIONAL.
        _, _, planet, _, _ = world
        assert any(c.band is ScaleBand.GROUND for c in journey(planet.circumference))

    def test_zoom_can_go_below_the_terrain_floor(self, world) -> None:  # type: ignore[no-untyped-def]
        # Otherwise "below terrain detail" could never be reported, and the
        # honesty about the resolution floor would be untestable.
        _, _, planet, terrain, _ = world
        assert any(
            terrain.is_clamped_at(c.metres_per_pixel)
            for c in journey(planet.circumference)
        )

    def test_terrain_has_detail_throughout_the_ground_band(self, world) -> None:  # type: ignore[no-untyped-def]
        _, _, planet, terrain, _ = world
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
        star, trajectory, planet, terrain, spin = world
        surface = pygame.Surface((WIDTH, HEIGHT))
        for camera in journey(planet.circumference):
            focused = _camera_for(camera, planet, following=True, anchor=0.0)
            surface.fill(BACKGROUND)
            _rebuild(star, trajectory, planet, terrain, spin).draw(focused, surface)
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
        _, _, planet, _, _ = world
        for camera in journey(planet.circumference):
            if camera.span > planet.circumference:
                continue  # planet still fits; centring on it is right
            focused = _camera_for(camera, planet, following=True, anchor=0.0)
            sx, sy = focused.surface_to_screen(planet, 0.0, 0.0)
            assert 0 <= float(sx) <= WIDTH, f"ground off-screen at {camera.band.value}"
            assert 0 <= float(sy) <= HEIGHT, f"ground off-screen at {camera.band.value}"


class TestTheSystemViewHoldsStill:
    """Following a moving planet at system zoom drags the whole view.

    `_camera_for` followed the planet whenever the viewport was wider than the
    circumference — which at system zoom is always. With the clock running, the
    camera tracked the orbiting planet and the star slid right across the
    window. What you want at system scale is to watch the planet move against a
    fixed background, which is the opposite.
    """

    def test_the_camera_does_not_move_at_system_zoom(self, world) -> None:  # type: ignore[no-untyped-def]
        _, trajectory, planet, _, _ = world
        camera = Camera(0.0, 0.0, WIDTH / 6.0, WIDTH, HEIGHT,
                        reference_length=planet.circumference)
        assert camera.band is ScaleBand.SYSTEM

        focuses = set()
        for step in (0, 400, 800, 1200):
            position = trajectory.positions[step % len(trajectory.positions)]
            moved = Disc(float(position[0]), float(position[1]), planet.circumference)
            looking = _camera_for(camera, moved, following=True, anchor=0.0)
            focuses.add((looking.focus_x, looking.focus_y))
        assert len(focuses) == 1, "the view moved while the planet orbited"

    def test_it_still_follows_once_the_planet_is_worth_following(self, world) -> None:  # type: ignore[no-untyped-def]
        _, _, planet, _, _ = world
        close = Camera(0.0, 0.0, WIDTH / (planet.circumference * 10.0), WIDTH, HEIGHT,
                       reference_length=planet.circumference)
        assert close.band is not ScaleBand.SYSTEM
        looking = _camera_for(close, planet, following=True, anchor=0.0)
        assert (looking.focus_x, looking.focus_y) != (close.focus_x, close.focus_y)


class TestThePlanetIsVisibleAtEveryZoom:
    """A world you cannot see is not much of a viewer.

    At the opening view the planet's radius is 0.0013 px. StarDisc has a
    minimum size; PlanetDisc did not, so Vellum simply was not drawn.
    """

    @staticmethod
    def _marked(surface: pygame.Surface, x: int, y: int) -> bool:
        """Is Vellum's own marker colour present near (x, y)?

        Checked by colour, not by "something is not background". The orbit
        trace passes exactly through the planet's position, so a background
        test passes whether or not the planet is drawn at all -- which it did,
        on the first version of this test.
        """
        patch = pygame.surfarray.array3d(surface)[
            max(0, x - 6) : x + 7, max(0, y - 6) : y + 7
        ]
        return bool(np.all(patch == np.array(VELLUM), axis=2).any())

    def test_the_planet_is_marked_at_system_zoom(self, world) -> None:  # type: ignore[no-untyped-def]
        star, trajectory, planet, terrain, spin = world
        camera = Camera(0.0, 0.0, WIDTH / 6.0, WIDTH, HEIGHT,
                        reference_length=planet.circumference)
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(BACKGROUND)
        _rebuild(star, trajectory, planet, terrain, spin).draw(camera, surface)
        sx, sy = camera.world_to_screen(planet.centre_x, planet.centre_y)
        assert self._marked(surface, int(float(sx)), int(float(sy))), (
            "Vellum is not drawn at system zoom -- its radius there is 0.0013 px"
        )

    @pytest.mark.parametrize("scale_factor", [1.0, 1e2, 1e4])
    def test_the_marker_survives_zooming_further_out(self, world, scale_factor: float) -> None:  # type: ignore[no-untyped-def]
        star, trajectory, planet, terrain, spin = world
        camera = Camera(0.0, 0.0, (WIDTH / 6.0) / scale_factor, WIDTH, HEIGHT,
                        reference_length=planet.circumference)
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(BACKGROUND)
        _rebuild(star, trajectory, planet, terrain, spin).draw(camera, surface)
        sx, sy = camera.world_to_screen(planet.centre_x, planet.centre_y)
        x, y = int(float(sx)), int(float(sy))
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            assert self._marked(surface, x, y)
