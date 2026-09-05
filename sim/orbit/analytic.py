"""Closed forms for the two-body orbit — the screening path.

Architecture rule 8 requires every layer to run at two fidelities: a cheap path
over the whole parameter grid, and a full solve for a chosen point. Here the
cheap path is nearly free, because the logarithmic potential gives closed forms
for everything that matters in the near-circular limit.

It also cross-checks the integrator independently. A disagreement between these
values and an integration in the near-circular limit is a bug in one of them.

This module must never integrate anything; a test asserts it does not import
the integrator.

Axioms used: T1.1 (gravity as a direct force, F = G2*M*m/r).
Abstracts: nothing.

Depends on: sim.units
Used by: sim.orbit, and any scan over orbital parameters
"""

from __future__ import annotations

import math

from sim.units import (
    G2,
    GRAVITATIONAL_CONSTANT,
    LENGTH,
    MASS,
    TIME,
    VELOCITY,
    Dimension,
    Quantity,
)

__all__ = [
    "APSIDAL_ANGLE_NEAR_CIRCULAR",
    "APSIDAL_REGRESSION_PER_ORBIT",
    "SEASON_CYCLE_ORBITS",
    "circular_period",
    "circular_speed",
    "radial_turning_radius",
    "turning_radius",
]

# DERIVED (T1.1): for a force F ~ r^n the apsidal angle of a near-circular
# orbit is pi/sqrt(3+n). With n = -1 that is pi/sqrt(2) — equivalently, the
# radial and angular frequencies stand in the ratio sqrt(2).
APSIDAL_ANGLE_NEAR_CIRCULAR: float = math.pi / math.sqrt(2.0)

# DERIVED: pericentre to pericentre sweeps twice the apsidal angle, so the
# apsis line falls short of a full turn by this much every orbit.
APSIDAL_REGRESSION_PER_ORBIT: float = 2.0 * math.pi - 2.0 * APSIDAL_ANGLE_NEAR_CIRCULAR

# DERIVED: 2*pi / regression = 2 + sqrt(2), exactly. A season therefore works
# its way round the calendar in about 3.414 orbits — not the ~900 years the
# monograph guesses, which is wrong by a factor of ~300.
SEASON_CYCLE_ORBITS: float = 2.0 * math.pi / APSIDAL_REGRESSION_PER_ORBIT


def circular_speed(mass: Quantity, radius: Quantity) -> Quantity:
    """Return the speed of a circular orbit — the same at every radius.

    In a logarithmic potential, ``r * dPhi/dr = G2*M`` with no ``r`` left in it,
    so ``v_c = sqrt(G2*M)`` regardless of distance. Every circular orbit around
    Kell, however far out, moves at the same speed. This is the
    two-dimensional analogue of a flat galactic rotation curve.

    The `radius` argument is accepted and validated but does not affect the
    result. That is the point, and dropping the parameter would hide it.

    Parameters
    ----------
    mass : Quantity
        Central mass, natural units.
    radius : Quantity
        Orbital radius. Validated, deliberately unused.

    Returns
    -------
    Quantity
        Circular speed.

    Raises
    ------
    ValueError
        If mass or radius is non-positive or non-finite.

    Examples
    --------
    >>> from sim.units import LENGTH, MASS, VELOCITY, Quantity
    >>> circular_speed(Quantity(4.0, MASS), Quantity(9.0, LENGTH)).magnitude(VELOCITY)
    2.0
    """
    m = _positive_scalar(mass, MASS, "mass")
    _positive_scalar(radius, LENGTH, "radius")
    g2 = _g2()
    return Quantity(math.sqrt(g2 * m), VELOCITY)


def circular_period(mass: Quantity, radius: Quantity) -> Quantity:
    """Return the period of a circular orbit: ``2*pi*r / sqrt(G2*M)``.

    Because the speed does not depend on radius, the period is **linear** in
    radius. Kepler's third law, ``T ~ r^(3/2)``, does not hold here.

    Parameters
    ----------
    mass : Quantity
        Central mass, natural units.
    radius : Quantity
        Orbital radius, natural units.

    Returns
    -------
    Quantity
        Orbital period.

    Examples
    --------
    >>> from sim.units import LENGTH, MASS, TIME, Quantity
    >>> t = circular_period(Quantity(1.0, MASS), Quantity(1.0, LENGTH))
    >>> round(t.magnitude(TIME), 6)
    6.283185
    """
    r = _positive_scalar(radius, LENGTH, "radius")
    speed = circular_speed(mass, radius).scalar(VELOCITY)
    return Quantity(2.0 * math.pi * r / speed, TIME)


