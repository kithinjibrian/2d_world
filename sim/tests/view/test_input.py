"""Camera resizing and drag-panning. Pure; no display needed.

The drag logic lives in a pure function for the same reason the camera does:
it is where the decisions are, and a viewer that can only be tested by looking
at it will not be tested.
"""

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from sim.view import Camera, Disc
from sim.view.app import _on_drag

PLANET = Disc(centre_x=1.0, centre_y=0.0, circumference=3.84e-5)


def cam(scale: float, fx: float = 1.0, fy: float = 0.0) -> Camera:
    return Camera(fx, fy, scale, 800, 600, reference_length=PLANET.circumference)


class TestResizing:
    def test_keeps_focus_scale_and_world(self) -> None:
        before = cam(1e6)
        after = before.resized(1024, 768)
        assert (after.focus_x, after.focus_y) == (before.focus_x, before.focus_y)
        assert after.scale == before.scale
        assert after.reference_length == before.reference_length
        assert (after.width, after.height) == (1024, 768)

    def test_a_wider_window_sees_more_world(self) -> None:
        before = cam(1e6)
        assert before.resized(1600, 600).span > before.span

    def test_resizing_can_change_the_band(self) -> None:
        # More viewport at the same zoom means more of the world in view.
        narrow = cam(1e6).resized(100, 600)
        wide = cam(1e6).resized(4000, 600)
        assert wide.span_ratio > narrow.span_ratio

    @pytest.mark.parametrize(("w", "h"), [(0, 600), (800, 0), (-1, 600)])
    def test_bad_size_raises(self, w: int, h: int) -> None:
        with pytest.raises(ValueError):
            cam(1e6).resized(w, h)


class TestFreeDrag:
    """Away from the surface, dragging moves the camera and drops follow."""

    def test_the_world_point_under_the_cursor_follows_the_cursor(self) -> None:
        # The invariant that makes a drag feel right: whatever you grabbed
        # stays under the pointer.
        camera = cam(1e5)
        grabbed_at = (300.0, 220.0)
        grabbed = camera.screen_to_world(*grabbed_at)
        moved, *_ = _on_drag(camera, PLANET, False, 0.0, 0.0, rel_x=57.0, rel_y=-31.0)
        now = moved.screen_to_world(grabbed_at[0] + 57.0, grabbed_at[1] - 31.0)
        assert now == pytest.approx(grabbed, rel=1e-9)

    def test_dragging_right_brings_the_world_right(self) -> None:
        camera = cam(1e5)
        moved, *_ = _on_drag(camera, PLANET, False, 0.0, 0.0, rel_x=40.0, rel_y=0.0)
        assert moved.focus_x < camera.focus_x

    def test_dragging_down_brings_the_world_down(self) -> None:
        camera = cam(1e5)
        moved, *_ = _on_drag(camera, PLANET, False, 0.0, 0.0, rel_x=0.0, rel_y=40.0)
        assert moved.focus_y > camera.focus_y

    def test_dragging_stops_following(self) -> None:
        # Otherwise the follow snaps the camera back every frame and the drag
        # does nothing at all -- the pointer moves and the view does not.
        wide = cam(1.0)  # whole system in view
        _, following, *_ = _on_drag(wide, PLANET, True, 0.0, 0.0, rel_x=10.0, rel_y=0.0)
        assert following is False


class TestDraggingOnTheGround:
    """Zoomed in and following, a drag walks the surface instead.

    Free-panning here would leave the planet within a few pixels of travel and
    show empty space -- the same failure as centring on the planet's centre.
    So while following past the point where the planet fills the view, a
    horizontal drag walks along the ground and a vertical drag changes height.
    """

    CLOSE = 1e11  # span far smaller than the circumference

    def test_horizontal_drag_walks_the_surface_and_keeps_following(self) -> None:
        camera = cam(self.CLOSE)
        assert camera.span < PLANET.circumference
        moved, following, anchor, _ = _on_drag(
            camera, PLANET, True, 0.0, 0.0, rel_x=100.0, rel_y=0.0
        )
        assert following is True
        assert anchor != 0.0
        assert moved.focus_x == camera.focus_x  # the camera itself did not move

    def test_walking_far_enough_wraps(self) -> None:
        camera = cam(self.CLOSE)
        _, _, anchor, _ = _on_drag(
            camera, PLANET, True, 0.0, 0.0,
            rel_x=-PLANET.circumference / camera.metres_per_pixel, rel_y=0.0,
        )
        assert 0.0 <= anchor < PLANET.circumference

    def test_vertical_drag_changes_height_not_position(self) -> None:
        """Dragging down brings the ground down, so the viewpoint rises.

        The same convention as the free pan: whatever is under the pointer
        stays under it. Screen y grows downward, so a positive rel_y is a
        downward drag and lifts the camera.
        """
        camera = cam(self.CLOSE)
        _, _, anchor, height = _on_drag(
            camera, PLANET, True, 0.0, 0.0, rel_x=0.0, rel_y=60.0
        )
        assert anchor == 0.0
        assert height > 0.0

    def test_height_does_not_go_below_the_ground(self) -> None:
        # Dragging up past the surface stops at it rather than burrowing.
        camera = cam(self.CLOSE)
        _, _, _, height = _on_drag(
            camera, PLANET, True, 0.0, 0.0, rel_x=0.0, rel_y=-1e9
        )
        assert height == 0.0

    def test_height_is_consistent_with_the_free_pan_convention(self) -> None:
        # Both regimes must agree on which way is up, or the transition
        # between them reverses the controls under the user's hand.
        wide = cam(1.0)
        panned, *_ = _on_drag(wide, PLANET, False, 0.0, 0.0, rel_x=0.0, rel_y=50.0)
        close = cam(self.CLOSE)
        _, _, _, height = _on_drag(close, PLANET, True, 0.0, 0.0, rel_x=0.0, rel_y=50.0)
        assert panned.focus_y > wide.focus_y  # free pan: viewpoint rises
        assert height > 0.0                   # on the ground: same

    def test_not_following_still_free_pans_when_zoomed_in(self) -> None:
        camera = cam(self.CLOSE)
        moved, following, anchor, _ = _on_drag(
            camera, PLANET, False, 0.0, 0.0, rel_x=30.0, rel_y=0.0
        )
        assert following is False
        assert anchor == 0.0
        assert moved.focus_x != camera.focus_x
