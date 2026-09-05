"""The camera: world-to-screen transforms, zoom, scale bands, and culling.

**This module imports no pygame**, and a test enforces that. Nearly all of the
viewer's difficulty is coordinate arithmetic, so nearly all of it lives here
where it can be tested without a display.

Two things about precision, measured rather than assumed (Session 11):

1. **Camera-relative transforms do not buy float64 precision** at this feature's
   range. With a focus 1e11 m away and two points a metre apart, the relative
   and absolute forms both give exactly 100 px -- eleven orders of magnitude sit
   comfortably inside float64's sixteen digits. What the absolute form actually
   breaks is *pixel coordinate magnitude*: 1e11 m at 100 px/m is 1e13 pixels,
   and SDL takes C ints that stop at 2.1e9. The renderer overflows long before
   the float does. (A float32 pipeline -- any GPU path -- would lose the
   precision too, which is why DECISION-016 chose SDL2 over OpenGL.)

2. **The real precision floor is in storing an absolute coordinate at all.** One
   float64 ulp at 1e11 m is about 15 microns, so a ground feature finer than
   that cannot be represented as an absolute world position however it is
   transformed. That is why a body on the surface is held as (surface
   coordinate, height) and composed hierarchically by `surface_to_screen`:
   the arithmetic stays in numbers of order the planet's radius, where an ulp is
   nanometres.

Axioms used: T0.1 (two dimensions) only. The viewer computes no physics.
Abstracts: nothing.

Depends on: sim.view.bands, sim.view.geometry
Used by: sim.view.scene, sim.view.render, sim.view.app
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

import numpy as np

from sim.view.bands import ScaleBand, band_for
from sim.view.geometry import Coordinate, Disc, add, mod, mul, sub

__all__ = ["Camera"]


@dataclass(frozen=True)
class Camera:
    """A window onto the plane.

    Attributes
    ----------
    focus_x, focus_y : float
        World point at the centre of the viewport.
    scale : float
        Pixels per world unit.
    width, height : int
        Viewport size in pixels.
    """

    focus_x: float
    focus_y: float
    scale: float
    width: int
    height: int
    #: The planet's circumference, used to decide the scale band. A band is
    #: "how much of the world can I see", which is a ratio rather than a
    #: length -- see sim.view.bands.
    reference_length: float = 1.0

    #: Zoom limits, expressed as the fraction of the world the viewport spans
    #: -- *not* as an absolute pixels-per-world-unit constant.
    #:
    #: Absolute limits were the first attempt and made the GROUND band
    #: unreachable: the simulation works in natural units where the orbital
    #: radius is about 1, so a cap of 1e9 px per world unit stopped the zoom
    #: at REGIONAL on a world 3.8e-5 units around. The same mistake the scale
    #: bands made, in a second place. A zoom limit is "how much of the world
    #: can I see", which is a ratio.
    MIN_SPAN_RATIO: Final[float] = 1e-10
    MAX_SPAN_RATIO: Final[float] = 1e7

    def __post_init__(self) -> None:
        if not math.isfinite(self.scale) or self.scale <= 0.0:
            raise ValueError(f"scale must be positive and finite, got {self.scale!r}")
        if not (math.isfinite(self.focus_x) and math.isfinite(self.focus_y)):
            raise ValueError(f"focus must be finite, got ({self.focus_x!r}, {self.focus_y!r})")
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"viewport must be positive, got {self.width}x{self.height}")
        if not math.isfinite(self.reference_length) or self.reference_length <= 0.0:
            raise ValueError(
                f"reference length must be positive and finite, got {self.reference_length!r}"
            )

    # --- transforms ------------------------------------------------------

    def world_to_screen(self, x: Coordinate, y: Coordinate) -> tuple[Coordinate, Coordinate]:
        """Map world coordinates to pixels, relative to the focus.

        Computes ``(world - focus) * scale`` and never ``world * scale``: the
        difference is small even when the coordinates are enormous, which keeps
        pixel values inside the range the renderer can accept.

        Returns
        -------
        tuple
            Screen x and y. Screen y increases downward; world y upward.
        """
        return self.offset_to_screen(
            sub(x, self.focus_x),
            sub(y, self.focus_y),
        )

    def offset_to_screen(
        self, dx: Coordinate, dy: Coordinate
    ) -> tuple[Coordinate, Coordinate]:
        """Map an offset already expressed relative to the focus."""
        return (
            self.width * 0.5 + dx * self.scale,
            self.height * 0.5 - dy * self.scale,
        )

    def anchored_to_screen(
        self,
        anchor_x: float,
        anchor_y: float,
        offset_x: Coordinate,
        offset_y: Coordinate,
    ) -> tuple[Coordinate, Coordinate]:
        """Map ``anchor + offset`` without ever forming the absolute sum.

        The anchor may be astronomically far away and the offset small. Taking
        ``anchor - focus`` first keeps both terms in a range where the offset
        is not rounded away. Summing them first would quantise the offset to
        the anchor's ulp -- 15 microns at 1e11 m.
        """
        return self.offset_to_screen(
            add(offset_x, anchor_x - self.focus_x),
            add(offset_y, anchor_y - self.focus_y),
        )

    def surface_to_screen(
        self, planet: Disc, surface: Coordinate, height: Coordinate
    ) -> tuple[Coordinate, Coordinate]:
        """Map a position on a planet's surface to pixels.

        Surface position is periodic: ``theta = 2*pi*s / circumference``, and
        the point sits at ``radius + height`` from the centre. One
        representation serves every zoom -- a stretch of ground looking straight
        and the world closing into a circle are the same formula, so the
        transition needs no special case.

        Parameters
        ----------
        planet : Disc
        surface : float | ndarray
            Position along the closed surface. Wraps.
        height : float | ndarray
            Height above the surface.
        """
        theta = mul(mod(surface, planet.circumference), 2.0 * math.pi / planet.circumference)
        distance = add(height, planet.radius)
        return self.anchored_to_screen(
            planet.centre_x,
            planet.centre_y,
            mul(distance, np.cos(theta)),
            mul(distance, np.sin(theta)),
        )

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        """Map pixels back to world coordinates."""
        return (
            self.focus_x + (sx - self.width * 0.5) / self.scale,
            self.focus_y - (sy - self.height * 0.5) / self.scale,
        )

    # --- movement --------------------------------------------------------

    def zoomed(self, factor: float) -> Camera:
        """Return a camera scaled by `factor`, clamped to the zoom limits."""
        if not math.isfinite(factor) or factor <= 0.0:
            raise ValueError(f"zoom factor must be positive and finite, got {factor!r}")
        target = min(max(self.scale * factor, self.min_scale), self.max_scale)
        return Camera(
            self.focus_x, self.focus_y, target, self.width, self.height, self.reference_length
        )

    def zoomed_about(self, factor: float, sx: float, sy: float) -> Camera:
        """Zoom while keeping the world point under a screen position fixed."""
        anchor = self.screen_to_world(sx, sy)
        zoomed = self.zoomed(factor)
        moved = zoomed.screen_to_world(sx, sy)
        return Camera(
            self.focus_x + (anchor[0] - moved[0]),
            self.focus_y + (anchor[1] - moved[1]),
            zoomed.scale,
            self.width,
            self.height,
            self.reference_length,
        )

    def panned(self, dx: float, dy: float) -> Camera:
        """Return a camera moved by a world-space offset."""
        return Camera(
            self.focus_x + dx, self.focus_y + dy, self.scale, self.width, self.height,
            self.reference_length,
        )

    def resized(self, width: int, height: int) -> Camera:
        """Return the same view in a different-sized window.

        Focus and zoom are preserved, so resizing shows more or less of the
        world rather than magnifying what was there. The scale band can change
        as a result, since a band is how much of the world is in view.
        """
        return Camera(self.focus_x, self.focus_y, self.scale, width, height,
                      self.reference_length)

    def focused_on(self, x: float, y: float) -> Camera:
        """Return a camera centred elsewhere, at the same zoom."""
        return Camera(x, y, self.scale, self.width, self.height, self.reference_length)

    def focused_on_surface(
        self, planet: Disc, surface: float, height: float = 0.0
    ) -> Camera:
        """Return a camera centred on a point of a planet's surface.

        Centring on the planet's *centre* is right only while the whole planet
        fits in the viewport. Past that it puts the camera inside the world with
        the ground thousands of pixels away, which is what "zoom in and see
        nothing" looked like before this existed.
        """
        theta = 2.0 * math.pi * (surface % planet.circumference) / planet.circumference
        distance = planet.radius + height
        return self.focused_on(
            planet.centre_x + distance * math.cos(theta),
            planet.centre_y + distance * math.sin(theta),
        )

    # --- reporting -------------------------------------------------------

    @property
    def metres_per_pixel(self) -> float:
        """World units covered by one pixel."""
        return 1.0 / self.scale

    @property
    def min_scale(self) -> float:
        """Widest zoom out: the viewport spans MAX_SPAN_RATIO worlds."""
        return self.width / (self.MAX_SPAN_RATIO * self.reference_length)

    @property
    def max_scale(self) -> float:
        """Deepest zoom in: the viewport spans MIN_SPAN_RATIO of the world."""
        return self.width / (self.MIN_SPAN_RATIO * self.reference_length)

    @property
    def span(self) -> float:
        """The viewport's width in world units."""
        return self.width * self.metres_per_pixel

    @property
    def span_ratio(self) -> float:
        """Viewport width as a fraction of the planet's circumference."""
        return self.span / self.reference_length

    @property
    def band(self) -> ScaleBand:
        """Which scale band this zoom level falls in."""
        return band_for(self.span_ratio)

    @property
    def is_clamped(self) -> bool:
        """True when the zoom has hit a limit, so callers can say so."""
        return self.scale <= self.min_scale or self.scale >= self.max_scale
