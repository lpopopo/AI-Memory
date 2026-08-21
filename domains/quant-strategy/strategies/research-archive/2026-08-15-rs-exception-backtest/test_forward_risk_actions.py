import unittest

import pandas as pd

import evaluate_forward_risk_actions as target


class ForwardRiskActionTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.to_datetime(["2026-08-14", "2026-08-17", "2026-08-18", "2026-08-19"])
        self.opens = pd.DataFrame({"A": [100.0, 110.0, 108.0, 90.0]}, index=self.dates)
        self.closes = pd.DataFrame({"A": [100.0, 105.0, 95.0, 80.0]}, index=self.dates)
        self.event = pd.Series(
            {
                "trigger_date": pd.Timestamp("2026-08-14"),
                "symbol": "A",
                "shares": 4,
                "review_state": "review",
                "observation_class": "retrospective_seed",
            }
        )

    def test_execution_is_first_valid_open_after_trigger(self):
        date = target.first_execution_date(self.event["trigger_date"], "A", self.opens, self.closes)
        self.assertEqual(date, pd.Timestamp("2026-08-17"))

    def test_horizon_counts_execution_session_as_one(self):
        date, close = target.fixed_horizon_point(pd.Timestamp("2026-08-17"), "A", self.closes, 1)
        self.assertEqual(date, pd.Timestamp("2026-08-17"))
        self.assertEqual(close, 105.0)
        date, close = target.fixed_horizon_point(pd.Timestamp("2026-08-17"), "A", self.closes, 3)
        self.assertEqual(date, pd.Timestamp("2026-08-19"))
        self.assertEqual(close, 80.0)

    def test_immature_horizon_is_unavailable(self):
        date, close = target.fixed_horizon_point(pd.Timestamp("2026-08-17"), "A", self.closes, 5)
        self.assertIsNone(date)
        self.assertIsNone(close)

    def test_full_exit_net_benefit_includes_slippage_and_commission(self):
        row = target.outcome_row(
            self.event,
            "full_exit",
            pd.Timestamp("2026-08-17"),
            110.0,
            1,
            pd.Timestamp("2026-08-17"),
            105.0,
        )
        self.assertAlmostEqual(row["gross_benefit_vs_hold"], 20.0)
        self.assertAlmostEqual(row["net_benefit_vs_hold"], 4 * (109.89 - 105.0) - 1.0)
        self.assertTrue(row["beneficial"])

    def test_half_exit_uses_integer_shares(self):
        self.assertEqual(target.action_shares(5, "half_exit"), 2)
        self.assertEqual(target.action_shares(5, "full_exit"), 5)

    def test_summary_keeps_empty_genuine_forward_unavailable(self):
        outcomes = target.evaluate_events(
            target.validate_events(
                pd.DataFrame(
                    [
                        {
                            "trigger_date": "2026-08-14",
                            "symbol": "A",
                            "shares": 4,
                            "review_state": "review",
                            "observation_class": "retrospective_seed",
                            "real_order_assumed": False,
                        }
                    ]
                )
            ),
            self.opens,
            self.closes,
        )
        summary = target.summarize(outcomes, "genuine_forward", "full_exit", "1")
        self.assertEqual(summary["mature_events"], 0)
        self.assertIsNone(summary["beneficial_events"])
        self.assertIsNone(summary["total_net_benefit"])

    def test_real_order_assumption_is_rejected(self):
        frame = pd.DataFrame(
            [
                {
                    "trigger_date": "2026-08-14",
                    "symbol": "A",
                    "shares": 4,
                    "review_state": "review",
                    "observation_class": "genuine_forward",
                    "real_order_assumed": True,
                }
            ]
        )
        with self.assertRaises(RuntimeError):
            target.validate_events(frame)


if __name__ == "__main__":
    unittest.main()
