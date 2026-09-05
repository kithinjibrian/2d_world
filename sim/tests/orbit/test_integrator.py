"""Integrator invariants: conservation, boundedness, finiteness.

The boundedness test is unusually strong for orbital code. A logarithmic
potential is unbounded above, so there is no escape velocity at any speed --
an integrator that ever produces an unbound trajectory is broken, and that is
a statement about every trajectory rather than a tolerance.
"""

import math

import numpy as np
import pytest

from sim.errors import InvariantError
from sim.orbit import (
    circular_speed,
    integrate,
    radial_turning_radius,
    specific_angular_momentum,
    specific_energy,
    turning_radius,
)
from sim.units import LENGTH, MASS, TIME, VELOCITY, Quantity

STAR = Quantity(1.0, MASS)
V_C = circular_speed(STAR, Quantity(1.0, LENGTH)).scalar(VELOCITY)


def run(speed: float, dt: float = 1e-3, steps: int = 20_000, radius: float = 1.0):  # type: ignore[no-untyped-def]
    return integrate(
        mass=STAR,
        position=Quantity(np.array([radius, 0.0]), LENGTH),
        velocity=Quantity(np.array([0.0, speed]), VELOCITY),
        timestep=Quantity(dt, TIME),
        steps=steps,
    )


class TestNothingEscapes:
    """No escape velocity exists — but that is an analytic fact, not one an
    integration can demonstrate at speed.

    The turning radius for a launch at speed v is r0 * exp(v^2 / (2*G2*M)). It
    is finite for every v, which is what "nothing escapes" means. But it grows
    exponentially, so at 100x the circular speed it is about e^5000 and no
    integration will ever reach it. A run that merely fails to turn around has
    demonstrated nothing. So boundedness is asserted two ways: integrated where
    the turning point is reachable, analytically where it is not.
    """

    @pytest.mark.parametrize("factor", [1.5, 2.0, 2.5])
    def test_trajectory_turns_around_when_the_turn_is_reachable(self, factor: float) -> None:
        traj = run(V_C * factor, dt=1e-3, steps=120_000)
        radii = traj.radius
        assert float(radii[-1]) < float(radii.max())

    @pytest.mark.parametrize("factor", [1.5, 2.0, 2.5])
    def test_integrated_maximum_matches_the_analytic_turning_radius(
        self, factor: float
    ) -> None:
        # Cross-checks the screening path against the full solve, in both
        # directions: a disagreement is a bug in one of them.
        traj = run(V_C * factor, dt=1e-3, steps=120_000)
        predicted = turning_radius(
            mass=STAR,
            radius=Quantity(1.0, LENGTH),
            radial_speed=Quantity(0.0, VELOCITY),
            tangential_speed=Quantity(V_C * factor, VELOCITY),
        ).scalar(LENGTH)
        assert float(traj.radius.max()) == pytest.approx(predicted, rel=1e-3)

    @pytest.mark.parametrize("factor", [1.0, 3.0, 10.0, 30.0])
    def test_turning_radius_is_finite_at_every_speed(self, factor: float) -> None:
        r = radial_turning_radius(
            STAR, Quantity(1.0, LENGTH), Quantity(V_C * factor, VELOCITY)
        ).scalar(LENGTH)
        assert math.isfinite(float(r))

    def test_turning_radius_grows_exponentially_with_speed(self) -> None:
        def turn(factor: float) -> float:
            value = radial_turning_radius(
                STAR, Quantity(1.0, LENGTH), Quantity(V_C * factor, VELOCITY)
            ).scalar(LENGTH)
            assert isinstance(value, float)
            return value

        # r_max = exp(v^2/2) with G2 = M = 1, so doubling v squares... rather,
        # quadruples the exponent.
        assert turn(2.0) == pytest.approx(math.exp(2.0), rel=1e-12)
        assert turn(4.0) == pytest.approx(math.exp(8.0), rel=1e-12)

    def test_beyond_about_38x_circular_the_turn_is_unrepresentable(self) -> None:
        """Still bound; the number just will not fit in a float.

        exp() overflows past an argument of ~709, so v^2/2 > 709 means
        v > ~37.7. Recorded because it is a surprising practical limit: the
        distance a fast object reaches before turning back becomes
        unrepresentable very quickly.
        """
        with pytest.raises(ValueError) as excinfo:
            radial_turning_radius(
                STAR, Quantity(1.0, LENGTH), Quantity(V_C * 40.0, VELOCITY)
            )
        assert "still bound" in str(excinfo.value)

    def test_state_stays_finite_even_at_extreme_speed(self) -> None:
        # It will not turn around within the window, and that is expected --
        # see the class docstring. What must hold is that nothing diverges.
        traj = run(V_C * 100.0, dt=1e-3, steps=60_000)
        assert np.all(np.isfinite(traj.positions))
        assert float(traj.radius.min()) > 0.0


