#!/usr/bin/env python3
"""Append-only forward diagnostics for missed trends and V9 core reversals."""
from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
V9 = QUANT_ROOT / "strategies" / "v9-execution"
sys.path.insert(0, str(V9 / "scripts"))

from v9_information_strategy import V9Backtester, V9Config  # noqa: E402


MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
EVENT = runpy.run_path(str(HERE / "evaluate_high_vol_trend.py"))
FORWARD = runpy.run_path(str(HERE / "run_forward_shadow.py"))
RESULTS = HERE / "results"
LEDGER = RESULTS / "forward_opportunity_diagnostics_ledger.csv"
STATUS_JSON = RESULTS / "forward_opportunity_diagnostics_status.json"
STATUS_MD = RESULTS / "forward_opportunity_diagnostics_status.md"
REGISTRATION = HERE / "forward-opportunity-diagnostics-preregistration.md"
START = pd.Timestamp("2026-08-17")
VERSION = "opportunity-diagnostics-v1"
ARRAY_FIELDS = (
    "rsr1_signal_symbols",
    "high_vol_central_symbols",
    "realized_5d_leaders",
    "high_vol_missed_leaders",
)
LEDGER_COLUMNS = [
    "date",
    "version",
    "source_complete",
    *ARRAY_FIELDS,
    "rsr1_signal_count",
    "high_vol_central_count",
    "realized_5d_leader_count",
    "high_vol_missed_leader_count",
    "smh_healthy",
    "core_month_end",
    "spy_base_target",
    "qqq_base_target",
    "core_cap",
    "spy_effective_target",
    "qqq_effective_target",
    "core_regime",
    "core_fear_score",
    "core_one_month_reversal",
    "research_only",
    "authorizes_trade",
]


def encode_symbols(symbols) -> str:
    return json.dumps(sorted(set(symbols)), ensure_ascii=False, separators=(",", ":"))


def core_monthly_table(engine: V9Backtester) -> pd.DataFrame:
    rows = []
    for location, date in enumerate(engine.close.index):
        if not engine._is_completed_month_end(location):
            continue
        base = engine.v8_base_weights[date]
        core_cap, _, fear = engine._effective_sleeve_caps(date)
        rows.append(
            {
                "date": date,
                "spy_base_target": float(base.get("SPY", 0.0)),
                "qqq_base_target": float(base.get("QQQ", 0.0)),
                "core_cap": float(core_cap),
                "spy_effective_target": float(base.get("SPY", 0.0) * core_cap),
                "qqq_effective_target": float(base.get("QQQ", 0.0) * core_cap),
                "core_regime": fear["regime"],
                "core_fear_score": int(fear["score"]),
            }
        )
    return pd.DataFrame(rows).set_index("date") if rows else pd.DataFrame()


def core_reversal_label(monthly: pd.DataFrame, date: pd.Timestamp) -> str:
    if monthly.empty or date not in monthly.index:
        return ""
    history = monthly.loc[:date]
    if len(history) < 3:
        return ""
    labels = set()
    for symbol in ("spy", "qqq"):
        values = history[f"{symbol}_effective_target"].iloc[-3:].astype(float).to_numpy()
        first_change = values[1] - values[0]
        second_change = values[2] - values[1]
        if first_change < -1e-12 and second_change > 1e-12:
            labels.add("down_then_up")
        elif first_change > 1e-12 and second_change < -1e-12:
            labels.add("up_then_down")
    return "+".join(sorted(labels))


def build_rows(
    panels: dict[str, pd.DataFrame],
    symbols: list[str],
    as_of: pd.Timestamp,
    start: pd.Timestamp = START,
) -> pd.DataFrame:
    dates = panels["close"].loc[start:as_of].index
    if dates.empty:
        return pd.DataFrame(columns=LEDGER_COLUMNS)
    _, candidate_config = FORWARD["frozen_configs"]()
    rsr_features = MODULE["build_features"](panels, symbols, candidate_config)
    rsr_signal = rsr_features["signal"].mul(rsr_features["smh_healthy"], axis=0).fillna(False)
    trend_components = EVENT["signal_components"](panels, symbols)
    trend_signal = EVENT["definition_signal"](
        trend_components, EVENT["DEFINITIONS"]["hv_central"]
    )
    vix = panels["close"][["^VIX", "^VIX3M"]].copy()
    engine = V9Backtester(
        panels,
        vix,
        [],
        V9Config(v8_core_weight=0.70, info_sleeve_weight=0.0),
        [],
    )
    monthly = core_monthly_table(engine)
    rows = []
    close = panels["close"]
    for date in dates:
        location = close.index.get_loc(date)
        window_start = max(0, location - 4)
        five_dates = close.index[window_start : location + 1]
        prior_location = location - 5
        realized = []
        if prior_location >= 0:
            prior_date = close.index[prior_location]
            for symbol in symbols:
                current = close.at[date, symbol]
                prior = close.at[prior_date, symbol]
                if pd.notna(current) and pd.notna(prior) and prior > 0 and current / prior - 1.0 >= 0.10:
                    realized.append(symbol)
        rsr_symbols = [symbol for symbol in symbols if bool(rsr_signal.at[date, symbol])]
        trend_symbols = [symbol for symbol in symbols if bool(trend_signal.at[date, symbol])]
        missed = []
        for symbol in realized:
            recent_rsr = bool(rsr_signal.loc[five_dates, symbol].any())
            atr = trend_components["atr_pct"].at[date, symbol]
            extension = trend_components["extension"].at[date, symbol]
            outside_low_vol = (
                (np.isfinite(atr) and float(atr) > 0.04)
                or (np.isfinite(extension) and float(extension) > 0.12)
            )
            if not recent_rsr and outside_low_vol:
                missed.append(symbol)
        month_end = date in monthly.index
        month = monthly.loc[date] if month_end else None
        rows.append(
            {
                "date": str(date.date()),
                "version": VERSION,
                "source_complete": True,
                "rsr1_signal_symbols": encode_symbols(rsr_symbols),
                "high_vol_central_symbols": encode_symbols(trend_symbols),
                "realized_5d_leaders": encode_symbols(realized),
                "high_vol_missed_leaders": encode_symbols(missed),
                "rsr1_signal_count": len(rsr_symbols),
                "high_vol_central_count": len(trend_symbols),
                "realized_5d_leader_count": len(realized),
                "high_vol_missed_leader_count": len(missed),
                "smh_healthy": bool(rsr_features["smh_healthy"].at[date]),
                "core_month_end": month_end,
                "spy_base_target": None if month is None else month["spy_base_target"],
                "qqq_base_target": None if month is None else month["qqq_base_target"],
                "core_cap": None if month is None else month["core_cap"],
                "spy_effective_target": None if month is None else month["spy_effective_target"],
                "qqq_effective_target": None if month is None else month["qqq_effective_target"],
                "core_regime": "" if month is None else month["core_regime"],
                "core_fear_score": None if month is None else month["core_fear_score"],
                "core_one_month_reversal": "" if month is None else core_reversal_label(monthly, date),
                "research_only": True,
                "authorizes_trade": False,
            }
        )
    return pd.DataFrame(rows, columns=LEDGER_COLUMNS)


