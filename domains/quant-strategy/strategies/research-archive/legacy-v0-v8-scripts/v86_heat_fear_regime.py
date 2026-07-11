"""V8 regime model with separate heat and fear scores."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class V86Config:
    hot_qqq_weight: float|None=None
    heat_threshold: int=6
    fear_threshold: int=5
    fear_exposure_cap: float=1.0
    confirmation: int=1
    def __post_init__(self):
        if self.hot_qqq_weight not in {None,.6,.7}:raise ValueError("invalid hot weight")
        if self.heat_threshold not in {5,6}:raise ValueError("invalid heat threshold")
        if self.fear_threshold not in {3,4,5}:raise ValueError("invalid fear threshold")
        if self.fear_exposure_cap not in {.25,.5,1.0}:raise ValueError("invalid fear cap")
        if self.confirmation not in {1,2}:raise ValueError("invalid confirmation")

class V86Allocator:
    def __init__(self,close,vix,config):
        self.close=close[["SPY","QQQ"]];self.vix=vix.reindex(close.index).ffill();self.config=config
        self.ma150=self.close.rolling(150).mean();self.ma200=self.close.rolling(200).mean();self.mom126=self.close.pct_change(126,fill_method=None)
        self.dd63=self.close/self.close.rolling(63).max()-1
        self.state="normal";self.pending=None;self.pending_count=0;self.audit=[]
    def scores(self,dt):
        heat=0
        for s in ("SPY","QQQ"):
            p=self.close.at[dt,s];ma=self.ma200.at[dt,s];mom=self.mom126.at[dt,s]
            heat+=int(pd.notna(ma) and p>ma);heat+=int(pd.notna(mom) and mom>0);heat+=int(pd.notna(ma) and p/ma-1>.03)
        fear=0;parts={}
        level=self.vix.at[dt,"^VIX"] if "^VIX" in self.vix else float("nan")
        parts["vix_level"]=2 if pd.notna(level) and level>=30 else (1 if pd.notna(level) and level>=22 else 0);fear+=parts["vix_level"]
        hist=self.vix.loc[:dt,"^VIX"].dropna() if "^VIX" in self.vix else pd.Series(dtype=float)
        spike=float(hist.iloc[-1]/hist.iloc[-6]-1) if len(hist)>=6 else float("nan")
        parts["vix_5d_spike"]=2 if pd.notna(spike) and spike>=.30 else (1 if pd.notna(spike) and spike>=.15 else 0);fear+=parts["vix_5d_spike"]
        ratio=float("nan")
        if {"^VIX","^VIX3M"}.issubset(self.vix.columns) and pd.notna(self.vix.at[dt,"^VIX3M"]):ratio=float(self.vix.at[dt,"^VIX"]/self.vix.at[dt,"^VIX3M"])
        parts["vix_term_structure"]=2 if pd.notna(ratio) and ratio>=1 else (1 if pd.notna(ratio) and ratio>=.95 else 0);fear+=parts["vix_term_structure"]
        dd=float(self.dd63.loc[dt].mean())
        parts["index_drawdown"]=2 if pd.notna(dd) and dd<=-.10 else (1 if pd.notna(dd) and dd<=-.05 else 0);fear+=parts["index_drawdown"]
        return heat,fear,{"vix":None if pd.isna(level) else float(level),"vix_5d":None if pd.isna(spike) else spike,"vix_vix3m":None if pd.isna(ratio) else ratio,"mean_dd63":None if pd.isna(dd) else dd,"fear_parts":parts}
    def _confirm(self,desired):
        if desired==self.state:self.pending=None;self.pending_count=0;return
        if desired==self.pending:self.pending_count+=1
        else:self.pending=desired;self.pending_count=1
        if self.pending_count>=self.config.confirmation:self.state=desired;self.pending=None;self.pending_count=0
    def target(self,dt):
        heat,fear,detail=self.scores(dt);desired="fear" if fear>=self.config.fear_threshold else ("hot" if self.config.hot_qqq_weight is not None and heat>=self.config.heat_threshold else "normal");self._confirm(desired)
        target={};votes={}
        for s in ("SPY","QQQ"):
            n=int(self.close.at[dt,s]>self.ma150.at[dt,s])+int(self.close.at[dt,s]>self.ma200.at[dt,s]);votes[s]=n
            if n:target[s]=.25*n
        if self.state=="fear" and sum(target.values())>self.config.fear_exposure_cap:
            scale=self.config.fear_exposure_cap/sum(target.values());target={s:w*scale for s,w in target.items()}
        elif self.state=="hot" and sum(target.values())>=.999999:target={"SPY":1-self.config.hot_qqq_weight,"QQQ":self.config.hot_qqq_weight}
        self.audit.append({"date":str(dt.date()),"heat_score":heat,"fear_score":fear,"detail":detail,"desired_state":desired,"state":self.state,"votes":votes,"target":target,"cash":1-sum(target.values())});return target
