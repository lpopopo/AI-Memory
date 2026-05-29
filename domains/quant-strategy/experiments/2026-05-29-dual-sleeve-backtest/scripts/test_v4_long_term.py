#!/usr/bin/env python3
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from backtest_dual_sleeve import (
    RESULTS_DIR,
    pct,
    run_buy_hold,
    summarize,
)
from test_v4_stock_alpha import (
    SECTOR_LEADERS,
    TACTICAL_POOL,
    VALUE_ETFS,
    V4Config,
    combine_weights,
    is_bear,
    is_bull,
    month_end_dates,
    prepare_indicators,
    value_weights,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_LONG_DIR = ROOT / "data_long"

SPLITS_LONG = [
    ("full_26yr", "2000-01-03", "2025-12-31"),
    ("dotcom_crash_2000_2002", "2000-01-03", "2002-12-31"),
    ("bull_market_2003_2007", "2003-01-02", "2007-12-31"),
    ("financial_crisis_2008", "2008-01-02", "2008-12-31"),
    ("bull_market_2009_2019", "2009-01-02", "2019-12-31"),
    ("covid_crash_2020", "2020-01-02", "2020-12-31"),
    ("bull_market_2021", "2021-01-04", "2021-12-31"),
    ("inflation_bear_2022", "2022-01-03", "2022-12-31"),
    ("bull_market_2023_2025", "2023-01-03", "2025-12-31"),
]


def load_long_term_data():
    cache_path = DATA_LONG_DIR / "yfinance_adjusted_close_2000_2025.csv"
    if not cache_path.exists():
        raise FileNotFoundError(f"Missing long-term consolidated dataset: {cache_path}")
    close = pd.read_csv(cache_path, index_col=0, parse_dates=True)
    return close.dropna(subset=["SPY", "QQQ"])


def slice_curve(curve, start, end):
    sliced = curve.loc[(curve.index >= pd.Timestamp(start)) & (curve.index <= pd.Timestamp(end))]
    if sliced.empty:
        return pd.Series(1.0, index=pd.date_range(start, end, freq="B"))
    return sliced / sliced.iloc[0]


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
            # If stock did not exist yet (before IPO), skip it safely
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
    
    # 4. Fallback if fewer stocks qualify
    if not selected_stocks:
        if config.fallback == "cash":
            return {}
        else:
            return {"QQQ": target_total}
            
    # Equal-weight the selected stocks
    return {symbol: target_total / len(selected_stocks) for symbol in selected_stocks}


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
    close = load_long_term_data()
    indicators = prepare_indicators(close)
    
    benchmarks = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    
    config = V4Config(
        name="dual_sleeve_v4_long_term",
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
    
    print("\nRunning 26-Year V4 Long-Term Backtest (2000-2025)...")
    curve, allocations = run_v4(close, indicators, config)
    
    curve.to_csv(RESULTS_DIR / "v4_long_term_best_equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "v4_long_term_best_monthly_allocations.csv", index=False)
    
    lines = [
        "# V4 Long-Term (26-Year) Backtest Summary",
        "",
        "This backtest runs the hybrid V4 stock-ETF dual sleeve strategy over a 26-year period (2000-2025), handling multiple macro regimes and financial crises.",
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
        "## Full-Period (26-Year) Comparison",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    
    comparison = {"Dual Sleeve V4 Long Term": curve, **benchmarks}
    for label, c in comparison.items():
        row = summarize(label, c)
        lines.append(
            f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | "
            f"{pct(row['volatility'])} | {row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )
        
    lines.extend(["", "## Historic Split Periods Performance", "", "| Period | Strategy | Final Value | CAGR | Max DD | Sharpe |", "| --- | --- | ---: | ---: | ---: | ---: |"])
    for split_name, start, end in SPLITS_LONG:
        for label, c in comparison.items():
            row = summarize(label, slice_curve(c, start, end))
            lines.append(f"| {split_name} | {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | {row['sharpe']:.2f} |")
            
    (RESULTS_DIR / "v4_long_term_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    full = summarize("Dual Sleeve V4 Long Term", curve)
    bear2008 = summarize("Dual Sleeve V4 Long Term", slice_curve(curve, "2008-01-02", "2008-12-31"))
    bear2022 = summarize("Dual Sleeve V4 Long Term", slice_curve(curve, "2022-01-03", "2022-12-31"))
    dotcom = summarize("Dual Sleeve V4 Long Term", slice_curve(curve, "2000-01-03", "2002-12-31"))
    
    print("\nBacktest Complete!")
    print(f"26-Yr CAGR: {pct(full['cagr'])}, Max Drawdown: {pct(full['max_drawdown'])}, Sharpe: {full['sharpe']:.2f}")
    print(f"Dot-com (00-02) CAGR: {pct(dotcom['cagr'])}, Max DD: {pct(dotcom['max_drawdown'])}")
    print(f"2008 GFC CAGR: {pct(bear2008['cagr'])}, Max DD: {pct(bear2008['max_drawdown'])}")
    print(f"2022 Inflation CAGR: {pct(bear2022['cagr'])}, Max DD: {pct(bear2022['max_drawdown'])}")


if __name__ == "__main__":
    main()
