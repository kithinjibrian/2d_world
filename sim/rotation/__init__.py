"""Vellum's rotation, and the day it produces.

Axioms used: T0.1, T0.2, T1.1, T2.2.
Abstracts: oblateness (a spinning body bulges; the disc stays circular), and
Kell's luminosity for absolute flux values.
"""

from sim.rotation.illumination import (
    incidence_cosine,
    intercepted_power,
    is_lit,
    lit_fraction,
    substellar_surface,
    surface_flux,
    terminator_surfaces,
)
from sim.rotation.spin import Spin, breakup_rate

__all__ = [
    "Spin",
    "breakup_rate",
    "incidence_cosine",
    "intercepted_power",
    "is_lit",
    "lit_fraction",
    "substellar_surface",
    "surface_flux",
    "terminator_surfaces",
]
