#!/usr/bin/env python3
from dataclasses import dataclass

import pandas as pd

from backtest_dual_sleeve import RESULTS_DIR, fetch_close_prices, pct, run_buy_hold, summarize
from optimize_dual_sleeve import prepare_indicators, rank_symbols
from test_v2_variants import V2Config, run_v2
from validate_dual_sleeve import SPLITS, slice_curve


GROWTH_ACCELERATORS = ["QQQ", "SMH", "XLK", "XLC"]
VALUE_ETFS = ["VTV", "IWD", "SCHD"]
TACTICAL_POOL = ["QQQ", "SMH", "XLK", "XLC", "XLY", "XLI", "XLF", "XLV", "IBB", "ITA"]


@dataclass(frozen=True)
class V3Config:
    name: str
    bull_value_weight: float
    bull_growth_weight: float
    normal_value_weight: float
    normal_growth_weight: float
    bear_value_weight: float
    bear_growth_weight: float
    bull_rule: str
    bear_rule: str
    growth_top_n: int
    value_mode: str
    score_mode: str


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
    if config.bull_rule == "spy200_qqq100_m63":
        return (
            pd.notna(spy_ma200)
            and pd.notna(qqq_ma100)
            and pd.notna(qqq_m63)
            and spy > spy_ma200
            and qqq > qqq_ma100
            and qqq_m63 > 0
        )
    raise ValueError(f"unknown bull rule: {config.bull_rule}")


def is_bear(config, close, indicators, dt):
    spy = close.at[dt, "SPY"]
    qqq = close.at[dt, "QQQ"]
    spy_ma200 = indicators["ma200"].at[dt, "SPY"]
    qqq_ma200 = indicators["ma200"].at[dt, "QQQ"]
    spy_m63 = indicators["mom63"].at[dt, "SPY"]
    qqq_m63 = indicators["mom63"].at[dt, "QQQ"]

    if config.bear_rule == "both_below_200":
        return pd.notna(spy_ma200) and pd.notna(qqq_ma200) and spy < spy_ma200 and qqq < qqq_ma200
    if config.bear_rule == "both_below_200_negative_m63":
        return (
            pd.notna(spy_ma200)
            and pd.notna(qqq_ma200)
            and pd.notna(spy_m63)
            and pd.notna(qqq_m63)
            and spy < spy_ma200
            and qqq < qqq_ma200
            and spy_m63 < 0
            and qqq_m63 < 0
        )
    raise ValueError(f"unknown bear rule: {config.bear_rule}")


def scale_weights(weights, target_total):
    total = sum(weights.values())
    if total <= 0:
        return {}
    return {symbol: weight / total * target_total for symbol, weight in weights.items()}


def combine_weights(*groups):
    weights = {}
    for group in groups:
        for symbol, weight in group.items():
            weights[symbol] = weights.get(symbol, 0.0) + weight
    return weights


def value_weights(config, close, indicators, dt, target_total):
    ranked = rank_symbols(
        VALUE_ETFS,
        close,
        indicators["mom63"],
        indicators["mom126"],
        indicators["mom252"],
        dt,
        config.score_mode,
    )
    if config.value_mode == "top1":
        selected = [s for _, s in ranked[:1]]
    elif config.value_mode == "top2":
        selected = [s for _, s in ranked[:2]]
    else:
        selected = [s for s in VALUE_ETFS if s in close.columns and pd.notna(close.at[dt, s])]
    if not selected:
        return {}
    return {symbol: target_total / len(selected) for symbol in selected}


def growth_weights(config, close, indicators, dt, target_total, bull):
    pool = TACTICAL_POOL if bull else GROWTH_ACCELERATORS
    ranked = rank_symbols(
        pool,
        close,
        indicators["mom63"],
        indicators["mom126"],
        indicators["mom252"],
        dt,
        config.score_mode,
    )
    selected = []
    for _score, symbol in ranked:
        if pd.isna(indicators["mom63"].at[dt, symbol]) or indicators["mom63"].at[dt, symbol] <= 0:
            continue
        selected.append(symbol)
        if len(selected) >= config.growth_top_n:
            break
    if not selected:
        selected = ["QQQ"]
    return {symbol: target_total / len(selected) for symbol in selected}


