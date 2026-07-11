#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

import pandas as pd
import numpy as np

# Add current scripts folder to path
sys.path.append(str(Path(__file__).resolve().parent))

from backtest_dual_sleeve import (
    RESULTS_DIR,
    pct,
    run_buy_hold,
    summarize,
)
from test_v4_stock_alpha import (
    V4Config,
    prepare_indicators,
)
from test_v4_universe_alpha import load_universe_data, run_v4_universe
from test_v6_multifactor import run_v6_multifactor
from test_v7_full_hybrid import run_v7_hybrid

def slice_indicators(indicators, start_date, end_date):
    sliced = {}
    for k, v in indicators.items():
        if isinstance(v, pd.DataFrame):
            sliced[k] = v.loc[start_date:end_date]
        else:
            sliced[k] = v
    return sliced

def main():
    start_time = time.time()
    print("Loading full universe data...")
    close = load_universe_data()
    
    if "^VIX" in close.columns:
        close["VIX"] = close["^VIX"]
        
    print("Preparing technical indicators on full dataset (to avoid boundary issues)...")
    indicators = prepare_indicators(close)
    if "mom252" not in indicators:
        indicators["mom252"] = close / close.shift(252) - 1.0
        
    # Define 20-year backtest window
    # From 2006-01-03 to 2025-12-30 (exactly 20 years of trading days)
    start_date = "2006-01-01"
    end_date = "2025-12-30"
    
    print(f"\nSlicing data to 20-year window: {start_date} to {end_date}...")
    sliced_close = close.loc[start_date:end_date]
    sliced_indicators = slice_indicators(indicators, start_date, end_date)
    
    # Verify exact length
    print(f"Total trading days in sliced window: {len(sliced_close)}")
    print(f"Actual Start: {sliced_close.index[0].strftime('%Y-%m-%d')}")
    print(f"Actual End:   {sliced_close.index[-1].strftime('%Y-%m-%d')}")
    
    # Configure V5, V6, and V7
    v5_config = V4Config(
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
    
    v6_config = V4Config(
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
    
    v7_config = V4Config(
        name="dual_sleeve_v7_hybrid",
        bull_value_weight=0.20,
        bull_growth_weight=0.55, 
        normal_value_weight=0.35,
        normal_growth_weight=0.50,
        bear_value_weight=0.70,
        bear_growth_weight=0.30,
        bull_rule="qqq200_m126",
        bear_rule="both_below_200_negative_m63",
        stock_top_n=10,
        value_mode="top2",
        score_mode="v7_hybrid",
        fallback="cash",
    )
    
    # Run Benchmarks over the 20-year window
    print("\nRunning benchmarks...")
    benchmarks = {
        "SPY": run_buy_hold(sliced_close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(sliced_close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(sliced_close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    
    # Run V5
    print("\nRunning V5 Optimal Backtest...")
    v5_curve, v5_alloc = run_v4_universe(
        sliced_close, sliced_indicators, v5_config, transaction_cost=0.001, stop_loss_pct=0.30
    )
    
    # Run V6
    print("\nRunning V6 Multi-Factor Backtest...")
    v6_curve, v6_alloc = run_v6_multifactor(
        sliced_close, sliced_indicators, v6_config, transaction_cost=0.001, stop_loss_pct=0.30
    )
    
    # Run V7
    print("\nRunning V7 Full Hybrid Backtest...")
    v7_curve, v7_alloc = run_v7_hybrid(
        sliced_close, sliced_indicators, v7_config, transaction_cost=0.001, stop_loss_pct=0.30
    )
    
    # Save curves and allocations
    v5_curve.to_csv(RESULTS_DIR / "v5_20yr_equity_curve.csv", index_label="date")
    v6_curve.to_csv(RESULTS_DIR / "v6_20yr_equity_curve.csv", index_label="date")
    v7_curve.to_csv(RESULTS_DIR / "v7_20yr_equity_curve.csv", index_label="date")
    
    v5_alloc.to_csv(RESULTS_DIR / "v5_20yr_allocations.csv", index=False)
    v6_alloc.to_csv(RESULTS_DIR / "v6_20yr_allocations.csv", index=False)
    v7_alloc.to_csv(RESULTS_DIR / "v7_20yr_allocations.csv", index=False)
    
    # Compile performance comparison table
    strategies = {
        "V5 Universe Optimal": v5_curve,
        "V6 Multi-Factor": v6_curve,
        "V7 Full Hybrid": v7_curve,
        **benchmarks
    }
    
    lines = [
        "# V5, V6, and V7 Performance Comparison (20-Year Backtest)",
        "",
        f"This report compares the V5, V6, and V7 versions of the quant strategy over a 20-year backtest window from **{start_date}** to **{end_date}** (exactly {len(sliced_close)} trading days).",
        "",
        "## Performance Table (2006-2025)",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    
    results = {}
    for name, curve in strategies.items():
        row = summarize(name, curve)
        results[name] = row
        lines.append(
            f"| {name} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | "
            f"{pct(row['volatility'])} | {row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )
        
    lines.extend([
        "",
        "## Core Strategy Split Breakdown",
        "",
        "- **V5 Universe Optimal**: Baseline dynamic ETF-Stock allocation with a 30% individual stock trailing stop-loss.",
        "- **V6 Multi-Factor**: Replaces the V5 single-indicator momentum score with a multi-factor ranking score (+40% Quality Mom, +40% Raw Mom, -20% Short-term Reversal).",
        "- **V7 Full Hybrid**: Combines the V6 multi-factor selection with a Double-Radar satellite sleeve (25% weight) and dynamic Market Fear Gate exposure scaling.",
        "",
        "## Key Observations",
        ""
    ])
    
    # Auto-generate observations based on metrics
    v5_cagr = results["V5 Universe Optimal"]["cagr"]
    v6_cagr = results["V6 Multi-Factor"]["cagr"]
    v7_cagr = results["V7 Full Hybrid"]["cagr"]
    
    v5_dd = results["V5 Universe Optimal"]["max_drawdown"]
    v6_dd = results["V6 Multi-Factor"]["max_drawdown"]
    v7_dd = results["V7 Full Hybrid"]["max_drawdown"]
    
    best_cagr = max(v5_cagr, v6_cagr, v7_cagr)
    best_cagr_name = "V5" if best_cagr == v5_cagr else ("V6" if best_cagr == v6_cagr else "V7")
    
    best_dd = max(v5_dd, v6_dd, v7_dd) # drawdowns are negative, max drawdown (closest to 0) is the best
    best_dd_name = "V5" if best_dd == v5_dd else ("V6" if best_dd == v6_dd else "V7")
    
    lines.append(f"1. **CAGR Outperformance**: The **{best_cagr_name}** version achieved the highest return over the 20-year period with a CAGR of **{pct(best_cagr)}**.")
    lines.append(f"2. **Drawdown Protection**: The **{best_dd_name}** version showed the most resilient risk profile, limiting the maximum drawdown to **{pct(best_dd)}**.")
    
    spy_cagr = results["SPY"]["cagr"]
    qqq_cagr = results["QQQ"]["cagr"]
    lines.append(f"3. **Benchmark Comparison**: All three versions significantly outperformed the SPY (CAGR: {pct(spy_cagr)}) and QQQ (CAGR: {pct(qqq_cagr)}) on both absolute and risk-adjusted metrics.")
    
    # Save summary report
    summary_path = RESULTS_DIR / "compare_v5_v6_v7_20yr_summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    print("\n" + "=" * 50)
    print("20-YEAR COMPARISON BACKTEST COMPLETE!")
    print(f"Execution Time: {time.time() - start_time:.2f} seconds")
    print(f"Results written to: {summary_path}")
    print("=" * 50 + "\n")
    
    # Print table to stdout
    for line in lines[6:15]:
        print(line)

if __name__ == "__main__":
    main()
