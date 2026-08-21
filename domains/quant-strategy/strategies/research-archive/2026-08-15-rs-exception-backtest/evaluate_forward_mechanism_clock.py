#!/usr/bin/env python3
"""Fixed-checkpoint forward evidence clock for entry quality and RSR2 exits."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

import pandas as pd

import evaluate_forward_edge_attribution as edge


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
INPUTS = edge.INPUTS
QUALITY_CHECKPOINTS = (5, 10, 20)
PAIRED_CHECKPOINTS = (5, 10, 20)
CHANGED_EXIT_CHECKPOINTS = (1, 2, 5)

OUTPUT_JSON = RESULTS / "forward_mechanism_evidence_clock.json"
OUTPUT_CSV = RESULTS / "forward_mechanism_evidence_clock.csv"
OUTPUT_REPORT = RESULTS / "forward_mechanism_evidence_clock_report.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordered(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.reset_index(drop=True)
    data = frame.copy()
    data["_exit_sort"] = pd.to_datetime(data["exit_date"], errors="coerce")
    data["_signal_sort"] = pd.to_datetime(data["signal_date"], errors="coerce")
    if data["_exit_sort"].isna().any() or data["_signal_sort"].isna().any():
        raise RuntimeError("closed mechanism outcome has an invalid date")
    data = data.sort_values(["_exit_sort", "_signal_sort", "symbol"], kind="stable")
    return data.drop(columns=["_exit_sort", "_signal_sort"]).reset_index(drop=True)


def direct_exclusion_rows(
    baseline: dict[tuple[str, str], dict], exclusion_keys: set[tuple[str, str]]
) -> pd.DataFrame:
    rows = []
    for key in sorted(set(baseline) & exclusion_keys):
        trade = baseline[key]
        rows.append(
            {
                "symbol": key[0],
                "signal_date": key[1],
                "exit_date": trade["exit_date"],
                "pnl": float(trade["pnl"]),
                "return": float(trade["return"]),
            }
        )
    return ordered(pd.DataFrame(rows, columns=["symbol", "signal_date", "exit_date", "pnl", "return"]))


def paired_rows(
    rsr1: dict[tuple[str, str], dict], rsr2: dict[tuple[str, str], dict]
) -> pd.DataFrame:
    rows = []
    for key in sorted(set(rsr1) & set(rsr2)):
        left, right = rsr1[key], rsr2[key]
        left_exit = pd.Timestamp(left["exit_date"])
        right_exit = pd.Timestamp(right["exit_date"])
        observed = float(right["pnl"] - left["pnl"])
        direct = float(left["shares"] * (right["exit_price"] - left["exit_price"]))
        rows.append(
            {
                "symbol": key[0],
                "signal_date": key[1],
                "exit_date": max(left_exit, right_exit).strftime("%Y-%m-%d"),
                "rsr1_pnl": float(left["pnl"]),
                "rsr2_pnl": float(right["pnl"]),
                "observed_pnl_delta": observed,
                "direct_exit_effect_on_rsr1_shares": direct,
                "capital_path_and_sizing_residual": observed - direct,
            }
        )
    columns = [
        "symbol",
        "signal_date",
        "exit_date",
        "rsr1_pnl",
        "rsr2_pnl",
        "observed_pnl_delta",
        "direct_exit_effect_on_rsr1_shares",
        "capital_path_and_sizing_residual",
    ]
    return ordered(pd.DataFrame(rows, columns=columns))


def quality_metrics(frame: pd.DataFrame) -> dict:
    if frame.empty:
        return {
            "outcomes": 0,
            "avoided_losers": None,
            "missed_winners": None,
            "loss_rate": None,
            "avoided_loss_dollars": None,
            "missed_profit_dollars": None,
            "net_pnl_removed": None,
            "mean_return": None,
            "direction": "awaiting_sample",
        }
    pnl = pd.to_numeric(frame["pnl"], errors="raise")
    returns = pd.to_numeric(frame["return"], errors="raise")
    losses = pnl <= 0
    loss_rate = float(losses.mean())
    net = float(pnl.sum())
    if loss_rate > 0.5 and net < 0:
        direction = "supportive_direction"
    elif loss_rate < 0.5 and net > 0:
        direction = "contradictory_direction"
    else:
        direction = "mixed_direction"
    return {
        "outcomes": int(len(frame)),
        "avoided_losers": int(losses.sum()),
        "missed_winners": int((pnl > 0).sum()),
        "loss_rate": loss_rate,
        "avoided_loss_dollars": float(-pnl.loc[losses].sum()),
        "missed_profit_dollars": float(pnl.loc[pnl > 0].sum()),
        "net_pnl_removed": net,
        "mean_return": float(returns.mean()),
        "direction": direction,
    }


def paired_metrics(frame: pd.DataFrame) -> dict:
    if frame.empty:
        return {
            "outcomes": 0,
            "rsr1_wins": None,
            "rsr2_wins": None,
            "win_rate_delta": None,
            "aggregate_total_pnl_delta": None,
            "aggregate_direct_exit_effect": None,
            "aggregate_path_sizing_residual": None,
            "direction": "awaiting_sample",
        }
    left = pd.to_numeric(frame["rsr1_pnl"], errors="raise")
    right = pd.to_numeric(frame["rsr2_pnl"], errors="raise")
    direct = float(frame["direct_exit_effect_on_rsr1_shares"].sum())
    win_delta = float((right > 0).mean() - (left > 0).mean())
    if direct > 0 and win_delta >= 0:
        direction = "supportive_direction"
    elif direct < 0 and win_delta <= 0:
        direction = "contradictory_direction"
    else:
        direction = "mixed_direction"
    return {
        "outcomes": int(len(frame)),
        "rsr1_wins": int((left > 0).sum()),
        "rsr2_wins": int((right > 0).sum()),
        "win_rate_delta": win_delta,
        "aggregate_total_pnl_delta": float(frame["observed_pnl_delta"].sum()),
        "aggregate_direct_exit_effect": direct,
        "aggregate_path_sizing_residual": float(
            frame["capital_path_and_sizing_residual"].sum()
        ),
        "direction": direction,
    }


def changed_exit_metrics(frame: pd.DataFrame) -> dict:
    if frame.empty:
        return {
            "outcomes": 0,
            "positive": None,
            "negative": None,
            "aggregate_direct_exit_effect": None,
            "direction": "awaiting_sample",
        }
    values = pd.to_numeric(frame["direct_exit_effect_on_rsr1_shares"], errors="raise")
    total = float(values.sum())
    direction = (
        "supportive_direction"
        if total > 0
        else "contradictory_direction" if total < 0 else "mixed_direction"
    )
    return {
        "outcomes": int(len(frame)),
        "positive": int((values > 0).sum()),
        "negative": int((values < 0).sum()),
        "aggregate_direct_exit_effect": total,
        "direction": direction,
    }


def checkpoint_clock(
    frame: pd.DataFrame,
    checkpoints: tuple[int, ...],
    metric_fn: Callable[[pd.DataFrame], dict],
) -> dict:
    count = int(len(frame))
    snapshots = []
    for checkpoint in checkpoints:
        if count < checkpoint:
            break
        snapshot = metric_fn(frame.iloc[:checkpoint].copy())
        snapshot["checkpoint"] = checkpoint
        snapshots.append(snapshot)
    next_checkpoint = next((checkpoint for checkpoint in checkpoints if checkpoint > count), None)
    return {
        "current_outcomes": count,
        "next_checkpoint": next_checkpoint,
        "latest_completed_checkpoint": snapshots[-1]["checkpoint"] if snapshots else None,
        "latest_checkpoint_interpretation": snapshots[-1]["direction"] if snapshots else "unavailable",
        "current_raw_metrics": metric_fn(frame),
        "checkpoint_snapshots": snapshots,
        "between_checkpoints_do_not_reclassify": bool(snapshots and count > snapshots[-1]["checkpoint"]),
    }


def evaluate() -> dict:
    status = json.loads(INPUTS["status"].read_text(encoding="utf-8"))
    signals = edge.read_csv(INPUTS["signals"])
    baseline = edge.keyed(edge.closed_trades(edge.read_csv(INPUTS["baseline"]), ledger=False))
    rsr1 = edge.keyed(edge.closed_trades(edge.read_csv(INPUTS["rsr1"]), ledger=True))
    rsr2 = edge.keyed(edge.closed_trades(edge.read_csv(INPUTS["rsr2"]), ledger=True))
    quality = direct_exclusion_rows(baseline, edge.direct_exclusion_keys(signals))
    paired = paired_rows(rsr1, rsr2)
    changed = paired.loc[
        paired["direct_exit_effect_on_rsr1_shares"].abs() > 1e-9
    ].reset_index(drop=True) if not paired.empty else paired.copy()

    quality_clock = checkpoint_clock(quality, QUALITY_CHECKPOINTS, quality_metrics)
    paired_clock = checkpoint_clock(paired, PAIRED_CHECKPOINTS, paired_metrics)
    changed_clock = checkpoint_clock(
        changed, CHANGED_EXIT_CHECKPOINTS, changed_exit_metrics
    )
    original_gate = bool(
        status.get("promotion_gate", {}).get("passed", False)
        and status.get("profit_protection_promotion_gate", {}).get("passed", False)
    )
    if original_gate:
        overall = "original_gate_review_eligible"
    elif quality_clock["latest_completed_checkpoint"] or paired_clock["latest_completed_checkpoint"]:
        overall = "checkpoint_frozen_observing"
    elif len(quality) or len(paired):
        overall = "accumulating_before_first_checkpoint"
    else:
        overall = "awaiting_sample"
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "real_account_modified": False,
        "live_order_authorization": False,
        "changes_promotion_gate": False,
        "new_parameter_search": False,
        "preregistration": "forward-mechanism-evidence-clock-preregistration.md",
        "as_of": status.get("as_of"),
        "sessions": int(status.get("sessions", 0)),
        "input_hashes": {name: digest(path) for name, path in INPUTS.items()},
        "checkpoints": {
            "entry_quality": list(QUALITY_CHECKPOINTS),
            "paired_rsr2": list(PAIRED_CHECKPOINTS),
            "changed_exit_diagnostic": list(CHANGED_EXIT_CHECKPOINTS),
        },
        "entry_quality_clock": quality_clock,
        "paired_rsr2_clock": paired_clock,
        "changed_exit_clock": changed_clock,
        "original_gate_review_eligible": original_gate,
        "overall_status": overall,
        "historical_calibration_is_forward_evidence": False,
        "decision": "accumulate immutable outcomes; interpret only frozen checkpoints; no rule or order change",
    }


def csv_rows(summary: dict) -> list[dict]:
    rows = []
    for mechanism, key in [
        ("entry_quality", "entry_quality_clock"),
        ("paired_rsr2", "paired_rsr2_clock"),
        ("changed_exit", "changed_exit_clock"),
    ]:
        clock = summary[key]
        rows.append(
            {
                "mechanism": mechanism,
                "current_outcomes": clock["current_outcomes"],
                "next_checkpoint": clock["next_checkpoint"],
                "latest_completed_checkpoint": clock["latest_completed_checkpoint"],
                "latest_checkpoint_interpretation": clock[
                    "latest_checkpoint_interpretation"
                ],
                "between_checkpoints_do_not_reclassify": clock[
                    "between_checkpoints_do_not_reclassify"
                ],
                "current_raw_direction": clock["current_raw_metrics"]["direction"],
            }
        )
    return rows


def write_report(summary: dict) -> None:
    quality = summary["entry_quality_clock"]
    paired = summary["paired_rsr2_clock"]
    changed = summary["changed_exit_clock"]
    lines = [
        "# Forward mechanism evidence clock",
        "",
        "## Current status",
        "",
        f"- Completed data through: `{summary['as_of']}`",
        f"- Completed forward sessions: {summary['sessions']}",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Original promotion-gate review eligible: `{summary['original_gate_review_eligible']}`",
        "",
        "| Mechanism | Current outcomes | Next fixed checkpoint | Latest frozen interpretation |",
        "| --- | ---: | ---: | --- |",
        f"| Entry-quality direct exclusions | {quality['current_outcomes']} | {quality['next_checkpoint'] or 'complete'} | {quality['latest_checkpoint_interpretation']} |",
        f"| Paired RSR1/RSR2 exits | {paired['current_outcomes']} | {paired['next_checkpoint'] or 'complete'} | {paired['latest_checkpoint_interpretation']} |",
        f"| Non-zero changed exits | {changed['current_outcomes']} | {changed['next_checkpoint'] or 'complete'} | {changed['latest_checkpoint_interpretation']} |",
        "",
        "## Interpretation discipline",
        "",
        "- Entry-quality and paired-strategy direction is reclassified only at 5, 10 and 20 closed outcomes.",
        "- Changed-exit economics are described at 1, 2 and 5 non-zero direct effects, but never promote RSR2.",
        "- Between checkpoints, raw dollars/counts may change while the last checkpoint label remains frozen.",
        "- Unavailable means no mature denominator; it never means zero economic effect.",
        "",
        "## Decision",
        "",
        "Continue append-only evidence collection. The first useful entry-quality/paired checkpoint is five outcomes; formal review still requires the original immutable gates. No order, formal V9 change, real-account change or historical parameter search is authorized.",
    ]
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary = evaluate()
    OUTPUT_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame(csv_rows(summary)).to_csv(OUTPUT_CSV, index=False)
    write_report(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

