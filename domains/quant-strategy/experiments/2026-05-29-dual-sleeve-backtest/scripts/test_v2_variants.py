#!/usr/bin/env python3
from dataclasses import dataclass

import pandas as pd

from backtest_dual_sleeve import RESULTS_DIR, fetch_close_prices, pct, run_buy_hold, summarize
from optimize_dual_sleeve import (
    Config,
    combine_weights,
    prepare_indicators,
    rank_symbols,
    tactical_weights,
    value_weights,
)
from validate_dual_sleeve import SPLITS, slice_curve


BASE_CONFIG = Config(
    name="base",
    value_mode="top2",
    tactical_top_n=2,
    regime="spy200_or_qqq100",
    tactical_filter="positive_m63",
    score_mode="m63_m126",
    fallback="qqq",
)


@dataclass(frozen=True)
class V2Config:
    name: str
    bull_value_weight: float
    bull_tactical_weight: float
    normal_value_weight: float
    normal_tactical_weight: float
    bull_rule: str
    tactical_top_n: int
    fallback: str
    include_qqq_in_bull_rank: bool


def month_end_dates(index):
    periods = index.to_period("M")
    return {dt for i, dt in enumerate(index) if i == len(index) - 1 or periods[i + 1] != periods[i]}


def is_bull(config, close, indicators, dt):
    qqq = close.at[dt, "QQQ"]
    spy = close.at[dt, "SPY"]
    qqq_ma100 = indicators["ma100"].at[dt, "QQQ"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    spy_ma200 = indicators["ma200"].at[dt, "SPY"]
    qqq_m63 = indicators["mom63"].at[dt, "QQQ"]
    qqq_m126 = indicators["mom126"].at[dt, "QQQ"]

    if config.bull_rule == "qqq100_m63":
        return pd.notna(qqq_ma100) and pd.notna(qqq_m63) and qqq > qqq_ma100 and qqq_m63 > 0
    if config.bull_rule == "qqq200_m126":
        return pd.notna(qqq_ma200) and pd.notna(qqq_m126) and qqq > qqq_ma200 and qqq_m126 > 0
    if config.bull_rule == "spy200_qqq100":
        return (
            pd.notna(spy_ma200)
            and pd.notna(qqq_ma100)
            and pd.notna(qqq_m63)
            and spy > spy_ma200
            and qqq > qqq_ma100
            and qqq_m63 > 0
        )
    raise ValueError(f"unknown bull rule: {config.bull_rule}")


def scale_weights(weights, target_total):
    total = sum(weights.values())
    if total <= 0:
        return {}
    return {symbol: weight / total * target_total for symbol, weight in weights.items()}


def v2_tactical_weights(config, close, indicators, dt, target_total, bull):
    temp = Config(
        name=config.name,
        value_mode=BASE_CONFIG.value_mode,
        tactical_top_n=config.tactical_top_n,
        regime=BASE_CONFIG.regime,
        tactical_filter=BASE_CONFIG.tactical_filter,
        score_mode=BASE_CONFIG.score_mode,
        fallback=config.fallback,
    )

    weights = tactical_weights(
        temp,
        close,
        indicators["ma50"],
        indicators["ma100"],
        indicators["ma200"],
        indicators["mom63"],
        indicators["mom126"],
        indicators["mom252"],
        dt,
    )

    if bull and config.include_qqq_in_bull_rank:
        candidates = list(dict.fromkeys(["QQQ"] + list(weights.keys())))
        ranked = rank_symbols(
            candidates,
            close,
            indicators["mom63"],
            indicators["mom126"],
            indicators["mom252"],
            dt,
            BASE_CONFIG.score_mode,
        )
        selected = [symbol for _, symbol in ranked[: config.tactical_top_n]]
        if selected:
            weights = {symbol: 1.0 / len(selected) for symbol in selected}

    return scale_weights(weights, target_total)


def run_v2(close, indicators, config):
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
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
            bull = is_bull(config, close, indicators, dt)
            value_target = config.bull_value_weight if bull else config.normal_value_weight
            tactical_target = config.bull_tactical_weight if bull else config.normal_tactical_weight

            v = value_weights(
                BASE_CONFIG,
                close,
                indicators["ma200"],
                indicators["mom63"],
                indicators["mom126"],
                indicators["mom252"],
                dt,
            )
            v = scale_weights(v, value_target)
            t = v2_tactical_weights(config, close, indicators, dt, tactical_target, bull)
            weights = combine_weights(v, t)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "bull": bull,
                    "value": "|".join(sorted(v)),
                    "tactical": "|".join(sorted(t)),
                    "cash": max(0.0, 1.0 - sum(weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def candidate_configs():
    idx = 1
    for bull_value, top_n, bull_rule, fallback, include_qqq in [
        (0.35, 2, "qqq100_m63", "qqq", True),
        (0.30, 2, "qqq100_m63", "qqq", True),
        (0.25, 2, "qqq100_m63", "qqq", True),
        (0.35, 3, "qqq100_m63", "qqq", True),
        (0.35, 2, "qqq200_m126", "qqq", True),
        (0.35, 2, "spy200_qqq100", "qqq", True),
        (0.35, 2, "qqq100_m63", "spy_qqq", True),
        (0.35, 2, "qqq100_m63", "qqq", False),
        (0.40, 2, "qqq100_m63", "qqq", True),
    ]:
        yield V2Config(
            name=f"dual_sleeve_v2_{idx:02d}",
            bull_value_weight=bull_value,
            bull_tactical_weight=1.0 - bull_value,
            normal_value_weight=0.5,
            normal_tactical_weight=0.5,
            bull_rule=bull_rule,
            tactical_top_n=top_n,
            fallback=fallback,
            include_qqq_in_bull_rank=include_qqq,
        )
        idx += 1


def split_summary(curve, label):
    rows = {}
    for split_name, start, end in SPLITS:
        rows[split_name] = summarize(label, slice_curve(curve, start, end))
    return rows


def candidate_score(full, test, train, bear):
    return (
        full["sharpe"]
        + test["sharpe"] * 0.8
        + full["cagr"]
        + test["cagr"]
        + bear["max_drawdown"] * 0.6
        + min(0.0, train["cagr"] - 0.20)
    )


def write_v2_summary(close, results, best_config, best_curve, benchmark_curves):
    lines = [
        "# V2 Variant Summary",
        "",
        "V2 tests bull-market participation upgrades on top of V1.",
        "",
        "## Best Candidate",
        "",
        f"- Name: `{best_config.name}`",
        f"- Bull value weight: `{best_config.bull_value_weight:.0%}`",
        f"- Bull tactical/growth weight: `{best_config.bull_tactical_weight:.0%}`",
        f"- Normal value weight: `{best_config.normal_value_weight:.0%}`",
        f"- Normal tactical weight: `{best_config.normal_tactical_weight:.0%}`",
        f"- Bull rule: `{best_config.bull_rule}`",
        f"- Tactical top N: `{best_config.tactical_top_n}`",
        f"- Fallback: `{best_config.fallback}`",
        f"- Include QQQ in bull rank: `{best_config.include_qqq_in_bull_rank}`",
        "",
        "## Full-Period Comparison",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    comparison_curves = {"Dual Sleeve V2 Best": best_curve, **benchmark_curves}
    for label, curve in comparison_curves.items():
        row = summarize(label, curve)
        lines.append(
            f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | "
            f"{pct(row['max_drawdown'])} | {pct(row['volatility'])} | "
            f"{row['sharpe']:.2f} | {row['sortino']:.2f} | {pct(row['win_rate'])} |"
        )

    lines.extend(
        [
            "",
            "## Top Candidates",
            "",
            "| Rank | Name | Full CAGR | Full DD | Full Sharpe | Test CAGR | Test DD | Test Sharpe | Train CAGR | Bear 2022 | Config |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for rank, item in enumerate(results[:9], start=1):
        cfg = item["config"]
        full = item["splits"]["full"]
        test = item["splits"]["test_2022_2026"]
        train = item["splits"]["train_2016_2021"]
        bear = item["splits"]["bear_2022"]
        cfg_text = (
            f"bull {cfg.bull_value_weight:.0%}/{cfg.bull_tactical_weight:.0%}, "
            f"{cfg.bull_rule}, top{cfg.tactical_top_n}, {cfg.fallback}, qqq_rank={cfg.include_qqq_in_bull_rank}"
        )
        lines.append(
            f"| {rank} | {cfg.name} | {pct(full['cagr'])} | {pct(full['max_drawdown'])} | {full['sharpe']:.2f} | "
            f"{pct(test['cagr'])} | {pct(test['max_drawdown'])} | {test['sharpe']:.2f} | "
            f"{pct(train['cagr'])} | {pct(bear['cagr'])} | {cfg_text} |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- V2 is still an ETF-proxy strategy, not the final individual-stock version.",
            "- The goal is to improve bull-market participation while watching whether 2022 protection degrades.",
            "- If V2 mostly becomes QQQ exposure, compare it skeptically against 50/50 SPY/QQQ and QQQ.",
        ]
    )
    (RESULTS_DIR / "v2_variant_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    benchmark_curves = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }

    results = []
    for config in candidate_configs():
        curve, allocations = run_v2(close, indicators, config)
        splits = split_summary(curve, config.name)
        score = candidate_score(
            splits["full"],
            splits["test_2022_2026"],
            splits["train_2016_2021"],
            splits["bear_2022"],
        )
        results.append({"config": config, "curve": curve, "allocations": allocations, "splits": splits, "score": score})

    results.sort(key=lambda item: item["score"], reverse=True)
    best = results[0]
    best["allocations"].to_csv(RESULTS_DIR / "v2_best_monthly_allocations.csv", index=False)
    best["curve"].to_csv(RESULTS_DIR / "v2_best_equity_curve.csv", index_label="date")
    write_v2_summary(close, results, best["config"], best["curve"], benchmark_curves)

    full = best["splits"]["full"]
    test = best["splits"]["test_2022_2026"]
    bear = best["splits"]["bear_2022"]
    print(
        f"best={best['config'].name} full CAGR={pct(full['cagr'])} "
        f"MDD={pct(full['max_drawdown'])} Sharpe={full['sharpe']:.2f}"
    )
    print(f"test CAGR={pct(test['cagr'])} MDD={pct(test['max_drawdown'])} Sharpe={test['sharpe']:.2f}")
    print(f"bear 2022 CAGR={pct(bear['cagr'])} MDD={pct(bear['max_drawdown'])} Sharpe={bear['sharpe']:.2f}")


if __name__ == "__main__":
    main()
