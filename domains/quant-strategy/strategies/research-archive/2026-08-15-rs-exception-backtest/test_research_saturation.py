import tempfile
import unittest
from pathlib import Path

import evaluate_research_saturation as target


class ResearchSaturationTests(unittest.TestCase):
    def test_parse_decision_branches_ignores_header_and_prose(self):
        text = """# Register

| Branch | Objective | Evidence result | Status | Reopen trigger |
| --- | --- | --- | --- | --- |
| Alpha | Test A | Result | Rejected | Fresh data |
| Beta | Test B | Result | Frozen | Gate |

No order is authorized.
"""
        self.assertEqual(target.parse_decision_branches(text), {"Alpha", "Beta"})

    def test_count_closed_trades_requires_exit_date(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.csv"
            path.write_text(
                "symbol,entry_price,exit_date,return\n"
                "AAOI,100,,\n"
                "MU,90,2026-08-20,0.10\n",
                encoding="utf-8",
            )
            self.assertEqual(target.count_closed_trades(path), 1)

    def test_status_count_has_priority_over_ledger_fallback(self):
        self.assertEqual(
            target.closed_trades_from_status(
                {"promotion_gate": {"closed_trades": 7}},
                "promotion_gate",
                "does-not-need-to-exist.csv",
            ),
            7,
        )


if __name__ == "__main__":
    unittest.main()
