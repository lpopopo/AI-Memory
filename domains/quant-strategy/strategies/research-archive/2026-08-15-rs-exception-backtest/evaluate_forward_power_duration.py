from __future__ import annotations

import json
import math
from statistics import NormalDist
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SCORECARD = RESULTS / "forward_expectancy_scorecard.json"
DAILY_RETURNS = RESULTS / "selection_bias_daily_returns.csv"

ALPHA = 0.05
TARGET_POWER = 0.80
MAX_SAMPLE = 500
BASELINE_RATE = 19 / 44
CALIBRATION_SESSIONS = 659
ARRIVAL_TRADES = 23
ARRIVAL_RATE = ARRIVAL_TRADES / CALIBRATION_SESSIONS
NORMAL = NormalDist()


def binomial_pmf_array(trials: int, rate: float) -> np.ndarray:
    wins = np.arange(trials + 1, dtype=float)
    if rate <= 0.0:
        result = np.zeros(trials + 1)
        result[0] = 1.0
        return result
    if rate >= 1.0:
        result = np.zeros(trials + 1)
        result[-1] = 1.0
        return result
    log_probabilities = np.array(
        [
            math.lgamma(trials + 1)
            - math.lgamma(int(value) + 1)
            - math.lgamma(trials - int(value) + 1)
            + value * math.log(rate)
            + (trials - value) * math.log1p(-rate)
            for value in wins
        ]
    )
    probabilities = np.exp(log_probabilities)
    return probabilities / probabilities.sum()


def binomial_sf(wins_minus_one: int, trials: int, rate: float) -> float:
    boundary = wins_minus_one + 1
    if boundary <= 0:
        return 1.0
    if boundary > trials:
        return 0.0
    return float(binomial_pmf_array(trials, rate)[boundary:].sum())


def poisson_sf(count_minus_one: int, mean: float) -> float:
    if count_minus_one < 0:
        return 1.0
    if mean <= 0.0:
        return 0.0
    boundary = count_minus_one + 1
    log_term = -mean + boundary * math.log(mean) - math.lgamma(boundary + 1)
    term = math.exp(log_term)
    total = term
    count = boundary
    while count < 100_000:
        count += 1
        term *= mean / count
        total += term
        if count > mean and term <= max(total, 1e-300) * 1e-15:
            break
    return max(0.0, min(1.0, total))


def wilson_interval(wins: int, trials: int, confidence: float = 0.95) -> tuple[float, float]:
    if trials <= 0:
        return np.nan, np.nan
    z = float(NORMAL.inv_cdf(0.5 + confidence / 2.0))
    p = wins / trials
    denominator = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denominator
    half = z / denominator * math.sqrt(p * (1.0 - p) / trials + z * z / (4.0 * trials * trials))
    return center - half, center + half


def critical_wins(trials: int, null_rate: float, alpha: float = ALPHA) -> int:
    for wins in range(trials + 1):
        if binomial_sf(wins - 1, trials, null_rate) <= alpha:
            return wins
    return trials + 1


def one_sample_power(trials: int, null_rate: float, true_rate: float) -> tuple[float, int]:
    boundary = critical_wins(trials, null_rate)
    power = binomial_sf(boundary - 1, trials, true_rate) if boundary <= trials else 0.0
    return power, boundary


def minimum_one_sample(
    null_rate: float,
    true_rate: float,
    target_power: float = TARGET_POWER,
    maximum: int = MAX_SAMPLE,
) -> tuple[int | None, float | None, int | None]:
    for trials in range(5, maximum + 1):
        power, boundary = one_sample_power(trials, null_rate, true_rate)
        if power >= target_power:
            return trials, power, boundary
    return None, None, None


def two_sample_z_power(trials: int, candidate_rate: float, baseline_rate: float) -> float:
    candidate_wins = np.arange(trials + 1)[:, None]
    baseline_wins = np.arange(trials + 1)[None, :]
    pooled = (candidate_wins + baseline_wins) / (2.0 * trials)
    denominator = np.sqrt(pooled * (1.0 - pooled) * (2.0 / trials))
    difference = candidate_wins / trials - baseline_wins / trials
    statistic = np.divide(
        difference,
        denominator,
        out=np.zeros_like(difference, dtype=float),
        where=denominator > 0,
    )
    reject = statistic >= float(NORMAL.inv_cdf(1.0 - ALPHA))
    probability = np.outer(
        binomial_pmf_array(trials, candidate_rate),
        binomial_pmf_array(trials, baseline_rate),
    )
    return float(probability[reject].sum())


