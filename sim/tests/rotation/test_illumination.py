"""Day and night on a closed surface.

The terminator is two points rather than a curve, so day and night are arcs.
The headline test is the intercepted-power identity, which is exact for a
point source rather than only in the distant limit.
"""

import math

import numpy as np
import pytest

from sim.errors import InvariantError
from sim.periodic import distance
from sim.rotation import (
    Spin,
    incidence_cosine,
    intercepted_power,
    is_lit,
    lit_fraction,
    substellar_surface,
    surface_flux,
    terminator_surfaces,
)
from sim.units import FLUX, LENGTH, LUMINOSITY, MASS, Quantity

CIRCUMFERENCE = 3.84e-5
MASS_Q = Quantity(3.0e-6, MASS)
RADIUS = CIRCUMFERENCE / (2.0 * math.pi)
LUMINOSITY_Q = Quantity(1.0, LUMINOSITY)


def spin(rate: float = 100.0) -> Spin:
    return Spin(rate=rate, circumference=CIRCUMFERENCE, mass=MASS_Q)


class TestTheTerminator:
    def test_there_are_exactly_two_terminator_points(self) -> None:
        """In three dimensions it is a great circle. Here it is two points."""
        points = terminator_surfaces(spin(), time=0.0, star_angle=0.0,
                                     distance=Quantity(RADIUS * 10.0, LENGTH))
        assert len(points) == 2
        assert points[0] != points[1]

    @pytest.mark.parametrize("d_over_r", [1.5, 2.0, 10.0, 1e3])
    def test_lit_fraction_is_arccos_r_over_d_by_pi(self, d_over_r: float) -> None:
        got = lit_fraction(Quantity(RADIUS, LENGTH), Quantity(RADIUS * d_over_r, LENGTH))
        assert got == pytest.approx(math.acos(1.0 / d_over_r) / math.pi, rel=1e-12)

    def test_a_distant_star_lights_exactly_half(self) -> None:
        got = lit_fraction(Quantity(RADIUS, LENGTH), Quantity(RADIUS * 1e9, LENGTH))
        assert got == pytest.approx(0.5, abs=1e-8)

    def test_a_close_star_lights_much_less_than_half(self) -> None:
        # The distant approximation is wrong by 6% at d/R = 10 and by a third
        # at d/R = 2, which is why the exact geometry is used.
        assert lit_fraction(
            Quantity(RADIUS, LENGTH), Quantity(RADIUS * 2.0, LENGTH)
        ) == pytest.approx(1.0 / 3.0, rel=1e-12)

    def test_the_star_must_be_outside_the_planet(self) -> None:
        with pytest.raises(ValueError):
            lit_fraction(Quantity(RADIUS, LENGTH), Quantity(RADIUS * 0.5, LENGTH))


class TestWhereTheSunIs:
    def test_the_substellar_point_faces_the_star(self) -> None:
        s = spin()
        for time in (0.0, 1e-4, 3e-3):
            sub = substellar_surface(s, time=time, star_angle=0.7)
            assert s.inertial_angle(sub, time) % (2.0 * math.pi) == pytest.approx(0.7)

    def test_the_substellar_point_moves_as_the_world_turns(self) -> None:
        s = spin()
        assert substellar_surface(s, 0.0, 0.0) != substellar_surface(s, 1e-4, 0.0)

    def test_it_returns_after_one_sidereal_day(self) -> None:
        """Compared as a circular distance, because positions wrap.

        After one day the phase lands 8.9e-16 short of a full turn, so the
        substellar point comes back as ``circumference - 1e-21``. Subtracting
        says it travelled the whole way round; on a closed curve it did not
        move at all.
        """
        s = spin()
        moved = distance(
            substellar_surface(s, 0.0, 0.0),
            substellar_surface(s, s.sidereal_day, 0.0),
            CIRCUMFERENCE,
        )
        assert float(moved) < CIRCUMFERENCE * 1e-9


