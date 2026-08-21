#!/usr/bin/env python3
"""Event-study the preregistered high-volatility trend participation module."""
from __future__ import annotations

import json
import runpy
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
SLIPPAGE = 0.001
COOLDOWN = 20


@dataclass(frozen=True)
class TrendDefinition:
    rs20_min: float
    volume_min: float
    atr_min: float
    atr_max: float
    extension_min: float
    extension_max: float
    close_location_min: float


DEFINITIONS = {
    "hv_relaxed": TrendDefinition(0.03, 1.2, 0.04, 0.12, 0.12, 0.30, 0.50),
    "hv_central": TrendDefinition(0.05, 1.5, 0.04, 0.12, 0.12, 0.25, 0.60),
    "hv_strict": TrendDefinition(0.10, 2.0, 0.04, 0.10, 0.12, 0.20, 0.70),
    "rsr1_low_vol_comparator": TrendDefinition(0.03, 1.2, -1.0, 0.04, 0.00, 0.12, 0.50),
}
PERIODS = {
    "development_2024_2025": (pd.Timestamp("2024-01-02"), pd.Timestamp("2025-12-31")),
    "retrospective_2026": (pd.Timestamp("2026-01-02"), pd.Timestamp("2026-08-07")),
}


def signal_components(
    panels: dict[str, pd.DataFrame], symbols: list[str]
) -> dict[str, pd.DataFrame | pd.Series]:
    close, open_, high, low, volume = (
        panels[name] for name in ("close", "open", "high", "low", "volume")
    )
    stock_close = close[symbols]
    ma20 = stock_close.rolling(20, min_periods=20).mean()
    ma50 = stock_close.rolling(50, min_periods=50).mean()
    previous_high20 = high[symbols].rolling(20, min_periods=20).max().shift(1)
    rs20 = (stock_close / stock_close.shift(20) - 1.0).sub(
        close["SMH"] / close["SMH"].shift(20) - 1.0, axis=0
    )
    volume_ratio = volume[symbols] / volume[symbols].rolling(20, min_periods=20).mean().shift(1)
    extension = stock_close / ma20 - 1.0
    prior_close = stock_close.shift(1)
    true_range = pd.DataFrame(
        np.maximum.reduce(
            [
                (high[symbols] - low[symbols]).to_numpy(),
                (high[symbols] - prior_close).abs().to_numpy(),
                (low[symbols] - prior_close).abs().to_numpy(),
            ]
        ),
        index=stock_close.index,
        columns=symbols,
    )
    atr_pct = true_range.rolling(14, min_periods=14).mean() / stock_close
    close_location = (stock_close - low[symbols]) / (high[symbols] - low[symbols]).replace(0.0, np.nan)
    positive_gap = open_[symbols] / prior_close - 1.0 >= 0.10
    day_range = (high[symbols] - low[symbols]) / open_[symbols]
    event_block = positive_gap | positive_gap.shift(1).fillna(False)
    event_block |= positive_gap.shift(2).fillna(False) & (day_range >= 0.03)

    broad_healthy = (
        (close["SPY"] > close["SPY"].rolling(200, min_periods=200).mean())
        & (close["QQQ"] > close["QQQ"].rolling(100, min_periods=100).mean())
        & (close["^VIX"] < 25.0)
        & (close["^VIX"] / close["^VIX3M"] < 1.0)
    )
    smh_healthy = close["SMH"] >= close["SMH"].rolling(50, min_periods=50).mean()
    shared = (
        (stock_close > ma20)
        & (stock_close > ma50)
        & (stock_close > previous_high20)
        & ~event_block
    )
    shared = shared.mul(broad_healthy & smh_healthy, axis=0).fillna(False)
    return {
        "shared": shared,
        "rs20": rs20,
        "volume_ratio": volume_ratio,
        "extension": extension,
        "atr_pct": atr_pct,
        "close_location": close_location,
    }


def definition_signal(components: dict, definition: TrendDefinition) -> pd.DataFrame:
    return (
        components["shared"]
        & (components["rs20"] >= definition.rs20_min)
        & (components["volume_ratio"] >= definition.volume_min)
        & (components["atr_pct"] > definition.atr_min)
        & (components["atr_pct"] <= definition.atr_max)
        & (components["extension"] > definition.extension_min)
        & (components["extension"] <= definition.extension_max)
        & (components["close_location"] >= definition.close_location_min)
    ).fillna(False)


def deduplicated_events(signal: pd.DataFrame, cooldown: int = COOLDOWN) -> list[tuple[pd.Timestamp, str]]:
    events = []
    for symbol in signal.columns:
        last_location = -cooldown - 1
        for location, date in enumerate(signal.index):
            if bool(signal.at[date, symbol]) and location - last_location > cooldown:
                events.append((date, symbol))
                last_location = location
    return sorted(events)


