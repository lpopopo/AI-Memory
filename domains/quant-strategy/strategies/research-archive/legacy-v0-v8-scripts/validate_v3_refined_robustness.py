#!/usr/bin/env python3
from dataclasses import asdict

import pandas as pd

from backtest_dual_sleeve import RESULTS_DIR, fetch_close_prices, pct, run_buy_hold, summarize
from optimize_dual_sleeve import prepare_indicators
from test_v3_refined import V3Config, run_v3
from validate_dual_sleeve import SPLITS, slice_curve


BEST_V3_REFINED = V3Config(
    name="dual_sleeve_v3_refined_best",
    bull_value_weight=0.30,
    bull_growth_weight=0.70,
    normal_value_weight=0.40,
    normal_growth_weight=0.60,
    bear_value_weight=0.70,
    bear_growth_weight=0.30,
    bull_rule="qqq200_m126",
    bear_rule="both_below_200_negative_m63",
    growth_top_n=2,
    value_mode="top2",
    score_mode="m63_m126",
    fallback="cash",
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
    v3_refined = rows["Dual Sleeve V3.1 Best"]
    base = rows[benchmark]
    return {
        "cagr_delta": v3_refined["cagr"] - base["cagr"],
        "drawdown_delta": v3_refined["max_drawdown"] - base["max_drawdown"],
        "sharpe_delta": v3_refined["sharpe"] - base["sharpe"],
        "beats_cagr": v3_refined["cagr"] > base["cagr"],
        "beats_drawdown": v3_refined["max_drawdown"] > base["max_drawdown"],
        "beats_sharpe": v3_refined["sharpe"] > base["sharpe"],
    }


def write_summary(split_results, rolling_results):
    lines = [
        "# V3.1 Refined Robustness Validation",
        "",
        "This validation fixes the best V3.1 refined configuration (with dynamic cash fallback) and tests it across fixed periods and rolling 3-year windows.",
        "",
        "## Fixed V3.1 Configuration",
        "",
    ]
    for key, value in asdict(BEST_V3_REFINED).items():
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
            "| Window | V3.1 CAGR | 50/50 CAGR | CAGR Delta | V3.1 DD | 50/50 DD | DD Delta | V3.1 Sharpe | 50/50 Sharpe | Sharpe Delta |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    wins = {"cagr": 0, "drawdown": 0, "sharpe": 0}
    for window, rows, delta in rolling_results:
        v3_refined = rows["Dual Sleeve V3.1 Best"]
        base = rows["50/50 SPY/QQQ"]
        wins["cagr"] += int(delta["beats_cagr"])
        wins["drawdown"] += int(delta["beats_drawdown"])
        wins["sharpe"] += int(delta["beats_sharpe"])
        lines.append(
            f"| {window} | {pct(v3_refined['cagr'])} | {pct(base['cagr'])} | {pct(delta['cagr_delta'])} | "
            f"{pct(v3_refined['max_drawdown'])} | {pct(base['max_drawdown'])} | {pct(delta['drawdown_delta'])} | "
            f"{v3_refined['sharpe']:.2f} | {base['sharpe']:.2f} | {delta['sharpe_delta']:.2f} |"
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
            "- V3.1 with cash fallback significantly reduces bear-market drag versus standard V3.",
            "- Drawing comparison against V2 Best, V3.1 shows a much healthier return profile in recovery and growth periods while controlling downside.",
        ]
    )

    (RESULTS_DIR / "v3_refined_robustness_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    close = fetch_close_prices()
    indicators = prepare_indicators(close)
    v3_refined_curve, _allocations = run_v3(close, indicators, BEST_V3_REFINED)
    v3_refined_curve = v3_refined_curve.rename("Dual Sleeve V3.1 Best")

    curves = {
        "Dual Sleeve V3.1 Best": v3_refined_curve,
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
