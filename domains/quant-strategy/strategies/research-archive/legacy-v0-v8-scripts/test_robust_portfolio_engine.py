import unittest
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robust_portfolio_engine import drift_weights, run_engine
from optimize_v8_robust import metrics
from v8_signal import target_from_close


class RobustPortfolioEngineTest(unittest.TestCase):
    def test_weights_drift_instead_of_free_daily_rebalance(self):
        factor, weights = drift_weights(
            {"A": 0.5, "B": 0.5}, pd.Series({"A": 0.10, "B": 0.0})
        )
        self.assertAlmostEqual(factor, 1.05)
        self.assertAlmostEqual(weights["A"], 0.55 / 1.05)
        self.assertAlmostEqual(weights["B"], 0.50 / 1.05)

    def test_close_signal_executes_next_close(self):
        dates = pd.date_range("2025-01-01", periods=4, freq="B")
        close = pd.DataFrame({"A": [100, 110, 121, 133.1]}, index=dates)
        result = run_engine(close, {dates[0]}, lambda _: {"A": 1.0}, transaction_cost=0)
        # No exposure to the first +10%; target executes at day 2 close.
        self.assertAlmostEqual(result.equity.iloc[1], 1.0)
        self.assertAlmostEqual(result.equity.iloc[2], 1.1)
        self.assertEqual(pd.Timestamp(result.executions.iloc[0]["date"]), dates[1])

    def test_stop_breach_executes_on_following_close(self):
        dates = pd.date_range("2025-01-01", periods=6, freq="B")
        close = pd.DataFrame({"A": [100, 100, 120, 105, 90, 90]}, index=dates)
        result = run_engine(
            close, {dates[0]}, lambda _: {"A": 1.0}, transaction_cost=0,
            stop_loss_pct=0.10,
        )
        # 105 breaches 10% from the 120 high at day 4 close; liquidation is day 5 close.
        self.assertGreater(result.weights.at[dates[3], "A"], 0)
        self.assertEqual(result.weights.at[dates[4], "A"], 0)
        self.assertAlmostEqual(result.equity.iloc[4], 0.9)

    def test_transaction_cost_charged_on_both_target_changes(self):
        dates = pd.date_range("2025-01-01", periods=5, freq="B")
        close = pd.DataFrame({"A": [100] * 5}, index=dates)
        targets = {dates[0]: {"A": 1.0}, dates[2]: {}}
        result = run_engine(close, set(targets), lambda dt: targets[dt], transaction_cost=0.001)
        self.assertAlmostEqual(result.equity.iloc[-1], 0.999 * 0.999)
        self.assertAlmostEqual(result.diagnostics["total_turnover"], 2.0)

    def test_split_metrics_rebase_existing_equity(self):
        dates = pd.date_range("2025-01-01", periods=253, freq="B")
        # A curve segment may begin at an arbitrary accumulated NAV. It still
        # represents exactly +10% over this one-year slice.
        curve = pd.Series([2.0 + 0.2 * i / 252 for i in range(253)], index=dates)
        result = metrics(curve)
        self.assertAlmostEqual(result["final_value"], 1.10, places=6)
        self.assertGreater(result["cagr"], 0.09)
        self.assertLess(result["cagr"], 0.11)

    def test_v8_two_vote_target(self):
        dates = pd.date_range("2024-01-01", periods=200, freq="B")
        close = pd.DataFrame({
            "SPY": range(100, 300),
            "QQQ": list(range(300, 100, -1)),
        }, index=dates)
        result = target_from_close(close)
        self.assertEqual(result["symbols"]["SPY"]["trend_votes"], 2)
        self.assertEqual(result["symbols"]["SPY"]["target_weight"], 0.5)
        self.assertEqual(result["symbols"]["QQQ"]["trend_votes"], 0)
        self.assertEqual(result["target_cash_weight"], 0.5)


if __name__ == "__main__":
    unittest.main()
