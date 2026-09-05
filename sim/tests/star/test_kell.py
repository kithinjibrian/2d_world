"""Tests for the Kell stub.

The stub exists to be replaced. Its most important behaviour is refusing to
answer questions it cannot honestly answer: a stub that returns a plausible
default is never revisited and silently becomes the model (anti-pattern 5).
"""

import pytest

from sim.star import Kell
from sim.units import LUMINOSITY, MASS, Quantity


def a_star() -> Kell:
    return Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))


class TestWhatItSupplies:
    def test_mass_is_a_world_constant(self) -> None:
        assert a_star().mass.scalar(MASS) == 1.0

    def test_luminosity_is_a_swept_parameter(self) -> None:
        assert a_star().luminosity.scalar(LUMINOSITY) == 1.0

    def test_rejects_non_positive_mass(self) -> None:
        with pytest.raises(ValueError):
            Kell(mass=Quantity(0.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))

    def test_rejects_non_positive_luminosity(self) -> None:
        with pytest.raises(ValueError):
            Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(-1.0, LUMINOSITY))

    def test_rejects_wrong_dimensions(self) -> None:
        from sim.errors import DimensionError
        from sim.units import LENGTH

        with pytest.raises(DimensionError):
            Kell(mass=Quantity(1.0, LENGTH), luminosity=Quantity(1.0, LUMINOSITY))


class TestWhatItRefuses:
    """Every one of these raises rather than guessing. See DECISION-010."""

    @pytest.mark.parametrize("attribute", ["radius", "effective_temperature", "lifetime"])
    def test_derived_stellar_properties_raise(self, attribute: str) -> None:
        with pytest.raises(NotImplementedError) as excinfo:
            getattr(a_star(), attribute)
        # The message must point at the decision, so whoever hits it knows the
        # stub is deliberate rather than unfinished by accident.
        assert "DECISION-010" in str(excinfo.value)

    def test_spectrum_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            a_star().spectrum()

    def test_evolution_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            a_star().luminosity_at_age(Quantity(1.0, MASS))
