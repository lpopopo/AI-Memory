#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from test_v4_universe_alpha import load_universe_data, prepare_indicators, run_v4_universe, V4Config
from backtest_dual_sleeve import summarize, pct

def main():
    print("Agent 1: Stop-Loss Parameter Scan")
    close = load_universe_data()
    indicators = prepare_indicators(close)
    
    config = V4Config(
        name="scan",
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
    
    stop_losses = [0.10, 0.15, 0.20, 0.25, 0.30]
    
    print("\n" + "="*50)
    print(f"{'Stop Loss':<10} | {'CAGR':<8} | {'Max DD':<8} | {'Sharpe':<6} | {'Sortino':<7}")
    print("-" * 50)
    
    for sl in stop_losses:
        curve, _ = run_v4_universe(close, indicators, config, transaction_cost=0.001, stop_loss_pct=sl)
        summary = summarize(f"SL {sl:.0%}", curve)
        print(f"{sl:<10.0%} | {pct(summary['cagr']):<8} | {pct(summary['max_drawdown']):<8} | {summary['sharpe']:<6.2f} | {summary['sortino']:<7.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
