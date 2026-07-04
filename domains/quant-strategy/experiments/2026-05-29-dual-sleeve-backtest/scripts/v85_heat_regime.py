"""V8 market-heat regime switcher using only SPY/QQQ causal indicators."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class V85Config:
    hot_qqq_weight: float | None = None
    hot_min_distance: float = 0.0
    hot_vol_cap: float | None = None
    cold_exposure_cap: float = 1.0
    confirmation: int = 1
    def __post_init__(self):
        if self.hot_qqq_weight not in {None,.6,.7}: raise ValueError("invalid hot QQQ weight")
        if self.hot_min_distance not in {0.0,.03,.05}: raise ValueError("invalid distance")
        if self.hot_vol_cap not in {None,.20,.25}: raise ValueError("invalid volatility cap")
        if self.cold_exposure_cap not in {.25,.5,1.0}: raise ValueError("invalid cold cap")
        if self.confirmation not in {1,2}: raise ValueError("invalid confirmation")


class V85Allocator:
    def __init__(self,close:pd.DataFrame,config:V85Config):
        self.close=close[["SPY","QQQ"]];self.config=config
        self.ma150=self.close.rolling(150).mean();self.ma200=self.close.rolling(200).mean()
        self.mom126=self.close.pct_change(126,fill_method=None)
        self.vol20=self.close.pct_change(fill_method=None).rolling(20).std()*np.sqrt(252)
        self.state="normal";self.pending=None;self.pending_count=0;self.audit=[]
    def _desired_state(self,dt):
        if self.config.hot_qqq_weight is None:return "normal"
        price=self.close.loc[dt];ma=self.ma200.loc[dt];mom=self.mom126.loc[dt]
        if price.isna().any() or ma.isna().any() or mom.isna().any():return "normal"
        distance=price/ma-1
        hot=bool((price>ma).all() and (mom>0).all() and distance.mean()>=self.config.hot_min_distance)
        if self.config.hot_vol_cap is not None:
            hot=hot and bool(self.vol20.loc[dt].max()<=self.config.hot_vol_cap)
        cold=bool((price<ma).all() and (mom<0).all())
        return "hot" if hot else ("cold" if cold else "normal")
    def _confirm(self,desired):
        if desired==self.state:self.pending=None;self.pending_count=0;return
        if desired==self.pending:self.pending_count+=1
        else:self.pending=desired;self.pending_count=1
        if self.pending_count>=self.config.confirmation:
            self.state=desired;self.pending=None;self.pending_count=0
    def target(self,dt):
        desired=self._desired_state(dt);self._confirm(desired)
        target={};votes={}
        for s in ("SPY","QQQ"):
            count=int(self.close.at[dt,s]>self.ma150.at[dt,s])+int(self.close.at[dt,s]>self.ma200.at[dt,s]);votes[s]=count
            if count:target[s]=.25*count
        if self.state=="hot" and sum(target.values())>=.999999:
            target={"SPY":1-self.config.hot_qqq_weight,"QQQ":self.config.hot_qqq_weight}
        elif self.state=="cold" and sum(target.values())>self.config.cold_exposure_cap:
            scale=self.config.cold_exposure_cap/sum(target.values());target={s:w*scale for s,w in target.items()}
        total=sum(target.values())
        if total>1.000001:raise AssertionError("no leverage allowed")
        self.audit.append({"date":str(dt.date()),"desired_state":desired,"state":self.state,"votes":votes,"target":target,"cash":1-total})
        return target
