"""Vellum's ground.

Axioms used: T0.1.
Abstracts: terrain statistics (amplitude, roughness) — see docs/AXIOMS.md §4.
"""

from sim.surface.noise import gradient_noise, mix64
from sim.surface.terrain import Terrain

__all__ = ["Terrain", "gradient_noise", "mix64"]
