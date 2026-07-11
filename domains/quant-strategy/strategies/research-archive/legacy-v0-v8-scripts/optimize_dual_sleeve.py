#!/usr/bin/env python3
import csv
import itertools
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from backtest_dual_sleeve import (
    RESULTS_DIR,
    TACTICAL_ETFS,
    VALUE_ETFS,
    fetch_close_prices,
    pct,
    run_buy_hold,
    summarize,
)


TRADING_DAYS = 252


@dataclass(frozen=True)
class Config:
    name: str
    value_mode: str
    tactical_top_n: int
    regime: str
    tactical_filter: str
    score_mode: str
    fallback: str


def month_end_dates(index):
    periods = index.to_period("M")
    return {dt for i, dt in enumerate(index) if i == len(index) - 1 or periods[i + 1] != periods[i]}


def combine_weights(*groups):
    weights = {}
    for group in groups:
        for symbol, weight in group.items():
            weights[symbol] = weights.get(symbol, 0.0) + weight
    return weights


def rank_symbols(symbols, close, mom63, mom126, mom252, dt, score_mode):
    ranked = []
    for symbol in symbols:
        if symbol not in close.columns or pd.isna(close.at[dt, symbol]):
            continue
        m63 = mom63.at[dt, symbol] if symbol in mom63.columns else None
        m126 = mom126.at[dt, symbol] if symbol in mom126.columns else None
        m252 = mom252.at[dt, symbol] if symbol in mom252.columns else None

        if score_mode == "m63_m126" and m63 is not None and m126 is not None:
            score = m63 + m126
        elif score_mode == "m126_m252" and m126 is not None and m252 is not None:
            score = m126 + m252
        elif score_mode == "m63_m126_m252" and m63 is not None and m126 is not None and m252 is not None:
            score = m63 + m126 + m252
        else:
            continue
        ranked.append((score, symbol))

    ranked.sort(reverse=True)
    return ranked


def value_weights(config, close, ma200, mom63, mom126, mom252, dt):
    available = [s for s in VALUE_ETFS if s in close.columns and pd.notna(close.at[dt, s])]
    if not available:
        return {}

    if config.value_mode == "equal":
        selected = available
    else:
        ranked = rank_symbols(available, close, mom63, mom126, mom252, dt, config.score_mode)
        if config.value_mode == "top1":
            selected = [s for _, s in ranked[:1]]
        elif config.value_mode == "top2":
            selected = [s for _, s in ranked[:2]]
        else:
            selected = [s for _, s in ranked[:3]]

        selected = [
            s
            for s in selected
            if s in ma200.columns and pd.notna(ma200.at[dt, s]) and close.at[dt, s] > ma200.at[dt, s]
        ]
        if not selected:
            selected = available

    weight = 0.5 / len(selected)
    return {s: weight for s in selected}


def regime_allows(config, close, ma100, ma200, dt):
    spy_ok = pd.notna(ma200.at[dt, "SPY"]) and close.at[dt, "SPY"] > ma200.at[dt, "SPY"]
    qqq_ok = pd.notna(ma100.at[dt, "QQQ"]) and close.at[dt, "QQQ"] > ma100.at[dt, "QQQ"]

    if config.regime == "none":
        return True
    if config.regime == "spy200":
        return spy_ok
    if config.regime == "spy200_or_qqq100":
        return spy_ok or qqq_ok
    if config.regime == "spy200_and_qqq100":
        return spy_ok and qqq_ok
    raise ValueError(f"unknown regime: {config.regime}")


def tactical_weights(config, close, ma50, ma100, ma200, mom63, mom126, mom252, dt):
    if not regime_allows(config, close, ma100, ma200, dt):
        return fallback_weights(config)

    ranked = []
    for score, symbol in rank_symbols(TACTICAL_ETFS, close, mom63, mom126, mom252, dt, config.score_mode):
        if config.tactical_filter == "ma50":
            if symbol not in ma50.columns or pd.isna(ma50.at[dt, symbol]) or close.at[dt, symbol] <= ma50.at[dt, symbol]:
                continue
        if config.tactical_filter == "positive_m63":
            if pd.isna(mom63.at[dt, symbol]) or mom63.at[dt, symbol] <= 0:
                continue
        if config.tactical_filter == "ma50_positive_m63":
            if symbol not in ma50.columns or pd.isna(ma50.at[dt, symbol]) or close.at[dt, symbol] <= ma50.at[dt, symbol]:
                continue
            if pd.isna(mom63.at[dt, symbol]) or mom63.at[dt, symbol] <= 0:
                continue
        ranked.append((score, symbol))

    selected = [s for _, s in ranked[: config.tactical_top_n]]
    if not selected:
        return fallback_weights(config)
    weight = 0.5 / len(selected)
    return {s: weight for s in selected}


def fallback_weights(config):
    if config.fallback == "cash":
        return {}
    if config.fallback == "spy":
        return {"SPY": 0.5}
    if config.fallback == "qqq":
        return {"QQQ": 0.5}
    if config.fallback == "spy_qqq":
        return {"SPY": 0.25, "QQQ": 0.25}
    raise ValueError(f"unknown fallback: {config.fallback}")


def prepare_indicators(close):
    return {
        "returns": close.pct_change(fill_method=None).fillna(0.0),
        "ma50": close.rolling(50).mean(),
        "ma100": close.rolling(100).mean(),
        "ma200": close.rolling(200).mean(),
        "mom63": close / close.shift(63) - 1.0,
        "mom126": close / close.shift(126) - 1.0,
        "mom252": close / close.shift(252) - 1.0,
        "rebalance_dates": month_end_dates(close.index),
    }


