"""Tests for Quantity, the boundary type.

DECISION-015 resolved to checking at module boundaries: a Quantity carries its
dimension so that a public function can validate on the way in, and unwraps to
a raw float or array for the numerics inside.
"""

import numpy as np
import pytest

from sim.errors import DimensionError
from sim.units import (
    ACCELERATION,
    DIMENSIONLESS,
    ENERGY,
    FORCE,
    GRAVITATIONAL_CONSTANT,
    LENGTH,
    MASS,
    TIME,
    Quantity,
)


class TestBoundaryUnwrap:
    def test_magnitude_returns_the_raw_value(self) -> None:
        q = Quantity(9.81, ACCELERATION)
        assert q.magnitude(ACCELERATION) == 9.81

    def test_magnitude_rejects_the_wrong_dimension(self) -> None:
        q = Quantity(9.81, ACCELERATION)
        with pytest.raises(DimensionError) as excinfo:
            q.magnitude(FORCE)
        message = str(excinfo.value)
        # Both dimensions must appear readably; two opaque tuples cost more
        # time than they save.
        assert "L T^-2" in message
        assert "M L T^-2" in message

    def test_magnitude_accepts_arrays(self) -> None:
        values = np.array([1.0, 2.0, 3.0])
        q = Quantity(values, LENGTH)
        assert np.array_equal(q.magnitude(LENGTH), values)


class TestArithmetic:
    def test_multiplication_combines_dimensions(self) -> None:
        f = Quantity(2.0, MASS) * Quantity(3.0, ACCELERATION)
        assert f.dimension == FORCE
        assert f.magnitude(FORCE) == pytest.approx(6.0)

    def test_division_combines_dimensions(self) -> None:
        v = Quantity(10.0, LENGTH) / Quantity(2.0, TIME)
        assert v.dimension == LENGTH / TIME
        assert v.magnitude(LENGTH / TIME) == pytest.approx(5.0)

    def test_addition_requires_matching_dimensions(self) -> None:
        assert (Quantity(1.0, LENGTH) + Quantity(2.0, LENGTH)).magnitude(LENGTH) == 3.0
        with pytest.raises(DimensionError):
            _ = Quantity(1.0, LENGTH) + Quantity(2.0, TIME)

    def test_subtraction_requires_matching_dimensions(self) -> None:
        assert (Quantity(3.0, LENGTH) - Quantity(2.0, LENGTH)).magnitude(LENGTH) == 1.0
        with pytest.raises(DimensionError):
            _ = Quantity(1.0, LENGTH) - Quantity(2.0, MASS)

    def test_power_scales_the_dimension(self) -> None:
        area = Quantity(3.0, LENGTH) ** 2
        assert area.dimension == LENGTH**2
        assert area.magnitude(LENGTH**2) == pytest.approx(9.0)

    def test_scalar_multiplication_leaves_the_dimension_alone(self) -> None:
        doubled = Quantity(2.0, ENERGY) * 2.0
        assert doubled.dimension == ENERGY
        assert doubled.magnitude(ENERGY) == pytest.approx(4.0)

    def test_arrays_flow_through_arithmetic(self) -> None:
        r = Quantity(np.array([1.0, 2.0, 4.0]), LENGTH)
        m = Quantity(8.0, MASS)
        g = Quantity(1.0, GRAVITATIONAL_CONSTANT) * m / r
        assert g.dimension == ACCELERATION
        assert np.allclose(g.magnitude(ACCELERATION), [8.0, 4.0, 2.0])


class TestTheGravityFormulaEndToEnd:
    """The discriminating case, exercised through real values rather than dimensions."""

    def test_correct_form_yields_an_acceleration(self) -> None:
        g2 = Quantity(1.0, GRAVITATIONAL_CONSTANT)
        mass = Quantity(4.0, MASS)
        radius = Quantity(2.0, LENGTH)
        g = g2 * mass / radius
        assert g.magnitude(ACCELERATION) == pytest.approx(2.0)

    def test_inverse_square_form_refuses_to_be_an_acceleration(self) -> None:
        g2 = Quantity(1.0, GRAVITATIONAL_CONSTANT)
        mass = Quantity(4.0, MASS)
        radius = Quantity(2.0, LENGTH)
        wrong = g2 * mass / radius**2
        with pytest.raises(DimensionError):
            wrong.magnitude(ACCELERATION)


class TestImmutability:
    def test_quantity_is_frozen(self) -> None:
        q = Quantity(1.0, LENGTH)
        with pytest.raises((AttributeError, TypeError)):
            q.value = 2.0  # type: ignore[misc]

    def test_dimensionless_quantity_reports_itself(self) -> None:
        ratio = Quantity(3.0, LENGTH) / Quantity(1.0, LENGTH)
        assert ratio.dimension == DIMENSIONLESS
        assert ratio.magnitude(DIMENSIONLESS) == pytest.approx(3.0)
