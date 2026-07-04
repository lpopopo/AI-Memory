import tempfile,unittest
from pathlib import Path
from run_v9_daily_execution import freeze_decision

class DailyExecutionTests(unittest.TestCase):
 def record(self,date="2026-07-02",digest="a"):return {"as_of":date,"decision_hash":digest}
 def test_same_decision_is_idempotent(self):
  p=Path(tempfile.mkdtemp())/"ledger.jsonl";self.assertEqual(freeze_decision(p,self.record()),"appended");self.assertEqual(freeze_decision(p,self.record()),"unchanged");self.assertEqual(len(p.read_text().splitlines()),1)
 def test_changed_frozen_decision_is_rejected(self):
  p=Path(tempfile.mkdtemp())/"ledger.jsonl";freeze_decision(p,self.record())
  with self.assertRaises(ValueError):freeze_decision(p,self.record(digest="b"))
 def test_historical_backfill_is_rejected(self):
  p=Path(tempfile.mkdtemp())/"ledger.jsonl";freeze_decision(p,self.record())
  with self.assertRaises(ValueError):freeze_decision(p,self.record(date="2026-07-01"))

if __name__=="__main__":unittest.main()
