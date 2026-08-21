#!/usr/bin/env python3
from __future__ import annotations

import unittest

import pandas as pd

from evaluate_v9_core_whipsaw import confirmed_daily_targets, paired_screen


class V9CoreWhipsawTests(unittest.TestCase):
    def setUp(self):
        self.index = pd.to_datetime(
            ["2026-01-30", "2026-02-27", "2026-03-31", "2026-04-30", "2026-05-29"]
        )

    def test_one_month_response_matches_raw_target(self):
        monthly = pd.DataFrame(
            {"SPY": [0.5, 0.5, 0.0, 0.5, 0.5], "QQQ": [0.5] * 5},
            index=self.index,
        )
        daily, _ = confirmed_daily_targets(self.index, monthly, 1, 1)
        self.assertEqual(daily[self.index[2]]["SPY"], 0.0)
        self.assertEqual(daily[self.index[3]]["SPY"], 0.5)

    def test_two_month_exit_ignores_single_month_break(self):
        monthly = pd.DataFrame(
            {"SPY": [0.5, 0.5, 0.0, 0.5, 0.5], "QQQ": [0.5] * 5},
            index=self.index,
        )
        daily, decisions = confirmed_daily_targets(self.index, monthly, 2, 1)
        self.assertEqual(daily[self.index[2]]["SPY"], 0.5)
        self.assertEqual(daily[self.index[3]]["SPY"], 0.5)
        self.assertTrue(pd.isna(decisions.at[self.index[3], "SPY_pending"]))

    def test_two_month_entry_waits_for_second_completed_month(self):
        monthly = pd.DataFrame(
            {"SPY": [0.0, 0.5, 0.5, 0.5, 0.5], "QQQ": [0.0] * 5},
            index=self.index,
        )
        daily, _ = confirmed_daily_targets(self.index, monthly, 1, 2)
        self.assertEqual(daily[self.index[1]]["SPY"], 0.0)
        self.assertEqual(daily[self.index[2]]["SPY"], 0.5)

    def test_no_change_before_month_end_decision(self):
        daily_index = pd.to_datetime(["2026-01-29", "2026-01-30", "2026-02-02"])
        monthly = pd.DataFrame({"SPY": [0.5], "QQQ": [0.5]}, index=[daily_index[1]])
        daily, _ = confirmed_daily_targets(daily_index, monthly, 1, 1)
        self.assertEqual(daily[daily_index[0]]["SPY"], 0.0)
        self.assertEqual(daily[daily_index[1]]["SPY"], 0.5)
        self.assertEqual(daily[daily_index[2]]["SPY"], 0.5)

    def test_identical_variant_is_not_a_promotion(self):
        rows = []
        for period in ("train_2025", "test_2026"):
            for variant in ("current_1m", "ma200_only"):
                rows.append(
                    {
                        "period": period,
                        "variant": variant,
                        "total_return": 0.1,
                        "max_drawdown": -0.05,
                        "sharpe": 1.0,
                        "turnover": 2.0,
                        "trades": 4,
                    }
                )
        screen = paired_screen(pd.DataFrame(rows))
        row = screen.loc[screen["variant"] == "ma200_only"].iloc[0]
        self.assertFalse(row["behaviorally_distinct"])
        self.assertFalse(row["passes_promotion_gate"])


if __name__ == "__main__":
    unittest.main()
