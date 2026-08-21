#!/usr/bin/env python3
"""Measure fixed historical edge fragility without searching a new strategy."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SAMPLES = 20_000
SEED = 20_260_821

ATTRIBUTION = RESULTS / "economic_edge_trade_attribution.csv"
DELTAS = RESULTS / "economic_edge_profit_lock_deltas.csv"
EXPECTANCY = RESULTS / "forward_expectancy_scorecard.csv"
SELECTION = RESULTS / "selection_bias_audit_summary.json"

OUTPUT_JSON = RESULTS / "historical_uncertainty_audit.json"
OUTPUT_CSV = RESULTS / "historical_uncertainty_audit_matrix.csv"
OUTPUT_REPORT = RESULTS / "historical_uncertainty_audit_report.md"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corrected_probability(mask: np.ndarray) -> float:
    return float((int(np.count_nonzero(mask)) + 1) / (len(mask) + 1))


def distribution(values: np.ndarray) -> dict[str, float]:
    return {
        "p025": float(np.quantile(values, 0.025)),
        "p05": float(np.quantile(values, 0.05)),
        "median": float(np.quantile(values, 0.50)),
        "p95": float(np.quantile(values, 0.95)),
        "p975": float(np.quantile(values, 0.975)),
    }


def cluster_frames(frame: pd.DataFrame) -> list[pd.DataFrame]:
    if frame.empty or "signal_date" not in frame:
        raise RuntimeError("signal-date clustered input is empty or malformed")
    return [group.reset_index(drop=True) for _, group in frame.groupby("signal_date", sort=True)]


def bootstrap_quality_exclusions(
    frame: pd.DataFrame,
    samples: int = SAMPLES,
    seed: int = SEED,
) -> dict:
    data = frame.loc[
        frame["group"].eq("baseline_only") & frame["reason"].ne("portfolio_path")
    ].copy()
    data["pnl"] = pd.to_numeric(data["pnl"], errors="raise")
    data["return"] = pd.to_numeric(data["return"], errors="raise")
    clusters = cluster_frames(data)
    rng = np.random.default_rng(seed)
    selected = rng.integers(0, len(clusters), size=(samples, len(clusters)))
    cluster_counts = np.array([len(cluster) for cluster in clusters], dtype=float)
    pnl_sums = np.array([cluster["pnl"].sum() for cluster in clusters], dtype=float)
    return_sums = np.array([cluster["return"].sum() for cluster in clusters], dtype=float)
    sampled_counts = cluster_counts[selected].sum(axis=1)
    pnl_means = pnl_sums[selected].sum(axis=1) / sampled_counts
    return_means = return_sums[selected].sum(axis=1) / sampled_counts

    jackknife = []
    for signal_date in sorted(data["signal_date"].astype(str).unique()):
        remaining = data.loc[data["signal_date"].astype(str).ne(signal_date)]
        jackknife.append(
            {
                "omitted_signal_date": signal_date,
                "mean_pnl": float(remaining["pnl"].mean()),
                "mean_return": float(remaining["return"].mean()),
            }
        )
    all_negative = all(row["mean_pnl"] < 0 and row["mean_return"] < 0 for row in jackknife)
    both_negative = (pnl_means < 0) & (return_means < 0)
    probability_both = corrected_probability(both_negative)
    label = (
        "historically_stable_selected_sample"
        if probability_both >= 0.90 and all_negative
        else "not_stable"
    )
    return {
        "trades": int(len(data)),
        "signal_date_clusters": int(len(clusters)),
        "observed": {
            "mean_pnl": float(data["pnl"].mean()),
            "mean_return": float(data["return"].mean()),
            "loss_rate": float((data["pnl"] <= 0).mean()),
        },
        "bootstrap": {
            "samples": samples,
            "seed": seed,
            "mean_pnl": distribution(pnl_means),
            "mean_return": distribution(return_means),
            "probability_mean_pnl_negative": corrected_probability(pnl_means < 0),
            "probability_mean_return_negative": corrected_probability(return_means < 0),
            "probability_both_negative": probability_both,
        },
        "leave_one_cluster_out": {
            "estimates": jackknife,
            "minimum_mean_pnl": min(row["mean_pnl"] for row in jackknife),
            "maximum_mean_pnl": max(row["mean_pnl"] for row in jackknife),
            "minimum_mean_return": min(row["mean_return"] for row in jackknife),
            "maximum_mean_return": max(row["mean_return"] for row in jackknife),
            "every_omission_keeps_both_negative": all_negative,
        },
        "evidence_label": label,
        "caveat": "selected current-list sample; family-wise selection concern remains applicable",
    }


def paired_metrics(frame: pd.DataFrame) -> dict[str, float]:
    return {
        "mean_total_pnl_delta": float(frame["pnl_delta"].mean()),
        "mean_direct_exit_effect": float(frame["direct_exit_effect_on_rsr1_shares"].mean()),
        "mean_path_sizing_residual": float(frame["capital_path_and_sizing_residual"].mean()),
        "win_rate_delta": float((frame["rsr2_pnl"] > 0).mean() - (frame["rsr1_pnl"] > 0).mean()),
    }


def removal_sensitivity(values: pd.Series) -> dict[str, float | int]:
    positive = values.loc[values > 1e-9].sort_values(ascending=False)
    total = float(values.sum())
    return {
        "nonzero_positive_rows": int(len(positive)),
        "observed_aggregate": total,
        "largest_positive": float(positive.iloc[0]) if len(positive) else 0.0,
        "two_largest_positive": float(positive.iloc[:2].sum()) if len(positive) else 0.0,
        "remaining_after_largest": float(total - positive.iloc[:1].sum()),
        "remaining_after_two_largest": float(total - positive.iloc[:2].sum()),
        "two_largest_share": float(positive.iloc[:2].sum() / total) if total else 0.0,
    }


def bootstrap_paired_deltas(
    frame: pd.DataFrame,
    samples: int = SAMPLES,
    seed: int = SEED,
) -> dict:
    data = frame.copy()
    numeric = [
        "rsr1_pnl",
        "rsr2_pnl",
        "pnl_delta",
        "direct_exit_effect_on_rsr1_shares",
        "capital_path_and_sizing_residual",
    ]
    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="raise")
    clusters = cluster_frames(data)
    rng = np.random.default_rng(seed)
    selected = rng.integers(0, len(clusters), size=(samples, len(clusters)))
    cluster_counts = np.array([len(cluster) for cluster in clusters], dtype=float)
    sampled_counts = cluster_counts[selected].sum(axis=1)

    def sampled_mean(column: str) -> np.ndarray:
        sums = np.array([cluster[column].sum() for cluster in clusters], dtype=float)
        return sums[selected].sum(axis=1) / sampled_counts

    rsr1_win_sums = np.array(
        [(cluster["rsr1_pnl"] > 0).sum() for cluster in clusters], dtype=float
    )
    rsr2_win_sums = np.array(
        [(cluster["rsr2_pnl"] > 0).sum() for cluster in clusters], dtype=float
    )
    draws = {
        "mean_total_pnl_delta": sampled_mean("pnl_delta"),
        "mean_direct_exit_effect": sampled_mean("direct_exit_effect_on_rsr1_shares"),
        "mean_path_sizing_residual": sampled_mean("capital_path_and_sizing_residual"),
        "win_rate_delta": (
            rsr2_win_sums[selected].sum(axis=1) - rsr1_win_sums[selected].sum(axis=1)
        )
        / sampled_counts,
    }

    jackknife = []
    for signal_date in sorted(data["signal_date"].astype(str).unique()):
        remaining = data.loc[data["signal_date"].astype(str).ne(signal_date)]
        metrics = paired_metrics(remaining)
        metrics["omitted_signal_date"] = signal_date
        metrics["aggregate_total_pnl_delta"] = float(remaining["pnl_delta"].sum())
        metrics["aggregate_direct_exit_effect"] = float(
            remaining["direct_exit_effect_on_rsr1_shares"].sum()
        )
        jackknife.append(metrics)

    probabilities = {
        f"probability_{name}_positive": corrected_probability(values > 0)
        for name, values in draws.items()
    }
    all_three = (
        (draws["mean_total_pnl_delta"] > 0)
        & (draws["mean_direct_exit_effect"] > 0)
        & (draws["win_rate_delta"] > 0)
    )
    direct_probability = probabilities["probability_mean_direct_exit_effect_positive"]
    direct_sensitivity = removal_sensitivity(data["direct_exit_effect_on_rsr1_shares"])
    all_direct_positive = all(row["aggregate_direct_exit_effect"] > 0 for row in jackknife)
    if direct_probability < 0.80 or not all_direct_positive:
        label = "not_stable"
    elif (
        direct_sensitivity["nonzero_positive_rows"] < 5
        or direct_sensitivity["remaining_after_two_largest"] <= 1e-9
    ):
        label = "directional_but_sparse"
    else:
        label = "historically_stable_selected_sample"

    return {
        "paired_trades": int(len(data)),
        "signal_date_clusters": int(len(clusters)),
        "observed": {
            **paired_metrics(data),
            "aggregate_total_pnl_delta": float(data["pnl_delta"].sum()),
            "aggregate_direct_exit_effect": float(
                data["direct_exit_effect_on_rsr1_shares"].sum()
            ),
            "aggregate_path_sizing_residual": float(
                data["capital_path_and_sizing_residual"].sum()
            ),
            "wins_rsr1": int((data["rsr1_pnl"] > 0).sum()),
            "wins_rsr2": int((data["rsr2_pnl"] > 0).sum()),
        },
        "bootstrap": {
            "samples": samples,
            "seed": seed,
            "distributions": {name: distribution(values) for name, values in draws.items()},
            **probabilities,
            "probability_total_direct_and_win_all_positive": corrected_probability(all_three),
        },
        "concentration": {
            "total_pnl_delta": removal_sensitivity(data["pnl_delta"]),
            "direct_exit_effect": direct_sensitivity,
        },
        "leave_one_cluster_out": {
            "estimates": jackknife,
            "minimum_aggregate_total_pnl_delta": min(
                row["aggregate_total_pnl_delta"] for row in jackknife
            ),
            "minimum_aggregate_direct_exit_effect": min(
                row["aggregate_direct_exit_effect"] for row in jackknife
            ),
            "every_omission_keeps_total_positive": all(
                row["aggregate_total_pnl_delta"] > 0 for row in jackknife
            ),
            "every_omission_keeps_direct_positive": all_direct_positive,
        },
        "evidence_label": label,
        "caveat": "paired historical account path; total delta includes capital-path and whole-share sizing",
    }


def retrospective_expectancy_context(frame: pd.DataFrame) -> list[dict]:
    data = frame.loc[frame["scope"].eq("retrospective_calibration")].copy()
    columns = [
        "closed_trades",
        "wins",
        "win_rate",
        "win_rate_wilson_95_low",
        "win_rate_wilson_95_high",
        "expectancy_per_trade",
        "profit_factor",
        "bootstrap_p05",
        "bootstrap_median",
        "bootstrap_p95",
        "bootstrap_probability_nonpositive",
    ]
    result = []
    for _, row in data.iterrows():
        values = {column: float(row[column]) for column in columns}
        values["closed_trades"] = int(values["closed_trades"])
        values["wins"] = int(values["wins"])
        result.append({"variant": str(row["variant"]), **values})
    return result


def matrix_rows(summary: dict) -> list[dict]:
    quality = summary["quality_filter_exclusions"]
    paired = summary["rsr2_paired_delta"]
    rows = []
    for mechanism, observed_key, dist_key, favorable_key in [
        ("quality_excluded_mean_pnl", "mean_pnl", "mean_pnl", "probability_mean_pnl_negative"),
        ("quality_excluded_mean_return", "mean_return", "mean_return", "probability_mean_return_negative"),
    ]:
        dist = quality["bootstrap"][dist_key]
        rows.append(
            {
                "mechanism": mechanism,
                "observed": quality["observed"][observed_key],
                **dist,
                "probability_favorable": quality["bootstrap"][favorable_key],
                "evidence_label": quality["evidence_label"],
            }
        )
    for mechanism, observed_key, probability_key in [
        ("rsr2_mean_total_pnl_delta", "mean_total_pnl_delta", "probability_mean_total_pnl_delta_positive"),
        ("rsr2_mean_direct_exit_effect", "mean_direct_exit_effect", "probability_mean_direct_exit_effect_positive"),
        ("rsr2_mean_path_sizing_residual", "mean_path_sizing_residual", "probability_mean_path_sizing_residual_positive"),
        ("rsr2_win_rate_delta", "win_rate_delta", "probability_win_rate_delta_positive"),
    ]:
        dist = paired["bootstrap"]["distributions"][observed_key]
        rows.append(
            {
                "mechanism": mechanism,
                "observed": paired["observed"][observed_key],
                **dist,
                "probability_favorable": paired["bootstrap"][probability_key],
                "evidence_label": paired["evidence_label"],
            }
        )
    return rows


def evaluate() -> dict:
    attribution = pd.read_csv(ATTRIBUTION)
    deltas = pd.read_csv(DELTAS)
    expectancy = pd.read_csv(EXPECTANCY)
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    quality = bootstrap_quality_exclusions(attribution)
    paired = bootstrap_paired_deltas(deltas)
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "real_account_modified": False,
        "live_order_authorization": False,
        "new_parameter_search": False,
        "preregistration": "historical-uncertainty-audit-preregistration.md",
        "samples": SAMPLES,
        "seed": SEED,
        "input_hashes": {
            path.name: file_hash(path)
            for path in (ATTRIBUTION, DELTAS, EXPECTANCY, SELECTION)
        },
        "quality_filter_exclusions": quality,
        "rsr2_paired_delta": paired,
        "absolute_expectancy_context": retrospective_expectancy_context(expectancy),
        "selection_bias_context": {
            "trial_cells": selection["trial_cells"],
            "pbo": selection["cscv"]["pbo"],
            "familywise_p_value": selection["familywise_reality_check"]["familywise_p_value"],
            "positive_return_blocks": selection["fixed_cell_stability"]["positive_return_blocks"],
            "positive_sharpe_blocks": selection["fixed_cell_stability"]["positive_sharpe_blocks"],
            "blocks": selection["fixed_cell_stability"]["blocks"],
            "contained": selection["gate"]["contained"],
        },
        "decision": {
            "entry_quality_mechanism": "historically useful inside the selected current-list sample; prioritize genuine-forward validation",
            "profit_lock_mechanism": "directionally favorable but sparse; do not optimize further or promote",
            "win_rate_interpretation": "RSR2 adds only one historical win versus RSR1; headline hit-rate uplift is fragile",
            "research_priority": "forward entry-quality loss avoidance before additional exit optimization",
            "formal_action": "none",
            "real_account_action": "none",
        },
    }


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_report(summary: dict) -> None:
    quality = summary["quality_filter_exclusions"]
    paired = summary["rsr2_paired_delta"]
    qboot = quality["bootstrap"]
    pboot = paired["bootstrap"]
    total = paired["concentration"]["total_pnl_delta"]
    direct = paired["concentration"]["direct_exit_effect"]
    context = {row["variant"]: row for row in summary["absolute_expectancy_context"]}
    rsr1 = context["RSR1-shadow"]
    rsr2 = context["RSR2-profit-lock-shadow"]
    lines = [
        "# Historical edge uncertainty audit",
        "",
        "## Bottom line",
        "",
        "The historical quality filter has a stable avoided-loss signature inside the already-selected current-list sample. RSR2's additional profit-lock benefit is directionally favorable but sparse, and its higher historical win rate is one trade rather than broad evidence.",
        "",
        "This strengthens the priority order—validate entry-quality loss avoidance forward before doing more exit optimization—but does not cure survivorship/selection bias or authorize a strategy change.",
        "",
        "## Absolute historical expectancy context",
        "",
        "| Variant | Trades | Win rate (Wilson 95%) | Mean return/trade | Cluster-bootstrap 5%-95% | P(nonpositive) |",
        "| --- | ---: | --- | ---: | --- | ---: |",
    ]
    for name in ("matched_baseline", "RSR1-shadow", "RSR2-profit-lock-shadow"):
        row = context[name]
        lines.append(
            f"| {name} | {row['closed_trades']} | {pct(row['win_rate'])} "
            f"({pct(row['win_rate_wilson_95_low'])}-{pct(row['win_rate_wilson_95_high'])}) | "
            f"{pct(row['expectancy_per_trade'])} | {pct(row['bootstrap_p05'])} to "
            f"{pct(row['bootstrap_p95'])} | {pct(row['bootstrap_probability_nonpositive'])} |"
        )
    lines.extend(
        [
            "",
            "## Entry-quality exclusion robustness",
            "",
            f"- Direct exclusions: {quality['trades']} trades / {quality['signal_date_clusters']} signal-date clusters.",
            f"- Observed excluded mean return / P&L: {pct(quality['observed']['mean_return'])} / ${quality['observed']['mean_pnl']:.2f} per trade.",
            f"- Bootstrap probability both mean return and mean P&L remain negative: {pct(qboot['probability_both_negative'])}.",
            f"- 95% mean-return interval: {pct(qboot['mean_return']['p025'])} to {pct(qboot['mean_return']['p975'])}.",
            f"- Every leave-one-signal-date-out estimate remains negative: {quality['leave_one_cluster_out']['every_omission_keeps_both_negative']}.",
            f"- Label: `{quality['evidence_label']}`—this is still selected-sample evidence, not transfer proof.",
            "",
            "## RSR2 incremental robustness",
            "",
            f"- Paired trades / signal-date clusters: {paired['paired_trades']} / {paired['signal_date_clusters']}.",
            f"- RSR1 wins versus RSR2 wins: {paired['observed']['wins_rsr1']} / {paired['observed']['wins_rsr2']}; the hit-rate difference is exactly one trade.",
            f"- Aggregate total P&L delta: ${paired['observed']['aggregate_total_pnl_delta']:.2f}; probability bootstrap mean is positive: {pct(pboot['probability_mean_total_pnl_delta_positive'])}.",
            f"- Direct exit effect: ${paired['observed']['aggregate_direct_exit_effect']:.2f}; probability bootstrap mean is positive: {pct(pboot['probability_mean_direct_exit_effect_positive'])}.",
            f"- Probability total P&L, direct effect and win-rate delta are all positive: {pct(pboot['probability_total_direct_and_win_all_positive'])}.",
            f"- Two largest total deltas explain {pct(total['two_largest_share'])}; remaining total delta after both: ${total['remaining_after_two_largest']:.2f}.",
            f"- Only {direct['nonzero_positive_rows']} paired trades have a positive direct exit effect; removing both leaves ${direct['remaining_after_two_largest']:.2f}.",
            f"- Every leave-one-cluster-out total/direct aggregate remains positive: {paired['leave_one_cluster_out']['every_omission_keeps_total_positive']} / {paired['leave_one_cluster_out']['every_omission_keeps_direct_positive']}.",
            f"- Label: `{paired['evidence_label']}`.",
            "",
            "## Decision",
            "",
            "1. Treat RSR1's loss-avoidance mechanism as the more important forward question. Its absolute historical expectancy bootstrap is strong, but the exact transfer and 7/10 stability gates still fail.",
            "2. Keep RSR2 as a separate frozen shadow. Its profit direction is favorable, but two direct exits and one win conversion are too sparse for promotion.",
            "3. Do not search a new profit trigger, floor, partial-exit fraction or holding period on this history.",
            "4. Formal V9, the real account and all order states remain unchanged.",
            "",
            "No order or live authorization is created by this report.",
        ]
    )
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary = evaluate()
    OUTPUT_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame(matrix_rows(summary)).to_csv(OUTPUT_CSV, index=False)
    write_report(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
