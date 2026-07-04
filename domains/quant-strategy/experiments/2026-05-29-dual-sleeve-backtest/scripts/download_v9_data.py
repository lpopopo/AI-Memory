#!/usr/bin/env python3
from pathlib import Path
import json,pandas as pd,yfinance as yf
ROOT=Path(__file__).resolve().parents[1];EVENTS=ROOT/"datasets/v9_information_events.json";OUT=ROOT/"datasets/data_v9"
def main():
 raw=json.loads(EVENTS.read_text());symbols=sorted({s for e in raw["events"] for s in e["symbols"]}|{"SPY","QQQ","^VIX","^VIX3M"});OUT.mkdir(parents=True,exist_ok=True)
 data=yf.download(symbols,start="2024-01-01",end=None,auto_adjust=True,progress=False,threads=True)
 for field in ("Open","High","Low","Close","Volume"):
  frame=data[field] if isinstance(data.columns,pd.MultiIndex) else data[[field]];frame.index=pd.to_datetime(frame.index).tz_localize(None);frame.to_csv(OUT/f"{field.lower()}.csv",index_label="Date")
 meta={"source":"Yahoo Finance via yfinance auto_adjust=True","symbols":symbols,"downloaded_at_utc":pd.Timestamp.now(tz="UTC").isoformat(),"last_date":str(frame.index[-1].date())};(OUT/"metadata.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2));print(meta)
if __name__=="__main__":main()
