#!/usr/bin/env python3
"""Read-only 5/20-session outcomes for immutable forward opportunity events."""
from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
LEDGER = RESULTS / "forward_opportunity_diagnostics_ledger.csv"
REGISTRATION = HERE / "forward-opportunity-outcome-preregistration.md"
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
HORIZONS = (5, 20)
EVENT_FIELDS = {
    "high_vol_central": "high_vol_central_symbols",
    "high_vol_missed_leader": "high_vol_missed_leaders",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def parse_symbols(value) -> list[str]:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return []
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        return []
    return sorted({str(symbol) for symbol in parsed if str(symbol)}) if isinstance(parsed, list) else []


def build_events(ledger: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    close, high, low = (panels[field] for field in ("close", "high", "low"))
    dates = close.index
    rows = []
    episode_state: dict[tuple[str, str], tuple[int, str]] = {}
    counters: dict[tuple[str, str], int] = {}
    for record in ledger.sort_values("date").itertuples(index=False):
        event_date = pd.Timestamp(record.date)
        if event_date not in dates:
            continue
        location = dates.get_loc(event_date)
        for event_type, field in EVENT_FIELDS.items():
            for symbol in parse_symbols(getattr(record, field)):
                key = (event_type, symbol)
                previous = episode_state.get(key)
                primary = previous is None or location - previous[0] > 5
                if primary:
                    counters[key] = counters.get(key, 0) + 1
                    episode_id = f"{event_type}:{symbol}:{counters[key]}"
                else:
                    episode_id = previous[1]
                episode_state[key] = (location, episode_id)
                reference = close.at[event_date, symbol] if symbol in close else np.nan
                base = {
                    "event_date": str(event_date.date()),
                    "event_type": event_type,
                    "symbol": symbol,
                    "episode_id": episode_id,
                    "primary_episode": primary,
                    "reference_close": reference,
                }
                for horizon in HORIZONS:
                    row = {**base, "horizon_sessions": horizon}
                    end_location = location + horizon
                    complete = (
                        end_location < len(dates)
                        and symbol in close
                        and symbol in high
                        and symbol in low
                        and pd.notna(reference)
                        and reference > 0
                    )
                    window = dates[location + 1 : end_location + 1] if complete else pd.DatetimeIndex([])
                    if complete:
                        horizon_close = close.at[dates[end_location], symbol]
                        highs = pd.to_numeric(high.loc[window, symbol], errors="coerce")
                        lows = pd.to_numeric(low.loc[window, symbol], errors="coerce")
                        complete = pd.notna(horizon_close) and highs.notna().all() and lows.notna().all()
                    row.update(
                        {
                            "matured": bool(complete),
                            "horizon_date": str(dates[end_location].date()) if complete else None,
                            "horizon_return": float(horizon_close / reference - 1.0) if complete else None,
                            "max_favorable_excursion": float(highs.max() / reference - 1.0) if complete else None,
                            "max_adverse_excursion": float(lows.min() / reference - 1.0) if complete else None,
                        }
                    )
                    rows.append(row)
    columns = [
        "event_date", "event_type", "symbol", "episode_id", "primary_episode",
        "reference_close", "horizon_sessions", "matured", "horizon_date",
        "horizon_return", "max_favorable_excursion", "max_adverse_excursion",
    ]
    return pd.DataFrame(rows, columns=columns)


def summarize(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for event_type in EVENT_FIELDS:
        for horizon in HORIZONS:
            block = events.loc[
                (events["event_type"] == event_type)
                & (events["horizon_sessions"] == horizon)
            ]
            matured = block.loc[block["matured"] & block["primary_episode"]]
            rows.append(
                {
                    "event_type": event_type,
                    "horizon_sessions": horizon,
                    "raw_events": int(len(block)),
                    "primary_episodes": int(block.loc[block["primary_episode"]]["episode_id"].nunique()),
                    "matured_primary_episodes": int(len(matured)),
                    "mean_return": float(matured["horizon_return"].mean()) if len(matured) else None,
                    "median_return": float(matured["horizon_return"].median()) if len(matured) else None,
                    "positive_return_rate": float((matured["horizon_return"] > 0).mean()) if len(matured) else None,
                    "mean_mfe": float(matured["max_favorable_excursion"].mean()) if len(matured) else None,
                    "mean_mae": float(matured["max_adverse_excursion"].mean()) if len(matured) else None,
                }
            )
    return pd.DataFrame(rows)


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{float(value):.2%}"


def write_report(summary: pd.DataFrame, meta: dict) -> None:
    lines = [
        "# Forward opportunity outcomes",
        "",
        f"- Completed data through: `{meta['as_of']}`",
        f"- Input ledger hash preserved: `{meta['input_ledger_hash_preserved']}`",
        "- Horizons: completed-session 5 and 20 only; no one-day decision metric.",
        "- Research-only; does not authorize a trade or alter RSR1/RSR2.",
        "",
        "| Event | Horizon | Raw events | Primary episodes | Matured | Mean return | Median | Positive | Mean MFE | Mean MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.event_type} | {row.horizon_sessions} | {row.raw_events} | "
            f"{row.primary_episodes} | {row.matured_primary_episodes} | "
            f"{pct(row.mean_return)} | {pct(row.median_return)} | "
            f"{pct(row.positive_return_rate)} | {pct(row.mean_mfe)} | {pct(row.mean_mae)} |"
        )
    lines.extend(
        [
            "",
            "Incomplete horizons remain `n/a` and contribute to no statistic. Repeated same-symbol observations within five sessions are shown as raw events but summarized once as an episode.",
        ]
    )
    (RESULTS / "forward_opportunity_outcomes_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    before = sha256(LEDGER)
    ledger = pd.read_csv(LEDGER) if LEDGER.exists() and LEDGER.stat().st_size else pd.DataFrame()
    panels, _ = BACKTEST["load_panels"]()
    events = build_events(ledger, panels) if not ledger.empty else build_events(pd.DataFrame(columns=["date", *EVENT_FIELDS.values()]), panels)
    summary = summarize(events)
    after = sha256(LEDGER)
    meta = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "as_of": str(panels["close"].index.max().date()),
        "registration_sha256": sha256(REGISTRATION),
        "input_ledger_sha256": after,
        "input_ledger_hash_preserved": before == after,
        "research_only": True,
        "authorizes_trade": False,
    }
    events.to_csv(RESULTS / "forward_opportunity_outcomes.csv", index=False)
    summary.to_csv(RESULTS / "forward_opportunity_outcomes_summary.csv", index=False)
    (RESULTS / "forward_opportunity_outcomes.json").write_text(
        json.dumps({**meta, "summary": summary.where(pd.notna(summary), None).to_dict("records")}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report(summary, meta)
    print(json.dumps({"as_of": meta["as_of"], "events": len(events) // len(HORIZONS), "matured_rows": int(events["matured"].sum()) if len(events) else 0, "ledger_preserved": meta["input_ledger_hash_preserved"]}, indent=2))


if __name__ == "__main__":
    main()
