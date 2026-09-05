"""Tests for the periodic gradient noise the terrain is built from.

The periodicity test is the one the lattice modulo exists to guarantee, and
the acceptance criteria require showing it fails when the modulo is removed.
"""

import numpy as np
import pytest

from sim.surface.noise import gradient_noise, mix64


class TestHash:
    def test_is_deterministic_across_calls(self) -> None:
        assert mix64(np.array([1, 2, 3])).tolist() == mix64(np.array([1, 2, 3])).tolist()

    def test_differs_for_neighbouring_inputs(self) -> None:
        # A hash that varies smoothly with its input produces visible lattice
        # structure rather than noise.
        values = mix64(np.arange(64))
        assert len(set(values.tolist())) == 64

    def test_does_not_call_python_hash(self) -> None:
        """Python randomises str/bytes hashing per process.

        A terrain built on it would differ between runs, which would quietly
        break the determinism the whole project rests on. Checked by parsing
        for a call rather than grepping the text, since the module docstring
        legitimately mentions it.
        """
        import ast
        from pathlib import Path

        tree = ast.parse(Path("sim/surface/noise.py").read_text())
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        assert "hash" not in called


class TestGradientNoise:
    @pytest.mark.parametrize("cells", [2, 8, 64])
    def test_is_exactly_periodic(self, cells: int) -> None:
        t = np.linspace(0.0, 1.0, 257)[:-1]
        here = gradient_noise(t, cells=cells, seed=7, octave=3)
        around = gradient_noise(t + 1.0, cells=cells, seed=7, octave=3)
        assert np.allclose(here, around, atol=1e-12)

    @pytest.mark.parametrize("cells", [2, 8, 64])
    def test_is_continuous_across_the_seam(self, cells: int) -> None:
        eps = 1e-9
        before = float(gradient_noise(np.array([1.0 - eps]), cells=cells, seed=7, octave=1)[0])
        after = float(gradient_noise(np.array([0.0]), cells=cells, seed=7, octave=1)[0])
        assert before == pytest.approx(after, abs=1e-6)

    def test_is_zero_at_lattice_points(self) -> None:
        # Gradient noise vanishes on the lattice by construction; a nonzero
        # value there means the interpolation is wrong.
        cells = 16
        t = np.arange(cells) / cells
        assert np.allclose(gradient_noise(t, cells=cells, seed=3, octave=0), 0.0, atol=1e-12)

    def test_is_bounded(self) -> None:
        t = np.linspace(0.0, 1.0, 4001)
        values = gradient_noise(t, cells=32, seed=11, octave=2)
        assert np.all(np.abs(values) <= 1.0)

    def test_different_seeds_give_different_fields(self) -> None:
        t = np.linspace(0.0, 1.0, 501)
        a = gradient_noise(t, cells=16, seed=1, octave=0)
        b = gradient_noise(t, cells=16, seed=2, octave=0)
        assert not np.allclose(a, b)

    def test_different_octaves_give_different_fields(self) -> None:
        t = np.linspace(0.0, 1.0, 501)
        a = gradient_noise(t, cells=16, seed=1, octave=0)
        b = gradient_noise(t, cells=16, seed=1, octave=1)
        assert not np.allclose(a, b)

    def test_is_finite_everywhere(self) -> None:
        t = np.linspace(-3.0, 5.0, 9001)
        assert np.all(np.isfinite(gradient_noise(t, cells=64, seed=5, octave=0)))

    @pytest.mark.parametrize("bad", [0, -4])
    def test_non_positive_cells_raises(self, bad: int) -> None:
        with pytest.raises(ValueError):
            gradient_noise(np.array([0.5]), cells=bad, seed=1, octave=0)