def run_config(close, indicators, config):
    returns = indicators["returns"]
    ma50 = indicators["ma50"]
    ma100 = indicators["ma100"]
    ma200 = indicators["ma200"]
    mom63 = indicators["mom63"]
    mom126 = indicators["mom126"]
    mom252 = indicators["mom252"]
    rebalance_dates = indicators["rebalance_dates"]

    equity = []
    allocations = []
    weights = {}
    value = 1.0

    for dt in close.index:
        day_return = 0.0
        for symbol, weight in weights.items():
            if symbol in returns.columns and pd.notna(returns.at[dt, symbol]):
                day_return += weight * returns.at[dt, symbol]
        value *= 1.0 + day_return
        equity.append(value)

        if dt in rebalance_dates:
            v = value_weights(config, close, ma200, mom63, mom126, mom252, dt)
            t = tactical_weights(config, close, ma50, ma100, ma200, mom63, mom126, mom252, dt)
            weights = combine_weights(v, t)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "value": "|".join(sorted(v)),
                    "tactical": "|".join(sorted(t)),
                    "cash": max(0.0, 1.0 - sum(weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def config_grid():
    idx = 1
    for value_mode, top_n, regime, tactical_filter, score_mode, fallback in itertools.product(
        ["equal", "top2"],
        [2, 3],
        ["none", "spy200_or_qqq100"],
        ["positive_m63", "ma50_positive_m63"],
        ["m63_m126"],
        ["cash", "qqq", "spy_qqq"],
    ):
        yield Config(
            name=f"v1_{idx:04d}",
            value_mode=value_mode,
            tactical_top_n=top_n,
            regime=regime,
            tactical_filter=tactical_filter,
            score_mode=score_mode,
            fallback=fallback,
        )
        idx += 1


def composite_score(summary):
    # Prefer risk-adjusted return, but penalize severe drawdown.
    return summary["sharpe"] + summary["cagr"] * 2.0 + summary["max_drawdown"]


def write_optimization_summary(close, rows, best_curve, best_allocations, best_config):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: r["composite_score"], reverse=True)

    with (RESULTS_DIR / "optimization_grid.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    best_curve.to_csv(RESULTS_DIR / "v1_best_equity_curve.csv", index_label="date")
    best_allocations.to_csv(RESULTS_DIR / "v1_best_monthly_allocations.csv", index=False)

    benchmark_curves = [
        run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    ]
    comparison = [summarize("Dual Sleeve V1 Best", best_curve)]
    comparison.extend(summarize(curve.name, curve) for curve in benchmark_curves)

    lines = [
        "# V1 Optimization Summary",
        "",
        f"Period: {close.index[0].strftime('%Y-%m-%d')} to {close.index[-1].strftime('%Y-%m-%d')}",
        "",
        "## Best Configuration",
        "",
        f"- Value mode: `{best_config.value_mode}`",
        f"- Tactical top N: `{best_config.tactical_top_n}`",
        f"- Regime filter: `{best_config.regime}`",
        f"- Tactical filter: `{best_config.tactical_filter}`",
        f"- Score mode: `{best_config.score_mode}`",
        f"- Fallback: `{best_config.fallback}`",
        "",
        "## Comparison",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in comparison:
        lines.append(
            f"| {row['name']} | {row['final_value']:.3f} | {pct(row['cagr'])} | "
            f"{pct(row['max_drawdown'])} | {pct(row['volatility'])} | "
            f"{row['sharpe']:.2f} | {row['sortino']:.2f} | {pct(row['win_rate'])} |"
        )

    lines.extend(
        [
            "",
            "## Top 10 Configurations By Composite Score",
            "",
            "| Rank | Config | Final | CAGR | Max DD | Sharpe | Value | Top N | Regime | Filter | Score | Fallback |",
            "| ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for rank, row in enumerate(rows[:10], start=1):
        lines.append(
            f"| {rank} | {row['name']} | {row['final_value']:.3f} | {pct(row['cagr'])} | "
            f"{pct(row['max_drawdown'])} | {row['sharpe']:.2f} | {row['value_mode']} | "
            f"{row['tactical_top_n']} | {row['regime']} | {row['tactical_filter']} | "
            f"{row['score_mode']} | {row['fallback']} |"
        )

    lines.extend(
        [
            "",
            "## Caution",
            "",
            "- This is an in-sample parameter scan on the same 10-year period.",
            "- Treat the best configuration as a candidate, not proof.",
            "- V2 should use walk-forward or train/test validation before accepting parameter changes.",
        ]
    )
    (RESULTS_DIR / "optimization_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    rows = []
    best = None

    for config in config_grid():
        curve, allocations = run_config(close, indicators, config)
        summary = summarize(config.name, curve)
        row = {
            **summary,
            "value_mode": config.value_mode,
            "tactical_top_n": config.tactical_top_n,
            "regime": config.regime,
            "tactical_filter": config.tactical_filter,
            "score_mode": config.score_mode,
            "fallback": config.fallback,
            "composite_score": composite_score(summary),
        }
        rows.append(row)
        if best is None or row["composite_score"] > best[0]["composite_score"]:
            best = (row, config, curve, allocations)

    best_row, best_config, best_curve, best_allocations = best
    write_optimization_summary(close, rows, best_curve, best_allocations, best_config)
    print(
        f"best={best_row['name']} final={best_row['final_value']:.3f} "
        f"CAGR={pct(best_row['cagr'])} MDD={pct(best_row['max_drawdown'])} "
        f"Sharpe={best_row['sharpe']:.2f}"
    )
    print(best_config)


if __name__ == "__main__":
    main()
