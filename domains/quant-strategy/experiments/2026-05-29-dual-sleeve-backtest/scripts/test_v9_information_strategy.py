import hashlib,json,tempfile,unittest
from pathlib import Path
import numpy as np,pandas as pd
from v9_information_strategy import V9Backtester,V9Config,V9EvidenceUpdate,chronological_split,load_event_store,load_evidence_store

class V9Tests(unittest.TestCase):
 def synthetic(self):
  i=pd.bdate_range("2024-01-01",periods=320);spy=np.linspace(100,130,320);qqq=np.linspace(100,140,320);x=np.linspace(100,180,320)
  close=pd.DataFrame({"SPY":spy,"QQQ":qqq,"X":x},index=i);op=close*.998;high=close*1.01;low=close*.995;vol=pd.DataFrame({"SPY":1e6,"QQQ":1e6,"X":2e6},index=i)
  panels={"open":op,"high":high,"low":low,"close":close,"volume":vol};vix=pd.DataFrame({"^VIX":15.,"^VIX3M":18.},index=i);return i,panels,vix
 def event_file(self,date):
  summary="synthetic test event";digest=hashlib.sha256(summary.encode()).hexdigest();data={"schema_version":1,"source_health":"healthy","events":[{"event_id":"e1","source":"x","author":"a","post_id":"p","published_at":date.isoformat(),"first_seen_at":date.isoformat(),"content_summary":summary,"content_hash":digest,"theme":"t","symbols":["X"],"evidence_level":"high","primary_validation":"yes","source_completeness":20,"thesis_novelty":20,"fundamental_validation":20,"crowding_penalty":0}]}
  f=tempfile.NamedTemporaryFile(mode="w",suffix=".json",delete=False);json.dump(data,f);f.close();return Path(f.name)
 def test_event_threshold_blocks_optimization(self):
  i,_,_=self.synthetic();events,_=load_event_store(self.event_file(i[-20]));self.assertFalse(chronological_split(events)["eligible"])
 def test_first_seen_controls_point_in_time_replay(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["events"][0]["published_at"]=i[-40].isoformat();path.write_text(json.dumps(d));events,_=load_event_store(path);self.assertEqual(events[0].effective_at,i[-20])
 def test_caps_and_no_leverage(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));r=V9Backtester(p,v,events,V9Config(source_healthy=True)).run();self.assertLessEqual(r.weights.drop(columns="cash").sum(axis=1).max(),1.000001);self.assertLessEqual(max(a["stock_targets"].get("X",0) for a in r.audit),.200001)
  self.assertGreater(r.weights["X"].max(),0,"qualifying two-day pullback must be able to enter")
 def test_source_failure_blocks_new_entries(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));r=V9Backtester(p,v,events,V9Config(source_healthy=False)).run();self.assertTrue((r.weights.get("X",pd.Series(0,index=i))==0).all())
  self.assertLess(r.diagnostics["turnover"],30,"unchanged fallback targets must not rebalance daily")
 def test_dated_source_failure_preserves_earlier_archive(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));r=V9Backtester(p,v,events,V9Config(source_healthy=False,source_failure_date=str(i[-5].date()))).run();self.assertGreater(r.weights.get("X",pd.Series(0,index=i)).max(),0)
 def test_hash_validation(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["events"][0]["content_hash"]="bad";path.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_event_store(path)
 def test_evidence_upgrade_is_point_in_time_and_non_additive(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));u=V9EvidenceUpdate("u",i[-10],("X",),"company_filing",18,"x");b=V9Backtester(p,v,events,V9Config(),[u]);self.assertEqual(b._fundamental_score(events[0],"X",i[-11]),20);self.assertEqual(b._fundamental_score(events[0],"X",i[-9]),20)
  weak=events[0].__class__(events[0].event_id,events[0].source,events[0].author,events[0].post_id,events[0].effective_at,events[0].content_hash,events[0].theme,events[0].symbols,events[0].source_completeness,events[0].thesis_novelty,8,events[0].crowding_penalty);b=V9Backtester(p,v,[weak],V9Config(),[u]);self.assertEqual(b._fundamental_score(weak,"X",i[-11]),8);self.assertEqual(b._fundamental_score(weak,"X",i[-9]),18)
 def test_evidence_store_rejects_commentary(self):
  summary="not primary";d={"updates":[{"update_id":"u","first_seen_at":"2026-01-01","symbols":["X"],"source_type":"blog_post","validation_score":20,"content_summary":summary,"content_hash":hashlib.sha256(summary.encode()).hexdigest()}]};f=Path(tempfile.NamedTemporaryFile(mode="w",delete=False).name);f.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_evidence_store(f)
 def test_drawdown_breakers(self):
  from v9_information_strategy import PositionState
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));b=V9Backtester(p,v,events,V9Config(source_healthy=False));dt=i[-1];px=float(p["close"].at[dt,"X"])
  b.stock_targets={"X":.20};b.states={"X":PositionState(px,px*.92,px,"t",90)}
  target,_,_=b._compose(dt,-.16,False);self.assertLessEqual(target.get("X",0),.10+1e-9)
  target,_,_=b._compose(dt,-.21,False);self.assertLessEqual(sum(target.values()),.50+1e-9)
  target,_,_=b._compose(dt,-.26,False);self.assertNotIn("X",target)
 def test_invalid_risk_limits(self):
  with self.assertRaises(ValueError):V9Config(max_single=.25)
if __name__=="__main__":unittest.main()
