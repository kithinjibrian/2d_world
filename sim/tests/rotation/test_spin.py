"""Vellum turning on itself: the frame, the day, and the limit."""

import math

import numpy as np
import pytest

from sim.rotation import Spin, breakup_rate
from sim.units import MASS, TIME, Quantity

CIRCUMFERENCE = 3.84e-5
MASS_Q = Quantity(3.0e-6, MASS)


def spin(rate: float = 100.0) -> Spin:
    return Spin(rate=rate, circumference=CIRCUMFERENCE, mass=MASS_Q)


class TestTheRotatingFrame:
    def test_a_surface_coordinate_is_body_fixed(self) -> None:
        """A rock stays where it is. The frame turns; the coordinate does not."""
        s = spin()
        rock = CIRCUMFERENCE * 0.3
        angles = [float(s.inertial_angle(rock, t)) for t in (0.0, 1e-4, 5e-4)]
        assert len({round(a, 12) for a in angles}) == 3  # it moves in space...
        # ...but its surface coordinate recovers exactly, at every time.
        for t in (0.0, 1e-4, 5e-4):
            back = float(s.surface_at_inertial_angle(s.inertial_angle(rock, t), t))
            assert back == pytest.approx(rock, rel=1e-12)

    def test_phase_is_exactly_periodic(self) -> None:
        s = spin()
        assert s.phase(0.0) == pytest.approx(s.phase(s.sidereal_day), abs=1e-9)
        assert s.phase(1e-5) == pytest.approx(s.phase(1e-5 + 7 * s.sidereal_day), abs=1e-9)

    def test_phase_stays_in_range_over_long_runs(self) -> None:
        # Taken modulo, so it cannot drift or lose precision over many turns.
        s = spin()
        for t in (0.0, 1e3, 1e9):
            assert 0.0 <= s.phase(t) < 2.0 * math.pi

    def test_zero_rate_is_legal_and_frozen(self) -> None:
        # What Vellum has today: a world that does not turn.
        s = spin(rate=0.0)
        assert s.inertial_angle(0.0, 0.0) == s.inertial_angle(0.0, 1e9)

    def test_accepts_arrays_of_surface_positions(self) -> None:
        s = spin()
        out = s.inertial_angle(np.linspace(0.0, CIRCUMFERENCE, 5), 1e-4)
        assert np.asarray(out).shape == (5,)


class TestDays:
    def test_sidereal_day_is_two_pi_over_the_rate(self) -> None:
        assert spin(rate=250.0).sidereal_day == pytest.approx(2.0 * math.pi / 250.0)

    def test_solar_day_differs_from_sidereal(self) -> None:
        """The classic error is conflating them. They differ by the orbit."""
        s = spin(rate=100.0)
        orbital = Quantity(1.0, TIME**-1)
        assert s.solar_day(orbital) != pytest.approx(s.sidereal_day)

    def test_the_difference_is_the_orbital_angular_rate(self) -> None:
        s = spin(rate=100.0)
        n = 7.0
        solar = s.solar_day(Quantity(n, TIME**-1))
        assert 2.0 * math.pi / solar == pytest.approx(s.rate - n)

    def test_a_world_turning_at_its_orbital_rate_has_no_solar_day(self) -> None:
        # Tidally frozen: one arc faces the star forever.
        s = spin(rate=5.0)
        assert math.isinf(s.solar_day(Quantity(5.0, TIME**-1)))


class TestBreakup:
    def test_surface_speed_at_breakup_is_the_circular_orbital_speed(self) -> None:
        """Striking, and it falls out of the two-dimensional force law.

        Breakup is sqrt(G2*M)/R, so the surface moves at sqrt(G2*M) -- which is
        the circular orbital speed, and in two dimensions that is the same at
        every radius. A 2D planet flies apart when its surface moves at the
        speed of an orbit anywhere in the system.
        """
        from sim.orbit import circular_speed
        from sim.units import LENGTH, VELOCITY

        omega = breakup_rate(MASS_Q, CIRCUMFERENCE)
        radius = CIRCUMFERENCE / (2.0 * math.pi)
        surface_speed = omega * radius
        v_c = circular_speed(MASS_Q, Quantity(1.0, LENGTH)).scalar(VELOCITY)
        assert surface_speed == pytest.approx(v_c, rel=1e-12)

    def test_a_rate_at_or_above_breakup_raises(self) -> None:
        omega = breakup_rate(MASS_Q, CIRCUMFERENCE)
        with pytest.raises(ValueError, match="breakup"):
            Spin(rate=omega * 1.01, circumference=CIRCUMFERENCE, mass=MASS_Q)
        with pytest.raises(ValueError, match="breakup"):
            Spin(rate=omega, circumference=CIRCUMFERENCE, mass=MASS_Q)

    def test_just_below_breakup_is_allowed(self) -> None:
        omega = breakup_rate(MASS_Q, CIRCUMFERENCE)
        assert Spin(rate=omega * 0.999, circumference=CIRCUMFERENCE, mass=MASS_Q).rate > 0


class TestMomentOfInertia:
    def test_a_uniform_disc_is_half_m_r_squared(self) -> None:
        """The case that does NOT differ from three dimensions.

        Density here is per area, not per volume, and the coefficient comes out
        identical anyway. Present for the same reason kinematic viscosity has a
        test: not everything changes in 2D, and a reader who assumes otherwise
        will "fix" something that was already right.
        """
        s = spin()
        expected = 0.5 * MASS_Q.scalar(MASS) * s.radius**2
        assert s.moment_of_inertia == pytest.approx(expected, rel=1e-12)

    def test_angular_momentum_is_a_signed_scalar(self) -> None:
        # No axis in the plane for it to point along.
        forward = spin(rate=100.0).angular_momentum
        assert isinstance(forward, float)
        assert forward > 0.0


class TestValidation:
    @pytest.mark.parametrize("bad", [-1.0, float("nan"), float("inf")])
    def test_bad_rate_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            Spin(rate=bad, circumference=CIRCUMFERENCE, mass=MASS_Q)

    @pytest.mark.parametrize("bad", [0.0, -1.0])
    def test_bad_circumference_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            Spin(rate=1.0, circumference=bad, mass=MASS_Q)

    def test_radius_follows_from_circumference(self) -> None:
        assert spin().radius == pytest.approx(CIRCUMFERENCE / (2.0 * math.pi))
