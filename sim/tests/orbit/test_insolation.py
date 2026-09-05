"""Insolation: flux dilutes as 1/r, because light spreads over a circle.

Every result here rests on Kell's stubbed luminosity (docs/AXIOMS.md section 4),
so none of it is a finding about stellar physics.
"""

import math

import numpy as np
import pytest

from sim.errors import DimensionError
from sim.orbit import circular_speed, flux_at, insolation_series, integrate
from sim.star import Kell
from sim.units import FLUX, LENGTH, LUMINOSITY, MASS, POWER, TIME, VELOCITY, Quantity

KELL = Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(4.0, LUMINOSITY))


class TestDilution:
    def test_flux_carries_the_flux_dimension(self) -> None:
        assert flux_at(KELL.luminosity, Quantity(2.0, LENGTH)).dimension == FLUX

    def test_flux_falls_as_one_over_r(self) -> None:
        near = flux_at(KELL.luminosity, Quantity(1.0, LENGTH)).scalar(FLUX)
        far = flux_at(KELL.luminosity, Quantity(4.0, LENGTH)).scalar(FLUX)
        assert far == pytest.approx(near / 4.0)

    def test_flux_does_not_fall_as_one_over_r_squared(self) -> None:
        near = flux_at(KELL.luminosity, Quantity(1.0, LENGTH)).scalar(FLUX)
        far = flux_at(KELL.luminosity, Quantity(4.0, LENGTH)).scalar(FLUX)
        assert far != pytest.approx(near / 16.0)

    def test_value_is_luminosity_over_two_pi_r(self) -> None:
        got = flux_at(KELL.luminosity, Quantity(2.0, LENGTH)).scalar(FLUX)
        assert got == pytest.approx(4.0 / (2.0 * math.pi * 2.0))

    def test_rejects_a_non_luminosity(self) -> None:
        with pytest.raises(DimensionError):
            flux_at(Quantity(1.0, POWER / LENGTH), Quantity(1.0, LENGTH))

    def test_rejects_non_positive_distance(self) -> None:
        with pytest.raises(ValueError):
            flux_at(KELL.luminosity, Quantity(0.0, LENGTH))


class TestSeriesOverAnOrbit:
    def test_series_tracks_the_trajectory(self) -> None:
        v_c = circular_speed(KELL.mass, Quantity(1.0, LENGTH)).scalar(VELOCITY)
        traj = integrate(
            mass=KELL.mass,
            position=Quantity(np.array([1.0, 0.0]), LENGTH),
            velocity=Quantity(np.array([0.0, v_c * 1.2]), VELOCITY),
            timestep=Quantity(1e-3, TIME),
            steps=20_000,
        )
        series = insolation_series(KELL, traj).array(FLUX)
        assert series.shape == (20_000,)
        assert np.all(series > 0.0)
        # Insolation is highest where the planet is closest.
        assert int(np.argmax(series)) == int(np.argmin(traj.radius))

    def test_a_circular_orbit_has_constant_insolation(self) -> None:
        v_c = circular_speed(KELL.mass, Quantity(1.0, LENGTH)).scalar(VELOCITY)
        traj = integrate(
            mass=KELL.mass,
            position=Quantity(np.array([1.0, 0.0]), LENGTH),
            velocity=Quantity(np.array([0.0, v_c]), VELOCITY),
            timestep=Quantity(1e-3, TIME),
            steps=10_000,
        )
        series = insolation_series(KELL, traj).array(FLUX)
        assert float(series.max() - series.min()) < 1e-6 * float(series.mean())
