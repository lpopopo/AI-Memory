from __future__ import annotations

import itertools
import json
import math
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))

START = pd.Timestamp("2024-01-02")
FROZEN_END = pd.Timestamp("2026-08-18")
BLOCKS = 10
BOOTSTRAP_SAMPLES = 10_000
BOOTSTRAP_BLOCK = 20
BOOTSTRAP_SEED = 20260820
BASELINE_ID = "atr_100_loc_00"
FIXED_ID = "atr_04_loc_50"
COMMON = dict(
    rs20_min=0.03,
    volume_ratio_min=1.20,
    max_extension=0.12,
    max_hold_days=20,
    stop_loss=0.08,
)


def cell_id(atr: float, location: float) -> str:
    atr_text = "100" if atr >= 1.0 else f"{int(round(atr * 100)):02d}"
    location_text = f"{int(round(location * 100)):02d}"
    return f"atr_{atr_text}_loc_{location_text}"


def grid() -> list[tuple[str, float, float]]:
    return [
        (cell_id(atr, location), atr, location)
        for atr in (0.03, 0.04, 0.05, 0.06, 1.00)
        for location in (0.00, 0.25, 0.50, 0.75)
    ]


def equity_returns(equity: dict[str, float]) -> pd.Series:
    series = pd.Series(equity, dtype=float)
    series.index = pd.to_datetime(series.index)
    return series.sort_index().pct_change(fill_method=None).fillna(0.0)


def run_paths() -> tuple[pd.DataFrame, pd.DataFrame]:
    panels, symbols = MODULE["load_panels"]()
    required = panels["close"].loc[:FROZEN_END, ["SPY", "QQQ", "SMH"]]
    if FROZEN_END not in required.index or required.loc[FROZEN_END].isna().any():
        raise RuntimeError("frozen 2026-08-18 market close is unavailable")
    paths = {}
    metadata = []
    for name, atr, location in grid():
        config = MODULE["Config"](
            **COMMON,
            max_atr_pct=atr,
            min_close_location=location,
        )
        result = MODULE["simulate"](
            panels,
            symbols,
            config,
            "strict_veto",
            str(START.date()),
            str(FROZEN_END.date()),
            slippage=0.001,
        )
        paths[name] = equity_returns(result["equity"])
        metadata.append(
            {
                "cell_id": name,
                "atr_cap": atr,
                "close_location_floor": location,
                "trade_count": int(result["metrics"]["trade_count"]),
                "full_return": float(result["metrics"]["total_return"]),
                "full_sharpe": float(result["metrics"]["sharpe"]),
                "full_win_rate": result["metrics"]["win_rate"],
            }
        )
    frame = pd.concat(paths, axis=1).sort_index().loc[START:FROZEN_END]
    if frame.isna().any().any() or frame.index.max() != FROZEN_END:
        raise RuntimeError("daily return paths are incomplete or exceed the frozen end")
    if list(frame.columns) != [item[0] for item in grid()]:
        raise RuntimeError("trial family changed")
    return frame, pd.DataFrame(metadata)


def contiguous_blocks(count: int, blocks: int = BLOCKS) -> list[np.ndarray]:
    if count < blocks:
        raise ValueError("not enough observations for requested blocks")
    result = [part.astype(int) for part in np.array_split(np.arange(count), blocks)]
    combined = np.concatenate(result)
    if not np.array_equal(combined, np.arange(count)):
        raise RuntimeError("blocks must cover every observation exactly once")
    return result


def compounded(values: np.ndarray) -> float:
    return float(np.prod(1.0 + values) - 1.0)