def minimum_two_sample(
    candidate_rate: float,
    baseline_rate: float,
    target_power: float = TARGET_POWER,
    maximum: int = MAX_SAMPLE,
) -> tuple[int | None, float | None]:
    for trials in range(5, maximum + 1):
        power = two_sample_z_power(trials, candidate_rate, baseline_rate)
        if power >= target_power:
            return trials, power
    return None, None


def wilson_event_probability(
    trials: int,
    true_rate: float,
    lower_threshold: float | None = None,
    maximum_half_width: float | None = None,
) -> float:
    if (lower_threshold is None) == (maximum_half_width is None):
        raise ValueError("specify exactly one Wilson event")
    wins = np.arange(trials + 1)
    accepted = []
    for value in wins:
        low, high = wilson_interval(int(value), trials)
        if lower_threshold is not None:
            accepted.append(low > lower_threshold)
        else:
            accepted.append((high - low) / 2.0 <= float(maximum_half_width))
    probabilities = binomial_pmf_array(trials, true_rate)
    return float(probabilities[np.asarray(accepted, dtype=bool)].sum())


def minimum_wilson_event(
    true_rate: float,
    lower_threshold: float | None = None,
    maximum_half_width: float | None = None,
    target_probability: float = TARGET_POWER,
    maximum: int = MAX_SAMPLE,
) -> tuple[int | None, float | None]:
    for trials in range(5, maximum + 1):
        probability = wilson_event_probability(
            trials,
            true_rate,
            lower_threshold=lower_threshold,
            maximum_half_width=maximum_half_width,
        )
        if probability >= target_probability:
            return trials, probability
    return None, None


def probability_reach(target: int, sessions: int, rate: float = ARRIVAL_RATE) -> float:
    return poisson_sf(target - 1, rate * sessions)


def completion_quantile(target: int, probability: float, rate: float = ARRIVAL_RATE) -> int:
    low, high = 0, max(int(math.ceil(target / rate)), 1)
    while probability_reach(target, high, rate) < probability:
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if probability_reach(target, middle, rate) >= probability:
            high = middle
        else:
            low = middle + 1
    return low


def load_calibration() -> list[dict]:
    payload = json.loads(SCORECARD.read_text(encoding="utf-8"))
    rows = {row["variant"]: row for row in payload["retrospective_calibration"]}
    expected = {
        "matched_baseline": (44, 19),
        "RSR1-shadow": (23, 15),
        "RSR2-profit-lock-shadow": (23, 16),
    }
    for name, (trades, wins) in expected.items():
        row = rows[name]
        if int(row["closed_trades"]) != trades or int(row["wins"]) != wins:
            raise RuntimeError(f"frozen calibration changed for {name}")
    dates = pd.read_csv(DAILY_RETURNS, usecols=["date"], parse_dates=["date"])
    if (
        len(dates) != CALIBRATION_SESSIONS
        or dates["date"].min() != pd.Timestamp("2024-01-02")
        or dates["date"].max() != pd.Timestamp("2026-08-18")
    ):
        raise RuntimeError("frozen session calibration changed")
    return [rows["RSR1-shadow"], rows["RSR2-profit-lock-shadow"]]


def build_one_sample(calibration: list[dict]) -> pd.DataFrame:
    rows = []
    for candidate in calibration:
        name = candidate["variant"]
        true_rate = float(candidate["win_rate"])
        nulls = {
            "candidate_breakeven": float(candidate["breakeven_win_rate"]),
            "matched_baseline_rate": BASELINE_RATE,
            "majority_50pct": 0.50,
        }
        for null_name, null_rate in nulls.items():
            power20, boundary20 = one_sample_power(20, null_rate, true_rate)
            minimum, achieved, boundary = minimum_one_sample(null_rate, true_rate)
            rows.append(
                {
                    "variant": name,
                    "null": null_name,
                    "null_rate": null_rate,
                    "planning_true_rate": true_rate,
                    "power_at_20": power20,
                    "critical_wins_at_20": boundary20,
                    "minimum_n_for_80pct_power": minimum,
                    "power_at_minimum_n": achieved,
                    "critical_wins_at_minimum_n": boundary,
                }
            )
    return pd.DataFrame(rows)


