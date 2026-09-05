"""Wrapping on a closed curve.

Vellum's surface has no edge, so every position on it is periodic. This is the
one place that fact is implemented, because the subtlety in it has now bitten
twice in two different modules.

Two traps, both found the hard way:

1. ``fmod(fmod(a, b) + b, b)`` -- the usual trick for giving a negative input a
   positive result -- quantises small values at ``b``'s ulp. On a surface
   3.84e7 units around that ulp is 7.45 nanometres, and a micron of position
   lost 0.16 percent of itself. Invisible in a unit test of the wrap, plainly
   wrong as a pixel offset at ground zoom.

2. Python's ``%`` avoids that but returns exactly ``b`` for a tiny negative
   input, because ``b - a`` rounds up to ``b``. That puts a position outside
   ``[0, b)`` and breaks index arithmetic downstream -- and it also makes a
   point one full rotation later compare unequal to itself.

Axioms used: T0.1 (the surface is a closed curve).
Abstracts: nothing.

Depends on: numpy
Used by: sim.view.geometry, sim.rotation.spin
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = ["distance", "separation", "wrap"]

Value = float | NDArray[np.float64]


def wrap(value: Value, period: float) -> Value:
    """Wrap into ``[0, period)``, preserving float-or-array typing.

    Parameters
    ----------
    value : float | NDArray[np.float64]
        Position on the closed curve. Any real value is valid.
    period : float
        The curve's length.

    Returns
    -------
    float | NDArray[np.float64]
        The equivalent position in ``[0, period)``. Never equal to `period`
        itself: a value half an ulp below the wrap point *is* the wrap point,
        which is zero.

    Examples
    --------
    >>> wrap(-1e-9, 3.84e7)
    0.0
    >>> wrap(1e-6, 3.84e7)
    1e-06
    """
    if isinstance(value, np.ndarray):
        wrapped = np.mod(value, period)
        return np.where(wrapped >= period, 0.0, wrapped)
    scalar = value % period
    return 0.0 if scalar >= period else scalar


def separation(a: Value, b: Value, period: float) -> Value:
    """Return the signed offset from `a` to `b`, taking the shorter way round.

    On a closed curve there are always two routes between two points, and the
    difference ``b - a`` is not one of them once either has wrapped. The result
    lies in ``(-period/2, period/2]``.

    This is also how positions on the surface must be *compared*: ``0`` and
    ``period - 1e-16`` are the same place, and subtracting them says otherwise.

    Parameters
    ----------
    a, b : float | NDArray[np.float64]
        Positions on the closed curve.
    period : float
        The curve's length.

    Returns
    -------
    float | NDArray[np.float64]
        Signed offset, positive when `b` lies ahead of `a`.

    Examples
    --------
    >>> separation(0.0, 9.0, 10.0)
    -1.0
    """
    offset = wrap(np.asarray(b) - np.asarray(a) + 0.5 * period, period)
    result = np.asarray(offset) - 0.5 * period
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.asarray(result, dtype=np.float64)
    return float(result)


def distance(a: Value, b: Value, period: float) -> Value:
    """Return how far apart two points are, the shorter way round.

    Never more than half the period: on a closed curve nothing is further away
    than the antipode.

    Examples
    --------
    >>> distance(0.0, 9.0, 10.0)
    1.0
    """
    result = np.abs(np.asarray(separation(a, b, period)))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.asarray(result, dtype=np.float64)
    return float(result)
