#!/usr/bin/env python3
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))

from test_v4_universe_alpha import (
    load_universe_data, prepare_indicators, V4Config, calculate_turnover, 
    month_end_dates, is_bull, is_bear, value_weights, growth_weights_universe, combine_weights
)
from backtest_dual_sleeve import summarize, pct

def run_v4_reentry(close, indicators, config, transaction_cost=0.001, stop_loss_pct=0.15):
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
    
    equity = []
    weights = {}
    pending_weights = None 
    high_water_marks = {}
    stopped_out_this_month = {} # symbol -> weight
    
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
                    
            # Clear stopped out tracking at rebalance
            stopped_out_this_month = {}
        else:
            # 1. Stop Loss Check
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
                    stopped_out_this_month[symbol] = weights[symbol]
                    del weights[symbol]
                    del high_water_marks[symbol]

            # 2. Re-entry Check
            symbols_to_rebuy = []
            for symbol, original_weight in stopped_out_this_month.items():
                current_price = close.at[dt, symbol] if symbol in close.columns else np.nan
                ma50 = indicators["ma50"].at[dt, symbol]
                
                if pd.notna(current_price) and pd.notna(ma50) and current_price > ma50:
                    symbols_to_rebuy.append(symbol)
                    
            if symbols_to_rebuy:
                for symbol in symbols_to_rebuy:
                    buy_cost = stopped_out_this_month[symbol] * transaction_cost
                    value *= (1.0 - buy_cost)
                    weights[symbol] = stopped_out_this_month[symbol]
                    high_water_marks[symbol] = close.at[dt, symbol]
                    del stopped_out_this_month[symbol]

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
                
            g = growth_weights_universe(config, close, indicators, dt, growth_target, bull)
            pending_weights = combine_weights(v, g)

    return pd.Series(equity, index=close.index, name="Reentry")

def main():
    print("Agent 2: Dynamic Re-entry Mechanism")
    close = load_universe_data()
    indicators = prepare_indicators(close)
    
    config = V4Config(
        name="reentry",
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
    
    curve = run_v4_reentry(close, indicators, config, stop_loss_pct=0.15)
    summary = summarize("15% SL + MA50 Re-entry", curve)
    
    print("\n" + "="*50)
    print(f"{'Strategy':<25} | {'CAGR':<8} | {'Max DD':<8} | {'Sharpe':<6} | {'Sortino':<7}")
    print("-" * 50)
    print(f"{summary['name']:<25} | {pct(summary['cagr']):<8} | {pct(summary['max_drawdown']):<8} | {summary['sharpe']:<6.2f} | {summary['sortino']:<7.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
