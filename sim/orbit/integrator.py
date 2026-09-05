"""Velocity-Verlet integration of the two-body orbit under F = G2*M*m/r.

**The integrator is symplectic, at a fixed timestep.** The PRP justified this
by claiming a non-symplectic scheme would manufacture spurious apsidal
precession. That was tested in Session 9 and **the claim is wrong for this
potential**: forward Euler inflated the orbit's maximum radius from 1.10 to
2.13 over 1500 time units while the measured apsidal sweep moved by under
0.001 degrees.

The reason is that a logarithmic potential is **scale-invariant** -- ``r -> k*r``
together with ``t -> k*t`` leaves the equation of motion unchanged -- so an
orbit inflated by numerical energy is nearly a rescaled copy of itself, with
the same shape and the same apsidal angle. Precession is protected here in a
way it would not be under an inverse-square force.

The requirement stands, for the reason the test suite now encodes: what secular
drift wrecks is the orbit's *scale*, and **flux goes as 1/r**, so a doubled
radius halves the insolation with no visible symptom in the precession
measurement. That is the plausible-wrong-number failure this project exists to
prevent -- simply located somewhere other than where the PRP predicted.
Adaptive stepping is excluded for the same reason: it breaks symplecticity.

Kell sits fixed at the origin and Vellum is a test particle. Two bodies only —
see the Must NOT Do section of PRPs/orbit-layer.md.

Axioms used: T0.2 (Newtonian mechanics), T0.3 (non-relativistic — peak_speed is
reported so that assumption becomes checkable), T1.1 (gravity as a direct
force).
Abstracts: nothing.

Depends on: sim.errors, sim.units
Used by: sim.orbit.analysis, sim.orbit.insolation
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError
from sim.units import (
    G2,
    GRAVITATIONAL_CONSTANT,
    LENGTH,
    MASS,
    TIME,
    VELOCITY,
    Dimension,
    Quantity,
)

__all__ = ["Trajectory", "integrate"]


@dataclass(frozen=True)
class Trajectory:
    """A sampled orbit. Positions and velocities are natural-unit arrays.

    Attributes
    ----------
    positions : NDArray[np.float64]
        Shape (steps, 2).
    velocities : NDArray[np.float64]
        Shape (steps, 2).
    times : NDArray[np.float64]
        Shape (steps,).
    """

    positions: NDArray[np.float64]
    velocities: NDArray[np.float64]
    times: NDArray[np.float64]

    @property
    def radius(self) -> NDArray[np.float64]:
        """Distance from Kell at each sample."""
        return np.hypot(self.positions[:, 0], self.positions[:, 1])

    @property
    def speed(self) -> NDArray[np.float64]:
        """Speed at each sample."""
        return np.hypot(self.velocities[:, 0], self.velocities[:, 1])

    @property
    def peak_speed(self) -> float:
        """The largest speed reached.

        Reported so that T0.3 — the assumption that dynamics are
        non-relativistic — can be checked rather than merely assumed. It is the
        one axiom flagged as unvalidated in docs/AXIOMS.md, and this is the
        first layer able to say anything about it.
        """
        return float(self.speed.max())


def integrate(
    mass: Quantity,
    position: Quantity,
    velocity: Quantity,
    timestep: Quantity,
    steps: int,
    *,
    max_relative_energy_drift: float = 1e-3,
) -> Trajectory:
    """Integrate an orbit with velocity-Verlet at a fixed timestep.

    Parameters
    ----------
    mass : Quantity
        Central mass, natural units. Must be positive and finite.
    position : Quantity
        Initial position, shape (2,). Must not be at the origin — the
        logarithmic potential is singular there.
    velocity : Quantity
        Initial velocity, shape (2,). Must carry non-zero angular momentum;
        see Raises.
    timestep : Quantity
        Fixed step. Must be positive and finite.
    steps : int
        Number of steps to take. Must be positive.
    max_relative_energy_drift : float, optional
        Guard on the symplectic bound, checked periodically. Exceeding it means
        the step is too large for the dynamics, which is a bug rather than a
        result.

    Returns
    -------
    Trajectory
        Positions, velocities and times, sampled every step.

    Raises
    ------
    ValueError
        On a non-positive or non-finite parameter, a start at the origin, or a
        launch with zero angular momentum. Radial infall reaches a singular
        potential, which a fixed-step symplectic scheme cannot resolve; use
        :func:`sim.orbit.analytic.radial_turning_radius` for that case instead
        of integrating it badly.
    InvariantError
        If the state becomes non-finite, if the trajectory approaches the
        singularity, or if energy drift exceeds the bound.

    Examples
    --------
    >>> import numpy as np
    >>> from sim.units import LENGTH, MASS, TIME, VELOCITY, Quantity
    >>> t = integrate(
    ...     mass=Quantity(1.0, MASS),
    ...     position=Quantity(np.array([1.0, 0.0]), LENGTH),
    ...     velocity=Quantity(np.array([0.0, 1.0]), VELOCITY),
    ...     timestep=Quantity(1e-3, TIME),
    ...     steps=10,
    ... )
    >>> t.positions.shape
    (10, 2)
    """
    gm = _scalar(mass, MASS, "mass", positive=True) * _g2()
    dt = _scalar(timestep, TIME, "timestep", positive=True)
    if steps <= 0:
        raise ValueError(f"steps must be positive, got {steps!r}")

    x, y = _vector(position, LENGTH, "position")
    vx, vy = _vector(velocity, VELOCITY, "velocity")

    r0 = math.hypot(x, y)
    if r0 <= 0.0:
        raise ValueError("position must not be the origin: the potential is singular there")
    if x * vy - y * vx == 0.0:
        raise ValueError(
            "velocity must carry non-zero angular momentum. A purely radial "
            "trajectory falls into a singular potential, which a fixed-step "
            "symplectic integrator cannot resolve. Use "
            "sim.orbit.analytic.radial_turning_radius for the radial case."
        )

    positions = np.empty((steps, 2), dtype=np.float64)
    velocities = np.empty((steps, 2), dtype=np.float64)
    times = np.empty(steps, dtype=np.float64)

    # The floor below which the trajectory is treated as having reached the
    # singularity. Relative to the launch radius, so it scales with the problem.
    floor = 1e-9 * r0
    energy0 = 0.5 * (vx * vx + vy * vy) + gm * math.log(r0)
    energy_scale = max(abs(energy0), 1.0)
    check_every = max(1, steps // 100)

    # Plain floats rather than numpy scalars in the loop: this is a two-body
    # problem in two dimensions, so array machinery costs more than it saves.
    inv = gm / (r0 * r0)
    ax, ay = -inv * x, -inv * y
    half = 0.5 * dt

    for i in range(steps):
        vx += half * ax
        vy += half * ay
        x += dt * vx
        y += dt * vy

        r_squared = x * x + y * y
        if not math.isfinite(r_squared):
            raise InvariantError(f"state became non-finite at step {i}")
        if r_squared < floor * floor:
            raise InvariantError(
                f"trajectory reached the singularity at step {i} (r < {floor:g})"
            )

        inv = gm / r_squared
        ax, ay = -inv * x, -inv * y
        vx += half * ax
        vy += half * ay

        positions[i, 0] = x
        positions[i, 1] = y
        velocities[i, 0] = vx
        velocities[i, 1] = vy
        times[i] = (i + 1) * dt

        if i % check_every == 0:
            energy = 0.5 * (vx * vx + vy * vy) + gm * math.log(math.sqrt(r_squared))
            if abs(energy - energy0) / energy_scale > max_relative_energy_drift:
                raise InvariantError(
                    f"energy drift {abs(energy - energy0) / energy_scale:.3e} exceeded "
                    f"{max_relative_energy_drift:g} at step {i}; the timestep is too "
                    "large for these dynamics"
                )

    return Trajectory(positions=positions, velocities=velocities, times=times)


def _g2() -> float:
    return G2.scalar(GRAVITATIONAL_CONSTANT)


def _scalar(quantity: Quantity, dimension: Dimension, name: str, *, positive: bool) -> float:
    value = quantity.scalar(dimension)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    if positive and value <= 0.0:
        raise ValueError(f"{name} must be positive, got {value!r}")
    return value


def _vector(quantity: Quantity, dimension: Dimension, name: str) -> tuple[float, float]:
    array = quantity.array(dimension)
    if array.shape != (2,):
        raise ValueError(f"{name} must have shape (2,), got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be finite, got {array!r}")
    return float(array[0]), float(array[1])
