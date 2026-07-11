#!/usr/bin/env python3
"""Produce the current V8 defensive-core target from completed daily bars."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

from v81_dynamic_enhancer import V81Config, run_signal_history


BASE_WEIGHTS = {"SPY": 0.50, "QQQ": 0.50}
V81_RESEARCH_CONFIG = V81Config(
    frequency="monthly", hysteresis=0.01, confirmation=1, floor_fraction=0.25
)


def target_from_close(close: pd.DataFrame) -> dict:
    if len(close) < 200:
        raise ValueError("at least 200 completed sessions are required")
    latest = close.iloc[-1]
    ma150 = close.rolling(150).mean().iloc[-1]
    ma200 = close.rolling(200).mean().iloc[-1]
    symbols = {}
    for symbol, base in BASE_WEIGHTS.items():
        votes = int(latest[symbol] > ma150[symbol]) + int(latest[symbol] > ma200[symbol])
        symbols[symbol] = {
            "close": float(latest[symbol]), "ma150": float(ma150[symbol]),
            "ma200": float(ma200[symbol]), "trend_votes": votes,
            "target_weight": base * votes / 2,
        }
    invested = sum(x["target_weight"] for x in symbols.values())
    return {
        "bar_date": str(close.index[-1].date()), "source": "Yahoo Finance via yfinance",
        "symbols": symbols, "target_equity_weight": invested,
        "target_cash_weight": 1 - invested,
    }


def target_v81_from_close(close: pd.DataFrame, config: V81Config = V81_RESEARCH_CONFIG) -> dict:
    required = ["SPY", "QQQ", "VT"]
    if len(close) < 200 or any(symbol not in close for symbol in required):
        raise ValueError("V8.1 requires at least 200 sessions for SPY, QQQ, and VT columns")
    audit, _allocator = run_signal_history(
        close[required], config, enhancer=True, include_incomplete_final=False
    )
    latest = close.iloc[-1]
    symbols = {}
    for symbol in required:
        symbols[symbol] = {
            "close": float(latest[symbol]),
            "target_weight": float(audit["target"].get(symbol, 0.0)),
        }
    return {
        "as_of_bar_date": str(close.index[-1].date()),
        "signal_rebalance_date": audit["date"],
        "source": "Yahoo Finance via yfinance",
        "status": "research_only_not_promoted",
        "config": {
            "frequency": config.frequency, "hysteresis": config.hysteresis,
            "confirmation": config.confirmation, "floor_fraction": config.floor_fraction,
        },
        "core_votes": audit["votes"],
        "enhancer": {
            "eligible": audit["eligible"], "scores": audit["scores"],
            "selected": audit["enhancer_selected"], "budget": audit["enhancer_budget"],
        },
        "symbols": symbols,
        "target_equity_weight": float(sum(audit["target"].values())),
        "target_cash_weight": float(audit["cash"]),
    }


def download_completed_close() -> pd.DataFrame:
    now_ny = datetime.now(ZoneInfo("America/New_York"))
    raw = yf.download(
        ["SPY", "QQQ", "VT"], start=(now_ny.date() - timedelta(days=500)).isoformat(),
        end=(now_ny.date() + timedelta(days=1)).isoformat(), auto_adjust=True,
        progress=False,
    )
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    if isinstance(close, pd.Series):
        close = close.to_frame()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    close = close.rename_axis("Date").dropna(subset=list(BASE_WEIGHTS))
    if now_ny.hour < 16 or (now_ny.hour == 16 and now_ny.minute < 15):
        close = close.loc[close.index.date < now_ny.date()]
    return close[["SPY", "QQQ", "VT"]]


def main():
    parser = argparse.ArgumentParser(description="Current V8 defensive-core signal")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--version", choices=["v8", "v8.1"], default="v8")
    args = parser.parse_args()
    close = download_completed_close()
    result = target_from_close(close) if args.version == "v8" else target_v81_from_close(close)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.version == "v8.1":
        print(f"V8.1 research signal as of {result['as_of_bar_date']} "
              f"(rebalance {result['signal_rebalance_date']}; {result['source']})")
        print(f"core votes={result['core_votes']} enhancer={result['enhancer']}")
        for symbol, item in result["symbols"].items():
            print(f"{symbol}: close={item['close']:.2f} target={item['target_weight']:.0%}")
        print(f"Total equity={result['target_equity_weight']:.0%} "
              f"cash={result['target_cash_weight']:.0%}")
        return
    print(f"V8 signal using completed bar {result['bar_date']} ({result['source']})")
    for symbol, item in result["symbols"].items():
        print(f"{symbol}: close={item['close']:.2f} MA150={item['ma150']:.2f} "
              f"MA200={item['ma200']:.2f} votes={item['trend_votes']}/2 "
              f"target={item['target_weight']:.0%}")
    print(f"Total equity={result['target_equity_weight']:.0%} "
          f"cash={result['target_cash_weight']:.0%}")


if __name__ == "__main__":
    main()
