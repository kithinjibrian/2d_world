"""Flux arriving at Vellum from Kell.

Light spreads over a **circle**, not a sphere, so flux dilutes as ``1/r`` and
not ``1/r^2``. Insolation therefore falls off far more slowly with distance
than it would in three dimensions, and the habitable zone is correspondingly
wide.

Every value here rests on Kell's stubbed luminosity, so **no result from this
module is a finding about stellar physics** — each is a consequence of a chosen
parameter. See docs/AXIOMS.md section 4.

Axioms used: T2.2 (radiation in 2D).
Abstracts: Kell's luminosity, via sim.star.Kell.

Depends on: sim.star, sim.units
Used by: the climate layers, when they exist
"""

from __future__ import annotations

import math

import numpy as np

from sim.orbit.integrator import Trajectory
from sim.star import Kell
from sim.units import FLUX, LENGTH, LUMINOSITY, Quantity

__all__ = ["flux_at", "insolation_series"]


def flux_at(luminosity: Quantity, distance: Quantity) -> Quantity:
    """Return the flux at a distance from a source: ``L / (2*pi*r)``.

    Parameters
    ----------
    luminosity : Quantity
        Radiated power.
    distance : Quantity
        Distance from the source. Must be positive and finite.

    Returns
    -------
    Quantity
        Flux — power per unit length of the receiving boundary, not per area.

    Raises
    ------
    DimensionError
        If either argument has the wrong dimensions.
    ValueError
        If the distance is non-positive or non-finite.

    Examples
    --------
    >>> from sim.units import FLUX, LENGTH, LUMINOSITY, Quantity
    >>> f = flux_at(Quantity(4.0, LUMINOSITY), Quantity(2.0, LENGTH))
    >>> round(f.magnitude(FLUX), 6)
    0.31831
    """
    power = luminosity.scalar(LUMINOSITY)
    radius = distance.scalar(LENGTH)
    if not math.isfinite(radius):
        raise ValueError(f"distance must be finite, got {radius!r}")
    if radius <= 0.0:
        raise ValueError(f"distance must be positive, got {radius!r}")
    return Quantity(power / (2.0 * math.pi * radius), FLUX)


def insolation_series(star: Kell, trajectory: Trajectory) -> Quantity:
    """Return the flux at Vellum over the course of a trajectory.

    Parameters
    ----------
    star : Kell
        The star. Its luminosity is a swept parameter, not a derived value.
    trajectory : Trajectory
        The sampled orbit.

    Returns
    -------
    Quantity
        Flux per sample, dimension FLUX.

    Examples
    --------
    >>> # See sim/tests/orbit/test_insolation.py.
    """
    power = star.luminosity.scalar(LUMINOSITY)
    radius = trajectory.radius
    if not np.all(radius > 0.0):
        raise ValueError("trajectory passes through the origin; flux is undefined there")
    return Quantity(power / (2.0 * np.pi * radius), FLUX)
