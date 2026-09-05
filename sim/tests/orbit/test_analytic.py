"""The screening path: closed forms for the near-circular limit.

Architecture rule 8 requires a cheap path alongside the full solve. Here it is
nearly free, because every near-circular result has a closed form.
"""

import ast
import math
from pathlib import Path

import pytest

from sim.orbit import (
    APSIDAL_ANGLE_NEAR_CIRCULAR,
    APSIDAL_REGRESSION_PER_ORBIT,
    SEASON_CYCLE_ORBITS,
    circular_period,
    circular_speed,
)
from sim.units import LENGTH, MASS, TIME, VELOCITY, Quantity


class TestCircularSpeedIsIndependentOfRadius:
    """v_c = sqrt(G2*M), the same at every distance.

    A logarithmic potential gives r*dPhi/dr = G2*M, with no r left in it. This
    is the two-dimensional analogue of a flat galactic rotation curve.
    """

    def test_speed_does_not_depend_on_radius(self) -> None:
        star = Quantity(1.0, MASS)
        speeds = [
            circular_speed(star, Quantity(r, LENGTH)).scalar(VELOCITY)
            for r in (0.5, 1.0, 4.0, 50.0, 1000.0)
        ]
        assert all(s == pytest.approx(speeds[0], rel=1e-15) for s in speeds)

    def test_speed_is_root_g2_m(self) -> None:
        for mass in (1.0, 4.0, 100.0):
            speed = circular_speed(Quantity(mass, MASS), Quantity(3.0, LENGTH))
            assert speed.scalar(VELOCITY) == pytest.approx(math.sqrt(mass))


class TestPeriodIsLinearInRadius:
    """Kepler's third law is replaced by T proportional to r, not r^(3/2)."""

    def test_fitted_exponent_is_one(self) -> None:
        star = Quantity(1.0, MASS)
        radii = [1.0, 2.0, 4.0, 8.0, 16.0]
        periods = [
            circular_period(star, Quantity(r, LENGTH)).scalar(TIME) for r in radii
        ]
        exponent = _log_log_slope(radii, periods)
        assert exponent == pytest.approx(1.0, abs=1e-12)

    def test_fitted_exponent_is_not_the_three_dimensional_three_halves(self) -> None:
        star = Quantity(1.0, MASS)
        radii = [1.0, 2.0, 4.0, 8.0]
        periods = [
            circular_period(star, Quantity(r, LENGTH)).scalar(TIME) for r in radii
        ]
        assert _log_log_slope(radii, periods) != pytest.approx(1.5, abs=0.1)

    def test_period_matches_two_pi_r_over_v(self) -> None:
        star, radius = Quantity(1.0, MASS), Quantity(7.0, LENGTH)
        expected = 2.0 * math.pi * 7.0 / circular_speed(star, radius).scalar(VELOCITY)
        assert circular_period(star, radius).scalar(TIME) == pytest.approx(expected)


class TestClosedForms:
    def test_apsidal_angle_is_pi_over_root_two(self) -> None:
        assert pytest.approx(math.pi / math.sqrt(2.0)) == APSIDAL_ANGLE_NEAR_CIRCULAR
        assert math.degrees(APSIDAL_ANGLE_NEAR_CIRCULAR) == pytest.approx(127.2792, abs=1e-4)

    def test_regression_per_orbit(self) -> None:
        assert math.degrees(APSIDAL_REGRESSION_PER_ORBIT) == pytest.approx(105.4416, abs=1e-4)

    def test_season_cycle_is_two_plus_root_two(self) -> None:
        # 360 / (360 - 180*sqrt(2)) = 2 + sqrt(2), exactly.
        assert pytest.approx(2.0 + math.sqrt(2.0), rel=1e-15) == SEASON_CYCLE_ORBITS
        assert pytest.approx(3.414214, abs=1e-6) == SEASON_CYCLE_ORBITS

    def test_season_cycle_follows_from_the_regression(self) -> None:
        assert pytest.approx(
            2.0 * math.pi / APSIDAL_REGRESSION_PER_ORBIT, rel=1e-12
        ) == SEASON_CYCLE_ORBITS


class TestScreeningPathDoesNotIntegrate:
    """A screening path that secretly integrates is not a screening path.

    Asserted structurally rather than by timing, so it cannot flake.
    """

    def test_analytic_module_does_not_import_the_integrator(self) -> None:
        source = Path("sim/orbit/analytic.py").read_text()
        imported: set[str] = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
        assert not any("integrator" in name for name in imported)


def _log_log_slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx, my = sum(lx) / n, sum(ly) / n
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly, strict=True))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den
