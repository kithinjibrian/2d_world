"""Basins on a closed curve.

Three of these are theorems rather than observations, so a failure is a bug in
the code and not a fact about the world.
"""

import numpy as np
import pytest

from sim.surface import Terrain
from sim.water import analyse

PROFILE = np.array([0.0, 2.0, 1.0, 3.0, 0.5, 2.5, 1.5, 2.2])


def terrain(octaves: int = 16) -> Terrain:
    c = 3.84e-5
    return Terrain(circumference=c, amplitude=c * 8e-4, roughness=2.0, seed=5, octaves=octaves)


def sampled(n: int) -> np.ndarray:
    t = terrain()
    s = np.linspace(0.0, t.circumference, n, endpoint=False)
    return np.asarray(t.height(s, resolution=t.circumference / n))


class TestTheoremsOfOneDimension:
    """Failures here are bugs, not findings."""

    def test_every_catchment_is_a_contiguous_arc(self) -> None:
        """In three dimensions a drainage basin can be any shape. Here it is
        an interval, and that is what "rivers cannot branch" means."""
        for heights in (PROFILE, sampled(2048)):
            basins = analyse(heights)
            for index in range(len(basins)):
                members = np.flatnonzero(basins.catchment == index)
                # Contiguous once rotated so the arc does not straddle the seam.
                gaps = np.diff(np.sort(members))
                wrapped = int((gaps > 1).sum())
                assert wrapped <= 1, f"basin {index} drains a broken set of arcs"

    def test_every_sample_drains_somewhere(self) -> None:
        for heights in (PROFILE, sampled(1024)):
            basins = analyse(heights)
            assert basins.catchment.min() >= 0
            assert basins.catchment.max() < len(basins)
            assert basins.catchment.size == heights.size

    def test_catchments_partition_the_world(self) -> None:
        basins = analyse(sampled(1024))
        counts = np.bincount(basins.catchment, minlength=len(basins))
        assert counts.sum() == 1024
        assert np.all(counts > 0)

    def test_the_catchment_map_agrees_with_walking_downhill(self) -> None:
        """The real check: descend from every sample and see where you land.

        Divides are excluded and asserted to be the *only* exceptions. A local
        maximum sits between two catchments and drains both ways, so whichever
        side it is assigned to is arbitrary — but nothing else may disagree.
        """
        heights = sampled(512)
        basins = analyse(heights)
        n = heights.size
        floors = {b.floor_index: i for i, b in enumerate(basins.basins)}
        left_n, right_n = np.roll(heights, 1), np.roll(heights, -1)
        divides = set(np.flatnonzero((heights > left_n) & (heights >= right_n)).tolist())

        disagreements = []
        for start in range(n):
            here = start
            for _ in range(n):
                if here in floors:
                    break
                left, right = (here - 1) % n, (here + 1) % n
                nxt = left if heights[left] < heights[right] else right
                if heights[nxt] >= heights[here]:
                    break
                here = nxt
            if here in floors and basins.catchment[start] != floors[here]:
                disagreements.append(start)

        assert disagreements, "expected divides to be ambiguous; none were"
        assert set(disagreements) <= divides, (
            f"{len(set(disagreements) - divides)} non-divide samples are mapped to a basin "
            "they do not drain into"
        )

    def test_each_basin_has_exactly_one_outlet(self) -> None:
        basins = analyse(PROFILE)
        for basin in basins.basins:
            assert basin.lip > basin.floor
            assert basin.depth_to_lip > 0.0

    def test_the_number_of_minima_and_maxima_agree(self) -> None:
        # On a closed curve they must alternate, so there are equally many.
        heights = sampled(4096)
        left, right = np.roll(heights, 1), np.roll(heights, -1)
        minima = int(((heights < left) & (heights <= right)).sum())
        maxima = int(((heights > left) & (heights >= right)).sum())
        assert minima == maxima


