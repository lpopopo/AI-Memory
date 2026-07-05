"""V9 Evaluation and Metric Calculation Framework."""
import numpy as np
import pandas as pd

def calculate_stats(curve: pd.Series) -> dict:
    if len(curve) < 2:
        return {"total_return": 0.0, "max_drawdown": 0.0, "annualized_sharpe": 0.0, "calmar": 0.0, "daily_win_rate": 0.0}
    curve = curve.dropna()
    if len(curve) == 0 or curve.iloc[0] == 0:
        return {"total_return": 0.0, "max_drawdown": 0.0, "annualized_sharpe": 0.0, "calmar": 0.0, "daily_win_rate": 0.0}
    curve = curve / curve.iloc[0]
    returns = curve.pct_change().dropna()
    dd = curve / curve.cummax() - 1
    total_ret = float(curve.iloc[-1] - 1)
    max_dd = float(dd.min())
    std = returns.std()
    sharpe = float(returns.mean() / std * np.sqrt(252)) if std > 0 else 0.0
    calmar = float(total_ret / abs(max_dd)) if max_dd < 0 else 0.0
    win_rate = float((returns > 0).mean()) if len(returns) > 0 else 0.0
    return {
        "total_return": total_ret,
        "max_drawdown": max_dd,
        "annualized_sharpe": sharpe,
        "calmar": calmar,
        "daily_win_rate": win_rate
    }

def evaluate_scheme(v9_equity: pd.Series, v8_equity: pd.Series, audit: list, ledger: list, cost_rate: float, execution_details: dict) -> dict:
    """
    Evaluates the V9 backtest run based on the STRICT Unified Evaluation Function.
    35% * Rel_V8 + 20% * Sharpe + 15% * Calmar + 10% * InfoContrib + 10% * WinRate - 5% * MaxDD_Penalty - 5% * Turnover_Penalty
    """
    v9_stats = calculate_stats(v9_equity)
    v8_stats = calculate_stats(v8_equity)
    
    rel_v8 = v9_stats["total_return"] - v8_stats["total_return"]
    sharpe = v9_stats["annualized_sharpe"]
    calmar = v9_stats["calmar"]
    win_rate = v9_stats["daily_win_rate"]
    max_dd = v9_stats["max_drawdown"]
    turnover = execution_details.get("turnover", 0.0)
    
    # Calculate true info contribution from audit
    info_contrib = sum(a.get("info_contrib", 0.0) for a in audit)
    
    # Count unique entries (BUY orders for info stocks)
    info_buys = [x for x in ledger if x["action"] == "BUY" and x["is_info"]]
    entries = len(info_buys)
    distinct_symbols = len(set(x["symbol"] for x in info_buys))
    trading_days = len(v9_equity)
    
    # Concentration check
    stock_pnl = {}
    for t in ledger:
        if t["is_info"]:
            sign = 1 if t["action"] == "SELL" else -1
            stock_pnl[t["symbol"]] = stock_pnl.get(t["symbol"], 0.0) + (t["shares"] * t["price"] * sign) - t["cost"]
            
    total_info_pnl = sum(stock_pnl.values())
    max_single_contrib = 0.0
    if total_info_pnl > 0:
        max_single_contrib = max(stock_pnl.values()) / total_info_pnl
        
    # Hard filters
    failed_filters = []
    
    # Sample criteria: >= 3 distinct events OR >= 30 trading days
    if distinct_symbols < 3 and trading_days < 30: 
        failed_filters.append("insufficient_evidence")
        
    if total_info_pnl > 0 and max_single_contrib > 0.60: failed_filters.append("single_stock_domination")
    if info_contrib <= 0: failed_filters.append("negative_info_contrib")
    if max_dd < v8_stats["max_drawdown"] - 0.05: failed_filters.append("severe_drawdown")
    
    # Calculate unified score
    score = (
        0.35 * rel_v8 * 100 + 
        0.20 * max(0, min(sharpe, 3.0)) + 
        0.15 * max(0, min(calmar, 5.0)) + 
        0.10 * info_contrib * 100 +
        0.10 * win_rate * 100 - 
        0.05 * abs(max_dd) * 100 - 
        0.05 * turnover * 10
    )
    
    # If it fails hard filters, heavily penalize to ensure it doesn't get picked
    if failed_filters:
        score = -999.0
    
    return {
        "unified_score": float(score),
        "total_return": v9_stats["total_return"],
        "max_drawdown": v9_stats["max_drawdown"],
        "annualized_sharpe": v9_stats["annualized_sharpe"],
        "calmar": v9_stats["calmar"],
        "rel_v8": rel_v8,
        "daily_win_rate": v9_stats["daily_win_rate"],
        "turnover": turnover,
        "entries": entries,
        "info_contrib": info_contrib,
        "max_single_contrib": max_single_contrib,
        "failed_filters": failed_filters
    }
