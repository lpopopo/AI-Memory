#!/usr/bin/env python3
from __future__ import annotations

import unittest

import pandas as pd

from run_forward_opportunity_diagnostics import (
    LEDGER_COLUMNS,
    START,
    core_reversal_label,
    merge_immutable,
)


class ForwardOpportunityDiagnosticsTests(unittest.TestCase):
    def row(self, date: str, count: int = 0) -> dict:
        result = {column: "" for column in LEDGER_COLUMNS}
        result.update(
            {
                "date": date,
                "version": "opportunity-diagnostics-v1",
                "source_complete": True,
                "high_vol_central_count": count,
                "research_only": True,
                "authorizes_trade": False,
            }
        )
        return result

    def test_core_reversal_uses_three_completed_months(self):
        dates = pd.to_datetime(["2026-01-30", "2026-02-27", "2026-03-31"])
        monthly = pd.DataFrame(
            {
                "spy_effective_target": [0.35, 0.0, 0.35],
                "qqq_effective_target": [0.35, 0.35, 0.35],
            },
            index=dates,
        )
        self.assertEqual(core_reversal_label(monthly, dates[-1]), "down_then_up")
        self.assertEqual(core_reversal_label(monthly.iloc[:2], dates[1]), "")

    def test_immutable_merge_appends_new_dates(self):
        existing = pd.DataFrame([self.row("2026-08-17")])
        computed = pd.DataFrame([self.row("2026-08-17"), self.row("2026-08-18", 1)])
        merged = merge_immutable(existing, computed)
        self.assertEqual(merged["date"].tolist(), ["2026-08-17", "2026-08-18"])

    def test_immutable_merge_rejects_changed_history(self):
        existing = pd.DataFrame([self.row("2026-08-17")])
        computed = pd.DataFrame([self.row("2026-08-17", 1)])
        with self.assertRaisesRegex(RuntimeError, "immutable diagnostic conflict"):
            merge_immutable(existing, computed)

    def test_prestart_row_is_forbidden(self):
        existing = pd.DataFrame([self.row(str((START - pd.Timedelta(days=1)).date()))])
        with self.assertRaisesRegex(RuntimeError, "pre-start"):
            merge_immutable(existing, pd.DataFrame(columns=LEDGER_COLUMNS))


if __name__ == "__main__":
    unittest.main()
