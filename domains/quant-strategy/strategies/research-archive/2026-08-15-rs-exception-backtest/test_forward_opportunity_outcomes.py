import importlib.util
import unittest
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("opportunity_outcomes", HERE / "evaluate_forward_opportunity_outcomes.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ForwardOpportunityOutcomeTests(unittest.TestCase):
    def panels(self, periods=30):
        index = pd.bdate_range("2026-08-17", periods=periods)
        close = pd.DataFrame({"A": [100.0 + i for i in range(periods)]}, index=index)
        return {
            "close": close,
            "high": close + 1.0,
            "low": close - 2.0,
        }

    def test_symbol_parser_is_deterministic_and_tolerates_empty(self):
        self.assertEqual(MODULE.parse_symbols('["B","A","A"]'), ["A", "B"])
        self.assertEqual(MODULE.parse_symbols(""), [])

    def test_exact_five_session_outcome_uses_no_earlier_or_later_close(self):
        panels = self.panels()
        ledger = pd.DataFrame(
            [{"date": "2026-08-17", "high_vol_central_symbols": "[]", "high_vol_missed_leaders": '["A"]'}]
        )
        events = MODULE.build_events(ledger, panels)
        row = events.loc[events["horizon_sessions"] == 5].iloc[0]
        self.assertTrue(row["matured"])
        self.assertEqual(row["horizon_date"], "2026-08-24")
        self.assertAlmostEqual(row["horizon_return"], 0.05)
        self.assertAlmostEqual(row["max_adverse_excursion"], -0.01)

    def test_incomplete_horizon_never_enters_summary(self):
        panels = self.panels(periods=2)
        ledger = pd.DataFrame(
            [{"date": "2026-08-17", "high_vol_central_symbols": "[]", "high_vol_missed_leaders": '["A"]'}]
        )
        events = MODULE.build_events(ledger, panels)
        summary = MODULE.summarize(events)
        row = summary.loc[
            (summary["event_type"] == "high_vol_missed_leader")
            & (summary["horizon_sessions"] == 5)
        ].iloc[0]
        self.assertEqual(row["matured_primary_episodes"], 0)
        self.assertTrue(pd.isna(row["mean_return"]))

    def test_consecutive_same_symbol_events_form_one_episode(self):
        panels = self.panels()
        ledger = pd.DataFrame(
            [
                {"date": "2026-08-17", "high_vol_central_symbols": "[]", "high_vol_missed_leaders": '["A"]'},
                {"date": "2026-08-18", "high_vol_central_symbols": "[]", "high_vol_missed_leaders": '["A"]'},
            ]
        )
        events = MODULE.build_events(ledger, panels)
        five = events.loc[events["horizon_sessions"] == 5]
        self.assertEqual(five["episode_id"].nunique(), 1)
        self.assertEqual(int(five["primary_episode"].sum()), 1)


if __name__ == "__main__":
    unittest.main()
