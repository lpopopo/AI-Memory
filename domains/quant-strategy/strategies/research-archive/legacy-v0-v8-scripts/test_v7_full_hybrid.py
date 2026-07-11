#!/usr/bin/env python3
import json
import sys
import time
from dataclasses import dataclass, asdict
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

# Market Fear threshold and logic for backtest (simplified for history)
@dataclass(frozen=True)
class FearResult:
    score: int
    regime: str
    risk_multiplier: float

def compute_fear_backtest(dt, close, indicators):
    points = 0
    
    # VIX Level
    vix = close.at[dt, "VIX"] if "VIX" in close.columns else np.nan
    if pd.notna(vix):
        if vix >= 35: points += 4
        elif vix >= 30: points += 3
        elif vix >= 22: points += 2
        elif vix >= 16: points += 1
    
    # SPY Drawdown (63d)
    spy_c = close["SPY"]
    dd63 = float(spy_c.at[dt] / spy_c.loc[:dt].iloc[-63:].max() - 1.0)
    if dd63 <= -0.12: points += 3
    elif dd63 <= -0.08: points += 2
    elif dd63 <= -0.04: points += 1
    
    # Trends
    spy_ma200 = indicators["ma200"].at[dt, "SPY"]
    if pd.notna(spy_ma200) and spy_c.at[dt] < spy_ma200: points += 3
    
    qqq_c = close["QQQ"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    if pd.notna(qqq_ma200) and qqq_c.at[dt] < qqq_ma200: points += 3

    # Regime Classification
    if points >= 9:
        return FearResult(score=points, regime="panic", risk_multiplier=0.20)
    elif points >= 5:
        return FearResult(score=points, regime="stress", risk_multiplier=0.50)
    elif points >= 3:
        return FearResult(score=points, regime="elevated", risk_multiplier=0.75)
    else:
        return FearResult(score=points, regime="normal", risk_multiplier=1.00)

def z_score(values):
    """Calculate cross-sectional Z-Scores."""
    if len(values) < 2: return [0.0 for _ in values]
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return [0.0 for _ in values]
    return [(v - mean) / std for v in values]

def growth_weights_v6_multifactor(config, close, indicators, dt, target_total):
    benchmarks_and_etfs = {"SPY", "QQQ", "VTV", "IWD", "SCHD", "VIX"}
    stock_pool = [col for col in close.columns if col not in benchmarks_and_etfs]
    
    factors = []
    for stock in stock_pool:
        if stock not in close.columns or pd.isna(close.at[dt, stock]): continue
        if close.at[dt, stock] < 5.0: continue
            
        ma50 = indicators["ma50"].at[dt, stock]
        ma200 = indicators["ma200"].at[dt, stock]
        m21 = indicators["mom21"].at[dt, stock]
        m63 = indicators["mom63"].at[dt, stock]
        m126 = indicators["mom126"].at[dt, stock]
        vol126 = indicators["vol126"].at[dt, stock]
        
        if any(pd.isna(v) for v in [ma50, ma200, m21, m63, m126, vol126]): continue
            
        if close.at[dt, stock] > ma50 and close.at[dt, stock] > ma200 and m63 > 0:
            quality_mom = m126 / vol126 if vol126 > 0 else 0
            factors.append({
                "stock": stock,
                "quality_mom": quality_mom,
                "raw_mom": m63,
                "short_term_rev": m21
            })
                
    if not factors: return {}
        
    z_q_mom = z_score([f["quality_mom"] for f in factors])
    z_r_mom = z_score([f["raw_mom"] for f in factors])
    z_s_rev = z_score([f["short_term_rev"] for f in factors])
    
    for i, f in enumerate(factors):
        f["final_score"] = (0.4 * z_q_mom[i]) + (0.4 * z_r_mom[i]) - (0.2 * z_s_rev[i])
        
    factors.sort(key=lambda x: x["final_score"], reverse=True)
    selected = [f["stock"] for f in factors[:config.stock_top_n]]
    weight = target_total / len(selected) if selected else 0
    return {symbol: weight for symbol in selected}

def double_radar_weights(close, indicators, dt, target_total):
    benchmarks_and_etfs = {"SPY", "QQQ", "VTV", "IWD", "SCHD", "VIX"}
    stock_pool = [col for col in close.columns if col not in benchmarks_and_etfs]
    
    # Radar Gate
    qqq_c = close.at[dt, "QQQ"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    qqq_m126 = indicators["mom126"].at[dt, "QQQ"]
    if qqq_c < qqq_ma200 or qqq_m126 <= 0:
        return {}
    
    eligible = []
    for stock in stock_pool:
        if stock not in close.columns or pd.isna(close.at[dt, stock]): continue
        if close.at[dt, stock] < 5.0: continue
        
        ma50 = indicators["ma50"].at[dt, stock]
        ma200 = indicators["ma200"].at[dt, stock]
        m63 = indicators["mom63"].at[dt, stock]
        m126 = indicators["mom126"].at[dt, stock]
        m252 = indicators["mom252"].at[dt, stock] if "mom252" in indicators else np.nan
        vol126 = indicators["vol126"].at[dt, stock]  # daily
        m21 = indicators["mom21"].at[dt, stock]
        
        if any(pd.isna(v) for v in [ma50, ma200, m63, m126, vol126, m21]): continue
        
        annualized_vol = vol126 * np.sqrt(252)
        ext50 = (close.at[dt, stock] / ma50) - 1.0
        
        if (close.at[dt, stock] > ma50 and close.at[dt, stock] > ma200 and 
            m63 > 0.15 and m126 > 0.25 and annualized_vol > 0.40 and ext50 < 0.35):
            eligible.append({
                "stock": stock,
                "m63": m63,
                "m126": m126,
                "m252": m252 if pd.notna(m252) else m126,
                "vol_ann": annualized_vol,
                "m21": m21,
                "ext50": ext50
            })
            
    if not eligible: return {}
    
    z_m126 = z_score([f["m126"] for f in eligible])
    z_m63 = z_score([f["m63"] for f in eligible])
    z_m252 = z_score([f["m252"] for f in eligible])
    z_vol = z_score([f["vol_ann"] for f in eligible])
    z_m21 = z_score([f["m21"] for f in eligible])
    z_ext = z_score([f["ext50"] for f in eligible])
    
    for i, f in enumerate(eligible):
        f["score"] = (0.3*z_m126[i] + 0.25*z_m63[i] + 0.2*z_m252[i] + 0.15*z_vol[i] - 0.1*z_m21[i] - 0.1*z_ext[i])
        
    eligible.sort(key=lambda x: x["score"], reverse=True)
    selected = [f["stock"] for f in eligible[:5]]
    weight = target_total / len(selected) if selected else 0
    return {symbol: weight for symbol in selected}

def run_v7_hybrid(close, indicators, config, transaction_cost=0.001, stop_loss_pct=0.30):
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
            value *= (1.0 - (turnover * transaction_cost))
            weights = pending_weights
            pending_weights = None
            
            # Reset high water marks
            high_water_marks = {}
            for symbol in weights.keys():
                if symbol in close.columns and pd.notna(close.at[dt, symbol]):
                    high_water_marks[symbol] = close.at[dt, symbol]
        else:
            # Trailing stop loss
            symbols_to_sell = []
            for symbol, weight in weights.items():
                if symbol in {"SPY", "QQQ", "VTV", "IWD", "SCHD", "VIX"}:
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
                    value *= (1.0 - (weights[symbol] * transaction_cost))
                    del weights[symbol]
                    del high_water_marks[symbol]

        equity.append(value)

        if dt in rebalance_dates:
            fear = compute_fear_backtest(dt, close, indicators)
            bull = is_bull(config, close, indicators, dt)
            bear = is_bear(config, close, indicators, dt)
            
            # Base targets
            if bear:
                core_val_t, core_grow_t = 0.70, 0.30
                radar_t = 0.0
            elif bull:
                core_val_t, core_grow_t = 0.20, 0.55
                radar_t = 0.25
            else:
                core_val_t, core_grow_t = 0.35, 0.50
                radar_t = 0.15
            
            # Core Selection
            v = value_weights(config, close, indicators, dt, core_val_t)
            if bear:
                # Filter value in bear
                v = {s: w for s, w in v.items() if close.at[dt, s] > indicators["ma200"].at[dt, s]}
            g = growth_weights_v6_multifactor(config, close, indicators, dt, core_grow_t)
            
            # Satellite Selection
            r = double_radar_weights(close, indicators, dt, radar_t)
            
            raw_weights = combine_weights(v, g, r)
            
            # Fear Gate Scaling
            scaled_weights = {s: w * fear.risk_multiplier for s, w in raw_weights.items()}
            pending_weights = scaled_weights
            
            allocations.append({
                "date": dt.strftime("%Y-%m-%d"),
                "regime": fear.regime,
                "risk_multiplier": fear.risk_multiplier,
                "core_val": "|".join(sorted(v)),
                "core_grow": "|".join(sorted(g)),
                "satellite": "|".join(sorted(r)),
                "cash": max(0.0, 1.0 - sum(pending_weights.values()))
            })

    return pd.Series(equity, index=close.index, name="v7_full_hybrid"), pd.DataFrame(allocations)

def main():
    start_time = time.time()
    print("Loading data...")
    close = load_universe_data()
    
    if "^VIX" in close.columns:
        close["VIX"] = close["^VIX"]
    
    print("Preparing indicators...")
    indicators = prepare_indicators(close)
    if "mom252" not in indicators:
        indicators["mom252"] = close / close.shift(252) - 1.0
    
    splits = [
        ("full_20yr", "2005-01-01", "2025-05-28"),
        ("dotcom_recovery", "2005-01-01", "2007-09-30"),
        ("financial_crisis", "2007-10-01", "2009-03-31"),
        ("post_crisis_bull", "2009-04-01", "2019-12-31"),
        ("covid_era", "2020-01-01", "2021-12-31"),
        ("inflation_bear", "2022-01-01", "2022-12-31"),
        ("ai_bull", "2023-01-01", "2025-05-28"),
    ]
    
    config = V4Config(
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
    
    print("\nRunning V7 Full Hybrid Backtest (Multi-Factor + Radar + Fear Gate + TSL)...")
    curve, allocations = run_v7_hybrid(close, indicators, config, stop_loss_pct=0.30)
    
    curve.to_csv(RESULTS_DIR / "v7_hybrid_equity_curve.csv", index_label="date")
    allocations.to_csv(RESULTS_DIR / "v7_hybrid_monthly_allocations.csv", index=False)
    
    benchmarks = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    
    lines = [
        "# V7 Full Hybrid Strategy Backtest Summary (20-Year)",
        "",
        "This version integrates the V6 Multi-Factor core, the Double-Radar Satellite module (annualized vol), the Market Fear Gate, and 30% Trailing Stop-Loss.",
        "",
        "## Configuration",
        "- Core: V6 Aggressive Multi-Factor (75% base)",
        "- Satellite: Double-Radar Top 5 (25% base)",
        "- Risk: Market Fear Gate scaling (20%/50%/75%/100%)",
        "- Stop-Loss: 30% Trailing Stop on individual stocks",
        "",
        "## Performance Comparison",
        "",
        "| Split | Strategy | Final Value | CAGR | Max DD | Sharpe |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    
    comparison = {"V7 Hybrid": curve, **benchmarks}
    for split_name, start, end in splits:
        for label, c in comparison.items():
            sc = slice_curve(c, start, end)
            if sc.empty: continue
            row = summarize(label, sc)
            lines.append(f"| {split_name} | {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | {row['sharpe']:.2f} |")
            
    summary_path = RESULTS_DIR / "v7_hybrid_summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    print(f"\nExecution Time: {time.time() - start_time:.2f}s")
    print(f"Results written to: {summary_path}")

if __name__ == "__main__":
    main()
