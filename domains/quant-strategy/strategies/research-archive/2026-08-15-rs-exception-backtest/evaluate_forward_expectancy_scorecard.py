#!/usr/bin/env python3
"""Read-only forward expectancy and sampling-uncertainty scorecard."""
from __future__ import annotations

import json
import math
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
FORWARD = runpy.run_path(str(HERE / "run_forward_shadow.py"))
BOOTSTRAP_SAMPLES = 10_000
BOOTSTRAP_SEED = 20_260_815
MIN_CLOSED_TRADES = 20


def wilson_interval(wins: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0:
        return (float("nan"), float("nan"))
    p = wins / total
    denominator = 1.0 + z * z / total
    center = (p + z * z / (2.0 * total)) / denominator
    half = z * math.sqrt(p * (1.0 - p) / total + z * z / (4.0 * total * total)) / denominator
    return max(0.0, center - half), min(1.0, center + half)


def clustered_expectancy_bootstrap(
    trades: pd.DataFrame,
    samples: int = BOOTSTRAP_SAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> dict:
    if trades.empty:
        return {
            "entry_date_clusters": 0,
            "samples": samples,
            "p05": None,
            "median": None,
            "p95": None,
            "probability_nonpositive": None,
        }
    clusters = [
        pd.to_numeric(group["return"], errors="coerce").dropna().to_numpy(dtype=float)
        for _, group in trades.groupby("entry_cluster", sort=True)
    ]
    clusters = [cluster for cluster in clusters if len(cluster)]
    if not clusters:
        return {
            "entry_date_clusters": 0,
            "samples": samples,
            "p05": None,
            "median": None,
            "p95": None,
            "probability_nonpositive": None,
        }
    rng = np.random.default_rng(seed)
    means = np.empty(samples, dtype=float)
    count = len(clusters)
    for index in range(samples):
        selected = rng.integers(0, count, size=count)
        draw = np.concatenate([clusters[position] for position in selected])
        means[index] = float(draw.mean())
    return {
        "entry_date_clusters": count,
        "samples": samples,
        "p05": float(np.quantile(means, 0.05)),
        "median": float(np.quantile(means, 0.50)),
        "p95": float(np.quantile(means, 0.95)),
        "probability_nonpositive": float((means <= 0.0).mean()),
    }


def evidence_label(
    closed_trades: int,
    expectancy: float | None,
    bootstrap_p05: float | None,
    profit_factor: float | None,
    max_symbol_profit_share: float | None,
) -> str:
    if closed_trades < MIN_CLOSED_TRADES:
        return "awaiting_sample"
    if expectancy is None or expectancy <= 0.0:
        return "observed_negative"
    if bootstrap_p05 is None or bootstrap_p05 <= 0.0 or profit_factor is None or profit_factor < 1.30:
        return "positive_but_fragile"
    if max_symbol_profit_share is None or max_symbol_profit_share > 0.35:
        return "positive_concentrated"
    return "positive_diversified"


def normalize_trades(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "symbol",
        "signal_date",
        "entry_date",
        "exit_date",
        "pnl",
        "return",
    ]
    if frame is None or frame.empty:
        return pd.DataFrame(columns=columns + ["entry_cluster"])
    data = frame.copy()
    rename = {
        "planned_execution_date": "entry_date",
        "net_pnl": "pnl",
    }
    data = data.rename(columns=rename)
    if "signal_status" in data:
        data = data.loc[data["signal_status"] == "closed"]
    for column in columns:
        if column not in data:
            data[column] = np.nan
    data["pnl"] = pd.to_numeric(data["pnl"], errors="coerce")
    data["return"] = pd.to_numeric(data["return"], errors="coerce")
    data = data.loc[data["pnl"].notna() & data["return"].notna()].copy()
    data["symbol"] = data["symbol"].astype(str)
    data["entry_cluster"] = data["entry_date"].fillna(data["signal_date"]).astype(str)
    return data[columns + ["entry_cluster"]].reset_index(drop=True)


def longest_loss_streak(trades: pd.DataFrame) -> int:
    if trades.empty:
        return 0
    ordered = trades.copy()
    ordered["exit_sort"] = pd.to_datetime(ordered["exit_date"], errors="coerce")
    ordered = ordered.sort_values(["exit_sort", "entry_cluster", "symbol"], na_position="last")
    longest = current = 0
    for pnl in ordered["pnl"]:
        if pnl <= 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def score_trades(
    frame: pd.DataFrame,
    theme_map: dict[str, str],
    scope: str,
    variant: str,
) -> dict:
    trades = normalize_trades(frame)
    closed = len(trades)
    wins = trades.loc[trades["pnl"] > 0]
    losses = trades.loc[trades["pnl"] <= 0]
    win_rate = len(wins) / closed if closed else None
    win_low, win_high = wilson_interval(len(wins), closed)
    average_win = float(wins["return"].mean()) if len(wins) else None
    average_loss = float(losses["return"].mean()) if len(losses) else None
    payoff = (
        average_win / abs(average_loss)
        if average_win is not None and average_loss is not None and average_loss < 0
        else None
    )
    breakeven_win_rate = (
        abs(average_loss) / (average_win + abs(average_loss))
        if average_win is not None
        and average_loss is not None
        and average_loss < 0
        and average_win + abs(average_loss) > 0
        else None
    )
    expectancy = float(trades["return"].mean()) if closed else None
    gross_profit = float(wins["pnl"].sum()) if len(wins) else 0.0
    gross_loss = float(-losses.loc[losses["pnl"] < 0, "pnl"].sum()) if len(losses) else 0.0
    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 999.0 if gross_profit > 0 else None
    )
    profit_by_symbol = (
        wins.groupby("symbol")["pnl"].sum().sort_values(ascending=False).to_dict()
        if len(wins)
        else {}
    )
    max_symbol_share = max(profit_by_symbol.values(), default=0.0) / gross_profit if gross_profit else None
    bootstrap = clustered_expectancy_bootstrap(trades)
    label = evidence_label(
        closed,
        expectancy,
        bootstrap["p05"],
        profit_factor,
        max_symbol_share,
    )
    themes = sorted({theme_map.get(symbol, "unknown") for symbol in trades["symbol"]})
    return {
        "scope": scope,
        "variant": variant,
        "evidence_label": label,
        "closed_trades": closed,
        "wins": int(len(wins)),
        "losses": int(len(losses)),
        "win_rate": win_rate,
        "win_rate_wilson_95_low": None if np.isnan(win_low) else float(win_low),
        "win_rate_wilson_95_high": None if np.isnan(win_high) else float(win_high),
        "average_win_return": average_win,
        "average_loss_return": average_loss,
        "payoff_ratio": payoff,
        "breakeven_win_rate": breakeven_win_rate,
        "win_rate_edge_vs_breakeven": (
            win_rate - breakeven_win_rate
            if win_rate is not None and breakeven_win_rate is not None
            else None
        ),
        "expectancy_per_trade": expectancy,
        "cumulative_net_pnl": float(trades["pnl"].sum()) if closed else 0.0,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "winning_symbols": int(len(profit_by_symbol)),
        "themes": themes,
        "theme_count": int(len(themes)),
        "max_symbol_profit_share": max_symbol_share,
        "profit_by_symbol": profit_by_symbol,
        "worst_trade_return": float(trades["return"].min()) if closed else None,
        "longest_loss_streak": longest_loss_streak(trades),
        "bootstrap": bootstrap,
        "research_only": True,
        "authorizes_trade": False,
    }


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def retrospective_calibration(theme_map: dict[str, str]) -> list[dict]:
    panels, all_symbols = BACKTEST["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    baseline_config, candidate_config = FORWARD["frozen_configs"]()
    start = "2024-01-02"
    end = str(panels["close"].index.max().date())
    baseline = BACKTEST["simulate"](
        panels, symbols, baseline_config, "strict_veto", start, end, slippage=0.001
    )
    rsr1 = BACKTEST["simulate"](
        panels, symbols, candidate_config, "strict_veto", start, end, slippage=0.001
    )
    rsr2 = BACKTEST["simulate"](
        panels,
        symbols,
        candidate_config,
        "strict_veto",
        start,
        end,
        slippage=0.001,
        profit_lock_trigger=FORWARD["PROFIT_LOCK_TRIGGER"],
        profit_lock_floor=FORWARD["PROFIT_LOCK_FLOOR"],
    )
    return [
        score_trades(pd.DataFrame(result["trades"]), theme_map, "retrospective_calibration", name)
        for name, result in (
            ("matched_baseline", baseline),
            ("RSR1-shadow", rsr1),
            ("RSR2-profit-lock-shadow", rsr2),
        )
    ]


def flatten_score(score: dict) -> dict:
    row = {key: value for key, value in score.items() if key not in {"bootstrap", "profit_by_symbol", "themes"}}
    row.update({f"bootstrap_{key}": value for key, value in score["bootstrap"].items()})
    row["themes"] = ";".join(score["themes"])
    row["profit_by_symbol"] = json.dumps(score["profit_by_symbol"], sort_keys=True)
    return row


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{float(value):.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{float(value):.2f}"


def write_report(summary: dict, scores: list[dict]) -> None:
    lines = [
        "# Forward expectancy scorecard",
        "",
        "## Current status",
        "",
        f"- Forward status: `{summary['forward_status']}`",
        f"- Completed data through: `{summary['as_of']}`",
        f"- Completed forward sessions: `{summary['sessions']}`",
        f"- Forward ledger hashes preserved: `{summary['input_ledgers_read_only']}`",
        "- This report is diagnostic-only and does not amend the original promotion gates.",
        "",
        "| Scope | Variant | Label | Trades | Win rate (Wilson 95%) | Payoff | Break-even win | Expectancy | PF | Bootstrap p05 / p95 | P(E<=0) | Top-symbol profit |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for score in scores:
        interval = (
            "n/a"
            if score["win_rate"] is None
            else f"{pct(score['win_rate'])} ({pct(score['win_rate_wilson_95_low'])}–{pct(score['win_rate_wilson_95_high'])})"
        )
        bootstrap = score["bootstrap"]
        bootstrap_interval = (
            "n/a"
            if bootstrap["p05"] is None
            else f"{pct(bootstrap['p05'])} / {pct(bootstrap['p95'])}"
        )
        lines.append(
            f"| {score['scope']} | {score['variant']} | {score['evidence_label']} | "
            f"{score['closed_trades']} | {interval} | {num(score['payoff_ratio'])} | "
            f"{pct(score['breakeven_win_rate'])} | {pct(score['expectancy_per_trade'])} | "
            f"{num(score['profit_factor'])} | {bootstrap_interval} | "
            f"{pct(bootstrap['probability_nonpositive'])} | {pct(score['max_symbol_profit_share'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Forward rows remain `awaiting_sample` until at least 20 trades close. Open or pending positions never enter the denominator.",
            "- The Wilson interval answers how uncertain the hit rate is; payoff and break-even win rate answer whether that hit rate is economically sufficient.",
            "- The cluster bootstrap keeps same-entry-date trades together. It remains descriptive because dates and regimes are not independent.",
            "- Retrospective calibration uses the hindsight-selected current list. It validates calculations and exposes uncertainty, but contributes zero forward evidence.",
            "",
            "Research-only. No order or strategy change is authorized.",
        ]
    )
    (RESULTS / "forward_expectancy_scorecard_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    status_path = RESULTS / "forward_shadow_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    theme_map = FORWARD["watchlist_theme_map"]()
    baseline = read_csv_if_exists(RESULTS / "forward_shadow_baseline_trades.csv")
    rsr1 = read_csv_if_exists(RESULTS / "forward_shadow_ledger.csv")
    rsr2 = read_csv_if_exists(RESULTS / "forward_profit_protection_ledger.csv")
    forward_scores = [
        score_trades(baseline, theme_map, "genuine_forward", "matched_baseline"),
        score_trades(rsr1, theme_map, "genuine_forward", "RSR1-shadow"),
        score_trades(rsr2, theme_map, "genuine_forward", "RSR2-profit-lock-shadow"),
    ]
    calibration = retrospective_calibration(theme_map)
    opportunity = read_csv_if_exists(RESULTS / "forward_opportunity_diagnostics_ledger.csv")
    opportunity_context = {
        "diagnostic_sessions": int(len(opportunity)),
        "realized_5d_leader_observations": int(
            pd.to_numeric(opportunity.get("realized_5d_leader_count", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()
        ),
        "high_vol_missed_leader_observations": int(
            pd.to_numeric(opportunity.get("high_vol_missed_leader_count", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()
        ),
        "core_one_month_reversals": int(
            opportunity.get("core_one_month_reversal", pd.Series(dtype=object)).fillna("").astype(str).str.len().gt(0).sum()
        ),
    }
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "forward_status": status.get("status"),
        "as_of": status.get("as_of"),
        "sessions": int(status.get("sessions", 0)),
        "research_only": True,
        "authorizes_trade": False,
        "changes_promotion_gate": False,
        "input_ledgers_read_only": True,
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "opportunity_context": opportunity_context,
        "forward_scores": forward_scores,
        "retrospective_calibration": calibration,
    }
    all_scores = forward_scores + calibration
    pd.DataFrame([flatten_score(score) for score in all_scores]).to_csv(
        RESULTS / "forward_expectancy_scorecard.csv", index=False
    )
    (RESULTS / "forward_expectancy_scorecard.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(summary, all_scores)
    print(
        json.dumps(
            {
                "forward_status": summary["forward_status"],
                "as_of": summary["as_of"],
                "sessions": summary["sessions"],
                "forward_closed_trades": {
                    score["variant"]: score["closed_trades"] for score in forward_scores
                },
                "historical_labels": {
                    score["variant"]: score["evidence_label"] for score in calibration
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
