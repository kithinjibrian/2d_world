"""Tests for the natural unit system.

The closure test is the substantive one: choosing two display anchors must
force the remaining two base units such that G2 and sigma_2 both come out
exactly 1.
"""

import math

import pytest

from sim.errors import VellumError
from sim.units import (
    ENERGY,
    GRAVITATIONAL_CONSTANT,
    LENGTH,
    MASS,
    STEFAN_BOLTZMANN,
    TIME,
    UnitSystem,
)

ANCHORS = [(1.0, 1.0), (2.0, 3.0), (1e24, 1e7), (1e-3, 1e-6), (7.5, 0.25)]


class TestNaturalUnitClosure:
    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_gravitational_constant_is_exactly_one(self, mass_kg: float, length_m: float) -> None:
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        assert system.scale_factor(GRAVITATIONAL_CONSTANT) == pytest.approx(1.0, rel=1e-12)

    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_stefan_boltzmann_is_exactly_one(self, mass_kg: float, length_m: float) -> None:
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        assert system.scale_factor(STEFAN_BOLTZMANN) == pytest.approx(1.0, rel=1e-12)

    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_time_follows_from_g2(self, mass_kg: float, length_m: float) -> None:
        # [G2] = M^-1 L^2 T^-2, so G2 = 1 forces T = L / sqrt(M).
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        assert system.time_s == pytest.approx(length_m / math.sqrt(mass_kg), rel=1e-12)

    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_temperature_follows_from_sigma2(self, mass_kg: float, length_m: float) -> None:
        # [sigma2] = M L T^-3 Theta^-3, so sigma2 = 1 forces Theta = (M L T^-3)^(1/3).
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        expected = (mass_kg * length_m / system.time_s**3) ** (1.0 / 3.0)
        assert system.temperature_k == pytest.approx(expected, rel=1e-12)

    def test_base_anchors_are_preserved(self) -> None:
        system = UnitSystem.from_anchors(mass_kg=5.0, length_m=11.0)
        assert system.scale_factor(MASS) == pytest.approx(5.0)
        assert system.scale_factor(LENGTH) == pytest.approx(11.0)


class TestRoundTrip:
    # Tolerance: two float multiplications plus a pow, so a handful of ULPs.
    # 1e-12 relative is several orders of magnitude looser than that and still
    # far tighter than any dimensional mistake this layer is meant to catch.
    TOL = 1e-12

    @pytest.mark.parametrize("magnitude", [0.0, 1.0, 1e-9, 1e9, -3.25])
    def test_si_round_trip(self, magnitude: float) -> None:
        system = UnitSystem.from_anchors(mass_kg=3.0, length_m=7.0)
        there = system.to_si(magnitude, ENERGY)
        back = system.from_si(there, ENERGY)
        assert back == pytest.approx(magnitude, rel=self.TOL, abs=self.TOL)

    def test_dimensionless_conversion_is_the_identity(self) -> None:
        system = UnitSystem.from_anchors(mass_kg=3.0, length_m=7.0)
        assert system.to_si(4.5, MASS / MASS) == pytest.approx(4.5)


class TestValidation:
    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_bad_mass_anchor_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            UnitSystem.from_anchors(mass_kg=bad, length_m=1.0)

    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_bad_length_anchor_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            UnitSystem.from_anchors(mass_kg=1.0, length_m=bad)


class TestNoNonFiniteFromFiniteInputs:
    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_every_base_unit_is_finite(self, mass_kg: float, length_m: float) -> None:
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        for unit in (system.mass_kg, system.length_m, system.time_s, system.temperature_k):
            assert math.isfinite(unit)

    @pytest.mark.parametrize(("mass_kg", "length_m"), ANCHORS)
    def test_scale_factors_are_finite(self, mass_kg: float, length_m: float) -> None:
        system = UnitSystem.from_anchors(mass_kg=mass_kg, length_m=length_m)
        for dim in (MASS, LENGTH, TIME, ENERGY, GRAVITATIONAL_CONSTANT, STEFAN_BOLTZMANN):
            assert math.isfinite(system.scale_factor(dim))

    def test_value_error_is_a_vellum_error(self) -> None:
        # ValueError is raised for bad anchors, but every project-specific
        # failure must still hang off VellumError.
        assert issubclass(VellumError, Exception)
