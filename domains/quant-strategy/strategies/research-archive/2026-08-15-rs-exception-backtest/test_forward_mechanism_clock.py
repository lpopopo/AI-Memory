import unittest

import pandas as pd

import evaluate_forward_mechanism_clock as target


class ForwardMechanismClockTests(unittest.TestCase):
    def test_quality_direction_keeps_profit_and_hit_rate_together(self):
        frame = pd.DataFrame(
            {"pnl": [-10.0, -5.0, 8.0], "return": [-0.1, -0.05, 0.08]}
        )
        result = target.quality_metrics(frame)
        self.assertEqual(result["direction"], "supportive_direction")
        self.assertAlmostEqual(result["loss_rate"], 2 / 3)
        self.assertEqual(result["net_pnl_removed"], -7.0)

    def test_checkpoint_snapshot_uses_first_five_and_does_not_reclassify_at_six(self):
        frame = pd.DataFrame(
            {
                "pnl": [-1.0, -1.0, -1.0, 1.0, 1.0, 100.0],
                "return": [-0.01, -0.01, -0.01, 0.01, 0.01, 1.0],
            }
        )
        clock = target.checkpoint_clock(frame, (5, 10, 20), target.quality_metrics)
        self.assertEqual(clock["latest_completed_checkpoint"], 5)
        self.assertEqual(clock["latest_checkpoint_interpretation"], "supportive_direction")
        self.assertEqual(clock["current_raw_metrics"]["direction"], "mixed_direction")
        self.assertTrue(clock["between_checkpoints_do_not_reclassify"])

    def test_paired_order_uses_later_exit_when_both_sides_known(self):
        first = ("A", "2026-08-17")
        second = ("B", "2026-08-18")
        rsr1 = {
            first: {"exit_date": "2026-08-25", "pnl": 1, "shares": 1, "exit_price": 10},
            second: {"exit_date": "2026-08-22", "pnl": 1, "shares": 1, "exit_price": 10},
        }
        rsr2 = {
            first: {"exit_date": "2026-08-26", "pnl": 2, "shares": 1, "exit_price": 11},
            second: {"exit_date": "2026-08-23", "pnl": 2, "shares": 1, "exit_price": 11},
        }
        rows = target.paired_rows(rsr1, rsr2)
        self.assertEqual(rows["symbol"].tolist(), ["B", "A"])
        self.assertEqual(rows["exit_date"].tolist(), ["2026-08-23", "2026-08-26"])

    def test_empty_registered_clock_is_read_only_and_unavailable(self):
        summary = target.evaluate()
        self.assertEqual(summary["overall_status"], "awaiting_sample")
        self.assertEqual(summary["entry_quality_clock"]["current_outcomes"], 0)
        self.assertEqual(
            summary["entry_quality_clock"]["latest_checkpoint_interpretation"],
            "unavailable",
        )
        self.assertFalse(summary["changes_promotion_gate"])
        self.assertFalse(summary["live_order_authorization"])


if __name__ == "__main__":
    unittest.main()
