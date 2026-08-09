import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

import freeze_v9_rule_e
from forward_state_inventory import ACCOUNT_NAMES, inspect_forward_state


class ForwardStateInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="v9-forward-inventory-")
        self.forward = Path(self.temp.name) / "forward"
        self.manifest = {
            "combined_code_hash": "code-hash",
            "frozen_at_utc": "2026-07-12T00:00:00Z",
            "baseline_event_snapshot_hash": "event-hash",
        }
        for account in ACCOUNT_NAMES:
            account_dir = self.forward / "accounts" / account
            account_dir.mkdir(parents=True)
            state = {
                "account": account,
                "code_hash": "code-hash",
                "initialized_at_utc": "2026-07-12T00:00:00Z",
                "baseline_event_snapshot_hash": "event-hash",
            }
            (account_dir / "initial_state.json").write_text(json.dumps(state), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_genesis_has_no_integrity_issue(self):
        inventory = inspect_forward_state(self.forward, self.manifest)
        self.assertEqual(inventory["initial_states"], 4)
        self.assertEqual(inventory["completed_sessions"], 0)
        self.assertEqual(inventory["issues"], [])

    def test_partial_session_is_rejected(self):
        path = self.forward / "accounts" / "v9_e" / "2026-07-13_state.json"
        path.write_text(json.dumps({"account": "v9_e", "as_of": "2026-07-13"}), encoding="utf-8")
        inventory = inspect_forward_state(self.forward, self.manifest)
        self.assertIn("forward account date sets are inconsistent", inventory["issues"])

    def test_complete_session_requires_all_artifacts(self):
        for account in ACCOUNT_NAMES:
            path = self.forward / "accounts" / account / "2026-07-13_state.json"
            path.write_text(json.dumps({"account": account, "as_of": "2026-07-13"}), encoding="utf-8")
        reports = self.forward / "reports"
        reports.mkdir(parents=True)
        (reports / "shadow_report_2026-07-13.json").write_text("{}", encoding="utf-8")
        inventory = inspect_forward_state(self.forward, self.manifest)
        self.assertTrue(any("missing open execution artifact" in issue for issue in inventory["issues"]))
        self.assertTrue(any("missing close decision artifact" in issue for issue in inventory["issues"]))

    def test_freeze_replace_detects_genesis(self):
        with patch.object(freeze_v9_rule_e, "FORWARD_DIR", self.forward):
            self.assertTrue(freeze_v9_rule_e.forward_has_artifacts())
            with patch.object(sys, "argv", ["freeze_v9_rule_e.py", "--replace"]):
                with self.assertRaisesRegex(RuntimeError, "refusing --replace"):
                    freeze_v9_rule_e.main()

    def test_generation_paths_are_versioned_and_validated(self):
        frozen, forward = freeze_v9_rule_e.generation_paths("v9-20260718", Path(self.temp.name))
        self.assertEqual(frozen, Path(self.temp.name) / "generations" / "v9-20260718" / "frozen")
        self.assertEqual(forward, Path(self.temp.name) / "generations" / "v9-20260718" / "forward")
        with self.assertRaises(ValueError):
            freeze_v9_rule_e.generation_paths("../escape", Path(self.temp.name))


if __name__ == "__main__":
    unittest.main()
