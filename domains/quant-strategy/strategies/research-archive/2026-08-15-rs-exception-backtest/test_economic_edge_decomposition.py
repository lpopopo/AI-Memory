import unittest

import evaluate_economic_edge_decomposition as target


class EconomicEdgeDecompositionTests(unittest.TestCase):
    def test_exclusion_reason_discloses_both_failures(self):
        self.assertEqual(target.exclusion_reason(0.05, 0.40), "atr_pct+close_location")
        self.assertEqual(target.exclusion_reason(0.03, 0.60), "portfolio_path")

    def test_economics_keeps_losses_and_opportunity_cost(self):
        result = target.economics(
            [
                {"pnl": 100.0, "return": 0.10},
                {"pnl": -40.0, "return": -0.04},
            ]
        )
        self.assertEqual(result["trades"], 2)
        self.assertAlmostEqual(result["win_rate"], 0.5)
        self.assertAlmostEqual(result["net_pnl"], 60.0)
        self.assertAlmostEqual(result["profit_factor"], 2.5)

    def test_winner_concentration_is_not_rescaled(self):
        trades = [
            {"symbol": "A", "signal_date": "2026-01-01", "pnl": 100.0, "return": 0.10},
            {"symbol": "B", "signal_date": "2026-01-02", "pnl": 50.0, "return": 0.05},
            {"symbol": "C", "signal_date": "2026-01-03", "pnl": -30.0, "return": -0.03},
        ]
        result = target.winner_concentration(trades)
        self.assertAlmostEqual(result["top_k"][0]["share_of_gross_profit"], 2 / 3)
        self.assertAlmostEqual(result["top_k"][0]["leave_out_net_pnl"], 20.0)

    def test_direct_exit_effect_formula_is_share_fixed(self):
        rsr1 = {"shares": 4, "exit_price": 95.0}
        rsr2 = {"shares": 7, "exit_price": 105.0}
        self.assertAlmostEqual(target.direct_exit_effect(rsr1, rsr2), 40.0)


if __name__ == "__main__":
    unittest.main()
