"""Day and night on a closed surface.

**The terminator is two points, not a curve.** In three dimensions it is a
great circle; here the surface is a closed curve, so the lit and dark regions
are two arcs meeting at two points.

The lit arc's half-angle is ``arccos(R/d)`` exactly, not the ``pi/2`` a distant
star would give. That matters: at ``d/R = 10`` the distant approximation is
wrong by 6%, and at ``d/R = 2`` it lights a third of the world rather than half.

The geometry is pinned by one identity. A convex body subtends
``2*arcsin(R/d)`` at a point source, so it intercepts ``L*arcsin(R/d)/pi`` of
the star's output -- **exactly**, not asymptotically. Integrating
``F(r)*cos(incidence)`` around the lit arc must give the same number, which
checks the incidence geometry, the ``1/r`` flux dilution and the terminator all
at once.

Absolute flux values rest on Kell's stubbed luminosity, so they are
consequences of a chosen parameter. The *geometry* of day and night is not:
it follows from T0.1 and is a genuine result.

Axioms used: T0.1 (two dimensions), T2.2 (radiation, flux diluting as 1/r).
Abstracts: Kell's luminosity, via the supplied value.

Depends on: sim.errors, sim.orbit.insolation, sim.rotation.spin, sim.units
Used by: sim.view.render, and the climate layers when they exist
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError
from sim.rotation.spin import Spin
from sim.units import FLUX, LENGTH, LUMINOSITY, Quantity

__all__ = [
    "incidence_cosine",
    "intercepted_power",
    "is_lit",
    "lit_fraction",
    "substellar_surface",
    "surface_flux",
    "terminator_surfaces",
]

Value = float | NDArray[np.float64]
Mask = np.bool_ | NDArray[np.bool_]


def lit_fraction(radius: Quantity, distance: Quantity) -> float:
    """Return the fraction of the surface in daylight: ``arccos(R/d)/pi``.

    Tends to exactly one half for a distant star, and is markedly less when the
    star is close -- a third at ``d/R = 2``.

    Raises
    ------
    ValueError
        If the star is not outside the planet.

    Examples
    --------
    >>> from sim.units import LENGTH, Quantity
    >>> round(lit_fraction(Quantity(1.0, LENGTH), Quantity(2.0, LENGTH)), 6)
    0.333333
    """
    r, d = _radius_and_distance(radius, distance)
    return math.acos(r / d) / math.pi


def terminator_surfaces(
    spin: Spin, time: float, star_angle: float, distance: Quantity
) -> tuple[float, float]:
    """Return the two surface coordinates where day meets night.

    Exactly two, always. That is what it means for the terminator to be a pair
    of points rather than a curve.
    """
    _, d = _radius_and_distance(Quantity(spin.radius, LENGTH), distance)
    half = math.acos(spin.radius / d)
    return (
        float(spin.surface_at_inertial_angle(star_angle - half, time)),
        float(spin.surface_at_inertial_angle(star_angle + half, time)),
    )


def substellar_surface(spin: Spin, time: float, star_angle: float) -> float:
    """Return the surface coordinate directly facing the star."""
    return float(spin.surface_at_inertial_angle(star_angle, time))


def _offset(spin: Spin, surface: Value, time: float, star_angle: float) -> Value:
    """Angle between a surface point's outward normal and the star direction."""
    angle = spin.inertial_angle(surface, time)
    return np.asarray(angle) - star_angle


def is_lit(
    spin: Spin, surface: Value, time: float, star_angle: float, distance: Quantity
) -> Mask:
    """Return whether each surface point can see the star.

    Lit where ``cos(angle from the substellar point) > R/d`` -- the tangent
    condition, not simply "on the near side".
    """
    _, d = _radius_and_distance(Quantity(spin.radius, LENGTH), distance)
    lit = np.cos(_offset(spin, surface, time, star_angle)) > spin.radius / d
    return np.asarray(lit) if isinstance(surface, np.ndarray) else np.bool_(lit)


def incidence_cosine(
    spin: Spin, surface: Value, time: float, star_angle: float, distance: Quantity
) -> Value:
    """Return the cosine of the angle between the surface normal and the star.

    Zero at the terminator and clamped to zero through the night, so darkness
    is exact rather than a small number.
    """
    _, d = _radius_and_distance(Quantity(spin.radius, LENGTH), distance)
    theta = _offset(spin, surface, time, star_angle)
    r = spin.radius
    to_star = np.sqrt(d * d + r * r - 2.0 * d * r * np.cos(theta))
    cosine = (d * np.cos(theta) - r) / to_star
    return np.maximum(cosine, 0.0)


def surface_flux(
    spin: Spin,
    surface: Value,
    time: float,
    star_angle: float,
    luminosity: Quantity,
    distance: Quantity,
) -> Quantity:
    """Return the flux falling on a surface point, zero through the night.

    The flux is evaluated at the point's own distance from the star rather than
    the planet centre's, which is what makes the intercepted-power identity come
    out exact rather than approximate.
    """
    _, d = _radius_and_distance(Quantity(spin.radius, LENGTH), distance)
    theta = _offset(spin, surface, time, star_angle)
    r = spin.radius
    to_star = np.sqrt(d * d + r * r - 2.0 * d * r * np.cos(theta))
    power = luminosity.scalar(LUMINOSITY)
    values = (power / (2.0 * np.pi * to_star)) * incidence_cosine(
        spin, surface, time, star_angle, distance
    )
    if not np.all(np.isfinite(values)):
        raise InvariantError("surface flux produced a non-finite value")
    return Quantity(values, FLUX)


def intercepted_power(spin: Spin, luminosity: Quantity, distance: Quantity) -> float:
    """Return the total power the planet takes from the star.

    Computed by integrating the flux around the lit arc. Must equal
    ``L*arcsin(R/d)/pi``, the share of the star's output the planet's shadow
    subtends -- exactly, for a convex body and a point source.
    """
    _, d = _radius_and_distance(Quantity(spin.radius, LENGTH), distance)
    half = math.acos(spin.radius / d)
    theta = np.linspace(-half, half, 200_001)
    surface = spin.surface_at_inertial_angle(theta, 0.0)
    flux = surface_flux(spin, surface, 0.0, 0.0, luminosity, distance).array(FLUX)
    return float(np.trapezoid(flux * spin.radius, theta))


def _radius_and_distance(radius: Quantity, distance: Quantity) -> tuple[float, float]:
    r = radius.scalar(LENGTH)
    d = distance.scalar(LENGTH)
    for name, value in (("radius", r), ("distance", d)):
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be positive and finite, got {value!r}")
    if d <= r:
        raise ValueError(
            f"the star must be outside the planet: distance {d!r} <= radius {r!r}"
        )
    return r, d
