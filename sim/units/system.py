"""The natural unit system: G2 = 1 and sigma_2 = 1.

There is no correct SI value for a constant of another universe, so the project
does not look for one. Instead the constants are normalised to 1 and the base
units follow:

    [G2]     = M^-1 L^2 T^-2 = 1   =>   T = L / sqrt(M)
    [sigma2] = M L T^-3 K^-3  = 1   =>   K = (M L T^-3)^(1/3)

So two display anchors — what one natural mass unit and one natural length unit
are called in kilograms and metres — fix all four base units. Those anchors are
cosmetic: they set what gets printed, and no physical result depends on them.
What is physical is dimensionless ratios (see docs/AXIOMS.md section 2).

Conversion to SI exists only for display. Nothing in a computation may use it.

Axioms used: T1.1 (G2), T2.2 (sigma_2).
Abstracts: nothing.

Depends on: sim.units.dimension, sim.units.named
Used by: display and reporting code only
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sim.units.dimension import Dimension

__all__ = ["UnitSystem"]


@dataclass(frozen=True)
class UnitSystem:
    """A natural unit system in which G2 and sigma_2 are both exactly 1.

    Construct with :meth:`from_anchors` rather than directly — the time and
    temperature units are not free, and building one by hand invites a system
    where the constants are not 1.

    Attributes
    ----------
    mass_kg : float
        Kilograms per natural mass unit. A display anchor.
    length_m : float
        Metres per natural length unit. A display anchor.
    time_s : float
        Seconds per natural time unit. Derived, not chosen.
    temperature_k : float
        Kelvin per natural temperature unit. Derived, not chosen.
    """

    mass_kg: float
    length_m: float
    time_s: float
    temperature_k: float

    @classmethod
    def from_anchors(cls, mass_kg: float, length_m: float) -> UnitSystem:
        """Build the system from the two free display anchors.

        Parameters
        ----------
        mass_kg : float
            Kilograms per natural mass unit. Must be positive and finite.
        length_m : float
            Metres per natural length unit. Must be positive and finite.

        Returns
        -------
        UnitSystem
            A system in which G2 and sigma_2 both evaluate to 1.

        Raises
        ------
        ValueError
            If either anchor is non-positive or non-finite. There is no
            sensible fallback, so this raises rather than clamping.

        Examples
        --------
        >>> system = UnitSystem.from_anchors(mass_kg=1.0, length_m=1.0)
        >>> round(system.time_s, 12)
        1.0
        """
        _require_positive_finite(mass_kg, "mass_kg")
        _require_positive_finite(length_m, "length_m")

        # [G2] = M^-1 L^2 T^-2, and G2 = 1, so L^2 / (M T^2) = 1.
        time_s = length_m / math.sqrt(mass_kg)
        # [sigma_2] = M L T^-3 K^-3, and sigma_2 = 1, so K^3 = M L T^-3.
        temperature_k = (mass_kg * length_m / time_s**3) ** (1.0 / 3.0)

        return cls(
            mass_kg=mass_kg,
            length_m=length_m,
            time_s=time_s,
            temperature_k=temperature_k,
        )

    def scale_factor(self, dimension: Dimension) -> float:
        """Return the SI magnitude of one natural unit of `dimension`.

        Parameters
        ----------
        dimension : Dimension
            The dimension to scale.

        Returns
        -------
        float
            The multiplier taking a natural-unit magnitude to an SI one. Always
            1.0 for a dimensionless quantity, and — by construction — for the
            gravitational and Stefan-Boltzmann constants.

        Examples
        --------
        >>> from sim.units import GRAVITATIONAL_CONSTANT
        >>> s = UnitSystem.from_anchors(mass_kg=2.0, length_m=3.0)
        >>> round(s.scale_factor(GRAVITATIONAL_CONSTANT), 12)
        1.0
        """
        # math.pow rather than ** : typeshed types float**float as Any, since
        # a negative base with a fractional exponent is complex. Every base
        # here is positive by construction, so math.pow is both correct and
        # typed as float.
        mass, length, time, temperature = dimension.exponents
        return (
            math.pow(self.mass_kg, float(mass))
            * math.pow(self.length_m, float(length))
            * math.pow(self.time_s, float(time))
            * math.pow(self.temperature_k, float(temperature))
        )

    def to_si(self, magnitude: float, dimension: Dimension) -> float:
        """Convert a natural-unit magnitude to SI. Display only.

        Never call this from a computation — see the DERIVATION RULE in
        CLAUDE.md. It exists so a number can be printed in familiar units.
        """
        return magnitude * self.scale_factor(dimension)

    def from_si(self, magnitude: float, dimension: Dimension) -> float:
        """Convert an SI magnitude to natural units. Display only."""
        return magnitude / self.scale_factor(dimension)


def _require_positive_finite(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite, got {value!r}")
