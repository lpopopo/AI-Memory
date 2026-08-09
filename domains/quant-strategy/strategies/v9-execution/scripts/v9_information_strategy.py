"""
V9 Backtest Engine implementing strict execution rules, order/position separation,
and comprehensive funnel tracking.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import hashlib, json, math
import numpy as np
import pandas as pd
from v9_fear_gate import compute_canonical_fear_gate

AI_CAPEX_THEMES = frozenset({
    "ai_architecture", "ai_bottleneck", "ai_cloud_factory", "ai_inference",
    "ai_interconnect", "custom_silicon", "hbm_upstream", "memory_efficiency",
    "memory_storage", "optical_components",
})

@dataclass(frozen=True)
class V9Event:
    event_id: str
    source: str
    author: str
    post_id: str
    effective_at: pd.Timestamp
    content_hash: str
    theme: str
    symbols: tuple[str, ...]
    source_completeness: int
    thesis_novelty: int
    fundamental_validation: int
    crowding_penalty: int
    point_in_time_eligible: bool = True

@dataclass(frozen=True)
class V9EvidenceUpdate:
    update_id: str
    effective_at: pd.Timestamp
    symbols: tuple[str, ...]
    source_type: str
    validation_score: int
    content_hash: str

@dataclass(frozen=True)
class V9Config:
    # Portfolio Structure
    v8_core_weight: float = 0.70  # Integrated SPY/QQQ index-core ceiling.
    info_sleeve_weight: float = 0.30  # Integrated individual-stock sleeve ceiling.

    # Information limits
    max_single: float = 0.10
    max_theme: float = 0.30
    max_names: int = 3
    risk_per_name: float = 0.015
    hard_stop: float = 0.08
    event_life_days: int = 40
    transaction_cost: float = 0.001

    # Source / Env
    source_healthy: bool = True
    source_failure_date: str | None = None

    # Score logic
    score_threshold: float = 70.0
    tech_weight: float = 1.0
    crowding_multiplier: float = 1.0
    min_fundamental: int = 10
    trusted_event_only: bool = False
    min_source_completeness: int = 0
    score_cap_scale: float = 1.0
    aggregate_common_factors: bool = True
    fear_gate_enabled: bool = True
    fear_allocation_policy: str = "core_priority" # 'proportional', 'core_priority'
    institutional_triple_confirmation: bool = False
    institutional_flow_overlay: bool = False
    institutional_quality_sizing: bool = False

    # Confirmation / Selection
    ranking_mode: bool = False
    tech_path_mode: str = "any" # 'breakout', 'pullback', 'trend', 'any'

    # Exits
    trim_r_multiple: float = 2.0
    trailing_stop_mode: str = "ma20" # 'ma20', 'ma50', 'pct10'
    dynamic_stop_mode: str = "fixed" # 'fixed', 'technical_staged'

    # Phase 3 & 4 Entry Rules
    entry_rule_version: str = "A" # 'A', 'B', 'C', 'D'
    dynamic_atr_max: float = 2.5
    wait_days_max: int = 10
    upgrade_trigger: str = "second_conf"
    time_stop_days: int = 3
    obs_size: float = 0.02

    def __post_init__(self):
        if not 0 <= self.v8_core_weight <= 1 or not 0 <= self.info_sleeve_weight <= 1:
            raise ValueError("sleeve weights must be within [0, 1]")
        if self.v8_core_weight + self.info_sleeve_weight > 1.000001:
            raise ValueError("core and information sleeves cannot exceed 100%")
        if not 0 < self.max_single <= .20 or not 0 < self.max_theme <= .40:
            raise ValueError("position or theme cap is outside the approved range")
        if not 1 <= self.max_names <= 5 or not 0 < self.risk_per_name <= .015:
            raise ValueError("name count or risk-per-name exceeds the approved range")
        if not 0 < self.hard_stop <= .10 or self.transaction_cost < 0:
            raise ValueError("invalid stop or transaction cost")
        if not 0 <= self.min_fundamental <= 20 or not 0 <= self.min_source_completeness <= 20:
            raise ValueError("information-quality floor is outside [0, 20]")
        if self.dynamic_stop_mode not in {"fixed", "technical_staged"}:
            raise ValueError("unknown dynamic stop mode")
        if self.fear_allocation_policy not in {"proportional", "core_priority"}:
            raise ValueError("unknown fear allocation policy")

@dataclass
class PendingOrder:
    symbol: str
    target_weight: float
    signal_date: pd.Timestamp
    score: float
    stop_price: float
    order_type: str # 'buy', 'sell', 'trim', 'v8_rebalance', 'drawdown_cut'
    theme: str = ""
    r_risk: float = 0.0
    is_observation: bool = False
    event_day_low: float = 0.0
    high_vol_entry: bool = False
    event_id: str = ""

@dataclass
class PositionState:
    entry: float
    shares: float
    initial_stop: float
    theme: str
    score: float
    r_risk: float
    trimmed: bool = False
    trailing_stop: float = 0.0
    days_held: int = 0
    peak: float = 0.0
    is_observation: bool = False
    event_day_low: float = 0.0
    qqq_entry: float = 0.0
    event_id: str = ""

@dataclass
class V9Result:
    equity: pd.Series
    weights: pd.DataFrame
    audit: list[dict]
    diagnostics: dict
    funnel: list[dict]
    ledger: list[dict]

def load_event_store(path: Path, use_retrospective: bool = False) -> tuple[list[V9Event], dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    events = []
    seen_ids = set()
    backfill = raw.get("retrospective_backfill", {})
    backfill_ids = set(backfill.get("event_ids", []))
    backfill_seen = backfill.get("archive_observed_at")

    for x in raw["events"]:
        event_id = str(x.get("event_id", "")).strip()
        if not event_id or event_id in seen_ids:
            raise ValueError(f"missing or duplicate event_id: {event_id}")

        symbols = x.get("symbols", [])
        if not symbols or any(not isinstance(s, str) or not s or s != s.strip().upper() for s in symbols):
            raise ValueError(f"invalid symbols: {event_id}")
        if len(symbols) != len(set(symbols)):
            raise ValueError(f"duplicate symbols: {event_id}")
        summary = x.get("content_summary", "")
        expected_hash = hashlib.sha256(summary.encode("utf-8")).hexdigest()
        if x.get("content_hash") != expected_hash:
            raise ValueError(f"invalid content hash: {event_id}")
        for key in ("source_completeness", "thesis_novelty", "fundamental_validation", "crowding_penalty"):
            if not 0 <= x.get(key, -1) <= 20:
                raise ValueError(f"{key} out of range: {event_id}")
        point_in_time_eligible = event_id not in backfill_ids

        # Real-time uses first_seen_at. Historical uses published_at (only for retrospective)
        if use_retrospective:
            ts_str = x.get("published_at") or x.get("first_seen_at")
        else:
            ts_str = x.get("first_seen_at") if point_in_time_eligible else backfill_seen

        if not ts_str: continue

        effective = pd.Timestamp(ts_str)
        if effective.tzinfo is not None:
            effective = effective.tz_convert("UTC").tz_localize(None)

        # Date only: delay to 23:59:59 to avoid intraday leakage
        if len(ts_str) <= 10:
            effective = effective.replace(hour=23, minute=59, second=59)

        events.append(V9Event(
            event_id, x.get("source", ""), x.get("author", ""), x.get("post_id", ""),
            effective, x.get("content_hash", ""), x.get("theme", ""), tuple(symbols),
            x.get("source_completeness", 0), x.get("thesis_novelty", 0),
            x.get("fundamental_validation", 0), x.get("crowding_penalty", 0),
            point_in_time_eligible
        ))
        seen_ids.add(event_id)
    return sorted(events, key=lambda e: e.effective_at), raw

def load_evidence_store(path: Path) -> tuple[list[V9EvidenceUpdate], dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    updates = []
    allowed = {"company_filing", "earnings_release", "company_ir", "regulator_filing"}
    for x in raw.get("updates", []):
        if x.get("source_type") not in allowed:
            raise ValueError(f"untrusted evidence type: {x.get('source_type')}")
        expected_hash = hashlib.sha256(x.get("content_summary", "").encode("utf-8")).hexdigest()
        if x.get("content_hash") != expected_hash:
            raise ValueError(f"invalid evidence hash: {x.get('update_id')}")
        effective = pd.Timestamp(x["first_seen_at"])
        if effective.tzinfo is not None: effective = effective.tz_convert("UTC").tz_localize(None)
        updates.append(V9EvidenceUpdate(x["update_id"], effective, tuple(x.get("symbols", [])), x["source_type"], x.get("validation_score", 0), x.get("content_hash", "")))
    ids = [row.update_id for row in updates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate evidence update id")
    return sorted(updates, key=lambda x: x.effective_at), raw

def chronological_split(events: list[V9Event], embargo_days: int=5) -> dict:
    reliable = [e for e in events if e.source_completeness >= 15 and e.point_in_time_eligible]
    counts = {"all": len(events), "reliable_point_in_time": len(reliable), "retrospective_only": sum(not e.point_in_time_eligible for e in events), "development": 0, "validation": 0, "test": 0}
    if len(reliable) < 50:
        return {"eligible": False, "reason": "fewer_than_50_reliable_point_in_time_events", "counts": counts, "embargo_days": embargo_days}
    a, b = int(len(reliable) * .6), int(len(reliable) * .8)
    counts.update({"development": a, "validation": b-a, "test": len(reliable)-b})
    return {"eligible": True, "counts": counts, "development": [e.event_id for e in reliable[:a]], "validation": [e.event_id for e in reliable[a:b]], "test": [e.event_id for e in reliable[b:]], "embargo_days": embargo_days}


class V9Backtester:
    def __init__(self, panels: dict[str, pd.DataFrame], vix: pd.DataFrame, events: list[V9Event], config: V9Config, evidence_updates: list[V9EvidenceUpdate] = None):
        self.p = panels
        self.close = panels["close"].sort_index()
        self.open = panels["open"].reindex_like(self.close)
        self.high = panels["high"].reindex_like(self.close)
        self.low = panels["low"].reindex_like(self.close)
        self.volume = panels["volume"].reindex_like(self.close)

        self.events = events
        self.cfg = config
        self.evidence_updates = evidence_updates or []
        self.vix = vix

        self.ma20 = self.close.rolling(20).mean()
        self.ma50 = self.close.rolling(50).mean()
        self.ma150 = self.close.rolling(150).mean()
        self.ma200 = self.close.rolling(200).mean()
        self.vol20 = self.volume.rolling(20).mean()

        prev = self.close.shift(1)
        tr = pd.DataFrame(np.maximum.reduce([
            (self.high - self.low).to_numpy(),
            (self.high - prev).abs().to_numpy(),
            (self.low - prev).abs().to_numpy()
        ]), index=self.close.index, columns=self.close.columns)
        self.atr20 = tr.rolling(20).mean()
        self.rs20 = self.close.pct_change(20, fill_method=None).sub(self.close["QQQ"].pct_change(20, fill_method=None), axis=0)
        self.prior20 = self.close.shift(1).rolling(20).max()

        self._fear_gate_cache: dict[pd.Timestamp, dict] = {}
        self.v8_base_weights = self._v8_base()

        self.positions = {} # symbol -> PositionState
        self.v8_shares = {"SPY": 0.0, "QQQ": 0.0}
        self.pending_orders = [] # list of PendingOrder

        self.waitlist = {} # (event_id, symbol) -> dict containing state metadata
        self.capacity_queue = {} # (event_id, symbol) -> dict containing state metadata
        self.audit = []
        self.funnel = []
        self.ledger = []

        self.cash = 1.0
        self.value = 1.0
        self.highwater = 1.0
        self.turnover = 0.0

    def _is_completed_month_end(self, i: int) -> bool:
        dt = self.close.index[i]
        if i + 1 < len(self.close.index):
            return self.close.index[i + 1].to_period("M") != dt.to_period("M")
        # Do not mistake an incomplete latest dataset row for month-end.
        return dt.normalize() == (dt + pd.offsets.BMonthEnd(0)).normalize()

    def _v8_base(self):
        v8 = {}
        latest8 = {}
        for i, dt in enumerate(self.close.index):
            if self._is_completed_month_end(i):
                # 0.5 per asset
                latest8 = {s: 0.5 * (int(self.close.at[dt, s] > self.ma150.at[dt, s]) + int(self.close.at[dt, s] > self.ma200.at[dt, s])) * 0.5 for s in ("SPY", "QQQ")}
            v8[dt] = dict(latest8)
        return v8

    def _fear_gate(self, dt: pd.Timestamp) -> dict:
        """Point-in-time portfolio gate using only completed bars through ``dt``."""
        if dt in self._fear_gate_cache:
            return self._fear_gate_cache[dt]
        canonical = compute_canonical_fear_gate(
            self.close,
            self.vix,
            dt,
            enabled=self.cfg.fear_gate_enabled,
        )
        result = {key: value for key, value in canonical.items() if key != "action"}
        result["signals"] = [
            {key: value for key, value in signal.items() if key != "note"}
            for signal in canonical["signals"]
        ]
        self._fear_gate_cache[dt] = result
        return result

    def _core_fear_gate(self, dt: pd.Timestamp) -> dict:
        if not self.cfg.fear_gate_enabled:
            return self._fear_gate(dt)
        # The core remains a monthly process. Its risk budget is fixed from the
        # latest completed month-end, except that a VIX>=35 panic cuts it once
        # and keeps the lower budget until the next month-end review. Stock
        # entries continue to use the current daily gate.
        loc = self.close.index.get_loc(dt)
        review_dt = dt
        for i in range(loc, -1, -1):
            if self._is_completed_month_end(i):
                review_dt = self.close.index[i]
                break
        core_fear = self._fear_gate(review_dt)
        if "^VIX" in self.vix.columns:
            since_review = self.vix.loc[review_dt:dt, "^VIX"].dropna()
            if not since_review.empty and float(since_review.max()) >= 35:
                core_fear = {
                    **core_fear,
                    "regime": "panic",
                    "risk_multiplier": .20,
                    "max_gross_exposure": .35,
                    "max_new_buy_exposure": 0.0,
                    "cash_floor": .65,
                    "panic_latched_since_month_end": True,
                }
        return core_fear

    def _effective_sleeve_caps(self, dt: pd.Timestamp) -> tuple[float, float, dict]:
        fear = self._fear_gate(dt)
        core_fear = self._core_fear_gate(dt)
        if self.cfg.fear_allocation_policy == "core_priority":
            core_cap = min(self.cfg.v8_core_weight, core_fear["max_gross_exposure"])
            info_cap = min(
                self.cfg.info_sleeve_weight,
                max(0.0, fear["max_gross_exposure"] - core_cap),
            )
            return core_cap, info_cap, fear
        return (
            self.cfg.v8_core_weight * core_fear["max_gross_exposure"],
            self.cfg.info_sleeve_weight * fear["max_gross_exposure"],
            fear,
        )

    def _event_for(self, symbol, dt):
        events = self.events
        if not self.cfg.source_healthy:
            if self.cfg.source_failure_date is None:
                return None
            failure = pd.Timestamp(self.cfg.source_failure_date)
            events = [e for e in events if e.effective_at.normalize() < failure]
        active = [e for e in events if e.effective_at.normalize() <= dt and (dt - e.effective_at.normalize()).days <= self.cfg.event_life_days and symbol in e.symbols]
        return active[-1] if active else None

    def _fundamental_score(self, event, symbol, dt):
        scores = [event.fundamental_validation] + [u.validation_score for u in self.evidence_updates if symbol in u.symbols and u.effective_at.normalize() <= dt]
        return max(scores)

    def _trusted_event_eligible(self, event, symbol, dt) -> bool:
        """Optional V9.1 gate; defaults off so frozen V9 behavior is unchanged."""
        if not self.cfg.trusted_event_only:
            return True
        return bool(
            event.point_in_time_eligible
            and event.source_completeness >= self.cfg.min_source_completeness
            and self._fundamental_score(event, symbol, dt) >= self.cfg.min_fundamental
        )

    def _theme_bucket(self, theme: str) -> str:
        if self.cfg.aggregate_common_factors and theme in AI_CAPEX_THEMES:
            return "ai_capex"
        return theme

    def _theme_exposure(self, close_prices: pd.Series) -> dict[str, float]:
        exposure: dict[str, float] = {}
        if self.value <= 0:
            return exposure
        for symbol, state in self.positions.items():
            price = close_prices.get(symbol)
            if pd.isna(price):
                continue
            bucket = self._theme_bucket(state.theme)
            exposure[bucket] = exposure.get(bucket, 0.0) + state.shares * float(price) / self.value
        return exposure

    def _flow_fragility_score(self, dt: pd.Timestamp) -> int:
        """Public-proxy score inspired by Citadel market-structure research."""
        loc = self.close.index.get_loc(dt)
        if loc < 21:
            return 0
        symbols = sorted({s for e in self.events for s in e.symbols if s in self.close.columns})
        if not symbols or pd.isna(self.close.at[dt, "QQQ"]):
            return 0
        prior = self.close.index[loc - 20]
        qqq_ret = self.close.at[dt, "QQQ"] / self.close.at[prior, "QQQ"] - 1
        rel = []
        extensions = []
        for symbol in symbols:
            if pd.notna(self.close.at[dt, symbol]) and pd.notna(self.close.at[prior, symbol]):
                rel.append(self.close.at[dt, symbol] / self.close.at[prior, symbol] - 1 - qqq_ret)
            if pd.notna(self.ma20.at[dt, symbol]) and self.ma20.at[dt, symbol] > 0 and pd.notna(self.close.at[dt, symbol]):
                extensions.append(self.close.at[dt, symbol] / self.ma20.at[dt, symbol] - 1)
        score = 0
        if rel:
            participation = float(np.mean(np.asarray(rel) > 0))
            score += 2 if participation < .35 else 1 if participation < .50 else 0
            median_rel = float(np.median(rel))
            score += 2 if median_rel > .05 else 1 if median_rel > .02 else 0
        if extensions:
            extension = float(np.median(extensions))
            score += 2 if extension > .08 else 1 if extension > .04 else 0
        vix = self.vix.at[dt, "^VIX"] if dt in self.vix.index else np.nan
        score += 2 if pd.notna(vix) and vix >= 22 else 1 if pd.notna(vix) and vix >= 16 else 0
        if loc >= 5 and dt in self.vix.index:
            p5 = self.close.index[loc - 5]
            if p5 in self.vix.index and pd.notna(self.vix.at[p5, "^VIX"]) and pd.notna(vix):
                q5 = self.close.at[dt, "QQQ"] / self.close.at[p5, "QQQ"] - 1
                v5 = vix / self.vix.at[p5, "^VIX"] - 1
                if q5 > 0 and v5 > 0:
                    score += 2
        return int(score)

    @staticmethod
    def _quality_size_multiplier(fundamental_validation: int) -> float:
        if fundamental_validation >= 15:
            return 1.0
        if fundamental_validation >= 12:
            return .75
        return .60

    def _tech_setup(self, s, dt, event_date=None):
        vals = [self.close.at[dt, s], self.ma20.at[dt, s], self.ma50.at[dt, s], self.ma200.at[dt, s], self.atr20.at[dt, s], self.rs20.at[dt, s], self.volume.at[dt, s], self.vol20.at[dt, s]]
        if any(pd.isna(x) for x in vals): return False, "unready", 0, "missing_data", False
        px, m20, m50, m200, atr, rs, vol, vavg = map(float, vals)

        # Rule D1 & D2 logic check
        chase_limit_pct = 0.08
        chase_limit_atr = 2.0

        ma20_dev = (px / m20 - 1) if m20 > 0 else 0
        atr_dev = (px - m20) / atr if atr > 0 else 0

        is_chased_8pct = ma20_dev > chase_limit_pct
        is_chased_2atr = atr_dev > chase_limit_atr

        # In Rule E, D1 only triggers if BOTH are met. We pass this info out.
        is_chased_both = is_chased_8pct and is_chased_2atr
        is_chased = is_chased_8pct or is_chased_2atr # for legacy rules

        breakout = px > self.prior20.at[dt, s] and px > m50 and px > m200 and vol >= 1.3 * vavg and rs > 0
        trend_conf = px > m20 and px > m50 and rs > 0

        # Check history for 'Wait Orders'
        dt_loc = self.close.index.get_loc(dt)
        recent_breakout = False
        trend_conf_count = 0

        if dt_loc >= 3:
            # 3日内累计两次趋势确认
            for i in range(dt_loc - 2, dt_loc + 1):
                idx = self.close.index[i]
                if pd.notna(self.close.at[idx, s]) and pd.notna(self.ma20.at[idx, s]) and pd.notna(self.ma50.at[idx, s]) and pd.notna(self.rs20.at[idx, s]):
                    if self.close.at[idx, s] > self.ma20.at[idx, s] and self.close.at[idx, s] > self.ma50.at[idx, s] and self.rs20.at[idx, s] > 0:
                        trend_conf_count += 1

            # 突破后首次回踩 (look back 10 days for a breakout)
            if dt_loc >= 10:
                for i in range(dt_loc - 10, dt_loc):
                    idx = self.close.index[i]
                    b_px = self.close.at[idx, s]
                    if pd.isna(b_px): continue
                    b_prior = self.prior20.at[idx, s]
                    b_m50 = self.ma50.at[idx, s]
                    b_m200 = self.ma200.at[idx, s]
                    b_vol = self.volume.at[idx, s]
                    b_vavg = self.vol20.at[idx, s]
                    b_rs = self.rs20.at[idx, s]
                    if pd.isna(b_prior) or pd.isna(b_m50) or pd.isna(b_m200) or pd.isna(b_vol) or pd.isna(b_vavg) or pd.isna(b_rs): continue
                    if b_px > b_prior and b_px > b_m50 and b_px > b_m200 and b_vol >= 1.3 * b_vavg and b_rs > 0:
                        recent_breakout = True
                        break

        pullback = recent_breakout and px > m50 and px > m200 and self.low.at[dt, s] <= m20 * 1.02 and px >= m20 and rs > 0
        trend_wait = trend_conf_count >= 2

        valid = False
        path = "none"
        if self.cfg.tech_path_mode == "breakout":
            valid = breakout
            path = "breakout"
        elif self.cfg.tech_path_mode == "pullback":
            valid = pullback
            path = "pullback"
        elif self.cfg.tech_path_mode == "trend":
            valid = trend_conf or trend_wait
            path = "trend"
        else:
            valid = breakout or pullback or trend_conf or trend_wait
            path = "breakout" if breakout else ("pullback" if pullback else "trend")

        if self.cfg.institutional_triple_confirmation:
            volume_confirmed = vol >= .80 * vavg
            trend_structure = px > m20 > m50
            valid = valid and trend_structure and rs > 0 and volume_confirmed
            if not valid:
                return False, "none", 0, "institutional_triple_confirmation_failed", False

        if not valid:
            return False, "none", 0, "technical_not_confirmed", False

        tech_score = (5 if px > m50 else 0) + (5 if rs > 0 else 0) + (5 if vol >= vavg else 0) + 10

        if is_chased:
            reason = "chase_both" if is_chased_both else ("chase_8pct" if is_chased_8pct else "chase_2atr")
            return valid, path, tech_score, reason, True
        else:
            return valid, path, tech_score, "", False

    def score_cap(self, score):
        if score < self.cfg.score_threshold: return 0
        base = 0.05 if score < 80 else 0.10 if score < 90 else 0.15
        return min(base * self.cfg.score_cap_scale, self.cfg.max_single)

    def _candidate_sizing_score(self, candidate: dict) -> float:
        """A triggered Rule E wait order earns the minimum executable score cap.

        D1/D2 are deliberately admitted below the main score threshold and must
        not subsequently be sized to zero merely because they used a wait path.
        """
        if candidate.get("rule") in {"D1", "D2"}:
            return max(float(candidate["score"]), self.cfg.score_threshold)
        return float(candidate["score"])

    def _initial_stop(self, symbol, dt, fixed_stop: float) -> float:
        """Use technical support when available, while retaining hard-stop risk cap."""
        if self.cfg.dynamic_stop_mode != "technical_staged":
            return fixed_stop
        px, m20, low, atr = (self.close.at[dt, symbol], self.ma20.at[dt, symbol], self.low.at[dt, symbol], self.atr20.at[dt, symbol])
        if any(pd.isna(x) for x in (px, m20, low, atr)) or atr <= 0:
            return fixed_stop
        support_stop = min(float(m20), float(low)) - .5 * float(atr)
        return min(float(px) * .99, max(float(fixed_stop), support_stop))

    def _technical_staged_stop(self, symbol, state, dt, close_price: float) -> float:
        """Four stages: structural risk, breakeven, rising-trend trail, mature trend trail."""
        if self.cfg.dynamic_stop_mode != "technical_staged":
            ts = state.initial_stop
            if self.cfg.trailing_stop_mode == "ma20": ts = float(self.ma20.at[dt, symbol])
            elif self.cfg.trailing_stop_mode == "ma50": ts = float(self.ma50.at[dt, symbol])
            elif self.cfg.trailing_stop_mode == "pct10": ts = state.peak * .90
            return max(state.trailing_stop, min(ts, close_price * .99))
        atr, m20, m50 = self.atr20.at[dt, symbol], self.ma20.at[dt, symbol], self.ma50.at[dt, symbol]
        if any(pd.isna(x) for x in (atr, m20, m50)) or atr <= 0:
            return state.trailing_stop
        loc = self.close.index.get_loc(dt)
        prior_m20 = self.ma20.at[self.close.index[max(0, loc - 3)], symbol]
        rising_m20 = pd.notna(prior_m20) and m20 > prior_m20
        risk = max(1e-6, state.entry - state.initial_stop)
        r_multiple = (close_price - state.entry) / risk
        breakeven = state.entry * (1 + 2 * self.cfg.transaction_cost)
        if r_multiple < 1:
            target = state.initial_stop
        elif r_multiple < 2:
            target = max(state.initial_stop, breakeven, (m20 - atr) if rising_m20 else state.initial_stop)
        else:
            trend_support = (m20 - .5 * atr) if rising_m20 else (m50 - atr)
            target = max(breakeven, trend_support, state.peak - 2.5 * atr)
        return max(state.trailing_stop, min(float(target), close_price * .99))

    def _execute_trade(self, symbol, dt, price, shares_diff, reason, is_info=True, is_observation=False, event_id=""):
        val = abs(shares_diff) * price
        cost = val * self.cfg.transaction_cost

        # Delete orders < 0.5% weight (unless it's a full exit/stop loss where we just want to clear the position)
        if val / self.value < 0.005 and reason not in ["stop_loss", "sell", "drawdown_cut", "v8_rebalance"]:
            return 0.0

        if abs(shares_diff) < 1e-6:
            return 0.0

        if shares_diff > 0:
            if self.cash < val + cost:
                # Fallback to available cash
                val = max(0, self.cash - cost)
                shares_diff = val / price
                cost = val * self.cfg.transaction_cost
            self.cash -= (val + cost)
            cash_flow = -val
        else:
            self.cash += (val - cost)
            cash_flow = val

        self.turnover += val

        self.daily_cost += cost
        if not is_info:
            self.daily_v8_flow += cash_flow
        elif is_observation:
            self.daily_info_obs_flow += cash_flow
        else:
            self.daily_info_off_flow += cash_flow

        self.ledger.append({
            "date": str(dt.date()),
            "symbol": symbol,
            "action": "BUY" if shares_diff > 0 else "SELL",
            "shares": shares_diff,
            "price": price,
            "cost": cost,
            "reason": reason,
            "is_info": is_info,
            "is_observation": is_observation
            ,"event_id": event_id
        })

        return shares_diff

    def run(self, warmup_start: str | None = None, trading_start: str | None = None, trading_end: str | None = None, _shadow_step: bool = False):
        warmup_start = warmup_start or str(self.close.index[0].date())
        trading_start = trading_start or warmup_start
        trading_end = trading_end or str(self.close.index[-1].date())
        if not _shadow_step:
            self.cash = 1.0
            self.value = 1.0
            self.highwater = 1.0
            self.positions = {}
            self.v8_shares = {"SPY": 0.0, "QQQ": 0.0}
            self.pending_orders = []
            self.waitlist = {}
            self.capacity_queue = {}
            self.audit = []
            self.funnel = []
            self.ledger = []
        else:
            self.audit = []
            self.funnel = []
            self.ledger = []

        equity = []
        weight_rows = []

        if not _shadow_step:
            self.cum_v8_pnl = 0.0
            self.cum_info_official_pnl = 0.0
            self.cum_info_obs_pnl = 0.0
            self.cum_cost = 0.0
        else:
            self.cum_v8_pnl = getattr(self, "cum_v8_pnl", 0.0)
            self.cum_info_official_pnl = getattr(self, "cum_info_official_pnl", 0.0)
            self.cum_info_obs_pnl = getattr(self, "cum_info_obs_pnl", 0.0)
            self.cum_cost = getattr(self, "cum_cost", 0.0)

        trading_start_dt = pd.Timestamp(trading_start)
        if _shadow_step and trading_start_dt not in self.close.index:
            return self

        run_index = pd.DatetimeIndex([trading_start_dt]) if _shadow_step else self.close.loc[pd.Timestamp(warmup_start):pd.Timestamp(trading_end)].index
        for dt in run_index:
            if dt < pd.Timestamp(warmup_start): continue

            is_trading = pd.Timestamp(trading_start) <= dt <= pd.Timestamp(trading_end)
            open_prices = self.open.loc[dt]
            low_prices = self.low.loc[dt]
            close_prices = self.close.loc[dt]

            self.daily_v8_flow = 0.0
            self.daily_info_off_flow = 0.0
            self.daily_info_obs_flow = 0.0
            self.daily_cost = 0.0

            if is_trading:
                # 1. NEXT-SESSION EXECUTION: stock orders at open; V8 core at close.
                executed_symbols = set()

                # A. Execute explicit pending orders at their governed price.
                for order in list(self.pending_orders):
                    s = order.symbol
                    if order.order_type == "v8_rebalance":
                        if pd.isna(close_prices.at[s]):
                            continue
                    elif pd.isna(open_prices.at[s]):
                        continue

                    if order.order_type in ["sell", "trim", "drawdown_cut"]:
                        if s in self.positions:
                            state = self.positions[s]
                            sell_frac = 1.0 if order.order_type != "trim" else 1/3
                            sell_shares = state.shares * sell_frac if order.order_type == "trim" else state.shares
                            if order.order_type == "drawdown_cut":
                                sell_shares = state.shares * (1.0 - order.target_weight) # target_weight holds reduction ratio

                            is_obs = state.is_observation if hasattr(state, 'is_observation') else False
                            self._execute_trade(s, dt, open_prices.at[s], -sell_shares, order.order_type, is_info=True, is_observation=is_obs, event_id=state.event_id)
                            state.shares -= sell_shares
                            if order.order_type == "trim": state.trimmed = True
                            if state.shares <= 1e-6: self.positions.pop(s)
                            executed_symbols.add(s)

                    elif order.order_type == "buy":
                        # Rule C: Reject if gap > 12%
                        if order.high_vol_entry and pd.notna(close_prices.at[s]):
                            gap = (open_prices.at[s] / self.close.at[self.close.index[self.close.index.get_loc(dt)-1], s]) - 1
                            if gap > 0.12:
                                self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "gap_too_large_rule_c", "event_id": None})
                                continue

                        pre_buy_val = self.cash + sum(self.positions[k].shares * open_prices.at[k] for k in self.positions if pd.notna(open_prices.at[k])) + sum(self.v8_shares[k] * open_prices.at[k] for k in self.v8_shares if pd.notna(open_prices.at[k]))
                        target_val = pre_buy_val * order.target_weight
                        current_val = self.positions[s].shares * open_prices.at[s] if s in self.positions else 0
                        buy_shares = (target_val - current_val) / open_prices.at[s] if target_val > current_val else 0

                        if buy_shares > 0:
                            actual_buy = self._execute_trade(s, dt, open_prices.at[s], buy_shares, "buy", is_info=True, is_observation=order.is_observation, event_id=order.event_id)
                            if actual_buy > 0:
                                if s in self.positions:
                                    self.positions[s].shares += actual_buy
                                    self.positions[s].is_observation = False # Upgraded
                                else:
                                    self.positions[s] = PositionState(open_prices.at[s], actual_buy, order.stop_price, order.theme, order.score, order.r_risk)
                                    self.positions[s].trailing_stop = order.stop_price
                                    self.positions[s].peak = open_prices.at[s]
                                    self.positions[s].is_observation = order.is_observation
                                    self.positions[s].event_day_low = order.event_day_low
                                    self.positions[s].qqq_entry = open_prices.at["QQQ"] if pd.notna(open_prices.at["QQQ"]) else 0.0
                                    self.positions[s].event_id = order.event_id
                                executed_symbols.add(s)

                    elif order.order_type == "v8_rebalance":
                        pre_val = self.cash + sum(self.positions[k].shares * close_prices.at[k] for k in self.positions if pd.notna(close_prices.at[k])) + sum(self.v8_shares[k] * close_prices.at[k] for k in self.v8_shares if pd.notna(close_prices.at[k]))
                        target_val = pre_val * order.target_weight
                        current_val = self.v8_shares.get(s, 0) * close_prices.at[s]
                        diff_val = target_val - current_val
                        weight_diff = abs(diff_val) / pre_val if pre_val > 0 else 0
                        diff_shares = diff_val / close_prices.at[s] if close_prices.at[s] > 0 else 0

                        # Only trade if deviation > 2% AND nominal value > 0.5% NAV AND shares > 1e-6
                        if weight_diff > 0.02 and abs(diff_val) > pre_val * 0.005 and abs(diff_shares) >= 1e-6:
                            actual_diff = self._execute_trade(s, dt, close_prices.at[s], diff_shares, "v8_rebalance", is_info=False)
                            self.v8_shares[s] = self.v8_shares.get(s, 0) + actual_diff

                self.pending_orders.clear()

                # B. Execute Intraday Stops (If not already sold at open)
                for s, state in list(self.positions.items()):
                    if s not in executed_symbols and pd.notna(low_prices.at[s]):
                        if low_prices.at[s] < state.trailing_stop:
                            exit_px = min(open_prices.at[s], state.trailing_stop)
                            is_obs = state.is_observation if hasattr(state, 'is_observation') else False
                            self._execute_trade(s, dt, exit_px, -state.shares, "stop_loss", is_info=True, is_observation=is_obs, event_id=state.event_id)
                            self.positions.pop(s)

            # 2. END OF DAY: Valuation
            info_official_val = sum(state.shares * close_prices.at[s] for s, state in self.positions.items() if not getattr(state, 'is_observation', False) and pd.notna(close_prices.at[s]))
            info_obs_val = sum(state.shares * close_prices.at[s] for s, state in self.positions.items() if getattr(state, 'is_observation', False) and pd.notna(close_prices.at[s]))
            v8_val = sum(shares * close_prices.at[s] for s, shares in self.v8_shares.items() if pd.notna(close_prices.at[s]))

            self.value = self.cash + info_official_val + info_obs_val + v8_val
            info_val = info_official_val + info_obs_val

            # Exact PnL attribution calculation
            has_prior_valuation = len(equity) > 0 or (_shadow_step and hasattr(self, "prev_v8_val"))
            if has_prior_valuation:
                daily_v8_pnl = (v8_val - getattr(self, 'prev_v8_val', 0.0)) + self.daily_v8_flow
                daily_info_off_pnl = (info_official_val - getattr(self, 'prev_info_off_val', 0.0)) + self.daily_info_off_flow
                daily_info_obs_pnl = (info_obs_val - getattr(self, 'prev_info_obs_val', 0.0)) + self.daily_info_obs_flow

                self.cum_v8_pnl += daily_v8_pnl
                self.cum_info_official_pnl += daily_info_off_pnl
                self.cum_info_obs_pnl += daily_info_obs_pnl
                self.cum_cost += self.daily_cost

                # Verify exact closure
                expected_value = 1.0 + self.cum_v8_pnl + self.cum_info_official_pnl + self.cum_info_obs_pnl - self.cum_cost
                if abs(self.value - expected_value) >= 1e-4:
                    raise AssertionError(f"PnL attribution drift at {dt}: value={self.value}, expected={expected_value}")

                info_contrib = (daily_info_off_pnl + daily_info_obs_pnl) / self.value
            else:
                daily_v8_pnl = daily_info_off_pnl = daily_info_obs_pnl = 0.0
                info_contrib = 0.0

            self.prev_v8_val = v8_val
            self.prev_info_off_val = info_official_val
            self.prev_info_obs_val = info_obs_val

            if is_trading:
                self.highwater = max(self.highwater, self.value)
                dd = self.value / self.highwater - 1
                core_cap, info_cap, fear_gate = self._effective_sleeve_caps(dt)

                # 3. DRAWDOWN RULES
                v9_blocked = False
                if dd <= -0.25:
                    for s in self.positions:
                        self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                    v9_blocked = True
                elif dd <= -0.20:
                    v9_blocked = True
                    # Cap total equity to 50%
                    if (info_val + v8_val) / self.value > 0.50:
                        reduce_ratio = 0.50 / ((info_val + v8_val) / self.value)
                        for s in self.positions:
                            self.pending_orders.append(PendingOrder(s, reduce_ratio, dt, 0, 0, "drawdown_cut"))
                        for s in self.v8_shares:
                            self.pending_orders.append(PendingOrder(s, self.v8_shares[s] * close_prices.at[s] / self.value * reduce_ratio, dt, 0, 0, "v8_rebalance"))
                elif dd <= -0.15:
                    v9_blocked = True
                    # Info sleeve cut in half
                    for s in self.positions:
                        self.pending_orders.append(PendingOrder(s, 0.5, dt, 0, 0, "drawdown_cut"))
                elif dd <= -0.10:
                    v9_blocked = True

                # 4. GENERATE T+1 EXITS/TRIMS/UPGRADES
                for s, state in list(self.positions.items()):
                    if pd.isna(close_prices.at[s]): continue
                    state.days_held += 1
                    state.peak = max(state.peak, float(close_prices.at[s]))

                    if state.is_observation:
                        # Time stops
                        if state.days_held >= self.cfg.time_stop_days:
                            qqq_ret = (close_prices.at["QQQ"] / state.qqq_entry - 1) if state.qqq_entry > 0 else 0
                            my_ret = (close_prices.at[s] / state.entry - 1)
                            if my_ret <= qqq_ret:
                                self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                                continue

                        if state.days_held >= 5 and close_prices.at[s] <= state.entry:
                            self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                            continue

                        if close_prices.at[s] < state.event_day_low:
                            self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                            continue

                        # Upgrade logic
                        px = float(close_prices.at[s])
                        m20 = float(self.ma20.at[dt, s])
                        m50 = float(self.ma50.at[dt, s])
                        rs = float(self.rs20.at[dt, s])

                        upgrade = False
                        if self.cfg.upgrade_trigger == "second_conf" and px > m20 and px > m50 and rs > 0:
                            upgrade = True
                        elif self.cfg.upgrade_trigger == "break_high" and px > state.peak:
                            upgrade = True

                        if upgrade and not v9_blocked and fear_gate["max_new_buy_exposure"] > 0:
                            # Upgrade target weight to what it normally would be
                            single_cap = 0.15 if state.score >= 80 else self.cfg.max_single
                            current_info_weight = info_val / self.value if self.value > 0 else 0.0
                            full_size = min(
                                self.score_cap(state.score) * fear_gate["risk_multiplier"],
                                single_cap,
                                max(0.0, info_cap - current_info_weight),
                                fear_gate["max_new_buy_exposure"],
                            )
                            if full_size >= .005:
                                self.pending_orders.append(PendingOrder(s, full_size, dt, state.score, state.initial_stop, "buy", event_id=state.event_id))

                    if state.days_held >= self.cfg.event_life_days:
                        self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                    elif close_prices.at[s] < self.ma50.at[dt, s]:
                        self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "sell"))
                    elif not state.trimmed and state.r_risk > 0:
                        if (close_prices.at[s] - state.entry) / state.r_risk >= self.cfg.trim_r_multiple:
                            self.pending_orders.append(PendingOrder(s, 0, dt, 0, 0, "trim"))

                    # Update trailing stop
                    state.trailing_stop = self._technical_staged_stop(s, state, dt, float(close_prices.at[s]))

                # 5. V8 CORE ORDERS
                v8_targets = self.v8_base_weights.get(dt, {})
                prev_dt = self.close.index[max(0, self.close.index.get_loc(dt)-1)]
                prev_v8_targets = self.v8_base_weights.get(prev_dt, {})
                prev_core_cap, _, _ = self._effective_sleeve_caps(prev_dt)

                assert sum(v8_targets.values()) <= 1.0, f"V8 targets sum to {sum(v8_targets.values())} > 1.0"

                for s in ("SPY", "QQQ"):
                    target_w = v8_targets.get(s, 0) * core_cap
                    prev_w = prev_v8_targets.get(s, 0) * prev_core_cap

                    bootstrap = target_w > 0 and not any(self.v8_shares.values()) and not any(row["reason"] == "v8_rebalance" for row in self.ledger)
                    # Formal V8 allows target-change trades only. Between signals, weights drift.
                    if target_w != prev_w or bootstrap:
                        self.pending_orders.append(PendingOrder(s, target_w, dt, 0, 0, "v8_rebalance"))

                # 5b. Safety Checks
                assert self.cash >= -1e-9, f"Cash deficit {self.cash}"

                # 6. INFO CANDIDATE GENERATION & FUNNEL
                # A. Evaluate Waitlist Transitions

                market_panic = fear_gate["regime"] == "panic"

                for key in list(self.waitlist.keys()):
                    w_state = self.waitlist[key]
                    s = key[1]
                    w_state["days_waited"] += 1

                    if w_state["days_waited"] > 10:
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": f"waitlist_expired_{w_state['rule']}", "event_id": key[0]})
                        del self.waitlist[key]
                        continue

                    px = float(close_prices.at[s]) if pd.notna(close_prices.at[s]) else 0
                    if px == 0: continue
                    m20 = float(self.ma20.at[dt, s]) if pd.notna(self.ma20.at[dt, s]) else 0
                    m50 = float(self.ma50.at[dt, s]) if pd.notna(self.ma50.at[dt, s]) else 0
                    atr = float(self.atr20.at[dt, s]) if pd.notna(self.atr20.at[dt, s]) else 0
                    rs = float(self.rs20.at[dt, s]) if pd.notna(self.rs20.at[dt, s]) else 0

                    if px < m50 or rs < 0 or market_panic or (s in self.positions):
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "waitlist_cancelled", "event_id": key[0]})
                        del self.waitlist[key]
                        continue

                    w_state["pullback_low"] = min(w_state.get("pullback_low", float('inf')), float(self.low.at[dt, s]) if pd.notna(self.low.at[dt, s]) else px)

                    if w_state["rule"] == "D1":
                        if (px - m20) <= 2 * atr and px > m20 and px > m50 and rs > 0 and px >= open_prices.at[s] and not market_panic:
                            w_state["trigger_buy"] = True

                    elif w_state["rule"] == "D2":
                        # Check touching MA20
                        if px > m20 and rs > 0:
                            # 3 days rolling check: 2 of 3 days > QQQ
                            dt_loc = self.close.index.get_loc(dt)
                            if dt_loc >= 3:
                                outperf_days = 0
                                for i in range(dt_loc - 2, dt_loc + 1):
                                    idx = self.close.index[i]
                                    if pd.notna(self.close.at[idx, s]) and pd.notna(self.close.at[idx, "QQQ"]):
                                        prev_idx = self.close.index[i-1]
                                        my_ret = self.close.at[idx, s] / self.close.at[prev_idx, s] - 1
                                        qq_ret = self.close.at[idx, "QQQ"] / self.close.at[prev_idx, "QQQ"] - 1
                                        if my_ret > qq_ret: outperf_days += 1
                                if outperf_days >= 2:
                                    w_state["trigger_buy"] = True

                # B. Evaluate Capacity Queue Transitions
                for key in list(self.capacity_queue.keys()):
                    q_state = self.capacity_queue[key]
                    s = key[1]
                    q_state["days_waited"] += 1

                    if q_state["days_waited"] > 5 or s in self.positions or market_panic:
                        del self.capacity_queue[key]
                        continue

                    px = float(close_prices.at[s]) if pd.notna(close_prices.at[s]) else 0
                    if px > self.ma20.at[dt, s] and self.rs20.at[dt, s] > 0:
                        q_state["trigger_buy"] = True

                # C. Scan New Events
                symbols = sorted({s for e in self.events for s in e.symbols if s in self.close})
                candidates = []

                theme_exposure = self._theme_exposure(close_prices)
                info_exposure = info_val / self.value

                for s in symbols:
                    reason = ""
                    e = self._event_for(s, dt)
                    if not e:
                        continue

                    key = (e.event_id, s)
                    if s in self.positions or any(o.symbol == s for o in self.pending_orders if o.order_type in ["buy", "sell"]):
                        continue # Already holding or pending

                    if key in self.waitlist:
                        if self.waitlist[key].get("trigger_buy"):
                            w_state = self.waitlist[key]
                            candidates.append({"symbol": s, "score": w_state["score"], "theme": e.theme,
                                               "initial_stop": close_prices.at[s] * (1 - self.cfg.hard_stop),
                                               "high_vol": False, "is_observation": True, "event_id": e.event_id,
                                               "waitlist_key": key, "rule": w_state["rule"], "pullback_low": w_state.get("pullback_low")})
                        continue

                    if key in self.capacity_queue:
                        if self.capacity_queue[key].get("trigger_buy"):
                            q_state = self.capacity_queue[key]
                            candidates.append({"symbol": s, "score": q_state["score"], "theme": e.theme,
                                               "initial_stop": close_prices.at[s] * (1 - self.cfg.hard_stop),
                                               "high_vol": False, "is_observation": False, "event_id": e.event_id,
                                               "queue_key": key, "rule": q_state["rule"]})
                        continue

                    valid, path, tech, tech_reason, high_vol = self._tech_setup(s, dt, e.effective_at.normalize())
                    fun = self._fundamental_score(e, s, dt)
                    if not self._trusted_event_eligible(e, s, dt):
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "trusted_event_quality_floor", "event_id": e.event_id})
                        continue
                    event_score = e.source_completeness + e.thesis_novelty + fun - (e.crowding_penalty * self.cfg.crowding_multiplier)
                    total_score = event_score + (tech * self.cfg.tech_weight)

                    # Entry Rule Logic Routing
                    if self.cfg.entry_rule_version in ["D1", "D1_D2", "E"]:
                        # E logic is a unified router
                        if tech_reason == "chase_both" and total_score >= self.cfg.score_threshold - 5 and fun >= self.cfg.min_fundamental:
                            self.waitlist[key] = {"rule": "D1", "days_waited": 0, "score": total_score, "pullback_low": float(self.low.at[dt, s])}
                            self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "added_to_d1_waitlist", "event_id": e.event_id})
                            continue
                        elif self.cfg.entry_rule_version in ["D1_D2", "E"] and self.cfg.score_threshold - 5 <= total_score < self.cfg.score_threshold and fun >= self.cfg.min_fundamental and valid:
                            self.waitlist[key] = {"rule": "D2", "days_waited": 0, "score": total_score, "pullback_low": float(self.low.at[dt, s])}
                            self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "added_to_d2_waitlist", "event_id": e.event_id})
                            continue
                        elif valid and total_score >= self.cfg.score_threshold:
                            candidates.append({"symbol": s, "score": total_score, "theme": e.theme, "initial_stop": close_prices.at[s] * (1 - self.cfg.hard_stop), "high_vol": False, "is_observation": False, "event_id": e.event_id, "fundamental": fun})
                        else:
                            self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": tech_reason if not valid else "score_below_threshold" if not high_vol else "chased_rule_a", "event_id": e.event_id})

                    elif self.cfg.entry_rule_version == "A":
                        if valid and total_score >= self.cfg.score_threshold:
                            candidates.append({"symbol": s, "score": total_score, "theme": e.theme, "initial_stop": close_prices.at[s] * (1 - self.cfg.hard_stop), "high_vol": False, "is_observation": False, "event_id": e.event_id, "fundamental": fun})
                        else:
                            self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": tech_reason if not valid else "score_below_threshold" if not high_vol else "chased_rule_a", "event_id": e.event_id})

                # Sort candidates by score descending
                candidates.sort(key=lambda x: x["score"], reverse=True)
                if v9_blocked or market_panic:
                    block_reason = "portfolio_drawdown_gate" if v9_blocked else "fear_gate_panic"
                    for cand in candidates:
                        self.funnel.append({"date": str(dt.date()), "symbol": cand["symbol"], "reason": block_reason, "event_id": cand.get("event_id")})
                    candidates = []
                flow_fragility = self._flow_fragility_score(dt) if self.cfg.institutional_flow_overlay else 0

                # Order Execution Logic for Candidates

                for cand in candidates:
                    s = cand["symbol"]
                    e_id = cand.get("event_id")

                    is_observation = cand.get("is_observation", False)
                    rule_type = cand.get("rule", "A")

                    if self.cfg.institutional_flow_overlay and flow_fragility >= 7 and cand.get("high_vol", False):
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "acute_flow_fragility_blocks_chase", "flow_fragility": flow_fragility, "event_id": e_id})
                        continue

                    if len(self.positions) + sum(1 for o in self.pending_orders if o.order_type == "buy") >= self.cfg.max_names:
                        if self.cfg.entry_rule_version == "E" and "queue_key" not in cand and "waitlist_key" not in cand:
                            self.capacity_queue[(e_id, s)] = {"rule": "Capacity", "days_waited": 0, "score": cand["score"]}
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "max_names_cap", "event_id": e_id})
                        continue

                    theme_bucket = self._theme_bucket(cand["theme"])
                    room_theme = self.cfg.max_theme - theme_exposure.get(theme_bucket, 0)
                    room_sleeve = info_cap - info_exposure
                    pending_new_buy = sum(o.target_weight for o in self.pending_orders if o.order_type == "buy")
                    room_new_buy = fear_gate["max_new_buy_exposure"] - pending_new_buy

                    if is_observation:
                        room_theme = min(room_theme, 0.06 - theme_exposure.get(theme_bucket, 0)) # Max 6% obs per common-factor theme

                    if room_theme <= 0:
                        if self.cfg.entry_rule_version == "E" and "queue_key" not in cand and "waitlist_key" not in cand:
                            self.capacity_queue[(e_id, s)] = {"rule": "Capacity", "days_waited": 0, "score": cand["score"]}
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "common_factor_theme_cap", "theme_bucket": theme_bucket, "event_id": e_id})
                        continue
                    if room_sleeve <= 0:
                        if self.cfg.entry_rule_version == "E" and "queue_key" not in cand and "waitlist_key" not in cand:
                            self.capacity_queue[(e_id, s)] = {"rule": "Capacity", "days_waited": 0, "score": cand["score"]}
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "sleeve_cap", "event_id": e_id})
                        continue
                    if room_new_buy <= 0 or market_panic:
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "fear_gate_new_buy_cap", "event_id": e_id})
                        continue

                    px = close_prices.at[s]

                    # Stop loss calculations
                    if rule_type == "D1":
                        cand["initial_stop"] = max(cand.get("pullback_low", px * 0.94), px * 0.94)
                    cand["initial_stop"] = self._initial_stop(s, dt, cand["initial_stop"])

                    dist = max(1e-4, px - cand["initial_stop"]) / px
                    risk_size = self.cfg.risk_per_name / dist
                    single_cap = 0.15 if cand["score"] >= 80 else self.cfg.max_single

                    size = min(self.score_cap(self._candidate_sizing_score(cand)), single_cap, risk_size, room_theme, room_sleeve, room_new_buy)
                    size *= fear_gate["risk_multiplier"]
                    if self.cfg.institutional_flow_overlay:
                        size *= .50 if flow_fragility >= 7 else .75 if flow_fragility >= 4 else 1.0
                    if self.cfg.institutional_quality_sizing:
                        fundamental = cand.get("fundamental", 10)
                        size *= self._quality_size_multiplier(fundamental)
                    if is_observation:
                        size = min(size, self.cfg.obs_size) # Cap observation size to 2%

                    if size < 0.005:
                        self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "below_minimum_order_size", "event_id": e_id})
                        continue

                    order = PendingOrder(s, size, dt, cand["score"], cand["initial_stop"], "buy", cand["theme"], px - cand["initial_stop"])
                    order.is_observation = is_observation
                    order.event_day_low = float(self.low.at[dt, s]) if pd.notna(self.low.at[dt, s]) else cand["initial_stop"]
                    order.event_id = e_id or ""

                    self.pending_orders.append(order)
                    theme_exposure[theme_bucket] = theme_exposure.get(theme_bucket, 0) + size
                    info_exposure += size
                    self.funnel.append({"date": str(dt.date()), "symbol": s, "reason": "accepted", "event_id": e_id})

                    if "waitlist_key" in cand:
                        del self.waitlist[cand["waitlist_key"]]
                    if "queue_key" in cand:
                        del self.capacity_queue[cand["queue_key"]]

                # Log state
                actual_weights = {s: (state.shares * close_prices.at[s] / self.value) for s, state in self.positions.items()}
                actual_weights.update({s: (shares * close_prices.at[s] / self.value) for s, shares in self.v8_shares.items()})
                weight_rows.append({"date": dt, **actual_weights, "cash": self.cash / self.value})
                equity.append(self.value)

                snapshot = self._build_decision_snapshot(dt, close_prices, dd, actual_weights)
                snapshot.update({
                    "info_contrib": info_contrib,
                    "v8_pnl": daily_v8_pnl,
                    "info_official_pnl": daily_info_off_pnl,
                    "info_obs_pnl": daily_info_obs_pnl,
                    "cost_pnl": self.daily_cost,
                    "pending_orders": [{"symbol": o.symbol, "type": o.order_type, "weight": o.target_weight} for o in self.pending_orders],
                })
                self.audit.append(snapshot)

        curve = pd.Series(equity, index=self.close.loc[trading_start:trading_end].index, name="V9")
        wf = pd.DataFrame(weight_rows).set_index("date").fillna(0)

        return V9Result(curve, wf, self.audit, {"turnover": self.turnover, "execution": "Stocks T+1 Open; V8 core T+1 Close"}, self.funnel, self.ledger)

    def _build_decision_snapshot(self, dt: pd.Timestamp, close_prices: pd.Series, drawdown: float, actual_weights: dict) -> dict:
        """Build the daily decision fields expected by run_v9_daily_execution."""
        v8_targets = self.v8_base_weights.get(dt, {})
        core_cap, stock_cap, fear_gate = self._effective_sleeve_caps(dt)
        final_target = {
            s: float(v8_targets.get(s, 0.0) * core_cap)
            for s in ("SPY", "QQQ")
        }
        for symbol, state in self.positions.items():
            price = close_prices.get(symbol)
            if pd.isna(price) or self.value <= 0:
                continue
            final_target[symbol] = float(state.shares * float(price) / self.value)

        stock_targets = {
            symbol: weight
            for symbol, weight in final_target.items()
            if symbol not in {"SPY", "QQQ"} and weight > 0
        }

        watchlist = []
        qualified = []
        symbols = sorted({s for e in self.events for s in e.symbols if s in self.close.columns})
        for symbol in symbols:
            event = self._event_for(symbol, dt)
            if event is None:
                continue
            valid, path, tech, tech_reason, high_vol = self._tech_setup(symbol, dt, event.effective_at.normalize())
            fun = self._fundamental_score(event, symbol, dt)
            event_score = (
                event.source_completeness
                + event.thesis_novelty
                + fun
                - (event.crowding_penalty * self.cfg.crowding_multiplier)
            )
            total_score = float(event_score + (tech * self.cfg.tech_weight if valid else 0.0))
            wait_key = (event.event_id, symbol)
            wait_rule = self.waitlist.get(wait_key, {}).get("rule")
            status = "hold" if symbol in self.positions else ("wait" if wait_rule else ("qualified" if valid and total_score >= self.cfg.score_threshold else "watch"))
            item = {
                "symbol": symbol,
                "score": total_score,
                "event": event.event_id,
                "theme": event.theme,
                "confirmed": bool(valid),
                "path": path if valid else "none",
                "status": status,
                "points_to_70": max(0.0, float(self.cfg.score_threshold) - total_score),
                "fundamental_validation": int(fun),
                "new_entries_allowed": bool(self.cfg.source_healthy),
                "tech_reason": tech_reason,
                "high_vol": bool(high_vol),
                "wait_rule": wait_rule,
            }
            watchlist.append(item)
            if status == "qualified":
                qualified.append(item)

        watchlist.sort(key=lambda row: row["score"], reverse=True)
        qualified.sort(key=lambda row: row["score"], reverse=True)

        return {
            "date": str(dt.date()),
            "drawdown": float(drawdown),
            "weights": actual_weights,
            "source_healthy": bool(self.cfg.source_healthy),
            "qualified": qualified,
            "watchlist": watchlist,
            "stock_targets": stock_targets,
            "final_target": final_target,
            "v8_base": {s: float(v8_targets.get(s, 0.0)) for s in ("SPY", "QQQ")},
            "fear_gate": fear_gate,
            "core_fear_gate": self._core_fear_gate(dt),
            "portfolio_limits": {
                "core_cap": float(core_cap),
                "stock_cap": float(stock_cap),
                "cash_floor": float(fear_gate["cash_floor"]),
                "max_gross_exposure": float(fear_gate["max_gross_exposure"]),
                "allocation_policy": self.cfg.fear_allocation_policy,
            },
            "ma_regime": {
                s: {
                    "above_ma150": bool(pd.notna(self.ma150.at[dt, s]) and self.close.at[dt, s] > self.ma150.at[dt, s]),
                    "above_ma200": bool(pd.notna(self.ma200.at[dt, s]) and self.close.at[dt, s] > self.ma200.at[dt, s]),
                    "score": float(v8_targets.get(s, 0.0) * 2.0),
                }
                for s in ("SPY", "QQQ")
            },
            "market_panic_vix35": bool(
                (self.vix.at[dt, "^VIX"] > 35)
                if (dt in self.vix.index and "^VIX" in self.vix.columns and pd.notna(self.vix.at[dt, "^VIX"]))
                else False
            ),
        }
