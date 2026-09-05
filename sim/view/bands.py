"""Scale bands: how far out we are, in four named steps.

A drawable declares which bands it appears in, so adding a layer means
answering one question rather than editing the renderer. The bands are
disjoint and exhaustive over positive span ratios.

**Imports no pygame** -- see sim.view.camera for why that matters.

Axioms used: none. Presentation, not physics.
Abstracts: nothing.

Depends on: nothing
Used by: sim.view.camera, sim.view.scene, sim.view.render
"""

from __future__ import annotations

import math
from enum import Enum
from typing import Final

__all__ = ["BAND_BOUNDS_RATIO", "ScaleBand", "band_for"]


class ScaleBand(Enum):
    """How far out we are, in four named steps."""

    GROUND = "ground"
    REGIONAL = "regional"
    PLANETARY = "planetary"
    SYSTEM = "system"


#: Upper bound of each band, as the **dimensionless ratio** of the viewport's
#: span to the planet's circumference. Ordered, disjoint, exhaustive.
#:
#: Absolute thresholds in metres were the first attempt and were simply wrong:
#: the simulation works in natural units where the orbital radius is about 1,
#: so every zoom level landed in one band. A band means "how much of the world
#: can I see", which is a ratio, not a length -- and ratios are the only thing
#: physically meaningful here anyway (docs/AXIOMS.md section 2).
BAND_BOUNDS_RATIO: Final[dict[ScaleBand, float]] = {
    ScaleBand.GROUND: 1e-4,     # a sliver of surface
    ScaleBand.REGIONAL: 0.5,    # a recognisable stretch of it
    ScaleBand.PLANETARY: 30.0,  # the whole world, and some space around it
    ScaleBand.SYSTEM: math.inf,  # the orbit
}


def band_for(span_ratio: float) -> ScaleBand:
    """Return the scale band for a viewport span, relative to the world.

    Parameters
    ----------
    span_ratio : float
        The viewport's width in world units divided by the planet's
        circumference. Dimensionless. Must be positive and not NaN.

    Returns
    -------
    ScaleBand

    Raises
    ------
    ValueError
        If the ratio is non-positive or NaN.

    Examples
    --------
    >>> band_for(1e-6) is ScaleBand.GROUND
    True
    >>> band_for(100.0) is ScaleBand.SYSTEM
    True
    """
    if math.isnan(span_ratio) or span_ratio <= 0.0:
        raise ValueError(f"span ratio must be positive, got {span_ratio!r}")
    for band, upper in BAND_BOUNDS_RATIO.items():
        if span_ratio < upper:
            return band
    return ScaleBand.SYSTEM  # pragma: no cover - the inf bound makes this unreachable
