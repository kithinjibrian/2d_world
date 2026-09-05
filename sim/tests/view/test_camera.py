"""Camera tests. All pure, all headless — camera.py imports no pygame.

The precision tests here were rewritten during Session 11 after measuring what
float64 actually does. See TestWhyTransformsAreAnchored for what was found.
"""

import ast
import math
from pathlib import Path

import numpy as np
import pytest

from sim.view import (
    BAND_BOUNDS_RATIO,
    Camera,
    ScaleBand,
    band_for,
    visible_surface_indices,
)

VIEWPORT = (800, 600)


def cam(scale: float, fx: float = 0.0, fy: float = 0.0) -> Camera:
    return Camera(focus_x=fx, focus_y=fy, scale=scale, width=800, height=600)


class TestTransform:
    def test_focus_lands_at_the_viewport_centre(self) -> None:
        sx, sy = cam(1.0, 5.0, 7.0).world_to_screen(5.0, 7.0)
        assert (sx, sy) == pytest.approx((400.0, 300.0))

    def test_y_increases_upward_in_the_world(self) -> None:
        # Screen y grows downward; world y grows upward. A point above the
        # focus must land above the centre.
        _, sy = cam(1.0).world_to_screen(0.0, 10.0)
        assert sy < 300.0

    def test_scale_is_pixels_per_world_unit(self) -> None:
        sx, _ = cam(3.0).world_to_screen(2.0, 0.0)
        assert sx == pytest.approx(400.0 + 6.0)

    @pytest.mark.parametrize("scale", [1e-9, 1e-3, 1.0, 1e3, 1e6])
    def test_round_trip(self, scale: float) -> None:
        c = cam(scale, 1e7, -3e6)
        for point in [(1e7, -3e6), (1e7 + 100.0 / scale, -3e6)]:
            sx, sy = c.world_to_screen(*point)
            back = c.screen_to_world(float(sx), float(sy))
            assert back == pytest.approx(point, rel=1e-12, abs=1e-9 / scale)

    def test_accepts_arrays(self) -> None:
        xs = np.array([0.0, 1.0, 2.0])
        ys = np.zeros(3)
        sx, sy = cam(2.0).world_to_screen(xs, ys)
        assert np.allclose(np.asarray(sx), [400.0, 402.0, 404.0])
        assert np.allclose(np.asarray(sy), [300.0, 300.0, 300.0])


class TestZoom:
    def test_zoom_is_reversible(self) -> None:
        c = cam(1.0)
        assert c.zoomed(4.0).zoomed(0.25).scale == pytest.approx(c.scale)

    def test_zoom_about_a_point_keeps_that_point_fixed(self) -> None:
        for scale in (1e-6, 1.0, 1e6):
            c = cam(scale, 1e9, -2e9)
            anchor = (612.0, 133.0)
            before = c.screen_to_world(*anchor)
            after = c.zoomed_about(3.0, *anchor).screen_to_world(*anchor)
            assert after == pytest.approx(before, rel=1e-9)

    def test_scale_is_clamped_and_says_so(self) -> None:
        c = cam(1.0)
        assert c.zoomed(1e30).is_clamped
        assert c.zoomed(1e-30).is_clamped
        assert not c.zoomed(2.0).is_clamped

    def test_clamping_never_reaches_zero_or_infinity(self) -> None:
        c = cam(1.0)
        assert c.zoomed(1e-300).scale > 0.0
        assert math.isfinite(c.zoomed(1e300).scale)

    def test_zoom_limits_scale_with_the_world(self) -> None:
        """The defect: absolute limits made GROUND unreachable.

        A limit expressed in pixels per world unit means nothing when the world
        is measured in natural units. Two worlds differing by a factor of a
        million must permit the same *fraction* of themselves to be seen.
        """
        small = Camera(0.0, 0.0, 1.0, 800, 600, reference_length=1.0)
        large = Camera(0.0, 0.0, 1.0, 800, 600, reference_length=1e6)
        assert large.max_scale == pytest.approx(small.max_scale * 1e-6)
        deepest_small = small.zoomed(1e30)
        deepest_large = large.zoomed(1e30)
        assert deepest_small.span_ratio == pytest.approx(deepest_large.span_ratio)

    def test_the_deepest_zoom_reaches_the_ground_band(self) -> None:
        c = Camera(0.0, 0.0, 1.0, 800, 600, reference_length=3.84e-5)
        assert c.zoomed(1e30).band is ScaleBand.GROUND

    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_bad_scale_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            cam(bad)

    @pytest.mark.parametrize("bad", [float("nan"), float("inf")])
    def test_bad_focus_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            cam(1.0, bad, 0.0)


