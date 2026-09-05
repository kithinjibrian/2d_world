"""Vellum turning on itself.

A disc rotating in the plane is a legitimate motion in two dimensions: every
point moves on a circle within the plane. The rotation *axis* would be
perpendicular to the plane and therefore outside the universe, which is why
angular momentum here is a **signed scalar** rather than a vector -- there is
no direction for it to point.

Surface coordinates are **body-fixed**: a rock stays at the same `s` forever
and the frame turns around it. That is the whole content of this module;
day, night and the terminator all follow from it.

**Vellum has no axial tilt and cannot have one** -- there is no axis to tilt in
a plane -- so there is no parameter for it. Seasons come from orbital
eccentricity alone, as `docs/AXIOMS.md` section 3 records.

Axioms used: T0.1 (two dimensions), T0.2 (Newtonian mechanics), T1.1 (gravity,
for the breakup limit).
Abstracts: oblateness. A spinning body bulges; modelling that needs the
material response abstracted at T2.4, so the disc stays circular. See
docs/AXIOMS.md section 4.

Depends on: sim.units
Used by: sim.rotation.illumination, sim.view.render
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from sim.periodic import wrap
from sim.units import G2, GRAVITATIONAL_CONSTANT, MASS, TIME, Quantity

__all__ = ["Spin", "breakup_rate"]

Angle = float | NDArray[np.float64]


def breakup_rate(mass: Quantity, circumference: float) -> float:
    """Return the spin rate at which a disc flies apart.

    Centrifugal acceleration at the surface equals surface gravity when
    ``omega**2 * R == G2*M/R``, so ``omega_max = sqrt(G2*M)/R``.

    The surface speed there is ``omega_max * R = sqrt(G2*M)``, which is exactly
    the **circular orbital speed** -- and in two dimensions that speed is the
    same at every radius. So a 2D planet flies apart when its surface moves at
    the speed of an orbit anywhere in the system.

    Parameters
    ----------
    mass : Quantity
        The planet's mass, natural units.
    circumference : float
        Its surface circumference, natural units.

    Returns
    -------
    float
        Maximum sustainable angular velocity, natural units.
    """
    m = mass.scalar(MASS)
    if not math.isfinite(m) or m <= 0.0:
        raise ValueError(f"mass must be positive and finite, got {m!r}")
    if not math.isfinite(circumference) or circumference <= 0.0:
        raise ValueError(f"circumference must be positive, got {circumference!r}")
    radius = circumference / (2.0 * math.pi)
    return math.sqrt(G2.scalar(GRAVITATIONAL_CONSTANT) * m) / radius


@dataclass(frozen=True)
class Spin:
    """A rotating planet.

    Parameters
    ----------
    rate : float
        Angular velocity, radians per unit time. **A world constant, not
        derived.** Zero is legal and means a world that does not turn -- one arc
        in permanent daylight, the opposite arc never seeing the star.
    circumference : float
        The closed surface's length. The radius follows from it.
    mass : Quantity
        The planet's mass, used only to check the rate against breakup.

    Examples
    --------
    >>> from sim.units import MASS, Quantity
    >>> s = Spin(rate=1.0, circumference=6.283185307179586,
    ...          mass=Quantity(1e-6, MASS))
    >>> round(s.sidereal_day, 6)
    6.283185
    """

    rate: float
    circumference: float
    mass: Quantity

    def __post_init__(self) -> None:
        if not math.isfinite(self.rate) or self.rate < 0.0:
            raise ValueError(f"rate must be finite and non-negative, got {self.rate!r}")
        if not math.isfinite(self.circumference) or self.circumference <= 0.0:
            raise ValueError(f"circumference must be positive, got {self.circumference!r}")
        limit = breakup_rate(self.mass, self.circumference)
        if self.rate >= limit:
            raise ValueError(
                f"rate {self.rate!r} is at or above breakup ({limit:.6g}): the surface "
                "would move at least as fast as a circular orbit and the world would "
                "come apart. A planet that cannot hold together is not a world to "
                "simulate."
            )

    @property
    def radius(self) -> float:
        """Surface radius, derived from the circumference."""
        return self.circumference / (2.0 * math.pi)

    @property
    def sidereal_day(self) -> float:
        """Time for one turn against the fixed stars. Infinite if not turning."""
        return math.inf if self.rate == 0.0 else 2.0 * math.pi / self.rate

    @property
    def moment_of_inertia(self) -> float:
        """``M R**2 / 2`` for a uniform disc.

        Identical to the three-dimensional coefficient, even though the density
        integrated here is per *area* rather than per volume. One of the few
        quantities two dimensions leaves alone.
        """
        return 0.5 * self.mass.scalar(MASS) * self.radius**2

    @property
    def angular_momentum(self) -> float:
        """A signed scalar. There is no axis for it to point along."""
        return self.moment_of_inertia * self.rate

    def phase(self, time: float) -> float:
        """Return the rotation phase at `time`, in [0, 2*pi).

        Taken modulo, so it cannot drift or lose precision over long runs.
        """
        return float(wrap(self.rate * time, 2.0 * math.pi))

    def inertial_angle(self, surface: Angle, time: float) -> Angle:
        """Map a body-fixed surface coordinate to its angle in space."""
        return (
            2.0 * math.pi * wrap(surface, self.circumference) / self.circumference
            + self.phase(time)
        )

    def surface_at_inertial_angle(self, angle: Angle, time: float) -> Angle:
        """Map an angle in space back to the surface coordinate now there."""
        turns = wrap(angle - self.phase(time), 2.0 * math.pi) / (2.0 * math.pi)
        return wrap(turns * self.circumference, self.circumference)

    def solar_day(self, orbital_rate: Quantity) -> float:
        """Return the time between successive noons.

        Different from the sidereal day, because the planet moves along its
        orbit while it turns. Conflating the two is the classic error, so both
        are available and named.

        Returns
        -------
        float
            Infinite when the spin matches the orbital rate — the world then
            keeps one arc facing the star forever.
        """
        relative = self.rate - orbital_rate.scalar(TIME**-1)
        return math.inf if relative == 0.0 else 2.0 * math.pi / relative
