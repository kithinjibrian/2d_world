"""Camera roll, and zoom about the cursor while following.

On a closed surface "up" is radially outward, and that points a different way
at every position -- the exact opposite halfway round the world. Without roll
the ground tilts as you walk and is upside down on the far side.
"""

import math
import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from sim.view import Camera, Disc
from sim.view.app import _camera_for, _on_zoom

PLANET = Disc(centre_x=1.0, centre_y=0.0, circumference=3.84e-5)


def cam(scale: float, rotation: float = 0.0) -> Camera:
    return Camera(
        1.0, 0.0, scale, 800, 600,
        reference_length=PLANET.circumference, rotation=rotation,
    )


class TestRotationTransform:
    @pytest.mark.parametrize("rotation", [0.0, 0.3, math.pi / 2, math.pi, -2.1])
    def test_round_trip(self, rotation: float) -> None:
        c = cam(1e5, rotation)
        for point in [(1.0, 0.0), (1.0 + 1e-4, 3e-5)]:
            sx, sy = c.world_to_screen(*point)
            back = c.screen_to_world(float(sx), float(sy))
            assert back == pytest.approx(point, abs=1e-12)

    def test_a_full_turn_is_the_identity(self) -> None:
        plain = cam(1e5, 0.0)
        turned = cam(1e5, 2.0 * math.pi)
        p = (1.0 + 5e-5, 2e-5)
        assert turned.world_to_screen(*p) == pytest.approx(plain.world_to_screen(*p))

    def test_a_quarter_turn_rolls_the_camera_not_the_world(self) -> None:
        """Rotation is *camera* roll, counter-clockwise.

        Rolling the camera counter-clockwise makes the world appear to turn
        clockwise, so world +x ends up at the bottom of the screen rather than
        the top. Pinned because getting the sign backwards puts the ground
        upside down and looks like a bug in `aligned_to_surface` instead.
        """
        c = cam(1.0, math.pi / 2)
        sx, sy = c.offset_to_screen(1.0, 0.0)
        assert float(sx) == pytest.approx(400.0)
        assert float(sy) > 300.0

    def test_rolling_by_minus_a_quarter_turn_is_the_other_way(self) -> None:
        c = cam(1.0, -math.pi / 2)
        _, sy = c.offset_to_screen(1.0, 0.0)
        assert float(sy) < 300.0

    def test_rotation_does_not_move_the_focus(self) -> None:
        c = cam(1e5, 1.234)
        assert c.world_to_screen(c.focus_x, c.focus_y) == pytest.approx((400.0, 300.0))

    def test_zoom_about_cursor_still_holds_its_point_when_rolled(self) -> None:
        c = cam(1e5, 0.7)
        at = (611.0, 132.0)
        before = c.screen_to_world(*at)
        after = c.zoomed_about(3.0, *at).screen_to_world(*at)
        assert after == pytest.approx(before, rel=1e-9)

    def test_non_finite_rotation_raises(self) -> None:
        with pytest.raises(ValueError):
            cam(1e5, float("nan"))


class TestAligningToTheSurface:
    """The ground must look level wherever you stand on it."""

    @pytest.mark.parametrize("fraction", [0.0, 0.125, 0.25, 0.5, 0.75, 0.9])
    def test_up_is_up_everywhere_on_the_world(self, fraction: float) -> None:
        surface = PLANET.circumference * fraction
        c = (
            cam(1e11)
            .focused_on_surface(PLANET, surface)
            .aligned_to_surface(PLANET, surface)
        )
        ground = c.surface_to_screen(PLANET, surface, 0.0)
        overhead = c.surface_to_screen(PLANET, surface, PLANET.radius * 1e-6)
        # Higher means further up the screen, at every point on the world.
        assert float(overhead[1]) < float(ground[1])
        # And directly above, not off to one side.
        assert float(overhead[0]) == pytest.approx(float(ground[0]), abs=1e-6)

    @pytest.mark.parametrize("fraction", [0.0, 0.3, 0.5, 0.8])
    def test_the_ground_runs_horizontally(self, fraction: float) -> None:
        surface = PLANET.circumference * fraction
        c = (
            cam(1e11)
            .focused_on_surface(PLANET, surface)
            .aligned_to_surface(PLANET, surface)
        )
        step = PLANET.circumference * 1e-9
        here = c.surface_to_screen(PLANET, surface, 0.0)
        along = c.surface_to_screen(PLANET, surface + step, 0.0)
        # Neighbouring ground is beside you, not above or below.
        assert abs(float(along[1]) - float(here[1])) < abs(float(along[0]) - float(here[0]))

    def test_the_far_side_of_the_world_is_not_upside_down(self) -> None:
        """Without roll this is exactly inverted, which is the whole point."""
        near, far = 0.0, PLANET.circumference * 0.5
        for surface in (near, far):
            c = (
                cam(1e11)
                .focused_on_surface(PLANET, surface)
                .aligned_to_surface(PLANET, surface)
            )
            ground = c.surface_to_screen(PLANET, surface, 0.0)
            up = c.surface_to_screen(PLANET, surface, PLANET.radius * 1e-6)
            assert float(up[1]) < float(ground[1])

    def test_camera_for_aligns_when_on_the_ground(self) -> None:
        close = cam(1e11)
        surface = PLANET.circumference * 0.4
        looking = _camera_for(close, PLANET, True, surface, 0.0)
        assert looking.rotation != 0.0

    def test_camera_for_leaves_roll_alone_when_the_planet_fits(self) -> None:
        wide = cam(1.0)
        assert wide.span > PLANET.circumference
        assert _camera_for(wide, PLANET, True, 0.0, 0.0).rotation == 0.0


class TestZoomingWhileFollowing:
    """Zoom about the cursor was silently discarded while following.

    The follow re-centres the camera every frame, so `zoomed_about` moved the
    focus and the override put it straight back -- every scroll zoomed to the
    middle regardless of where the pointer was. On the ground the analogue is
    to move the anchor instead.
    """

    CLOSE = 1e11

    def test_the_surface_point_under_the_cursor_stays_there(self) -> None:
        camera = cam(self.CLOSE)
        anchor, height = PLANET.circumference * 0.2, 0.0
        cursor_x = 700.0
        offset = cursor_x - camera.width * 0.5
        before = anchor + offset * camera.metres_per_pixel

        zoomed, new_anchor, _ = _on_zoom(
            camera, PLANET, True, anchor, height, 2.0, cursor_x, 300.0
        )
        after = new_anchor + offset * zoomed.metres_per_pixel
        assert after == pytest.approx(before, rel=1e-9)

    def test_zooming_at_the_centre_leaves_the_anchor_alone(self) -> None:
        camera = cam(self.CLOSE)
        _, anchor, _ = _on_zoom(
            camera, PLANET, True, 1e-6, 0.0, 2.0, camera.width * 0.5, camera.height * 0.5
        )
        assert anchor == pytest.approx(1e-6)

    def test_zoom_changes_the_scale(self) -> None:
        camera = cam(self.CLOSE)
        zoomed, _, _ = _on_zoom(camera, PLANET, True, 0.0, 0.0, 2.0, 700.0, 300.0)
        assert zoomed.scale > camera.scale

    def test_not_following_falls_back_to_zoom_about_cursor(self) -> None:
        camera = cam(1e5)
        at = (700.0, 220.0)
        before = camera.screen_to_world(*at)
        zoomed, _, _ = _on_zoom(camera, PLANET, False, 0.0, 0.0, 3.0, *at)
        assert zoomed.screen_to_world(*at) == pytest.approx(before, rel=1e-9)
