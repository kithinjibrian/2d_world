"""Tests for the dimension algebra and the named-dimension table.

The named-dimension test is the executable copy of docs/AXIOMS.md section 2.
If either drifts from the other, it must fail.
"""

from fractions import Fraction
from typing import ClassVar

import pytest

from sim.errors import DimensionError
from sim.units import (
    ACCELERATION,
    DIMENSIONLESS,
    ENERGY,
    FLUX,
    FORCE,
    GRAVITATIONAL_CONSTANT,
    KINEMATIC_VISCOSITY,
    LENGTH,
    MASS,
    NAMED_DIMENSIONS,
    POWER,
    PRESSURE,
    STEFAN_BOLTZMANN,
    SURFACE_DENSITY,
    TEMPERATURE,
    TIME,
    VELOCITY,
    VISCOSITY,
    Dimension,
)


class TestAlgebra:
    def test_multiplication_adds_exponents(self) -> None:
        expected = Dimension(mass=1, length=1)
        assert expected == MASS * LENGTH

    def test_division_subtracts_exponents(self) -> None:
        assert LENGTH / TIME == VELOCITY

    def test_power_multiplies_exponents(self) -> None:
        expected = Dimension(length=2)
        assert expected == LENGTH**2

    def test_dimensionless_is_the_identity(self) -> None:
        assert FORCE * DIMENSIONLESS == FORCE
        assert FORCE / FORCE == DIMENSIONLESS
        assert DIMENSIONLESS.is_dimensionless

    def test_fractional_exponents_survive_a_cube_root(self) -> None:
        # sigma_2 = 1 fixes the temperature scale through a cube root, so a
        # dimension system restricted to integer exponents cannot express it.
        root = (MASS * LENGTH / TIME**3) ** Fraction(1, 3)
        assert root**3 == MASS * LENGTH / TIME**3
        assert root.mass == Fraction(1, 3)

    def test_int_exponents_are_coerced_to_fractions(self) -> None:
        assert isinstance(Dimension(mass=1).mass, Fraction)

    def test_is_immutable(self) -> None:
        with pytest.raises((AttributeError, TypeError)):
            MASS.mass = Fraction(2)  # type: ignore[misc]

    def test_is_hashable(self) -> None:
        assert len({FORCE, FORCE, ENERGY}) == 2

    def test_algebra_does_not_mutate_operands(self) -> None:
        before = (FORCE.mass, FORCE.length, FORCE.time, FORCE.temperature)
        _ = FORCE * LENGTH / TIME**2
        assert (FORCE.mass, FORCE.length, FORCE.time, FORCE.temperature) == before

    def test_str_is_readable(self) -> None:
        assert str(DIMENSIONLESS) == "dimensionless"
        assert str(FORCE) == "M L T^-2"

    def test_multiplying_by_a_non_dimension_raises(self) -> None:
        with pytest.raises(DimensionError):
            _ = MASS * 2  # type: ignore[operator]


class TestNamedDimensions:
    """The executable copy of docs/AXIOMS.md section 2.

    Exponents are (mass, length, time, temperature).
    """

    EXPECTED: ClassVar[dict[str, tuple[int, int, int, int]]] = {
        "MASS": (1, 0, 0, 0),
        "LENGTH": (0, 1, 0, 0),
        "TIME": (0, 0, 1, 0),
        "TEMPERATURE": (0, 0, 0, 1),
        "VELOCITY": (0, 1, -1, 0),
        "ACCELERATION": (0, 1, -2, 0),
        "FORCE": (1, 1, -2, 0),
        "ENERGY": (1, 2, -2, 0),
        "POWER": (1, 2, -3, 0),
        # Differs from 3D: mass per unit AREA, not volume.
        "SURFACE_DENSITY": (1, -2, 0, 0),
        # Differs from 3D: force per unit LENGTH, not area.
        "PRESSURE": (1, 0, -2, 0),
        # Power per unit LENGTH of radiating curve, not per area.
        "FLUX": (1, 1, -3, 0),
        # Differs from 3D (m^3 kg^-1 s^-2).
        "GRAVITATIONAL_CONSTANT": (-1, 2, -2, 0),
        # Emission goes as T^3, so sigma_2 carries Theta^-3.
        "STEFAN_BOLTZMANN": (1, 1, -3, -3),
        # Differs from 3D (M L^-1 T^-1).
        "VISCOSITY": (1, 0, -1, 0),
        # Does NOT differ from 3D. Not everything changes in two dimensions.
        "KINEMATIC_VISCOSITY": (0, 2, -1, 0),
    }

    @pytest.mark.parametrize("name", sorted(EXPECTED))
    def test_matches_axioms_table(self, name: str) -> None:
        m, ln, t, th = self.EXPECTED[name]
        assert NAMED_DIMENSIONS[name] == Dimension(
            mass=m, length=ln, time=t, temperature=th
        ), f"{name} disagrees with docs/AXIOMS.md section 2"

    def test_registry_covers_every_expected_name(self) -> None:
        assert set(self.EXPECTED) <= set(NAMED_DIMENSIONS)

    def test_no_three_dimensional_forms_are_defined(self) -> None:
        """A name that exists can be selected by accident; one that does not, cannot.

        See the Must NOT Do section of PRPs/units-layer.md.
        """
        forbidden = {"DENSITY_3D", "VOLUME_DENSITY", "PRESSURE_3D", "VOLUME"}
        assert forbidden & set(NAMED_DIMENSIONS) == set()

    def test_composites_agree_with_their_definitions(self) -> None:
        assert FORCE == MASS * ACCELERATION
        assert ENERGY == FORCE * LENGTH
        assert POWER == ENERGY / TIME
        assert FLUX == POWER / LENGTH
        assert PRESSURE == FORCE / LENGTH
        assert GRAVITATIONAL_CONSTANT == FORCE * LENGTH / MASS**2
        assert STEFAN_BOLTZMANN == FLUX / TEMPERATURE**3
        assert KINEMATIC_VISCOSITY == VISCOSITY / SURFACE_DENSITY
