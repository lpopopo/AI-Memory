from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import pit_low_vol_backtest as pit


HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "results"
VARIANTS = ("equal_weekly", "soft_vol_weekly", "buffer_equal", "buffer_soft_vol")


def soft_vol_weights(selected: pd.DataFrame) -> pd.Series:
    if selected.empty:
        return pd.Series(dtype=float)
    equal = pd.Series(1.0 / len(selected), index=selected.index)
    inverse_sqrt_vol = 1.0 / np.sqrt(selected["rv20"].clip(lower=0.01))
    risk_weights = inverse_sqrt_vol / inverse_sqrt_vol.sum()
    # A 50/50 blend keeps every selected momentum name and prevents the
    # volatility estimate from dominating a small five-name sleeve.
    return 0.5 * equal + 0.5 * risk_weights


def buffered_selection(snapshot: pd.DataFrame, previous: list[str]) -> pd.DataFrame:
    if snapshot.empty:
        return snapshot
    keep_zone = set(snapshot.head(10).index)
    retained = [symbol for symbol in previous if symbol in keep_zone]
    additions = [symbol for symbol in snapshot.index if symbol not in retained]
    selected = (retained + additions)[: pit.TOP_N]
    return snapshot.loc[selected]


def build_targets(
    prices: pd.DataFrame,
    membership: pd.DataFrame,
    features: dict[str, pd.DataFrame | pd.Series],
) -> dict[str, pd.DataFrame]:
    records: dict[str, list[pd.Series]] = {name: [] for name in VARIANTS}
    previous: dict[str, list[str]] = {"buffer_equal": [], "buffer_soft_vol": []}
    for date in pit.weekly_signal_dates(prices.index):
        snapshot = pit.candidate_snapshot(date, prices, membership, features)
        selections = {
            "equal_weekly": snapshot.head(pit.TOP_N),
            "soft_vol_weekly": snapshot.head(pit.TOP_N),
            "buffer_equal": buffered_selection(snapshot, previous["buffer_equal"]),
            "buffer_soft_vol": buffered_selection(snapshot, previous["buffer_soft_vol"]),
        }
        for name, selected in selections.items():
            weights = pd.Series(0.0, index=prices.columns, name=date)
            if not selected.empty:
                if name in ("soft_vol_weekly", "buffer_soft_vol"):
                    weights.loc[selected.index] = soft_vol_weights(selected)
                else:
                    weights.loc[selected.index] = 1.0 / len(selected)
            records[name].append(weights)
            if name in previous:
                previous[name] = list(selected.index)
    return {name: pd.DataFrame(rows) for name, rows in records.items()}


