import unittest
import pandas as pd
import json
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent))

from shadow_integrity import TamperAlarmException, verify_genesis, verify_daily_state, digest, state_digest
from init_forward_accounts import main as init_accounts
from freeze_v9_rule_e import main as freeze_manifest
from run_v9_shadow import main as run_shadow

ROOT = Path(__file__).resolve().parent.parent
SHADOW_DIR = ROOT / "results" / "shadow_portfolio"
FORWARD_DIR = SHADOW_DIR / "forward"

class TestForwardIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            shutil.rmtree(FORWARD_DIR)
        except:
            pass
        
        with patch("sys.argv", ["freeze_v9_rule_e.py", "--replace"]):
            freeze_manifest()
            
        init_accounts()
        
        cls.manifest = json.loads((SHADOW_DIR / "frozen" / "code_manifest.json").read_text())
        cls.run_id = cls.manifest["combined_code_hash"][:8]
        cls.dry_run_dir = SHADOW_DIR / "dry_run" / cls.run_id
        
        # We need to initialize the dry_run genesis by copying forward
        if cls.dry_run_dir.exists():
            shutil.rmtree(cls.dry_run_dir)
        shutil.copytree(FORWARD_DIR, cls.dry_run_dir)

    def test_a_e2e_scenario1(self):
        """initial_state -> Monday Close Decision (No execution on day 1)"""
        with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-27", "--dry-run"]):
            run_shadow()
            
        for acc in ["v8_base", "v9_a", "v9_e", "passive_50_50"]:
            exec_file = self.dry_run_dir / "executions" / acc / "2026-05-27_open_execution.json"
            self.assertTrue(exec_file.exists())
            exec_data = json.loads(exec_file.read_text())
            self.assertEqual(len(exec_data["rows"]), 0)

    def test_b_e2e_scenario2(self):
        """Monday State -> Tuesday Open Execution -> Tuesday Close State"""
        with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-28", "--dry-run"]):
            run_shadow()
            
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
                with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-05-29", "--dry-run"]):
                    run_shadow()
            self.assertIn("prior state hash is invalid", str(context.exception))
        finally:
            state_file.write_text(original)

    def test_d_tampering_skip_day(self):
        """Skipping a trading day triggers TamperAlarm"""
        # May 29 is Friday. May 30, 31 are weekends. Let's try skipping May 29 and run June 1st (2026-06-01 is Monday).
        with self.assertRaises(TamperAlarmException) as context:
            with patch("sys.argv", ["run_v9_shadow.py", "--as-of", "2026-06-01", "--dry-run"]):
                run_shadow()
        self.assertIn("Skip day detected!", str(context.exception))

if __name__ == "__main__":
    unittest.main()
