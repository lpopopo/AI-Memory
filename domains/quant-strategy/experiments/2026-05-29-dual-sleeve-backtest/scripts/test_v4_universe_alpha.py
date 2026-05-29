#!/usr/bin/env python3
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import numpy as np

# Inject current scripts folder to path
sys.path.append(str(Path(__file__).resolve().parent))

from backtest_dual_sleeve import (
    RESULTS_DIR,
    pct,
    run_buy_hold,
    summarize,
)
from test_v4_stock_alpha import (
    VALUE_ETFS,
    V4Config,
    combine_weights,
    is_bear,
    is_bull,
    month_end_dates,
    prepare_indicators,
    value_weights,
)
from test_v4_long_term import SPLITS_LONG, slice_curve

ROOT = Path(__file__).resolve().parents[1]
DATA_UNIVERSE_DIR = ROOT / "data_universe"
DATA_LONG_DIR = ROOT / "data_long"


def load_universe_data():
    univ_path = DATA_UNIVERSE_DIR / "us_stock_universe_2000_2025.csv"
    long_path = DATA_LONG_DIR / "yfinance_adjusted_close_2000_2025.csv"
    
    if not univ_path.exists():
        raise FileNotFoundError(f"Missing master stock universe dataset: {univ_path}")
    if not long_path.exists():
        raise FileNotFoundError(f"Missing value ETF long-term dataset: {long_path}")
        
    print("Loading stock universe dataset...")
    df_univ = pd.read_csv(univ_path, index_col=0, parse_dates=True)
    
    print("Loading value ETFs dataset...")
    df_long = pd.read_csv(long_path, index_col=0, parse_dates=True)
    
    print("Aligning and merging datasets...")
    combined = df_univ.join(df_long[["VTV", "IWD", "SCHD"]], how="left")
    combined = combined.sort_index()
    combined = combined.dropna(subset=["SPY", "QQQ"])
    
    print(f"Loaded master dataset successfully: {combined.shape[0]} rows, {combined.shape[1]} columns.")
    return combined


def growth_weights_universe(config, close, indicators, dt, target_total, bull):
    benchmarks_and_etfs = {"SPY", "QQQ", "VTV", "IWD", "SCHD"}
    stock_pool = [col for col in close.columns if col not in benchmarks_and_etfs]
    
    eligible_stocks = []
    for stock in stock_pool:
        if stock not in close.columns or pd.isna(close.at[dt, stock]):
            continue
            
        stock_close = close.at[dt, stock]
        
        if stock_close < 5.0:
            continue
            
        stock_ma50 = indicators["ma50"].at[dt, stock]
        stock_ma200 = indicators["ma200"].at[dt, stock]
        stock_m63 = indicators["mom63"].at[dt, stock]
        stock_m126 = indicators["mom126"].at[dt, stock]
        stock_m252 = indicators["mom252"].at[dt, stock]
        
        if (
            pd.isna(stock_close)
            or pd.isna(stock_ma50)
            or pd.isna(stock_ma200)
            or pd.isna(stock_m63)
            or pd.isna(stock_m126)
            or pd.isna(stock_m252) 
        ):
            continue
            
        if stock_close > stock_ma50 and stock_close > stock_ma200:
            if stock_m63 > 0:
                score = stock_m63 + stock_m126
                eligible_stocks.append((score, stock))
                
    eligible_stocks.sort(reverse=True)
    selected_stocks = [s for _, s in eligible_stocks[:config.stock_top_n]]
    
    if not selected_stocks:
        return {}
        
    weight_per_stock = target_total / config.stock_top_n
    return {symbol: weight_per_stock for symbol in selected_stocks}


def calculate_turnover(old_weights, new_weights):
    all_symbols = set(old_weights.keys()).union(set(new_weights.keys()))
    turnover = 0.0
    for symbol in all_symbols:
        old_w = old_weights.get(symbol, 0.0)
        new_w = new_weights.get(symbol, 0.0)
        turnover += abs(new_w - old_w)
    return turnover