def event_outcomes(
    panels: dict[str, pd.DataFrame],
    components: dict,
    variant: str,
    signal: pd.DataFrame,
) -> pd.DataFrame:
    close, open_, high, low = (panels[name] for name in ("close", "open", "high", "low"))
    dates = close.index
    rows = []
    for signal_date, symbol in deduplicated_events(signal):
        signal_location = dates.get_loc(signal_date)
        if signal_location + 1 >= len(dates):
            continue
        entry_location = signal_location + 1
        entry_date = dates[entry_location]
        entry_open = float(open_.at[entry_date, symbol])
        qqq_open = float(open_.at[entry_date, "QQQ"])
        if not np.isfinite(entry_open) or entry_open <= 0 or not np.isfinite(qqq_open) or qqq_open <= 0:
            continue
        base = {
            "variant": variant,
            "signal_date": signal_date,
            "entry_date": entry_date,
            "symbol": symbol,
            "signal_close": float(close.at[signal_date, symbol]),
            "entry_open": entry_open,
            "entry_gap": float(entry_open / close.at[signal_date, symbol] - 1.0),
            "rs20": float(components["rs20"].at[signal_date, symbol]),
            "volume_ratio": float(components["volume_ratio"].at[signal_date, symbol]),
            "atr_pct": float(components["atr_pct"].at[signal_date, symbol]),
            "extension": float(components["extension"].at[signal_date, symbol]),
            "close_location": float(components["close_location"].at[signal_date, symbol]),
        }
        for horizon in (5, 10, 20):
            exit_location = entry_location + horizon - 1
            if exit_location >= len(dates):
                continue
            exit_date = dates[exit_location]
            path = dates[entry_location : exit_location + 1]
            entry_fill = entry_open * (1.0 + SLIPPAGE)
            exit_fill = float(close.at[exit_date, symbol]) * (1.0 - SLIPPAGE)
            net_return = exit_fill / entry_fill - 1.0
            qqq_return = float(close.at[exit_date, "QQQ"]) / qqq_open - 1.0
            rows.append(
                {
                    **base,
                    "horizon": horizon,
                    "exit_date": exit_date,
                    "net_return": net_return,
                    "qqq_return": qqq_return,
                    "excess_qqq": net_return - qqq_return,
                    "mae": float(low.loc[path, symbol].min() / entry_fill - 1.0),
                    "mfe": float(high.loc[path, symbol].max() / entry_fill - 1.0),
                }
            )
    return pd.DataFrame(rows)


