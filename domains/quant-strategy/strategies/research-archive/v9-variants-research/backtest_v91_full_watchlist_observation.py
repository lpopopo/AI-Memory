#!/usr/bin/env python3
"""Technical-observation replay for every formal user-selected stock.

This report never creates trades for symbols lacking a point-in-time V9 event.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd

SCRIPTS=Path(__file__).resolve().parent;ROOT=SCRIPTS.parent;sys.path.insert(0,str(SCRIPTS))
from validate_v9_information_strategy import load_data
from v9_information_strategy import V9Backtester,V9Config,load_event_store,load_evidence_store

START="2026-05-01"

def main():
    watch=json.loads((ROOT.parents[1]/"references/user-selected-watchlist.json").read_text(encoding="utf-8"))["tickers"]
    panels,vix,meta=load_data();events,_=load_event_store(ROOT/"datasets/v9_information_events.json");updates,_=load_evidence_store(ROOT/"datasets/v9_evidence_updates.json")
    engine=V9Backtester(panels,vix,events,V9Config(tech_path_mode="any"),updates);close=panels["close"]
    dates=close.loc[START:].index;latest=dates[-1];event_symbols={s for e in events if e.point_in_time_eligible for s in e.symbols}
    rows=[]
    for item in watch:
        s,theme=item["symbol"],item["theme"]
        if s not in close.columns:
            rows.append({"symbol":s,"theme":theme,"coverage":"missing_price_data"});continue
        valid=breakout=trend=pullback=chased=0
        for dt in dates:
            ok,path,_,reason,high_vol=engine._tech_setup(s,dt)
            valid+=int(ok); breakout+=int(ok and path=="breakout"); trend+=int(ok and path=="trend"); pullback+=int(ok and path=="pullback"); chased+=int(high_vol)
        ok,path,score,reason,high_vol=engine._tech_setup(s,latest)
        px=float(close.at[latest,s]);ma20=float(engine.ma20.at[latest,s]);ma50=float(engine.ma50.at[latest,s]);ma200=float(engine.ma200.at[latest,s]);rs=float(engine.rs20.at[latest,s])
        rows.append({"symbol":s,"theme":theme,"coverage":"covered","has_point_in_time_event":s in event_symbols,"technical_valid_days":valid,"breakout_days":breakout,"pullback_days":pullback,"trend_days":trend,"chased_days":chased,"latest_close":px,"latest_ma20":ma20,"latest_ma50":ma50,"latest_ma200":ma200,"latest_rs20_vs_qqq":rs,"latest_technical_valid":ok,"latest_path":path,"latest_reason":reason,"latest_chased":high_vol,"v9_status":"event_and_technical_candidate" if ok and s in event_symbols else "technical_only_no_event" if ok else "not_technically_confirmed"})
    frame=pd.DataFrame(rows).sort_values(["coverage","technical_valid_days","symbol"],ascending=[True,False,True])
    out=ROOT/"results";frame.to_csv(out/"v91_full_watchlist_observation.csv",index=False)
    summary={"status":"observation_only_no_orders","period":[START,str(latest.date())],"watchlist_count":len(watch),"covered_count":int((frame.coverage=="covered").sum()),"missing_price_data":frame.loc[frame.coverage!="covered","symbol"].tolist(),"point_in_time_event_names":int(frame.get("has_point_in_time_event",pd.Series(dtype=bool)).fillna(False).sum()),"latest_technical_valid_names":frame.loc[(frame.coverage=="covered") & frame.latest_technical_valid,"symbol"].tolist(),"event_and_technical_candidates":frame.loc[(frame.coverage=="covered") & frame.has_point_in_time_event & frame.latest_technical_valid,"symbol"].tolist(),"data_last_date":meta["last_date"]}
    (out/"v91_full_watchlist_observation_metrics.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# V9.1 全自选技术观察回测","",f"区间：{START} 至 {latest.date()}。全体自选股均进入技术观察；无点时资讯的股票不产生 V9 交易授权。","",f"- 覆盖：{summary['covered_count']}/{len(watch)}","- 缺失行情："+(", ".join(summary["missing_price_data"]) or "无"),"- 最新技术确认："+(", ".join(summary["latest_technical_valid_names"]) or "无"),"- 同时具备点时资讯与技术确认："+(", ".join(summary["event_and_technical_candidates"]) or "无"),"","详表：`v91_full_watchlist_observation.csv`。"]
    (out/"v91_full_watchlist_observation_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