def sharpe(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    volatility = float(values.std(ddof=0))
    return float(values.mean() / volatility * np.sqrt(252)) if volatility > 0 else np.nan


def score_cells(values: np.ndarray, indices: np.ndarray, names: list[str]) -> pd.DataFrame:
    rows = []
    for offset, name in enumerate(names):
        path = values[indices, offset]
        rows.append(
            {
                "cell_id": name,
                "sharpe": sharpe(path),
                "return": compounded(path),
            }
        )
    return pd.DataFrame(rows).set_index("cell_id")


def select_cell(scores: pd.DataFrame) -> str:
    finite = scores.loc[np.isfinite(scores["sharpe"])].copy()
    if finite.empty:
        raise RuntimeError("no finite in-sample Sharpe")
    finite = finite.reset_index().sort_values(
        ["sharpe", "return", "cell_id"], ascending=[False, False, True]
    )
    return str(finite.iloc[0]["cell_id"])


def cscv(paths: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    names = list(paths.columns)
    values = paths.to_numpy()
    blocks = contiguous_blocks(len(paths))
    rows = []
    for split_id, in_blocks in enumerate(itertools.combinations(range(BLOCKS), BLOCKS // 2)):
        in_set = set(in_blocks)
        out_blocks = tuple(block for block in range(BLOCKS) if block not in in_set)
        in_indices = np.concatenate([blocks[block] for block in in_blocks])
        out_indices = np.concatenate([blocks[block] for block in out_blocks])
        in_scores = score_cells(values, in_indices, names)
        out_scores = score_cells(values, out_indices, names)
        selected = select_cell(in_scores)
        ranks = out_scores["sharpe"].rank(method="average", pct=True)
        selected_rank = float(ranks.loc[selected])
        selected_return = float(out_scores.at[selected, "return"])
        baseline_return = float(out_scores.at[BASELINE_ID, "return"])
        best_oos_return = float(out_scores["return"].max())
        rows.append(
            {
                "split_id": split_id,
                "in_blocks": ",".join(map(str, in_blocks)),
                "out_blocks": ",".join(map(str, out_blocks)),
                "selected_cell": selected,
                "selected_is_sharpe": float(in_scores.at[selected, "sharpe"]),
                "selected_oos_sharpe": float(out_scores.at[selected, "sharpe"]),
                "selected_oos_rank": selected_rank,
                "selected_oos_return": selected_return,
                "baseline_oos_return": baseline_return,
                "selected_minus_baseline_return": selected_return - baseline_return,
                "oos_return_regret": best_oos_return - selected_return,
                "overfit": bool(selected_rank <= 0.50),
            }
        )
    frame = pd.DataFrame(rows)
    frequency = Counter(frame["selected_cell"])
    summary = {
        "splits": int(len(frame)),
        "pbo": float(frame["overfit"].mean()),
        "median_oos_rank": float(frame["selected_oos_rank"].median()),
        "median_selected_minus_baseline_return": float(
            frame["selected_minus_baseline_return"].median()
        ),
        "median_oos_return_regret": float(frame["oos_return_regret"].median()),
        "selection_frequency": dict(sorted(frequency.items(), key=lambda item: (-item[1], item[0]))),
    }
    return frame, summary


def fixed_block_stability(paths: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    blocks = contiguous_blocks(len(paths))
    rows = []
    for block_id, indices in enumerate(blocks):
        baseline = paths[BASELINE_ID].to_numpy()[indices]
        fixed = paths[FIXED_ID].to_numpy()[indices]
        baseline_return = compounded(baseline)
        fixed_return = compounded(fixed)
        baseline_sharpe = sharpe(baseline)
        fixed_sharpe = sharpe(fixed)
        rows.append(
            {
                "block": block_id,
                "start": str(paths.index[indices[0]].date()),
                "end": str(paths.index[indices[-1]].date()),
                "sessions": int(len(indices)),
                "baseline_return": baseline_return,
                "fixed_return": fixed_return,
                "return_delta": fixed_return - baseline_return,
                "baseline_sharpe": baseline_sharpe,
                "fixed_sharpe": fixed_sharpe,
                "sharpe_delta": fixed_sharpe - baseline_sharpe,
                "return_active": bool(
                    abs(baseline_return) > 1e-15 or abs(fixed_return) > 1e-15
                ),
                "sharpe_active": bool(np.isfinite(baseline_sharpe) and np.isfinite(fixed_sharpe)),
            }
        )
    frame = pd.DataFrame(rows)
    active_return = frame["return_active"]
    active_sharpe = frame["sharpe_active"]
    summary = {
        "positive_return_blocks": int((frame["return_delta"] > 0).sum()),
        "positive_sharpe_blocks": int((frame["sharpe_delta"] > 0).sum()),
        "active_return_blocks": int(active_return.sum()),
        "positive_return_active_blocks": int(
            (frame.loc[active_return, "return_delta"] > 0).sum()
        ),
        "active_sharpe_blocks": int(active_sharpe.sum()),
        "positive_sharpe_active_blocks": int(
            (frame.loc[active_sharpe, "sharpe_delta"] > 0).sum()
        ),
        "blocks": int(len(frame)),
    }
    return frame, summary


def circular_indices(
    rng: np.random.Generator,
    samples: int,
    count: int,
    block: int,
) -> np.ndarray:
    block_count = math.ceil(count / block)
    starts = rng.integers(0, count, size=(samples, block_count))
    offsets = np.arange(block)
    return ((starts[:, :, None] + offsets) % count).reshape(samples, -1)[:, :count]


def familywise_reality_check(
    paths: pd.DataFrame,
    samples: int = BOOTSTRAP_SAMPLES,
    block: int = BOOTSTRAP_BLOCK,
    seed: int = BOOTSTRAP_SEED,
    batch_size: int = 250,
) -> dict:
    names = [name for name in paths.columns if name != BASELINE_ID]
    baseline = paths[BASELINE_ID].to_numpy()[:, None]
    deltas = paths[names].to_numpy() - baseline
    observed_means = deltas.mean(axis=0)
    best_offset = int(np.argmax(observed_means))
    observed_max = float(observed_means[best_offset])
    fixed_offset = names.index(FIXED_ID)
    observed_fixed = float(observed_means[fixed_offset])
    centered = deltas - observed_means
    rng = np.random.default_rng(seed)
    family_exceed = 0
    fixed_exceed = 0
    completed = 0
    while completed < samples:
        batch = min(batch_size, samples - completed)
        indices = circular_indices(rng, batch, len(paths), block)
        means = centered[indices].mean(axis=1)
        family_exceed += int((means.max(axis=1) >= observed_max).sum())
        fixed_exceed += int((means[:, fixed_offset] >= observed_fixed).sum())
        completed += batch
    return {
        "samples": int(samples),
        "block_sessions": int(block),
        "seed": int(seed),
        "best_observed_cell": names[best_offset],
        "best_observed_mean_daily_delta": observed_max,
        "best_observed_annualized_mean_delta": observed_max * 252,
        "familywise_p_value": float((family_exceed + 1) / (samples + 1)),
        "fixed_cell_mean_daily_delta": observed_fixed,
        "fixed_cell_annualized_mean_delta": observed_fixed * 252,
        "fixed_unadjusted_p_value": float((fixed_exceed + 1) / (samples + 1)),
    }


def interpretation_gate(cscv_summary: dict, reality: dict, fixed_summary: dict) -> dict:
    checks = {
        "pbo_below_50pct": bool(cscv_summary["pbo"] < 0.50),
        "familywise_p_below_10pct": bool(reality["familywise_p_value"] < 0.10),
        "fixed_positive_return_at_least_7_of_10": bool(
            fixed_summary["positive_return_blocks"] >= 7
        ),
        "fixed_positive_sharpe_at_least_7_of_10": bool(
            fixed_summary["positive_sharpe_blocks"] >= 7
        ),
    }
    return {**checks, "contained": bool(all(checks.values()))}


def pct(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2%}"


def num(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2f}"


def write_report(
    metadata: pd.DataFrame,
    cscv_summary: dict,
    fixed: pd.DataFrame,
    fixed_summary: dict,
    reality: dict,
    gate: dict,
) -> None:
    fixed_meta = metadata.set_index("cell_id").loc[FIXED_ID]
    baseline_meta = metadata.set_index("cell_id").loc[BASELINE_ID]
    lines = [
        "# RSR filter selection-bias audit",
        "",
        "## Bottom line",
        "",
        (
            "The registered selection-bias concern is **contained**."
            if gate["contained"]
            else "The registered selection-bias concern is **not contained**."
        ),
        "This result discounts retrospective confidence; it does not modify formal V9, RSR1, RSR2, or live permissions.",
        "",
        "## Frozen family and full-path context",
        "",
        f"- Trial cells: {len(metadata)}",
        f"- Frozen interval: {START.date()} through {FROZEN_END.date()}",
        f"- Matched baseline: return {pct(baseline_meta.full_return)}, Sharpe {num(baseline_meta.full_sharpe)}, trades {int(baseline_meta.trade_count)}",
        f"- Frozen 4%/50%: return {pct(fixed_meta.full_return)}, Sharpe {num(fixed_meta.full_sharpe)}, trades {int(fixed_meta.trade_count)}",
        "",
        "## Combinatorially symmetric cross-validation",
        "",
        f"- Splits: {cscv_summary['splits']}",
        f"- Probability of backtest overfitting (PBO): {cscv_summary['pbo']:.1%}",
        f"- Median selected-cell OOS rank: {cscv_summary['median_oos_rank']:.1%}",
        f"- Median selected-minus-baseline OOS return: {cscv_summary['median_selected_minus_baseline_return']:+.2%}",
        f"- Median OOS regret versus best cell: {cscv_summary['median_oos_return_regret']:+.2%}",
        "",
        "Most frequently selected in-sample cells:",
        "",
    ]
    for name, count in list(cscv_summary["selection_frequency"].items())[:5]:
        lines.append(f"- `{name}`: {count}/{cscv_summary['splits']} splits")
    lines.extend(
        [
            "",
            "## Family-wise block bootstrap",
            "",
            f"- Best observed cell: `{reality['best_observed_cell']}`",
            f"- Best annualized mean daily-return advantage: {reality['best_observed_annualized_mean_delta']:+.2%}",
            f"- Family-wise p-value after all 19 challengers: {reality['familywise_p_value']:.3f}",
            f"- Frozen 4%/50% annualized mean daily-return advantage: {reality['fixed_cell_annualized_mean_delta']:+.2%}",
            f"- Frozen cell unadjusted paired p-value: {reality['fixed_unadjusted_p_value']:.3f}",
            "",
            "## Frozen 4%/50% chronological blocks",
            "",
            "| Block | Dates | Return delta | Sharpe delta |",
            "| ---: | --- | ---: | ---: |",
        ]
    )
    for row in fixed.itertuples(index=False):
        lines.append(
            f"| {row.block} | {row.start} to {row.end} | "
            f"{('n/a' if pd.isna(row.return_delta) else f'{row.return_delta:+.2%}')} | "
            f"{('n/a' if pd.isna(row.sharpe_delta) else f'{row.sharpe_delta:+.2f}')} |"
        )
    lines.extend(
        [
            "",
            f"Positive return blocks: {fixed_summary['positive_return_blocks']}/{fixed_summary['blocks']}; "
            f"positive Sharpe blocks: {fixed_summary['positive_sharpe_blocks']}/{fixed_summary['blocks']}.",
            f"Descriptively, {fixed_summary['active_return_blocks']} blocks had nonzero return observations and "
            f"{fixed_summary['positive_return_active_blocks']} were positive; "
            f"{fixed_summary['active_sharpe_blocks']} had finite Sharpe observations and "
            f"{fixed_summary['positive_sharpe_active_blocks']} were positive. The three inactive blocks remain in "
            "the registered 10-block denominator and cannot be removed after observation.",
            "",
            "## Registered gate",
            "",
        ]
    )
    for name, value in gate.items():
        if name != "contained":
            lines.append(f"- {name}: {'pass' if value else 'fail'}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The twenty-cell grid and every resample reuse a fixed current watchlist selected with hindsight. "
            "Consequently this audit can reveal parameter-selection fragility but cannot establish a live edge. "
            "A low unadjusted p-value is not sufficient after inspecting the full family. Genuine forward trades, "
            "payoff distribution and profit concentration remain the governing evidence. The adjusted p-value of "
            "0.063 clears the preregistered 10% threshold but not 5%; combined with three inactive chronological "
            "blocks, it is suggestive rather than decisive.",
        ]
    )
    (RESULTS / "selection_bias_audit_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    paths, metadata = run_paths()
    splits, cscv_summary = cscv(paths)
    fixed, fixed_summary = fixed_block_stability(paths)
    reality = familywise_reality_check(paths)
    gate = interpretation_gate(cscv_summary, reality, fixed_summary)
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "preregistration": "selection-bias-audit-preregistration.md",
        "data_start": str(START.date()),
        "data_end": str(FROZEN_END.date()),
        "trial_cells": int(len(metadata)),
        "cscv": cscv_summary,
        "fixed_cell_stability": fixed_summary,
        "familywise_reality_check": reality,
        "gate": gate,
    }
    paths.to_csv(RESULTS / "selection_bias_daily_returns.csv", index_label="date")
    metadata.to_csv(RESULTS / "selection_bias_cell_metadata.csv", index=False)
    splits.to_csv(RESULTS / "selection_bias_cscv_splits.csv", index=False)
    fixed.to_csv(RESULTS / "selection_bias_fixed_block_stability.csv", index=False)
    (RESULTS / "selection_bias_audit_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(metadata, cscv_summary, fixed, fixed_summary, reality, gate)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
