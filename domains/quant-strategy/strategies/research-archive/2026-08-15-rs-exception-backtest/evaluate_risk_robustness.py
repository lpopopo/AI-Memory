#!/usr/bin/env python3
"""Evaluate top training-selected risk filters on the common 2026 test interval."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
CONFIG_FIELDS = tuple(MODULE["Config"].__dataclass_fields__)
INTEGER_FIELDS = {"max_hold_days", "breadth_count_min"}


def config_from_row(row: pd.Series):
    values = {}
    for field in CONFIG_FIELDS:
        value = row[field]
        values[field] = int(value) if field in INTEGER_FIELDS else float(value)
    return MODULE["Config"](**values)


def main() -> None:
    grid = pd.read_csv(RESULTS / "train_risk_parameter_grid.csv").head(20)
    panels, symbols = MODULE["load_panels"]()
    default = MODULE["simulate"](
        panels, symbols, MODULE["Config"](), "strict_veto", "2026-01-01", "2026-08-07"
    )["metrics"]
    rows = []
    for rank, (_, row) in enumerate(grid.iterrows(), start=1):
        cfg = config_from_row(row)
        metrics = MODULE["simulate"](
            panels, symbols, cfg, "strict_veto", "2026-01-01", "2026-08-07"
        )["metrics"]
        rows.append({
            "train_rank": rank,
            **{field: getattr(cfg, field) for field in CONFIG_FIELDS},
            **metrics,
            "return_delta_vs_default": metrics["total_return"] - default["total_return"],
            "drawdown_delta_vs_default": metrics["max_drawdown"] - default["max_drawdown"],
            "sharpe_delta_vs_default": metrics["sharpe"] - default["sharpe"],
            "win_rate_delta_vs_default": (
                metrics["win_rate"] - default["win_rate"] if metrics["win_rate"] is not None else np.nan
            ),
        })
    frame = pd.DataFrame(rows)
    frame.to_csv(RESULTS / "top20_risk_2026_test.csv", index=False)
    summary = {
        "tested_training_ranks": 20,
        "default_2026": default,
        "share_positive_return_delta": float((frame["return_delta_vs_default"] > 0).mean()),
        "share_nonworse_drawdown": float((frame["drawdown_delta_vs_default"] >= 0).mean()),
        "share_positive_sharpe_delta": float((frame["sharpe_delta_vs_default"] > 0).mean()),
        "share_nonworse_win_rate": float((frame["win_rate_delta_vs_default"] >= 0).mean()),
        "median_return_delta": float(frame["return_delta_vs_default"].median()),
        "median_drawdown_delta": float(frame["drawdown_delta_vs_default"].median()),
        "median_sharpe_delta": float(frame["sharpe_delta_vs_default"].median()),
        "median_win_rate_delta": float(frame["win_rate_delta_vs_default"].median()),
        "median_trade_count": float(frame["trade_count"].median()),
        "status": "robustness_diagnostic_only; post_hoc and not fresh OOS",
    }
    (RESULTS / "risk_robustness.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Risk-Filter Robustness Diagnostic",
        "",
        "Top 20 configurations were selected using 2024-2025 only, then evaluated on the common 2026 interval.",
        "The ATR hypothesis itself was defined after inspecting 2026 failures, so this is not fresh OOS evidence.",
        "",
        f"- Positive return delta: `{summary['share_positive_return_delta']:.0%}`",
        f"- Non-worse drawdown: `{summary['share_nonworse_drawdown']:.0%}`",
        f"- Positive Sharpe delta: `{summary['share_positive_sharpe_delta']:.0%}`",
        f"- Non-worse win rate: `{summary['share_nonworse_win_rate']:.0%}`",
        f"- Median return delta: `{summary['median_return_delta']:+.2%}`",
        f"- Median drawdown delta: `{summary['median_drawdown_delta']:+.2%}`",
        f"- Median Sharpe delta: `{summary['median_sharpe_delta']:+.2f}`",
        f"- Median win-rate delta: `{summary['median_win_rate_delta']:+.2%}`",
        f"- Median trades: `{summary['median_trade_count']:.1f}`",
        "",
        "This diagnostic can nominate a forward-shadow filter but cannot promote it.",
    ]
    (RESULTS / "risk_robustness.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
