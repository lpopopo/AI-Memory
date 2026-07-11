#!/usr/bin/env python3
from pathlib import Path

import pandas as pd

from backtest_dual_sleeve import RESULTS_DIR, fetch_close_prices, pct, run_buy_hold, summarize
from optimize_dual_sleeve import Config, prepare_indicators, run_config


BEST_V1 = Config(
    name="dual_sleeve_v1_best",
    value_mode="top2",
    tactical_top_n=2,
    regime="spy200_or_qqq100",
    tactical_filter="positive_m63",
    score_mode="m63_m126",
    fallback="qqq",
)

SPLITS = [
    ("full", "2016-05-31", "2026-05-28"),
    ("train_2016_2021", "2016-05-31", "2021-12-31"),
    ("test_2022_2026", "2022-01-01", "2026-05-28"),
    ("bear_2022", "2022-01-01", "2022-12-31"),
    ("post_2023_2026", "2023-01-01", "2026-05-28"),
]


def rebase_curve(curve):
    return curve / curve.iloc[0]


def slice_curve(curve, start, end):
    sliced = curve.loc[(curve.index >= pd.Timestamp(start)) & (curve.index <= pd.Timestamp(end))]
    if sliced.empty:
        raise RuntimeError(f"empty slice {start} to {end} for {curve.name}")
    return rebase_curve(sliced)


def compare_split(name, start, end, curves):
    rows = []
    for label, curve in curves.items():
        rows.append(summarize(label, slice_curve(curve, start, end)))
    return name, rows


def write_validation_summary(split_results):
    lines = [
        "# V1 Revalidation Summary",
        "",
        "This file revalidates the V1 best configuration after optimization.",
        "",
        "Fixed V1 configuration:",
        "",
        "- Value mode: `top2`",
        "- Tactical top N: `2`",
        "- Regime filter: `spy200_or_qqq100`",
        "- Tactical filter: `positive_m63`",
        "- Score mode: `m63_m126`",
        "- Fallback: `qqq`",
        "",
    ]

    for split_name, rows in split_results:
        lines.extend(
            [
                f"## {split_name}",
                "",
                "| Strategy | Final Value | CAGR | Max Drawdown | Volatility | Sharpe | Sortino | Win Rate |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in rows:
            lines.append(
                f"| {row['name']} | {row['final_value']:.3f} | {pct(row['cagr'])} | "
                f"{pct(row['max_drawdown'])} | {pct(row['volatility'])} | "
                f"{row['sharpe']:.2f} | {row['sortino']:.2f} | {pct(row['win_rate'])} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Read",
            "",
            "- Full-period reproduction should match the optimization summary except for tiny rounding differences.",
            "- The train/test split checks whether the optimized rule survives outside the period that visually dominated selection.",
            "- If V1 only looks good in one segment, treat it as a candidate that needs more robust validation.",
        ]
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "validation_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    v1_curve, _allocations = run_config(close, indicators, BEST_V1)
    v1_curve = v1_curve.rename("Dual Sleeve V1 Best")

    curves = {
        "Dual Sleeve V1 Best": v1_curve,
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }

    split_results = [compare_split(name, start, end, curves) for name, start, end in SPLITS]
    write_validation_summary(split_results)

    for split_name, rows in split_results:
        print(split_name)
        for row in rows:
            print(
                f"  {row['name']}: final={row['final_value']:.3f}, "
                f"CAGR={pct(row['cagr'])}, MDD={pct(row['max_drawdown'])}, Sharpe={row['sharpe']:.2f}"
            )


if __name__ == "__main__":
    main()
