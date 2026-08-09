import unittest
import pandas as pd
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent))

from shadow_integrity import TamperAlarmException, digest, state_digest
import run_v9_shadow as runner
from freeze_v9_rule_e import RESULT_AFFECTING_FILES

ROOT = Path(__file__).resolve().parent.parent

class TestForwardIntegrity(unittest.TestCase):
    def test_manifest_covers_shared_risk_source_and_execution_modules(self):
        required = {
            "scripts/v9_fear_gate.py",
            "scripts/v9_source_health.py",
            "scripts/v9_account_allocator.py",
            "scripts/v9_signal.py",
            "scripts/run_v9_daily_execution.py",
            "scripts/test_v9_account_allocator.py",
            "scripts/test_v9_daily_execution.py",
            "validation/source-health-recovery-contract.md",
        }
        self.assertTrue(required.issubset(RESULT_AFFECTING_FILES))

    @classmethod
    def setUpClass(cls):
        cls.temp_root = Path(tempfile.mkdtemp(prefix="v9-forward-integrity-"))
        cls.shadow_dir = cls.temp_root / "shadow_portfolio"
        cls.frozen_dir = cls.shadow_dir / "frozen"
        cls.frozen_dir.mkdir(parents=True)

        source_frozen = ROOT / "results" / "shadow_portfolio" / "frozen"
        config = json.loads((source_frozen / "config.json").read_text(encoding="utf-8"))
        baseline = json.loads((source_frozen / "baseline_event_snapshot.json").read_text(encoding="utf-8"))
        cls.manifest = {
            "combined_code_hash": "isolated-forward-integrity-test",
            "baseline_event_snapshot_hash": digest(baseline),
            "frozen_at_utc": "2026-05-26T20:01:00Z",
            "forward_eligible": True,
            "files": {},
        }
        (cls.frozen_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")
        (cls.frozen_dir / "baseline_event_snapshot.json").write_text(
            json.dumps(baseline, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )
        (cls.frozen_dir / "code_manifest.json").write_text(
            json.dumps(cls.manifest, sort_keys=True), encoding="utf-8"
        )

        cls.run_id = "integrity"
        cls.dry_run_dir = cls.shadow_dir / "dry_run" / cls.run_id
        runner.initialize_mode_accounts(cls.dry_run_dir, "dry_run", cls.manifest, config)

        cls.patchers = [
            patch.object(runner, "SHADOW_DIR", cls.shadow_dir),
            patch.object(runner, "FROZEN_DIR", cls.frozen_dir),
            patch.object(runner, "verify_code_manifest", return_value=cls.manifest),
        ]
        for patcher in cls.patchers:
            patcher.start()

    @classmethod
    def tearDownClass(cls):
        for patcher in reversed(cls.patchers):
            patcher.stop()
        shutil.rmtree(cls.temp_root, ignore_errors=True)

    def test_a_e2e_scenario1(self):
        """initial_state -> Monday Close Decision (No execution on day 1)"""
        with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-27", "--dry-run", "--run-id", self.run_id]):
            runner.main()
            
        for acc in ["v8_base", "v9_a", "v9_e", "passive_50_50"]:
            exec_file = self.dry_run_dir / "executions" / acc / "2026-05-27_open_execution.json"
            self.assertTrue(exec_file.exists())
            exec_data = json.loads(exec_file.read_text())
            self.assertEqual(len(exec_data["rows"]), 0)
        report = json.loads((self.dry_run_dir / "reports" / "shadow_report_2026-05-27.json").read_text())
        self.assertFalse(report["source_health_audit"]["new_information_entries_allowed"])
        self.assertEqual(report["source_health_audit"]["eligible_event_count"], 0)
        self.assertFalse(report["broker_submission_enabled"])

    def test_b_e2e_scenario2(self):
        """Monday State -> Tuesday Open Execution -> Tuesday Close State"""
        with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-28", "--dry-run", "--run-id", self.run_id]):
            runner.main()
            
        for acc in ["v8_base", "v9_a", "v9_e", "passive_50_50"]:
            state_file = self.dry_run_dir / "accounts" / acc / "2026-05-28_state.json"
            self.assertTrue(state_file.exists())
            state = json.loads(state_file.read_text())
            prior = json.loads((self.dry_run_dir / "accounts" / acc / "2026-05-27_state.json").read_text())
            self.assertEqual(state["previous_state_hash"], state_digest(prior))

    def test_c_tampering_prior_state_edit(self):
        """Modifying prior state content triggers TamperAlarm"""
        state_file = self.dry_run_dir / "accounts" / "v9_e" / "2026-05-28_state.json"
        original = state_file.read_text()
        try:
            state = json.loads(original)
            state["cash"] = 999.0
            state_file.write_text(json.dumps(state))
            
            with self.assertRaises(TamperAlarmException) as context:
                with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-29", "--dry-run", "--run-id", self.run_id]):
                    runner.main()
            self.assertIn("prior state hash is invalid", str(context.exception))
        finally:
            state_file.write_text(original)

    def test_d_tampering_skip_day(self):
        """Skipping a trading day triggers TamperAlarm"""
        # May 29 is Friday. May 30, 31 are weekends. Let's try skipping May 29 and run June 1st (2026-06-01 is Monday).
        with self.assertRaises(TamperAlarmException) as context:
            with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-06-01", "--dry-run", "--run-id", self.run_id]):
                runner.main()
        self.assertIn("Skip day detected!", str(context.exception))

if __name__ == "__main__":
    unittest.main()