def radial_turning_radius(mass: Quantity, radius: Quantity, speed: Quantity) -> Quantity:
    """Return where a purely radial launch turns around: ``r0 * exp(v^2 / (2*G2*M))``.

    This is the closed form of "there is no escape velocity". The logarithmic
    potential is unbounded above, so **every** finite launch speed has a finite
    turning radius — however large. The cost of getting far away is exponential
    in ``v^2``, which is why nothing ever leaves and why the sky keeps falling
    back.

    Parameters
    ----------
    mass : Quantity
        Central mass, natural units.
    radius : Quantity
        Launch radius, natural units.
    speed : Quantity
        Launch speed, purely radial.

    Returns
    -------
    Quantity
        The radius at which radial motion reverses. Mathematically finite for
        every input.

    Raises
    ------
    ValueError
        If the turning radius overflows double precision, which happens above
        roughly 37.7 times the circular speed. The trajectory is still bound;
        the number simply cannot be represented.

    Examples
    --------
    >>> from sim.units import LENGTH, MASS, VELOCITY, Quantity
    >>> r = radial_turning_radius(
    ...     Quantity(1.0, MASS), Quantity(1.0, LENGTH), Quantity(2.0, VELOCITY)
    ... )
    >>> round(r.magnitude(LENGTH), 4)
    7.3891
    """
    m = _positive_scalar(mass, MASS, "mass")
    r0 = _positive_scalar(radius, LENGTH, "radius")
    v = speed.scalar(VELOCITY)
    if not math.isfinite(v):
        raise ValueError(f"speed must be finite, got {v!r}")
    exponent = v * v / (2.0 * _g2() * m)
    try:
        return Quantity(r0 * math.exp(exponent), LENGTH)
    except OverflowError as overflow:
        # Mathematically the turning radius is still finite -- nothing escapes,
        # ever. It simply exceeds what a float can represent, which happens at
        # only about 37.7 times the circular speed, since exp() overflows past
        # an argument of ~709. Worth knowing: the distance a fast object gets
        # to before turning back becomes unrepresentable astonishingly quickly.
        raise ValueError(
            f"turning radius exceeds double precision (exponent {exponent:.4g}). "
            "The trajectory is still bound -- a logarithmic potential admits no "
            "escape velocity at any speed -- but its turning radius cannot be "
            "represented as a float."
        ) from overflow


def turning_radius(
    mass: Quantity,
    radius: Quantity,
    radial_speed: Quantity,
    tangential_speed: Quantity,
) -> Quantity:
    """Return the outer turning radius for a general launch.

    Solves ``E = L^2/(2r^2) + G2*M*ln(r)`` for the outer root by bisection.
    Closed form when the tangential speed is zero — see
    :func:`radial_turning_radius`.

    Bisection rather than a solver from scipy: the dependency list is closed
    (see STACK in CLAUDE.md), and the function is monotone in the bracket, so
    fifteen lines suffice.

    Parameters
    ----------
    mass : Quantity
        Central mass, natural units.
    radius : Quantity
        Launch radius, natural units.
    radial_speed, tangential_speed : Quantity
        Velocity components at launch.

    Returns
    -------
    Quantity
        Outer turning radius. Always finite — nothing escapes.
    """
    m = _positive_scalar(mass, MASS, "mass")
    r0 = _positive_scalar(radius, LENGTH, "radius")
    v_r = radial_speed.scalar(VELOCITY)
    v_t = tangential_speed.scalar(VELOCITY)

    gm = _g2() * m
    if v_t == 0.0:
        return radial_turning_radius(mass, radius, radial_speed)

    angular = r0 * v_t
    energy = 0.5 * (v_r * v_r + v_t * v_t) + gm * math.log(r0)

    def excess(r: float) -> float:
        """Energy available for radial motion. Zero at a turning point."""
        return energy - (angular * angular / (2.0 * r * r) + gm * math.log(r))

    # Bracket: walk outward until the radial energy goes negative. The log term
    # grows without bound, so this always terminates.
    low, high = r0, max(r0 * 2.0, r0 + 1.0)
    while excess(high) > 0.0:
        high *= 2.0
        if high > 1e300:  # pragma: no cover - unreachable for finite energies
            raise ValueError("turning radius overflowed; launch speed is absurd")
    for _ in range(200):
        mid = 0.5 * (low + high)
        if excess(mid) > 0.0:
            low = mid
        else:
            high = mid
    return Quantity(0.5 * (low + high), LENGTH)


def _g2() -> float:
    return G2.scalar(GRAVITATIONAL_CONSTANT)


def _positive_scalar(quantity: Quantity, dimension: Dimension, name: str) -> float:
    value = quantity.scalar(dimension)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    if value <= 0.0:
        raise ValueError(f"{name} must be positive, got {value!r}")
    return value
