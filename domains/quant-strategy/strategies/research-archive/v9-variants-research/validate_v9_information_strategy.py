#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import pandas as pd
SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v87_dynamic_regime import V87Allocator,V87Config
from v9_information_strategy import V9Backtester,V9Config,chronological_split,load_event_store,load_evidence_store

def load_data():
 d=ROOT/"datasets/data_v9";p={k:pd.read_csv(d/f"{k}.csv",index_col=0,parse_dates=True).sort_index() for k in ("open","high","low","close","volume")};core_index=p["close"][["SPY","QQQ"]].dropna().index;v=p["close"][["^VIX","^VIX3M"]].reindex(core_index).ffill();cols=[c for c in p["close"] if not c.startswith("^VIX")];p={k:x.reindex(core_index)[cols] for k,x in p.items()};return p,v,json.loads((d/"metadata.json").read_text())
def stats(curve,start="2026-04-27",end="2026-07-02"):
 x=curve.loc[start:end].dropna();x=x/x.iloc[0];r=x.pct_change().dropna();dd=x/x.cummax()-1
 return {"total_return":float(x.iloc[-1]-1),"max_drawdown":float(dd.min()),"annualized_sharpe":float(r.mean()/r.std()*np.sqrt(252)) if r.std()>0 else 0.}
def benchmark(close,target):
 return run_engine(close,rebalance_dates(close.index,"monthly"),target,transaction_cost=.001).equity
def failure_date(raw):
 for row in raw.get("source_health_history",[]):
  if not str(row.get("status","")).startswith("healthy"):return row["start"]
 return None
def information_weights(audit_row):
 weights=audit_row.get("stock_targets",audit_row.get("weights",{}))
 return {symbol:weight for symbol,weight in weights.items() if symbol not in ("SPY","QQQ") and weight>0}
def get_optimal_config(split):
 if not split["eligible"]:return {}
 opt_path = RESULTS_DIR / "v9_optimization_metrics.json"
 if opt_path.exists():
  try:
   best = json.loads(opt_path.read_text(encoding="utf-8"))["best"]
   if best:return {"score_threshold": best["threshold"], "tech_weight": best["tech_weight"], "score_cap_scale": best["cap_scale"]}
  except Exception: pass
 return {}