class TestScaleBands:
    """Bands are dimensionless ratios of viewport span to circumference.

    Absolute thresholds in metres were the first attempt and were wrong: the
    simulation works in natural units where the orbital radius is about 1, so
    every zoom level fell in a single band. A smoke render across twelve
    decades reported "ground" at every one of them, which is what surfaced it.
    """

    def test_bands_partition_the_range_with_no_gap_or_overlap(self) -> None:
        for ratio in (1e-9, 1e-5, 1e-3, 0.1, 1.0, 10.0, 100.0, 1e9):
            assert isinstance(band_for(ratio), ScaleBand)
        bounds = sorted(BAND_BOUNDS_RATIO.values())
        assert bounds == sorted(set(bounds))

    def test_bands_run_ground_to_system_as_you_zoom_out(self) -> None:
        assert band_for(1e-6) is ScaleBand.GROUND
        assert band_for(1e-2) is ScaleBand.REGIONAL
        assert band_for(2.0) is ScaleBand.PLANETARY
        assert band_for(1e3) is ScaleBand.SYSTEM

    def test_camera_reports_its_band_from_the_world_it_is_looking_at(self) -> None:
        # A viewport 800 px wide, on a world 1e6 units around.
        world = 1e6
        # 800 px at 1e3 px/unit spans 0.8 units: a sliver of a 1e6 world.
        seeing_ground = Camera(0.0, 0.0, 1e3, 800, 600, reference_length=world)
        # 800 px spanning a hundred circumferences.
        seeing_all = Camera(0.0, 0.0, 800.0 / (world * 100.0), 800, 600, reference_length=world)
        assert seeing_ground.band is ScaleBand.GROUND
        assert seeing_all.band is ScaleBand.SYSTEM
        assert seeing_ground.span_ratio < seeing_all.span_ratio

    def test_span_ratio_is_dimensionless_and_scale_free(self) -> None:
        # The same fraction of two worlds of different size is the same band.
        small = Camera(0.0, 0.0, 800.0 / 1.0, 800, 600, reference_length=1.0)
        large = Camera(0.0, 0.0, 800.0 / 1e9, 800, 600, reference_length=1e9)
        assert small.span_ratio == pytest.approx(large.span_ratio)
        assert small.band is large.band

    @pytest.mark.parametrize("bad", [0.0, -1.0])
    def test_non_positive_ratio_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            band_for(bad)

    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_bad_reference_length_raises(self, bad: float) -> None:
        with pytest.raises(ValueError):
            Camera(0.0, 0.0, 1.0, 800, 600, reference_length=bad)


class TestSurfaceCulling:
    """Two binary searches, not a scan. The first law fixes the sort order."""

    def test_matches_brute_force_including_across_the_seam(self) -> None:
        rng = np.random.default_rng(20260905)
        circumference = 3.84e7
        positions = np.sort(rng.uniform(0.0, circumference, 4000))
        for _ in range(60):
            start = float(rng.uniform(0.0, circumference))
            width = float(rng.uniform(1.0, circumference * 0.6))
            end = start + width
            got = set(visible_surface_indices(positions, start, end, circumference).tolist())
            wrapped = np.mod(positions - start, circumference)
            expected = set(np.flatnonzero(wrapped <= width).tolist())
            assert got == expected

    def test_a_full_wrap_returns_everything(self) -> None:
        positions = np.linspace(0.0, 1000.0, 50)
        got = visible_surface_indices(positions, 0.0, 1000.0, 1000.0)
        assert len(got) == 50

    def test_requires_sorted_input(self) -> None:
        with pytest.raises(ValueError):
            visible_surface_indices(np.array([5.0, 1.0, 3.0]), 0.0, 10.0, 100.0)


class TestPurity:
    """Almost all the difficulty lives in the pure modules, so it stays testable.

    Only render.py and app.py may touch a display. If that ever stops being
    true, the viewer stops being testable without one.
    """

    @pytest.mark.parametrize(
        "module", ["camera.py", "bands.py", "geometry.py", "scene.py", "sidebar.py"]
    )
    def test_pure_modules_import_no_pygame(self, module: str) -> None:
        source = Path("sim/view", module).read_text()
        names: set[str] = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
            elif isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
        assert not any("pygame" in name for name in names)
