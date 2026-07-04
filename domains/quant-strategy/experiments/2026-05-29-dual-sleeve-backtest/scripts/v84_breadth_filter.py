"""Point-in-time breadth overlay for the unchanged V8 core."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class V84Config:
    breadth_ma: int | None = None
    threshold: float = 0.0
    weak_multiplier: float = 1.0
    def __post_init__(self):
        if self.breadth_ma not in {None,100,200}: raise ValueError("invalid breadth MA")
        if self.threshold not in {0.0,.4,.5,.6}: raise ValueError("invalid threshold")
        if self.weak_multiplier not in {0.0,.5,.75,1.0}: raise ValueError("invalid multiplier")


def build_breadth(stock_close: pd.DataFrame, membership: pd.DataFrame, ma_days: int) -> pd.Series:
    ma=stock_close.rolling(ma_days,min_periods=ma_days).mean()
    dates=stock_close.groupby(stock_close.index.to_period("M")).tail(1).index
    rows={}
    for dt in dates:
        mask=(membership["opt-in"]<=dt)&(membership["opt-out"].isna()|(membership["opt-out"]>dt))
        members=set(membership.loc[mask,"symbol"])
        cols=[s for s in members if s in stock_close.columns]
        if not cols: rows[dt]=float("nan"); continue
        px=stock_close.loc[dt,cols]; avg=ma.loc[dt,cols]
        valid=px.notna()&avg.notna()
        rows[dt]=float((px[valid]>avg[valid]).mean()) if valid.any() else float("nan")
    return pd.Series(rows,name=f"breadth_ma{ma_days}")


class V84Allocator:
    def __init__(self, close, config, breadth=None):
        self.close=close[["SPY","QQQ"]]; self.config=config; self.breadth=breadth
        self.ma150=self.close.rolling(150).mean(); self.ma200=self.close.rolling(200).mean()
        self.audit=[]
    def target(self,dt):
        target={}
        for symbol in ("SPY","QQQ"):
            votes=int(self.close.at[dt,symbol]>self.ma150.at[dt,symbol])+int(self.close.at[dt,symbol]>self.ma200.at[dt,symbol])
            if votes: target[symbol]=.25*votes
        value=None; scale=1.0
        if self.config.breadth_ma is not None and self.breadth is not None:
            prior=self.breadth.loc[:dt].dropna()
            value=float(prior.iloc[-1]) if len(prior) else None
            if value is not None and value<self.config.threshold: scale=self.config.weak_multiplier
        target={s:w*scale for s,w in target.items() if w*scale>1e-12}
        self.audit.append({"date":str(dt.date()),"breadth":value,"scale":scale,"target":target,"cash":1-sum(target.values())})
        return target
