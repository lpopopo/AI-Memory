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
from test_v4_universe_alpha import load_universe_data, calculate_turnover
from test_v4_long_term import SPLITS_LONG, slice_curve

def z_score(values):
    """Calculate cross-sectional Z-Scores."""
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return [0.0 for _ in values]
    return [(v - mean) / std for v in values]


def growth_weights_v6_multifactor(config, close, indicators, dt, target_total, bull):
    """
    V6 Aggressive Multi-Factor Stock Scanner
    Factors: Quality Momentum (40%), Raw Momentum (40%), Short-Term Reversal Penalty (20%)
    """
    benchmarks_and_etfs = {"SPY", "QQQ", "VTV", "IWD", "SCHD"}
    stock_pool = [col for col in close.columns if col not in benchmarks_and_etfs]
    
    eligible_stocks = []
    
    # Pre-calculate factors for eligible stocks
    factors = []
    for stock in stock_pool:
        if stock not in close.columns or pd.isna(close.at[dt, stock]):
            continue
            
        stock_close = close.at[dt, stock]
        if stock_close < 5.0:
            continue
            
        ma50 = indicators["ma50"].at[dt, stock]
        ma200 = indicators["ma200"].at[dt, stock]
        m21 = indicators["mom21"].at[dt, stock]
        m63 = indicators["mom63"].at[dt, stock]
        m126 = indicators["mom126"].at[dt, stock]
        m252 = indicators["mom252"].at[dt, stock]
        vol126 = indicators["vol126"].at[dt, stock]
        
        if (
            pd.isna(stock_close) or pd.isna(ma50) or pd.isna(ma200) or
            pd.isna(m21) or pd.isna(m63) or pd.isna(m126) or pd.isna(m252) or pd.isna(vol126)
        ):
            continue
            
        # Strict dual-trend filter
        if stock_close > ma50 and stock_close > ma200:
            # Positive momentum filter
            if m63 > 0:
                # Raw factors
                quality_mom = m126 / vol126 if vol126 > 0 else 0
                raw_mom = m63
                short_term_rev = m21
                
                factors.append({
                    "stock": stock,
                    "quality_mom": quality_mom,
                    "raw_mom": raw_mom,
                    "short_term_rev": short_term_rev
                })
                
    if not factors:
        return {}
        
    # Cross-sectional Standardization (Z-Score)
    q_mom_values = [f["quality_mom"] for f in factors]
    r_mom_values = [f["raw_mom"] for f in factors]
    s_rev_values = [f["short_term_rev"] for f in factors]
    
    z_q_mom = z_score(q_mom_values)
    z_r_mom = z_score(r_mom_values)
    z_s_rev = z_score(s_rev_values)
    
    # Calculate combined Aggressive Score
    for i, f in enumerate(factors):
        # A: Aggressive Weighting -> 40% Quality Mom, 40% Raw Mom, -20% Short-term Reversal
        score = (0.4 * z_q_mom[i]) + (0.4 * z_r_mom[i]) - (0.2 * z_s_rev[i])
        f["final_score"] = score
        
    # Sort and rank
    factors.sort(key=lambda x: x["final_score"], reverse=True)
    selected_stocks = [f["stock"] for f in factors[:config.stock_top_n]]
    
    weight_per_stock = target_total / config.stock_top_n
    return {symbol: weight_per_stock for symbol in selected_stocks}


def run_v6_multifactor(close, indicators, config, transaction_cost=0.001, stop_loss_pct=0.30):
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
        
        if pending_weights is not None:
            turnover = calculate_turnover(weights, pending_weights)
            cost = turnover * transaction_cost
            value *= (1.0 - cost) 
            weights = pending_weights
            pending_weights = None
            
            high_water_marks = {}
            for symbol in weights.keys():
                if symbol in close.columns and pd.notna(close.at[dt, symbol]):
                    high_water_marks[symbol] = close.at[dt, symbol]
        else:
            symbols_to_sell = []
            for symbol, weight in weights.items():
                if symbol in {"SPY", "QQQ", "VTV", "IWD", "SCHD"}:
                    continue 
                    
                current_price = close.at[dt, symbol] if symbol in close.columns else np.nan
                if pd.isna(current_price): continue
                    
                if symbol not in high_water_marks:
                    high_water_marks[symbol] = current_price
                else:
                    high_water_marks[symbol] = max(high_water_marks[symbol], current_price)
                    
                if current_price < high_water_marks[symbol] * (1.0 - stop_loss_pct):
                    symbols_to_sell.append(symbol)
                    
            if symbols_to_sell:
                for symbol in symbols_to_sell:
                    sell_cost = weights[symbol] * transaction_cost
                    value *= (1.0 - sell_cost)
                    del weights[symbol]
                    del high_water_marks[symbol]

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
            if bear:
                filtered_v = {}
                for symbol, w in v.items():
                    ma200 = indicators["ma200"].at[dt, symbol]
                    current_price = close.at[dt, symbol]
                    if pd.notna(ma200) and current_price > ma200:
                        filtered_v[symbol] = w
                v = filtered_v
                
            g = growth_weights_v6_multifactor(config, close, indicators, dt, growth_target, bull)
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
    
    config = V4Config(
        name="dual_sleeve_v6_multifactor_aggressive",
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
        score_mode="multifactor",
        fallback="cash",
    )
    
    print("\nRunning V6 Multi-Factor Aggressive Backtest...")
    curve, allocations = run_v6_multifactor(close, indicators, config, stop_loss_pct=0.30)
    
    curve.to_csv(RESULTS_DIR / "v6_multifactor_equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "v6_multifactor_monthly_allocations.csv", index=False)
    
    lines = [
        "# V6 Multi-Factor Strategy Backtest Summary",
        "",
        "This version upgrades the selection engine from Raw Momentum to an Aggressive Multi-Factor Model using cross-sectional Z-Score standardization.",
        "",
        "## Factor Weighting (Aggressive)",
        "",
        "- **+40% Quality Momentum**: `mom126 / vol126` (Rewards high returns with low volatility)",
        "- **+40% Raw Momentum**: `mom63` (Rewards recent strong uptrends)",
        "- **-20% Short-Term Reversal**: `mom21` (Penalizes stocks that spiked too fast in the last month to avoid mean reversion)",
        "",
        "## Configuration",
        "",
        f"- Strategy Name: `{config.name}`",
        f"- Risk Management: `30% Trailing Stop-Loss + Bear Market Value Trend Filter`",
        "",
        "## Full-Period (26-Year) Comparison (2000-2025)",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    
    comparison = {"Dual Sleeve V6 Multi-Factor": curve, **benchmarks}
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
            
    (RESULTS_DIR / "v6_multifactor_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    full = summarize("Dual Sleeve V6 Multi-Factor", curve)
    bear2008 = summarize("Dual Sleeve V6 Multi-Factor", slice_curve(curve, "2008-01-02", "2008-12-31"))
    bear2022 = summarize("Dual Sleeve V6 Multi-Factor", slice_curve(curve, "2022-01-03", "2022-12-31"))
    dotcom = summarize("Dual Sleeve V6 Multi-Factor", slice_curve(curve, "2000-01-03", "2002-12-31"))
    
    print("\n" + "=" * 50)
    print("V6 MULTI-FACTOR BACKTEST COMPLETE!")
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
