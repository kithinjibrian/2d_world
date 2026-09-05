"""Standing water on Vellum.

Axioms used: T0.1, T1.1.
Abstracts: terrain statistics — every count and fraction here rests on a chosen
roughness. See docs/AXIOMS.md §4.
"""

from sim.water.basins import Basin, BasinSet, analyse
from sim.water.filling import Lake, WaterState, fill

__all__ = ["Basin", "BasinSet", "Lake", "WaterState", "analyse", "fill"]