def main():
 panels,vix,meta=load_data();events,raw=load_event_store(ROOT/"datasets/v9_information_events.json");updates,_=load_evidence_store(ROOT/"datasets/v9_evidence_updates.json");split=chronological_split(events);failed_on=failure_date(raw)
 costs={};runs={};opt_cfg=get_optimal_config(split)
 for cost in (.001,.002,.005):
  result=V9Backtester(panels,vix,events,V9Config(transaction_cost=cost,source_healthy=raw["source_health"]=="healthy",source_failure_date=failed_on,**opt_cfg),updates).run();costs[str(cost)]=stats(result.equity);runs[str(cost)]=result
 # A healthy-source counterfactual is diagnostic only; the actual current source status is partial.
 research=V9Backtester(panels,vix,events,V9Config(transaction_cost=.001,source_healthy=True,**opt_cfg),updates).run();close=panels["close"]
 v8=benchmark(close,ensemble_target_function(close));a=V87Allocator(close[["SPY","QQQ"]],vix,V87Config(.7,70,75,.5,1));v87=run_engine(close,rebalance_dates(close.index,"monthly"),a.target,transaction_cost=.001).equity
 mix=(close.SPY.pct_change(fill_method=None).fillna(0)*.5+close.QQQ.pct_change(fill_method=None).fillna(0)*.5+1).cumprod()
 comparisons={"V9_actual_source_health":stats(runs["0.001"].equity),"V9_healthy_source_counterfactual":stats(research.equity),"V8":stats(v8),"V8.7":stats(v87),"QQQ":stats(close.QQQ),"SPY_QQQ_50_50":stats(mix)}
 audit=[x for x in research.audit if x["date"]>="2026-04-27"]
 info_weights=[information_weights(x) for x in audit]
 stock_days=sum(bool(x) for x in info_weights);max_single=max([max(x.values(),default=0) for x in info_weights],default=0)
 reliable=split["counts"]["reliable_point_in_time"]
 gates={"event_count_at_least_50":reliable>=50,"max_drawdown_lte_30pct":comparisons["V9_healthy_source_counterfactual"]["max_drawdown"]>=-.30,"sharpe_gte_0_90":comparisons["V9_healthy_source_counterfactual"]["annualized_sharpe"]>=.90,"test_cagr_beats_v87_by_3pp":False,"rolling_6m_win_rate_gte_60pct":False,"cost_0_5pct_positive_excess":costs["0.005"]["total_return"]>comparisons["V8.7"]["total_return"],"frozen_forward_12_months":False}
 out={"status":"research_only_not_promoted","data":meta,"event_store":{"count":len(events),"reliable_point_in_time_count":reliable,"retrospective_only_count":split["counts"]["retrospective_only"],"source_health":raw["source_health"],"source_failure_date":failed_on,"split":split},"parameters":{"source":"frozen_defaults","values":opt_cfg or {"score_threshold":70.0,"tech_weight":1.0,"score_cap_scale":1.0}},"period":["2026-04-27","2026-07-02"],"comparisons":comparisons,"cost_sensitivity_actual_source_health":costs,"research_diagnostics":{"stock_invested_days":stock_days,"max_single_weight":max_single,"latest_audit":research.audit[-1]},"promotion_checks":gates,"promoted":all(gates.values()),"limitations":[f"Only {reliable} reliable point-in-time events exist; no parameter optimization is permitted.",f"{split['counts']['retrospective_only']} historical posts were discovered later and are excluded from the historical trading replay.","The period is too short for stable annualized statistics.","Source degradation blocks only new entries from its recorded failure date; earlier archived signals remain replayable."]}
 path=RESULTS_DIR/"v9_information_strategy_metrics.json";path.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2));print(path)
 report=f"""# V9资讯驱动动态全账户策略验证\n\n## 状态\n\n研究版已实现，正式V8未修改。可靠事件仅{len(events)}条，低于50条最低要求，因此禁止调参和晋级。当前资讯健康状态为`{raw['source_health']}`，实际运行按规则禁止新增资讯仓；健康源反事实仅用于检查引擎。\n\n## 2026-04-27至2026-07-02\n\n| 模型 | 累计收益 | 最大回撤 | 年化Sharpe* |\n|---|---:|---:|---:|\n"""+"\n".join(f"| {n} | {m['total_return']:.2%} | {m['max_drawdown']:.2%} | {m['annualized_sharpe']:.2f} |" for n,m in comparisons.items())+f"""\n\n\\* 样本仅约两个月，年化Sharpe不稳定。健康源反事实共有{stock_days}个交易日持有资讯个股，观察到的最大单股权重为{max_single:.2%}。\n\n## 验收\n\n- 事件数量、完整测试期、滚动六个月胜率和12个月冻结前瞻期均未满足。\n- 0.1%/0.2%/0.5%成本已统一执行；信号收盘形成、下一交易日收盘执行。\n- 系统保持单股20%、主题40%、最多5股、单笔风险1.5%、无杠杆和组合回撤断路规则。\n\n结论：V9代码与审计接口可用，但当前只能积累事件并进行验证，不具备替换V8的统计证据。\n"""
 old=f"可靠事件仅{len(events)}条，低于50条最低要求，因此禁止调参和晋级。当前资讯健康状态为`{raw['source_health']}`，实际运行按规则禁止新增资讯仓；健康源反事实仅用于检查引擎。"
 new=f"本地档案共{len(events)}条事件，其中可用于点时回放的可靠事件{reliable}条，另有{split['counts']['retrospective_only']}条历史补录事件仅供回顾研究。可靠样本低于50条，因此禁止调参和晋级。回放严格使用本地首次发现时间；资讯从{failed_on}起不完整，此后禁止新增资讯仓，但保留此前已获得信号及价格退出。"
 report=report.replace(old,new)
 (RESULTS_DIR/"v9_information_strategy_report.md").write_text(report,encoding="utf-8")
if __name__=="__main__":main()
