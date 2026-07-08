import hashlib,json,tempfile,unittest
from pathlib import Path
import numpy as np,pandas as pd
from v9_information_strategy import PositionState,V9Backtester,V9Config,V9EvidenceUpdate,chronological_split,load_event_store,load_evidence_store

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
 def test_retrospective_event_uses_archive_observation_and_is_ineligible(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["retrospective_backfill"]={"archive_observed_at":i[-5].isoformat(),"event_ids":["e1"]};path.write_text(json.dumps(d));events,_=load_event_store(path)
  self.assertEqual(events[0].effective_at,i[-5]);self.assertFalse(events[0].point_in_time_eligible);self.assertEqual(chronological_split(events)["counts"]["retrospective_only"],1)
 def test_caps_and_no_leverage(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));r=V9Backtester(p,v,events,V9Config(source_healthy=True)).run();self.assertLessEqual(r.weights.drop(columns="cash").sum(axis=1).max(),1.000001);self.assertLessEqual(r.weights.get("X",pd.Series(0,index=i)).max(),.200001)
 def test_source_failure_blocks_new_entries(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));r=V9Backtester(p,v,events,V9Config(source_healthy=False)).run();self.assertTrue((r.weights.get("X",pd.Series(0,index=i))==0).all())
  self.assertLess(r.diagnostics["turnover"],30,"unchanged fallback targets must not rebalance daily")
 def test_dated_source_failure_preserves_earlier_archive(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));b=V9Backtester(p,v,events,V9Config(source_healthy=False,source_failure_date=str(i[-5].date())));self.assertIsNotNone(b._event_for("X",i[-4]))
 def test_hash_validation(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["events"][0]["content_hash"]="bad";path.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_event_store(path)
 def test_duplicate_event_identity_is_rejected(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["events"].append(dict(d["events"][0]));path.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_event_store(path)
 def test_invalid_symbol_is_rejected(self):
  i,_,_=self.synthetic();path=self.event_file(i[-20]);d=json.loads(path.read_text());d["events"][0]["symbols"]=["x"];path.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_event_store(path)
 def test_evidence_upgrade_is_point_in_time_and_non_additive(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));u=V9EvidenceUpdate("u",i[-10],("X",),"company_filing",18,"x");b=V9Backtester(p,v,events,V9Config(),[u]);self.assertEqual(b._fundamental_score(events[0],"X",i[-11]),20);self.assertEqual(b._fundamental_score(events[0],"X",i[-9]),20)
  weak=events[0].__class__(events[0].event_id,events[0].source,events[0].author,events[0].post_id,events[0].effective_at,events[0].content_hash,events[0].theme,events[0].symbols,events[0].source_completeness,events[0].thesis_novelty,8,events[0].crowding_penalty);b=V9Backtester(p,v,[weak],V9Config(),[u]);self.assertEqual(b._fundamental_score(weak,"X",i[-11]),8);self.assertEqual(b._fundamental_score(weak,"X",i[-9]),18)
 def test_evidence_store_rejects_commentary(self):
  summary="not primary";d={"updates":[{"update_id":"u","first_seen_at":"2026-01-01","symbols":["X"],"source_type":"blog_post","validation_score":20,"content_summary":summary,"content_hash":hashlib.sha256(summary.encode()).hexdigest()}]};f=Path(tempfile.NamedTemporaryFile(mode="w",delete=False).name);f.write_text(json.dumps(d))
  with self.assertRaises(ValueError):load_evidence_store(f)
 def test_drawdown_breakers(self):
  self.assertEqual(V9Config().risk_per_name,.015);self.assertEqual(V9Config().hard_stop,.08)
 def test_invalid_risk_limits(self):
  with self.assertRaises(ValueError):V9Config(max_single=.25)
 def test_common_factor_theme_exposure_is_aggregated(self):
  i,p,v=self.synthetic();p={k:df.assign(Y=df["X"]) for k,df in p.items()};b=V9Backtester(p,v,[],V9Config(aggregate_common_factors=True));b.value=100
  b.positions={"X":PositionState(10,1,9,"ai_interconnect",75,1),"Y":PositionState(10,2,9,"memory_storage",75,1)}
  exposure=b._theme_exposure(pd.Series({"X":10.,"Y":10.}));self.assertEqual(set(exposure),{"ai_capex"});self.assertAlmostEqual(exposure["ai_capex"],.30)
 def test_common_factor_aggregation_can_be_ablated(self):
  i,p,v=self.synthetic();b=V9Backtester(p,v,[],V9Config(aggregate_common_factors=False));self.assertEqual(b._theme_bucket("memory_storage"),"memory_storage")
 def test_institutional_triple_confirmation_rejects_weak_volume(self):
  i,p,v=self.synthetic();p["volume"].loc[i[-1],"X"]=1.;events,_=load_event_store(self.event_file(i[-30]));b=V9Backtester(p,v,events,V9Config(institutional_triple_confirmation=True));ok,_,_,reason,_=b._tech_setup("X",i[-1],events[0].effective_at.normalize());self.assertFalse(ok);self.assertEqual(reason,"institutional_triple_confirmation_failed")
 def test_flow_fragility_score_is_bounded(self):
  i,p,v=self.synthetic();events,_=load_event_store(self.event_file(i[-30]));b=V9Backtester(p,v,events,V9Config(institutional_flow_overlay=True));score=b._flow_fragility_score(i[-1]);self.assertGreaterEqual(score,0);self.assertLessEqual(score,10)
 def test_evidence_quality_position_multipliers(self):
  self.assertEqual(V9Backtester._quality_size_multiplier(10),.60);self.assertEqual(V9Backtester._quality_size_multiplier(12),.75);self.assertEqual(V9Backtester._quality_size_multiplier(15),1.0)
if __name__=="__main__":unittest.main()
