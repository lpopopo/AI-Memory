import tempfile,unittest
from pathlib import Path
from run_v9_daily_execution import append_account_audit,build_account_audit,build_action_ledger,freeze_decision

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
 def test_skipped_completed_session_is_rejected(self):
  p=Path(tempfile.mkdtemp())/"ledger.jsonl";freeze_decision(p,self.record(date="2026-07-01"))
  with self.assertRaises(ValueError):freeze_decision(p,{"as_of":"2026-07-03","previous_market_date":"2026-07-02","decision_hash":"b"})
 def test_account_audit_chain_is_append_only_and_idempotent(self):
  p=Path(tempfile.mkdtemp())/"audits.jsonl";audit={"account_audit_hash":"x","account_as_of":"2026-08-07"}
  self.assertEqual(append_account_audit(p,audit),"appended");self.assertEqual(append_account_audit(p,audit),"unchanged");self.assertEqual(len(p.read_text().splitlines()),1)
 def test_required_action_due_without_fill_is_a_missed_operation(self):
  ledger=build_action_ledger("2026-08-07",[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","signal_date":"2026-07-31","execution_date":"2026-08-03"}],[],{"alerts":[],"proposed_orders":[],"order_authorized":False})
  self.assertTrue(ledger["has_missed_required_action"]);self.assertEqual(ledger["counts"]["missed_required_action"],1)
 def test_open_order_is_not_prematurely_called_missed(self):
  ledger=build_action_ledger("2026-08-07",[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","execution_date":"2026-08-03"}],[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","status":"open"}],{"alerts":[],"proposed_orders":[],"order_authorized":False})
  self.assertFalse(ledger["has_missed_required_action"]);self.assertEqual(ledger["counts"]["required_action_open"],1)
 def test_filled_required_action_closes_the_loop(self):
  ledger=build_action_ledger("2026-08-07",[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","execution_date":"2026-08-03"}],[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","status":"filled"}],{"alerts":[],"proposed_orders":[],"order_authorized":False})
  self.assertFalse(ledger["has_missed_required_action"]);self.assertEqual(ledger["counts"]["executed_required_action"],1)
 def test_terminal_partial_fill_remains_a_missed_required_action(self):
  ledger=build_action_ledger("2026-08-07",[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","shares":2,"execution_date":"2026-08-03"}],[{"action_id":"v8-spy","symbol":"SPY","side":"BUY","shares":1,"status":"filled"}],{"alerts":[],"proposed_orders":[],"order_authorized":False})
  self.assertTrue(ledger["has_missed_required_action"]);self.assertEqual(ledger["rows"][0]["reason"],"required_execution_due_with_incomplete_fill")
 def test_account_audit_never_enables_broker_submission(self):
  model={"as_of":"2026-08-07","decision_hash":"d","next_target":{"SPY":.35,"QQQ":.35},"portfolio_limits":{"cash_floor":.05,"stock_cap":.25},"model_pending_orders":[]}
  state={"as_of":"2026-08-07","cash":3756.49,"positions":{"GLW":2,"MXL":6,"MRVL":4,"QCOM":2},"stock_symbols":["GLW","MXL","MRVL","QCOM"],"orders":[],"required_actions":[],"authorization":{"approved":False,"reason":"late_fill_not_authorized"}}
  prices={"GLW":165.68,"MXL":74.98,"MRVL":218.72,"QCOM":167.86,"SPY":773.26,"QQQ":723.03};audit=build_account_audit(model,state,prices)
  self.assertFalse(audit["broker_submission_enabled"]);self.assertEqual(audit["reconciliation"]["executable_orders"],[]);self.assertTrue(audit["action_ledger"]["counts"]["blocked_signal"]>=1)
 def test_future_account_snapshot_is_rejected_against_stale_market_data(self):
  model={"as_of":"2026-08-06","decision_hash":"d","next_target":{"SPY":.35,"QQQ":.35},"portfolio_limits":{"cash_floor":.05,"stock_cap":.25}}
  with self.assertRaises(ValueError):build_account_audit(model,{"as_of":"2026-08-07","cash":1,"positions":{}},{"SPY":1,"QQQ":1})

if __name__=="__main__":unittest.main()