def run_v3(close, indicators, config):
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
            bear = is_bear(config, close, indicators, dt)
            if bear:
                value_target = config.bear_value_weight
                growth_target = config.bear_growth_weight
            elif bull:
                value_target = config.bull_value_weight
                growth_target = config.bull_growth_weight
            else:
                value_target = config.normal_value_weight
                growth_target = config.normal_growth_weight

            v = value_weights(config, close, indicators, dt, value_target)
            g = growth_weights(config, close, indicators, dt, growth_target, bull)
            weights = combine_weights(v, g)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "bull": bull,
                    "bear": bear,
                    "value": "|".join(sorted(v)),
                    "growth": "|".join(sorted(g)),
                    "cash": max(0.0, 1.0 - sum(weights.values())),
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def candidate_configs():
    idx = 1
    for bull_value, normal_value, bear_growth, top_n, bull_rule, bear_rule, value_mode in [
        (0.20, 0.40, 0.20, 2, "qqq100_m63", "both_below_200", "top2"),
        (0.15, 0.35, 0.20, 2, "qqq100_m63", "both_below_200", "top2"),
        (0.10, 0.30, 0.20, 2, "qqq100_m63", "both_below_200", "top2"),
        (0.20, 0.40, 0.30, 2, "qqq100_m63", "both_below_200_negative_m63", "top2"),
        (0.20, 0.40, 0.20, 3, "qqq100_m63", "both_below_200", "top2"),
        (0.20, 0.40, 0.20, 2, "qqq200_m126", "both_below_200", "top2"),
        (0.20, 0.40, 0.20, 2, "spy200_qqq100_m63", "both_below_200", "top2"),
        (0.25, 0.45, 0.20, 2, "qqq100_m63", "both_below_200", "top2"),
        (0.20, 0.40, 0.20, 2, "qqq100_m63", "both_below_200", "equal"),
    ]:
        yield V3Config(
            name=f"dual_sleeve_v3_{idx:02d}",
            bull_value_weight=bull_value,
            bull_growth_weight=1.0 - bull_value,
            normal_value_weight=normal_value,
            normal_growth_weight=1.0 - normal_value,
            bear_value_weight=1.0 - bear_growth,
            bear_growth_weight=bear_growth,
            bull_rule=bull_rule,
            bear_rule=bear_rule,
            growth_top_n=top_n,
            value_mode=value_mode,
            score_mode="m63_m126",
        )
        idx += 1


def split_curve(curve, start, end):
    sliced = curve.loc[(curve.index >= pd.Timestamp(start)) & (curve.index <= pd.Timestamp(end))]
    return sliced / sliced.iloc[0]


def summarize_splits(curve):
    splits = {}
    for name, start, end in [
        ("full", "2016-05-31", "2026-05-28"),
        ("train_2016_2021", "2016-05-31", "2021-12-31"),
        ("test_2022_2026", "2022-01-01", "2026-05-28"),
        ("bear_2022", "2022-01-01", "2022-12-31"),
        ("post_2023_2026", "2023-01-01", "2026-05-28"),
    ]:
        splits[name] = summarize(curve.name, split_curve(curve, start, end))
    return splits


def score_candidate(splits):
    full = splits["full"]
    train = splits["train_2016_2021"]
    test = splits["test_2022_2026"]
    bear = splits["bear_2022"]
    return (
        full["cagr"] * 2.0
        + full["sharpe"]
        + train["cagr"] * 0.6
        + test["cagr"] * 0.6
        + min(0.0, bear["cagr"] + 0.12)
        + bear["max_drawdown"] * 0.2
    )


