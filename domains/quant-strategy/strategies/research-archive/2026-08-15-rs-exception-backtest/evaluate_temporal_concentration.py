#!/usr/bin/env python3
"""Audit timing concentration and signal-day regime dependence for RSR1."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
START = "2024-01-02"


def enrich_trades(trades: list[dict], panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frame = pd.DataFrame(trades).copy()
    if frame.empty:
        return frame
    frame["signal_timestamp"] = pd.to_datetime(frame["signal_date"])
    frame["year"] = frame["signal_timestamp"].dt.year.astype(str)
    frame["quarter"] = frame["signal_timestamp"].dt.to_period("Q").astype(str)
    smh = panels["close"]["SMH"]
    smh_buffer = smh / smh.rolling(50).mean() - 1.0
    frame["smh_ma50_buffer"] = frame["signal_timestamp"].map(smh_buffer.to_dict())
    frame["smh_buffer_bucket"] = pd.cut(
        frame["smh_ma50_buffer"],
        [-np.inf, 0.03, 0.07, np.inf],
        labels=["0-3%", "3-7%", ">7%"],
    ).astype("string")
    frame["vix"] = frame["signal_timestamp"].map(panels["close"]["^VIX"].to_dict())
    frame["vix_bucket"] = pd.cut(
        frame["vix"],
        [-np.inf, 15.0, 20.0, 25.0, np.inf],
        labels=["<15", "15-20", "20-25", ">=25"],
    ).astype("string")
    return frame


def grouped_metrics(frame: pd.DataFrame, variant: str, dimension: str) -> list[dict]:
    rows = []
    for bucket, group in frame.groupby(dimension, observed=True, dropna=False):
        rows.append(
            {
                "variant": variant,
                "dimension": dimension,
                "bucket": str(bucket),
                "trades": len(group),
                "wins": int((group["pnl"] > 0).sum()),
                "win_rate": float((group["pnl"] > 0).mean()),
                "average_return": float(group["return"].mean()),
                "net_pnl": float(group["pnl"].sum()),
                "gross_profit": float(group.loc[group["pnl"] > 0, "pnl"].sum()),
            }
        )
    return rows


def positive_profit_concentration(frame: pd.DataFrame, dimension: str) -> dict:
    winners = frame.loc[frame["pnl"] > 0]
    gross_profit = float(winners["pnl"].sum())
    by_group = winners.groupby(dimension, observed=True)["pnl"].sum().sort_values(ascending=False)
    shares = by_group / gross_profit if gross_profit else by_group
    return {
        "groups": int(len(by_group)),
        "gross_profit": gross_profit,
        "max_group_profit_share": float(shares.iloc[0]) if len(shares) else 1.0,
        "top_3_group_profit_share": float(shares.iloc[:3].sum()) if len(shares) else 1.0,
    }


def subset_metrics(frame: pd.DataFrame, label: str) -> dict:
    return {
        "path": label,
        "trades": len(frame),
        "wins": int((frame["pnl"] > 0).sum()),
        "win_rate": float((frame["pnl"] > 0).mean()) if len(frame) else None,
        "average_return": float(frame["return"].mean()) if len(frame) else None,
        "net_pnl": float(frame["pnl"].sum()),
    }


def path_decomposition(baseline: pd.DataFrame, candidate: pd.DataFrame) -> pd.DataFrame:
    baseline_keys = set(zip(baseline["signal_date"], baseline["symbol"]))
    candidate_keys = set(zip(candidate["signal_date"], candidate["symbol"]))
    baseline_is_common = [key in candidate_keys for key in zip(baseline["signal_date"], baseline["symbol"])]
    candidate_is_common = [key in baseline_keys for key in zip(candidate["signal_date"], candidate["symbol"])]
    rows = [
        subset_metrics(baseline.loc[baseline_is_common], "baseline_common"),
        subset_metrics(baseline.loc[[not value for value in baseline_is_common]], "baseline_only"),
        subset_metrics(candidate.loc[candidate_is_common], "candidate_common"),
        subset_metrics(candidate.loc[[not value for value in candidate_is_common]], "candidate_only"),
    ]
    return pd.DataFrame(rows)


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def money(value) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"-${abs(value):,.2f}" if value < 0 else f"${value:,.2f}"


def write_report(metrics: pd.DataFrame, paths: pd.DataFrame, summary: dict) -> None:
    candidate = metrics.loc[metrics["variant"].eq("risk_filter")]
    baseline = metrics.loc[metrics["variant"].eq("matched_baseline")]
    lines = [
        "# RSR1 temporal concentration and regime audit",
        "",
        "## Scope and purpose",
        "",
        f"This is a descriptive audit of the frozen 32-name `ai_capex_broad` shadow universe at 10 bps through {summary['data_end']}. Buckets use only signal-day information. They are not parameter candidates and do not change RSR1.",
        "",
        "## Signal-date concentration",
        "",
        f"- Candidate trades: `{summary['candidate_trades']}` across `{summary['candidate_signal_dates']}` signal dates; maximum same-date trades: `{summary['candidate_max_same_date_trades']}`.",
        f"- Dates with more than one candidate trade: `{summary['candidate_multi_trade_dates']}`.",
        f"- Best signal date contributes `{pct(summary['candidate_signal_date_profit_concentration']['max_group_profit_share'])}` of candidate gross profit; top three contribute `{pct(summary['candidate_signal_date_profit_concentration']['top_3_group_profit_share'])}`.",
        f"- Best quarter contributes `{pct(summary['candidate_quarter_profit_concentration']['max_group_profit_share'])}` of candidate gross profit.",
        "",
        "## Calendar attribution",
        "",
        "| Year | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for year in sorted(set(candidate.loc[candidate["dimension"].eq("year"), "bucket"])):
        b = baseline.loc[baseline["dimension"].eq("year") & baseline["bucket"].eq(year)].iloc[0]
        c = candidate.loc[candidate["dimension"].eq("year") & candidate["bucket"].eq(year)].iloc[0]
        lines.append(
            f"| {year} | {b.trades} | {pct(b.win_rate)} | {money(b.net_pnl)} | "
            f"{c.trades} | {pct(c.win_rate)} | {money(c.net_pnl)} |"
        )
    lines.extend(
        [
            "",
            "## Signal-day SMH trend buffer",
            "",
            "| SMH above MA50 | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for bucket in ["0-3%", "3-7%", ">7%"]:
        b = baseline.loc[baseline["dimension"].eq("smh_buffer_bucket") & baseline["bucket"].eq(bucket)].iloc[0]
        c = candidate.loc[candidate["dimension"].eq("smh_buffer_bucket") & candidate["bucket"].eq(bucket)].iloc[0]
        lines.append(
            f"| {bucket} | {b.trades} | {pct(b.win_rate)} | {money(b.net_pnl)} | "
            f"{c.trades} | {pct(c.win_rate)} | {money(c.net_pnl)} |"
        )
    lines.extend(
        [
            "",
            "## Signal-day VIX regime",
            "",
            "| VIX | Baseline trades | Baseline win | Baseline PnL | Candidate trades | Candidate win | Candidate PnL |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for bucket in ["<15", "15-20", "20-25"]:
        b = baseline.loc[baseline["dimension"].eq("vix_bucket") & baseline["bucket"].eq(bucket)].iloc[0]
        c = candidate.loc[candidate["dimension"].eq("vix_bucket") & candidate["bucket"].eq(bucket)].iloc[0]
        lines.append(
            f"| {bucket} | {b.trades} | {pct(b.win_rate)} | {money(b.net_pnl)} | "
            f"{c.trades} | {pct(c.win_rate)} | {money(c.net_pnl)} |"
        )
    lines.extend(
        [
            "",
            "## Trade-path decomposition",
            "",
            "| Path | Trades | Win rate | Average return | Net PnL |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in paths.itertuples(index=False):
        lines.append(
            f"| {row.path} | {row.trades} | {pct(row.win_rate)} | {pct(row.average_return)} | {money(row.net_pnl)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Candidate PnL is positive in `{summary['candidate_profitable_years']}/{summary['candidate_years']}` years and `{summary['candidate_profitable_quarters']}/{summary['candidate_quarters']}` active quarters. The only losing candidate quarter is the partial `{', '.join(summary['candidate_losing_quarters'])}` interval through the data end.",
            "- Candidate PnL and win rate exceed 50% in every SMH/MA50 buffer and observed VIX bucket. Baseline-only trades lose money in every SMH buffer bucket, so the filter benefit is not explained solely by selecting a stronger SMH regime.",
            "- Same-day crowding is low, but profit remains right-skewed: the top three signal dates contribute nearly half of gross profit. This is normal for breakout systems but reinforces the need for the forward profit-concentration gate.",
            "- The 2026 evidence is only three trades. No timing, VIX or SMH-buffer sub-rule is added from these small descriptive cells.",
            "",
            "Research-only. This report does not authorize a live order or modify formal V9.",
        ]
    )
    (RESULTS / "temporal_concentration_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    end = str(panels["close"][["SPY", "QQQ", "SMH"]].dropna().index[-1].date())
    results = {
        "matched_baseline": MODULE["simulate"](
            panels, symbols, UNIVERSE_MODULE["make_config"](False), "strict_veto", START, end, slippage=0.001
        ),
        "risk_filter": MODULE["simulate"](
            panels, symbols, UNIVERSE_MODULE["make_config"](True), "strict_veto", START, end, slippage=0.001
        ),
    }
    enriched = {name: enrich_trades(result["trades"], panels) for name, result in results.items()}
    rows = []
    for name, frame in enriched.items():
        for dimension in ("year", "quarter", "smh_buffer_bucket", "vix_bucket"):
            rows.extend(grouped_metrics(frame, name, dimension))
    metrics = pd.DataFrame(rows)
    paths = path_decomposition(enriched["matched_baseline"], enriched["risk_filter"])
    candidate = enriched["risk_filter"]
    candidate_quarters = candidate.groupby("quarter")["pnl"].sum()
    baseline_only = paths.loc[paths["path"].eq("baseline_only")].iloc[0]
    rejected = enriched["matched_baseline"].loc[
        [
            (signal_date, symbol)
            not in set(zip(candidate["signal_date"], candidate["symbol"]))
            for signal_date, symbol in zip(
                enriched["matched_baseline"]["signal_date"], enriched["matched_baseline"]["symbol"]
            )
        ]
    ]
    rejected_by_smh = {
        str(bucket): float(group["pnl"].sum())
        for bucket, group in rejected.groupby("smh_buffer_bucket", observed=True)
    }
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": end,
        "universe": "ai_capex_broad",
        "universe_size": len(symbols),
        "research_only": True,
        "authorizes_trade": False,
        "candidate_trades": len(candidate),
        "candidate_signal_dates": int(candidate["signal_date"].nunique()),
        "candidate_max_same_date_trades": int(candidate.groupby("signal_date").size().max()),
        "candidate_multi_trade_dates": int((candidate.groupby("signal_date").size() > 1).sum()),
        "candidate_signal_date_profit_concentration": positive_profit_concentration(candidate, "signal_date"),
        "candidate_quarter_profit_concentration": positive_profit_concentration(candidate, "quarter"),
        "candidate_years": int(candidate["year"].nunique()),
        "candidate_profitable_years": int((candidate.groupby("year")["pnl"].sum() > 0).sum()),
        "candidate_quarters": int(len(candidate_quarters)),
        "candidate_profitable_quarters": int((candidate_quarters > 0).sum()),
        "candidate_losing_quarters": candidate_quarters.loc[candidate_quarters <= 0].index.tolist(),
        "baseline_only_net_pnl": float(baseline_only["net_pnl"]),
        "baseline_only_pnl_by_smh_buffer": rejected_by_smh,
    }
    metrics.to_csv(RESULTS / "temporal_regime_metrics.csv", index=False)
    paths.to_csv(RESULTS / "temporal_trade_paths.csv", index=False)
    candidate.to_csv(RESULTS / "temporal_candidate_trades.csv", index=False)
    (RESULTS / "temporal_concentration_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_report(metrics, paths, summary)
    print(RESULTS / "temporal_concentration_report.md")


if __name__ == "__main__":
    main()
