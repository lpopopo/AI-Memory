"""V9 event-driven full-account research strategy. Formal V8 is untouched."""
from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
import hashlib,json,math
import numpy as np
import pandas as pd
from v87_dynamic_regime import V87Allocator,V87Config

@dataclass(frozen=True)
class V9Event:
    event_id:str; source:str; author:str; post_id:str; effective_at:pd.Timestamp
    content_hash:str; theme:str; symbols:tuple[str,...]; source_completeness:int
    thesis_novelty:int; fundamental_validation:int; crowding_penalty:int

@dataclass(frozen=True)
class V9EvidenceUpdate:
    update_id:str; effective_at:pd.Timestamp; symbols:tuple[str,...]
    source_type:str; validation_score:int; content_hash:str

@dataclass(frozen=True)
class V9Config:
    max_single:float=.20; max_theme:float=.40; max_names:int=5
    risk_per_name:float=.015; hard_stop:float=.08; event_life_days:int=60
    transaction_cost:float=.001; source_healthy:bool=True
    source_failure_date:str|None=None
    def __post_init__(self):
        if not 0<self.max_single<=.20:raise ValueError("single-name cap must be <=20%")
        if not 0<self.max_theme<=.40:raise ValueError("theme cap must be <=40%")
        if not 1<=self.max_names<=5:raise ValueError("at most five information names")
        if not 0<self.risk_per_name<=.015:raise ValueError("risk per name must be <=1.5%")
        if not 0<self.hard_stop<=.08:raise ValueError("hard stop must be <=8%")
        if self.transaction_cost<0:raise ValueError("transaction cost cannot be negative")

@dataclass
class PositionState:
    entry:float; initial_stop:float; peak:float; theme:str; score:float
    trimmed:bool=False; confirm_days:int=0

@dataclass
class V9Result:
    equity:pd.Series; weights:pd.DataFrame; audit:list[dict]; diagnostics:dict

def load_event_store(path:Path)->tuple[list[V9Event],dict]:
    raw=json.loads(path.read_text(encoding="utf-8"));events=[]
    for x in raw["events"]:
        # Replay from local availability; publication time alone would backfill knowledge.
        effective=pd.Timestamp(x["first_seen_at"] or x["published_at"])
        if effective.tzinfo is not None:effective=effective.tz_convert("UTC").tz_localize(None)
        expected=hashlib.sha256(x["content_summary"].encode("utf-8")).hexdigest()
        if x["content_hash"]!=expected:raise ValueError(f"invalid content hash: {x['event_id']}")
        for k in ("source_completeness","thesis_novelty","fundamental_validation"):
            if not 0<=x[k]<=20:raise ValueError(f"{k} out of range")
        if not 0<=x["crowding_penalty"]<=20:raise ValueError("crowding penalty out of range")
        events.append(V9Event(x["event_id"],x["source"],x["author"],x["post_id"],effective,x["content_hash"],x["theme"],tuple(x["symbols"]),x["source_completeness"],x["thesis_novelty"],x["fundamental_validation"],x["crowding_penalty"]))
    return sorted(events,key=lambda e:e.effective_at),raw

def load_evidence_store(path:Path)->tuple[list[V9EvidenceUpdate],dict]:
    raw=json.loads(path.read_text(encoding="utf-8"));updates=[];allowed={"company_filing","earnings_release","company_ir","regulator_filing"}
    for x in raw.get("updates",[]):
        if x["source_type"] not in allowed:raise ValueError(f"untrusted evidence type: {x['source_type']}")
        if not 0<=x["validation_score"]<=20:raise ValueError("validation_score out of range")
        expected=hashlib.sha256(x["content_summary"].encode("utf-8")).hexdigest()
        if x["content_hash"]!=expected:raise ValueError(f"invalid evidence hash: {x['update_id']}")
        effective=pd.Timestamp(x["first_seen_at"])
        if effective.tzinfo is not None:effective=effective.tz_convert("UTC").tz_localize(None)
        updates.append(V9EvidenceUpdate(x["update_id"],effective,tuple(x["symbols"]),x["source_type"],x["validation_score"],x["content_hash"]))
    ids=[x.update_id for x in updates]
    if len(ids)!=len(set(ids)):raise ValueError("duplicate evidence update id")
    return sorted(updates,key=lambda x:x.effective_at),raw

