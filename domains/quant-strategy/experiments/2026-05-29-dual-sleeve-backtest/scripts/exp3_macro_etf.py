#!/usr/bin/env python3
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))

from test_v4_universe_alpha import (
    load_universe_data, prepare_indicators, calculate_turnover, month_end_dates
)
from backtest_dual_sleeve import summarize, pct

def run_macro_etf(close, indicators, transaction_cost=0.001):
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
    
    # Universe of Macro/Sector ETFs
    etf_pool = ['SPY', 'QQQ', 'XLU', 'XLP', 'XLV', 'XLE', 'XLK']
    
    equity = []
    weights = {}
    pending_weights = None 
    
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
            
        equity.append(value)

        if dt in rebalance_dates:
            eligible = []
            for symbol in etf_pool:
                if symbol not in close.columns: continue
                current_price = close.at[dt, symbol]
                ma200 = indicators["ma200"].at[dt, symbol]
                m63 = indicators["mom63"].at[dt, symbol]
                m126 = indicators["mom126"].at[dt, symbol]
                
                if pd.isna(current_price) or pd.isna(ma200) or pd.isna(m63) or pd.isna(m126):
                    continue
                    
                # Dual momentum + Trend filter
                if current_price > ma200 and m63 > 0:
                    score = m63 + m126
                    eligible.append((score, symbol))
                    
            eligible.sort(reverse=True)
            selected = [s for _, s in eligible[:3]]
            
            pending_weights = {}
            if selected:
                w = 1.0 / 3.0
                for s in selected:
                    pending_weights[s] = w

    return pd.Series(equity, index=close.index, name="Macro_ETF")

def main():
    print("Agent 3: Macro ETF Rotation")
    close = load_universe_data()
    indicators = prepare_indicators(close)
    
    curve = run_macro_etf(close, indicators)
    summary = summarize("Macro ETF (Top 3)", curve)
    
    print("\n" + "="*50)
    print(f"{'Strategy':<25} | {'CAGR':<8} | {'Max DD':<8} | {'Sharpe':<6} | {'Sortino':<7}")
    print("-" * 50)
    print(f"{summary['name']:<25} | {pct(summary['cagr']):<8} | {pct(summary['max_drawdown']):<8} | {summary['sharpe']:<6.2f} | {summary['sortino']:<7.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
