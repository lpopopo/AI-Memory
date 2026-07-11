#!/usr/bin/env python3
"""Phase 2: Rejection Event Study."""
import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from validate_v9_information_strategy import load_data

def main():
    funnel_path = RESULTS_DIR / "v9_unique_funnel.json"
    if not funnel_path.exists():
        print("Run export_v9_clean_ledger.py first.")
        sys.exit(1)
        
    funnel = json.loads(funnel_path.read_text())
    panels, vix, meta = load_data()
    
    close_px = panels["close"]
    open_px = panels["open"]
    high_px = panels["high"]
    low_px = panels["low"]
    
    ma20 = close_px.rolling(20).mean()
    prev = close_px.shift(1)
    tr = pd.DataFrame(np.maximum.reduce([
        (high_px - low_px).to_numpy(),
        (high_px - prev).abs().to_numpy(),
        (low_px - prev).abs().to_numpy()
    ]), index=close_px.index, columns=close_px.columns)
    atr20 = tr.rolling(20).mean()
    
    study_records = []
    
    for f in funnel:
        dt_str = f["date"]
        s = f["symbol"]
        reason = f["reason"]
        
        if s not in close_px.columns or dt_str not in close_px.index:
            continue
            
        dt_loc = close_px.index.get_loc(dt_str)
        if dt_loc >= len(close_px.index) - 1:
            continue # No future data
            
        # Entry is next day open
        t1_idx = close_px.index[dt_loc + 1]
        entry_price = open_px.at[t1_idx, s]
        if pd.isna(entry_price): continue
        
        qqq_entry = open_px.at[t1_idx, "QQQ"]
        
        # Event day stats
        c0 = close_px.at[dt_str, s]
        m20 = ma20.at[dt_str, s]
        a20 = atr20.at[dt_str, s]
        
        ma20_dev = (c0 / m20 - 1) if m20 else 0
        atr_dev = (c0 - m20) / a20 if a20 else 0
        gap = (entry_price / c0 - 1) if c0 else 0
        
        # Forward returns
        fwd_ret = {}
        qqq_ret = {}
        for d in [1, 3, 5, 10]:
            if dt_loc + 1 + d < len(close_px.index):
                fd_idx = close_px.index[dt_loc + 1 + d]
                c_d = close_px.at[fd_idx, s]
                q_d = close_px.at[fd_idx, "QQQ"]
                fwd_ret[f"ret_{d}d"] = (c_d / entry_price - 1) if pd.notna(c_d) else np.nan
                qqq_ret[f"qqq_ret_{d}d"] = (q_d / qqq_entry - 1) if pd.notna(q_d) else np.nan
            else:
                fwd_ret[f"ret_{d}d"] = np.nan
                qqq_ret[f"qqq_ret_{d}d"] = np.nan
                
        # MFE / MAE over 10 days (relative to entry price)
        mfe = 0.0
        mae = 0.0
        touched_ma20 = False
        entered_2atr = False
        
        for i in range(1, min(11, len(close_px.index) - dt_loc - 1)):
            idx = close_px.index[dt_loc + i]
            h = high_px.at[idx, s]
            l = low_px.at[idx, s]
            c = close_px.at[idx, s]
            cm20 = ma20.at[idx, s]
            ca20 = atr20.at[idx, s]
            
            if pd.notna(h) and h > entry_price:
                mfe = max(mfe, h / entry_price - 1)
            if pd.notna(l) and l < entry_price:
                mae = min(mae, l / entry_price - 1)
                
            if pd.notna(l) and pd.notna(cm20) and l <= cm20 * 1.01:
                touched_ma20 = True
                
            if pd.notna(c) and pd.notna(cm20) and pd.notna(ca20):
                if (c - cm20) <= 2 * ca20:
                    entered_2atr = True
                    
        # Group determination
        group = "Other"
        if reason == "chase_filter":
            if ma20_dev > 0.08 and atr_dev > 2: group = "Both 8% and 2ATR"
            elif ma20_dev > 0.08: group = "Only 8%"
            elif atr_dev > 2: group = "Only 2ATR"
            else: group = "Chase (Intraday/Unknown)"
        elif reason == "technical_not_confirmed":
            group = "Tech Not Confirmed"
        elif reason in ["max_names_cap", "theme_cap", "sleeve_cap", "cash_shortage", "market_gate_blocked"]:
            group = "Risk Blocked"
        elif reason == "score_below_threshold":
            group = "Score Below Threshold"
            
        record = {
            "event_id": f.get("event_id"),
            "date": dt_str,
            "symbol": s,
            "reason": reason,
            "group": group,
            "ma20_dev": ma20_dev,
            "atr_dev": atr_dev,
            "gap": gap,
            "mfe_10d": mfe,
            "mae_10d": mae,
            "touched_ma20_10d": touched_ma20,
            "entered_2atr_10d": entered_2atr,
            **fwd_ret,
            **qqq_ret
        }
        study_records.append(record)
        
    df = pd.DataFrame(study_records)
    if df.empty:
        print("No valid rejection records to study.")
        sys.exit(0)
        
    # Compute alphas
    for d in [1, 3, 5, 10]:
        df[f"alpha_{d}d"] = df[f"ret_{d}d"] - df[f"qqq_ret_{d}d"]
        
    # Export raw
    df.to_csv(RESULTS_DIR / "v9_rejection_event_study.csv", index=False)
    
    # Summary
    summary = []
    groups = df["group"].unique()
    for g in groups:
        gdf = df[df["group"] == g]
        if gdf.empty: continue
        
        count = len(gdf)
        win_rate_5d = (gdf["alpha_5d"] > 0).mean()
        avg_alpha_5d = gdf["alpha_5d"].mean()
        med_mae = gdf["mae_10d"].median()
        touch_rate = gdf["touched_ma20_10d"].mean()
        atr_rate = gdf["entered_2atr_10d"].mean()
        
        summary.append({
            "group": g,
            "count": count,
            "alpha_5d_win_rate": float(win_rate_5d),
            "avg_alpha_5d": float(avg_alpha_5d),
            "median_mae_10d": float(med_mae),
            "touched_ma20_rate": float(touch_rate),
            "entered_2atr_rate": float(atr_rate)
        })
        
    (RESULTS_DIR / "v9_rejection_summary.json").write_text(json.dumps(summary, indent=2))
    
    # Generate Markdown Report
    report = ["# V9 Rejection Event Study", ""]
    report.append("## 1. Group Breakdown and Forward Returns")
    report.append("| Group | Count | 5D Win Rate (vs QQQ) | Avg 5D Alpha | Median 10D MAE | 10D MA20 Touch Rate | 10D 2ATR Enter Rate |")
    report.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for row in summary:
        report.append(f"| {row['group']} | {row['count']} | {row['alpha_5d_win_rate']:.2%} | {row['avg_alpha_5d']:.2%} | {row['median_mae_10d']:.2%} | {row['touched_ma20_rate']:.2%} | {row['entered_2atr_rate']:.2%} |")
        
    report.append("")
    report.append("## 2. Judgement Analysis")
    report.append("Criteria for a successful signal group: 5D Win Rate >= 60%, Avg 5D Alpha > 2%, Median MAE > -5%.")
    for row in summary:
        success = row['alpha_5d_win_rate'] >= 0.60 and row['avg_alpha_5d'] > 0.02 and row['median_mae_10d'] >= -0.05
        report.append(f"- **{row['group']}**: {'✅ PASS' if success else '❌ FAIL'}")
        
    (RESULTS_DIR / "v9_rejection_report.md").write_text("\n".join(report), encoding="utf-8")
    print("Rejection study completed.")

if __name__ == "__main__":
    main()
