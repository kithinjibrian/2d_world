"""The two-body Kell-Vellum orbit under two-dimensional gravity.

Public surface of the orbit layer. Import from here.

Axioms used: T0.2, T0.3, T1.1, T2.2.
Abstracts: Kell's luminosity (insolation only).
"""

from sim.orbit.analysis import (
    apsidal_angle,
    pericentre_indices,
    pericentre_to_pericentre_angle,
    specific_angular_momentum,
    specific_energy,
)
from sim.orbit.analytic import (
    APSIDAL_ANGLE_NEAR_CIRCULAR,
    APSIDAL_REGRESSION_PER_ORBIT,
    SEASON_CYCLE_ORBITS,
    circular_period,
    circular_speed,
    radial_turning_radius,
    turning_radius,
)
from sim.orbit.insolation import flux_at, insolation_series
from sim.orbit.integrator import Trajectory, integrate

__all__ = [
    "APSIDAL_ANGLE_NEAR_CIRCULAR",
    "APSIDAL_REGRESSION_PER_ORBIT",
    "SEASON_CYCLE_ORBITS",
    "Trajectory",
    "apsidal_angle",
    "circular_period",
    "circular_speed",
    "flux_at",
    "insolation_series",
    "integrate",
    "pericentre_indices",
    "pericentre_to_pericentre_angle",
    "radial_turning_radius",
    "specific_angular_momentum",
    "specific_energy",
    "turning_radius",
]
