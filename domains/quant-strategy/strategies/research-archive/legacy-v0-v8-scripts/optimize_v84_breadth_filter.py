#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,sys
from dataclasses import asdict
from pathlib import Path
import pandas as pd
SCRIPTS=Path(__file__).resolve().parent; ROOT=SCRIPTS.parent; sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_etf import DEV_START,DEV_END,OOS_START,END,load_etfs,rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v84_breadth_filter import V84Allocator,V84Config,build_breadth

def periods(x): return {"development_2006_2018":metrics(rebase(x,DEV_START,DEV_END)),"secondary_2019_2025":metrics(rebase(x,OOS_START,END)),"full_2006_2025":metrics(rebase(x,DEV_START,END))}
def run(close,cfg,breadth,cost=.001):
 a=V84Allocator(close,cfg,breadth); r=run_engine(close,rebalance_dates(close.index,"monthly"),a.target,transaction_cost=cost); return r,a
def main():
 close=load_etfs()[["SPY","QQQ"]].loc[DEV_START:END]
 pit=ROOT/"datasets/data_point_in_time"
 stocks=pd.read_csv(pit/"adjusted_close.csv",index_col=0,parse_dates=True).sort_index().loc[DEV_START:END]
 history=pd.read_csv(pit/"membership_history.csv"); history["symbol"]=history["symbol"].str.upper().str.replace(".","-",regex=False)
 history["opt-in"]=pd.to_datetime(history["opt-in"]); history["opt-out"]=pd.to_datetime(history["opt-out"])
 breadth={d:build_breadth(stocks,history,d) for d in (100,200)}
 cfgs=[V84Config()]+[V84Config(ma,t,m) for ma,t,m in itertools.product((100,200),(.4,.5,.6),(0,.5,.75))]
 candidates=[]; results={}; allocators={}
 for i,cfg in enumerate(cfgs):
  r,a=run(close,cfg,breadth.get(cfg.breadth_ma)); dev=periods(r.equity)["development_2006_2018"]; key=f"candidate_{i:02d}"
  candidates.append({"key":key,"config":asdict(cfg),"development":dev,"development_eligible":dev["max_drawdown"]>=-.30 and dev["sharpe"]>=.90,"turnover":r.diagnostics["total_turnover"]});results[key]=r;allocators[key]=a
 pool=[x for x in candidates if x["development_eligible"]] or [x for x in candidates if x["development"]["max_drawdown"]>=-.30]
 selected=max(pool or candidates,key=lambda x:x["development"]["cagr"]); r=results[selected["key"]]; selected["metrics"]=periods(r.equity); selected["latest_audit"]=allocators[selected["key"]].audit[-1]
 cfg=V84Config(**selected["config"]); costs={str(c):periods(run(close,cfg,breadth.get(cfg.breadth_ma),c)[0].equity) for c in (.001,.002,.005)}
 sec=selected["metrics"]["secondary_2019_2025"]; checks={"development_gate":selected["development_eligible"],"secondary_cagr":sec["cagr"]>=.17,"secondary_drawdown":sec["max_drawdown"]>=-.30,"secondary_sharpe":sec["sharpe"]>=.90}
 metadata=json.loads((pit/"metadata.json").read_text())
 out={"method":{"development":[DEV_START,DEV_END],"secondary":[OOS_START,END],"secondary_is_not_fresh_oos":True,"candidate_count":len(candidates),"membership_source":metadata["membership_source"],"price_source":metadata["price_source"],"residual_survivorship_bias":True,"transaction_cost":.001},"selected":selected,"development_eligible_count":sum(x["development_eligible"] for x in candidates),"all_candidates":candidates,"baseline_v8":periods(results["candidate_00"].equity),"cost_sensitivity":costs,"promotion_checks":checks,"promoted":all(checks.values())}
 path=RESULTS_DIR/"v84_breadth_filter_metrics.json";path.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({"selected":selected,"eligible_count":out["development_eligible_count"],"checks":checks},ensure_ascii=False,indent=2));print(path)
if __name__=="__main__":main()
