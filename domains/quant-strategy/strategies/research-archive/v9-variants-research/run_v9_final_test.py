#!/usr/bin/env python3
"""V9 Phase 3: Retrospective Control Test Execution & Reporting."""
from __future__ import annotations
import json
import sys
from pathlib import Path
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from backtest_dual_sleeve import RESULTS_DIR
from optimize_v8_core import ensemble_target_function
from v9_information_strategy import V9Backtester, V9Config, load_event_store, load_evidence_store
from v9_evaluation import calculate_stats
from validate_v9_information_strategy import load_data, benchmark

WARMUP_START = "2026-01-01"
TEST_START = "2026-06-18"
TEST_END = "2026-07-02"

def main():
    panels, vix, meta = load_data()
    updates, _ = load_evidence_store(ROOT / "datasets/v9_evidence_updates.json")
    
    close = panels["close"]
    v8_test = benchmark(close, ensemble_target_function(close)).loc[TEST_START:TEST_END]
    
    frozen_path = RESULTS_DIR / "v9_frozen_config.json"
    if not frozen_path.exists():
        print("CRITICAL ERROR: v9_frozen_config.json not found. Must run optimization first.")
        sys.exit(1)
        
    frozen_cfg = json.loads(frozen_path.read_text())
    
    versions = {
        "Baseline-A": {"v8_core_weight": 0.7, "info_sleeve_weight": 0.3, "entry_rule_version": "A"},
        "Baseline-D1": {"v8_core_weight": 0.7, "info_sleeve_weight": 0.3, "entry_rule_version": "D1"},
        "Baseline-D1+D2": {"v8_core_weight": 0.7, "info_sleeve_weight": 0.3, "entry_rule_version": "D1_D2"},
        "Rule E": {"v8_core_weight": 0.7, "info_sleeve_weight": 0.3, "entry_rule_version": "E"},
    }
    
    final_report = ["# V9 Retrospective Control Test Report", ""]
    final_report.append(f"**Test Period:** {TEST_START} to {TEST_END} (Retrospective Control)")
    final_report.append(f"**Transaction Cost:** 0.5% strictly applied to all trades")
    final_report.append("")
    
    attribution_data = {}
    
    for mode, is_retro in [("Retrospective (Published At)", True), ("Point-In-Time (First Seen At)", False)]:
        events, raw = load_event_store(ROOT / "datasets/v9_information_events.json", use_retrospective=is_retro)
        final_report.append(f"# {mode}")
        
        for name, alloc in versions.items():
            cfg_kwargs = {**frozen_cfg, **alloc, "transaction_cost": 0.005}
            cfg = V9Config(**cfg_kwargs)
            bt = V9Backtester(panels, vix, events, cfg, updates)
            res = bt.run(warmup_start=WARMUP_START, trading_start=TEST_START, trading_end=TEST_END)
            
            stats = calculate_stats(res.equity)
            v8_stats = calculate_stats(v8_test)
            
            v8_daily_contrib = 0.0
            info_official_daily_contrib = 0.0
            info_obs_daily_contrib = 0.0
            cost_daily_contrib = 0.0
            
            obs_buys = 0
            
            # Step 1: Accumulate exact PnL contributions from the audit log
            daily_costs = {}
            obs_buys = 0
            for t in res.ledger:
                d = pd.Timestamp(t["date"])
                daily_costs[d] = daily_costs.get(d, 0.0) + t["cost"]
                if t["is_info"] and t.get("is_observation", False) and t["action"] == "BUY":
                    obs_buys += 1
            
            # The backtester calculates exact PnL tracking
            v8_daily_contrib = sum(a.get("v8_pnl", 0.0) for a in res.audit)
            info_official_daily_contrib = sum(a.get("info_official_pnl", 0.0) for a in res.audit)
            info_obs_daily_contrib = sum(a.get("info_obs_pnl", 0.0) for a in res.audit)
            cost_daily_contrib = sum(a.get("cost_pnl", 0.0) for a in res.audit)
            total_info_contrib = info_official_daily_contrib + info_obs_daily_contrib
            
            actual_total_return = res.equity.iloc[-1] - 1.0
            reconstructed_total_return = v8_daily_contrib + total_info_contrib - cost_daily_contrib
            error = abs(actual_total_return - reconstructed_total_return)
            
            # Enforce 1bp exact closure
            assert error < 1e-4, f"PnL Closure Error > 1bp: {error}. Actual: {actual_total_return}, Recon: {reconstructed_total_return}"
            
            entries = len([x for x in res.ledger if x["action"] == "BUY" and x["is_info"]])
            
            passed = bool(
                entries >= 2 and 
                total_info_contrib > 0
            )
            
            attribution_data[f"{mode}_{name}"] = {
                "metrics": stats,
                "rel_v8": stats["total_return"] - v8_stats["total_return"],
                "entries": entries,
                "info_contrib": total_info_contrib,
                "passed": passed,
                "obs_buys": obs_buys,
                "total_return": stats["total_return"],
                "max_drawdown": stats["max_drawdown"]
            }
            
            if name == "Balanced" and not is_retro:
                # Deduplicate funnel by event_id + symbol
                seen_events = set()
                unique_funnel = []
                for f in res.funnel:
                    key = (f.get("event_id"), f.get("symbol"))
                    if key not in seen_events:
                        seen_events.add(key)
                        unique_funnel.append(f)
                
                (RESULTS_DIR / "v9_unique_funnel.json").write_text(json.dumps(unique_funnel, indent=2))
                (RESULTS_DIR / "v9_engine_audit.json").write_text(json.dumps(res.audit, indent=2))
                
                ledger_df = pd.DataFrame(res.ledger)
                if not ledger_df.empty:
                    ledger_df.to_csv(RESULTS_DIR / "v9_trade_ledger_clean.csv", index=False)
                else:
                    (RESULTS_DIR / "v9_trade_ledger_clean.csv").write_text("date,symbol,action,shares,price,cost,reason,is_info\n")
            
            final_report.append(f"## {name} Version")
            final_report.append(f"- **Total Return:** {stats['total_return']:.2%}")
            final_report.append(f"- **Excess vs V8:** {stats['total_return'] - v8_stats['total_return']:.2%}")
            final_report.append(f"- **Max Drawdown:** {stats['max_drawdown']:.2%}")
            final_report.append(f"- **Info Contribution:** {total_info_contrib:.2%}")
            final_report.append(f"- **Entries:** {entries}")
            final_report.append(f"- **Total Trading Costs:** {cost_daily_contrib:.2%}")
            final_report.append(f"- **Observation Buys:** {obs_buys}")
            final_report.append(f"- **Closure Error:** {error:.4%}")
            
            final_report.append(f"\n- **Passed Acceptance:** {'✅ YES' if passed else '❌ NO'}")
            if not passed:
                reasons = []
                if entries < 2: reasons.append("Insufficient entries (< 2)")
                if total_info_contrib <= 0: reasons.append("Negative info contribution")
                final_report.append(f"  - *Failure Reasons:* {', '.join(reasons)}")
            final_report.append("")
            
        # Summary Table for the mode
        final_report.append("### Attribution Breakdown")
        final_report.append("| Strategy Version | Obs Buys | Total Entries | Info Contribution | Total Return | Max Drawdown |")
        final_report.append("|---|---|---|---|---|---|")
        final_report.append(f"| Baseline-A | {attribution_data[f'{mode}_Baseline-A']['obs_buys']} | {attribution_data[f'{mode}_Baseline-A']['entries']} | {attribution_data[f'{mode}_Baseline-A']['info_contrib']:.4%} | {attribution_data[f'{mode}_Baseline-A']['total_return']:.4%} | {attribution_data[f'{mode}_Baseline-A']['max_drawdown']:.4%} |")
        final_report.append(f"| Baseline-D1 | {attribution_data[f'{mode}_Baseline-D1']['obs_buys']} | {attribution_data[f'{mode}_Baseline-D1']['entries']} | {attribution_data[f'{mode}_Baseline-D1']['info_contrib']:.4%} | {attribution_data[f'{mode}_Baseline-D1']['total_return']:.4%} | {attribution_data[f'{mode}_Baseline-D1']['max_drawdown']:.4%} |")
        final_report.append(f"| Baseline-D1+D2 | {attribution_data[f'{mode}_Baseline-D1+D2']['obs_buys']} | {attribution_data[f'{mode}_Baseline-D1+D2']['entries']} | {attribution_data[f'{mode}_Baseline-D1+D2']['info_contrib']:.4%} | {attribution_data[f'{mode}_Baseline-D1+D2']['total_return']:.4%} | {attribution_data[f'{mode}_Baseline-D1+D2']['max_drawdown']:.4%} |")
        final_report.append(f"| Rule E | {attribution_data[f'{mode}_Rule E']['obs_buys']} | {attribution_data[f'{mode}_Rule E']['entries']} | {attribution_data[f'{mode}_Rule E']['info_contrib']:.4%} | {attribution_data[f'{mode}_Rule E']['total_return']:.4%} | {attribution_data[f'{mode}_Rule E']['max_drawdown']:.4%} |")
        final_report.append("")

    (RESULTS_DIR / "v9_attribution.json").write_text(json.dumps(attribution_data, indent=2))
    (RESULTS_DIR / "v9_final_report.md").write_text("\n".join(final_report), encoding="utf-8")
    
    print("\nTest completed. Artifacts generated in results directory.")

if __name__ == "__main__":
    main()
