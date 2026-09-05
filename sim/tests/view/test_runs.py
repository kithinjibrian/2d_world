"""Splitting a mask into contiguous runs.

This existed inline in `TerrainTrace.draw` as index juggling, and it shipped a
crash: when the last sample flipped, the trailing run held a single point and
`pygame.draw.aalines` refuses fewer than two. Extracted so it can be tested at
all — the inline version could only be exercised by rendering, and rendering
happened to never produce a terminator on the final sample.
"""

from itertools import pairwise

import numpy as np
import pytest

from sim.view.geometry import contiguous_runs


def mask(text: str) -> np.ndarray:
    return np.array([c == "D" for c in text], dtype=bool)


class TestRuns:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("DDDDD", [(0, 5, True)]),
            ("nnnnn", [(0, 5, False)]),
            ("DDnnn", [(0, 2, True), (2, 5, False)]),
            ("DDDDn", [(0, 4, True), (4, 5, False)]),
            ("nDDDD", [(0, 1, False), (1, 5, True)]),
            ("DnDnD", [(0, 1, True), (1, 2, False), (2, 3, True), (3, 4, False), (4, 5, True)]),
            ("D", [(0, 1, True)]),
        ],
    )
    def test_segments_correctly(self, text: str, expected: list[tuple[int, int, bool]]) -> None:
        assert contiguous_runs(mask(text)) == expected

    def test_an_empty_mask_has_no_runs(self) -> None:
        assert contiguous_runs(np.array([], dtype=bool)) == []

    def test_runs_tile_the_mask_without_gap_or_overlap(self) -> None:
        rng = np.random.default_rng(20260906)
        for _ in range(200):
            values = rng.random(int(rng.integers(1, 40))) > 0.5
            runs = contiguous_runs(values)
            assert runs[0][0] == 0
            assert runs[-1][1] == len(values)
            for (_, stop, _), (next_start, _, _) in pairwise(runs):
                assert stop == next_start

    def test_neighbouring_runs_always_differ(self) -> None:
        rng = np.random.default_rng(7)
        for _ in range(200):
            values = rng.random(int(rng.integers(1, 40))) > 0.5
            runs = contiguous_runs(values)
            for (_, _, a), (_, _, b) in pairwise(runs):
                assert a != b

    def test_every_run_reports_the_value_it_covers(self) -> None:
        values = mask("DDnnnDn")
        for start, stop, value in contiguous_runs(values):
            assert bool(values[start:stop].all()) == value
            assert bool((~values[start:stop]).all()) != value


class TestTheCrashItPrevents:
    """A single-sample trailing run is the exact case that crashed."""

    def test_a_flip_on_the_last_sample_yields_a_one_element_run(self) -> None:
        runs = contiguous_runs(mask("DDDDn"))
        assert runs[-1] == (4, 5, False)
        assert runs[-1][1] - runs[-1][0] == 1

    def test_an_alternating_mask_is_all_single_element_runs(self) -> None:
        assert all(stop - start == 1 for start, stop, _ in contiguous_runs(mask("DnDnD")))
