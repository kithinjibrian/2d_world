"""Filling Vellum's basins, and letting the overflow find its way.

Water is **an area**, not a volume: the world is two-dimensional, so a body of
water is a region of the plane and ``INT (level - h) ds`` carries ``L**2``. A
quantity named "volume" in this module would be a mistake.

The model, stated plainly because it is a choice: water arrives in proportion to
each catchment's length, each basin fills to the level its share supports, and
any excess passes through the basin's single outlet into the neighbour beyond
it. Two basins share a level only once both are filled to the saddle between
them -- until then they are separate lakes at different heights, which is what
"a basin that never fills to its lip has no outlet" means in practice.

**There is no global sea level.** Disconnected basins hold different levels, and
a basin whose water never reaches its lip is sealed permanently: no flood route,
no drainage web, no chance passage from one to another.

Lakes are always contiguous arcs of basins, which is another consequence of one
dimension -- water cannot merge two basins without submerging everything
between them.

Axioms used: T0.1, T1.1.
Abstracts: terrain statistics -- every wet fraction reported here rests on a
chosen roughness. See docs/AXIOMS.md section 4.

Depends on: sim.errors, sim.water.basins
Used by: sim.view.render
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError
from sim.water.basins import BasinSet

__all__ = ["Lake", "WaterState", "fill"]

#: The cascade settles in far fewer rounds than there are basins; this only
#: exists so a bug cannot spin forever.
_MAX_ROUNDS = 10_000


@dataclass(frozen=True)
class Lake:
    """A connected body of standing water.

    Attributes
    ----------
    level : float
        Height of the water surface. One level per lake -- that is what makes
        it one lake.
    area : float
        How much water it holds. An **area**, not a volume.
    basins : tuple[int, ...]
        Which basins it covers, as indices into the BasinSet.
    spilling : bool
        Whether it is full to its lip and overflowing. A lake that is not
        spilling has no outlet at all: what is in it is sealed.
    """

    level: float
    area: float
    basins: tuple[int, ...]
    spilling: bool

    @property
    def sealed(self) -> bool:
        """True when this water has nowhere to go, and nothing can leave it."""
        return not self.spilling


@dataclass(frozen=True)
class WaterState:
    """Where the water ended up.

    Attributes
    ----------
    depth : NDArray[np.float64]
        Water depth at each sample. Zero on dry ground, never negative.
    lakes : tuple[Lake, ...]
        Every standing body, in order around the world.
    """

    depth: NDArray[np.float64]
    lakes: tuple[Lake, ...]

    @property
    def wet_fraction(self) -> float:
        """The fraction of the surface under water."""
        return float((self.depth > 0.0).mean())

    @property
    def total_area(self) -> float:
        """Total water held. Conserved; compare against what was supplied."""
        return float(sum(lake.area for lake in self.lakes))

    def sealed_lakes(self) -> tuple[Lake, ...]:
        """Lakes with no outlet. What is in one is sealed permanently."""
        return tuple(lake for lake in self.lakes if lake.sealed)


def fill(
    heights: NDArray[np.float64],
    basins: BasinSet,
    water_area: float,
    spacing: float,
) -> WaterState:
    """Distribute water over the surface and let it settle.

    Parameters
    ----------
    heights : NDArray[np.float64]
        Ground profile, sampled evenly around the closed curve.
    basins : BasinSet
        From :func:`sim.water.basins.analyse` on the same profile.
    water_area : float
        Total water, as an **area**. Zero is legal and means a dry world.
    spacing : float
        Distance between samples along the surface.

    Returns
    -------
    WaterState

    Raises
    ------
    ValueError
        On a negative or non-finite water area, or a non-positive spacing.
    InvariantError
        If water area is not conserved, or the cascade fails to settle.
    """
    h = np.asarray(heights, dtype=np.float64)
    if not math.isfinite(water_area) or water_area < 0.0:
        raise ValueError(f"water area must be finite and non-negative, got {water_area!r}")
    if not math.isfinite(spacing) or spacing <= 0.0:
        raise ValueError(f"spacing must be positive, got {spacing!r}")

    count = len(basins)
    # Water arrives in proportion to catchment length: a longer arc gathers
    # more. Nothing is placed by hand.
    lengths = np.bincount(basins.catchment, minlength=count).astype(np.float64)
    supply = water_area * lengths / lengths.sum() if water_area > 0.0 else np.zeros(count)

    members: list[list[int]] = [[i] for i in range(count)]
    samples: list[NDArray[np.float64]] = [
        np.sort(h[_arc(basins.basins[i].start, basins.basins[i].stop, h.size)])
        for i in range(count)
    ]
    held = list(supply)
    alive = list(range(count))
    # The divide heights either side of each lake, in order around the world.
    left_lip = [basins.basins[i].lip for i in range(count)]
    right_lip = list(left_lip)
    for i in range(count):
        nxt = (i + 1) % count
        shared = float(h[(basins.basins[i].stop - 1) % h.size])
        right_lip[i] = shared
        left_lip[nxt] = shared

    for _ in range(_MAX_ROUNDS):
        # Transfers first, to convergence. A merge is irreversible, so it must
        # never be decided on a transient state: mid-cascade a lake can be
        # holding water that is on its way somewhere else, and merging on that
        # basis joins two bodies that never actually meet. That produced lakes
        # whose level *fell* as water was added, which is impossible.
        if _transfer(alive, samples, held, left_lip, right_lip, spacing):
            continue
        if _merge_once(
            alive, members, samples, held, left_lip, right_lip, spacing
        ):
            continue
        break
    else:  # pragma: no cover - a bug, not a result
        raise InvariantError("water did not settle; the cascade is not converging")

    lakes: list[Lake] = []
    depth = np.zeros(h.size, dtype=np.float64)
    for root in alive:
        if held[root] <= 0.0:
            continue
        level = _level(samples[root], held[root], spacing)
        lip = min(left_lip[root], right_lip[root])
        wet = np.concatenate(
            [_arc(basins.basins[b].start, basins.basins[b].stop, h.size) for b in members[root]]
        )
        depth[wet] = np.maximum(level - h[wet], 0.0)
        lakes.append(
            Lake(
                level=level,
                area=float(held[root]),
                basins=tuple(sorted(members[root])),
                spilling=level >= lip - 1e-12,
            )
        )

    settled = float(depth.sum() * spacing)
    if water_area > 0.0 and abs(settled - water_area) > 1e-6 * water_area:
        raise InvariantError(
            f"water area not conserved: supplied {water_area!r}, holding {settled!r}"
        )
    return WaterState(depth=depth, lakes=tuple(lakes))


def _transfer(
    alive: list[int],
    samples: list[NDArray[np.float64]],
    held: list[float],
    left_lip: list[float],
    right_lip: list[float],
    spacing: float,
) -> bool:
    """Move overflow across lips, without merging anything.

    Runs to convergence before any merge is considered. A lake whose neighbour
    is already full to the shared saddle is left alone here -- that is a merge,
    and merges are decided only once nothing is still in transit.
    """
    moved = False
    for position, root in enumerate(alive):
        if held[root] <= 0.0:
            continue
        level = _level(samples[root], held[root], spacing)
        for side in (0, 1):
            lip = left_lip[root] if side == 0 else right_lip[root]
            if level <= lip + 1e-15:
                continue
            neighbour = (
                alive[(position - 1) % len(alive)]
                if side == 0
                else alive[(position + 1) % len(alive)]
            )
            if neighbour == root:
                continue  # one lake around the whole world; nowhere to spill
            if _level(samples[neighbour], held[neighbour], spacing) >= lip - 1e-15:
                continue  # both full: a merge, handled once transfers settle
            capacity = _capacity(samples[root], lip, spacing)
            excess = held[root] - capacity
            if excess <= 1e-18:
                continue
            held[root] = capacity
            held[neighbour] += excess
            level = _level(samples[root], held[root], spacing)
            moved = True
    return moved


def _merge_once(
    alive: list[int],
    members: list[list[int]],
    samples: list[NDArray[np.float64]],
    held: list[float],
    left_lip: list[float],
    right_lip: list[float],
    spacing: float,
) -> bool:
    """Join one pair of lakes that have genuinely met over their saddle."""
    for position, root in enumerate(alive):
        if held[root] <= 0.0:
            continue
        level = _level(samples[root], held[root], spacing)
        for side in (0, 1):
            lip = left_lip[root] if side == 0 else right_lip[root]
            if level <= lip + 1e-15:
                continue
            neighbour = (
                alive[(position - 1) % len(alive)]
                if side == 0
                else alive[(position + 1) % len(alive)]
            )
            if neighbour == root:
                continue
            if _level(samples[neighbour], held[neighbour], spacing) < lip - 1e-15:
                continue
            # Both reach the saddle -- but would the joined body *stay* above
            # it? If the two together settle lower than the saddle, they part
            # again as soon as they meet: the donor drains to its brim and the
            # rest runs on. Merging anyway is irreversible and drops the donor
            # below its own lip, which showed up as a lake whose level fell
            # while water was being added.
            combined = np.sort(np.concatenate([samples[root], samples[neighbour]]))
            if _level(combined, held[root] + held[neighbour], spacing) < lip - 1e-15:
                capacity = _capacity(samples[root], lip, spacing)
                excess = held[root] - capacity
                if excess <= 1e-18:
                    continue
                held[root] = capacity
                held[neighbour] += excess
                return True
            _merge(
                alive, members, samples, held, left_lip, right_lip,
                root, neighbour, side,
            )
            return True
    return False


def _merge(
    alive: list[int],
    members: list[list[int]],
    samples: list[NDArray[np.float64]],
    held: list[float],
    left_lip: list[float],
    right_lip: list[float],
    root: int,
    neighbour: int,
    side: int,
) -> None:
    """Join two lakes that have met over the saddle between them."""
    keep, gone = (neighbour, root) if side == 0 else (root, neighbour)
    members[keep] = members[keep] + members[gone]
    samples[keep] = np.sort(np.concatenate([samples[keep], samples[gone]]))
    held[keep] = held[keep] + held[gone]
    held[gone] = 0.0
    right_lip[keep] = right_lip[gone] if side == 0 else right_lip[neighbour]
    if side == 0:
        right_lip[keep] = right_lip[root]
    else:
        left_lip[keep] = left_lip[root]
        right_lip[keep] = right_lip[neighbour]
    alive.remove(gone)


def _level(sorted_heights: NDArray[np.float64], area: float, spacing: float) -> float:
    """Return the water surface height for a given area over a sorted profile."""
    if area <= 0.0:
        return float(sorted_heights[0])
    cumulative = np.cumsum(sorted_heights)
    counts = np.arange(1, sorted_heights.size + 1, dtype=np.float64)
    # Area submerging the first k samples, evaluated at the k-th height.
    capacity = (sorted_heights * counts - cumulative) * spacing
    k = int(np.searchsorted(capacity, area, side="right"))
    if k >= sorted_heights.size:
        k = sorted_heights.size
    return float((area / spacing + cumulative[k - 1]) / k)


def _capacity(sorted_heights: NDArray[np.float64], level: float, spacing: float) -> float:
    """Return the water area held below a level."""
    return float(np.maximum(level - sorted_heights, 0.0).sum() * spacing)


def _arc(start: int, stop: int, size: int) -> NDArray[np.int64]:
    return np.arange(start, stop, dtype=np.int64) % size
