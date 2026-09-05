"""The list of things in the system, and picking one to look at.

Vellum orbits fast enough that catching it by hand and zooming in is not
practical: at system scale it crosses the window in a few seconds and its
radius there is three pixels. Selecting it from a list and being taken to it is
the only workable way in.

Layout and hit-testing live here and **import no pygame**, so the part with
decisions in it is testable without a display. The drawing is in
`sim.view.render`.

Axioms used: none. Presentation, not physics.
Abstracts: nothing.

Depends on: sim.view.camera, sim.view.geometry
Used by: sim.view.render, sim.view.app
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from sim.view.camera import Camera
from sim.view.geometry import Disc

__all__ = ["PANEL_WIDTH", "ROW_HEIGHT", "TOP", "Target", "frame", "row_at"]

#: Panel geometry, in pixels.
PANEL_WIDTH: Final = 190
ROW_HEIGHT: Final = 30
TOP: Final = 52

#: How much of the viewport a framed body should span. A quarter leaves the
#: thing you selected obviously the subject while keeping its surroundings.
FRAMED_FRACTION: Final = 0.25


@dataclass(frozen=True)
class Target:
    """Something in the system you can select and be taken to.

    Attributes
    ----------
    name : str
        What it is called in the list.
    x, y : float
        Where it is now, in world coordinates. Rebuilt each frame for anything
        that moves.
    radius : float
        Size used for framing. For Kell this is a **display** radius: the star
        is stubbed and its real radius raises by design (DECISION-010), so
        nothing here may be read as a physical result.
    surface : Disc | None
        Present when the body has ground you can stand on. Vellum has one; Kell
        does not.
    """

    name: str
    x: float
    y: float
    radius: float
    surface: Disc | None = None

    @property
    def has_ground(self) -> bool:
        """Whether the camera can descend to a surface on this body."""
        return self.surface is not None


def row_at(mouse_x: float, mouse_y: float, count: int) -> int | None:
    """Return the index of the row under the pointer, or None.

    Returns None for anything outside the panel, so the caller can treat a
    click on the world as a drag rather than a selection.

    Examples
    --------
    >>> row_at(20.0, TOP + 5.0, 2)
    0
    >>> row_at(400.0, TOP + 5.0, 2) is None
    True
    """
    if not (0.0 <= mouse_x < PANEL_WIDTH):
        return None
    index = int((mouse_y - TOP) // ROW_HEIGHT)
    if mouse_y < TOP or not (0 <= index < count):
        return None
    return index


def frame(camera: Camera, target: Target) -> Camera:
    """Return a camera looking at `target`, sized so it fills the view.

    This is the jump the pointer cannot make. Vellum's radius at system scale
    is about three pixels and it is moving; framing it crosses five orders of
    magnitude in one step and lands with the planet as the subject.
    """
    span = 2.0 * target.radius / FRAMED_FRACTION
    scale = camera.width / span
    factor = scale / camera.scale
    return camera.zoomed(factor).focused_on(target.x, target.y)
