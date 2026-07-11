#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parent;sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_etf import DEV_START,DEV_END,OOS_START,END,load_etfs,rebase
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v85_heat_regime import V85Allocator,V85Config

def configs():
 yield V85Config()
 for qqq,distance,vol,cold,confirm in itertools.product((.6,.7),(0,.03,.05),(None,.20,.25),(.25,.5),(1,2)):
  yield V85Config(qqq,distance,vol,cold,confirm)
def periods(x):return {"development_2006_2018":metrics(rebase(x,DEV_START,DEV_END)),"secondary_2019_2025":metrics(rebase(x,OOS_START,END)),"full_2006_2025":metrics(rebase(x,DEV_START,END))}
def run(close,cfg,cost=.001):
 a=V85Allocator(close,cfg);r=run_engine(close,rebalance_dates(close.index,"monthly"),a.target,transaction_cost=cost);return r,a
def rolling(x):
 rows=[]
 for y in range(2006,2024):
  z=x.loc[f"{y}-01-01":f"{y+2}-12-31"].dropna()
  if len(z)>=600:rows.append({"window":f"{y}-{y+2}",**metrics(z/z.iloc[0])})
 return rows
def stress(x):return {n:metrics(rebase(x,a,b)) for n,a,b in [("2008","2008-01-01","2008-12-31"),("2020","2020-01-01","2020-12-31"),("2022","2022-01-01","2022-12-31")]}
def main():
 close=load_etfs()[["SPY","QQQ"]].loc[DEV_START:END];candidates=[];results={};allocators={}
 for i,cfg in enumerate(configs()):
  r,a=run(close,cfg);dev=periods(r.equity)["development_2006_2018"];key=f"candidate_{i:02d}";eligible=dev["max_drawdown"]>=-.30 and dev["sharpe"]>=.90
  candidates.append({"key":key,"config":asdict(cfg),"development":dev,"development_eligible":eligible,"turnover":r.diagnostics["total_turnover"]});results[key]=r;allocators[key]=a
 pool=[x for x in candidates if x["development_eligible"]] or [x for x in candidates if x["development"]["max_drawdown"]>=-.30]
 selected=max(pool or candidates,key=lambda x:x["development"]["cagr"]);r=results[selected["key"]];a=allocators[selected["key"]]
 selected["metrics"]=periods(r.equity);selected["rolling_3y"]=rolling(r.equity);selected["stress"]=stress(r.equity);selected["state_frequency"]=dict(Counter(x["state"] for x in a.audit));selected["latest_audit"]=a.audit[-1]
 cfg=V85Config(**selected["config"]);costs={str(c):periods(run(close,cfg,c)[0].equity) for c in (.001,.002,.005)}
 sec=selected["metrics"]["secondary_2019_2025"];checks={"development_gate":selected["development_eligible"],"secondary_cagr":sec["cagr"]>=.17,"secondary_drawdown":sec["max_drawdown"]>=-.30,"secondary_sharpe":sec["sharpe"]>=.90}
 near=[x for x in candidates if x["development"]["max_drawdown"]>=-.30 and x["development"]["cagr"]>=selected["development"]["cagr"]-.01]
 out={"method":{"development":[DEV_START,DEV_END],"secondary":[OOS_START,END],"secondary_is_not_fresh_oos":True,"candidate_count":len(candidates),"selection":"maximize development CAGR after hard gates","asset_scope":["SPY","QQQ","cash"],"transaction_cost":.001,"no_leverage":True},"selected":selected,"development_eligible_count":sum(x["development_eligible"] for x in candidates),"near_optimal_count":len(near),"all_candidates":candidates,"baseline_v8":periods(results["candidate_00"].equity),"cost_sensitivity":costs,"promotion_checks":checks,"promoted":all(checks.values())}
 path=RESULTS_DIR/"v85_heat_regime_metrics.json";path.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({"selected":selected,"eligible_count":out["development_eligible_count"],"near_optimal_count":len(near),"checks":checks},ensure_ascii=False,indent=2));print(path)
if __name__=="__main__":main()
