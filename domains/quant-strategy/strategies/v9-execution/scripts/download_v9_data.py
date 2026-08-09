#!/usr/bin/env python3
"""Refresh completed V9 daily bars without destroying a usable cache on failure."""
from pathlib import Path
import argparse,json,pandas as pd,yfinance as yf
ROOT=Path(__file__).resolve().parents[1];EVENTS=ROOT/"datasets/v9_information_events.json";OUT=ROOT/"datasets/data_v9"
# Fear Gate advisory breadth/credit proxies used by v9_research_monitors only.
DIAGNOSTIC_SYMBOLS={"SMH","IWM","RSP","HYG","LQD"}
FIELDS=("Open","High","Low","Close","Volume")
REQUIRED_MARKET_SYMBOLS={"SPY","QQQ","SMH","IWM","RSP","HYG","LQD","^VIX","^VIX3M"}
CBOE_HISTORY_URLS={
 "^VIX":"https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
 "^VIX3M":"https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv",
}

def load_cache()->dict[str,pd.DataFrame]:
 cached={}
 for field in FIELDS:
  path=OUT/f"{field.lower()}.csv"
  cached[field]=pd.read_csv(path,index_col=0,parse_dates=True).sort_index() if path.exists() else pd.DataFrame()
 return cached

def series_from_download(data:pd.DataFrame,field:str)->pd.Series:
 col=data[field] if isinstance(data.columns,pd.MultiIndex) else data[[field]]
 if isinstance(col,pd.DataFrame):col=col.iloc[:,0]
 col.index=pd.to_datetime(col.index).tz_localize(None)
 return col.dropna()

def parse_cboe_history(data:pd.DataFrame,completed_through:pd.Timestamp)->pd.DataFrame:
 normalized=data.rename(columns={column:str(column).strip().upper() for column in data.columns})
 if "DATE" not in normalized.columns or "CLOSE" not in normalized.columns:
  raise ValueError("Cboe history must contain DATE and CLOSE columns")
 normalized.index=pd.to_datetime(normalized.pop("DATE"),errors="coerce")
 normalized=normalized.loc[normalized.index.notna()]
 parsed=pd.DataFrame(index=normalized.index)
 for field in ("OPEN","HIGH","LOW","CLOSE"):
  if field in normalized:parsed[field.title()]=pd.to_numeric(normalized[field],errors="coerce")
 return parsed.sort_index().loc[:completed_through].dropna(how="all")

def apply_cboe_history(dfs:dict[str,pd.DataFrame],source_status:dict,completed_through:pd.Timestamp)->None:
 for symbol,url in CBOE_HISTORY_URLS.items():
  prior=dict(source_status.get(symbol,{}))
  try:
   official=parse_cboe_history(pd.read_csv(url),completed_through)
   if official.empty or official["Close"].dropna().empty:
    raise RuntimeError("no official close data returned")
   for field in official.columns:
    existing=dfs[field][symbol] if symbol in dfs[field] else pd.Series(dtype=float)
    merged=existing.reindex(existing.index.union(official.index))
    merged.update(official[field])
    dfs[field]=dfs[field].reindex(dfs[field].index.union(merged.index))
    dfs[field][symbol]=merged
   source_status[symbol]={
    "source":"Cboe official daily price history",
    "status":"official_override",
    "url":url,
    "last_date":str(official["Close"].dropna().index[-1].date()),
    "prior_source_status":prior,
   }
   print(f"Applied official Cboe history for {symbol}")
  except Exception as error:
   prior["cboe_official_error"]=str(error)
   source_status[symbol]=prior
   print(f"Cboe official history unavailable for {symbol}: {error}")

def validate_required_close(close:pd.DataFrame,completed_through:pd.Timestamp)->None:
 missing=sorted(REQUIRED_MARKET_SYMBOLS-set(close.columns))
 stale=sorted(symbol for symbol in REQUIRED_MARKET_SYMBOLS if symbol in close and (close[symbol].dropna().empty or close[symbol].dropna().index[-1]<completed_through))
 if missing or stale:raise RuntimeError(f"required market data incomplete; missing={missing}, stale={stale}")

def atomic_write_csv(frame:pd.DataFrame,path:Path)->None:
 temporary=path.with_suffix(path.suffix+".tmp")
 frame.to_csv(temporary,index_label="Date");temporary.replace(path)

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--events-only",action="store_true",help="exclude the formal user-selected watchlist");ap.add_argument("--completed-through",required=True,help="last completed U.S. session, YYYY-MM-DD");ap.add_argument("--no-write",action="store_true");args=ap.parse_args();completed_through=pd.Timestamp(args.completed_through).normalize()
 raw=json.loads(EVENTS.read_text(encoding="utf-8"));event_symbols={s for e in raw["events"] for s in e["symbols"]}
 watchlist_path=ROOT.parents[1]/"references/user-selected-watchlist.json"
 watchlist=set() if args.events_only else {x["symbol"] for x in json.loads(watchlist_path.read_text(encoding="utf-8"))["tickers"]}
 symbols=sorted(event_symbols|watchlist|DIAGNOSTIC_SYMBOLS|{"SPY","QQQ","^VIX","^VIX3M"});OUT.mkdir(parents=True,exist_ok=True);cached=load_cache()
 print(f"Downloading {len(symbols)} symbols individually...")
 dfs={field:pd.DataFrame() for field in FIELDS};source_status={}
 for s in symbols:
  try:
   data=yf.download(s,start="2024-01-01",end=(completed_through+pd.Timedelta(days=1)).strftime("%Y-%m-%d"),auto_adjust=True,progress=False,threads=False)
   if data.empty:
    raise RuntimeError("no data returned")
   for field in FIELDS:dfs[field][s]=series_from_download(data,field).loc[:completed_through]
   source_status[s]={"source":"Yahoo Finance via yfinance auto_adjust=True","status":"downloaded","last_date":str(dfs["Close"][s].dropna().index[-1].date())}
   print(f"Successfully downloaded {s}")
  except Exception as e:
   if all(s in cached[field].columns for field in FIELDS):
    for field in FIELDS:dfs[field][s]=cached[field][s].loc[:completed_through]
    last=dfs["Close"][s].dropna().index[-1] if not dfs["Close"][s].dropna().empty else None;source_status[s]={"source":"existing local cache","status":"cached_fallback","error":str(e),"last_date":str(last.date()) if last is not None else None};print(f"Using cached fallback for {s}: {e}")
   else:source_status[s]={"source":None,"status":"failed","error":str(e),"last_date":None};print(f"Error downloading {s}: {e}")

 apply_cboe_history(dfs,source_status,completed_through)
 validate_required_close(dfs["Close"],completed_through)
 core_index=dfs["Close"][["SPY","QQQ"]].dropna().index;last_date=core_index[-1]
 if last_date!=completed_through:raise RuntimeError(f"core data ends at {last_date.date()}, expected {completed_through.date()}")
 meta={"source":"Yahoo Finance via yfinance auto_adjust=True with local-cache fallback; Cboe official history for volatility indices","symbols":list(dfs["Close"].columns),"event_symbols":sorted(event_symbols),"user_watchlist_symbols":sorted(watchlist),"downloaded_at_utc":pd.Timestamp.now(tz="UTC").isoformat(),"completed_through":str(completed_through.date()),"last_date":str(last_date.date()),"symbol_status":source_status}
 if not args.no_write:
  for field in FIELDS:atomic_write_csv(dfs[field].sort_index(),OUT/f"{field.lower()}.csv")
  temporary=OUT/"metadata.json.tmp";temporary.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8");temporary.replace(OUT/"metadata.json")
 print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
