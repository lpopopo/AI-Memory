#!/usr/bin/env python3
"""Phase 6: Small-Scale Sequential Optimization Harness."""
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store
from v9_evaluation import evaluate_scheme
from validate_v9_information_strategy import load_data, benchmark

WARMUP_START = "2026-01-01"
DEV_START = "2026-04-27"
DEV_END = "2026-05-22"
VAL_START = "2026-05-28"
VAL_END = "2026-06-12"

def generate_grid(rule_version):
    if rule_version == "A":
        return [{"entry_rule_version": "A"}]
        
    grid = []
    for obs in (0.02, 0.03):
        for atr in (2.0, 2.5):
            for wait in (5, 10):
                for upg in ("second_conf", "break_high"):
                    for ts in (3, 5):
                        grid.append({
                            "entry_rule_version": rule_version,
                            "obs_size": obs,
                            "dynamic_atr_max": atr,
                            "wait_days_max": wait,
                            "upgrade_trigger": upg,
                            "time_stop_days": ts
                        })
    return grid

def main():
    panels, vix, meta = load_data()
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json", use_retrospective=True)
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    
    close = panels["close"]
    v8_dev = benchmark(close, ensemble_target_function(close)).loc[DEV_START:DEV_END]
    v8_val = benchmark(close, ensemble_target_function(close)).loc[VAL_START:VAL_END]
    
    rules_to_test = ["D1_D2", "D1", "D", "B", "C", "A"]
    best_frozen_config = None
    
    for rule in rules_to_test:
        print(f"\n--- Testing Rule Version {rule} ---")
        grid = generate_grid(rule)
        
        # 1. Dev Stage
        dev_results = []
        for i, var in enumerate(grid):
            cfg = V9Config(**var)
            bt = V9Backtester(panels, vix, events, cfg, updates)
            res = bt.run(warmup_start=WARMUP_START, trading_start=DEV_START, trading_end=DEV_END)
            ev = evaluate_scheme(res.equity, v8_dev, res.audit, res.ledger, cfg.transaction_cost, res.diagnostics)
            if ev["unified_score"] != -999.0: # Passed hard filters
                dev_results.append((ev["unified_score"], var))
                
        if not dev_results:
            print(f"Rule {rule} failed all Dev filters.")
            continue
            
        dev_results.sort(key=lambda x: x[0], reverse=True)
        print(f"Rule {rule} passed Dev with {len(dev_results)} configs. Best Dev Score: {dev_results[0][0]:.2f}")
        
        # 2. Validation Stage (Cost = 0.005)
        val_results = []
        for _, var in dev_results:
            var_val = {**var, "transaction_cost": 0.005}
            cfg = V9Config(**var_val)
            bt = V9Backtester(panels, vix, events, cfg, updates)
            res = bt.run(warmup_start=WARMUP_START, trading_start=VAL_START, trading_end=VAL_END)
            ev = evaluate_scheme(res.equity, v8_val, res.audit, res.ledger, cfg.transaction_cost, res.diagnostics)
            
            # Acceptance Criteria: info_contrib > 0
            if ev["info_contrib"] > 0 and ev["unified_score"] != -999.0:
                val_results.append((ev["unified_score"], var_val, ev))
                
        if val_results:
            val_results.sort(key=lambda x: x[0], reverse=True)
            best_frozen_config = val_results[0][1]
            print(f"SUCCESS! Rule {rule} passed Validation. Freezing Config.")
            break
        else:
            print(f"Rule {rule} failed Validation (no positive info_contrib or hard filter fail).")
            
    if not best_frozen_config:
        print("\nFAILURE: All rules failed. Falling back to Rule A baseline.")
        best_frozen_config = {"entry_rule_version": "A", "transaction_cost": 0.005}
        
    (RESULTS_DIR / "v9_frozen_config.json").write_text(json.dumps(best_frozen_config, indent=2))
    print("\nOptimization Pipeline Complete. Config Frozen.")

if __name__ == "__main__":
    main()
