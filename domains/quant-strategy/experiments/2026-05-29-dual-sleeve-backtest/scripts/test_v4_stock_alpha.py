#!/usr/bin/env python3
import json
import time
from dataclasses import dataclass

import pandas as pd

from backtest_dual_sleeve import (
    DATA_DIR,
    RESULTS_DIR,
    fetch_close_prices,
    fetch_symbol_close,
    pct,
    run_buy_hold,
    summarize,
)
from validate_dual_sleeve import SPLITS, slice_curve


SECTOR_LEADERS = {
    "XLK": ["AAPL", "MSFT", "AVGO"],
    "SMH": ["NVDA", "TSM", "AMD"],
    "XLC": ["META", "GOOGL", "NFLX"],
    "XLY": ["AMZN", "TSLA", "HD"],
    "XLF": ["JPM", "BAC", "MS"],
    "XLV": ["LLY", "UNH", "ABBV"],
    "XLI": ["GE", "CAT", "HON"],
    "XLE": ["XOM", "CVX", "COP"],
    "XLP": ["PG", "COST", "KO"],
    "XLB": ["LIN", "SHW", "APD"],
    "XLU": ["NEE", "SO", "DUK"],
    "XLRE": ["PLD", "AMT", "EQIX"],
    "IBB": ["REGN", "VRTX", "AMGN"],
    "ITA": ["RTX", "LMT", "GD"],
}

VALUE_ETFS = ["VTV", "IWD", "SCHD"]
TACTICAL_POOL = ["QQQ", "SMH", "XLK", "XLC", "XLY", "XLI", "XLF", "XLV", "IBB", "ITA"]
ALL_LEADER_STOCKS = sorted(set(s for leaders in SECTOR_LEADERS.values() for s in leaders))


@dataclass(frozen=True)
class V4Config:
    name: str
    bull_value_weight: float
    bull_growth_weight: float
    normal_value_weight: float
    normal_growth_weight: float
    bear_value_weight: float
    bear_growth_weight: float
    bull_rule: str
    bear_rule: str
    stock_top_n: int
    value_mode: str
    score_mode: str
    fallback: str