def run_v4_universe(close, indicators, config, transaction_cost=0.001, stop_loss_pct=0.15):
    """
    Runs the V4.3 Backtest with:
    - T+1 Execution & Transaction costs
    - Daily Trailing Stop-Loss for individual stocks
    - Absolute Trend Filter for Value ETFs during Bear markets
    """
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
    
    equity = []
    allocations = []
    
    weights = {}
    pending_weights = None 
    high_water_marks = {}
    
    value = 1.0

    for dt in close.index:
        day_return = 0.0
        for symbol, weight in weights.items():
            if symbol in returns.columns and pd.notna(returns.at[dt, symbol]):
                day_return += weight * returns.at[dt, symbol]
        
        value *= (1.0 + day_return)
        
        # 1. Execute pending trades from yesterday's rebalance
        if pending_weights is not None:
            turnover = calculate_turnover(weights, pending_weights)
            cost = turnover * transaction_cost
            value *= (1.0 - cost) 
            weights = pending_weights
            pending_weights = None
            
            # Reset high water marks for all active positions
            high_water_marks = {}
            for symbol in weights.keys():
                if symbol in close.columns and pd.notna(close.at[dt, symbol]):
                    high_water_marks[symbol] = close.at[dt, symbol]
        else:
            # 2. Daily Trailing Stop-Loss check for existing positions
            symbols_to_sell = []
            for symbol, weight in weights.items():
                if symbol in {"SPY", "QQQ", "VTV", "IWD", "SCHD"}:
                    continue # Do not stop-loss ETFs this way
                    
                current_price = close.at[dt, symbol] if symbol in close.columns else np.nan
                if pd.isna(current_price):
                    continue
                    
                if symbol not in high_water_marks:
                    high_water_marks[symbol] = current_price
                else:
                    high_water_marks[symbol] = max(high_water_marks[symbol], current_price)
                    
                # Check against -15% stop loss
                if current_price < high_water_marks[symbol] * (1.0 - stop_loss_pct):
                    symbols_to_sell.append(symbol)
                    
            if symbols_to_sell:
                for symbol in symbols_to_sell:
                    sell_cost = weights[symbol] * transaction_cost
                    value *= (1.0 - sell_cost)
                    del weights[symbol]
                    del high_water_marks[symbol]

        equity.append(value)

        # 3. Monthly Rebalancing Signals
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
            
            # Absolute Trend Filter for Value ETFs in Bear markets
            if bear:
                filtered_v = {}
                for symbol, w in v.items():
                    ma200 = indicators["ma200"].at[dt, symbol]
                    current_price = close.at[dt, symbol]
                    # Only hold if above its 200-day MA
                    if pd.notna(ma200) and current_price > ma200:
                        filtered_v[symbol] = w
                v = filtered_v
                
            g = growth_weights_universe(config, close, indicators, dt, growth_target, bull)
            
            pending_weights = combine_weights(v, g)
            
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "bull": bull,
                    "bear": bear,
                    "value": "|".join(sorted(v)),
                    "growth": "|".join(sorted(g)),
                    "cash": max(0.0, 1.0 - sum(pending_weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def main():
    start_time = time.time()
    close = load_universe_data()
    
    print("Calculating technical indicators...")
    indicators = prepare_indicators(close)
    
    benchmarks = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    
    # Configure V5 Optimal
    config = V4Config(
        name="dual_sleeve_v5_universe_optimal",
        bull_value_weight=0.30,
        bull_growth_weight=0.70,
        normal_value_weight=0.40,
        normal_growth_weight=0.60,
        bear_value_weight=0.70,
        bear_growth_weight=0.30,
        bull_rule="qqq200_m126",
        bear_rule="both_below_200_negative_m63",
        stock_top_n=10,
        value_mode="top2",
        score_mode="m63_m126",
        fallback="cash",
    )
    
    print("\nRunning V5 Optimal Backtest (30% Trailing Stop-Loss & Bear Trend Filter)...")
    curve, allocations = run_v4_universe(close, indicators, config, transaction_cost=0.001, stop_loss_pct=0.30)
    
    # Save outputs
    curve.to_csv(RESULTS_DIR / "v5_universe_equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "v5_universe_monthly_allocations.csv", index=False)
    
    # Write summary
    lines = [
        "# V5 Optimal Full-Universe Strategy Backtest Summary",
        "",
        "This version incorporates the optimal 30% trailing stop-loss discovered via multi-agent parameter scanning.",
        "",
        "## Risk Management Upgrades (V5)",
        "",
        "- **30% Trailing Stop-Loss**: Individual growth stocks are tracked daily against their high-water mark. If they drop 30%, they are sold immediately, converting their weight to cash.",
        "- **Value Sleeve Trend Filter**: During bear markets, Value ETFs (VTV/IWD) are only held if their price is above the 200-day moving average. Otherwise, that defensive sleeve also goes 100% to cash to avoid system crashes.",
        "",
        "## Configuration",
        "",
        f"- Strategy Name: `{config.name}`",
        f"- Target stocks: `Top 10 individual stocks from the S&P 500 & Nasdaq 100 constituents`",
        "",
        "## Full-Period (26-Year) Comparison (2000-2025)",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    
    comparison = {"Dual Sleeve V5 Optimal": curve, **benchmarks}
    for label, c in comparison.items():
        row = summarize(label, c)
        lines.append(
            f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | "
            f"{pct(row['volatility'])} | {row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )
        
    lines.extend([
        "",
        "## Historic Split Periods Performance",
        "",
        "| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |",
        "| --- | --- | ---: | ---: | ---: | ---: |"
    ])
    for split_name, start, end in SPLITS_LONG:
        for label, c in comparison.items():
            row = summarize(label, slice_curve(c, start, end))
            lines.append(f"| {split_name} | {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | {row['sharpe']:.2f} |")
            
    (RESULTS_DIR / "v5_universe_optimal_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    # Print results to stdout
    full = summarize("Dual Sleeve V5 Optimal", curve)
    bear2008 = summarize("Dual Sleeve V5 Optimal", slice_curve(curve, "2008-01-02", "2008-12-31"))
    bear2022 = summarize("Dual Sleeve V5 Optimal", slice_curve(curve, "2022-01-03", "2022-12-31"))
    dotcom = summarize("Dual Sleeve V5 Optimal", slice_curve(curve, "2000-01-03", "2002-12-31"))
    
    print("\n" + "=" * 50)
    print("V5 OPTIMAL BACKTEST COMPLETE!")
    print(f"Execution Time: {time.time() - start_time:.2f} seconds")
    print("-" * 50)
    print(f"26-Yr CAGR:           {pct(full['cagr'])}")
    print(f"26-Yr Max Drawdown:   {pct(full['max_drawdown'])}")
    print(f"26-Yr Sharpe Ratio:   {full['sharpe']:.2f}")
    print(f"26-Yr Sortino Ratio:  {full['sortino']:.2f}")
    print("-" * 50)
    print(f"Dot-com Crash (00-02) CAGR: {pct(dotcom['cagr'])}, Max DD: {pct(dotcom['max_drawdown'])}")
    print(f"2008 Crisis CAGR:           {pct(bear2008['cagr'])}, Max DD: {pct(bear2008['max_drawdown'])}")
    print(f"2022 Inflation CAGR:         {pct(bear2022['cagr'])}, Max DD: {pct(bear2022['max_drawdown'])}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