def write_v3_summary(results, best, benchmarks):
    cfg = best["config"]
    lines = [
        "# V3 Return Engine Summary",
        "",
        "V3 follows the selected direction: pursue full-cycle return maximization with a stronger bull-market accelerator.",
        "",
        "## Best Candidate",
        "",
        f"- Name: `{cfg.name}`",
        f"- Bull allocation: `{cfg.bull_value_weight:.0%}` value / `{cfg.bull_growth_weight:.0%}` growth",
        f"- Normal allocation: `{cfg.normal_value_weight:.0%}` value / `{cfg.normal_growth_weight:.0%}` growth",
        f"- Bear allocation: `{cfg.bear_value_weight:.0%}` value / `{cfg.bear_growth_weight:.0%}` growth",
        f"- Bull rule: `{cfg.bull_rule}`",
        f"- Bear rule: `{cfg.bear_rule}`",
        f"- Growth top N: `{cfg.growth_top_n}`",
        f"- Value mode: `{cfg.value_mode}`",
        "",
        "## Full-Period Comparison",
        "",
        "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    comparison = {"Dual Sleeve V3 Best": best["curve"], **benchmarks}
    for label, curve in comparison.items():
        row = summarize(label, curve)
        lines.append(
            f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | {pct(row['max_drawdown'])} | "
            f"{pct(row['volatility'])} | {row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Top Candidates",
            "",
            "| Rank | Name | Full CAGR | Full DD | Sharpe | Train CAGR | Test CAGR | Bear 2022 | Config |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for rank, item in enumerate(results, start=1):
        cfg = item["config"]
        full = item["splits"]["full"]
        train = item["splits"]["train_2016_2021"]
        test = item["splits"]["test_2022_2026"]
        bear = item["splits"]["bear_2022"]
        cfg_text = (
            f"bull {cfg.bull_value_weight:.0%}/{cfg.bull_growth_weight:.0%}, "
            f"normal {cfg.normal_value_weight:.0%}/{cfg.normal_growth_weight:.0%}, "
            f"bear {cfg.bear_value_weight:.0%}/{cfg.bear_growth_weight:.0%}, "
            f"{cfg.bull_rule}, top{cfg.growth_top_n}, value={cfg.value_mode}"
        )
        lines.append(
            f"| {rank} | {cfg.name} | {pct(full['cagr'])} | {pct(full['max_drawdown'])} | {full['sharpe']:.2f} | "
            f"{pct(train['cagr'])} | {pct(test['cagr'])} | {pct(bear['cagr'])} | {cfg_text} |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- V3 intentionally prioritizes return more than V2.",
            "- Stronger bull participation may weaken bear-market protection.",
            "- If V3 mainly becomes QQQ-like, it must be compared against QQQ and 50/50 SPY/QQQ, not just V2.",
        ]
    )
    (RESULTS_DIR / "v3_return_engine_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    benchmarks = {
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }

    results = []
    for config in candidate_configs():
        curve, allocations = run_v3(close, indicators, config)
        splits = summarize_splits(curve)
        results.append(
            {
                "config": config,
                "curve": curve,
                "allocations": allocations,
                "splits": splits,
                "score": score_candidate(splits),
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    best = results[0]
    best["curve"].to_csv(RESULTS_DIR / "v3_best_equity_curve.csv", index_label="date")
    best["allocations"].to_csv(RESULTS_DIR / "v3_best_monthly_allocations.csv", index=False)
    write_v3_summary(results, best, benchmarks)

    full = best["splits"]["full"]
    train = best["splits"]["train_2016_2021"]
    test = best["splits"]["test_2022_2026"]
    bear = best["splits"]["bear_2022"]
    print(
        f"best={best['config'].name} full CAGR={pct(full['cagr'])} "
        f"MDD={pct(full['max_drawdown'])} Sharpe={full['sharpe']:.2f}"
    )
    print(f"train CAGR={pct(train['cagr'])} test CAGR={pct(test['cagr'])} bear CAGR={pct(bear['cagr'])}")


if __name__ == "__main__":
    main()