def build_two_sample(calibration: list[dict]) -> pd.DataFrame:
    rows = []
    for candidate in calibration:
        true_rate = float(candidate["win_rate"])
        minimum, achieved = minimum_two_sample(true_rate, BASELINE_RATE)
        rows.append(
            {
                "variant": candidate["variant"],
                "candidate_rate": true_rate,
                "baseline_rate": BASELINE_RATE,
                "power_at_equal_n_20": two_sample_z_power(20, true_rate, BASELINE_RATE),
                "minimum_equal_n_for_80pct_power": minimum,
                "power_at_minimum_equal_n": achieved,
            }
        )
    return pd.DataFrame(rows)


def build_wilson(calibration: list[dict]) -> pd.DataFrame:
    rows = []
    for candidate in calibration:
        name = candidate["variant"]
        true_rate = float(candidate["win_rate"])
        thresholds = {
            "candidate_breakeven": float(candidate["breakeven_win_rate"]),
            "matched_baseline_rate": BASELINE_RATE,
            "majority_50pct": 0.50,
        }
        for threshold_name, threshold in thresholds.items():
            minimum, achieved = minimum_wilson_event(
                true_rate, lower_threshold=threshold
            )
            rows.append(
                {
                    "variant": name,
                    "event": f"lower_bound_above_{threshold_name}",
                    "threshold": threshold,
                    "probability_at_20": wilson_event_probability(
                        20, true_rate, lower_threshold=threshold
                    ),
                    "minimum_n_for_80pct_probability": minimum,
                    "probability_at_minimum_n": achieved,
                }
            )
        minimum, achieved = minimum_wilson_event(
            true_rate, maximum_half_width=0.10
        )
        rows.append(
            {
                "variant": name,
                "event": "half_width_at_most_10pct",
                "threshold": 0.10,
                "probability_at_20": wilson_event_probability(
                    20, true_rate, maximum_half_width=0.10
                ),
                "minimum_n_for_80pct_probability": minimum,
                "probability_at_minimum_n": achieved,
            }
        )
    return pd.DataFrame(rows)


def build_duration(
    one_sample: pd.DataFrame, two_sample: pd.DataFrame, wilson: pd.DataFrame
) -> pd.DataFrame:
    targets = {20}
    for column, frame in (
        ("minimum_n_for_80pct_power", one_sample),
        ("minimum_equal_n_for_80pct_power", two_sample),
        ("minimum_n_for_80pct_probability", wilson),
    ):
        targets.update(int(value) for value in frame[column].dropna())
    rows = []
    for target in sorted(targets):
        expected = target / ARRIVAL_RATE
        rows.append(
            {
                "target_trades": target,
                "expected_sessions": expected,
                "median_completion_sessions": completion_quantile(target, 0.50),
                "p80_completion_sessions": completion_quantile(target, 0.80),
                "expected_years_252": expected / 252.0,
                "probability_within_126_sessions": probability_reach(target, 126),
            }
        )
    return pd.DataFrame(rows)


def pct(value: float | None) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.1%}"


