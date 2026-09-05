"""Precision tests: what actually breaks across eleven orders of magnitude.

Rewritten twice during Session 11 after measuring rather than assuming. See
TestWhyTransformsAreAnchored for what the measurements showed.
"""

import math

import pytest

from sim.view import Camera, Disc


def cam(scale: float, fx: float = 0.0, fy: float = 0.0) -> Camera:
    return Camera(focus_x=fx, focus_y=fy, scale=scale, width=800, height=600)



class TestWhyTransformsAreAnchored:
    """Measured in Session 11; the PRP's stated reason was wrong.

    Camera-relative transforms do **not** buy float64 precision at these
    ranges. With a focus 1e11 m away and two points 1 m apart, the relative and
    absolute forms both give exactly 100.00 px. The eleven orders of magnitude
    the feature spans sit comfortably inside float64's ~16 digits.

    Two things are true instead, and these tests pin them:

    1. What absolute transforms actually break is **pixel coordinate
       magnitude**: 1e11 m at 100 px/m is 1e13 pixels, and SDL takes C ints
       whose range stops at 2.1e9. The renderer overflows long before the float
       does.
    2. The precision ceiling is in **storing** an absolute world coordinate at
       all, not in transforming it. At 1e11 m, one float64 ulp is about 15
       microns, so a ground feature finer than that cannot be represented as an
       absolute position no matter how it is transformed. That is why surface
       positions are held in surface coordinates and composed hierarchically —
       see TestHierarchicalPrecision.
    """

    def test_screen_coordinates_stay_bounded_at_extreme_focus(self) -> None:
        c = cam(100.0, 1e11, 0.0)
        sx, sy = c.world_to_screen(1e11 + 1.0, 0.0)
        assert abs(float(sx)) < 1e4
        assert abs(float(sy)) < 1e4

    def test_an_absolute_transform_would_overflow_the_renderer(self) -> None:
        # Documents the failure the anchored form avoids. Not a mutation:
        # the absolute product is computed here to show its magnitude.
        absolute_pixels = 1e11 * 100.0
        assert absolute_pixels > 2**31 - 1

    def test_one_metre_still_resolves_at_solar_system_focus(self) -> None:
        c = cam(100.0, 1e11, 0.0)
        a = c.world_to_screen(1e11, 0.0)[0]
        b = c.world_to_screen(1e11 + 1.0, 0.0)[0]
        assert float(b) - float(a) == pytest.approx(100.0)

    def test_absolute_world_coordinates_quantise_at_about_15_microns(self) -> None:
        # The real precision floor, and the reason for hierarchical composition.
        assert math.ulp(1e11) == pytest.approx(1.5e-5, rel=0.5)


