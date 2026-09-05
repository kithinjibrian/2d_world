"""Selecting something in the system and being taken to it."""

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from sim.view import Camera, Disc, ScaleBand
from sim.view.sidebar import PANEL_WIDTH, ROW_HEIGHT, TOP, Target, frame, row_at

PLANET = Disc(centre_x=1.0, centre_y=0.0, circumference=3.84e-5)
KELL = Target("Kell", 0.0, 0.0, radius=0.02)
VELLUM = Target("Vellum", 1.0, 0.0, radius=PLANET.radius, surface=PLANET)


def cam(scale: float = 1280.0 / 6.0) -> Camera:
    return Camera(0.0, 0.0, scale, 1280, 800, reference_length=PLANET.circumference)


class TestHitTesting:
    def test_rows_map_to_indices(self) -> None:
        for index in range(3):
            y = TOP + index * ROW_HEIGHT + ROW_HEIGHT * 0.5
            assert row_at(20.0, y, 3) == index

    def test_clicks_on_the_world_are_not_selections(self) -> None:
        # Otherwise every drag in the world would also change the selection.
        assert row_at(PANEL_WIDTH + 1.0, TOP + 5.0, 3) is None
        assert row_at(600.0, 400.0, 3) is None

    def test_above_the_first_row_is_not_a_selection(self) -> None:
        assert row_at(20.0, TOP - 10.0, 3) is None

    def test_below_the_last_row_is_not_a_selection(self) -> None:
        assert row_at(20.0, TOP + 3 * ROW_HEIGHT + 5.0, 3) is None

    def test_an_empty_list_selects_nothing(self) -> None:
        assert row_at(20.0, TOP + 5.0, 0) is None


class TestFraming:
    def test_the_target_ends_up_at_the_centre(self) -> None:
        framed = frame(cam(), VELLUM)
        sx, sy = framed.world_to_screen(VELLUM.x, VELLUM.y)
        assert float(sx) == pytest.approx(640.0)
        assert float(sy) == pytest.approx(400.0)

    def test_framing_vellum_crosses_five_orders_of_magnitude(self) -> None:
        """The jump the pointer cannot make by hand.

        At system scale Vellum is three pixels across and moving; framing has
        to do in one step what dragging and scrolling cannot do at all.
        """
        start = cam()
        framed = frame(start, VELLUM)
        assert framed.scale / start.scale > 1e5

    def test_the_framed_body_fills_a_useful_part_of_the_view(self) -> None:
        framed = frame(cam(), VELLUM)
        on_screen = 2.0 * VELLUM.radius * framed.scale
        assert 0.15 < on_screen / framed.width < 0.6

    def test_framing_vellum_leaves_the_system_band(self) -> None:
        # Which is what re-engages following: the camera deliberately does not
        # chase an orbiting body while the whole system is in view.
        assert cam().band is ScaleBand.SYSTEM
        assert frame(cam(), VELLUM).band is not ScaleBand.SYSTEM

    def test_framing_kell_keeps_the_system_in_view(self) -> None:
        # The star is enormous next to the planet, so framing it stays wide.
        framed = frame(cam(), KELL)
        assert framed.span > PLANET.circumference

    def test_framing_respects_the_zoom_limits(self) -> None:
        tiny = Target("speck", 0.0, 0.0, radius=1e-30)
        framed = frame(cam(), tiny)
        assert framed.scale <= cam().max_scale


class TestTargets:
    def test_vellum_has_ground_and_kell_does_not(self) -> None:
        assert VELLUM.has_ground
        assert not KELL.has_ground

    def test_kells_radius_is_a_display_value(self) -> None:
        """Kell is stubbed; its real radius raises by design.

        The number here exists so the star can be drawn and framed, and must
        never be read as a physical result. See DECISION-010.
        """
        from sim.star import Kell
        from sim.units import LUMINOSITY, MASS, Quantity

        star = Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))
        with pytest.raises(NotImplementedError):
            _ = star.radius


class TestSelectingVellumGetsYouToTheGround:
    """The whole point: the journey the pointer cannot make.

    Vellum crosses the window in seconds at system scale and is three pixels
    across there. Clicking its row must land you on the planet, following, with
    the ground reachable by scrolling from there.
    """

    def test_the_row_click_lands_on_the_planet_and_follows(self) -> None:
        from sim.view.app import _camera_for, _demo_world, targets_for

        star, _, planet, *_ = _demo_world()
        targets = targets_for(star, planet)
        assert [t.name for t in targets] == ["Kell", "Vellum"]

        picked = row_at(20.0, TOP + ROW_HEIGHT + 5.0, len(targets))
        assert picked == 1

        start = cam()
        framed = frame(start, targets[picked])
        looking = _camera_for(framed, planet, following=True, anchor=0.0)
        assert looking.focus_x == pytest.approx(planet.centre_x)
        assert looking.focus_y == pytest.approx(planet.centre_y)

    def test_and_the_ground_is_reachable_by_scrolling_from_there(self) -> None:
        from sim.view.app import _camera_for, _demo_world, targets_for

        star, _, planet, *_ = _demo_world()
        camera = frame(cam(), targets_for(star, planet)[1])
        for _ in range(9):
            camera = camera.zoomed(4.0)
        assert camera.band is ScaleBand.GROUND

        looking = _camera_for(camera, planet, following=True, anchor=0.0)
        sx, sy = looking.surface_to_screen(planet, 0.0, 0.0)
        assert 0 <= float(sx) <= looking.width
        assert 0 <= float(sy) <= looking.height

    def test_selecting_kell_does_not_pretend_the_star_has_ground(self) -> None:
        from sim.view.app import _demo_world, targets_for

        star, _, planet, *_ = _demo_world()
        assert not targets_for(star, planet)[0].has_ground
