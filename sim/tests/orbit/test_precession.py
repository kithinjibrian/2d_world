"""The headline measurement: apsidal precession under F ~ 1/r.

No orbit closes under an inverse-first-power force (Bertrand), so the apsis
line moves every orbit. The near-circular apsidal angle is pi/sqrt(2), giving
a regression of about 105.44 degrees per orbit and a season that works round
the calendar in 2 + sqrt(2) orbits.

The timestep-convergence test is not optional decoration: a non-symplectic
integrator manufactures precession, and without convergence evidence a
plausible-looking number cannot be distinguished from a numerical artefact.
"""

import math

import numpy as np
import pytest

from sim.orbit import (
    APSIDAL_ANGLE_NEAR_CIRCULAR,
    apsidal_angle,
    circular_speed,
    integrate,
    pericentre_to_pericentre_angle,
)
from sim.units import LENGTH, MASS, TIME, VELOCITY, Quantity

STAR = Quantity(1.0, MASS)
V_C = circular_speed(STAR, Quantity(1.0, LENGTH)).scalar(VELOCITY)


def measure(speed_factor: float, dt: float, steps: int) -> float:
    """Return the measured pericentre-to-pericentre sweep, in radians."""
    traj = integrate(
        mass=STAR,
        position=Quantity(np.array([1.0, 0.0]), LENGTH),
        velocity=Quantity(np.array([0.0, V_C * speed_factor]), VELOCITY),
        timestep=Quantity(dt, TIME),
        steps=steps,
    )
    return pericentre_to_pericentre_angle(traj)


class TestNearCircularLimit:
    def test_apsidal_angle_approaches_pi_over_root_two(self) -> None:
        # At v/v_c = 1.01 the physical departure from the near-circular limit
        # is of order (dv)^2, roughly 0.002 degrees -- well inside tolerance.
        sweep = measure(1.01, dt=1e-4, steps=200_000)
        assert math.degrees(sweep / 2.0) == pytest.approx(
            math.degrees(APSIDAL_ANGLE_NEAR_CIRCULAR), abs=0.02
        )

    def test_pericentre_sweep_is_twice_the_apsidal_angle(self) -> None:
        # The distinction the drafting script got wrong. Pericentre to
        # pericentre is 254.56 degrees; the apsidal angle is half of it.
        sweep = measure(1.01, dt=1e-4, steps=200_000)
        assert math.degrees(sweep) == pytest.approx(254.5584, abs=0.05)
        assert apsidal_angle_of(sweep) == pytest.approx(127.2792, abs=0.03)

    def test_the_apsis_regresses_by_about_105_degrees_per_orbit(self) -> None:
        sweep = measure(1.01, dt=1e-4, steps=200_000)
        regression = 360.0 - math.degrees(sweep)
        assert regression == pytest.approx(105.4416, abs=0.05)

    def test_no_orbit_closes(self) -> None:
        # A closed orbit would sweep exactly 360 degrees between pericentres.
        sweep = math.degrees(measure(1.01, dt=1e-4, steps=200_000))
        assert abs(sweep - 360.0) > 100.0


class TestEccentricityDrift:
    """The closed form describes the near-circular limit only."""

    def test_sweep_departs_monotonically_from_the_limit(self) -> None:
        limit = math.degrees(2.0 * APSIDAL_ANGLE_NEAR_CIRCULAR)
        deviations = [
            abs(math.degrees(measure(f, dt=1e-4, steps=200_000)) - limit)
            for f in (1.02, 1.05, 1.10)
        ]
        assert deviations == sorted(deviations)
        assert deviations[0] < 0.05
        assert deviations[-1] > 0.1


class TestTimestepConvergence:
    """Without this, the precession number is unverified however good it looks."""

    def test_measurement_is_timestep_independent(self) -> None:
        sweeps = [
            measure(1.01, dt=dt, steps=int(20.0 / dt))
            for dt in (4e-4, 2e-4, 1e-4)
        ]
        spread = max(sweeps) - min(sweeps)
        assert math.degrees(spread) < 0.02

    def test_error_shrinks_as_the_timestep_shrinks(self) -> None:
        target = 2.0 * APSIDAL_ANGLE_NEAR_CIRCULAR
        coarse = abs(measure(1.01, dt=8e-4, steps=25_000) - target)
        fine = abs(measure(1.01, dt=1e-4, steps=200_000) - target)
        assert fine <= coarse


class TestSeasonCycle:
    def test_a_season_works_round_the_calendar_in_two_plus_root_two_orbits(self) -> None:
        sweep = measure(1.01, dt=1e-4, steps=200_000)
        regression = 2.0 * math.pi - sweep
        cycle = 2.0 * math.pi / regression
        assert cycle == pytest.approx(2.0 + math.sqrt(2.0), abs=0.01)

    def test_it_is_nothing_like_the_monograph_guess(self) -> None:
        # The monograph says seasons precess over ~900 years. Recorded as a
        # contrast, not a target -- see the DERIVATION RULE.
        sweep = measure(1.01, dt=1e-4, steps=200_000)
        cycle = 2.0 * math.pi / (2.0 * math.pi - sweep)
        assert cycle < 10.0


def apsidal_angle_of(sweep: float) -> float:
    return math.degrees(sweep / 2.0)


def test_apsidal_angle_helper_returns_half_the_sweep() -> None:
    traj = integrate(
        mass=STAR,
        position=Quantity(np.array([1.0, 0.0]), LENGTH),
        velocity=Quantity(np.array([0.0, V_C * 1.01]), VELOCITY),
        timestep=Quantity(1e-4, TIME),
        steps=200_000,
    )
    assert apsidal_angle(traj) == pytest.approx(
        pericentre_to_pericentre_angle(traj) / 2.0, rel=1e-12
    )
