"""Scene tests: which drawables are asked to draw, and when."""

import pytest

from sim.errors import VellumError
from sim.view import Camera, ScaleBand, Scene


class Recorder:
    """A drawable that records the bands it was drawn in."""

    def __init__(self, bands: frozenset[ScaleBand]) -> None:
        self.bands = bands
        self.calls: list[ScaleBand] = []

    def draw(self, camera: Camera, target: object) -> None:
        self.calls.append(camera.band)


class Exploder:
    bands = frozenset({ScaleBand.GROUND, ScaleBand.SYSTEM})

    def draw(self, camera: Camera, target: object) -> None:
        raise RuntimeError("layer is broken")


def cam(scale: float) -> Camera:
    return Camera(
        focus_x=0.0, focus_y=0.0, scale=scale, width=800, height=600, reference_length=1e6
    )


class TestBandFiltering:
    def test_drawn_only_inside_declared_bands(self) -> None:
        ground = Recorder(frozenset({ScaleBand.GROUND}))
        system = Recorder(frozenset({ScaleBand.SYSTEM}))
        scene = Scene()
        scene.add(ground)
        scene.add(system)

        scene.draw(cam(1e4), target=None)     # GROUND
        scene.draw(cam(1e-6), target=None)    # SYSTEM

        assert ground.calls == [ScaleBand.GROUND]
        assert system.calls == [ScaleBand.SYSTEM]

    def test_a_drawable_in_every_band_is_always_drawn(self) -> None:
        everywhere = Recorder(frozenset(ScaleBand))
        scene = Scene()
        scene.add(everywhere)
        for scale in (1e4, 1.0, 1e-3, 1e-6):
            scene.draw(cam(scale), target=None)
        assert len(everywhere.calls) == 4

    def test_registration_order_is_draw_order(self) -> None:
        order: list[str] = []

        class Named:
            bands = frozenset(ScaleBand)

            def __init__(self, name: str) -> None:
                self.name = name

            def draw(self, camera: Camera, target: object) -> None:
                order.append(self.name)

        scene = Scene()
        scene.add(Named("back"))
        scene.add(Named("front"))
        scene.draw(cam(1.0), target=None)
        assert order == ["back", "front"]


class TestRegistrationErrors:
    def test_empty_bands_raises(self) -> None:
        # It would silently never appear, which is the worst failure a viewer
        # can have: the picture looks fine and is missing a layer.
        with pytest.raises(VellumError):
            Scene().add(Recorder(frozenset()))

    def test_a_broken_layer_propagates_rather_than_being_skipped(self) -> None:
        # A viewer that quietly skips a failing layer shows a plausible picture
        # of the wrong world.
        scene = Scene()
        scene.add(Exploder())
        with pytest.raises(RuntimeError, match="layer is broken"):
            scene.draw(cam(1e4), target=None)
