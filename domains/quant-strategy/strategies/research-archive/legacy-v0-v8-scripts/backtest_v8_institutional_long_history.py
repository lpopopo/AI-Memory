#!/usr/bin/env python3
"""Long-history V8 ablation for AQR trend confirmation and Citadel flow fragility."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import yfinance as yf

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from optimize_v8_core import ensemble_target_function
from optimize_v8_robust import metrics
from robust_portfolio_engine import run_engine
from test_v3_refined import month_end_dates

TICKERS = ["SPY", "QQQ", "SMH", "RSP", "IWM", "HYG", "LQD", "^VIX", "^VIX3M"]
START, DEV_END, TEST_START, TEST_END = "2010-01-01", "2018-12-31", "2019-01-01", "2025-12-31"


def load_ohlcv():
    close_path = ROOT / "datasets" / "institutional_v8_close_2009_2026.csv"
    volume_path = ROOT / "datasets" / "institutional_v8_volume_2009_2026.csv"
    if close_path.exists() and volume_path.exists():
        close = pd.read_csv(close_path, index_col=0, parse_dates=True)
        volume = pd.read_csv(volume_path, index_col=0, parse_dates=True)
        if set(TICKERS).issubset(close.columns) and close.index.max() >= pd.Timestamp("2026-07-02"):
            return close.sort_index(), volume.sort_index()
    raw = yf.download(TICKERS, start="2009-01-01", end="2026-07-03", auto_adjust=True, progress=False, threads=True)
    close = raw["Close"][TICKERS].dropna(subset=["SPY", "QQQ"])
    volume = raw["Volume"].reindex(close.index)[TICKERS]
    close.index = pd.to_datetime(close.index).tz_localize(None);volume.index=close.index
    close.to_csv(close_path);volume.to_csv(volume_path)
    return close, volume


def flow_fragility(close: pd.DataFrame) -> pd.Series:
    score = pd.Series(0, index=close.index, dtype=float)
    for ratio in ((close.RSP / close.SPY), (close.IWM / close.SPY), (close.HYG / close.LQD)):
        change = ratio.pct_change(21, fill_method=None)
        score += np.select([change <= -.05, change <= -.025], [2, 1], default=0)
    semi = (close.SMH / close.QQQ).pct_change(21, fill_method=None)
    score += np.select([semi >= .05, semi >= .02], [2, 1], default=0)
    extension = close.QQQ / close.QQQ.rolling(20).mean() - 1
    score += np.select([extension >= .08, extension >= .04], [2, 1], default=0)
    q5 = close.QQQ.pct_change(5, fill_method=None);v5=close["^VIX"].pct_change(5, fill_method=None)
    score += ((q5 > 0) & (v5 > 0)).astype(int) * 2
    return score.where(close[["SPY", "QQQ", "SMH", "^VIX"]].notna().all(axis=1))


def aqr_confirmed(close, volume, symbol, dt):
    price = close[symbol];ma20=price.rolling(20).mean();ma50=price.rolling(50).mean();vol20=volume[symbol].rolling(20).mean()
    benchmark = close.SPY if symbol == "QQQ" else close.RSP
    relative = (price / benchmark).pct_change(20, fill_method=None)
    values = [price.at[dt], ma20.at[dt], ma50.at[dt], volume.at[dt, symbol], vol20.at[dt], relative.at[dt]]
    if any(pd.isna(x) for x in values):
        return False
    return bool(price.at[dt] > ma20.at[dt] > ma50.at[dt] and relative.at[dt] > 0 and volume.at[dt, symbol] >= .8 * vol20.at[dt])


def target_path(close, volume, mode):
    base_fn = ensemble_target_function(close[["SPY", "QQQ"]]);monthly=set(month_end_dates(close.index));flow=flow_fragility(close)
    base={"SPY":0.,"QQQ":0.};state=dict(base);rows=[]
    pending_increase={"SPY":False,"QQQ":False}
    for dt in close.index:
        if dt in monthly:
            new=base_fn(dt)
            for s in ("SPY","QQQ"):
                pending_increase[s]=new[s]>state[s]+1e-12
                if new[s]<state[s]: state[s]=new[s]
            base=new
        for s in ("SPY","QQQ"):
            if not pending_increase[s] or base[s] <= state[s]+1e-12: continue
            trend_ok = True if mode not in {"aqr","combined"} else aqr_confirmed(close,volume,s,dt)
            if not trend_ok: continue
            multiplier=1.0
            if mode in {"citadel","combined"}:
                fs=flow.at[dt]
                multiplier=.5 if pd.notna(fs) and fs>=7 else .75 if pd.notna(fs) and fs>=4 else 1.0
            state[s]=state[s]+(base[s]-state[s])*multiplier
            # A scaled initial allocation is not repeatedly pyramided every day.
            if multiplier<1: pending_increase[s]=False
            elif state[s]>=base[s]-1e-12: pending_increase[s]=False
        rows.append({"date":dt,**state,"flow_fragility":flow.at[dt]})
    return pd.DataFrame(rows).set_index("date")


def run(close,volume,mode,cost=.001):
    targets=target_path(close,volume,mode);weights=targets[["SPY","QQQ"]];changed=weights.ne(weights.shift()).any(axis=1)
    result=run_engine(close[["SPY","QQQ"]],set(weights.index[changed]),lambda dt:weights.loc[dt].to_dict(),transaction_cost=cost)
    return result,targets


def periods(curve):
    return {"development_2010_2018":metrics(curve.loc[START:DEV_END]),"frozen_2019_2025":metrics(curve.loc[TEST_START:TEST_END]),"covid_2020":metrics(curve.loc["2020-01-01":"2020-12-31"]),"inflation_2022":metrics(curve.loc["2022-01-01":"2022-12-31"]),"forward_2026":metrics(curve.loc["2026-01-01":])}


def main():
    close,volume=load_ohlcv();close=close.loc[START:];volume=volume.reindex(close.index)
    modes=["baseline","aqr","citadel","combined"];runs={m:run(close,volume,m) for m in modes}
    output={"status":"development_and_frozen_ablation","periods":{"development":[START,DEV_END],"frozen":[TEST_START,TEST_END]},"variants":{m:{"metrics":periods(r[0].equity),"turnover":float(r[0].diagnostics["total_turnover"]),"executions":int(len(r[0].executions))} for m,r in runs.items()},"cost_sensitivity":{m:{str(c):periods(run(close,volume,m,c)[0].equity)["frozen_2019_2025"] for c in (.001,.002,.005)} for m in modes},"quality_module":"excluded because no point-in-time financial panel exists"}
    results=ROOT/"results";mp=results/"v8_institutional_long_history_metrics.json";rp=results/"v8_institutional_long_history_report.md";mp.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    def row(m,p):
        x=output["variants"][m]["metrics"][p];return f"| {m} | {x['cagr']:.2%} | {x['max_drawdown']:.2%} | {x['sharpe']:.2f} | {x['final_value']-1:.2%} | {output['variants'][m]['turnover']:.1f} |"
    dev="\n".join(row(m,"development_2010_2018") for m in modes);test="\n".join(row(m,"frozen_2019_2025") for m in modes)
    rp.write_text(f"""# V8四大机构覆盖层长历史回测

## 开发期2010–2018
|版本|CAGR|最大回撤|Sharpe|累计收益|全期换手|
|---|---:|---:|---:|---:|---:|
{dev}

## 冻结期2019–2025
|版本|CAGR|最大回撤|Sharpe|累计收益|全期换手|
|---|---:|---:|---:|---:|---:|
{test}

AQR只控制V8风险增加时的趋势/相对强度/成交量确认；Citadel只缩放新增风险，不机械卖出现有持仓。GMO/Man质量模块因缺少点时财务面板未进入本轮长历史回测。
""",encoding="utf-8")
    print(json.dumps({"metrics":str(mp),"report":str(rp)},ensure_ascii=False,indent=2))


if __name__=="__main__":main()
