#!/usr/bin/env python3
from pathlib import Path
import argparse,json,pandas as pd,yfinance as yf
ROOT=Path(__file__).resolve().parents[1];EVENTS=ROOT/"datasets/v9_information_events.json";OUT=ROOT/"datasets/data_v9"
# Fear Gate advisory breadth/credit proxies used by v9_research_monitors only.
DIAGNOSTIC_SYMBOLS={"SMH","IWM","RSP","HYG","LQD"}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--events-only",action="store_true",help="exclude the formal user-selected watchlist");args=ap.parse_args()
 raw=json.loads(EVENTS.read_text(encoding="utf-8"));event_symbols={s for e in raw["events"] for s in e["symbols"]}
 watchlist_path=ROOT.parents[1]/"references/user-selected-watchlist.json"
 watchlist=set() if args.events_only else {x["symbol"] for x in json.loads(watchlist_path.read_text(encoding="utf-8"))["tickers"]}
 symbols=sorted(event_symbols|watchlist|DIAGNOSTIC_SYMBOLS|{"SPY","QQQ","^VIX","^VIX3M"});OUT.mkdir(parents=True,exist_ok=True)
 print(f"Downloading {len(symbols)} symbols individually...")
 dfs = {f: pd.DataFrame() for f in ("Open","High","Low","Close","Volume")}
 for s in symbols:
  try:
   data=yf.download(s,start="2024-01-01",end=None,auto_adjust=True,progress=False)
   if data.empty:
    print(f"Skipping {s}: No data returned")
    continue
   for field in ("Open","High","Low","Close","Volume"):
    # If MultiIndex or single column
    col = data[field] if isinstance(data.columns, pd.MultiIndex) else data[[field]]
    # Ensure it's a Series
    if isinstance(col, pd.DataFrame):
     col = col.iloc[:, 0]
    dfs[field][s] = col
   print(f"Successfully downloaded {s}")
  except Exception as e:
   print(f"Error downloading {s}: {e}")

 for field in ("Open","High","Low","Close","Volume"):
  frame = dfs[field]
  frame.index = pd.to_datetime(frame.index).tz_localize(None)
  frame.to_csv(OUT/f"{field.lower()}.csv",index_label="Date")
 meta={"source":"Yahoo Finance via yfinance auto_adjust=True","symbols":list(dfs["Close"].columns),"event_symbols":sorted(event_symbols),"user_watchlist_symbols":sorted(watchlist),"downloaded_at_utc":pd.Timestamp.now(tz="UTC").isoformat(),"last_date":str(frame.index[-1].date())};(OUT/"metadata.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8");print(meta)
if __name__=="__main__":main()
