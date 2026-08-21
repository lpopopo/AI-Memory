import unittest

import evaluate_objective_frontier as target


class ObjectiveFrontierTests(unittest.TestCase):
    def test_dominance_uses_less_negative_drawdown_as_better(self):
        metrics = ("total_return", "max_drawdown", "sharpe")
        stronger = {
            "comparable_group": "test",
            "total_return": 0.2,
            "max_drawdown": -0.02,
            "sharpe": 1.5,
        }
        weaker = {
            "comparable_group": "test",
            "total_return": 0.1,
            "max_drawdown": -0.05,
            "sharpe": 1.0,
        }
        self.assertTrue(target.dominates(stronger, weaker, metrics))
        self.assertFalse(target.dominates(weaker, stronger, metrics))

    def test_tradeoff_remains_on_frontier(self):
        rows = [
            {
                "family": "combined_2026_architecture",
                "comparable_group": "same",
                "total_return": 0.20,
                "max_drawdown": -0.05,
                "sharpe": 1.0,
            },
            {
                "family": "combined_2026_architecture",
                "comparable_group": "same",
                "total_return": 0.10,
                "max_drawdown": -0.02,
                "sharpe": 1.5,
            },
        ]
        target.assign_pareto_status(rows)
        self.assertEqual([row["pareto_status"] for row in rows], ["pareto_frontier"] * 2)

    def test_single_candidate_is_descriptive_not_selected(self):
        rows = [
            {
                "family": "high_volatility_sleeve",
                "comparable_group": "only",
            }
        ]
        target.assign_pareto_status(rows)
        self.assertEqual(rows[0]["pareto_status"], "descriptive_single_candidate")

    def test_registered_matrix_keeps_historical_and_deployable_leaders_separate(self):
        rows = target.build_rows()
        summary = target.build_summary(rows)
        self.assertEqual(summary["best_historical_multi_objective_candidate"]["variant"], "RSR2")
        self.assertEqual(summary["best_deployable_architecture"]["variant"], "formal V9 70/30")
        self.assertFalse(summary["formal_v9_modified"])
        self.assertFalse(summary["live_order_authorization"])

    def test_stock_family_marks_rsr2_as_frontier_not_promoted(self):
        rows = target.build_rows()
        rsr2 = next(
            row
            for row in rows
            if row["family"] == "stock_selection_exit" and row["variant"] == "RSR2"
        )
        self.assertEqual(rsr2["pareto_status"], "pareto_frontier")
        self.assertIn("no promotion", rsr2["formal_status"])


if __name__ == "__main__":
    unittest.main()

