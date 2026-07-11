#!/usr/bin/env python3
"""Optimize V9 event-driven strategy hyperparameters to maximize returns."""
from __future__ import annotations
import itertools, json, sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from validate_v9_information_strategy import load_data, stats
from v9_information_strategy import V9Backtester, V9Config, chronological_split, load_event_store, load_evidence_store

def run_grid_search(panels, vix, events, updates):
    candidates = []
    
    # Grid definition
    thresholds = [60.0, 65.0, 70.0]
    tech_weights = [1.0, 1.5, 2.0]
    cap_scales = [1.0, 1.5, 2.0]
    
    total = len(thresholds) * len(tech_weights) * len(cap_scales)
    count = 0
    
    for thresh, tw, cs in itertools.product(thresholds, tech_weights, cap_scales):
        count += 1
        name = f"t{thresh}_tw{tw}_cs{cs}"
        cfg = V9Config(
            score_threshold=thresh, 
            tech_weight=tw, 
            score_cap_scale=cs, 
            source_healthy=True,  # Assume healthy source for pure parameter search
            transaction_cost=0.001
        )
        
        b = V9Backtester(panels, vix, events, cfg, updates)
        result = b.run()
        
        try:
            curve_stats = stats(result.equity)
            score = curve_stats["total_return"] + curve_stats["annualized_sharpe"] * 0.05
        except Exception:
            curve_stats = {"total_return": 0.0, "max_drawdown": 0.0, "annualized_sharpe": 0.0}
            score = -999.0
            
        candidates.append({
            "name": name,
            "threshold": thresh,
            "tech_weight": tw,
            "cap_scale": cs,
            "metrics": curve_stats,
            "score": score
        })
        print(f"[{count}/{total}] {name}: {curve_stats['total_return']:.2%} return")
        
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates

def main():
    panels, vix, meta = load_data()
    events, raw = load_event_store(ROOT / "datasets/v9_information_events.json")
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    split = chronological_split(events)
    path = RESULTS_DIR / "v9_optimization_metrics.json"
    if not split["eligible"]:
        output = {
            "status": "optimization_blocked",
            "reason": split["reason"],
            "split": split,
            "best": None,
            "grid_size": 0,
            "note": "Historical posts discovered retrospectively are excluded from point-in-time eligibility. No hyperparameter was selected."
        }
        path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Optimization blocked: {split['reason']}")
        print(path)
        return
    
    candidates = run_grid_search(panels, vix, events, updates)
    
    best = candidates[0]
    output = {
        "best": best,
        "top_5": candidates[:5],
        "grid_size": len(candidates)
    }
    
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Optimization complete. Best params: {best['name']} -> {best['metrics']['total_return']:.2%} return")
    print(path)

if __name__ == "__main__":
    main()
