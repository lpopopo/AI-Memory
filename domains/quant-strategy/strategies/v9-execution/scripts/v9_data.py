"""Shared completed-bar data loader for the V9 execution workflow."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_data():
    data_dir = ROOT / "datasets" / "data_v9"
    panels = {
        key: pd.read_csv(data_dir / f"{key}.csv", index_col=0, parse_dates=True).sort_index()
        for key in ("open", "high", "low", "close", "volume")
    }
    core_index = panels["close"][["SPY", "QQQ"]].dropna().index
    vix = panels["close"][["^VIX", "^VIX3M"]].reindex(core_index).ffill()
    symbols = [symbol for symbol in panels["close"] if not symbol.startswith("^VIX")]
    panels = {key: panel.reindex(core_index)[symbols] for key, panel in panels.items()}
    metadata = json.loads((data_dir / "metadata.json").read_text(encoding="utf-8"))
    return panels, vix, metadata
