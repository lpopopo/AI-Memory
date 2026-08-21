import unittest

import numpy as np
import pandas as pd

import evaluate_historical_uncertainty as target


class HistoricalUncertaintyTests(unittest.TestCase):
    def test_corrected_probability_applies_plus_one_correction(self):
        self.assertAlmostEqual(target.corrected_probability(np.array([False, False])), 1 / 3)
        self.assertAlmostEqual(target.corrected_probability(np.array([True, True])), 1.0)

    def test_cluster_bootstrap_keeps_same_day_rows_together(self):
        frame = pd.DataFrame(
            {
                "signal_date": ["2026-01-01", "2026-01-01", "2026-01-02"],
                "value": [1, 2, 3],
            }
        )
        clusters = target.cluster_frames(frame)
        self.assertEqual([len(cluster) for cluster in clusters], [2, 1])

    def test_removal_sensitivity_does_not_rescale(self):
        result = target.removal_sensitivity(pd.Series([100.0, 40.0, 10.0, 0.0]))
        self.assertEqual(result["observed_aggregate"], 150.0)
        self.assertEqual(result["remaining_after_largest"], 50.0)
        self.assertEqual(result["remaining_after_two_largest"], 10.0)

    def test_paired_metrics_separates_direct_and_path(self):
        frame = pd.DataFrame(
            {
                "pnl_delta": [20.0, 0.0],
                "direct_exit_effect_on_rsr1_shares": [5.0, 0.0],
                "capital_path_and_sizing_residual": [15.0, 0.0],
                "rsr1_pnl": [-2.0, 3.0],
                "rsr2_pnl": [18.0, 3.0],
            }
        )
        result = target.paired_metrics(frame)
        self.assertEqual(result["mean_total_pnl_delta"], 10.0)
        self.assertEqual(result["mean_direct_exit_effect"], 2.5)
        self.assertEqual(result["mean_path_sizing_residual"], 7.5)
        self.assertEqual(result["win_rate_delta"], 0.5)

    def test_registered_audit_is_read_only_and_keeps_sparse_label(self):
        summary = target.evaluate()
        self.assertFalse(summary["formal_v9_modified"])
        self.assertFalse(summary["real_account_modified"])
        self.assertFalse(summary["live_order_authorization"])
        self.assertFalse(summary["new_parameter_search"])
        self.assertEqual(summary["rsr2_paired_delta"]["evidence_label"], "directional_but_sparse")


if __name__ == "__main__":
    unittest.main()
