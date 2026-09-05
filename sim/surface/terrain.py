"""Vellum's ground: height as a function of position along the closed surface.

The surface is a closed curve, so height is a function of **one** periodic
coordinate. There is no second surface coordinate, and an API taking two would
misunderstand the world.

Terrain is a procedural base field plus an optional sampled residual
(DECISION-017). The base is multi-octave gradient noise: octave ``n`` lays
``2**n`` cells over the surface, so its wavelength is ``C / 2**n`` and the
finest detail available is ``C / 2**octaves``. That floor is finite and real --
"evaluable at any resolution" was always an overstatement, and this module
reports the floor rather than inventing smooth ground below it.

**Terrain statistics are abstracted, not derived.** Nothing in docs/AXIOMS.md
predicts a roughness exponent; deriving one would need tectonics and erosion,
which are not modelled. Amplitude and roughness are world constants. Any result
about mountains, slopes or basin shapes is therefore a consequence of a choice,
not a finding about two-dimensional physics. See docs/AXIOMS.md section 4.

Axioms used: T0.1 (two dimensions -- a closed surface curve).
Abstracts: terrain statistics (amplitude, roughness).

Depends on: sim.errors, sim.surface.noise, sim.units
Used by: sim.view.render, and the water layer when it exists
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from sim.errors import InvariantError
from sim.surface.noise import gradient_noise
from sim.units import LENGTH, Quantity

__all__ = ["Terrain"]

#: Samples used once at construction to normalise the field to the requested
#: RMS amplitude. Deterministic, so the normalisation is part of the seed.
_NORMALISATION_SAMPLES: int = 1 << 15


class Terrain:
    """A height field on a closed surface.

    Parameters
    ----------
    circumference : float
        Length of the closed surface curve, natural units. Positions are
        periodic with this.
    amplitude : float
        Target RMS height. **A world constant, not derived** -- see the module
        docstring.
    roughness : float
        Spectral exponent ``beta`` in ``P(k) ~ k**-beta``. Octave amplitudes
        fall as ``2**(-(beta-1)*n/2)`` -- the ``-1`` is the one-dimensional
        mode-density factor, see the comment in ``__init__``. This is what
        makes the field fractal rather than merely random. **A world constant,
        not derived.**
    seed : int
        World seed. The same seed gives byte-identical terrain.
    octaves : int
        Number of octaves. Sets the resolution floor at ``C / 2**octaves``.
    residual : NDArray[np.float64] | None
        Optional sampled heights added on top, evenly spaced around the
        surface and interpolated periodically. This is where a crater or an
        eroded channel will live -- modifications that cannot be expressed by
        changing a noise parameter. Costs nothing when absent.

    Examples
    --------
    >>> t = Terrain(circumference=1000.0, amplitude=10.0, roughness=2.0,
    ...             seed=1, octaves=8)
    >>> bool(abs(float(t.height(0.0)) - float(t.height(1000.0))) < 1e-9)
    True
    """

    def __init__(
        self,
        circumference: float,
        amplitude: float,
        roughness: float,
        seed: int,
        octaves: int,
        residual: NDArray[np.float64] | None = None,
    ) -> None:
        _require_positive(circumference, "circumference")
        _require_positive(amplitude, "amplitude")
        if not math.isfinite(roughness):
            raise ValueError(f"roughness must be finite, got {roughness!r}")
        if octaves <= 0:
            raise ValueError(f"octaves must be positive, got {octaves!r}")

        self.circumference = circumference
        self.amplitude = amplitude
        self.roughness = roughness
        self.seed = int(seed)
        self.octaves = int(octaves)

        if residual is not None:
            residual = np.asarray(residual, dtype=np.float64)
            if residual.size == 0:
                raise ValueError("residual must not be empty")
            if not np.all(np.isfinite(residual)):
                raise ValueError("residual must be finite")
        self.residual = residual

        # Octave amplitudes fall as 2**(-p*n), and the measured spectral slope
        # is -(2p + 1), not -2p. The extra 1 is mode density: in one dimension
        # an octave band [2**n, 2**(n+1)) holds ~2**n Fourier modes, so power
        # *per mode* carries an additional factor of k**-1. Verified against
        # measurement -- p = 0.5, 1.0, 1.5 give slopes -1.98, -2.96, -3.92.
        # So to deliver P(k) ~ k**-beta: p = (beta - 1) / 2.
        decay = 2.0 ** (-0.5 * (roughness - 1.0))
        self._weights = decay ** np.arange(self.octaves, dtype=np.float64)
        self._scale = 1.0
        self._scale = amplitude / self._measured_rms()

    # --- the field -------------------------------------------------------

    def height(
        self, surface: float | NDArray[np.float64], resolution: float | None = None
    ) -> NDArray[np.float64]:
        """Return the ground height at one or more surface positions.

        Parameters
        ----------
        surface : float | NDArray[np.float64]
            Position along the closed surface. Wraps; any real value is valid.
        resolution : float | None
            Finest detail wanted, in world units. Only the octaves that matter
            at that scale are summed, so a whole-world profile does not pay for
            metre detail. ``None`` uses every octave. A request finer than
            :attr:`resolution_floor` returns the finest available -- see
            :meth:`is_clamped_at`; it is never met with invented detail.

        Returns
        -------
        NDArray[np.float64]
            Heights, natural units.

        Raises
        ------
        ValueError
            If `resolution` is non-positive.
        InvariantError
            If any height is non-finite. The noise is bounded by construction,
            so that means the hash or the interpolation is broken.
        """
        count = self.octaves if resolution is None else self.octaves_for(resolution)
        values = self._base(np.asarray(surface, dtype=np.float64), count)
        if self.residual is not None:
            values = values + self._residual_at(np.asarray(surface, dtype=np.float64))
        if not np.all(np.isfinite(values)):
            raise InvariantError("terrain produced a non-finite height")
        return values

    def height_quantity(
        self, surface: float | NDArray[np.float64], resolution: float | None = None
    ) -> Quantity:
        """Return :meth:`height` as a dimensioned Quantity, for boundaries."""
        return Quantity(self.height(surface, resolution), LENGTH)

    def _base(self, surface: NDArray[np.float64], count: int) -> NDArray[np.float64]:
        t = surface / self.circumference
        total = np.zeros(np.shape(t), dtype=np.float64)
        for octave in range(count):
            total = total + self._weights[octave] * gradient_noise(
                t, cells=2**octave, seed=self.seed, octave=octave
            )
        return self._scale * total

    def _residual_at(self, surface: NDArray[np.float64]) -> NDArray[np.float64]:
        assert self.residual is not None
        samples = self.residual.size
        position = np.mod(surface / self.circumference, 1.0) * samples
        lower = np.floor(position).astype(np.int64)
        frac = position - lower
        # Wrap the upper index so interpolation is continuous across the seam.
        interpolated = (1.0 - frac) * self.residual[lower % samples] + frac * self.residual[
            (lower + 1) % samples
        ]
        return np.asarray(interpolated, dtype=np.float64)

    def _measured_rms(self) -> float:
        s = np.linspace(0.0, self.circumference, _NORMALISATION_SAMPLES, endpoint=False)
        return float(np.sqrt(np.mean(self._base(s, self.octaves) ** 2)))

    # --- reporting -------------------------------------------------------

    @property
    def resolution_floor(self) -> float:
        """Finest detail this terrain contains: ``circumference / 2**octaves``.

        Real and finite. Below it there is nothing to show, and the field says
        so rather than returning smooth invention.
        """
        return self.circumference / 2.0**self.octaves

    @property
    def maximum_height(self) -> float:
        """Upper bound on ``|height|``, from the octave amplitudes."""
        bound = self._scale * float(np.sum(self._weights))
        if self.residual is not None:
            bound += float(np.max(np.abs(self.residual)))
        return bound

    def octaves_for(self, resolution: float) -> int:
        """Return how many octaves are needed to resolve `resolution`."""
        _require_positive(resolution, "resolution")
        wanted = math.ceil(math.log2(self.circumference / resolution))
        return max(1, min(self.octaves, wanted))

    def is_clamped_at(self, resolution: float) -> bool:
        """True when `resolution` is finer than this terrain contains."""
        _require_positive(resolution, "resolution")
        return resolution < self.resolution_floor


def _require_positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite, got {value!r}")
