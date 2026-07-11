#!/usr/bin/env python3
"""Emit the latest auditable V9 research signal without changing formal V8."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parent;sys.path.insert(0,str(SCRIPTS))
from v9_data import ROOT,load_data
from v9_information_strategy import V9Backtester,V9Config,chronological_split,load_event_store,load_evidence_store
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--json",action="store_true");ap.add_argument("--assume-source-healthy",action="store_true",help="diagnostic only; never changes stored source health");args=ap.parse_args()
 panels,vix,meta=load_data();events,raw=load_event_store(ROOT/"datasets/v9_information_events.json");updates,_=load_evidence_store(ROOT/"datasets/v9_evidence_updates.json");healthy=raw["source_health"]=="healthy" or args.assume_source_healthy
 failed_on=next((x["start"] for x in raw.get("source_health_history",[]) if not str(x.get("status","")).startswith("healthy")),None)
 result=V9Backtester(panels,vix,events,V9Config(source_healthy=healthy,source_failure_date=None if args.assume_source_healthy else failed_on),updates).run();latest=result.audit[-1]
 out={"as_of":latest["date"],"version":"V9_unified_portfolio","source_health_stored":raw["source_health"],"source_health_used":"healthy" if healthy else raw["source_health"],"diagnostic_override":args.assume_source_healthy,"event_count":len(events),"validation_split":chronological_split(events),"qualified":latest["qualified"],"watchlist":latest["watchlist"],"stock_targets":latest["stock_targets"],"final_target":latest["final_target"],"drawdown":latest["drawdown"],"constraints":{"single_name_max":.20,"theme_max":.40,"max_names":5,"risk_per_name":.015,"no_leverage":True},"data_source":meta["source"]}
 print(json.dumps(out,ensure_ascii=False,indent=2) if args.json else "\n".join([f"V9 unified portfolio signal {out['as_of']}",f"source={out['source_health_used']} events={len(events)}",f"qualified={out['qualified']}",f"stock={out['stock_targets']}",f"final={out['final_target']}","human review required"]));
if __name__=="__main__":main()
