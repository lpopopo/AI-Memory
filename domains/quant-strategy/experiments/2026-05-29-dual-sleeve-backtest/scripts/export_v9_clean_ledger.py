#!/usr/bin/env python3
"""Phase 1: Export Clean Ledger & Deduplicated Funnel."""
import json
import sys
from pathlib import Path
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store
from validate_v9_information_strategy import load_data

WARMUP_START = "2026-01-01"
# We define the isolated periods to strictly segregate states
PERIODS = {
    "dev": ("2026-04-27", "2026-05-22"),
    "val": ("2026-05-28", "2026-06-12"),
    "test": ("2026-06-18", "2026-07-02")
}

def main():
    panels, vix, meta = load_data()
    # We use retrospective=True to get all historical events with their published_at dates 
    # to perform the Rejection Event Study properly across the whole historical period.
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json", use_retrospective=True)
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    
    cfg = V9Config(score_threshold=65) # Baseline config
    
    all_ledgers = []
    all_audits = []
    all_funnels = []
    
    for p_name, (start, end) in PERIODS.items():
        print(f"Running isolated backtest for {p_name} ({start} to {end})...")
        bt = V9Backtester(panels, vix, events, cfg, updates)
        res = bt.run(warmup_start=WARMUP_START, trading_start=start, trading_end=end)
        
        # Add period label to audit
        for a in res.audit:
            a["period"] = p_name
        all_audits.extend(res.audit)
        
        # Add period label to ledger
        for l in res.ledger:
            l["period"] = p_name
        all_ledgers.extend(res.ledger)
        
        # Add period label to funnel
        for f in res.funnel:
            f["period"] = p_name
        all_funnels.extend(res.funnel)
        
    # Deduplicate funnel: "连续多日拒绝只算一个独立机会"
    # Group by event_id + symbol, keeping the FIRST rejection reason and date
    unique_funnel = {}
    for f in all_funnels:
        if not f.get("event_id"): continue # Skip those without event_id
        
        key = f"{f['event_id']}_{f['symbol']}"
        if key not in unique_funnel:
            unique_funnel[key] = f
        else:
            # We already recorded the first rejection, ignore subsequent ones for this event+symbol
            pass
            
    dedup_funnel_list = list(unique_funnel.values())
    
    # Export
    (RESULTS_DIR / "v9_engine_audit.json").write_text(json.dumps(all_audits, indent=2))
    (RESULTS_DIR / "v9_unique_funnel.json").write_text(json.dumps(dedup_funnel_list, indent=2))
    
    ledger_df = pd.DataFrame(all_ledgers)
    if not ledger_df.empty:
        ledger_df.to_csv(RESULTS_DIR / "v9_trade_ledger_clean.csv", index=False)
    else:
        (RESULTS_DIR / "v9_trade_ledger_clean.csv").write_text("date,symbol,action,shares,price,cost,reason,is_info,period\n")

    print(f"Exported {len(all_ledgers)} trades, {len(all_audits)} audit days, and {len(dedup_funnel_list)} unique rejections.")

if __name__ == "__main__":
    main()
