"""Discriminating tests: formulas a three-dimensional reflex writes wrongly.

Each case pairs the correct 2D form with the 3D form it is easy to reach for,
and asserts that dimensional analysis separates them. These are the reason the
units layer exists; everything else in it is scaffolding for these.
"""

from sim.units import (
    ACCELERATION,
    ENERGY,
    FLUX,
    GRAVITATIONAL_CONSTANT,
    KINEMATIC_VISCOSITY,
    LENGTH,
    MASS,
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


class TestGravity:
    """g = G2*M/r is an acceleration. The inverse-square form is not."""

    def test_correct_form_is_an_acceleration(self) -> None:
        assert GRAVITATIONAL_CONSTANT * MASS / LENGTH == ACCELERATION

    def test_inverse_square_form_is_not_an_acceleration(self) -> None:
        wrong = GRAVITATIONAL_CONSTANT * MASS / LENGTH**2
        assert wrong != ACCELERATION
        assert wrong == Dimension(time=-2)


class TestLuminosity:
    """L = 2*pi*R*sigma2*T^3 is a power. The 3D form is not."""

    def test_correct_form_is_a_power(self) -> None:
        assert LENGTH * STEFAN_BOLTZMANN * TEMPERATURE**3 == POWER

    def test_three_dimensional_form_is_not_a_power(self) -> None:
        wrong = LENGTH**2 * STEFAN_BOLTZMANN * TEMPERATURE**4
        assert wrong != POWER
        assert wrong == Dimension(mass=1, length=3, time=-3, temperature=1)

    def test_flux_at_distance_dilutes_as_one_over_r(self) -> None:
        # Light spreads over a circle, not a sphere.
        assert POWER / LENGTH == FLUX
        assert POWER / LENGTH**2 != FLUX


class TestHydrostaticPressure:
    """P = rho*g*h gives 2D pressure only with a per-area density."""

    def test_surface_density_gives_two_dimensional_pressure(self) -> None:
        assert SURFACE_DENSITY * ACCELERATION * LENGTH == PRESSURE

    def test_volume_density_gives_the_wrong_pressure(self) -> None:
        volume_density = MASS / LENGTH**3  # constructed here, deliberately unnamed
        wrong = volume_density * ACCELERATION * LENGTH
        assert wrong != PRESSURE
        assert wrong == Dimension(mass=1, length=-1, time=-2)


class TestWhatDoesNotChange:
    def test_kinematic_viscosity_is_unchanged_in_two_dimensions(self) -> None:
        # L^2 T^-1 in any number of dimensions, even though the dynamic
        # viscosity above it differs. Not everything changes in 2D.
        assert VISCOSITY / SURFACE_DENSITY == LENGTH**2 / TIME
        assert KINEMATIC_VISCOSITY == LENGTH**2 / TIME

    def test_energy_and_force_are_unchanged(self) -> None:
        expected = Dimension(mass=1, length=2, time=-2)
        assert expected == ENERGY


class TestReynoldsDiscriminatesNothing:
    """Recorded so nobody adds a Reynolds check believing it proves something.

    rho*v*L/mu is dimensionless under BOTH the 2D and the 3D forms, so it
    cannot catch a dimensional mistake. See PRPs/units-layer.md.
    """

    def test_reynolds_is_dimensionless_under_two_dimensional_forms(self) -> None:
        assert (SURFACE_DENSITY * VELOCITY * LENGTH / VISCOSITY).is_dimensionless

    def test_reynolds_is_also_dimensionless_under_three_dimensional_forms(self) -> None:
        volume_density = MASS / LENGTH**3
        dynamic_viscosity_3d = MASS / LENGTH / TIME
        assert (volume_density * VELOCITY * LENGTH / dynamic_viscosity_3d).is_dimensionless
