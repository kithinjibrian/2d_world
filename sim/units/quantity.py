"""Quantity — a value paired with its dimensions, for use at module boundaries.

DECISION-015 resolved that dimensions are checked at module boundaries rather
than carried through inner loops. So a public function accepts and returns
Quantity, validates on the way in with ``magnitude()``, and works with the
unwrapped float or array inside. The cost is one check per call rather than one
per element, which matters because DECISION-009 multiplies any inner-loop cost
by the size of the parameter scan.

The failure this guards against — a constant or a formula composed with the
wrong dimensions — happens at definition and composition, which are exactly the
boundaries. It does not happen inside a loop that has already been handed
correct arrays.

Axioms used: none directly; this is apparatus, not physics.
Abstracts: nothing.

Depends on: sim.errors, sim.units.dimension
Used by: every module with a public numerical interface
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

from sim.errors import DimensionError
from sim.units.dimension import Dimension, Exponent

__all__ = ["Quantity", "Value"]

#: A magnitude: either a scalar or an array of them. Never carries units.
Value: TypeAlias = float | NDArray[np.float64]


@dataclass(frozen=True, eq=False)
class Quantity:
    """A magnitude in natural units, tagged with its dimensions.

    Equality is deliberately not defined: a Quantity may hold an array, for
    which ``==`` is elementwise and has no single truth value. Compare
    ``.dimension`` and ``.magnitude(...)`` separately.

    Parameters
    ----------
    value : float | NDArray[np.float64]
        The magnitude, in natural units (see sim.units.system). Never SI.
    dimension : Dimension
        What the magnitude is a magnitude of.

    Examples
    --------
    >>> from sim.units import Quantity, MASS, ACCELERATION, FORCE
    >>> f = Quantity(2.0, MASS) * Quantity(3.0, ACCELERATION)
    >>> f.magnitude(FORCE)
    6.0
    """

    value: Value
    dimension: Dimension

    def magnitude(self, expected: Dimension) -> Value:
        """Unwrap to a raw magnitude, checking the dimensions first.

        This is the boundary crossing: past this point the numerics work on
        plain floats and arrays. Naming the expected dimension at the call site
        is the point — it documents what the caller believes it is holding, and
        that belief is what gets checked.

        Parameters
        ----------
        expected : Dimension
            The dimension the caller requires.

        Returns
        -------
        float | NDArray[np.float64]
            The magnitude, in natural units.

        Raises
        ------
        DimensionError
            If the quantity's dimension is not exactly `expected`. Both
            dimensions appear in the message.

        Examples
        --------
        >>> from sim.units import Quantity, ACCELERATION
        >>> Quantity(9.81, ACCELERATION).magnitude(ACCELERATION)
        9.81
        """
        if self.dimension != expected:
            raise DimensionError(
                f"expected a quantity in [{expected}], got [{self.dimension}]"
            )
        return self.value

    def scalar(self, expected: Dimension) -> float:
        """Unwrap to a single float, checking dimensions and shape.

        Use this wherever the caller knows it is holding one value. It exists
        because ``magnitude`` returns ``float | NDArray``, which every caller
        would otherwise have to narrow by hand — and a narrowing written by
        hand at forty call sites is a narrowing that will be wrong at one.

        Parameters
        ----------
        expected : Dimension
            The dimension the caller requires.

        Returns
        -------
        float

        Raises
        ------
        DimensionError
            If the dimension does not match.
        ValueError
            If the value is an array rather than a scalar.

        Examples
        --------
        >>> from sim.units import Quantity, LENGTH
        >>> Quantity(2.0, LENGTH).scalar(LENGTH)
        2.0
        """
        value = self.magnitude(expected)
        if not isinstance(value, float):
            raise ValueError(
                f"expected a scalar quantity in [{expected}], got an array of "
                f"shape {np.shape(value)}"
            )
        return value

    def array(self, expected: Dimension) -> NDArray[np.float64]:
        """Unwrap to a float64 array, checking dimensions.

        A scalar is promoted to a zero-dimensional array rather than rejected,
        so callers that accept either shape need only one path.

        Parameters
        ----------
        expected : Dimension
            The dimension the caller requires.

        Returns
        -------
        NDArray[np.float64]

        Raises
        ------
        DimensionError
            If the dimension does not match.
        """
        return np.asarray(self.magnitude(expected), dtype=np.float64)

    def __mul__(self, other: Quantity | float) -> Quantity:
        """Multiply, combining dimensions. A plain number leaves them alone."""
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.dimension * other.dimension)
        return Quantity(self.value * other, self.dimension)

    def __rmul__(self, other: float) -> Quantity:
        return Quantity(other * self.value, self.dimension)

    def __truediv__(self, other: Quantity | float) -> Quantity:
        """Divide, combining dimensions. A plain number leaves them alone."""
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.dimension / other.dimension)
        return Quantity(self.value / other, self.dimension)

    def __add__(self, other: Quantity) -> Quantity:
        """Add, requiring identical dimensions."""
        self._require_same(other, "add")
        return Quantity(self.value + other.value, self.dimension)

    def __sub__(self, other: Quantity) -> Quantity:
        """Subtract, requiring identical dimensions."""
        self._require_same(other, "subtract")
        return Quantity(self.value - other.value, self.dimension)

    def __neg__(self) -> Quantity:
        return Quantity(-self.value, self.dimension)

    def __pow__(self, exponent: Exponent) -> Quantity:
        """Raise to a power, scaling the dimension by the same exponent."""
        return Quantity(self.value ** float(exponent), self.dimension**exponent)

    def _require_same(self, other: Quantity, verb: str) -> None:
        if self.dimension != other.dimension:
            raise DimensionError(
                f"cannot {verb} [{self.dimension}] and [{other.dimension}]: "
                "only quantities of the same dimension may be combined additively"
            )

    def __repr__(self) -> str:
        return f"Quantity({self.value!r}, {self.dimension})"
