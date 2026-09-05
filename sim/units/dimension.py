"""Physical dimensions in two spatial dimensions.

A Dimension is a vector of exponents over four base dimensions — mass, length,
time, temperature. It carries no magnitude; it is the type of a quantity, not
the quantity. The named dimensions at the bottom of this module are the
authoritative in-code copy of docs/AXIOMS.md section 2.

Exponents are Fractions rather than ints because setting sigma_2 = 1 fixes the
temperature scale through a cube root (see sim.units.system), which an integer
exponent cannot express.

No three-dimensional form is defined anywhere in this module. That is
deliberate: a name that exists can be selected by accident, and a name that
does not exist cannot. See the Must NOT Do section of PRPs/units-layer.md.

Axioms used: T0.1 (two spatial dimensions), T0.2 (Newtonian mechanics),
T1.1 (gravity as a direct force), T2.2 (radiation with T^3 emission).
Abstracts: nothing. This is the only module in the project able to say that.

Depends on: sim.errors
Used by: sim.units.quantity, sim.units.system, sim.units.constants
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from fractions import Fraction
from typing import Final, TypeAlias, cast

from sim.errors import DimensionError

__all__ = ["Dimension", "Exponent"]

#: What may be passed as an exponent. Coerced to Fraction on construction, so
#: every exponent is a Fraction once the object exists — see `exponents`.
Exponent: TypeAlias = Fraction | int

_SYMBOLS: Final = (("mass", "M"), ("length", "L"), ("time", "T"), ("temperature", "K"))


@dataclass(frozen=True)
class Dimension:
    """The dimensions of a physical quantity, as exponents over the base set.

    Immutable and hashable. Arithmetic returns new instances and never mutates
    an operand.

    Parameters
    ----------
    mass, length, time, temperature : Fraction | int
        Exponents over the four base dimensions. Integers are coerced to
        Fraction, so ``Dimension(mass=1)`` and ``Dimension(mass=Fraction(1))``
        are equal and hash alike.

    Examples
    --------
    >>> from sim.units import MASS, ACCELERATION, FORCE
    >>> MASS * ACCELERATION == FORCE
    True
    """

    mass: Exponent = 0
    length: Exponent = 0
    time: Exponent = 0
    temperature: Exponent = 0

    def __post_init__(self) -> None:
        # Coerce so that Dimension(mass=1) equals and hashes like
        # Dimension(mass=Fraction(1)). Frozen dataclasses require the
        # object.__setattr__ escape hatch to normalise a field.
        for field in fields(self):
            object.__setattr__(self, field.name, Fraction(getattr(self, field.name)))

    @property
    def is_dimensionless(self) -> bool:
        """True when every exponent is zero."""
        return all(getattr(self, name) == 0 for name, _ in _SYMBOLS)

    @property
    def exponents(self) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        """The exponents as a tuple, ordered (mass, length, time, temperature).

        Always Fractions: __post_init__ coerces on construction, so this is the
        type-safe accessor for anyone who needs that guarantee.
        """
        return cast(
            "tuple[Fraction, Fraction, Fraction, Fraction]",
            (self.mass, self.length, self.time, self.temperature),
        )

    def __mul__(self, other: Dimension) -> Dimension:
        """Combine two dimensions by adding their exponents."""
        if not isinstance(other, Dimension):
            raise DimensionError(
                f"cannot multiply a Dimension by {type(other).__name__}; "
                "a Dimension has no magnitude, so scaling it is meaningless"
            )
        return Dimension(
            self.mass + other.mass,
            self.length + other.length,
            self.time + other.time,
            self.temperature + other.temperature,
        )

    def __truediv__(self, other: Dimension) -> Dimension:
        """Combine two dimensions by subtracting their exponents."""
        if not isinstance(other, Dimension):
            raise DimensionError(
                f"cannot divide a Dimension by {type(other).__name__}; "
                "a Dimension has no magnitude, so scaling it is meaningless"
            )
        return Dimension(
            self.mass - other.mass,
            self.length - other.length,
            self.time - other.time,
            self.temperature - other.temperature,
        )

    def __pow__(self, exponent: Exponent) -> Dimension:
        """Raise a dimension to a power, multiplying every exponent."""
        factor = Fraction(exponent)
        return Dimension(
            self.mass * factor,
            self.length * factor,
            self.time * factor,
            self.temperature * factor,
        )

    def __str__(self) -> str:
        """Render readably, e.g. ``M L T^-2``.

        Used in DimensionError messages: a mismatch reported as two opaque
        tuples costs more time to read than it saves to write.
        """
        parts: list[str] = []
        for name, symbol in _SYMBOLS:
            power: Fraction = getattr(self, name)
            if power == 0:
                continue
            parts.append(symbol if power == 1 else f"{symbol}^{power}")
        return " ".join(parts) if parts else "dimensionless"

    def __repr__(self) -> str:
        return f"Dimension({self})"
