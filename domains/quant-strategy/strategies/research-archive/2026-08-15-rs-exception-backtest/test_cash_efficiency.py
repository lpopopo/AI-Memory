from pathlib import Path
import runpy
import unittest

import pandas as pd


HERE = Path(__file__).resolve().parent
CASH = runpy.run_path(str(HERE / "evaluate_cash_efficiency.py"))


class CashEfficiencyTests(unittest.TestCase):
    def test_buy_hold_uses_whole_shares_and_two_sided_costs(self):
        prices = pd.Series(
            [100.0, 110.0],
            index=pd.to_datetime(["2026-01-02", "2026-01-05"]),
        )
        metrics = CASH["buy_hold_metrics"](prices, "2026-01-02", "2026-01-05")
        self.assertIsInstance(metrics["shares"], int)
        self.assertGreater(metrics["costs"], 2.0)
        self.assertLess(metrics["total_return"], 0.10)

    def test_fixed_path_cash_overlay_reconstructs_recorded_equity(self):
        dates = pd.to_datetime(["2026-01-02", "2026-01-05"])
        panels = {"close": pd.DataFrame({"AAOI": [100.0, 110.0]}, index=dates)}
        trade = {
            "symbol": "AAOI",
            "entry_date": "2026-01-02",
            "entry_price": 100.0,
            "shares": 1,
            "exit_date": "2026-01-05",
            "exit_price": 110.0,
            "pnl": 8.0,
            "return": 8.0 / 101.0,
            "entry_type": "normal",
        }
        result = {
            "trades": [trade],
            "equity": {"2026-01-02": 5999.0, "2026-01-05": 6008.0},
            "metrics": {"turnover": 210.0 / 6000.0, "costs": 2.0},
        }
        reconstructed = CASH["fixed_path_cash_overlay"](result, panels, None)
        self.assertEqual(reconstructed["equity"].tolist(), [5999.0, 6008.0])


if __name__ == "__main__":
    unittest.main()
