"""A stubbed star.

DECISION-010: Kell's structure is not solved. Mass is a world constant and
luminosity is a swept parameter (DECISION-009), supplied from outside rather
than derived from stellar physics.

Under a scan this is not a placeholder so much as an extra axis of the sweep.
Deriving the star later does not invalidate anything -- it *collapses* that
axis, by predicting luminosity from stellar mass instead of sweeping it
independently. That is a better position to derive a star from than the
beginning, because by then there will be a map of which luminosities matter.

Everything beyond mass and luminosity raises. A stub that returns a plausible
default is never revisited and silently becomes the model -- see anti-pattern 5
in CLAUDE.md. Any result computed from this object's luminosity is a
consequence of a chosen parameter, not a finding about stellar physics.

Axioms used: T2.2.
Abstracts: Kell's luminosity, and all of stellar structure.

Depends on: sim.units
Used by: sim.orbit.insolation
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NoReturn

from sim.units import LUMINOSITY, MASS, Quantity

__all__ = ["Kell"]

_STUB = (
    "Kell is stubbed: its structure is not solved, so {what} is not available. "
    "See DECISION-010 and docs/AXIOMS.md section 4. This raises rather than "
    "returning a default, because a stub that answers everything is never replaced."
)


@dataclass(frozen=True)
class Kell:
    """Vellum's star, as far as the simulation currently models it.

    Parameters
    ----------
    mass : Quantity
        Stellar mass, in natural units. A world constant.
    luminosity : Quantity
        Radiated power, in natural units. A swept parameter, ABSTRACTED --
        not derived from anything.

    Examples
    --------
    >>> from sim.units import LUMINOSITY, MASS, Quantity
    >>> kell = Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))
    >>> kell.mass.magnitude(MASS)
    1.0
    """

    mass: Quantity
    luminosity: Quantity

    def __post_init__(self) -> None:
        # Validate at the boundary: these are the only two values this object
        # will ever vouch for, so they had better be real.
        for value, dimension, name in (
            (self.mass, MASS, "mass"),
            (self.luminosity, LUMINOSITY, "luminosity"),
        ):
            magnitude = value.scalar(dimension)
            if not math.isfinite(magnitude):
                raise ValueError(f"{name} must be finite, got {magnitude!r}")
            if magnitude <= 0.0:
                raise ValueError(f"{name} must be positive, got {magnitude!r}")

    @property
    def radius(self) -> NoReturn:
        """Not available — requires solving 2D stellar structure."""
        raise NotImplementedError(_STUB.format(what="radius"))

    @property
    def effective_temperature(self) -> NoReturn:
        """Not available — requires solving 2D stellar structure."""
        raise NotImplementedError(_STUB.format(what="effective temperature"))

    @property
    def lifetime(self) -> NoReturn:
        """Not available — requires a nuclear energy source, which is not modelled."""
        raise NotImplementedError(_STUB.format(what="lifetime"))

    def spectrum(self) -> NoReturn:
        """Not available — radiative transfer is grey at best, and T1.2 abstracts EM."""
        raise NotImplementedError(_STUB.format(what="a spectrum"))

    def luminosity_at_age(self, age: Quantity) -> NoReturn:
        """Not available — stellar evolution is not modelled."""
        raise NotImplementedError(_STUB.format(what="luminosity as a function of age"))
