import importlib.util
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("partial_profit", HERE / "evaluate_partial_profit_scaleout.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BACKTEST = MODULE.BACKTEST


class PartialProfitScaleoutTests(unittest.TestCase):
    def test_one_share_cannot_be_partially_sold(self):
        order, status = BACKTEST["partial_exit_order"](1, 500.0, 0.001, 0.5, 200.0)
        self.assertIsNone(order)
        self.assertEqual(status, "ineligible_whole_shares")

    def test_half_whole_share_order_includes_slippage_and_notional(self):
        order, status = BACKTEST["partial_exit_order"](4, 300.0, 0.001, 0.5, 200.0)
        self.assertEqual(status, "executed")
        self.assertEqual(order["shares"], 2)
        self.assertAlmostEqual(order["fill"], 299.70)
        self.assertAlmostEqual(order["gross_proceeds"], 599.40)

    def test_partial_exit_respects_minimum_notional(self):
        order, status = BACKTEST["partial_exit_order"](2, 150.0, 0.001, 0.5, 200.0)
        self.assertIsNone(order)
        self.assertEqual(status, "ineligible_min_notional")

    def test_aggregate_pnl_uses_original_trade_cost_once(self):
        position = {
            "cost_basis": 500.0,
            "original_cost_basis": 1000.0,
            "realized_pnl": 100.0,
        }
        pnl, trade_return = BACKTEST["aggregate_position_pnl"](position, 600.0)
        self.assertAlmostEqual(pnl, 200.0)
        self.assertAlmostEqual(trade_return, 0.20)

    def test_decomposition_keeps_capacity_created_trade_separate(self):
        trades = pd.DataFrame(
            [
                {"initial_nav": 6000.0, "slippage": 0.001, "period_name": "full", "variant_name": "RSR2", "symbol": "A", "signal_date": "2025-01-01", "pnl": 10.0},
                {"initial_nav": 6000.0, "slippage": 0.001, "period_name": "full", "variant_name": "partial_half_at_15", "symbol": "A", "signal_date": "2025-01-01", "pnl": 8.0, "partial_exit_status": "executed"},
                {"initial_nav": 6000.0, "slippage": 0.001, "period_name": "full", "variant_name": "partial_half_at_15", "symbol": "B", "signal_date": "2025-02-01", "pnl": -3.0, "partial_exit_status": None},
            ]
        )
        result = MODULE.decompose_trade_paths(trades)
        common = result.loc[result["group"] == "common"].iloc[0]
        added = result.loc[result["group"] == "candidate_only"].iloc[0]
        self.assertAlmostEqual(common["pnl_delta"], -2.0)
        self.assertAlmostEqual(added["pnl_delta"], -3.0)

    def _screen_fixture(self):
        rows = []
        for nav in MODULE.NAVS:
            for slippage in MODULE.SLIPPAGES:
                for period in MODULE.PERIODS:
                    for variant in MODULE.VARIANTS:
                        candidate = variant == "partial_half_at_15"
                        rows.append(
                            {
                                "initial_nav": nav,
                                "slippage": slippage,
                                "period_name": period,
                                "variant_name": variant,
                                "total_return": 0.12 if candidate else 0.10,
                                "max_drawdown": -0.10,
                                "sharpe": 1.1 if candidate else 1.0,
                                "win_rate": 0.60,
                                "partial_exits": 6 if candidate else 0,
                                "profitable_symbols": 4,
                                "top_symbol_profit_share": 0.30,
                            }
                        )
        return pd.DataFrame(rows)

    def test_screen_rejects_insufficient_heldout_exits(self):
        metrics = self._screen_fixture()
        metrics.loc[
            (metrics["variant_name"] == "partial_half_at_15")
            & (metrics["period_name"] == "heldout_2026"),
            "partial_exits",
        ] = 1
        screen = MODULE.advancement_screen(metrics)
        self.assertEqual(screen["status"], "insufficient")
        self.assertFalse(screen["passes"])

    def test_screen_passes_only_complete_positive_comparison(self):
        screen = MODULE.advancement_screen(self._screen_fixture())
        self.assertEqual(screen["status"], "pass")
        self.assertTrue(screen["passes"])


if __name__ == "__main__":
    unittest.main()