class TestCountingNeedsAThreshold:
    """The finding that shaped this layer.

    Terrain is fractal, so counting local minima measures the sampling rather
    than the world. Persistence does not.
    """

    def test_raw_minima_multiply_as_the_grid_is_refined(self) -> None:
        counts = []
        for n in (512, 2048, 8192):
            heights = sampled(n)
            left, right = np.roll(heights, 1), np.roll(heights, -1)
            counts.append(int(((heights < left) & (heights <= right)).sum()))
        # Each refinement finds far more, without limit.
        assert counts[1] > 2 * counts[0]
        assert counts[2] > 2 * counts[1]

    def test_deep_basins_grow_far_more_slowly(self) -> None:
        """Persistence is much more stable than counting minima — but not stable.

        Measured over a 64-fold refinement of the same terrain: raw minima grow
        with an exponent of 1.00, meaning they multiply without limit and
        measure only the grid. Deep basins grow with an exponent of about 0.28.

        That is the honest statement, and it is weaker than "persistence is
        sampling-independent". For terrain that is fractal at every scale there
        is **no** sampling-independent basin count, because there are genuinely
        basins at every scale. Persistence makes the count converge far more
        slowly; it does not make it converge. So a count must always be
        reported with both its threshold and its resolution.
        """
        sizes = (512, 32768)
        raw, deep = [], []
        for n in sizes:
            heights = sampled(n)
            left, right = np.roll(heights, 1), np.roll(heights, -1)
            raw.append(int(((heights < left) & (heights <= right)).sum()))
            deep.append(len(analyse(heights).deeper_than(0.25 * float(heights.std()))))

        raw_growth = raw[1] / raw[0]
        deep_growth = deep[1] / deep[0]
        assert raw_growth > 30.0, "raw minima should multiply roughly with the sampling"
        assert deep_growth < 6.0, "deep basins should be far more stable than that"
        assert deep_growth < raw_growth / 5.0

    def test_a_count_without_a_threshold_is_refused(self) -> None:
        basins = analyse(PROFILE)
        with pytest.raises(ValueError, match="persistence"):
            basins.deeper_than(0.0)
        with pytest.raises(ValueError):
            basins.deeper_than(-1.0)

    def test_deeper_thresholds_admit_fewer_basins(self) -> None:
        basins = analyse(sampled(4096))
        amplitude = terrain().amplitude
        counts = [len(basins.deeper_than(amplitude * f)) for f in (0.01, 0.05, 0.1, 0.25, 0.5)]
        assert counts == sorted(counts, reverse=True)


class TestPersistenceValues:
    def test_matches_a_hand_worked_profile(self) -> None:
        """Checked by hand against the merge tree, minimum by minimum."""
        expected = {0: 3.0, 2: 1.0, 4: 2.0, 6: 0.7}
        for basin in analyse(PROFILE).basins:
            assert basin.persistence == pytest.approx(expected[basin.floor_index])

    def test_equal_floors_do_not_confuse_it(self) -> None:
        # Identifying a dying basin by height rather than index picks the wrong
        # one whenever two floors are equal. This is that case.
        heights = np.array([0.0, 2.0, 0.0, 3.0, 0.0, 2.5])
        values = sorted(b.persistence for b in analyse(heights).basins)
        assert values == pytest.approx([2.0, 2.5, 3.0])

    def test_the_deepest_basin_never_dies(self) -> None:
        basins = analyse(PROFILE)
        deepest = min(basins.basins, key=lambda b: b.floor)
        assert deepest.persistence == pytest.approx(PROFILE.max() - PROFILE.min())


class TestValidation:
    @pytest.mark.parametrize("heights", [np.array([1.0]), np.array([1.0, 2.0])])
    def test_too_few_samples_raises(self, heights: np.ndarray) -> None:
        with pytest.raises(ValueError):
            analyse(heights)

    def test_non_finite_heights_raise(self) -> None:
        with pytest.raises(ValueError):
            analyse(np.array([0.0, np.nan, 1.0, 2.0]))

    def test_a_flat_world_has_no_basins(self) -> None:
        with pytest.raises(ValueError, match="extrema"):
            analyse(np.zeros(16))
