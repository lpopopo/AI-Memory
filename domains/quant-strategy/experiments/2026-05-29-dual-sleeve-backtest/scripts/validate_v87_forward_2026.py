#!/usr/bin/env python3
"""Frozen-parameter 2026 forward validation for V8, V8.5 and V8.7."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from robust_portfolio_engine import run_engine
from v81_dynamic_enhancer import rebalance_dates
from v85_heat_regime import V85Allocator,V85Config
from v87_dynamic_regime import V87Allocator,V87Config

OUT=ROOT/"datasets/data_v87_forward"
def download():
    OUT.mkdir(parents=True,exist_ok=True)
    raw=yf.download(["SPY","QQQ","^VIX","^VIX3M"],start="2000-01-01",end=None,auto_adjust=True,progress=False,threads=True)
    close=raw["Close"] if isinstance(raw.columns,pd.MultiIndex) else raw[["Close"]]
    close.index=pd.to_datetime(close.index).tz_localize(None);close=close.sort_index()
    close.to_csv(OUT/"market_adjusted_close.csv",index_label="Date")
    core_complete=close[["SPY","QQQ"]].dropna().index[-1]
    meta={"source":"Yahoo Finance via yfinance auto_adjust=True","downloaded_at_utc":pd.Timestamp.now(tz="UTC").isoformat(),"first_date":str(close.index[0].date()),"last_source_row":str(close.index[-1].date()),"last_complete_core_date":str(core_complete.date()),"non_null":{c:int(close[c].notna().sum()) for c in close}}
    (OUT/"metadata.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2));return close,meta
def stats(curve,start="2025-12-31"):
    x=curve.loc[start:].dropna();x=x/x.iloc[0];r=x.pct_change().dropna();dd=x/x.cummax()-1
    return {"total_return":float(x.iloc[-1]-1),"max_drawdown":float(dd.min()),"annualized_volatility":float(r.std()*np.sqrt(252)),"annualized_sharpe":float(r.mean()/r.std()*np.sqrt(252)) if r.std()>0 else 0.0,"final_value":float(x.iloc[-1])}
def main():
    data,meta=download();close=data[["SPY","QQQ"]].dropna();vix=data[["^VIX","^VIX3M"]].reindex(close.index).ffill()
    dates=rebalance_dates(close.index,"monthly")
    v8=run_engine(close,dates,ensemble_target_function(close),transaction_cost=.001)
    a85=V85Allocator(close,V85Config(.7,.03,None,.25,2));v85=run_engine(close,dates,a85.target,transaction_cost=.001)
    a87=V87Allocator(close,vix,V87Config(.7,70,75,.5,1));v87=run_engine(close,dates,a87.target,transaction_cost=.001)
    spy=(close.SPY/close.SPY.iloc[0]);qqq=(close.QQQ/close.QQQ.iloc[0])
    results={"V8":stats(v8.equity),"V8.5":stats(v85.equity),"V8.7":stats(v87.equity),"SPY":stats(spy),"QQQ":stats(qqq)}
    ytd_audit=[x for x in a87.audit if x["date"]>="2026-01-01"]
    out={"status":"forward_validation_parameters_frozen","data":meta,"period":{"start":"2025-12-31","end":meta["last_complete_core_date"]},"results":results,"v87_frozen_config":{"hot_qqq_weight":.7,"heat_threshold":70,"fear_threshold":75,"fear_multiplier":.5,"confirmation":1},"v87_2026_audit":ytd_audit,"latest_v87_signal":a87.audit[-1],"latest_v85_signal":a85.audit[-1],"limitations":["2026 sample is short and cannot establish statistical significance.","Sharpe is annualized from a partial year and is unstable.","Latest incomplete month signal is informational and has not executed until the next session close."]}
    path=RESULTS_DIR/"v87_forward_2026_metrics.json";path.write_text(json.dumps(out,ensure_ascii=False,indent=2));
    rows=[]
    for name,m in results.items():rows.append(f"| {name} | {m['total_return']:.2%} | {m['max_drawdown']:.2%} | {m['annualized_volatility']:.2%} | {m['annualized_sharpe']:.2f} |")
    audit=[]
    for x in ytd_audit:audit.append(f"| {x['date']} | {x['heat_score']:.1f} | {x['fear_score']:.1f} | {x['state']} | {x['target'].get('SPY',0):.0%} | {x['target'].get('QQQ',0):.0%} | {x['cash']:.0%} |")
    report=f"""# V8.7 2026前瞻验证\n\n参数在2025年数据结束后冻结，本报告没有重新优化。数据源：{meta['source']}；SPY/QQQ最新完整行情日：{meta['last_complete_core_date']}。\n\n## 结果\n\n| 模型 | 2026累计收益 | 最大回撤 | 年化波动 | 年化Sharpe* |\n|---|---:|---:|---:|---:|\n{chr(10).join(rows)}\n\n\\* 当前仅为短期样本，年化Sharpe非常不稳定，不作为晋级依据。\n\n## V8.7月度状态\n\n| 日期 | 热度 | 恐慌 | 状态 | SPY目标 | QQQ目标 | 现金 |\n|---|---:|---:|---|---:|---:|---:|\n{chr(10).join(audit)}\n\n## 当前结论\n\n验证已经启动，但样本不足，正式V8不变。V8.7继续按冻结参数记录，不因2026阶段结果调参。最新月尚未结束时，最后一行只作为即时研究信号，需到下一交易日收盘才执行。\n"""
    (RESULTS_DIR/"v87_forward_2026_report.md").write_text(report,encoding="utf-8")
    print(json.dumps({"data":meta,"results":results,"latest":a87.audit[-1]},ensure_ascii=False,indent=2));print(path)
if __name__=="__main__":main()