def chronological_split(events:list[V9Event],embargo_days:int=5)->dict:
    reliable=[e for e in events if e.source_completeness>=15]
    counts={"all":len(events),"reliable":len(reliable),"development":0,"validation":0,"test":0}
    if len(reliable)<50:return {"eligible":False,"reason":"fewer_than_50_reliable_events","counts":counts,"embargo_days":embargo_days}
    n=len(reliable);a=int(n*.6);b=int(n*.8);counts.update({"development":a,"validation":b-a,"test":n-b})
    return {"eligible":True,"counts":counts,"development":[e.event_id for e in reliable[:a]],"validation":[e.event_id for e in reliable[a:b]],"test":[e.event_id for e in reliable[b:]],"embargo_days":embargo_days}

class V9Backtester:
    def __init__(self,panels:dict[str,pd.DataFrame],vix:pd.DataFrame,events:list[V9Event],config:V9Config=V9Config(),evidence_updates:list[V9EvidenceUpdate]|None=None):
        self.p=panels;self.close=panels["close"].sort_index();self.events=events;self.cfg=config;self.evidence_updates=evidence_updates or []
        self.open=panels["open"].reindex_like(self.close);self.high=panels["high"].reindex_like(self.close);self.low=panels["low"].reindex_like(self.close);self.volume=panels["volume"].reindex_like(self.close)
        self.ma20=self.close.rolling(20).mean();self.ma50=self.close.rolling(50).mean();self.ma150=self.close.rolling(150).mean();self.ma200=self.close.rolling(200).mean();self.vol20=self.volume.rolling(20).mean()
        prev=self.close.shift(1);tr=pd.DataFrame(np.maximum.reduce([(self.high-self.low).to_numpy(),(self.high-prev).abs().to_numpy(),(self.low-prev).abs().to_numpy()]),index=self.close.index,columns=self.close.columns);self.atr20=tr.rolling(20).mean()
        self.rs20=self.close.pct_change(20,fill_method=None).sub(self.close["QQQ"].pct_change(20,fill_method=None),axis=0)
        self.prior20=self.close.shift(1).rolling(20).max();self.confirm={};self.states={};self.stock_targets={};self.audit=[];self.latest_watch=[]
        self.v87_targets,self.v8_targets,self.market_heat=self._fallbacks(vix)
    def _fallbacks(self,vix):
        a=V87Allocator(self.close[["SPY","QQQ"]],vix,V87Config(.7,70,75,.5,1));v87={};v8={};heats={};latest87={};latest8={};latest_heat=0
        periods=self.close.index.to_period("M")
        for i,dt in enumerate(self.close.index):
            if i==len(self.close)-1 or periods[i+1]!=periods[i]:
                latest87=a.target(dt);latest_heat=a.audit[-1]["heat_score"];latest8={s:.25*(int(self.close.at[dt,s]>self.ma150.at[dt,s])+int(self.close.at[dt,s]>self.ma200.at[dt,s])) for s in ("SPY","QQQ")}
            v87[dt]=dict(latest87);v8[dt]=dict(latest8);heats[dt]=latest_heat
        return v87,v8,heats
    def _event_for(self,symbol,dt):
        active=[e for e in self.events if e.effective_at.normalize()<=dt and (dt-e.effective_at.normalize()).days<=self.cfg.event_life_days and symbol in e.symbols]
        return active[-1] if active else None
    def _fundamental_score(self,event,symbol,dt):
        scores=[event.fundamental_validation]+[u.validation_score for u in self.evidence_updates if symbol in u.symbols and u.effective_at.normalize()<=dt]
        return max(scores)
    def _setup(self,s,dt):
        vals=[self.close.at[dt,s],self.ma20.at[dt,s],self.ma50.at[dt,s],self.ma200.at[dt,s],self.atr20.at[dt,s],self.rs20.at[dt,s],self.volume.at[dt,s],self.vol20.at[dt,s]]
        if any(pd.isna(x) for x in vals):return False,"unready",0
        px,m20,m50,m200,atr,rs,vol,vavg=map(float,vals);trend=px>m50 and px>m200;no_chase=(px/m20-1)<=.08 and (px-m20)<=2*atr
        breakout=px>self.prior20.at[dt,s] and vol>=1.5*vavg and trend and rs>0
        support=max(m20,m50);pullback=trend and self.low.at[dt,s]<=support*1.02 and px>=self.open.at[dt,s] and rs>0
        condition=(breakout or pullback) and no_chase;key=(s,(self._event_for(s,dt).event_id if self._event_for(s,dt) else "none"));self.confirm[key]=self.confirm.get(key,0)+1 if condition else 0
        technical=(5 if trend else 0)+(5 if rs>0 else 0)+(5 if vol>=vavg else 0)+(10 if self.confirm[key]>=2 else 0)
        return self.confirm[key]>=2,("breakout" if breakout else "pullback" if pullback else "none"),technical
    @staticmethod
    def score_cap(score):
        return 0 if score<70 else .05 if score<80 else .10 if score<90 else .15
    def _compose(self,dt,dd,allow_new):
        exits=[]
        for s,state in list(self.states.items()):
            state.peak=max(state.peak,float(self.close.at[dt,s]));risk=state.entry-state.initial_stop
            stop=max(state.initial_stop,min(float(self.ma50.at[dt,s]),state.entry*.99));trail=max(float(self.ma20.at[dt,s]),state.peak*.90)
            if self.close.at[dt,s]<stop or (state.trimmed and self.close.at[dt,s]<trail):self.stock_targets.pop(s,None);self.states.pop(s,None);exits.append({"symbol":s,"reason":"stop_or_trail"});continue
            if not state.trimmed and risk>0 and self.close.at[dt,s]>=state.entry+2*risk:self.stock_targets[s]*=2/3;state.trimmed=True;exits.append({"symbol":s,"reason":"trim_2R"})
        candidates=[];watch=[]
        if dd>-.10:
            symbols=sorted({s for e in self.events for s in e.symbols if s in self.close})
            for s in symbols:
                e=self._event_for(s,dt)
                if not e:continue
                confirmed,path,tech=self._setup(s,dt);heat=max(0,min(15,float(self.market_heat.get(dt,0))/100*15))
                fundamental=self._fundamental_score(e,s,dt);score=e.source_completeness+e.thesis_novelty+fundamental+tech+heat-e.crowding_penalty
                status="qualified" if confirmed and score>=70 else "confirming" if score>=70 else "validation_gap" if confirmed and score>=65 else "watch"
                watch.append({"symbol":s,"score":score,"event":e.event_id,"theme":e.theme,"fundamental_validation":fundamental,"confirmed":confirmed,"path":path,"status":status,"points_to_70":max(0,70-score),"new_entries_allowed":allow_new})
                if allow_new and confirmed and score>=70:candidates.append((score,s,e,path))
        self.latest_watch=sorted(watch,key=lambda x:x["score"],reverse=True)
        theme_used={}
        for s,w in self.stock_targets.items():theme_used[self.states[s].theme]=theme_used.get(self.states[s].theme,0)+w
        for score,s,e,path in sorted(candidates,reverse=True):
            if s in self.stock_targets:
                key=(s,e.event_id)
                if score>=90 and self.confirm.get(key,0)>=4:
                    px=float(self.close.at[dt,s]);risk_frac=max((px-self.states[s].initial_stop)/px,.001);room=self.cfg.max_theme-theme_used.get(e.theme,0)+self.stock_targets[s]
                    grown=min(.20,self.cfg.max_single,self.cfg.risk_per_name/risk_frac,room)
                    if grown>self.stock_targets[s]:theme_used[e.theme]+=grown-self.stock_targets[s];self.stock_targets[s]=grown
                continue
            if len(self.stock_targets)>=self.cfg.max_names:continue
            px=float(self.close.at[dt,s]);m50=float(self.ma50.at[dt,s]);stop=max(px*(1-self.cfg.hard_stop),min(m50,px*.99));risk_frac=max((px-stop)/px,.001)
            cap=min(self.score_cap(score),self.cfg.max_single,self.cfg.risk_per_name/risk_frac,self.cfg.max_theme-theme_used.get(e.theme,0))
            if cap<=0:continue
            self.stock_targets[s]=cap;self.states[s]=PositionState(px,stop,px,e.theme,score);theme_used[e.theme]=theme_used.get(e.theme,0)+cap
        if dd<=-.25:self.stock_targets.clear();self.states.clear();fallback=self.v8_targets.get(dt,{})
        else:fallback=self.v87_targets.get(dt,{})
        stocks=dict(self.stock_targets)
        if dd<=-.15:stocks={s:w*.5 for s,w in stocks.items()}
        residual=max(0,1-sum(stocks.values()));target=dict(stocks)
        for s,w in fallback.items():target[s]=target.get(s,0)+w*residual
        if dd<=-.20 and dd>-.25:
            gross=sum(target.values());scale=.5/gross if gross>.5 else 1;target={s:w*scale for s,w in target.items()}
        if sum(target.values())>1.000001:raise AssertionError("leverage prohibited")
        return target,exits,candidates
    def run(self,start=None,end=None):
        returns=self.close.pct_change(fill_method=None);weights={};pending=None;last_desired=None;value=1.;highwater=1.;equity=[];weight_rows=[];turnover=0
        for dt in self.close.index:
            factor=max(0,1-sum(weights.values()))+sum(w*(1+(0 if pd.isna(returns.at[dt,s]) else returns.at[dt,s])) for s,w in weights.items());value*=factor
            grown={s:w*(1+(0 if pd.isna(returns.at[dt,s]) else returns.at[dt,s]))/factor for s,w in weights.items()}
            weights=grown
            if pending is not None:
                before=dict(weights);traded=sum(abs(weights.get(s,0)-pending.get(s,0)) for s in set(weights)|set(pending));value*=1-traded*self.cfg.transaction_cost;turnover+=traded;weights=pending
                for s,state in self.states.items():
                    if before.get(s,0)<=1e-12 and weights.get(s,0)>0:
                        state.entry=float(self.close.at[dt,s]);state.peak=state.entry;state.initial_stop=max(state.entry*(1-self.cfg.hard_stop),min(float(self.ma50.at[dt,s]),state.entry*.99))
                pending=None
            highwater=max(highwater,value);dd=value/highwater-1
            allow=self.cfg.source_healthy or (self.cfg.source_failure_date is not None and dt<pd.Timestamp(self.cfg.source_failure_date))
            target,actions,cands=self._compose(dt,dd,allow)
            theme_actual={}
            for s,state in self.states.items():theme_actual[state.theme]=theme_actual.get(state.theme,0)+weights.get(s,0)
            overweight=any(weights.get(s,0)>self.cfg.max_single+1e-6 for s in self.states) or any(w>self.cfg.max_theme+1e-6 for w in theme_actual.values())
            changed=overweight or last_desired is None or set(target)!=set(last_desired) or any(abs(target.get(s,0)-last_desired.get(s,0))>1e-12 for s in set(target)|set(last_desired or {}))
            pending=target if changed else None
            if changed:last_desired=dict(target)
            self.audit.append({"date":str(dt.date()),"drawdown":dd,"source_healthy":allow,"stock_targets":dict(self.stock_targets),"final_target":target,"actions":actions,"qualified":[{"symbol":s,"score":score,"event":e.event_id,"path":path} for score,s,e,path in cands],"watchlist":self.latest_watch[:10]})
            equity.append(value);weight_rows.append({"date":dt,**weights,"cash":max(0,1-sum(weights.values()))})
        curve=pd.Series(equity,index=self.close.index,name="V9");wf=pd.DataFrame(weight_rows).set_index("date").fillna(0)
        if start:curve=curve.loc[start:];wf=wf.loc[start:]
        if end:curve=curve.loc[:end];wf=wf.loc[:end]
        return V9Result(curve,wf,self.audit,{"turnover":turnover,"execution":"signal close -> next close","source_healthy":self.cfg.source_healthy,"source_failure_date":self.cfg.source_failure_date})
