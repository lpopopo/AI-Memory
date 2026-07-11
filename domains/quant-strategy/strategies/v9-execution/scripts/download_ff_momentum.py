#!/usr/bin/env python3
"""Download Ken French momentum factor files into datasets/data_factor."""
from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "datasets" / "data_factor"
DAILY_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily_CSV.zip"
MONTHLY_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip"


def _read_french_csv(raw: bytes) -> pd.DataFrame:
    text = raw.decode("latin-1")
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() and line.strip()[0].isdigit())
    header_idx = start - 1 if start > 0 else start
    end = next(
        (i for i, line in enumerate(lines[start:], start) if not line.strip() or line.lower().startswith("annual")),
        len(lines),
    )
    block = "\n".join(lines[header_idx:end])
    frame = pd.read_csv(io.StringIO(block))
    # Keep the first column as the date even if unnamed; drop other padding columns.
    keep = [frame.columns[0]] + [c for c in frame.columns[1:] if not str(c).startswith("Unnamed")]
    frame = frame.loc[:, keep]
    date_col = frame.columns[0]
    frame = frame.rename(columns={date_col: "date"})
    date_values = frame["date"].astype(str).str.strip()
    parsed = pd.to_datetime(date_values, format="%Y%m%d", errors="coerce")
    if parsed.isna().all():
        parsed = pd.to_datetime(date_values, format="%Y%m", errors="coerce")
    frame["date"] = parsed
    frame = frame.dropna(subset=["date"]).set_index("date").sort_index()
    frame.columns = [str(c).strip().replace(" ", "") for c in frame.columns]
    for column in frame.columns:
        values = pd.to_numeric(frame[column], errors="coerce")
        values = values.mask(values <= -99.0)
        frame[column] = values / 100.0
    return frame


def _momentum_column(frame: pd.DataFrame) -> str:
    for column in frame.columns:
        normalized = column.lower().replace("-", "")
        if "mom" in normalized or normalized == "umd":
            return column
    raise KeyError(f"momentum column not found in {list(frame.columns)}")


def download_zip_csv(url: str) -> pd.DataFrame:
    with urlopen(url, timeout=60) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        name = next(n for n in archive.namelist() if n.lower().endswith(".csv"))
        return _read_french_csv(archive.read(name))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--monthly-only", action="store_true")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {"source": "Ken French Data Library", "files": {}}
    if not args.monthly_only:
        daily = download_zip_csv(DAILY_URL)
        mom_col = _momentum_column(daily)
        daily_path = OUT_DIR / "ff_mom_daily.csv"
        daily.to_csv(daily_path)
        wml = daily[[mom_col]].rename(columns={mom_col: "WML"})
        legs_path = OUT_DIR / "ff_wml_daily.csv"
        wml.to_csv(legs_path)
        manifest["files"]["ff_mom_daily.csv"] = {
            "rows": int(len(daily)),
            "start": str(daily.index.min().date()),
            "end": str(daily.index.max().date()),
            "columns": list(daily.columns),
        }
        manifest["files"]["ff_wml_daily.csv"] = {
            "rows": int(len(wml)),
            "start": str(wml.index.min().date()),
            "end": str(wml.index.max().date()),
            "columns": ["WML"],
            "note": "Winner/loser legs require CRSP reconstruction; WML only is stored here.",
        }

    monthly = download_zip_csv(MONTHLY_URL)
    monthly_path = OUT_DIR / "ff_mom_monthly.csv"
    monthly.to_csv(monthly_path)
    manifest["files"]["ff_mom_monthly.csv"] = {
        "rows": int(len(monthly)),
        "start": str(monthly.index.min().date()),
        "end": str(monthly.index.max().date()),
        "columns": list(monthly.columns),
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(OUT_DIR), "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
