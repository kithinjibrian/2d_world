"""Wrapping on a closed curve — the shared implementation.

Both traps recorded here as regressions, because each shipped once.
"""

import numpy as np
import pytest

from sim.periodic import distance, separation, wrap

PERIOD = 3.84e7


class TestRange:
    @pytest.mark.parametrize("value", [0.0, 1e-9, -1e-9, 1.0, -1.0, PERIOD, -PERIOD, 7.3 * PERIOD])
    def test_result_is_always_in_range(self, value: float) -> None:
        assert 0.0 <= float(wrap(value, PERIOD)) < PERIOD

    def test_the_wrap_point_folds_to_zero(self) -> None:
        # `%` returns exactly the period for a tiny negative, because
        # period - value rounds up. That is outside [0, period).
        assert wrap(-1e-9, PERIOD) == 0.0
        assert wrap(PERIOD, PERIOD) == 0.0


class TestPrecision:
    def test_small_positive_values_are_not_quantised(self) -> None:
        # fmod(fmod(a,b)+b, b) loses 0.16% of a micron here, because adding the
        # period quantises at the period's ulp of 7.45 nanometres.
        assert wrap(1e-6, PERIOD) == 1e-6
        assert wrap(1e-9, PERIOD) == 1e-9

    def test_negatives_land_where_they_should(self) -> None:
        assert wrap(-1.0, PERIOD) == pytest.approx(PERIOD - 1.0)


class TestArrays:
    def test_wraps_elementwise(self) -> None:
        got = np.asarray(wrap(np.array([-1e-9, 0.0, 1.0, PERIOD, 2.5 * PERIOD]), PERIOD))
        assert np.all(got >= 0.0)
        assert np.all(got < PERIOD)

    def test_matches_the_scalar_path(self) -> None:
        values = [-1e-9, 1e-6, 1.0, -1.0, 3.3 * PERIOD]
        array = np.asarray(wrap(np.array(values), PERIOD))
        assert np.allclose(array, [float(wrap(v, PERIOD)) for v in values], rtol=0, atol=0)


class TestSeparationOnAClosedCurve:
    """Two points always have two routes between them. Take the shorter."""

    def test_the_short_way_round_is_taken(self) -> None:
        assert distance(0.0, 9.0, 10.0) == pytest.approx(1.0)
        assert separation(0.0, 9.0, 10.0) == pytest.approx(-1.0)

    def test_nothing_is_further_away_than_the_antipode(self) -> None:
        for b in np.linspace(0.0, 3.0 * PERIOD, 97):
            assert float(distance(0.0, b, PERIOD)) <= PERIOD * 0.5 + 1e-9

    def test_a_point_one_ulp_short_of_a_full_turn_is_where_it_started(self) -> None:
        """The failure that motivated this function.

        After exactly one sidereal day the phase lands 8.9e-16 short of a full
        turn, so the substellar point comes back as ``circumference - 1e-21``.
        Subtracting says it moved the whole way round; the circular distance
        says it did not move at all.
        """
        almost = PERIOD * (1.0 - 1e-16)
        assert abs(almost - 0.0) == pytest.approx(PERIOD, rel=1e-9)   # naive
        assert float(distance(almost, 0.0, PERIOD)) < 1e-6            # correct

    def test_is_symmetric_and_antisymmetric(self) -> None:
        a, b = 3.7, PERIOD - 2.1
        assert float(distance(a, b, PERIOD)) == pytest.approx(float(distance(b, a, PERIOD)))
        assert float(separation(a, b, PERIOD)) == pytest.approx(-float(separation(b, a, PERIOD)))

    def test_works_on_arrays(self) -> None:
        got = np.asarray(distance(np.array([0.0, 1.0]), np.array([PERIOD, PERIOD - 1.0]), PERIOD))
        assert np.allclose(got, [0.0, 2.0])