def summarize(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for period, (start, end) in PERIODS.items():
        for variant in DEFINITIONS:
            for horizon in (5, 10, 20):
                sample = events.loc[
                    events["variant"].eq(variant)
                    & events["horizon"].eq(horizon)
                    & events["signal_date"].between(start, end)
                ]
                rows.append(
                    {
                        "period": period,
                        "variant": variant,
                        "horizon": horizon,
                        "events": len(sample),
                        "mean_return": float(sample["net_return"].mean()) if len(sample) else np.nan,
                        "median_return": float(sample["net_return"].median()) if len(sample) else np.nan,
                        "win_rate": float(sample["net_return"].gt(0).mean()) if len(sample) else np.nan,
                        "mean_excess_qqq": float(sample["excess_qqq"].mean()) if len(sample) else np.nan,
                        "mean_mae": float(sample["mae"].mean()) if len(sample) else np.nan,
                        "mean_mfe": float(sample["mfe"].mean()) if len(sample) else np.nan,
                        "mfe_mae_ratio": (
                            float(sample["mfe"].mean() / abs(sample["mae"].mean()))
                            if len(sample) and sample["mae"].mean() < 0
                            else np.nan
                        ),
                    }
                )
    return pd.DataFrame(rows)


def positive_return_concentration(events: pd.DataFrame) -> float:
    sample = events.loc[
        events["variant"].eq("hv_central")
        & events["horizon"].eq(20)
        & events["net_return"].gt(0)
        & events["signal_date"].between(PERIODS["development_2024_2025"][0], PERIODS["retrospective_2026"][1])
    ]
    gross = sample.groupby("symbol")["net_return"].sum()
    return float(gross.max() / gross.sum()) if not gross.empty and gross.sum() > 0 else np.nan


def continuation_gate(metrics: pd.DataFrame, events: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    m20 = metrics.loc[metrics["horizon"].eq(20)].set_index(["period", "variant"])
    central = m20.xs("hv_central", level="variant")
    checks = {
        "minimum_event_count": bool(
            central.at["development_2024_2025", "events"] >= 15
            and central.at["retrospective_2026", "events"] >= 5
        ),
        "positive_mean_both": bool((central["mean_return"] > 0).all()),
        "positive_median_both": bool((central["median_return"] > 0).all()),
        "positive_excess_both": bool((central["mean_excess_qqq"] > 0).all()),
        "win_rate_ge_50_both": bool((central["win_rate"] >= 0.50).all()),
        "mfe_mae_ge_1_25_both": bool((central["mfe_mae_ratio"] >= 1.25).all()),
    }
    concentration = positive_return_concentration(events)
    checks["positive_return_concentration_le_35"] = bool(
        np.isfinite(concentration) and concentration <= 0.35
    )
    neighbor_rows = []
    for variant in ("hv_relaxed", "hv_central", "hv_strict"):
        sample = m20.xs(variant, level="variant")
        passes = bool(
            (sample["mean_return"] > 0).all()
            and (sample["median_return"] > 0).all()
            and (sample["mean_excess_qqq"] > 0).all()
        )
        neighbor_rows.append({"variant": variant, "positive_in_both_periods": passes})
    neighbors = pd.DataFrame(neighbor_rows)
    checks["two_of_three_neighbors_positive"] = bool(neighbors["positive_in_both_periods"].sum() >= 2)
    summary = {
        **checks,
        "positive_return_concentration": concentration,
        "passes_event_continuation_gate": all(checks.values()),
    }
    return summary, neighbors


def pct(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2%}"


def write_report(metrics: pd.DataFrame, gate: dict, neighbors: pd.DataFrame) -> None:
    m20 = metrics.loc[metrics["horizon"].eq(20)]
    lines = [
        "# High-volatility trend participation event study",
        "",
        "## Boundary",
        "",
        "The definitions and continuation gate were frozen in `high-vol-trend-preregistration.md` before reading these outputs. The current-list universe is hindsight-selected, and the numerical module was specified after seeing 2026; all results are retrospective and cannot authorize a trade.",
        "",
        "## 20-session outcomes",
        "",
        "| Period | Variant | Events | Mean | Median | Win rate | Mean excess vs QQQ | Mean MAE | Mean MFE | MFE/|MAE| |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in m20.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.variant} | {row.events} | {pct(row.mean_return)} | "
            f"{pct(row.median_return)} | {pct(row.win_rate)} | {pct(row.mean_excess_qqq)} | "
            f"{pct(row.mean_mae)} | {pct(row.mean_mfe)} | "
            f"{'n/a' if pd.isna(row.mfe_mae_ratio) else f'{row.mfe_mae_ratio:.2f}'} |"
        )
    lines.extend(["", "## Continuation gate", ""])
    for key, value in gate.items():
        if key in {"positive_return_concentration", "passes_event_continuation_gate"}:
            continue
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            f"- `positive_return_concentration`: `{pct(gate['positive_return_concentration'])}`",
            f"- `passes_event_continuation_gate`: `{gate['passes_event_continuation_gate']}`",
            "",
            "## Decision",
            "",
        ]
    )
    if gate["passes_event_continuation_gate"]:
        lines.append("The event layer passes the preregistered screen and may proceed to a separately specified portfolio simulation. It is still not promotable without genuine forward evidence.")
    else:
        lines.append("Stop this branch. Do not build or optimize a high-volatility portfolio sleeve on the same data. Continue recording missed high-volatility leaders as a non-trading diagnostic only.")
    (RESULTS / "high_vol_trend_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    components = signal_components(panels, symbols)
    blocks = []
    for name, definition in DEFINITIONS.items():
        signal = definition_signal(components, definition)
        block = event_outcomes(panels, components, name, signal)
        if not block.empty:
            blocks.append(block)
    events = pd.concat(blocks, ignore_index=True) if blocks else pd.DataFrame()
    metrics = summarize(events)
    gate, neighbors = continuation_gate(metrics, events)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_last_date": str(panels["close"].index[-1].date()),
        "universe": "ai_capex_broad",
        "symbols": len(symbols),
        "research_only": True,
        "authorizes_trade": False,
        **gate,
        "decision": (
            "proceed_to_portfolio_simulation_research_only"
            if gate["passes_event_continuation_gate"]
            else "stop_high_vol_sleeve_branch_keep_diagnostic_only"
        ),
    }
    events.to_csv(RESULTS / "high_vol_trend_events.csv", index=False)
    metrics.to_csv(RESULTS / "high_vol_trend_metrics.csv", index=False)
    neighbors.to_csv(RESULTS / "high_vol_trend_neighbors.csv", index=False)
    (RESULTS / "high_vol_trend_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, gate, neighbors)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
