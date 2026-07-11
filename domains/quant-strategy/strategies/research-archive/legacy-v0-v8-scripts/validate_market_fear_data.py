#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))

from market_fear import MARKET_TICKERS, RESULTS_DIR, compute_fear, download_market_data, pct


CORE_COLUMNS = ["SPY", "QQQ", "SMH", "^VIX", "^VIX3M"]
OPTIONAL_COLUMNS = ["IWM", "RSP", "HYG", "LQD", "TLT"]


def status(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def validate_close(close: pd.DataFrame) -> tuple[list[dict], list[str]]:
    checks = []
    warnings = []

    checks.append(
        {
            "check": "non_empty_dataset",
            "status": status(not close.empty),
            "detail": f"{len(close)} rows, {len(close.columns)} columns",
        }
    )

    for col in CORE_COLUMNS:
        exists = col in close.columns
        non_na = int(close[col].notna().sum()) if exists else 0
        ok = exists and non_na >= 200
        checks.append(
            {
                "check": f"core_column_{col}",
                "status": status(ok),
                "detail": f"exists={exists}, non_na_rows={non_na}",
            }
        )

    for col in OPTIONAL_COLUMNS:
        exists = col in close.columns
        non_na = int(close[col].notna().sum()) if exists else 0
        ok = exists and non_na >= 100
        checks.append(
            {
                "check": f"optional_column_{col}",
                "status": status(ok),
                "detail": f"exists={exists}, non_na_rows={non_na}",
            }
        )
        if not ok:
            warnings.append(f"Optional market fear column `{col}` is weak or missing.")

    latest = close.dropna(how="all").iloc[-1]
    sanity_rules = [
        ("SPY", 50, 2000),
        ("QQQ", 50, 2000),
        ("SMH", 10, 2000),
        ("^VIX", 5, 100),
        ("^VIX3M", 5, 100),
    ]
    for col, low, high in sanity_rules:
        value = latest.get(col)
        ok = pd.notna(value) and low <= float(value) <= high
        checks.append(
            {
                "check": f"latest_value_sanity_{col}",
                "status": status(ok),
                "detail": "n/a" if pd.isna(value) else f"{float(value):.4f} in [{low}, {high}]",
            }
        )

    return checks, warnings


def write_report(close: pd.DataFrame, checks: list[dict], warnings: list[str]) -> Path:
    result = compute_fear(close)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RESULTS_DIR / "market_fear_data_validation.md"
    json_path = RESULTS_DIR / "market_fear_data_validation.json"

    payload = {
        "tickers_requested": MARKET_TICKERS,
        "start": close.index[0].strftime("%Y-%m-%d"),
        "end": close.index[-1].strftime("%Y-%m-%d"),
        "rows": len(close),
        "columns": list(close.columns),
        "checks": checks,
        "warnings": warnings,
        "fear_result": {
            "as_of": result.as_of,
            "score": result.score,
            "regime": result.regime,
            "risk_multiplier": result.risk_multiplier,
            "cash_floor": result.cash_floor,
        },
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Market Fear Data Validation",
        "",
        f"- Data range: `{payload['start']}` to `{payload['end']}`",
        f"- Rows: `{payload['rows']}`",
        f"- Columns returned: `{', '.join(payload['columns'])}`",
        f"- Latest regime: `{result.regime}`",
        f"- Latest score: `{result.score}`",
        f"- Risk multiplier: `{result.risk_multiplier:.0%}`",
        f"- Cash floor: `{result.cash_floor:.0%}`",
        "",
        "## Checks",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check['check']} | {check['status']} | {check['detail']} |")

    lines.extend(["", "## Latest Fear Signals", "", "| Signal | Value | Points | Note |", "| --- | ---: | ---: | --- |"])
    for signal in result.signals:
        value = pct(signal.value) if "change" in signal.name or "drawdown" in signal.name or "21d" in signal.name else ("n/a" if signal.value is None else f"{signal.value:.2f}")
        lines.append(f"| {signal.name} | {value} | {signal.points} | {signal.note} |")

    if warnings:
        lines.extend(["", "## Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.extend(["", "## Warnings", "", "- None."])

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    close = download_market_data(start="2025-01-01", end="2026-05-30")
    checks, warnings = validate_close(close)
    report_path = write_report(close, checks, warnings)
    failed = [check for check in checks if check["status"] == "FAIL" and check["check"].startswith("core_")]
    print(f"Wrote {report_path}")
    if failed:
        raise SystemExit(f"core market fear validation failed: {failed}")


if __name__ == "__main__":
    main()
