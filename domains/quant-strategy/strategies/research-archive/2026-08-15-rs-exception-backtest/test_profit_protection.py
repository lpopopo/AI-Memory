from pathlib import Path
import runpy
import unittest


HERE = Path(__file__).resolve().parent
PROTECTION = runpy.run_path(str(HERE / "evaluate_profit_protection.py"))


class ProfitProtectionTests(unittest.TestCase):
    def test_path_signature_detects_exit_path_changes(self):
        one = {"trades": [{"signal_date": "2026-01-01", "symbol": "AAOI", "entry_date": "2026-01-02", "exit_date": "2026-01-10", "exit_reason": "signal"}]}
        two = {"trades": [{"signal_date": "2026-01-01", "symbol": "AAOI", "entry_date": "2026-01-02", "exit_date": "2026-01-08", "exit_reason": "profit_lock"}]}
        self.assertNotEqual(PROTECTION["path_signature"](one), PROTECTION["path_signature"](two))


if __name__ == "__main__":
    unittest.main()
