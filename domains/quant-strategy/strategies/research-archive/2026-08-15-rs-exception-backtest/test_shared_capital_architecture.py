import importlib.util
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "shared_capital", HERE / "evaluate_shared_capital_architecture.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SharedCapitalArchitectureTests(unittest.TestCase):
    def test_desired_whole_shares_rounds_down_and_reserves_fee(self):
        shares = MODULE.desired_whole_shares(6000.0, 0.35, 700.0)
        self.assertEqual(shares, 2)
        self.assertLessEqual(shares * 700.0 * 1.001 + 1.0, 6000.0 * 0.35)

    def test_combined_metrics_uses_supplied_initial_nav(self):
        index = pd.bdate_range("2026-01-02", periods=30)
        curve = pd.Series([5751.77 + i for i in range(30)], index=index)
        metrics = MODULE.combined_metrics(curve, 5751.77)
        self.assertAlmostEqual(metrics["final_value"], 5780.77)
        self.assertGreater(metrics["total_return"], 0.0)
        self.assertEqual(metrics["max_drawdown"], 0.0)

    def test_screen_requires_every_nav_and_period(self):
        rows = []
        for nav in MODULE.NAVS:
            for period in MODULE.PERIODS:
                for architecture in MODULE.ARCHITECTURES:
                    challenger = architecture == "challenger_80_20"
                    rows.append(
                        {
                            "initial_nav": nav,
                            "period": period,
                            "architecture": architecture,
                            "total_return": 0.12 if challenger else 0.10,
                            "max_drawdown": -0.11 if challenger else -0.10,
                            "sharpe": 1.0,
                            "monthly_win_rate": 0.60,
                            "average_core_exposure": 0.60 if challenger else 0.50,
                            "closed_stock_trades": 4,
                            "stock_win_rate": 0.75,
                            "max_gross_exposure": 0.95,
                            "minimum_cash": 10.0,
                            "ledger_reconciles": True,
                        }
                    )
        metrics = pd.DataFrame(rows)
        screen, passes = MODULE.challenger_screen(metrics)
        self.assertTrue(passes)
        self.assertTrue(screen["passes"].all())
        metrics.loc[
            (metrics["initial_nav"] == MODULE.NAVS[0])
            & (metrics["period"] == "heldout_2026")
            & (metrics["architecture"] == "challenger_80_20"),
            "total_return",
        ] = 0.0
        _, passes = MODULE.challenger_screen(metrics)
        self.assertFalse(passes)


if __name__ == "__main__":
    unittest.main()
