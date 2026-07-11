"""Adaptive V8 heat/fear regimes based on trailing three-year percentiles."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

WINDOW=756
MIN_PERIODS=252
def rolling_percentile(series:pd.Series)->pd.Series:
    def rank_last(values):
        values=values[np.isfinite(values)]
        return float(np.mean(values<=values[-1])) if len(values) else np.nan
    return series.rolling(WINDOW,min_periods=MIN_PERIODS).apply(rank_last,raw=True)
def weighted_available(parts:dict[str,float],weights:dict[str,float])->float:
    valid=[k for k,v in parts.items() if pd.notna(v)]
    if not valid:return float("nan")
    return 100*sum(parts[k]*weights[k] for k in valid)/sum(weights[k] for k in valid)

@dataclass(frozen=True)
class V87Config:
    hot_qqq_weight:float|None=None
    heat_threshold:int=80
    fear_threshold:int=85
    fear_multiplier:float=1.0
    confirmation:int=1
    def __post_init__(self):
        if self.hot_qqq_weight not in {None,.6,.7}:raise ValueError("invalid hot weight")
        if self.heat_threshold not in {70,75,80}:raise ValueError("invalid heat threshold")
        if self.fear_threshold not in {75,80,85}:raise ValueError("invalid fear threshold")
        if self.fear_multiplier not in {.5,.75,1.0}:raise ValueError("invalid fear multiplier")
        if self.confirmation not in {1,2}:raise ValueError("invalid confirmation")

class V87Allocator:
    def __init__(self,close,vix,config):
        self.close=close[["SPY","QQQ"]];self.vix=vix.reindex(close.index).ffill();self.config=config
        self.ma150=self.close.rolling(150).mean();self.ma200=self.close.rolling(200).mean()
        mom126=self.close.pct_change(126,fill_method=None).mean(axis=1);distance=(self.close/self.ma200-1).mean(axis=1);relative=(self.close.QQQ/self.close.SPY).pct_change(63,fill_method=None)
        vix_level=self.vix["^VIX"];vix_spike=vix_level.pct_change(5,fill_method=None);term=self.vix["^VIX"]/self.vix["^VIX3M"]
        severity=-(self.close/self.close.rolling(63).max()-1).mean(axis=1)
        self.heat_parts={"momentum":rolling_percentile(mom126),"distance":rolling_percentile(distance),"relative_strength":rolling_percentile(relative)}
        self.fear_parts={"vix_level":rolling_percentile(vix_level),"vix_spike":rolling_percentile(vix_spike),"term_structure":rolling_percentile(term),"drawdown":rolling_percentile(severity)}
        self.state="normal";self.pending=None;self.pending_count=0;self.audit=[]
    def scores(self,dt):
        votes=sum(int(self.close.at[dt,s]>ma.at[dt,s]) for s in ("SPY","QQQ") for ma in (self.ma150,self.ma200));trend=votes/4
        hp={k:float(v.at[dt]) if pd.notna(v.at[dt]) else np.nan for k,v in self.heat_parts.items()};hp["trend"]=trend
        fp={k:float(v.at[dt]) if pd.notna(v.at[dt]) else np.nan for k,v in self.fear_parts.items()}
        heat=weighted_available(hp,{"trend":.35,"momentum":.30,"distance":.20,"relative_strength":.15})
        fear=weighted_available(fp,{"vix_level":.30,"vix_spike":.20,"term_structure":.25,"drawdown":.25})
        return heat,fear,votes,hp,fp
    def _confirm(self,desired):
        if desired==self.state:self.pending=None;self.pending_count=0;return
        if desired==self.pending:self.pending_count+=1
        else:self.pending=desired;self.pending_count=1
        if self.pending_count>=self.config.confirmation:self.state=desired;self.pending=None;self.pending_count=0
    def target(self,dt):
        heat,fear,votes,hp,fp=self.scores(dt);weak=votes<=2
        desired="fear" if pd.notna(fear) and fear>=self.config.fear_threshold and weak else ("hot" if self.config.hot_qqq_weight is not None and pd.notna(heat) and heat>=self.config.heat_threshold and fear<60 else "normal")
        self._confirm(desired);target={}
        per_votes={}
        for s in ("SPY","QQQ"):
            n=int(self.close.at[dt,s]>self.ma150.at[dt,s])+int(self.close.at[dt,s]>self.ma200.at[dt,s]);per_votes[s]=n
            if n:target[s]=.25*n
        if self.state=="fear":target={s:w*self.config.fear_multiplier for s,w in target.items()}
        elif self.state=="hot" and sum(target.values())>=.999999:target={"SPY":1-self.config.hot_qqq_weight,"QQQ":self.config.hot_qqq_weight}
        self.audit.append({"date":str(dt.date()),"heat_score":heat,"fear_score":fear,"heat_parts":hp,"fear_parts":fp,"desired_state":desired,"state":self.state,"votes":per_votes,"target":target,"cash":1-sum(target.values())});return target
