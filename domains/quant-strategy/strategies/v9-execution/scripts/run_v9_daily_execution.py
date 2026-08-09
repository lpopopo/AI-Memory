#!/usr/bin/env python3
"""Create an auditable V9 daily decision; this never sends an order."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
import pandas as pd

SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))

TERMINAL_ORDER_STATES={"filled","cancelled","canceled","rejected","expired"}
OPEN_ORDER_STATES={"new","open","pending","partially_filled","unknown"}

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
 if existing and record.get("previous_market_date") and max(x["as_of"] for x in existing)!=record["previous_market_date"]:raise ValueError("completed trading session was skipped; start a new generation instead of backfilling")
 ledger.parent.mkdir(parents=True,exist_ok=True)
 with ledger.open("a",encoding="utf-8") as f:f.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
 return "appended"

def append_account_audit(ledger:Path,audit:dict)->str:
 existing=[]
 if ledger.exists():existing=[json.loads(x) for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()]
 same=[x for x in existing if x["account_audit_hash"]==audit["account_audit_hash"]]
 if same:return "unchanged"
 ledger.parent.mkdir(parents=True,exist_ok=True)
 with ledger.open("a",encoding="utf-8") as f:f.write(json.dumps(audit,ensure_ascii=False,sort_keys=True)+"\n")
 return "appended"

def _position_shares(raw:dict)->dict[str,int]:
 positions={}
 for symbol,value in raw.items():
  shares=value.get("shares") if isinstance(value,dict) else value
  if isinstance(shares,bool) or int(shares)!=shares or shares<0:raise ValueError(f"invalid whole-share position: {symbol}")
  positions[str(symbol).strip().upper()]=int(shares)
 return positions

def build_action_ledger(as_of:str,required_actions:list[dict],orders:list[dict],reconciliation:dict,model_pending_orders:list[dict]|None=None,blocked_signals:list[dict]|None=None)->dict:
 rows=[];matched_order_indexes=set();as_of_dt=pd.Timestamp(as_of)
 normalized_orders=[{**order,"status":str(order.get("status","unknown")).lower(),"symbol":str(order.get("symbol","")).upper(),"side":str(order.get("side",order.get("action",""))).upper()} for order in orders]
 for required in required_actions:
  action_id=str(required.get("action_id",required.get("id","")))
  symbol=str(required.get("symbol","")).upper();side=str(required.get("side",required.get("action",""))).upper()
  matches=[(i,order) for i,order in enumerate(normalized_orders) if (action_id and order.get("action_id")==action_id) or (order["symbol"]==symbol and order["side"]==side)]
  for i,_ in matches:matched_order_indexes.add(i)
  statuses={order["status"] for _,order in matches}
  required_shares=required.get("shares");filled_shares=sum(float(order.get("filled_shares",order.get("shares",0))) for _,order in matches if order["status"]=="filled")
  fill_complete="filled" in statuses and (required_shares is None or filled_shares>=float(required_shares))
  execution_date=pd.Timestamp(required["execution_date"]) if required.get("execution_date") else None
  if fill_complete:category="executed_required_action";reason="confirmed_filled"
  elif statuses & OPEN_ORDER_STATES:category="required_action_open";reason="broker_order_not_terminal"
  elif execution_date is None or execution_date>as_of_dt:category="required_action_pending";reason="execution_window_not_due"
  else:category="missed_required_action";reason="required_execution_due_with_incomplete_fill" if filled_shares>0 else "required_execution_due_without_fill"
  rows.append({"action_id":action_id,"symbol":symbol,"side":side,"category":category,"reason":reason,"signal_date":required.get("signal_date"),"execution_date":required.get("execution_date"),"required_shares":required_shares,"filled_shares":filled_shares,"matched_order_states":sorted(statuses)})
 for i,order in enumerate(normalized_orders):
  if i not in matched_order_indexes:
   rows.append({"action_id":order.get("action_id",""),"symbol":order["symbol"],"side":order["side"],"category":"unmapped_broker_order_review","reason":"broker_order_has_no_required_action","matched_order_states":[order["status"]]})
 for pending in model_pending_orders or []:
  rows.append({"action_id":"","symbol":pending.get("symbol",""),"side":"MODEL","category":"model_action_pending_human_review","reason":pending.get("type","model_pending_order"),"target_weight":pending.get("weight")})
 for signal in blocked_signals or []:
  rows.append({"action_id":signal.get("signal_id",""),"symbol":signal.get("symbol",""),"side":signal.get("side",""),"category":"blocked_signal","reason":signal.get("reason","unspecified_gate")})
 if reconciliation.get("proposed_orders") and not reconciliation.get("order_authorized"):
  rows.append({"action_id":"","symbol":"PORTFOLIO","side":"RECONCILE","category":"blocked_signal","reason":reconciliation.get("authorization_reason","signal_not_authorized")})
 if "stock_sleeve_over_cap_no_new_stock_risk" in reconciliation.get("alerts",[]):
  rows.append({"action_id":"","symbol":"STOCK_SLEEVE","side":"BUY","category":"correct_skip","reason":"new_stock_risk_blocked_by_sleeve_cap"})
 if not rows:
  rows.append({"action_id":"","symbol":"PORTFOLIO","side":"NONE","category":"correct_skip","reason":"no_required_or_authorized_action"})
 counts={}
 for row in rows:counts[row["category"]]=counts.get(row["category"],0)+1
 return {"as_of":as_of,"rows":rows,"counts":counts,"has_missed_required_action":counts.get("missed_required_action",0)>0}

def build_account_audit(model_record:dict,account_state:dict,prices:dict[str,float])->dict:
 from v9_account_allocator import reconcile_whole_share_account
 model_as_of=pd.Timestamp(model_record["as_of"]);snapshot_as_of=pd.Timestamp(account_state["as_of"])
 if snapshot_as_of>model_as_of:raise ValueError("account snapshot is newer than completed model market data")
 positions=_position_shares(account_state.get("positions",{}));orders=list(account_state.get("orders",[]))
 unresolved=[order for order in orders if str(order.get("status","unknown")).lower() not in TERMINAL_ORDER_STATES]
 authorization=dict(account_state.get("authorization",{}));snapshot_exact=snapshot_as_of==model_as_of
 approved=bool(authorization.get("approved",False)) and snapshot_exact and not unresolved
 if not snapshot_exact:reason="stale_account_snapshot"
 elif unresolved:reason="unresolved_broker_order_veto"
 else:reason=str(authorization.get("reason","explicit_human_approval" if approved else "signal_not_authorized"))
 desired_core={symbol:float(model_record["next_target"].get(symbol,0.0)) for symbol in ("SPY","QQQ")}
 limits=model_record["portfolio_limits"]
 core_symbols=set(desired_core);stock_symbols=set(account_state.get("stock_symbols",set(positions)-core_symbols))
 reconciliation=reconcile_whole_share_account(cash=float(account_state["cash"]),positions=positions,prices=prices,desired_core_weights=desired_core,stock_symbols=stock_symbols,cash_floor=float(limits["cash_floor"]),stock_cap=float(limits["stock_cap"]),fee_per_order=float(account_state.get("fee_per_order",1.0)),order_authorized=approved,authorization_reason=reason)
 action_ledger=build_action_ledger(str(snapshot_as_of.date()),list(account_state.get("required_actions",[])),orders,reconciliation,list(model_record.get("model_pending_orders",[])),list(account_state.get("blocked_signals",[])))
 payload={"model_as_of":model_record["as_of"],"model_decision_hash":model_record["decision_hash"],"account_as_of":str(snapshot_as_of.date()),"account_observed_at":account_state.get("observed_at"),"account_snapshot_hash":stable_hash(account_state),"snapshot_exact":snapshot_exact,"unresolved_order_count":len(unresolved),"broker_submission_enabled":False,"reconciliation":reconciliation,"action_ledger":action_ledger}
 payload["account_audit_hash"]=stable_hash(payload);return payload

def build_decision()->dict:
 # Keep ledger/hash helpers importable without optional market-data packages.
 from v9_data import load_data
 from v9_information_strategy import V9Backtester,V9Config,chronological_split,load_event_store,load_evidence_store
 from v9_research_monitors import build_research_diagnostics
 from v9_source_health import build_source_health_audit
 panels,vix,meta=load_data();store=ROOT/"datasets/v9_information_events.json";evidence_store=ROOT/"datasets/v9_evidence_updates.json";events,raw=load_event_store(store);updates,_=load_evidence_store(evidence_store)
 failed_on=next((x["start"] for x in raw.get("source_health_history",[]) if not str(x.get("status","")).startswith("healthy")),None)
 health_audit=build_source_health_audit(raw,meta["last_date"]);healthy=health_audit["new_information_entries_allowed"];cfg=V9Config(source_healthy=healthy,source_failure_date=failed_on)
 result=V9Backtester(panels,vix,events,cfg,updates).run();latest=result.audit[-1]
 required=("qualified","watchlist","stock_targets","final_target","source_healthy","drawdown","date","fear_gate","portfolio_limits")
 missing=[key for key in required if key not in latest]
 if missing:raise KeyError(f"audit schema missing fields: {missing}")
 queue=[]
 for item in latest["watchlist"]:
  reason=[]
  if not item.get("confirmed"):reason.append("等待连续两日价格确认")
  fun=item.get("fundamental_validation",0)
  if fun<20:reason.append(f"补充一手验证：当前{fun}/20")
  if item.get("points_to_70",0)>0:reason.append(f"距离入场线{item['points_to_70']:.2f}分")
  if item.get("wait_rule"):reason.append(f"Rule E waitlist={item['wait_rule']}")
  queue.append({**item,"next_work":reason})
 as_of=pd.Timestamp(latest["date"])
 diagnostics=build_research_diagnostics(panels["close"],vix,as_of)
 previous_market_date=str(panels["close"].index[panels["close"].index.get_loc(as_of)-1].date()) if panels["close"].index.get_loc(as_of)>0 else None
 core={"as_of":latest["date"],"previous_market_date":previous_market_date,"strategy":"V9_unified_portfolio","order_authorized":False,"broker_submission_enabled":False,"source_health":raw["source_health"],"source_failure_date":failed_on,"source_health_audit":health_audit,"new_information_entries_allowed":healthy and latest["source_healthy"],"qualified":latest["qualified"],"research_queue":queue,"current_stock_targets":latest["stock_targets"],"next_target":latest["final_target"],"portfolio_drawdown":latest["drawdown"],"ma_regime":latest.get("ma_regime",{}),"fear_gate":latest["fear_gate"],"portfolio_limits":latest["portfolio_limits"],"model_pending_orders":latest.get("pending_orders",[]),"diagnostics":diagnostics,"event_archive_hash":hashlib.sha256(store.read_bytes()).hexdigest(),"evidence_archive_hash":hashlib.sha256(evidence_store.read_bytes()).hexdigest(),"evidence_update_count":len(updates),"event_count":len(events),"validation_split":chronological_split(events),"market_data_last_date":meta["last_date"],"execution":"human review; stock orders next-session open; V8 core next-session close; no automatic brokerage order"}
 core["decision_hash"]=stable_hash(core);return core

def main():
 parser=argparse.ArgumentParser();parser.add_argument("--ledger",type=Path,default=ROOT/"results/v9_forward_decisions.jsonl");parser.add_argument("--output-dir",type=Path,default=ROOT/"results/v9_daily");parser.add_argument("--account-state",type=Path);parser.add_argument("--account-audit-ledger",type=Path,default=ROOT/"results/v9_account_audits.jsonl");parser.add_argument("--account-output-dir",type=Path,default=ROOT/"results/v9_account_audits");args=parser.parse_args()
 record=build_decision();status=freeze_decision(args.ledger,record);args.output_dir.mkdir(parents=True,exist_ok=True);path=args.output_dir/f"{record['as_of']}.json"
 if path.exists() and json.loads(path.read_text(encoding="utf-8"))["decision_hash"]!=record["decision_hash"]:raise ValueError("daily decision artifact is already frozen with different content")
 path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
 output={"freeze_status":status,"artifact":str(path),**record}
 if args.account_state:
  from v9_data import load_data
  account_state=json.loads(args.account_state.read_text(encoding="utf-8"));panels,_,_=load_data();price_row=panels["close"].loc[pd.Timestamp(record["as_of"])]
  audit=build_account_audit(record,account_state,{symbol:float(value) for symbol,value in price_row.dropna().items()});audit_status=append_account_audit(args.account_audit_ledger,audit);args.account_output_dir.mkdir(parents=True,exist_ok=True);audit_path=args.account_output_dir/f"{audit['account_as_of']}-{audit['account_audit_hash'][:12]}.json"
  if not audit_path.exists():audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
  output.update({"account_audit_status":audit_status,"account_audit_artifact":str(audit_path),"account_audit":audit})
 print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
