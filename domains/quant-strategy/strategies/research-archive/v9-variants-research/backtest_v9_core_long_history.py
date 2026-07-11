#!/usr/bin/env python3
"""20-year V9 engine baseline without fabricated historical information events."""
from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd
import yfinance as yf

SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))
from backtest_dual_sleeve import RESULTS_DIR
from v9_evaluation import calculate_stats
from v9_information_strategy import V9Backtester,V9Config

WARMUP, START, END = "2005-01-01", "2006-01-03", "2025-12-30"

def series(symbol, field):
    data=yf.download(symbol,start=WARMUP,end="2025-12-31",auto_adjust=True,progress=False)
    if data.empty: raise ValueError(f"no data for {symbol}")
    value=data[field]
    return value.iloc[:,0] if isinstance(value,pd.DataFrame) else value

def main():
    fields={name:pd.DataFrame() for name in ("open","high","low","close","volume")}
    for symbol in ("SPY","QQQ"):
        for field,name in (("Open","open"),("High","high"),("Low","low"),("Close","close"),("Volume","volume")):
            fields[name][symbol]=series(symbol,field)
    index=fields["close"].dropna().index
    fields={name:frame.reindex(index) for name,frame in fields.items()}
    vix=pd.DataFrame({"^VIX":series("^VIX","Close")}).reindex(index).ffill()
    try: vix["^VIX3M"]=series("^VIX3M","Close").reindex(index).ffill()
    except Exception: vix["^VIX3M"]=vix["^VIX"]
    runs={}
    def metrics(curve):
        out=calculate_stats(curve)
        years=(len(curve)-1)/252
        out["cagr"]=(1+out["total_return"])**(1/years)-1 if years>0 else 0.0
        return out
    for name,cfg in {
        "V8_equivalent_full_core":V9Config(v8_core_weight=1.0,info_sleeve_weight=0.0,transaction_cost=.001),
        "V9_fallback_core_70pct":V9Config(v8_core_weight=.70,info_sleeve_weight=.30,transaction_cost=.001),
    }.items():
        result=V9Backtester(fields,vix,[],cfg,[]).run(warmup_start=WARMUP,trading_start=START,trading_end=END)
        runs[name]={"metrics":metrics(result.equity),"information_entries":0,"information_contribution":0.0,"execution":result.diagnostics["execution"]}
    static=(fields["close"]["SPY"].pct_change(fill_method=None).fillna(0)*.5+fields["close"]["QQQ"].pct_change(fill_method=None).fillna(0)*.5+1).cumprod().loc[START:END]
    runs["static_SPY_QQQ_50_50"]={"metrics":metrics(static),"information_entries":0,"information_contribution":0.0,"execution":"buy-and-hold comparator"}
    out={"status":"v9_engine_core_only_not_information_alpha","period":[START,END],"warmup_start":WARMUP,"data_source":"Yahoo Finance via yfinance auto_adjust=True","information_event_policy":"No historical V9 events were fabricated; the local event archive begins in 2026.","runs":runs,"limitation":"This validates only the V9 fallback/core portfolio mechanics over 20 years. It cannot validate V9/V9.1 information-stock alpha without a dated 2006-2025 event archive."}
    (RESULTS_DIR/"v9_core_only_20yr_metrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# V9 无资讯核心 20 年回测","",f"区间：{START} 至 {END}。没有伪造 2006–2025 的资讯事件，因此资讯交易均为 0；本报告只验证 V9 引擎的 SPY/QQQ 核心与现金回退。","", "| 版本 | 累计收益 | CAGR | 最大回撤 | 年化 Sharpe |", "| --- | ---: | ---: | ---: | ---: |"]
    for name,row in runs.items():
        m=row["metrics"];lines.append(f"| {name} | {m['total_return']:.2%} | {m['cagr']:.2%} | {m['max_drawdown']:.2%} | {m['annualized_sharpe']:.2f} |")
    lines += ["", "结论：这不是 V9 资讯 alpha 回测。完整 20 年 V9 验证需要逐条可追溯的历史资讯、首次可见时间和一手证据更新。"]
    (RESULTS_DIR/"v9_core_only_20yr_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
