"""Basins on a closed curve, and where a drop of water goes.

Everything here is one-dimensional, which is not a simplification but the
shape of the world: the surface is a closed curve, so ``h`` is a function of one
periodic coordinate and a basin is a local minimum of it.

Three consequences are theorems rather than choices, and the tests treat them
that way:

- **A catchment is a contiguous arc**, bounded by the maxima either side. In
  three dimensions a drainage basin can be any shape; here it is an interval.
- **A basin has exactly one outlet** — the lower of its two enclosing maxima.
  Not a network and not a choice.
- **Rivers cannot branch.** A tributary would have to arrive from a side that
  does not exist. Discharge accumulates along a channel, but there is only ever
  one channel between two points, so nothing joins anything.

**Counting basins requires a depth threshold.** Terrain is fractal, so local
minima multiply without limit as the sampling is refined -- 207 at a thousand
samples and 52,101 at a quarter of a million, on the same terrain. The
scale-free measure is **persistence**: how deep a basin is below the point where
it merges into a deeper one, which is a property of the shape rather than of the
grid. A count without a threshold is not an answer.

Axioms used: T0.1 (a closed surface curve), T1.1 (gravity gives downhill).
Abstracts: terrain statistics, since the ground's shape is chosen -- so every
count here rests on a chosen roughness. See docs/AXIOMS.md section 4.

Depends on: sim.errors, numpy
Used by: sim.water.filling, sim.view.render
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError

__all__ = ["Basin", "BasinSet", "analyse"]


@dataclass(frozen=True)
class Basin:
    """One local minimum of the ground, and the arc that drains into it.

    Attributes
    ----------
    floor_index : int
        Sample index of the lowest point.
    floor : float
        Height there.
    start, stop : int
        The catchment arc, as sample indices. ``stop`` is exclusive and the arc
        may wrap past the end of the array -- it is a closed curve.
    lip : float
        The lower of the two enclosing maxima: the height at which this basin
        first spills. Its single outlet.
    persistence : float
        Depth below the saddle at which this basin merges into a deeper one.
        Not the same as ``lip - floor``: a deep basin beside a shallow one
        survives past the shallow one's lip. This is the scale-free measure of
        how much of a basin it is.
    """

    floor_index: int
    floor: float
    start: int
    stop: int
    lip: float
    persistence: float

    @property
    def depth_to_lip(self) -> float:
        """How deep the basin is before it spills over its own edge."""
        return self.lip - self.floor


@dataclass(frozen=True)
class BasinSet:
    """Every basin on the surface, with the catchment map.

    Attributes
    ----------
    basins : tuple[Basin, ...]
        In order of position around the world.
    catchment : NDArray[np.int64]
        For each sample, the index of the basin it drains to. Every sample
        drains somewhere; there is nowhere else to go.
    """

    basins: tuple[Basin, ...]
    catchment: NDArray[np.int64]

    def __len__(self) -> int:
        return len(self.basins)

    def deeper_than(self, persistence: float) -> tuple[Basin, ...]:
        """Return the basins deeper than a threshold.

        The threshold is required. Terrain is fractal, so "how many basins are
        there" has no answer without one -- see the module docstring.
        """
        if persistence <= 0.0:
            raise ValueError(
                f"persistence threshold must be positive, got {persistence!r}. "
                "Every local minimum is a basin at some scale, so an unqualified "
                "count is a property of the sampling rather than of the world."
            )
        return tuple(b for b in self.basins if b.persistence > persistence)


def analyse(heights: NDArray[np.float64]) -> BasinSet:
    """Find every basin on a closed surface profile.

    Parameters
    ----------
    heights : NDArray[np.float64]
        Ground height, sampled evenly around the closed curve. Periodic: the
        last sample neighbours the first.

    Returns
    -------
    BasinSet

    Raises
    ------
    ValueError
        If there are fewer than three samples, or any height is non-finite.
    """
    h = np.asarray(heights, dtype=np.float64)
    if h.size < 3:
        raise ValueError(f"need at least three samples, got {h.size}")
    if not np.all(np.isfinite(h)):
        raise ValueError("heights must be finite")

    minima, maxima = _extrema(h)
    if minima.size == 0 or maxima.size == 0:
        raise ValueError(
            "the profile has no interior extrema; a closed curve with water "
            "needs at least one basin and one divide"
        )

    persistence = _persistence(h, minima)
    basins: list[Basin] = []
    # Filled with -1 rather than np.empty: an uncovered sample must be a
    # visible failure, not uninitialised memory quietly read as a basin index.
    catchment = np.full(h.size, -1, dtype=np.int64)

    for order, floor_index in enumerate(minima.tolist()):
        before = maxima[maxima < floor_index]
        after = maxima[maxima > floor_index]
        # Wrap: the divide before the first minimum is the last maximum.
        left_divide = int(before[-1]) if before.size else int(maxima[-1])
        right_divide = int(after[0]) if after.size else int(maxima[0])

        start = (left_divide + 1) % h.size
        stop = right_divide + 1 if right_divide >= start else right_divide + 1 + h.size
        indices = np.arange(start, stop) % h.size
        catchment[indices] = order

        basins.append(
            Basin(
                floor_index=floor_index,
                floor=float(h[floor_index]),
                start=start,
                stop=int(stop),
                lip=float(min(h[left_divide], h[right_divide])),
                persistence=float(persistence[order]),
            )
        )
    if np.any(catchment < 0):
        raise InvariantError(
            f"{int((catchment < 0).sum())} samples belong to no basin; the catchments "
            "must tile the world, since water has nowhere else to go"
        )
    return BasinSet(basins=tuple(basins), catchment=catchment)


def _persistence(h: NDArray[np.float64], minima: NDArray[np.int64]) -> NDArray[np.float64]:
    """Return each minimum's depth below the saddle where it merges.

    Flooding upward: sweep samples in height order, joining each to its
    already-flooded neighbours. When two basins meet, the shallower one dies
    there and its persistence is the saddle height less its own floor. The
    deepest basin never dies and takes the full range of the profile.

    Each component tracks the *index* of its lowest sample rather than its
    height, so the dying basin is identified directly. Matching on height would
    pick the wrong basin whenever two floors happen to be equal.
    """
    n = int(h.size)
    parent = list(range(n))
    lowest = list(range(n))  # per root, the sample index of its lowest point

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    span = float(h.max() - h.min())
    result = {int(i): span for i in minima.tolist()}
    flooded = np.zeros(n, dtype=bool)

    for i in np.argsort(h, kind="stable").tolist():
        flooded[i] = True
        for j in ((i - 1) % n, (i + 1) % n):
            if not flooded[j]:
                continue
            a, b = find(i), find(j)
            if a == b:
                continue
            low_a, low_b = lowest[a], lowest[b]
            if h[low_a] < h[low_b]:
                a, b, low_a, low_b = b, a, low_b, low_a  # a is shallower, dies
            if low_a in result:
                result[low_a] = float(h[i] - h[low_a])
            parent[a] = b
            lowest[b] = low_b

    return np.array([result[int(i)] for i in minima.tolist()], dtype=np.float64)


def _extrema(h: NDArray[np.float64]) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """Return the minima and maxima, handling flat ground.

    Comparing each sample against its immediate neighbours breaks whenever two
    adjacent samples are equal: on one real profile a plateau produced five
    maxima and four minima, so they no longer alternated and two samples fell
    into no basin at all. Rounded or quantised ground makes exact ties common.

    Runs of equal height are collapsed to one point first. On the collapsed
    profile every comparison is strict, so minima and maxima must alternate
    around the closed curve and the catchments are guaranteed to tile it.
    """
    n = int(h.size)
    # Start at a point that differs from its predecessor, so runs do not
    # straddle the seam.
    changes = np.flatnonzero(h != np.roll(h, 1))
    if changes.size == 0:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64)
    origin = int(changes[0])
    rolled = np.roll(h, -origin)
    starts = np.flatnonzero(rolled != np.roll(rolled, 1))
    reduced = rolled[starts]

    left = np.roll(reduced, 1)
    right = np.roll(reduced, -1)
    low = np.flatnonzero((reduced < left) & (reduced < right))
    high = np.flatnonzero((reduced > left) & (reduced > right))

    def back(indices: NDArray[np.int64]) -> NDArray[np.int64]:
        return np.sort((starts[indices] + origin) % n).astype(np.int64)

    return back(low), back(high)
