"""Measuring an orbit: conserved quantities and the apsidal angle.

**A naming warning, learned the hard way.** The *apsidal angle* is the sweep
from pericentre to apocentre — pi/sqrt(2) here. The *pericentre-to-pericentre*
sweep is twice that. A drafting script conflated them and produced a nonsensical
regression of -149 degrees per orbit from a perfectly good measurement. Both
functions below are named for exactly what they return.

Pericentres are located by parabolic refinement rather than by taking the
nearest sample, so the measurement is not limited by the timestep's resolution
of the minimum.

Axioms used: T1.1.
Abstracts: nothing.

Depends on: sim.errors, sim.orbit.integrator, sim.units
Used by: sim.orbit
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError
from sim.orbit.integrator import Trajectory
from sim.units import G2, GRAVITATIONAL_CONSTANT, MASS, Quantity

__all__ = [
    "apsidal_angle",
    "pericentre_indices",
    "pericentre_to_pericentre_angle",
    "specific_angular_momentum",
    "specific_energy",
]


def specific_energy(trajectory: Trajectory, mass: Quantity) -> NDArray[np.float64]:
    """Return specific orbital energy at each sample: ``v^2/2 + G2*M*ln(r)``.

    The potential is logarithmic, so energy is defined only up to an additive
    constant. That is harmless — only differences matter, and the unbounded
    growth of ``ln r`` is precisely why nothing escapes.

    Parameters
    ----------
    trajectory : Trajectory
        The sampled orbit.
    mass : Quantity
        Central mass, natural units.

    Returns
    -------
    NDArray[np.float64]
        Specific energy per sample, natural units.
    """
    gm = _gm(mass)
    speed = trajectory.speed
    return 0.5 * speed * speed + gm * np.log(trajectory.radius)


def specific_angular_momentum(trajectory: Trajectory) -> NDArray[np.float64]:
    """Return specific angular momentum at each sample.

    In two dimensions this is a signed **scalar**, not a vector: there is no
    third axis for it to point along. The same reason the magnetic field would
    be a scalar here, were electromagnetism modelled.

    Returns
    -------
    NDArray[np.float64]
        ``x*vy - y*vx`` per sample.
    """
    x = trajectory.positions[:, 0]
    y = trajectory.positions[:, 1]
    vx = trajectory.velocities[:, 0]
    vy = trajectory.velocities[:, 1]
    return x * vy - y * vx


def pericentre_indices(trajectory: Trajectory) -> NDArray[np.int64]:
    """Return the sample indices at which the radius is a local minimum."""
    radius = trajectory.radius
    interior = np.arange(1, len(radius) - 1)
    is_minimum = (radius[interior] < radius[interior - 1]) & (
        radius[interior] < radius[interior + 1]
    )
    return interior[is_minimum].astype(np.int64)


def pericentre_to_pericentre_angle(trajectory: Trajectory) -> float:
    """Return the angle swept between successive pericentres, in radians.

    This is **twice** the apsidal angle. For a near-circular orbit under
    ``F ~ 1/r`` it is ``2*pi/sqrt(2)`` — about 254.56 degrees — so the apsis
    line falls about 105.44 degrees short of a full turn every orbit and no
    orbit ever closes.

    Pericentre times are refined by fitting a parabola through the three
    samples bracketing each minimum, so the result is not limited by how
    finely the timestep happens to sample the turning point.

    Returns
    -------
    float
        Mean sweep between consecutive pericentres, radians.

    Raises
    ------
    InvariantError
        If fewer than two pericentres were found. Too short an integration is a
        caller error, not a degenerate result to paper over.

    Examples
    --------
    >>> # See sim/tests/orbit/test_precession.py for a worked measurement.
    """
    indices = pericentre_indices(trajectory)
    if len(indices) < 2:
        raise InvariantError(
            f"found {len(indices)} pericentres; at least two are needed to measure a "
            "sweep. Integrate for longer."
        )

    radius = trajectory.radius
    angle = np.unwrap(
        np.arctan2(trajectory.positions[:, 1], trajectory.positions[:, 0])
    )

    refined: list[float] = []
    for index in indices:
        left, middle, right = radius[index - 1], radius[index], radius[index + 1]
        # Vertex of the parabola through three equally spaced samples, as an
        # offset in samples from the middle one. Denominator vanishes only if
        # the three are collinear, which a strict local minimum rules out.
        denominator = left - 2.0 * middle + right
        offset = 0.0 if denominator == 0.0 else 0.5 * (left - right) / denominator
        # Linear interpolation of the angle at that fractional sample.
        neighbour = angle[index + 1] if offset >= 0.0 else angle[index - 1]
        refined.append(float(angle[index] + abs(offset) * (neighbour - angle[index])))

    return float(np.mean(np.diff(refined)))


def apsidal_angle(trajectory: Trajectory) -> float:
    """Return the apsidal angle — pericentre to **apocentre** — in radians.

    Half the pericentre-to-pericentre sweep. For a near-circular orbit this is
    ``pi/sqrt(2)``, about 127.28 degrees.

    Returns
    -------
    float
        Apsidal angle, radians.
    """
    return pericentre_to_pericentre_angle(trajectory) / 2.0


def _gm(mass: Quantity) -> float:
    m = mass.scalar(MASS)
    g2 = G2.scalar(GRAVITATIONAL_CONSTANT)
    if not math.isfinite(m) or m <= 0.0:
        raise ValueError(f"mass must be positive and finite, got {m!r}")
    return g2 * m
