"""Geometry the viewer needs: a planet disc, and culling on a closed surface.

**Imports no pygame** -- see sim.view.camera.

Axioms used: T0.1 (two dimensions). No physics is computed here.
Abstracts: nothing.

Depends on: numpy
Used by: sim.view.camera, sim.view.render
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import pairwise
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

from sim.periodic import wrap

__all__ = [
    "Coordinate",
    "Disc",
    "add",
    "contiguous_runs",
    "mod",
    "mul",
    "sub",
    "visible_surface_indices",
]

#: A scalar or an array of them. Never carries units.
Coordinate: TypeAlias = float | NDArray[np.float64]


@dataclass(frozen=True)
class Disc:
    """A planet, as the viewer needs it: a centre and a closed surface.

    The circumference is stored and the radius derived. They are not
    independent for a circle, and storing both invites exactly the
    inconsistency it caused when this class first had both fields -- a surface
    coordinate then maps to an arc 2 percent short of itself, which is the kind
    of error that looks like rounding until someone measures it.

    Attributes
    ----------
    centre_x, centre_y : float
        World position of the centre.
    circumference : float
        Length of the closed surface curve. Surface coordinates are periodic
        with this length: walk far enough and you arrive behind yourself.
    """

    centre_x: float
    centre_y: float
    circumference: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.circumference) or self.circumference <= 0.0:
            raise ValueError(
                f"circumference must be positive and finite, got {self.circumference!r}"
            )
        if not (math.isfinite(self.centre_x) and math.isfinite(self.centre_y)):
            raise ValueError("centre must be finite")

    @property
    def radius(self) -> float:
        """Surface radius, derived from the circumference."""
        return self.circumference / (2.0 * math.pi)


def visible_surface_indices(
    positions: NDArray[np.float64],
    start: float,
    end: float,
    circumference: float,
) -> NDArray[np.int64]:
    """Return indices of surface positions inside an arc, handling the seam.

    Two binary searches rather than a scan. Bodies on the ground are held sorted
    by surface position, and the first law guarantees that order never changes
    -- nothing passes anything -- so the array index *is* the spatial index and
    it never needs rebuilding. See MEMORY.md decision 8.

    Parameters
    ----------
    positions : NDArray[np.float64]
        Surface positions, **sorted ascending**.
    start, end : float
        Arc bounds. ``end`` may exceed the circumference; the arc wraps.
    circumference : float
        Length of the closed surface.

    Returns
    -------
    NDArray[np.int64]
        Indices inside the arc, in ascending index order.

    Raises
    ------
    ValueError
        If `positions` is not sorted, or the circumference is non-positive.
    """
    if circumference <= 0.0:
        raise ValueError(f"circumference must be positive, got {circumference!r}")
    if positions.size > 1 and not np.all(np.diff(positions) >= 0.0):
        raise ValueError("positions must be sorted ascending")

    width = end - start
    if width >= circumference:
        return np.arange(positions.size, dtype=np.int64)

    low = start % circumference
    high = low + width
    if high <= circumference:
        first = int(np.searchsorted(positions, low, side="left"))
        last = int(np.searchsorted(positions, high, side="right"))
        return np.arange(first, last, dtype=np.int64)

    # The arc straddles the seam: one run to the end, one from the start.
    tail = int(np.searchsorted(positions, low, side="left"))
    head = int(np.searchsorted(positions, high - circumference, side="right"))
    return np.concatenate(
        (np.arange(0, head, dtype=np.int64), np.arange(tail, positions.size, dtype=np.int64))
    )


def sub(a: Coordinate, b: float) -> Coordinate:
    """Subtract a scalar, preserving float-or-array typing."""
    return a - b


def add(a: Coordinate, b: Coordinate) -> Coordinate:
    """Add, preserving float-or-array typing."""
    return a + b


def mul(a: Coordinate, b: Coordinate) -> Coordinate:
    """Multiply, preserving float-or-array typing."""
    return a * b


def mod(a: Coordinate, b: float) -> Coordinate:
    """Wrap into [0, b), preserving float-or-array typing.

    Delegates to :func:`sim.periodic.wrap`, which is the single home for this
    after the same subtlety bit twice in two modules.
    """
    return wrap(a, b)


def contiguous_runs(mask: NDArray[np.bool_]) -> list[tuple[int, int, bool]]:
    """Split a boolean mask into maximal runs of equal value.

    Returns ``(start, stop, value)`` with `stop` exclusive, tiling the mask with
    no gap and no overlap, and with neighbouring runs always differing.

    Exists because doing this inline shipped a crash: when the last sample
    flipped, the trailing run held a single element, and drawing a polyline
    through one point raises. Inline index juggling could only be exercised by
    rendering, and rendering never happened to put a terminator on the final
    sample.

    Parameters
    ----------
    mask : NDArray[np.bool_]
        Values to segment.

    Returns
    -------
    list[tuple[int, int, bool]]
        One entry per run. Empty for an empty mask.

    Examples
    --------
    >>> import numpy as np
    >>> contiguous_runs(np.array([True, True, False]))
    [(0, 2, True), (2, 3, False)]
    """
    if mask.size == 0:
        return []
    changes = np.flatnonzero(np.diff(mask.astype(np.int8))) + 1
    bounds = [0, *changes.tolist(), int(mask.size)]
    return [(start, stop, bool(mask[start])) for start, stop in pairwise(bounds)]