def normalized(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy().reindex(columns=LEDGER_COLUMNS)
    for column in result.columns:
        result[column] = result[column].fillna("").astype(str)
    return result


def merge_immutable(existing: pd.DataFrame, computed: pd.DataFrame) -> pd.DataFrame:
    if existing.empty:
        merged = computed.copy()
    else:
        if (pd.to_datetime(existing["date"]) < START).any():
            raise RuntimeError("diagnostic ledger contains a pre-start row")
        old = normalized(existing).set_index("date")
        new = normalized(computed).set_index("date")
        overlap = old.index.intersection(new.index)
        if len(overlap) and not old.loc[overlap].equals(new.loc[overlap]):
            mismatched = [date for date in overlap if not old.loc[date].equals(new.loc[date])]
            raise RuntimeError(f"immutable diagnostic conflict: {mismatched}")
        additions = computed.loc[~computed["date"].isin(existing["date"])].copy()
        merged = pd.concat([existing, additions], ignore_index=True)
    if not merged.empty:
        merged = merged.sort_values("date").reset_index(drop=True)
    return merged.reindex(columns=LEDGER_COLUMNS)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def write_status(output: dict) -> None:
    lines = [
        "# Forward opportunity diagnostics",
        "",
        f"- Status: `{output['status']}`",
        f"- Completed data through: `{output['as_of']}`",
        f"- Required start: `{START.date()}`",
        f"- Source complete: `{output['source_complete']}`",
        f"- Recorded sessions: `{output['recorded_sessions']}`",
        f"- High-vol central signals: `{output['high_vol_central_signals']}`",
        f"- Realized high-vol missed leaders: `{output['high_vol_missed_leaders']}`",
        f"- Core one-month reversals: `{output['core_one_month_reversals']}`",
        "- Research-only: `true`",
        "- Authorizes trade: `false`",
        "",
        output["message"],
    ]
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols, sources, as_of, cutoff, source_complete, missing = FORWARD["extend_panels"]()
    symbols = FORWARD["shadow_universe"](all_symbols)
    relevant_missing = sorted(set(missing) & (set(symbols) | {"SPY", "QQQ", "SMH", "^VIX", "^VIX3M"}))
    complete = not relevant_missing and as_of >= cutoff
    existing = pd.read_csv(LEDGER) if LEDGER.exists() else pd.DataFrame(columns=LEDGER_COLUMNS)
    status = "awaiting_start"
    message = "No completed U.S. session at or after the registered start; the ledger was not changed."
    if as_of >= START and not complete:
        status = "data_incomplete"
        message = "Required completed-session data are incomplete; the immutable ledger was preserved."
    elif as_of >= START:
        computed = build_rows(panels, symbols, as_of)
        try:
            merged = merge_immutable(existing, computed)
        except RuntimeError as error:
            status = "immutable_conflict"
            message = str(error) + "; the ledger was preserved."
        else:
            merged.to_csv(LEDGER, index=False)
            existing = merged
            status = "observing"
            message = "Completed-session diagnostics appended or verified; no order is authorized."
    if not LEDGER.exists():
        existing.reindex(columns=LEDGER_COLUMNS).to_csv(LEDGER, index=False)
    output = {
        "version": VERSION,
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "status": status,
        "as_of": str(as_of.date()),
        "expected_completed_cutoff": str(cutoff.date()),
        "source_complete": complete,
        "missing_latest": relevant_missing,
        "recorded_sessions": len(existing),
        "high_vol_central_signals": int(pd.to_numeric(existing.get("high_vol_central_count", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "high_vol_missed_leaders": int(pd.to_numeric(existing.get("high_vol_missed_leader_count", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "core_one_month_reversals": int(existing.get("core_one_month_reversal", pd.Series(dtype=str)).fillna("").ne("").sum()),
        "research_only": True,
        "authorizes_trade": False,
        "registration_sha256": sha256(REGISTRATION),
        "ledger_sha256": sha256(LEDGER),
        "sources": sources,
        "message": message,
    }
    STATUS_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    write_status(output)
    print(json.dumps({key: output[key] for key in ("status", "as_of", "source_complete", "recorded_sessions", "message")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
