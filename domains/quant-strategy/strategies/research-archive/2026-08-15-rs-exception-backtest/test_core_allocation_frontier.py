import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "core_allocation_frontier", HERE / "evaluate_core_allocation_frontier.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CoreAllocationFrontierTests(unittest.TestCase):
    def test_long_cache_reconstructs_v9_panel_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.csv"
            frame = pd.DataFrame(
                {
                    "date": pd.bdate_range("2020-01-02", periods=2),
                    **{
                        f"{symbol}_{field}": [1.0, 2.0]
                        for symbol in ("SPY", "QQQ")
                        for field in ("open", "high", "low", "close", "volume")
                    },
                    "VIX_close": [15.0, float("nan")],
                    "VIX3M_close": [17.0, float("nan")],
                }
            )
            frame.to_csv(path, index=False)
            original = MODULE.LONG_CACHE
            try:
                MODULE.LONG_CACHE = path
                panels, vix = MODULE._read_long_cache()
            finally:
                MODULE.LONG_CACHE = original
            self.assertEqual(list(panels["close"].columns), ["SPY", "QQQ"])
            self.assertEqual(list(vix.columns), ["^VIX", "^VIX3M"])
            self.assertEqual(len(panels["close"]), 2)
            self.assertEqual(float(vix.iloc[-1]["^VIX"]), 15.0)
            self.assertEqual(float(vix.iloc[-1]["^VIX3M"]), 17.0)

    def test_curve_metrics_reports_win_and_drawdown(self):
        index = pd.bdate_range("2024-01-02", periods=300)
        curve = pd.Series([100.0 + i * 0.1 for i in range(300)], index=index)
        metrics = MODULE.curve_metrics(curve)
        self.assertGreater(metrics["total_return"], 0)
        self.assertEqual(metrics["max_drawdown"], 0.0)
        self.assertEqual(metrics["monthly_win_rate"], 1.0)

    def test_rolling_metrics_uses_frozen_window_size(self):
        index = pd.bdate_range("2010-01-04", periods=800)
        curve = pd.Series([100.0 + i * 0.05 for i in range(800)], index=index)
        rows = MODULE.rolling_metrics(curve)
        self.assertFalse(rows.empty)
        self.assertEqual(rows.iloc[0]["start"], index[0])
        self.assertEqual(rows.iloc[0]["end"], index[MODULE.ROLLING_SESSIONS - 1])

    def test_screen_selects_only_candidate_passing_every_gate(self):
        rows = []
        periods = list(MODULE.SCREEN_PERIODS) + ["full_2006_2025"]
        for period in periods:
            for cap in MODULE.CAPS:
                excess = cap - MODULE.REFERENCE_CAP
                rows.append(
                    {
                        "period": period,
                        "core_cap": cap,
                        "total_return": 0.10 + excess,
                        "max_drawdown": -0.10 - max(excess, 0) * 0.10,
                        "sharpe": 1.0,
                        "monthly_win_rate": 0.60,
                    }
                )
        metrics = pd.DataFrame(rows)
        rolling = pd.DataFrame(
            {
                "core_cap": MODULE.CAPS,
                "rolling_positive_return_rate": [0.8] * len(MODULE.CAPS),
            }
        )
        screen = MODULE.balanced_challenger_screen(metrics, rolling)
        self.assertTrue(screen["passes_balanced_challenger_screen"].all())
        bad = metrics.copy()
        bad.loc[
            (bad["period"] == "heldout_2026") & (bad["core_cap"] == 0.80),
            "total_return",
        ] = 0.0
        failed = MODULE.balanced_challenger_screen(bad, rolling).set_index("core_cap")
        self.assertFalse(bool(failed.at[0.80, "passes_balanced_challenger_screen"]))


if __name__ == "__main__":
    unittest.main()