class TestConservation:
    def test_energy_drift_is_bounded_not_secular(self) -> None:
        # Velocity-Verlet is symplectic, so energy oscillates within a bounded
        # band rather than drifting. Compare the drift of the first half of the
        # run against the second: a secular scheme would grow, this must not.
        traj = run(V_C * 1.05, dt=1e-3, steps=200_000)
        energy = specific_energy(traj, STAR)
        first, second = energy[: len(energy) // 2], energy[len(energy) // 2 :]
        spread_first = float(first.max() - first.min())
        spread_second = float(second.max() - second.min())
        assert spread_second < 2.0 * spread_first + 1e-12

    def test_relative_energy_error_is_small(self) -> None:
        traj = run(V_C * 1.05, dt=1e-4, steps=100_000)
        energy = specific_energy(traj, STAR)
        scale = float(np.abs(energy).max()) or 1.0
        assert float(energy.max() - energy.min()) / scale < 1e-6

    def test_angular_momentum_is_conserved(self) -> None:
        traj = run(V_C * 1.05, dt=1e-4, steps=100_000)
        angular = specific_angular_momentum(traj)
        assert float(angular.max() - angular.min()) < 1e-9 * abs(float(angular[0]))

    def test_angular_momentum_is_a_scalar_in_two_dimensions(self) -> None:
        # There is no axis to point along, so it is a signed scalar per sample.
        traj = run(V_C, dt=1e-3, steps=1_000)
        assert specific_angular_momentum(traj).shape == (1_000,)


class TestValidation:
    def test_non_finite_state_is_impossible_from_finite_inputs(self) -> None:
        traj = run(V_C * 3.0, dt=1e-3, steps=50_000)
        assert np.all(np.isfinite(traj.positions))
        assert np.all(np.isfinite(traj.velocities))

    def test_radius_is_always_strictly_positive(self) -> None:
        traj = run(V_C * 1.2, dt=1e-3, steps=50_000)
        assert float(traj.radius.min()) > 0.0

    @pytest.mark.parametrize("bad", [0.0, -1e-3, float("nan"), float("inf")])
    def test_bad_timestep_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            run(V_C, dt=bad, steps=10)

    def test_non_positive_steps_raises(self) -> None:
        with pytest.raises(ValueError):
            run(V_C, steps=0)

    def test_starting_at_the_origin_raises(self) -> None:
        # The logarithmic potential is singular at r = 0.
        with pytest.raises(ValueError):
            run(V_C, radius=0.0)

    def test_radial_infall_into_the_singularity_raises(self) -> None:
        # Launched with no angular momentum, the particle falls straight in.
        # That is a setup error, and it must surface rather than produce inf.
        with pytest.raises((InvariantError, ValueError)):
            integrate(
                mass=STAR,
                position=Quantity(np.array([1.0, 0.0]), LENGTH),
                velocity=Quantity(np.array([0.0, 0.0]), VELOCITY),
                timestep=Quantity(1e-3, TIME),
                steps=200_000,
            )


class TestDeterminism:
    def test_identical_inputs_reproduce_identical_output(self) -> None:
        a = run(V_C * 1.05, dt=1e-3, steps=5_000)
        b = run(V_C * 1.05, dt=1e-3, steps=5_000)
        assert np.array_equal(a.positions, b.positions)
        assert np.array_equal(a.velocities, b.velocities)


class TestOrbitScaleDoesNotDrift:
    """The invariant that actually catches a non-symplectic integrator here.

    Measured during Session 9: apsidal precession is NOT the sensitive quantity
    in a logarithmic potential. Forward Euler injects energy steadily -- the
    orbit's maximum radius grew from 1.10 to 2.13 over 1500 time units -- yet
    the measured apsidal sweep moved by under 0.001 degrees. The reason is that
    a logarithmic potential is scale-invariant (r -> k*r with t -> k*t leaves
    the equation of motion unchanged), so an orbit inflated by numerical energy
    is very nearly a rescaled copy of itself, with the same shape and the same
    apsidal angle.

    What secular drift wrecks instead is the orbit's *scale*, and flux goes as
    1/r. A doubled radius halves the insolation with no visible symptom in the
    precession measurement -- exactly the plausible-wrong-number failure this
    project is built to prevent, just located somewhere other than where the
    PRP predicted.
    """

    def test_maximum_radius_is_the_same_early_and_late(self) -> None:
        traj = run(V_C * 1.05, dt=1e-3, steps=400_000)
        radius = traj.radius
        tenth = len(radius) // 10
        early = float(radius[:tenth].max())
        late = float(radius[-tenth:].max())
        # Verlet holds this to ~1e-8. Euler inflates the orbit by tens of
        # percent over the same run.
        assert late == pytest.approx(early, rel=1e-6)

    def test_energy_band_does_not_widen_with_run_length(self) -> None:
        short = specific_energy(run(V_C * 1.05, dt=1e-3, steps=50_000), STAR)
        long = specific_energy(run(V_C * 1.05, dt=1e-3, steps=400_000), STAR)
        band_short = float(short.max() - short.min())
        band_long = float(long.max() - long.min())
        # Bounded, not secular: an eightfold longer run must not widen the band.
        assert band_long < 2.0 * band_short + 1e-12
