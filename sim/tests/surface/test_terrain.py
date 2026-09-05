"""Tests for the terrain field itself."""

import numpy as np
import pytest

from sim.surface import Terrain
from sim.units import LENGTH

CIRCUMFERENCE = 3.84e7
AMPLITUDE = 4.0e3
ROUGHNESS = 2.0


def terrain(**kwargs: object) -> Terrain:
    defaults: dict[str, object] = {
        "circumference": CIRCUMFERENCE,
        "amplitude": AMPLITUDE,
        "roughness": ROUGHNESS,
        "seed": 20260905,
        "octaves": 16,
    }
    defaults.update(kwargs)
    return Terrain(**defaults)  # type: ignore[arg-type]


class TestPeriodicity:
    """The property the lattice modulo exists to guarantee."""

    def test_height_repeats_exactly_after_one_circumference(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 513)[:-1]
        t = terrain()
        assert np.allclose(t.height(s), t.height(s + CIRCUMFERENCE), atol=1e-9)

    def test_repeats_after_many_circumferences(self) -> None:
        s = np.array([0.0, 1.0, 12345.678, CIRCUMFERENCE * 0.5])
        t = terrain()
        assert np.allclose(t.height(s), t.height(s + 7.0 * CIRCUMFERENCE), atol=1e-9)

    def test_is_continuous_across_the_seam(self) -> None:
        t = terrain()
        step = 1.0
        before = float(t.height(np.array([CIRCUMFERENCE - step]))[0])
        after = float(t.height(np.array([0.0]))[0])
        # No discontinuity: the difference is bounded by the local slope.
        assert abs(after - before) < AMPLITUDE * 0.05


class TestDeterminism:
    def test_same_seed_is_byte_identical(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 1001)
        assert np.array_equal(terrain().height(s), terrain().height(s))

    def test_different_seeds_differ(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 1001)
        assert not np.allclose(terrain(seed=1).height(s), terrain(seed=2).height(s))


class TestResolutionConsistency:
    def test_a_point_evaluated_alone_matches_the_same_point_in_an_array(self) -> None:
        t = terrain()
        dense = np.linspace(0.0, CIRCUMFERENCE, 4097)
        alone = t.height(np.array([dense[1234]]))[0]
        assert float(alone) == pytest.approx(float(t.height(dense)[1234]), rel=1e-15)

    def test_adding_octaves_adds_detail_without_moving_the_coarse_shape(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 2049)
        coarse = terrain(octaves=6).height(s)
        fine = terrain(octaves=16).height(s)
        # The fine field keeps the coarse structure...
        assert float(np.corrcoef(coarse, fine)[0, 1]) > 0.7
        # ...and has more small-scale variation than the coarse one.
        assert float(np.std(np.diff(fine))) > float(np.std(np.diff(coarse)))

    def test_requesting_a_resolution_selects_octaves(self) -> None:
        t = terrain(octaves=20)
        assert t.octaves_for(CIRCUMFERENCE) < t.octaves_for(1.0)


class TestStatistics:
    """The field must be what it claims, not merely random."""

    def test_rms_height_matches_the_configured_amplitude(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 1 << 15, endpoint=False)
        rms = float(np.sqrt(np.mean(terrain().height(s) ** 2)))
        assert rms == pytest.approx(AMPLITUDE, rel=0.15)

    def test_mean_is_near_zero(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 1 << 15, endpoint=False)
        h = terrain().height(s)
        assert abs(float(np.mean(h))) < 0.2 * float(np.std(h))

    @pytest.mark.parametrize("roughness", [1.5, 2.0, 2.5])
    def test_power_spectrum_slope_matches_the_roughness(self, roughness: float) -> None:
        """What separates fractal terrain from a field that is merely random.

        For P(k) ~ k^-beta the octave amplitudes must fall as 2^(-beta*n/2).
        Uniform amplitudes give a flat spectrum and this test catches it.
        """
        n = 1 << 15
        s = np.linspace(0.0, CIRCUMFERENCE, n, endpoint=False)
        h = terrain(roughness=roughness, octaves=14).height(s)
        power = np.abs(np.fft.rfft(h)) ** 2
        k = np.arange(power.size)
        band = slice(4, 2048)
        slope = np.polyfit(np.log(k[band]), np.log(power[band]), 1)[0]
        assert slope == pytest.approx(-roughness, abs=0.45)

    def test_bounded_by_the_octave_amplitudes(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 20001)
        t = terrain()
        assert np.all(np.abs(t.height(s)) <= t.maximum_height)


