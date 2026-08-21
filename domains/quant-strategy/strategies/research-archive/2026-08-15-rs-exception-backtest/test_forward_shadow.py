from pathlib import Path
import runpy
import unittest

import pandas as pd


HERE = Path(__file__).resolve().parent
FORWARD = runpy.run_path(str(HERE / "run_forward_shadow.py"))
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))


class ForwardShadowTests(unittest.TestCase):
    def test_empty_baseline_trade_frame_preserves_schema(self):
        frame = FORWARD["baseline_trade_frame"]([])
        self.assertTrue(frame.empty)
        self.assertEqual(list(frame.columns), list(FORWARD["BASELINE_TRADE_COLUMNS"]))

    def test_completed_cutoff_excludes_weekend_and_live_session(self):
        cutoff = FORWARD["completed_cutoff"]
        self.assertEqual(cutoff(pd.Timestamp("2026-08-15 12:00", tz="UTC")), pd.Timestamp("2026-08-14"))
        self.assertEqual(cutoff(pd.Timestamp("2026-08-17 15:00", tz="UTC")), pd.Timestamp("2026-08-14"))
        self.assertEqual(cutoff(pd.Timestamp("2026-08-17 23:00", tz="UTC")), pd.Timestamp("2026-08-17"))

    def test_matched_pair_differs_only_on_two_risk_fields(self):
        baseline, candidate = FORWARD["frozen_configs"]()
        baseline_dict = baseline.__dict__
        candidate_dict = candidate.__dict__
        differences = {key for key in baseline_dict if baseline_dict[key] != candidate_dict[key]}
        self.assertEqual(differences, {"max_atr_pct", "min_close_location"})

    def test_forward_snapshot_does_not_terminal_liquidate(self):
        panels, symbols = BACKTEST["load_panels"]()
        config = BACKTEST["Config"]()
        result = BACKTEST["simulate"](
            panels,
            symbols,
            config,
            "strict_veto",
            "2026-01-01",
            "2026-08-07",
            liquidate_final=False,
        )
        self.assertFalse(result["liquidated_at_end"])
        self.assertTrue(all(trade.get("exit_reason") != "terminal" for trade in result["trades"]))

    def test_slippage_is_an_explicit_sensitivity_input(self):
        panels, symbols = BACKTEST["load_panels"]()
        config = BACKTEST["Config"]()
        low = BACKTEST["simulate"](
            panels, symbols, config, "strict_veto", "2025-01-01", "2025-12-31", slippage=0.001
        )
        high = BACKTEST["simulate"](
            panels, symbols, config, "strict_veto", "2025-01-01", "2025-12-31", slippage=0.002
        )
        self.assertGreater(high["metrics"]["costs"], low["metrics"]["costs"])
        self.assertLess(high["metrics"]["total_return"], low["metrics"]["total_return"])
        fixed_path = BACKTEST["fixed_path_cost_stress"](
            low, source_slippage=0.001, stressed_slippage=0.002
        )
        unchanged = BACKTEST["fixed_path_cost_stress"](
            low, source_slippage=0.001, stressed_slippage=0.001
        )
        self.assertEqual(fixed_path["closed_trades"], low["metrics"]["trade_count"])
        self.assertAlmostEqual(unchanged["total_return"], low["metrics"]["total_return"])
        self.assertLess(fixed_path["total_return"], low["metrics"]["total_return"])

    def test_pending_baseline_action_is_preserved(self):
        order = {"signal_date": "2026-08-17", "symbol": "AAOI"}
        candidate = {"trades": [], "pending_entries": [order]}
        baseline = {"trades": [], "pending_entries": [order]}
        ledger = FORWARD["trade_ledger"](
            candidate,
            baseline,
            pd.Timestamp("2026-08-17"),
            pd.DatetimeIndex([pd.Timestamp("2026-08-17")]),
        )
        self.assertEqual(ledger.iloc[0]["baseline_action"], "pending")
        self.assertEqual(ledger.iloc[0]["planned_execution_date"], "next_session")

    def test_shadow_universe_uses_explicit_common_factor_scope(self):
        themes = FORWARD["watchlist_theme_map"]()
        self.assertEqual(themes["KO"], "consumer_defensive_beverages")
        self.assertEqual(themes["RKLB"], "space_satellite")
        self.assertEqual(themes["CEG"], "ai_power_nuclear_generation")

        _, all_symbols = BACKTEST["load_panels"]()
        shadow_symbols = FORWARD["shadow_universe"](all_symbols)
        self.assertEqual(len(all_symbols), 35)
        self.assertEqual(len(shadow_symbols), 32)
        self.assertEqual(set(all_symbols) - set(shadow_symbols), {"KO", "RKLB", "RDW"})
        self.assertTrue({"TSLA", "TTMI", "CEG"}.issubset(shadow_symbols))

    def test_profit_concentration_aggregates_repeated_wins_by_symbol(self):
        concentration = FORWARD["symbol_profit_concentration"](
            [
                {"symbol": "AAOI", "pnl": 30.0},
                {"symbol": "AAOI", "pnl": 30.0},
                {"symbol": "NVDA", "pnl": 40.0},
                {"symbol": "AAOI", "pnl": -20.0},
            ]
        )
        self.assertEqual(concentration["gross_profit"], 100.0)
        self.assertEqual(concentration["profit_by_symbol"], {"AAOI": 60.0, "NVDA": 40.0})
        self.assertAlmostEqual(concentration["max_symbol_profit_share"], 0.60)

    def test_profit_lock_ledger_preserves_rsr1_pending_action(self):
        order = {"signal_date": "2026-08-17", "symbol": "AAOI"}
        challenger = {"trades": [], "pending_entries": [order]}
        rsr1 = {"trades": [], "pending_entries": [order]}
        ledger = FORWARD["profit_lock_ledger"](
            challenger,
            rsr1,
            pd.Timestamp("2026-08-17"),
            pd.DatetimeIndex([pd.Timestamp("2026-08-17")]),
        )
        self.assertEqual(ledger.iloc[0]["version"], "RSR2-profit-lock-shadow")
        self.assertEqual(ledger.iloc[0]["rsr1_action"], "pending")
        self.assertEqual(ledger.iloc[0]["planned_execution_date"], "next_session")

    def test_profit_lock_forward_components_run_on_completed_history(self):
        panels, all_symbols = BACKTEST["load_panels"]()
        symbols = FORWARD["shadow_universe"](all_symbols)
        start = pd.Timestamp("2026-01-01")
        as_of = pd.Timestamp("2026-08-07")
        pair_10 = FORWARD["run_pair"](panels, symbols, start, as_of, 0.001)
        pair_20 = FORWARD["run_pair"](panels, symbols, start, as_of, 0.002)
        _, candidate_config = FORWARD["frozen_configs"]()
        challenger_10 = BACKTEST["simulate"](
            panels,
            symbols,
            candidate_config,
            "strict_veto",
            str(start.date()),
            str(as_of.date()),
            liquidate_final=False,
            slippage=0.001,
            profit_lock_trigger=FORWARD["PROFIT_LOCK_TRIGGER"],
            profit_lock_floor=FORWARD["PROFIT_LOCK_FLOOR"],
        )
        challenger_20 = BACKTEST["simulate"](
            panels,
            symbols,
            candidate_config,
            "strict_veto",
            str(start.date()),
            str(as_of.date()),
            liquidate_final=False,
            slippage=0.002,
            profit_lock_trigger=FORWARD["PROFIT_LOCK_TRIGGER"],
            profit_lock_floor=FORWARD["PROFIT_LOCK_FLOOR"],
        )
        ledger = FORWARD["profit_lock_ledger"](
            challenger_10, pair_10["risk_filter"], as_of, panels["close"].index
        )
        gate = FORWARD["profit_lock_promotion_gate"](
            pair_10["risk_filter"],
            challenger_10,
            pair_20["risk_filter"],
            challenger_20,
            len(panels["close"].loc[start:as_of]),
        )
        self.assertEqual(list(ledger.columns), list(FORWARD["PROFIT_LEDGER_COLUMNS"]))
        self.assertIn("survives_fixed_path_20bps_vs_rsr1", gate["checks"])
        self.assertFalse(gate["sample_ready"])


if __name__ == "__main__":
    unittest.main()
