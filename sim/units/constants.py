"""The normalised physical constants.

Both are 1 by construction, not by measurement — see sim.units.system. They are
Quantities rather than bare floats so that composing them into a formula carries
dimensions, which is what makes the discriminating tests possible.

Axioms used: T1.1, T2.2.
Abstracts: nothing.

Depends on: sim.units.named, sim.units.quantity
Used by: every module doing gravitation or radiation
"""

from __future__ import annotations

from typing import Final

from sim.units.named import GRAVITATIONAL_CONSTANT, STEFAN_BOLTZMANN
from sim.units.quantity import Quantity

__all__ = ["G2", "SIGMA_2"]

#: AXIOM (T1.1): gravity is a postulated direct force, not spacetime curvature —
#: 2+1D general relativity has zero propagating degrees of freedom and produces
#: no attraction at all. Gauss's law in a plane gives F = G2*m1*m2/r.
#: Normalised to 1; the value is a choice of units, not a measurement.
G2: Final = Quantity(1.0, GRAVITATIONAL_CONSTANT)

#: AXIOM (T2.2): blackbody flux per unit length of radiating curve goes as T^3,
#: from counting modes in two dimensions. Normalised to 1.
SIGMA_2: Final = Quantity(1.0, STEFAN_BOLTZMANN)