def evaluate(prices: pd.DataFrame, targets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name in VARIANTS:
        for cost_bps in (0.0, 10.0, 20.0, 50.0):
            result, _ = pit.simulate(prices, targets[name], cost_bps=cost_bps)
            for metric in pit.period_metrics(result, name, "zero_return"):
                if not str(metric["variant"]).endswith("mapped_25pct"):
                    rows.append({"cost_bps": cost_bps, **metric})
    return pd.DataFrame(rows)


def rolling_compare(
    prices: pd.DataFrame, targets: dict[str, pd.DataFrame], candidate_name: str
) -> tuple[pd.DataFrame, dict[str, float]]:
    baseline, _ = pit.simulate(prices, targets["equal_weekly"], cost_bps=10.0)
    candidate, _ = pit.simulate(prices, targets[candidate_name], cost_bps=10.0)
    return pit.rolling_three_year_comparison(baseline, candidate)


def pct(value: float) -> str:
    return "NA" if pd.isna(value) else f"{value:.2%}"


def num(value: float) -> str:
    return "NA" if pd.isna(value) else f"{value:.2f}"


def write_report(metrics: pd.DataFrame, rolling_summaries: dict[str, dict[str, float]]) -> None:
    lines = [
        "# PIT soft sizing and turnover-buffer exploration",
        "",
        "## Boundary",
        "",
        "This is a post-hoc exploration on the same partial point-in-time adjusted-close panel. It cannot promote a rule. "
        "All variants keep the same eligible names; no low-volatility stock is excluded.",
        "",
        "- `equal_weekly`: original top-five equal-weight weekly baseline.",
        "- `soft_vol_weekly`: same five names, blending equal weights 50/50 with inverse-square-root-volatility weights.",
        "- `buffer_equal`: keep an existing name while it remains in the top ten, then fill to five; equal weight.",
        "- `buffer_soft_vol`: combine the top-ten holding buffer and soft volatility tilt.",
        "",
        "## Ten-basis-point results",
        "",
        "| Variant | Period | CAGR | Max DD | Sharpe | Monthly win | Annual turnover |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    selected = metrics.loc[metrics["cost_bps"] == 10.0]
    for row in selected.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.period} | {pct(row.cagr)} | {pct(row.max_drawdown)} | {num(row.sharpe)} | "
            f"{pct(row.monthly_win_rate)} | {num(row.annual_turnover)} |"
        )
    lines.extend(
        [
            "",
            "## Final-period cost sensitivity",
            "",
            "| Variant | Cost | CAGR | Max DD | Sharpe |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    final = metrics.loc[metrics["period"] == "final_2020_2025"]
    for row in final.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.cost_bps:.0f} bps | {pct(row.cagr)} | {pct(row.max_drawdown)} | {num(row.sharpe)} |"
        )
    lines.extend(["", "## Rolling three-year comparison versus equal weekly", ""])
    for name, summary in rolling_summaries.items():
        lines.append(
            f"- `{name}`: higher CAGR {summary['higher_cagr_rate']:.1%}, better drawdown "
            f"{summary['better_drawdown_rate']:.1%}, higher Sharpe {summary['higher_sharpe_rate']:.1%}, "
            f"higher monthly win rate {summary['higher_monthly_win_rate']:.1%} across "
            f"{int(summary['windows'])} windows."
        )
    lines.extend(
        [
            "",
            "## Retrospective screen",
            "",
            "| Variant | Better CAGR and Sharpe in validation/final at 10/20 bps | Lower turnover | No worse drawdown | Result |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    baseline = metrics.loc[metrics["variant"] == "equal_weekly"].set_index(["period", "cost_bps"])
    required_periods = ("validation_2015_2019", "final_2020_2025")
    required_costs = (10.0, 20.0)
    for name in VARIANTS[1:]:
        candidate = metrics.loc[metrics["variant"] == name].set_index(["period", "cost_bps"])
        keys = [(period, cost) for period in required_periods for cost in required_costs]
        return_quality = all(
            candidate.loc[key, "cagr"] > baseline.loc[key, "cagr"]
            and candidate.loc[key, "sharpe"] > baseline.loc[key, "sharpe"]
            for key in keys
        )
        lower_turnover = all(
            candidate.loc[(period, 10.0), "annual_turnover"] < baseline.loc[(period, 10.0), "annual_turnover"]
            for period in required_periods
        )
        drawdown = all(
            candidate.loc[key, "max_drawdown"] >= baseline.loc[key, "max_drawdown"] for key in keys
        )
        passed = return_quality and lower_turnover and drawdown
        yn = lambda value: "yes" if value else "no"
        lines.append(
            f"| {name} | {yn(return_quality)} | {yn(lower_turnover)} | {yn(drawdown)} | "
            f"{'shadow-worthy' if passed else 'reject'} |"
        )
    lines.extend(
        [
            "",
            "## Decision standard",
            "",
            "A useful successor must improve validation and final-period net return/Sharpe at both 10 and 20 bps, reduce turnover materially, "
            "and avoid a worse max drawdown. Passing this retrospective screen would justify only a new preregistered shadow version.",
            "",
            "None passed. The soft volatility tilt reduced neither turnover nor return sacrifice. The top-ten holding buffer helped 2020-2025 "
            "and lowered turnover, but materially worsened 2015-2019; it is not stable enough to create a second shadow candidate.",
        ]
    )
    (OUT_DIR / "pit_sizing_turnover_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    prices, membership, market = pit.load_inputs()
    features = pit.calculate_features(prices, market)
    targets = build_targets(prices, membership, features)
    metrics = evaluate(prices, targets)
    rolling_summaries: dict[str, dict[str, float]] = {}
    for name in VARIANTS[1:]:
        rolling, summary = rolling_compare(prices, targets, name)
        rolling.to_csv(OUT_DIR / f"pit_rolling_3y_{name}.csv", index=False)
        rolling_summaries[name] = summary
    metrics.to_csv(OUT_DIR / "pit_sizing_turnover_metrics.csv", index=False)
    write_report(metrics, rolling_summaries)
    print(OUT_DIR / "pit_sizing_turnover_report.md")


if __name__ == "__main__":
    main()