def probability_text(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    if 0.0 < value < 0.0001:
        return "<0.01%"
    return f"{value:.1%}"


def write_report(
    calibration: list[dict],
    one_sample: pd.DataFrame,
    two_sample: pd.DataFrame,
    wilson: pd.DataFrame,
    duration: pd.DataFrame,
) -> None:
    lines = [
        "# Forward validation power and duration audit",
        "",
        "## Bottom line",
        "",
        "Twenty closed trades can be a useful economic falsification screen, but it cannot establish the historical 65%-70% hit-rate headline with high confidence.",
        "The original gate is unchanged; larger values below are second-stage confidence benchmarks only.",
        "",
        "## Exact one-sample power",
        "",
        "| Variant | Null | Power at 20 | Wins needed at 20 | n for 80% power |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in one_sample.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.null} ({row.null_rate:.1%}) | {pct(row.power_at_20)} | "
            f"{int(row.critical_wins_at_20)} | {int(row.minimum_n_for_80pct_power)} |"
        )
    lines.extend(
        [
            "",
            "## Equal-sample relative comparison versus the 43.18% baseline",
            "",
            "| Variant | Power at 20+20 | Equal n per arm for 80% power |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in two_sample.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {pct(row.power_at_equal_n_20)} | {int(row.minimum_equal_n_for_80pct_power)} |"
        )
    lines.extend(
        [
            "",
            "## Wilson 95% confidence events",
            "",
            "| Variant | Event | Probability at 20 | n for 80% probability |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for row in wilson.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.event} | {pct(row.probability_at_20)} | "
            f"{int(row.minimum_n_for_80pct_probability)} |"
        )
    lines.extend(
        [
            "",
            "## Historical-rate duration calibration",
            "",
            f"Planning rate: {ARRIVAL_TRADES} trades / {CALIBRATION_SESSIONS} sessions = {ARRIVAL_RATE:.4f} trades/session.",
            "",
            "| Target trades | Expected sessions | Expected years | Median sessions | 80% completion | P(reach by 126 sessions) |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in duration.itertuples(index=False):
        lines.append(
            f"| {int(row.target_trades)} | {row.expected_sessions:.0f} | {row.expected_years_252:.1f} | "
            f"{int(row.median_completion_sessions)} | {int(row.p80_completion_sessions)} | "
            f"{probability_text(row.probability_within_126_sessions)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "At twenty trades, strong power against the candidate's low break-even hit rate can show that the payoff distribution is economically plausible. "
            "It is a different claim from proving that future win rate exceeds 50% or reproduces the retrospective advantage over baseline. "
            "The break-even comparison is conditional on the historical average-win/average-loss relationship; forward payoff and expectancy must still be measured directly. "
            "The arrival model also shows that the 20-trade condition, not 126 sessions, is likely to be the binding clock. "
            "Do not expand the universe or loosen filters to accelerate that clock; doing so would create a different strategy and invalidate the frozen comparison.",
            "",
            "Research-only. No order is authorized and no promotion gate is changed.",
        ]
    )
    (RESULTS / "forward_power_duration_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    calibration = load_calibration()
    one_sample = build_one_sample(calibration)
    two_sample = build_two_sample(calibration)
    wilson = build_wilson(calibration)
    duration = build_duration(one_sample, two_sample, wilson)
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "changes_promotion_gate": False,
        "preregistration": "forward-power-duration-audit-preregistration.md",
        "alpha_one_sided": ALPHA,
        "target_power": TARGET_POWER,
        "maximum_sample_search": MAX_SAMPLE,
        "baseline_rate": BASELINE_RATE,
        "arrival": {
            "trades": ARRIVAL_TRADES,
            "sessions": CALIBRATION_SESSIONS,
            "rate_per_session": ARRIVAL_RATE,
        },
        "variants": [
            {
                "variant": row["variant"],
                "planning_win_rate": row["win_rate"],
                "break_even_win_rate": row["breakeven_win_rate"],
            }
            for row in calibration
        ],
        "one_sample_power": json.loads(one_sample.to_json(orient="records")),
        "two_sample_power": json.loads(two_sample.to_json(orient="records")),
        "wilson_confidence": json.loads(wilson.to_json(orient="records")),
        "duration": json.loads(duration.to_json(orient="records")),
        "interpretation": {
            "twenty_trades_powerful_against_breakeven": bool(
                one_sample.loc[
                    one_sample["null"] == "candidate_breakeven", "power_at_20"
                ].ge(TARGET_POWER).all()
            ),
            "twenty_trades_powerful_against_majority": bool(
                one_sample.loc[
                    one_sample["null"] == "majority_50pct", "power_at_20"
                ].ge(TARGET_POWER).all()
            ),
            "twenty_trade_gate_is_binding_clock": True,
            "changes_promotion_gate": False,
        },
    }
    one_sample.to_csv(RESULTS / "forward_power_one_sample.csv", index=False)
    two_sample.to_csv(RESULTS / "forward_power_two_sample.csv", index=False)
    wilson.to_csv(RESULTS / "forward_power_wilson.csv", index=False)
    duration.to_csv(RESULTS / "forward_power_duration.csv", index=False)
    (RESULTS / "forward_power_duration_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(calibration, one_sample, two_sample, wilson, duration)
    print(RESULTS / "forward_power_duration_report.md")


if __name__ == "__main__":
    main()
