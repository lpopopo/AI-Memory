#!/usr/bin/env python3
"""Timestamp-aware replay of Kay/美研芒格君 June 2026 themes."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"datasets/data_xhs_replay_2026_06/adjusted_close.csv";RESULTS=ROOT/"results"
EVENTS=[
 ("MRVL叙事与拥挤提示","2026-06-03",["MRVL"],"利润保护，不新增追涨"),
 ("AI瓶颈候选篮子","2026-06-22",["TER","CRDO","MXL","AXTI","TTMI"],"仅条件触发；MXL禁止高于92追入，TTMI允许220突破确认"),
 ("CRDO互联长文","2026-06-24",["CRDO"],"研究队列，不因文章直接买入"),
 ("存储层级/HBM-DDR-NAND-HDD","2026-06-25",["MU","WDC","STX","SNDK"],"主题拥挤且组合重叠，禁止追涨"),
 ("ALAB/MRVL/CRDO互联分层","2026-06-26",["ALAB","MRVL","CRDO"],"候选研究，需订单、收入、估值和价格确认"),
 ("HBM上游设备链","2026-06-26",["AMAT","LRCX","KLAC","ASML"],"二手传导待公司一手证据，不直接交易"),
]
def main():
 c=pd.read_csv(DATA,index_col=0,parse_dates=True).sort_index();end=pd.Timestamp("2026-07-02");rows=[]
 for name,date,syms,rule in EVENTS:
  dt=pd.Timestamp(date);window=c.loc[dt:end];base=window.iloc[0];r=window[syms].div(base[syms]).sub(1);basket=r.mean(axis=1);q=window.QQQ/base.QQQ-1
  rows.append({"idea":name,"anchor":date,"symbols":syms,"strategy_rule":rule,"return_to_2026_07_02":float(basket.iloc[-1]),"excess_vs_qqq":float((basket-q).iloc[-1]),"max_drawdown":float((1+basket).div((1+basket).cummax()).sub(1).min()),"five_session_return":float(basket.iloc[5]) if len(basket)>5 else None,"constituent_returns":{s:float(c.at[end,s]/base[s]-1) for s in syms}})
 # TTMI false-breakout replay: June 22 close confirms >220, next-close proxy entry, hard exit after <188 close.
 ttmi={"signal_close":"2026-06-22","proxy_entry_close":"2026-06-23","entry":float(c.at[pd.Timestamp('2026-06-23'),'TTMI']),"stop_confirmation_close":"2026-06-29","proxy_exit_close":"2026-06-30","exit":float(c.at[pd.Timestamp('2026-06-30'),'TTMI'])}
 ttmi["stopped_return"]=ttmi["exit"]/ttmi["entry"]-1;ttmi["hold_to_july2_return"]=float(c.at[end,'TTMI']/ttmi["entry"]-1)
 out={"method":{"source":"Yahoo Finance adjusted close cache","end":"2026-07-02","event_anchor":"first actionable completed close on/after timestamped local evidence","lookahead":False,"limitations":["Later June ideas have fewer than five sessions of evidence.","Theme baskets are equal weighted and are not claimed as executable portfolios.","Xiaohongshu items without reliable timestamps are excluded or anchored to first verified local visibility."]},"events":rows,"ttmi_false_breakout":ttmi}
 (RESULTS/"xhs_ideas_replay_2026_06_metrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
