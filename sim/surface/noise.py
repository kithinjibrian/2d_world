"""Periodic gradient noise: the building block of Vellum's ground.

One octave of 1D gradient noise on a lattice of `cells` cells spanning the unit
interval. The cell index is taken **modulo the cell count**, which is what makes
the field exactly periodic -- ``noise(t) == noise(t + 1)`` by construction
rather than by stitching two ends together. On a closed surface that matters:
there is no edge to hide a seam behind.

Gradients come from an integer hash rather than a random number generator, so a
position can be evaluated on its own without generating everything before it.
That is the whole reason terrain is procedural here: a Fourier sum would need
38 million coefficients to reach metre detail on a 38,400 km surface, where this
needs 26 octaves. See DECISION-017.

The hash is explicit integer mixing (a splitmix64 finaliser). Python randomises
``hash()`` for strings and bytes per process, so a terrain built on it would
differ between runs -- a test asserts this module does not call it.

Axioms used: T0.1 (the surface is a closed curve, so height is a function of one
periodic coordinate).
Abstracts: nothing itself; see sim.surface.terrain for what terrain statistics
rest on.

Depends on: numpy
Used by: sim.surface.terrain
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = ["gradient_noise", "mix64"]

_MASK: int = (1 << 64) - 1


def mix64(values: NDArray[np.int64] | NDArray[np.uint64]) -> NDArray[np.uint64]:
    """Return a splitmix64 finaliser applied elementwise.

    A hash whose output varies smoothly with its input produces visible lattice
    structure rather than noise, so this avalanches: one input bit changes about
    half the output bits.

    Parameters
    ----------
    values : NDArray
        Integer lattice indices, already combined with seed and octave.

    Returns
    -------
    NDArray[np.uint64]
        Well-mixed 64-bit values.

    Examples
    --------
    >>> import numpy as np
    >>> bool(mix64(np.array([1])) != mix64(np.array([2])))
    True
    """
    x = values.astype(np.uint64)
    # Bit patterns from splitmix64. The multiplications wrap, which is intended.
    with np.errstate(over="ignore"):
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9 & _MASK)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB & _MASK)
        x = x ^ (x >> np.uint64(31))
    return x


def _gradients(index: NDArray[np.int64], cells: int, seed: int, octave: int) -> NDArray[np.float64]:
    """Return a gradient in [-1, 1] for each lattice index, wrapped periodically."""
    wrapped = np.mod(index, cells).astype(np.int64)
    # Fold seed and octave in so octaves are independent fields rather than
    # rescalings of one another.
    key = wrapped + np.int64(0x9E3779B97F4A7C15 & 0x7FFFFFFF) * np.int64(octave + 1)
    key = key + np.int64(seed) * np.int64(0x2545F4914F6CDD1D & 0x7FFFFFFF)
    mixed = mix64(key)
    # Map the top 53 bits to [-1, 1).
    unit = (mixed >> np.uint64(11)).astype(np.float64) / float(1 << 53)
    return 2.0 * unit - 1.0


def gradient_noise(
    t: NDArray[np.float64], cells: int, seed: int, octave: int
) -> NDArray[np.float64]:
    """Return one octave of periodic gradient noise over the unit interval.

    Parameters
    ----------
    t : NDArray[np.float64]
        Positions, in units of the full period. Values outside [0, 1) wrap.
    cells : int
        Lattice cells across the period. Must be positive. Periodicity is exact
        because the cell index is taken modulo this.
    seed : int
        World seed.
    octave : int
        Which octave this is; folded into the hash so octaves are independent.

    Returns
    -------
    NDArray[np.float64]
        Values in [-1, 1], zero at every lattice point.

    Raises
    ------
    ValueError
        If `cells` is not positive.

    Examples
    --------
    >>> import numpy as np
    >>> v = gradient_noise(np.array([0.0, 0.25]), cells=4, seed=1, octave=0)
    >>> bool(abs(v[0]) < 1e-12)   # zero on the lattice
    True
    """
    if cells <= 0:
        raise ValueError(f"cells must be positive, got {cells!r}")

    scaled = np.asarray(t, dtype=np.float64) * cells
    lower = np.floor(scaled)
    frac = scaled - lower
    index = lower.astype(np.int64)

    g0 = _gradients(index, cells, seed, octave)
    g1 = _gradients(index + 1, cells, seed, octave)

    # Perlin's quintic fade: zero first and second derivatives at the ends, so
    # neighbouring cells join without a visible crease.
    fade = frac * frac * frac * (frac * (frac * 6.0 - 15.0) + 10.0)
    return (1.0 - fade) * (g0 * frac) + fade * (g1 * (frac - 1.0))
