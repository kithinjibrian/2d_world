"""The viewer: a window that zooms from the whole system down to the ground.

Public surface of the view layer. Import from here.

**How a future layer joins the view** — implement two things and register:
a `bands` attribute naming the `ScaleBand`s it appears in, and
`draw(camera, target)`. Use `camera.surface_to_screen` for anything sitting on
the ground, never an absolute world position, and `visible_surface_indices` to
cull a sorted array of bodies to the visible arc. That is the whole contract;
there is no scene graph and no registry beyond a list.

Axioms used: T0.1. The viewer computes no physics.
Abstracts: nothing.
"""

from sim.view.bands import BAND_BOUNDS_RATIO, ScaleBand, band_for
from sim.view.camera import Camera
from sim.view.geometry import Coordinate, Disc, visible_surface_indices
from sim.view.scene import Drawable, Scene

__all__ = [
    "BAND_BOUNDS_RATIO",
    "Camera",
    "Coordinate",
    "Disc",
    "Drawable",
    "ScaleBand",
    "Scene",
    "band_for",
    "visible_surface_indices",
]