class TestResolutionFloor:
    def test_floor_is_circumference_over_two_to_the_octaves(self) -> None:
        t = terrain(octaves=12)
        assert t.resolution_floor == pytest.approx(CIRCUMFERENCE / 2**12)

    def test_requesting_finer_detail_reports_that_it_was_clamped(self) -> None:
        t = terrain(octaves=10)
        assert t.is_clamped_at(t.resolution_floor * 0.01)
        assert not t.is_clamped_at(t.resolution_floor * 100.0)

    def test_finer_requests_return_the_finest_available_not_invented_detail(self) -> None:
        t = terrain(octaves=10)
        s = np.linspace(0.0, CIRCUMFERENCE, 513)
        at_floor = t.height(s, resolution=t.resolution_floor)
        below_floor = t.height(s, resolution=t.resolution_floor * 1e-6)
        assert np.array_equal(at_floor, below_floor)


class TestResidual:
    def test_adding_a_residual_shifts_height_by_exactly_the_residual(self) -> None:
        residual = np.zeros(64)
        residual[16] = 250.0
        base = terrain()
        with_residual = terrain(residual=residual)
        at_sample = CIRCUMFERENCE * 16.0 / 64.0
        s = np.array([at_sample])
        assert float(with_residual.height(s)[0] - base.height(s)[0]) == pytest.approx(250.0)

    def test_residual_interpolates_periodically_across_the_seam(self) -> None:
        residual = np.zeros(8)
        residual[0] = 100.0
        t = terrain(residual=residual)
        base = terrain()
        just_before = np.array([CIRCUMFERENCE - CIRCUMFERENCE / 16.0])
        lift = float(t.height(just_before)[0] - base.height(just_before)[0])
        # Halfway between the last sample (0) and the wrapped first (100).
        assert lift == pytest.approx(50.0, rel=1e-6)

    def test_no_residual_costs_nothing_and_changes_nothing(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 1001)
        assert np.array_equal(terrain(residual=None).height(s), terrain().height(s))

    def test_non_finite_residual_raises_at_construction(self) -> None:
        with pytest.raises(ValueError):
            terrain(residual=np.array([0.0, np.nan, 1.0]))

    def test_empty_residual_raises(self) -> None:
        with pytest.raises(ValueError):
            terrain(residual=np.array([]))


class TestValidation:
    @pytest.mark.parametrize("field", ["circumference", "amplitude"])
    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_bad_positive_parameters_raise(self, field: str, bad: float) -> None:
        with pytest.raises(ValueError):
            terrain(**{field: bad})

    @pytest.mark.parametrize("bad", [0, -3])
    def test_bad_octave_count_raises(self, bad: int) -> None:
        with pytest.raises(ValueError):
            terrain(octaves=bad)

    def test_non_positive_resolution_raises(self) -> None:
        with pytest.raises(ValueError):
            terrain().height(np.array([0.0]), resolution=0.0)

    def test_heights_are_finite_over_a_dense_sweep(self) -> None:
        s = np.linspace(0.0, CIRCUMFERENCE, 50_001)
        assert np.all(np.isfinite(terrain().height(s)))

    def test_height_is_a_length(self) -> None:
        q = terrain().height_quantity(np.array([0.0, 1e6]))
        assert q.dimension == LENGTH


class TestScalarAndArray:
    def test_accepts_a_scalar(self) -> None:
        assert isinstance(float(terrain().height(1234.0)), float)

    def test_scalar_matches_array_of_one(self) -> None:
        t = terrain()
        assert float(t.height(1234.0)) == pytest.approx(float(t.height(np.array([1234.0]))[0]))