class TestHierarchicalPrecision:
    """Surface positions are composed anchor + offset, never summed absolutely.

    A body on the ground is (surface coordinate, height). Converting that to an
    absolute world position would quantise it to the planet's distance from
    Kell — 15 microns at 1e11 m. Composing it as an offset from the planet
    centre keeps the arithmetic in numbers of order the planet radius, where a
    float64 ulp is nanometres.
    """

    # Vellum-scale: a closed surface 3.84e7 m around, 1e11 m from Kell.
    PLANET = Disc(centre_x=1e11, centre_y=0.0, circumference=3.84e7)

    def test_a_micron_on_the_ground_survives(self) -> None:
        """Viewed at the top of the disc, so the displacement lies along x.

        The planet's centre is 1e11 from the origin **in x**, so this is the
        orientation where an absolute composition would fold the micron into
        that huge coordinate and lose it. Measured at the side of the disc
        instead, the displacement is in y where the anchor is zero, and the
        test passes whether or not the transform is anchored -- which it did,
        until a mutation run showed the test was not exercising the property
        it claimed to.

        A millimetre would survive either way: one ulp at 1e11 m is ~15
        microns, so a millimetre is 66 ulps. A micron is not.
        """
        planet = self.PLANET
        quarter = planet.circumference * 0.25  # theta = pi/2, the top
        c = Camera(
            focus_x=planet.centre_x,
            focus_y=planet.centre_y + planet.radius,
            scale=1e8,
            width=800,
            height=600,
        )
        a = c.surface_to_screen(planet, surface=quarter, height=0.0)
        b = c.surface_to_screen(planet, surface=quarter + 1e-6, height=0.0)
        # 1 micron of surface at 1e8 px/m is 100 px, and at the top of the disc
        # it lies almost entirely along x.
        assert abs(float(b[0]) - float(a[0])) == pytest.approx(100.0, rel=1e-3)

    def test_composing_absolutely_would_lose_a_micron(self) -> None:
        # The contrast, computed explicitly: forming the absolute coordinate
        # destroys the micron before any transform runs.
        absolute = self.PLANET.centre_x + self.PLANET.radius
        assert absolute == absolute + 1e-6  # already gone

    def test_wrapping_does_not_quantise_small_positions(self) -> None:
        """Regression: the first `mod` helper lost 0.16% of a micron.

        It wrapped with ``fmod(fmod(a, b) + b, b)`` to make negatives positive.
        Adding the circumference quantises at that value's ulp -- 7.45 nm for a
        3.84e7 m surface -- which is invisible in a unit test of `mod` itself
        and plainly visible as a wrong pixel offset at ground zoom.
        """
        from sim.view.geometry import mod

        assert mod(1e-6, 3.84e7) == 1e-6
        assert mod(-1.0, 3.84e7) == pytest.approx(3.84e7 - 1.0)
        assert 0.0 <= float(mod(-1e-9, 3.84e7)) < 3.84e7

    def test_and_the_hierarchical_offset_keeps_nanometres(self) -> None:
        # The offset arithmetic happens at the planet's radius, ~6.1e6 m, where
        # one ulp is about a nanometre rather than fifteen microns.
        assert math.ulp(self.PLANET.radius) < 1e-8

    def test_surface_position_wraps(self) -> None:
        c = Camera(focus_x=1e11, focus_y=0.0, scale=1e-4, width=800, height=600)
        here = c.surface_to_screen(self.PLANET, surface=1234.0, height=0.0)
        around = c.surface_to_screen(
            self.PLANET, surface=1234.0 + self.PLANET.circumference, height=0.0
        )
        assert here == pytest.approx(around, abs=1e-6)

    def test_height_lifts_away_from_the_centre(self) -> None:
        c = Camera(focus_x=1e11, focus_y=0.0, scale=1e-4, width=800, height=600)
        ground = c.surface_to_screen(self.PLANET, surface=0.0, height=0.0)
        up = c.surface_to_screen(self.PLANET, surface=0.0, height=1e5)
        assert float(up[0]) > float(ground[0])


class TestFocusingOnTheSurface:
    """Centring on the planet's centre is only right while the planet fits.

    Past that it puts the camera inside the world, with the ground thousands
    of pixels off-screen -- which looked like "zoom in and the world vanishes".
    """

    PLANET = Disc(centre_x=1.0, centre_y=0.0, circumference=3.84e-5)

    def test_the_focused_point_lands_at_the_viewport_centre(self) -> None:
        c = Camera(0.0, 0.0, 1e9, 800, 600, reference_length=self.PLANET.circumference)
        for surface in (0.0, 1e-6, self.PLANET.circumference * 0.37):
            focused = c.focused_on_surface(self.PLANET, surface)
            sx, sy = focused.surface_to_screen(self.PLANET, surface, 0.0)
            assert float(sx) == pytest.approx(400.0, abs=1e-3)
            assert float(sy) == pytest.approx(300.0, abs=1e-3)

    def test_focusing_wraps_with_the_surface(self) -> None:
        c = Camera(0.0, 0.0, 1e9, 800, 600, reference_length=self.PLANET.circumference)
        here = c.focused_on_surface(self.PLANET, 1e-6)
        around = c.focused_on_surface(self.PLANET, 1e-6 + self.PLANET.circumference)
        assert here.focus_x == pytest.approx(around.focus_x)
        assert here.focus_y == pytest.approx(around.focus_y)

    def test_height_lifts_the_focus_off_the_ground(self) -> None:
        c = Camera(0.0, 0.0, 1e9, 800, 600, reference_length=self.PLANET.circumference)
        ground = c.focused_on_surface(self.PLANET, 0.0, 0.0)
        aloft = c.focused_on_surface(self.PLANET, 0.0, 1e-6)
        assert aloft.focus_x > ground.focus_x
