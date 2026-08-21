#!/usr/bin/env python3
"""Read-only forward attribution of avoided loss, missed winners, and RSR2 path effects."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
START = pd.Timestamp("2026-08-17")
INPUTS = {
    "signals": RESULTS / "forward_shadow_signals.csv",
    "baseline": RESULTS / "forward_shadow_baseline_trades.csv",
    "rsr1": RESULTS / "forward_shadow_ledger.csv",
    "rsr2": RESULTS / "forward_profit_protection_ledger.csv",
    "status": RESULTS / "forward_shadow_status.json",
}
OVERLAY_COLUMNS = [
    "symbol",
    "signal_date",
    "rsr1_pnl",
    "rsr2_pnl",
    "observed_pnl_delta",
    "direct_exit_effect_on_rsr1_shares",
    "capital_path_and_sizing_residual",
    "rsr1_exit_reason",
    "rsr2_exit_reason",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def truthy(series: pd.Series) -> pd.Series:
    return series.fillna(False).astype(str).str.lower().isin({"true", "1", "yes"})


def closed_trades(frame: pd.DataFrame, ledger: bool) -> pd.DataFrame:
    columns = ["symbol", "signal_date", "entry_date", "entry_price", "shares", "exit_date", "exit_price", "exit_reason", "pnl", "return"]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    data = frame.copy()
    if ledger:
        data = data.rename(columns={"planned_execution_date": "entry_date", "net_pnl": "pnl"})
        if "signal_status" in data:
            data = data.loc[data["signal_status"].eq("closed")]
        if "source_complete" in data:
            data = data.loc[truthy(data["source_complete"])]
    for column in columns:
        if column not in data:
            data[column] = pd.NA
    data["signal_date"] = pd.to_datetime(data["signal_date"], errors="coerce")
    data = data.loc[data["signal_date"].notna() & (data["signal_date"] >= START)].copy()
    for column in ("entry_price", "shares", "exit_price", "pnl", "return"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.loc[data["exit_date"].notna() & data["pnl"].notna() & data["return"].notna()].copy()
    data["signal_date"] = data["signal_date"].dt.strftime("%Y-%m-%d")
    return data[columns].reset_index(drop=True)


def keyed(frame: pd.DataFrame) -> dict[tuple[str, str], dict]:
    result = {}
    for row in frame.to_dict("records"):
        key = (str(row["symbol"]), str(row["signal_date"]))
        if key in result:
            raise RuntimeError(f"duplicate forward trade key: {key}")
        result[key] = row
    return result


def direct_exclusion_keys(signals: pd.DataFrame) -> set[tuple[str, str]]:
    if signals.empty:
        return set()
    required = {"date", "symbol", "matched_baseline_signal", "risk_filter_signal"}
    if not required.issubset(signals.columns):
        raise RuntimeError(f"forward signal schema missing: {sorted(required - set(signals.columns))}")
    dates = pd.to_datetime(signals["date"], errors="coerce")
    mask = (
        dates.ge(START)
        & truthy(signals["matched_baseline_signal"])
        & ~truthy(signals["risk_filter_signal"])
    )
    return set(zip(signals.loc[mask, "symbol"].astype(str), dates.loc[mask].dt.strftime("%Y-%m-%d")))


def direct_exclusion_summary(baseline: dict, exclusion_keys: set[tuple[str, str]]) -> dict:
    rows = [baseline[key] for key in sorted(set(baseline) & exclusion_keys)]
    if not rows:
        return {
            "status": "awaiting_closed_baseline_exclusion",
            "closed_direct_exclusions": 0,
            "avoided_losing_trades": None,
            "avoided_loss_dollars": None,
            "missed_winning_trades": None,
            "missed_profit_dollars": None,
            "net_pnl_removed": None,
        }
    pnl = pd.Series([float(row["pnl"]) for row in rows], dtype=float)
    return {
        "status": "observing",
        "closed_direct_exclusions": len(rows),
        "avoided_losing_trades": int((pnl <= 0).sum()),
        "avoided_loss_dollars": float(-pnl.loc[pnl <= 0].sum()),
        "missed_winning_trades": int((pnl > 0).sum()),
        "missed_profit_dollars": float(pnl.loc[pnl > 0].sum()),
        "net_pnl_removed": float(pnl.sum()),
    }


def overlay_summary(rsr1: dict, rsr2: dict) -> tuple[dict, pd.DataFrame]:
    keys = sorted(set(rsr1) & set(rsr2))
    rows = []
    for key in keys:
        left, right = rsr1[key], rsr2[key]
        observed = float(right["pnl"] - left["pnl"])
        direct = float(left["shares"] * (right["exit_price"] - left["exit_price"]))
        rows.append(
            {
                "symbol": key[0],
                "signal_date": key[1],
                "rsr1_pnl": float(left["pnl"]),
                "rsr2_pnl": float(right["pnl"]),
                "observed_pnl_delta": observed,
                "direct_exit_effect_on_rsr1_shares": direct,
                "capital_path_and_sizing_residual": observed - direct,
                "rsr1_exit_reason": left["exit_reason"],
                "rsr2_exit_reason": right["exit_reason"],
            }
        )
    details = pd.DataFrame(rows).reindex(columns=OVERLAY_COLUMNS)
    if details.empty:
        return (
            {
                "status": "awaiting_paired_rsr_exit",
                "paired_closed_trades": 0,
                "aggregate_pnl_delta": None,
                "aggregate_direct_exit_effect": None,
                "aggregate_capital_path_and_sizing_residual": None,
                "largest_positive_delta_share": None,
                "two_largest_positive_delta_share": None,
            },
            details,
        )
    total = float(details["observed_pnl_delta"].sum())
    positive = details.loc[details["observed_pnl_delta"] > 0, "observed_pnl_delta"].sort_values(ascending=False)
    return (
        {
            "status": "observing",
            "paired_closed_trades": int(len(details)),
            "improved": int((details["observed_pnl_delta"] > 1e-9).sum()),
            "worsened": int((details["observed_pnl_delta"] < -1e-9).sum()),
            "unchanged": int((details["observed_pnl_delta"].abs() <= 1e-9).sum()),
            "aggregate_pnl_delta": total,
            "aggregate_direct_exit_effect": float(details["direct_exit_effect_on_rsr1_shares"].sum()),
            "aggregate_capital_path_and_sizing_residual": float(details["capital_path_and_sizing_residual"].sum()),
            "largest_positive_delta_share": float(positive.iloc[:1].sum() / total) if total else None,
            "two_largest_positive_delta_share": float(positive.iloc[:2].sum() / total) if total else None,
            "profit_lock_exits": int(details["rsr2_exit_reason"].eq("profit_lock").sum()),
        },
        details,
    )


def evaluate() -> tuple[dict, pd.DataFrame]:
    status = json.loads(INPUTS["status"].read_text(encoding="utf-8"))
    signals = read_csv(INPUTS["signals"])
    baseline = keyed(closed_trades(read_csv(INPUTS["baseline"]), ledger=False))
    rsr1 = keyed(closed_trades(read_csv(INPUTS["rsr1"]), ledger=True))
    rsr2 = keyed(closed_trades(read_csv(INPUTS["rsr2"]), ledger=True))
    exclusion = direct_exclusion_summary(baseline, direct_exclusion_keys(signals))
    overlay, details = overlay_summary(rsr1, rsr2)
    common_rsr1_baseline = set(rsr1) & set(baseline)
    review_eligible = bool(
        status.get("promotion_gate", {}).get("passed", False)
        and status.get("profit_protection_promotion_gate", {}).get("passed", False)
    )
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "changes_promotion_gate": False,
        "as_of": status.get("as_of"),
        "sessions": int(status.get("sessions", 0)),
        "input_hashes": {name: digest(path) for name, path in INPUTS.items()},
        "closed_trade_counts": {
            "matched_baseline": len(baseline),
            "RSR1-shadow": len(rsr1),
            "RSR2-profit-lock-shadow": len(rsr2),
        },
        "path_pairing": {
            "common_baseline_rsr1": len(common_rsr1_baseline),
            "baseline_only": len(set(baseline) - set(rsr1)),
            "rsr1_only": len(set(rsr1) - set(baseline)),
        },
        "direct_quality_exclusions": exclusion,
        "profit_lock_attribution": overlay,
        "review_eligible": review_eligible,
        "overall_status": "review_eligible"
        if review_eligible
        else ("observing" if exclusion["status"] == "observing" or overlay["status"] == "observing" else "awaiting_sample"),
        "historical_calibration_is_forward_evidence": False,
    }
    return summary, details


def money(value) -> str:
    return "unavailable" if value is None else f"${value:.2f}"


def count_text(value) -> str:
    return "unavailable" if value is None else str(value)


def write_report(summary: dict) -> None:
    exclusion = summary["direct_quality_exclusions"]
    overlay = summary["profit_lock_attribution"]
    lines = [
        "# Forward economic-edge attribution",
        "",
        "## Current state",
        "",
        f"- As of completed session: {summary['as_of']}",
        f"- Completed forward sessions: {summary['sessions']}",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Closed baseline / RSR1 / RSR2 trades: {summary['closed_trade_counts']['matched_baseline']} / {summary['closed_trade_counts']['RSR1-shadow']} / {summary['closed_trade_counts']['RSR2-profit-lock-shadow']}",
        "",
        "## Direct quality exclusions",
        "",
        f"- Status: `{exclusion['status']}`",
        f"- Closed direct exclusions: {exclusion['closed_direct_exclusions']}",
        f"- Avoided losing trades / dollars: {count_text(exclusion['avoided_losing_trades'])} / {money(exclusion['avoided_loss_dollars'])}",
        f"- Missed winning trades / dollars: {count_text(exclusion['missed_winning_trades'])} / {money(exclusion['missed_profit_dollars'])}",
        "",
        "## RSR2 versus RSR1",
        "",
        f"- Status: `{overlay['status']}`",
        f"- Paired closed trades: {overlay['paired_closed_trades']}",
        f"- Aggregate P&L delta: {money(overlay['aggregate_pnl_delta'])}",
        f"- Direct exit effect: {money(overlay['aggregate_direct_exit_effect'])}",
        f"- Capital/sizing path residual: {money(overlay['aggregate_capital_path_and_sizing_residual'])}",
        "",
        "Unavailable values mean no mature denominator; they are not zero. Historical calibration contributes zero forward evidence. This scorecard is read-only and authorizes no order or rule change.",
    ]
    (RESULTS / "forward_edge_attribution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary, details = evaluate()
    (RESULTS / "forward_edge_attribution.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    details.to_csv(RESULTS / "forward_edge_attribution_trades.csv", index=False)
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
