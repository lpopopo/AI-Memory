import json
import unittest

import numpy as np
import pandas as pd

import evaluate_pit_exact_filter as target


class PitExactFilterTests(unittest.TestCase):
    def test_membership_mask_is_opt_in_inclusive_opt_out_exclusive(self):
        dates = pd.date_range("2020-01-01", periods=4, freq="D")
        membership = pd.DataFrame(
            {
                "symbol": ["ABC"],
                "opt-in": [pd.Timestamp("2020-01-02")],
                "opt-out": [pd.Timestamp("2020-01-04")],
            }
        )
        result = target.membership_mask(membership, dates, ["ABC"])
        self.assertEqual(result["ABC"].tolist(), [False, True, True, False])

    def test_trade_statistics_reports_economic_not_just_hit_rate_metrics(self):
        trades = pd.DataFrame(
            {
                "return": [0.10, 0.05, -0.02],
                "pnl": [100.0, 50.0, -20.0],
            }
        )
        result = target.trade_statistics(trades)
        self.assertAlmostEqual(result["win_rate"], 2 / 3)
        self.assertAlmostEqual(result["profit_factor"], 7.5)
        self.assertAlmostEqual(result["payoff_ratio"], 3.75)
        self.assertAlmostEqual(result["breakeven_win_rate"], 1 / 4.75)

    def test_screen_requires_both_registered_out_of_sample_periods(self):
        rows = []
        for period in ("validation_2020_2022", "final_2023_2025"):
            rows.extend(
                [
                    {
                        "period": period,
                        "variant": "matched_baseline",
                        "trade_count": 30,
                        "total_return": 0.05,
                        "sharpe": 0.5,
                        "max_drawdown": -0.10,
                        "win_rate": 0.50,
                        "mean_trade_return": 0.01,
                    },
                    {
                        "period": period,
                        "variant": "combined_4pct_50pct",
                        "trade_count": 25,
                        "total_return": 0.06,
                        "sharpe": 0.6,
                        "max_drawdown": -0.08,
                        "win_rate": 0.55,
                        "mean_trade_return": 0.02,
                    },
                ]
            )
        metrics = pd.DataFrame(rows)
        passed, rows = target.screen(
            metrics,
            {"validation_2020_2022": 0.90, "final_2023_2025": 0.90},
        )
        self.assertTrue(passed)
        json.dumps({"passed": passed, "rows": rows})
        metrics.loc[
            (metrics["period"] == "final_2023_2025")
            & (metrics["variant"] == "combined_4pct_50pct"),
            "sharpe",
        ] = 0.4
        passed, _ = target.screen(
            metrics,
            {"validation_2020_2022": 0.90, "final_2023_2025": 0.90},
        )
        self.assertFalse(passed)

    def test_nonliquidating_period_does_not_fabricate_terminal_trade(self):
        panels, membership, stocks = target.load_inputs()
        members = target.membership_mask(membership, panels["close"].index, stocks)
        features = target.build_features(panels, stocks, members)
        _, trades = target.simulate_period(
            panels,
            features,
            stocks,
            "matched_baseline",
            pd.Timestamp("2023-01-01"),
            pd.Timestamp("2025-12-31"),
            liquidate_final=False,
        )
        self.assertFalse(trades["exit_reason"].eq("terminal").any())
        self.assertTrue(trades["exit_date"].isna().any())


if __name__ == "__main__":
    unittest.main()
