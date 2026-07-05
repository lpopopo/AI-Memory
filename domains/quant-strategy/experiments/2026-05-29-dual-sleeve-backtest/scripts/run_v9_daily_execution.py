#!/usr/bin/env python3
"""Create an auditable V9 daily decision; this never sends an order."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
import pandas as pd

SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))

def stable_hash(value)->str:
 payload=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
 return hashlib.sha256(payload).hexdigest()

def freeze_decision(ledger:Path,record:dict)->str:
 existing=[]
 if ledger.exists():existing=[json.loads(x) for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()]
 same=[x for x in existing if x["as_of"]==record["as_of"]]
 if same:
  if same[0]["decision_hash"]!=record["decision_hash"]:raise ValueError(f"frozen decision changed for {record['as_of']}")
  return "unchanged"
 if existing and record["as_of"]<max(x["as_of"] for x in existing):raise ValueError("historical decision backfill is prohibited")
 ledger.parent.mkdir(parents=True,exist_ok=True)
 with ledger.open("a",encoding="utf-8") as f:f.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
 return "appended"

def build_decision()->dict:
 # Keep ledger/hash helpers importable without optional market-data packages.
 from validate_v9_information_strategy import load_data
 from v9_information_strategy import V9Backtester,V9Config,chronological_split,load_event_store,load_evidence_store
 panels,vix,meta=load_data();store=ROOT/"datasets/v9_information_events.json";evidence_store=ROOT/"datasets/v9_evidence_updates.json";events,raw=load_event_store(store);updates,_=load_evidence_store(evidence_store)
 failed_on=next((x["start"] for x in raw.get("source_health_history",[]) if not str(x.get("status","")).startswith("healthy")),None)
 healthy=raw["source_health"]=="healthy";cfg=V9Config(source_healthy=healthy,source_failure_date=failed_on)
 result=V9Backtester(panels,vix,events,cfg,updates).run();latest=result.audit[-1]
 queue=[]
 for item in latest["watchlist"]:
  reason=[]
  if not item["confirmed"]:reason.append("等待连续两日价格确认")
  if item["fundamental_validation"]<20:reason.append(f"补充一手验证：当前{item['fundamental_validation']}/20")
  if item["points_to_70"]>0:reason.append(f"距离入场线{item['points_to_70']:.2f}分")
  queue.append({**item,"next_work":reason})
 core={"as_of":latest["date"],"strategy":"V9_research","formal_strategy":"V8","order_authorized":False,"source_health":raw["source_health"],"source_failure_date":failed_on,"new_information_entries_allowed":latest["source_healthy"],"qualified":latest["qualified"],"research_queue":queue,"current_stock_targets":latest["stock_targets"],"next_target":latest["final_target"],"portfolio_drawdown":latest["drawdown"],"event_archive_hash":hashlib.sha256(store.read_bytes()).hexdigest(),"evidence_archive_hash":hashlib.sha256(evidence_store.read_bytes()).hexdigest(),"evidence_update_count":len(updates),"event_count":len(events),"validation_split":chronological_split(events),"market_data_last_date":meta["last_date"],"execution":"human review; signal close then next trading session; no automatic brokerage order"}
 core["decision_hash"]=stable_hash(core);return core

def main():
 parser=argparse.ArgumentParser();parser.add_argument("--ledger",type=Path,default=ROOT/"results/v9_forward_decisions.jsonl");parser.add_argument("--output-dir",type=Path,default=ROOT/"results/v9_daily");args=parser.parse_args()
 record=build_decision();status=freeze_decision(args.ledger,record);args.output_dir.mkdir(parents=True,exist_ok=True);path=args.output_dir/f"{record['as_of']}.json"
 if path.exists() and json.loads(path.read_text(encoding="utf-8"))["decision_hash"]!=record["decision_hash"]:raise ValueError("daily decision artifact is already frozen with different content")
 path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"freeze_status":status,"artifact":str(path),**record},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
