#!/usr/bin/env python3
from dataclasses import asdict

import pandas as pd

from backtest_dual_sleeve import RESULTS_DIR, fetch_close_prices, pct, run_buy_hold, summarize
from optimize_dual_sleeve import prepare_indicators
from test_v2_variants import V2Config, run_v2
from validate_dual_sleeve import SPLITS, slice_curve


BEST_V2 = V2Config(
    name="dual_sleeve_v2_best",
    bull_value_weight=0.35,
    bull_tactical_weight=0.65,
    normal_value_weight=0.50,
    normal_tactical_weight=0.50,
    bull_rule="qqq200_m126",
    tactical_top_n=2,
    fallback="qqq",
    include_qqq_in_bull_rank=True,
)


def rolling_windows(index, years=3):
    start_year = index[0].year
    end_year = index[-1].year
    windows = []
    for year in range(start_year, end_year - years + 2):
        start = pd.Timestamp(f"{year}-01-01")
        end = pd.Timestamp(f"{year + years - 1}-12-31")
        if end < index[0] or start > index[-1]:
            continue
        actual = index[(index >= start) & (index <= end)]
        if len(actual) > 500:
            windows.append((f"{year}-{year + years - 1}", actual[0], actual[-1]))
    return windows


def compare(curves, start, end):
    rows = {}
    for label, curve in curves.items():
        rows[label] = summarize(label, slice_curve(curve, start, end))
    return rows


def outcome_against(rows, benchmark="50/50 SPY/QQQ"):
    v2 = rows["Dual Sleeve V2 Best"]
    base = rows[benchmark]
    return {
        "cagr_delta": v2["cagr"] - base["cagr"],
        "drawdown_delta": v2["max_drawdown"] - base["max_drawdown"],
        "sharpe_delta": v2["sharpe"] - base["sharpe"],
        "beats_cagr": v2["cagr"] > base["cagr"],
        "beats_drawdown": v2["max_drawdown"] > base["max_drawdown"],
        "beats_sharpe": v2["sharpe"] > base["sharpe"],
    }


def write_summary(split_results, rolling_results):
    lines = [
        "# V2 Robustness Validation",
        "",
        "This validation fixes the best V2 configuration and tests it across fixed periods and rolling 3-year windows.",
        "",
        "## Fixed V2 Configuration",
        "",
    ]
    for key, value in asdict(BEST_V2).items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(["", "## Fixed Split Results", ""])
    for split_name, rows in split_results:
        lines.extend(
            [
                f"### {split_name}",
                "",
                "| Strategy | Final Value | CAGR | Max Drawdown | Sharpe |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for label, row in rows.items():
            lines.append(
                f"| {label} | {row['final_value']:.3f} | {pct(row['cagr'])} | "
                f"{pct(row['max_drawdown'])} | {row['sharpe']:.2f} |"
            )
        delta = outcome_against(rows)
        lines.extend(
            [
                "",
                f"Against 50/50 SPY/QQQ: CAGR delta {pct(delta['cagr_delta'])}, "
                f"drawdown delta {pct(delta['drawdown_delta'])}, Sharpe delta {delta['sharpe_delta']:.2f}.",
                "",
            ]
        )

    lines.extend(
        [
            "## Rolling 3-Year Windows",
            "",
            "| Window | V2 CAGR | 50/50 CAGR | CAGR Delta | V2 DD | 50/50 DD | DD Delta | V2 Sharpe | 50/50 Sharpe | Sharpe Delta |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    wins = {"cagr": 0, "drawdown": 0, "sharpe": 0}
    for window, rows, delta in rolling_results:
        v2 = rows["Dual Sleeve V2 Best"]
        base = rows["50/50 SPY/QQQ"]
        wins["cagr"] += int(delta["beats_cagr"])
        wins["drawdown"] += int(delta["beats_drawdown"])
        wins["sharpe"] += int(delta["beats_sharpe"])
        lines.append(
            f"| {window} | {pct(v2['cagr'])} | {pct(base['cagr'])} | {pct(delta['cagr_delta'])} | "
            f"{pct(v2['max_drawdown'])} | {pct(base['max_drawdown'])} | {pct(delta['drawdown_delta'])} | "
            f"{v2['sharpe']:.2f} | {base['sharpe']:.2f} | {delta['sharpe_delta']:.2f} |"
        )

    total = len(rolling_results)
    lines.extend(
        [
            "",
            "## Rolling Win Counts Versus 50/50 SPY/QQQ",
            "",
            f"- CAGR wins: {wins['cagr']} / {total}",
            f"- Drawdown wins: {wins['drawdown']} / {total}",
            f"- Sharpe wins: {wins['sharpe']} / {total}",
            "",
            "## Read",
            "",
            "- Positive drawdown delta means V2 had a shallower drawdown.",
            "- This is still ETF-proxy validation; individual-stock sleeves remain untested.",
            "- A robust strategy should not depend on only one rolling window.",
        ]
    )

    if wins["cagr"] < total or wins["drawdown"] < total:
        lines.extend(
            [
                "",
                "## Initial Interpretation",
                "",
                "- V2 should be treated as improved but not fully proven.",
                "- The key question is whether its rolling-window behavior is consistent enough to justify moving to individual-stock testing.",
            ]
        )

    (RESULTS_DIR / "v2_robustness_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    v2_curve, _allocations = run_v2(close, indicators, BEST_V2)
    v2_curve = v2_curve.rename("Dual Sleeve V2 Best")

    curves = {
        "Dual Sleeve V2 Best": v2_curve,
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }

    split_results = []
    for split_name, start, end in SPLITS:
        rows = compare(curves, start, end)
        split_results.append((split_name, rows))

    rolling_results = []
    for window, start, end in rolling_windows(close.index, years=3):
        rows = compare(curves, start, end)
        rolling_results.append((window, rows, outcome_against(rows)))

    write_summary(split_results, rolling_results)

    print("Fixed split validation:")
    for split_name, rows in split_results:
        delta = outcome_against(rows)
        print(
            f"{split_name}: CAGR delta={pct(delta['cagr_delta'])}, "
            f"DD delta={pct(delta['drawdown_delta'])}, Sharpe delta={delta['sharpe_delta']:.2f}"
        )
    print("Rolling windows:")
    for window, _rows, delta in rolling_results:
        print(
            f"{window}: CAGR delta={pct(delta['cagr_delta'])}, "
            f"DD delta={pct(delta['drawdown_delta'])}, Sharpe delta={delta['sharpe_delta']:.2f}"
        )


if __name__ == "__main__":
    main()