def fetch_all_data():
    # 1. Fetch ETF close prices
    etf_close = fetch_close_prices()
    
    # 2. Fetch stock close prices
    stock_series = {}
    failures = {}
    print(f"Checking/downloading individual leader stocks: {len(ALL_LEADER_STOCKS)} symbols...")
    for symbol in ALL_LEADER_STOCKS:
        try:
            stock_series[symbol] = fetch_symbol_close(symbol)
        except Exception as err:
            failures[symbol] = str(err)
            print(f"Failed to fetch {symbol}: {err}")
            
    if failures:
        (DATA_DIR / "stock_download_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
        
    stocks_df = pd.concat(stock_series, axis=1)
    stocks_df.columns = list(stock_series.keys())
    stocks_df = stocks_df.sort_index()
    stocks_df.index = pd.to_datetime(stocks_df.index).tz_localize(None)
    
    # 3. Combine both
    combined = pd.concat([etf_close, stocks_df], axis=1)
    combined = combined.sort_index()
    combined = combined.dropna(subset=["SPY", "QQQ"]) # Align on trading days
    return combined


def month_end_dates(index):
    periods = index.to_period("M")
    return {dt for i, dt in enumerate(index) if i == len(index) - 1 or periods[i + 1] != periods[i]}


def prepare_indicators(close):
    returns = close.pct_change(fill_method=None).fillna(0.0)
    return {
        "returns": returns,
        "ma50": close.rolling(50).mean(),
        "ma100": close.rolling(100).mean(),
        "ma200": close.rolling(200).mean(),
        "mom21": close / close.shift(21) - 1.0,
        "mom63": close / close.shift(63) - 1.0,
        "mom126": close / close.shift(126) - 1.0,
        "mom252": close / close.shift(252) - 1.0,
        "vol126": returns.rolling(126).std(),
        "vol252": returns.rolling(252).std(),
    }


def is_bull(config, close, indicators, dt):
    qqq = close.at[dt, "QQQ"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    qqq_m126 = indicators["mom126"].at[dt, "QQQ"]
    return pd.notna(qqq_ma200) and pd.notna(qqq_m126) and qqq > qqq_ma200 and qqq_m126 > 0


def is_bear(config, close, indicators, dt):
    spy = close.at[dt, "SPY"]
    qqq = close.at[dt, "QQQ"]
    spy_ma200 = indicators["ma200"].at[dt, "SPY"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    spy_m63 = indicators["mom63"].at[dt, "SPY"]
    qqq_m63 = indicators["mom63"].at[dt, "QQQ"]
    return (
        pd.notna(spy_ma200)
        and pd.notna(qqq_ma200)
        and pd.notna(spy_m63)
        and pd.notna(qqq_m63)
        and spy < spy_ma200
        and qqq < qqq_ma200
        and spy_m63 < 0
        and qqq_m63 < 0
    )


def value_weights(config, close, indicators, dt, target_total):
    ranked = []
    for symbol in VALUE_ETFS:
        if symbol not in close.columns or pd.isna(close.at[dt, symbol]):
            continue
        m63 = indicators["mom63"].at[dt, symbol]
        m126 = indicators["mom126"].at[dt, symbol]
        if pd.notna(m63) and pd.notna(m126):
            ranked.append((m63 + m126, symbol))
    ranked.sort(reverse=True)
    selected = [s for _, s in ranked[:2]] if ranked else VALUE_ETFS
    return {symbol: target_total / len(selected) for symbol in selected}


def growth_weights(config, close, indicators, dt, target_total, bull):
    # 1. Select top 2 tactical sectors/ETFs
    ranked_sectors = []
    for sector in TACTICAL_POOL:
        if sector not in close.columns or pd.isna(close.at[dt, sector]):
            continue
        m63 = indicators["mom63"].at[dt, sector]
        m126 = indicators["mom126"].at[dt, sector]
        if pd.notna(m63) and pd.notna(m126):
            ranked_sectors.append((m63 + m126, sector))
    ranked_sectors.sort(reverse=True)
    selected_sectors = [sec for _, sec in ranked_sectors[:2]]
    
    # 2. Retrieve candidate stock pool
    candidate_stocks = []
    for sector in selected_sectors:
        leaders = SECTOR_LEADERS.get(sector, [])
        candidate_stocks.extend(leaders)
    candidate_stocks = sorted(set(candidate_stocks))
    
    # 3. Filter and rank candidate stocks
    eligible_stocks = []
    for stock in candidate_stocks:
        if stock not in close.columns or pd.isna(close.at[dt, stock]):
            continue
        stock_close = close.at[dt, stock]
        stock_ma50 = indicators["ma50"].at[dt, stock]
        stock_m63 = indicators["mom63"].at[dt, stock]
        stock_m126 = indicators["mom126"].at[dt, stock]
        
        # Stock-level trend & momentum filters
        if pd.notna(stock_ma50) and stock_close > stock_ma50:
            if pd.notna(stock_m63) and stock_m63 > 0:
                score = stock_m63 + stock_m126 if pd.notna(stock_m126) else stock_m63
                eligible_stocks.append((score, stock))
                
    eligible_stocks.sort(reverse=True)
    selected_stocks = [s for _, s in eligible_stocks[:config.stock_top_n]]
    
    # 4. Fallback to cash if fewer stocks qualify
    if not selected_stocks:
        if config.fallback == "cash":
            return {}
        else:
            return {"QQQ": target_total}
            
    # Equal-weight the selected stocks
    return {symbol: target_total / len(selected_stocks) for symbol in selected_stocks}


def combine_weights(*groups):
    weights = {}
    for group in groups:
        for symbol, weight in group.items():
            weights[symbol] = weights.get(symbol, 0.0) + weight
    return weights


def run_v4(close, indicators, config):
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
    equity = []
    allocations = []
    weights = {}
    value = 1.0

    for dt in close.index:
        day_return = 0.0
        for symbol, weight in weights.items():
            if symbol in returns.columns and pd.notna(returns.at[dt, symbol]):
                day_return += weight * returns.at[dt, symbol]
        value *= 1.0 + day_return
        equity.append(value)

        if dt in rebalance_dates:
            bull = is_bull(config, close, indicators, dt)
            bear = is_bear(config, close, indicators, dt)
            if bear:
                value_target = config.bear_value_weight
                growth_target = config.bear_growth_weight
            elif bull:
                value_target = config.bull_value_weight
                growth_target = config.bull_growth_weight
            else:
                value_target = config.normal_value_weight
                growth_target = config.normal_growth_weight

            v = value_weights(config, close, indicators, dt, value_target)
            g = growth_weights(config, close, indicators, dt, growth_target, bull)
            weights = combine_weights(v, g)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "bull": bull,
                    "bear": bear,
                    "value": "|".join(sorted(v)),
                    "growth": "|".join(sorted(g)),
                    "cash": max(0.0, 1.0 - sum(weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def main():
    close = fetch_all_data()
    indicators = prepare_indicators(close)
    
    benchmarks = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    
    # Configure V4 using our optimized V3.1 framework
    config = V4Config(
        name="dual_sleeve_v4_best",
        bull_value_weight=0.30,
        bull_growth_weight=0.70,
        normal_value_weight=0.40,
        normal_growth_weight=0.60,
        bear_value_weight=0.70,
        bear_growth_weight=0.30,
        bull_rule="qqq200_m126",
        bear_rule="both_below_200_negative_m63",
        stock_top_n=3,
        value_mode="top2",
        score_mode="m63_m126",
        fallback="cash",
    )
    
    print("\nRunning V4 backtest (Hybrid ETF-Stock Strategy)...")
    curve, allocations = run_v4(close, indicators, config)
    
    curve.to_csv(RESULTS_DIR / "v4_best_equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "v4_best_monthly_allocations.csv", index=False)
    
    # Generate summary
    lines = [
        "# V4 Stock Alpha (V4.0) Backtest Summary",
        "",
        "V4 upgrades the Tactical Growth Sleeve from sector/theme ETFs to a dynamic selection of individual mega-cap leaders inside those hot sectors.",
        "",
        "## Configuration",
        "",
        f"- Name: `{config.name}`",
        f"- Fallback strategy: `{config.fallback}`",
        f"- Bull allocation: `{config.bull_value_weight:.0%}` value / `{config.bull_growth_weight:.0%}` growth",
        f"- Normal allocation: `{config.normal_value_weight:.0%}` value / `{config.normal_growth_weight:.0%}` growth",
        f"- Bear allocation: `{config.bear_value_weight:.0%}` value / `{config.bear_growth_weight:.0%}` growth",
        f"- Stock top N: `{config.stock_top_n}`",
        "",
        "## Full-Period Comparison",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    
    comparison = {"Dual Sleeve V4 Best": curve, **benchmarks}
    for label, c in comparison.items():
        row = summarize(label, c)
        lines.append(
            f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | "
            f"{pct(row['volatility'])} | {row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )
        
    # Slices/splits
    lines.extend(["", "## Split Periods Performance", "", "| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |", "| --- | --- | ---: | ---: | ---: | ---: |"])
    for split_name, start, end in SPLITS:
        for label, c in comparison.items():
            row = summarize(label, slice_curve(c, start, end))
            lines.append(f"| {split_name} | {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | {row['sharpe']:.2f} |")
            
    (RESULTS_DIR / "v4_stock_alpha_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    # Print results
    full = summarize("Dual Sleeve V4 Best", curve)
    bear2022 = summarize("Dual Sleeve V4 Best", slice_curve(curve, "2022-01-01", "2022-12-31"))
    train = summarize("Dual Sleeve V4 Best", slice_curve(curve, "2016-05-31", "2021-12-31"))
    
    print("\nBacktest Complete!")
    print(f"Full CAGR: {pct(full['cagr'])}, Full MDD: {pct(full['max_drawdown'])}, Sharpe: {full['sharpe']:.2f}")
    print(f"Train CAGR: {pct(train['cagr'])}, Bear 2022 CAGR: {pct(bear2022['cagr'])}, Bear 2022 MDD: {pct(bear2022['max_drawdown'])}")


if __name__ == "__main__":
    main()
