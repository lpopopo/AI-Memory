#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_LONG_DIR = ROOT / "datasets" / "data_long"
cache_path = DATA_LONG_DIR / "yfinance_adjusted_close_2000_2025.csv"

def main():
    if not cache_path.exists():
        print(f"ERROR: Dataset file does not exist: {cache_path}")
        return

    print("Loading dataset...")
    df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
    
    print("\n================ DATASET INTEGRITY REPORT ================")
    print(f"Total Trading Days: {len(df)}")
    print(f"Start Date:         {df.index[0].strftime('%Y-%m-%d')}")
    print(f"End Date:           {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"Total Symbols:      {len(df.columns)}")
    
    # Sort columns by their date of first non-NaN data to verify IPO/launch date alignment
    reports = []
    for col in sorted(df.columns):
        series = df[col].dropna()
        total_valid = len(series)
        nan_count = len(df) - total_valid
        completeness = total_valid / len(df)
        
        first_date = series.index[0].strftime('%Y-%m-%d') if total_valid > 0 else "N/A"
        last_date = series.index[-1].strftime('%Y-%m-%d') if total_valid > 0 else "N/A"
        
        reports.append({
            "Symbol": col,
            "Valid Days": total_valid,
            "NaN Days": nan_count,
            "Completeness": f"{completeness:.2%}",
            "First Date": first_date,
            "Last Date": last_date
        })
        
    report_df = pd.DataFrame(reports)
    print("\nFirst 15 Symbols (Sorted Alphabetically):")
    print(report_df.head(15).to_string(index=False))
    
    print("\nLast 15 Symbols (Sorted Alphabetically):")
    print(report_df.tail(15).to_string(index=False))
    
    # Check essential benchmarks SPY & QQQ
    print("\n================ ESSENTIAL BENCHMARK STATUS ================")
    for b in ["SPY", "QQQ"]:
        if b in df.columns:
            b_valid = df[b].dropna()
            print(f"{b}: Completeness = {len(b_valid)/len(df):.2%}, Valid Days = {len(b_valid)}, First Date = {b_valid.index[0].strftime('%Y-%m-%d')}, Last Date = {b_valid.index[-1].strftime('%Y-%m-%d')}")
        else:
            print(f"CRITICAL ERROR: {b} column is missing from the dataset!")
            
    print("==========================================================")

if __name__ == "__main__":
    main()
