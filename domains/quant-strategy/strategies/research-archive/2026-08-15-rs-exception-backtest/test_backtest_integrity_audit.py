import unittest

import pandas as pd

import evaluate_backtest_integrity_audit as target


class BacktestIntegrityAuditTests(unittest.TestCase):
    def test_panel_invariants_detects_economic_ohlc_error(self):
        index = pd.to_datetime(["2026-01-02"])
        panels = {
            "open": pd.DataFrame({"ABC": [10.0]}, index=index),
            "high": pd.DataFrame({"ABC": [9.0]}, index=index),
            "low": pd.DataFrame({"ABC": [8.0]}, index=index),
            "close": pd.DataFrame({"ABC": [9.5]}, index=index),
            "volume": pd.DataFrame({"ABC": [100.0]}, index=index),
        }
        result = target.panel_invariants(panels)
        self.assertEqual(result["invalid_high_bars"], 1)
        self.assertEqual(len(result["invalid_ohlc_records"]), 1)

    def test_cash_replay_orders_same_day_stop_after_entry(self):
        trades = [
            {
                "entry_date": "2026-01-02",
                "entry_price": 100.0,
                "shares": 2,
                "partial_exit_shares": 0,
                "exit_date": "2026-01-02",
                "exit_price": 90.0,
                "exit_reason": "stop",
            }
        ]
        result = target.cash_replay(trades, 1_000.0)
        self.assertAlmostEqual(result["minimum_cash"], 799.0)
        self.assertAlmostEqual(result["ending_cash_for_closed_and_open_path"], 978.0)

    def test_maximum_concurrent_excludes_opening_exit_from_exit_day(self):
        dates = pd.to_datetime(["2026-01-02", "2026-01-05"])
        trades = [
            {"entry_date": "2026-01-02", "exit_date": "2026-01-05"},
            {"entry_date": "2026-01-05", "exit_date": None},
        ]
        self.assertEqual(target.maximum_concurrent(trades, dates), 1)


if __name__ == "__main__":
    unittest.main()
