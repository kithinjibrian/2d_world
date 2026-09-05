"""The named dimensions Vellum needs, in two dimensions.

This module is the in-code copy of docs/AXIOMS.md section 2. The table test in
sim/tests/units/test_dimension.py asserts the two agree, and must fail if
either drifts.

Where a dimension differs from its three-dimensional form, the comment says so.
Where it does not — kinematic viscosity, energy, force — that is worth knowing
too: not everything changes in two dimensions, and a reader who assumes
otherwise will "fix" something that was already right.

No three-dimensional form is defined here. See sim.units.dimension.

Axioms used: T0.1, T0.2, T1.1, T2.2.
Abstracts: nothing.

Depends on: sim.units.dimension
Used by: everything that names a physical quantity
"""

from __future__ import annotations

from typing import Final

from sim.units.dimension import Dimension

# --- base ---------------------------------------------------------------

DIMENSIONLESS: Final = Dimension()
MASS: Final = Dimension(mass=1)
LENGTH: Final = Dimension(length=1)
TIME: Final = Dimension(time=1)
TEMPERATURE: Final = Dimension(temperature=1)

# --- kinematics (unchanged in 2D) ---------------------------------------

VELOCITY: Final = LENGTH / TIME
ACCELERATION: Final = VELOCITY / TIME
MOMENTUM: Final = MASS * VELOCITY
ANGULAR_MOMENTUM: Final = MOMENTUM * LENGTH
MOMENT_OF_INERTIA: Final = MASS * LENGTH**2

# --- mechanics (unchanged in 2D) ----------------------------------------

FORCE: Final = MASS * ACCELERATION
ENERGY: Final = FORCE * LENGTH
POWER: Final = ENERGY / TIME

# --- quantities that differ in 2D ---------------------------------------

#: Mass per unit AREA, not volume: Vellum is a disc and has no third extent.
SURFACE_DENSITY: Final = MASS / LENGTH**2

#: Force per unit LENGTH, not area. A boundary in the plane is a line.
PRESSURE: Final = FORCE / LENGTH

#: Power per unit LENGTH of radiating curve, not per unit area.
FLUX: Final = POWER / LENGTH

#: F = G2*m1*m2/r, so [G2] = M^-1 L^2 T^-2. Not the 3D constant's dimensions,
#: and not the same kind of quantity. AXIOM (T1.1).
GRAVITATIONAL_CONSTANT: Final = FORCE * LENGTH / MASS**2

#: Emission scales as T^3 in two dimensions, so sigma_2 carries Theta^-3.
#: AXIOM (T2.2).
STEFAN_BOLTZMANN: Final = FLUX / TEMPERATURE**3

#: Dynamic viscosity: stress over strain rate. In 2D stress is a force per
#: length, giving M T^-1 rather than the three-dimensional M L^-1 T^-1.
VISCOSITY: Final = PRESSURE * TIME

#: Radiated power. Dimensionally identical to POWER — the two-dimensionality
#: shows up in the formula (L = 2*pi*R*sigma_2*T^3) and in how flux dilutes
#: (1/r, not 1/r^2), not in the dimension itself. Named separately because a
#: call site reads better for it.
LUMINOSITY: Final = POWER

# --- and one that does not ----------------------------------------------

#: L^2 T^-1 in any number of dimensions, even though the dynamic viscosity it
#: derives from differs. Present specifically as the counterexample.
KINEMATIC_VISCOSITY: Final = VISCOSITY / SURFACE_DENSITY

# --- thermodynamics ------------------------------------------------------

HEAT_CAPACITY: Final = ENERGY / TEMPERATURE
SPECIFIC_HEAT_CAPACITY: Final = ENERGY / (MASS * TEMPERATURE)

#: Registry for the table test and for error reporting. Keys are the names
#: above; nothing may be added here that is not also a module-level constant.
NAMED_DIMENSIONS: Final[dict[str, Dimension]] = {
    "DIMENSIONLESS": DIMENSIONLESS,
    "MASS": MASS,
    "LENGTH": LENGTH,
    "TIME": TIME,
    "TEMPERATURE": TEMPERATURE,
    "VELOCITY": VELOCITY,
    "ACCELERATION": ACCELERATION,
    "MOMENTUM": MOMENTUM,
    "ANGULAR_MOMENTUM": ANGULAR_MOMENTUM,
    "MOMENT_OF_INERTIA": MOMENT_OF_INERTIA,
    "FORCE": FORCE,
    "ENERGY": ENERGY,
    "POWER": POWER,
    "LUMINOSITY": LUMINOSITY,
    "SURFACE_DENSITY": SURFACE_DENSITY,
    "PRESSURE": PRESSURE,
    "FLUX": FLUX,
    "GRAVITATIONAL_CONSTANT": GRAVITATIONAL_CONSTANT,
    "STEFAN_BOLTZMANN": STEFAN_BOLTZMANN,
    "VISCOSITY": VISCOSITY,
    "KINEMATIC_VISCOSITY": KINEMATIC_VISCOSITY,
    "HEAT_CAPACITY": HEAT_CAPACITY,
    "SPECIFIC_HEAT_CAPACITY": SPECIFIC_HEAT_CAPACITY,
}
