"""The scene: which drawables are asked to draw, and when.

Registration is a list and dispatch is a band check. Deliberately not a scene
graph, an event bus, or a plugin system -- the cost of adding the fourth layer
must be adding one class.

**Imports no pygame.** The draw target is opaque here, so band dispatch is
testable with no display at all.

Axioms used: none. Presentation, not physics.
Abstracts: nothing.

Depends on: sim.errors, sim.view.bands, sim.view.camera
Used by: sim.view.app
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from sim.errors import VellumError
from sim.view.bands import ScaleBand
from sim.view.camera import Camera

__all__ = ["Drawable", "Scene"]


@runtime_checkable
class Drawable(Protocol):
    """Something the viewer can draw at some range of zoom levels.

    A layer joins the view by implementing this and being registered. It
    declares the bands it appears in; the scene never asks it to draw outside
    them, so a drawable need not check the zoom itself.
    """

    @property
    def bands(self) -> frozenset[ScaleBand]:
        """The scale bands in which this appears. Must not be empty."""
        ...

    def draw(self, camera: Camera, target: object) -> None:
        """Draw onto `target` through `camera`."""
        ...


class Scene:
    """An ordered collection of drawables, dispatched by scale band.

    Examples
    --------
    >>> scene = Scene()                     # doctest: +SKIP
    >>> scene.add(StarDisc(kell))           # doctest: +SKIP
    >>> scene.draw(camera, surface)         # doctest: +SKIP
    """

    def __init__(self) -> None:
        self._drawables: list[Drawable] = []

    def add(self, drawable: Drawable) -> None:
        """Register a drawable. Draw order is registration order.

        Raises
        ------
        VellumError
            If the drawable declares no bands. It would then silently never
            appear, which is the worst failure a viewer can have: the picture
            looks fine and is quietly missing a layer.
        """
        if not drawable.bands:
            raise VellumError(
                f"{type(drawable).__name__} declares no scale bands, so it would never "
                "be drawn. Declare the bands it appears in."
            )
        self._drawables.append(drawable)

    def draw(self, camera: Camera, target: object) -> None:
        """Draw every registered drawable whose bands include the current one.

        Exceptions from a drawable propagate. A viewer that quietly skips a
        broken layer shows a plausible picture of the wrong world, which is
        worse than showing nothing.
        """
        band = camera.band
        for drawable in self._drawables:
            if band in drawable.bands:
                drawable.draw(camera, target)

    def __len__(self) -> int:
        return len(self._drawables)
