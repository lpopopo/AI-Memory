#!/usr/bin/env python3
"""Point-in-time attribution for the V9 information-to-execution funnel."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from validate_v9_information_strategy import load_data
from v9_information_strategy import V9Backtester,V9Config,load_event_store,load_evidence_store

HORIZONS=(5,20,60)

def main():
 panels,vix,meta=load_data();events,raw=load_event_store(ROOT/"datasets/v9_information_events.json");updates,_=load_evidence_store(ROOT/"datasets/v9_evidence_updates.json")
 close=panels["close"];engine=V9Backtester(panels,vix,events,V9Config(source_healthy=True),updates);rows=[]
 for event in events:
  available=close.index[close.index>=event.effective_at.normalize()]
  if available.empty:continue
  signal_date=available[0];loc=close.index.get_loc(signal_date)
  for symbol in event.symbols:
   if symbol not in close or pd.isna(close.at[signal_date,symbol]):continue
   row={"event_id":event.event_id,"symbol":symbol,"theme":event.theme,"first_seen":str(event.effective_at),"signal_date":str(signal_date.date())}
   for h in HORIZONS:
    if loc+h<len(close.index) and not pd.isna(close.iloc[loc+h][symbol]):
     own=float(close.iloc[loc+h][symbol]/close.iloc[loc][symbol]-1);bench=float(close.iloc[loc+h]["QQQ"]/close.iloc[loc]["QQQ"]-1)
     row[f"return_{h}d"]=own;row[f"excess_qqq_{h}d"]=own-bench
   max_score=-np.inf;confirmed=False;first_confirm=None
   for dt in close.index[loc:min(loc+21,len(close.index))]:
    if engine._event_for(symbol,dt)!=event:continue
    ok,path,technical=engine._setup(symbol,dt);heat=max(0,min(15,float(engine.market_heat.get(dt,0))/100*15))
    score=event.source_completeness+event.thesis_novelty+engine._fundamental_score(event,symbol,dt)+technical+heat-event.crowding_penalty
    if score>max_score:max_score=score
    if ok and first_confirm is None:confirmed=True;first_confirm=str(dt.date())
   row.update({"price_confirmed_20d":confirmed,"first_confirm":first_confirm,"max_score_20d":None if max_score==-np.inf else float(max_score),"qualified_70":bool(confirmed and max_score>=70)})
   rows.append(row)
 frame=pd.DataFrame(rows);unique=frame.sort_values("first_seen").drop_duplicates(["signal_date","symbol"],keep="last")
 summary={"event_count":len(events),"event_symbol_pairs":len(frame),"unique_symbol_signal_pairs":len(unique),"price_confirmed_pairs":int(unique.price_confirmed_20d.sum()),"qualified_pairs":int(unique.qualified_70.sum())}
 for h in HORIZONS:
  col=f"excess_qqq_{h}d";valid=unique[col].dropna() if col in unique else pd.Series(dtype=float)
  summary[f"{h}d"]={"observations":int(len(valid)),"mean_excess":float(valid.mean()) if len(valid) else None,"median_excess":float(valid.median()) if len(valid) else None,"win_rate":float((valid>0).mean()) if len(valid) else None}
 near=unique[unique.price_confirmed_20d & ~unique.qualified_70].sort_values("max_score_20d",ascending=False).head(10)
 out={"status":"descriptive_only_no_parameter_selection","point_in_time_rule":"local first-seen date","data_last_date":meta["last_date"],"summary":summary,"near_misses":near.to_dict("records")}
 (RESULTS_DIR/"v9_information_funnel_metrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 frame.to_csv(RESULTS_DIR/"v9_information_event_study.csv",index=False)
 lines=["# V9 资讯到执行漏斗", "", "本报告严格按本地首次发现时间计算，只做描述性归因，不用于17条可靠事件上的参数优化。相同股票、相同信号日的重复帖子只计一次，避免重复放大结果。", "", "## 漏斗", "", f"- 资讯事件：{len(events)}条", f"- 原始事件—股票组合：{len(frame)}组", f"- 去重股票—信号日组合：{len(unique)}组", f"- 20个交易日内完成价格确认：{summary['price_confirmed_pairs']}组", f"- 同时达到70分：{summary['qualified_pairs']}组", "", "## 相对QQQ事件表现", "", "| 期限 | 样本 | 平均超额 | 中位超额 | 胜率 |", "|---|---:|---:|---:|---:|"]
 for h in HORIZONS:
  x=summary[f"{h}d"];fmt=lambda v:"—" if v is None else f"{v:.2%}"
  lines.append(f"| {h}日 | {x['observations']} | {fmt(x['mean_excess'])} | {fmt(x['median_excess'])} | {fmt(x['win_rate'])} |")
 lines += ["", "## 解释", "", "选题超额衡量博主发现方向的价值；价格确认和70分门槛衡量量化执行是否允许下注。样本不足时，不因临界候选未成交而降低门槛。"]
 (RESULTS_DIR/"v9_information_funnel_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