class TestDayAndNight:
    DISTANCE = Quantity(RADIUS * 50.0, LENGTH)

    def test_the_substellar_point_is_lit_and_its_antipode_is_not(self) -> None:
        s = spin()
        sub = substellar_surface(s, 0.0, 0.0)
        assert bool(is_lit(s, sub, 0.0, 0.0, self.DISTANCE))
        assert not bool(is_lit(s, sub + CIRCUMFERENCE * 0.5, 0.0, 0.0, self.DISTANCE))

    def test_every_point_sees_both_over_one_rotation(self) -> None:
        """A day. This is the whole point of the layer."""
        s = spin()
        times = np.linspace(0.0, s.sidereal_day, 400)
        for fraction in (0.0, 0.17, 0.5, 0.83):
            place = CIRCUMFERENCE * fraction
            lit = np.array([bool(is_lit(s, place, t, 0.0, self.DISTANCE)) for t in times])
            assert lit.any(), "this point never sees daylight"
            assert (~lit).any(), "this point never sees night"

    def test_a_frozen_world_has_permanent_day_and_permanent_night(self) -> None:
        # What Vellum has today, with no rotation at all.
        s = spin(rate=0.0)
        sub = substellar_surface(s, 0.0, 0.0)
        far = sub + CIRCUMFERENCE * 0.5
        for t in (0.0, 1e3, 1e9):
            assert bool(is_lit(s, sub, t, 0.0, self.DISTANCE))
            assert not bool(is_lit(s, far, t, 0.0, self.DISTANCE))

    def test_the_lit_arc_is_the_predicted_fraction_of_the_world(self) -> None:
        s = spin()
        places = np.linspace(0.0, CIRCUMFERENCE, 200_001)[:-1]
        lit = np.asarray(is_lit(s, places, 0.0, 0.0, self.DISTANCE))
        expected = lit_fraction(Quantity(RADIUS, LENGTH), self.DISTANCE)
        assert float(lit.mean()) == pytest.approx(expected, abs=1e-4)


class TestFlux:
    DISTANCE = Quantity(RADIUS * 50.0, LENGTH)

    def test_night_is_exactly_zero(self) -> None:
        """Not small. A leaky terminator makes darkness a tolerance question."""
        s = spin()
        dark = substellar_surface(s, 0.0, 0.0) + CIRCUMFERENCE * 0.5
        flux = surface_flux(s, dark, 0.0, 0.0, LUMINOSITY_Q, self.DISTANCE)
        assert flux.scalar(FLUX) == 0.0

    def test_the_substellar_point_is_the_brightest(self) -> None:
        s = spin()
        sub = substellar_surface(s, 0.0, 0.0)
        here = surface_flux(s, sub, 0.0, 0.0, LUMINOSITY_Q, self.DISTANCE).scalar(FLUX)
        aside = surface_flux(
            s, sub + CIRCUMFERENCE * 0.1, 0.0, 0.0, LUMINOSITY_Q, self.DISTANCE
        ).scalar(FLUX)
        assert here > aside > 0.0

    def test_incidence_falls_to_zero_at_the_terminator(self) -> None:
        s = spin()
        a, _ = terminator_surfaces(s, 0.0, 0.0, self.DISTANCE)
        grazing = float(incidence_cosine(s, a, 0.0, 0.0, self.DISTANCE))
        assert grazing == pytest.approx(0.0, abs=1e-9)

    def test_flux_carries_the_flux_dimension(self) -> None:
        s = spin()
        flux = surface_flux(s, 0.0, 0.0, 0.0, LUMINOSITY_Q, self.DISTANCE)
        assert flux.dimension == FLUX

    def test_non_finite_inputs_raise(self) -> None:
        s = spin()
        with pytest.raises((ValueError, InvariantError)):
            surface_flux(s, 0.0, 0.0, 0.0, LUMINOSITY_Q, Quantity(float("nan"), LENGTH))


class TestInterceptedPower:
    """The headline invariant, and it is exact rather than asymptotic.

    A convex body subtends 2*arcsin(R/d) at a point source, so it intercepts
    L*arcsin(R/d)/pi exactly. Integrating F(r)*cos(incidence) around the lit arc
    must give the same number, which pins the incidence geometry, the 1/r flux
    dilution and the terminator all at once.
    """

    @pytest.mark.parametrize("d_over_r", [1.5, 2.0, 5.0, 10.0, 100.0])
    def test_matches_the_shadow_the_planet_casts(self, d_over_r: float) -> None:
        distance = Quantity(RADIUS * d_over_r, LENGTH)
        got = intercepted_power(spin(), LUMINOSITY_Q, distance)
        exact = 1.0 * math.asin(1.0 / d_over_r) / math.pi
        assert got == pytest.approx(exact, rel=1e-6)

    def test_it_is_not_merely_the_distant_approximation(self) -> None:
        # F_centre * 2R is 4.7% low at d/R = 2. If the implementation used it,
        # the test above would fail there and pass far away.
        d_over_r = 2.0
        distance = Quantity(RADIUS * d_over_r, LENGTH)
        approximation = (1.0 / (2.0 * math.pi * RADIUS * d_over_r)) * 2.0 * RADIUS
        exact = math.asin(1.0 / d_over_r) / math.pi
        assert approximation != pytest.approx(exact, rel=1e-3)
        assert intercepted_power(spin(), LUMINOSITY_Q, distance) == pytest.approx(exact, rel=1e-6)

    def test_it_does_not_depend_on_the_rotation_rate(self) -> None:
        distance = Quantity(RADIUS * 20.0, LENGTH)
        rates = [0.0, 50.0, 100.0]
        powers = [intercepted_power(spin(r), LUMINOSITY_Q, distance) for r in rates]
        assert all(p == pytest.approx(powers[0], rel=1e-9) for p in powers)
