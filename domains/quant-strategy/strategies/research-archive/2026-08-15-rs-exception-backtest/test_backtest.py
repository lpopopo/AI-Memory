from pathlib import Path
import runpy
import unittest

import pandas as pd


MODULE = runpy.run_path(str(Path(__file__).with_name("run_backtest.py")))


class BacktestIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panels, cls.symbols = MODULE["load_panels"]()

    def test_signal_execution_is_next_session(self):
        result = MODULE["simulate"](
            self.panels, self.symbols, MODULE["Config"](), "rs_exception", "2026-01-01", "2026-08-07"
        )
        for trade in result["trades"]:
            self.assertGreater(trade["entry_date"], trade["signal_date"])

    def test_strict_veto_has_no_exception_entries(self):
        result = MODULE["simulate"](
            self.panels, self.symbols, MODULE["Config"](), "strict_veto", "2024-01-02", "2026-08-07"
        )
        self.assertEqual(result["metrics"]["exception_trade_count"], 0)
        self.assertTrue(all(trade["smh_healthy_on_signal"] for trade in result["trades"]))

    def test_costs_and_whole_shares_are_enforced(self):
        result = MODULE["simulate"](
            self.panels, self.symbols, MODULE["Config"](), "rs_exception", "2024-01-02", "2026-08-07"
        )
        self.assertGreater(result["metrics"]["costs"], 0)
        self.assertTrue(all(isinstance(trade["shares"], int) and trade["shares"] >= 1 for trade in result["trades"]))

    def test_profit_stop_ratchets_only_after_completed_close_trigger(self):
        ratchet = MODULE["ratcheted_profit_stop"]
        unchanged, raised = ratchet(100.0, 92.0, 109.99, 0.10, 0.0)
        self.assertEqual(unchanged, 92.0)
        self.assertFalse(raised)
        changed, raised = ratchet(100.0, 92.0, 110.0, 0.10, 0.0)
        self.assertEqual(changed, 100.0)
        self.assertTrue(raised)
        never_lowered, raised = ratchet(100.0, 105.0, 120.0, 0.10, 0.0)
        self.assertEqual(never_lowered, 105.0)
        self.assertFalse(raised)

    def test_missing_open_preserves_pending_exit_until_executable(self):
        date = pd.Timestamp("2026-01-02")
        opens = pd.DataFrame({"AAOI": [float("nan")], "MU": [100.0]}, index=[date])
        positions = {"AAOI": {}, "MU": {}}
        executable, deferred = MODULE["partition_pending_exit_fills"](
            {"AAOI", "MU"}, positions, opens, date, 0.001
        )
        self.assertEqual(deferred, {"AAOI"})
        self.assertEqual(executable["MU"], (100.0, 99.9))

    def test_cash_return_overlay_ignores_pre_start_return_and_accrues_later_cash(self):
        start, end = "2026-01-02", "2026-01-09"
        dates = self.panels["close"].loc[start:end].index
        base = MODULE["simulate"](
            self.panels, self.symbols, MODULE["Config"](), "strict_veto", start, end
        )
        first_only = pd.Series(0.0, index=dates)
        first_only.iloc[0] = 0.10
        unchanged = MODULE["simulate"](
            self.panels,
            self.symbols,
            MODULE["Config"](),
            "strict_veto",
            start,
            end,
            cash_returns=first_only,
        )
        later = pd.Series(0.001, index=dates)
        later.iloc[0] = 0.0
        accrued = MODULE["simulate"](
            self.panels,
            self.symbols,
            MODULE["Config"](),
            "strict_veto",
            start,
            end,
            cash_returns=later,
        )
        self.assertAlmostEqual(unchanged["metrics"]["total_return"], base["metrics"]["total_return"])
        self.assertEqual(unchanged["metrics"]["cash_yield_earned"], 0.0)
        self.assertGreater(accrued["metrics"]["cash_yield_earned"], 0.0)
        self.assertGreater(accrued["metrics"]["total_return"], base["metrics"]["total_return"])

    def test_initial_nav_and_stock_sleeve_cap_are_configurable(self):
        nav = 5751.77
        config = MODULE["Config"](stock_sleeve_max=0.20)
        result = MODULE["simulate"](
            self.panels,
            self.symbols,
            config,
            "strict_veto",
            "2026-01-02",
            "2026-01-09",
            initial_nav=nav,
        )
        self.assertAlmostEqual(float(next(iter(result["equity"].values()))), nav, places=6)
        self.assertGreater(result["metrics"]["turnover"], 0.0)
        self.assertLessEqual(max(result["exposure"].values()), 0.20 + 1e-9)
        with self.assertRaises(ValueError):
            MODULE["simulate"](
                self.panels,
                self.symbols,
                MODULE["Config"](stock_sleeve_max=0.31),
                "strict_veto",
                "2026-01-02",
                "2026-01-09",
            )


if __name__ == "__main__":
    unittest.main()
