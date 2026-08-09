"""Frozen event study for the read-only market/semiconductor turn monitor."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from v9_data import load_data
from v9_research_monitors import market_semiconductor_turn_snapshot


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "results" / "validation" / "market_semiconductor_turn_validation.json"
OUT_MD = ROOT / "results" / "validation" / "market-semiconductor-turn-validation.md"
HORIZONS = (5, 10, 21, 63)


def forward_rows(close: pd.DataFrame, dates: list[pd.Timestamp]) -> list[dict]:
    rows: list[dict] = []
    for dt in dates:
        loc = close.index.get_loc(dt)
        if not isinstance(loc, int):
            continue
        row: dict = {"date": str(dt.date())}
        for horizon in HORIZONS:
            if loc + horizon >= len(close):
                continue
            for ticker in ("SPY", "QQQ", "SMH"):
                row[f"{ticker}_{horizon}d"] = float(close[ticker].iloc[loc + horizon] / close[ticker].iloc[loc] - 1.0)
            row[f"SMH_excess_QQQ_{horizon}d"] = row[f"SMH_{horizon}d"] - row[f"QQQ_{horizon}d"]
        rows.append(row)
    return rows


def summarize(rows: list[dict]) -> dict:
    frame = pd.DataFrame(rows)
    metrics: dict = {}
    for column in frame.columns:
        if column == "date":
            continue
        values = pd.to_numeric(frame[column], errors="coerce").dropna()
        metrics[column] = {
            "count": int(len(values)),
            "mean": None if values.empty else float(values.mean()),
            "median": None if values.empty else float(values.median()),
            "positive_rate": None if values.empty else float((values > 0).mean()),
        }
    return {"event_count": len(rows), "metrics": metrics, "rows": rows}


def main() -> None:
    panels, vix, metadata = load_data()
    close = panels["close"].dropna(subset=["SPY", "QQQ", "SMH", "RSP", "HYG", "LQD"])
    snapshots = []
    for dt in close.index[200:]:
        snapshots.append(market_semiconductor_turn_snapshot(close, vix, dt))

    confirmed_dates: list[pd.Timestamp] = []
    baseline_dates: list[pd.Timestamp] = []
    previous_confirmed = False
    for snapshot in snapshots:
        dt = pd.Timestamp(snapshot["as_of"])
        confirmed = bool(snapshot.get("confirmed_turn"))
        if confirmed and not previous_confirmed:
            confirmed_dates.append(dt)
        previous_confirmed = confirmed
        measurements = snapshot.get("measurements") or {}
        confirmations = snapshot.get("confirmations") or {}
        if (
            snapshot.get("recent_stress_base")
            and measurements.get("fear_regime") in {"normal", "elevated"}
            and confirmations.get("qqq_above_ma20")
        ):
            baseline_dates.append(dt)

    candidate = summarize(forward_rows(close, confirmed_dates))
    baseline = summarize(forward_rows(close, baseline_dates))
    adequate_count = candidate["event_count"] >= 20
    result = {
        "experiment": "market_semiconductor_turn_monitor",
        "as_of": metadata.get("last_date"),
        "data_start": str(close.index.min().date()),
        "data_end": str(close.index.max().date()),
        "candidate_rising_edges": candidate,
        "baseline_stress_repair_days": baseline,
        "promotion_eligible": False,
        "adequate_independent_event_count": adequate_count,
        "decision": (
            "eligible_for_further_out_of_sample_review" if adequate_count
            else "insufficient_independent_events; keep monitor-only"
        ),
        "authorizes_trade": False,
        "thresholds_optimized": False,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    def median(group: dict, key: str) -> str:
        value = ((group.get("metrics") or {}).get(key) or {}).get("median")
        return "n/a" if value is None else f"{value:.2%}"

    lines = [
        "# Market / Semiconductor Turn Monitor Validation",
        "",
        f"- Data: `{result['data_start']}` to `{result['data_end']}`",
        f"- Confirmed-turn rising edges: `{candidate['event_count']}`",
        f"- Baseline stress-repair days: `{baseline['event_count']}`",
        f"- Decision: `{result['decision']}`",
        "- Formal weights changed: `false`",
        "- Authorizes trade: `false`",
        "",
        "| Horizon | Candidate SMH median | Baseline SMH median | Candidate SMH-QQQ median | Baseline SMH-QQQ median |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for horizon in HORIZONS:
        lines.append(
            f"| {horizon}d | {median(candidate, f'SMH_{horizon}d')} | {median(baseline, f'SMH_{horizon}d')} | "
            f"{median(candidate, f'SMH_excess_QQQ_{horizon}d')} | {median(baseline, f'SMH_excess_QQQ_{horizon}d')} |"
        )
    lines += [
        "",
        "This is a descriptive event study. Rising-edge count below 20 is an automatic non-promotion result.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
