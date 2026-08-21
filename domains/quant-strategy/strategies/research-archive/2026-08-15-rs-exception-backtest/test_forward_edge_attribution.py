import unittest

import pandas as pd

import evaluate_forward_edge_attribution as target


class ForwardEdgeAttributionTests(unittest.TestCase):
    def test_empty_sample_is_unavailable_not_zero(self):
        result = target.direct_exclusion_summary({}, set())
        self.assertEqual(result["status"], "awaiting_closed_baseline_exclusion")
        self.assertIsNone(result["avoided_losing_trades"])
        self.assertIsNone(result["missed_profit_dollars"])

    def test_empty_overlay_preserves_output_schema(self):
        result, rows = target.overlay_summary({}, {})
        self.assertEqual(result["status"], "awaiting_paired_rsr_exit")
        self.assertEqual(list(rows.columns), target.OVERLAY_COLUMNS)

    def test_unavailable_count_is_not_rendered_as_zero_or_none(self):
        self.assertEqual(target.count_text(None), "unavailable")
        self.assertEqual(target.count_text(0), "0")

    def test_direct_exclusion_reports_both_loss_and_missed_profit(self):
        baseline = {
            ("A", "2026-08-17"): {"pnl": -20.0},
            ("B", "2026-08-18"): {"pnl": 10.0},
        }
        result = target.direct_exclusion_summary(baseline, set(baseline))
        self.assertEqual(result["avoided_losing_trades"], 1)
        self.assertEqual(result["missed_winning_trades"], 1)
        self.assertAlmostEqual(result["net_pnl_removed"], -10.0)

    def test_overlay_separates_direct_exit_and_sizing_path(self):
        key = ("A", "2026-08-17")
        rsr1 = {key: {"pnl": 20.0, "shares": 2, "exit_price": 110.0, "exit_reason": "signal"}}
        rsr2 = {key: {"pnl": 50.0, "shares": 3, "exit_price": 120.0, "exit_reason": "profit_lock"}}
        result, rows = target.overlay_summary(rsr1, rsr2)
        self.assertAlmostEqual(result["aggregate_pnl_delta"], 30.0)
        self.assertAlmostEqual(result["aggregate_direct_exit_effect"], 20.0)
        self.assertAlmostEqual(result["aggregate_capital_path_and_sizing_residual"], 10.0)
        self.assertEqual(len(rows), 1)

    def test_signal_keys_require_baseline_true_and_rsr1_false(self):
        signals = pd.DataFrame(
            {
                "date": ["2026-08-17", "2026-08-18"],
                "symbol": ["A", "B"],
                "matched_baseline_signal": [True, True],
                "risk_filter_signal": [False, True],
            }
        )
        self.assertEqual(target.direct_exclusion_keys(signals), {("A", "2026-08-17")})


if __name__ == "__main__":
    unittest.main()
