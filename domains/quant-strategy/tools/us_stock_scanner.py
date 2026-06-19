#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import numpy as np
import yfinance as yf

# Watchlist tickers from L1 Memory
WATCHLIST_TICKERS = [
    # 1. 存储/内存瓶颈
    "DRAM", "MU", "WDC", "STX", "SNDK",
    # 2. 光互连/定制芯片/光模块
    "MRVL", "AVGO", "ALAB", "COHR", "LITE", "AAOI", "MXL", "AXTI", "CRDO",
    # 3. AI服务器/机架整合
    "SMCI",
    # 4. AI工厂/云/数据库基建
    "ORCL",
    # 5. 半导体设备/测试/验证
    "TER", "ASML", "AMAT", "KLAC", "LRCX",
    # 6. 航天与卫星通信
    "RKLB", "RDW",
    # 7. 物理AI/自动驾驶
    "TSLA",
    # 8. 边缘推理/设备AI
    "QCOM",
    # 9. AI算力与PC/芯片代工
    "NVDA", "AMD", "INTC",
    # 10. 光纤与网络通信
    "GLW", "NOK",
    # 11. PCB与电子制造
    "TTMI"
]

def load_universe_symbols():
    # Read S&P 500 & Nasdaq 100 constituents from cached long-term file
    univ_path = Path("D:/code/AI-Memory/domains/quant-strategy/experiments/2026-05-29-dual-sleeve-backtest/datasets/data_universe/us_stock_universe_2000_2025.csv")
    symbols = []
    if univ_path.exists():
        try:
            df = pd.read_csv(univ_path, nrows=2)
            cols = [col for col in df.columns if col not in ["Date", "Unnamed: 0"]]
            symbols.extend(cols)
        except Exception as e:
            print(f"Warning: Failed to load symbols from {univ_path}: {e}")
    
    # Merge with manual watchlist
    merged = set(symbols + WATCHLIST_TICKERS)
    # Filter out empty or index symbols
    cleaned = {s.strip().upper() for s in merged if s and s.strip() and not s.startswith("^")}
    # Remove obsolete symbols if any
    cleaned.discard("SPY")
    cleaned.discard("QQQ")
    cleaned.discard("SNDK") # SNDK was acquired
    return sorted(list(cleaned))

def z_score(values):
    if len(values) < 2:
        return [0.0 for _ in values]
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return [0.0 for _ in values]
    return [(v - mean) / std for v in values]

def fetch_earnings_and_fundamentals(symbol):
    info_data = {
        "earnings_date": "N/A",
        "revenue_growth": None,
        "gross_margin": None,
        "debt_to_equity": None,
        "pe_ratio": None,
        "market_cap": None
    }
    try:
        ticker = yf.Ticker(symbol)
        
        # 1. Try to fetch earnings calendar
        try:
            calendar = ticker.calendar
            if calendar is not None and "Earnings Date" in calendar:
                dates = calendar["Earnings Date"]
                if isinstance(dates, list) and len(dates) > 0:
                    info_data["earnings_date"] = dates[0].strftime("%Y-%m-%d")
                elif hasattr(dates, "iloc") and len(dates) > 0:
                    info_data["earnings_date"] = dates.iloc[0].strftime("%Y-%m-%d")
        except Exception:
            pass
            
        # 2. Try to fetch fundamental info
        try:
            info = ticker.info
            if info:
                info_data["revenue_growth"] = info.get("revenueGrowth")
                info_data["gross_margin"] = info.get("grossMargins")
                info_data["debt_to_equity"] = info.get("debtToEquity")
                info_data["pe_ratio"] = info.get("trailingPE")
                info_data["market_cap"] = info.get("marketCap")
        except Exception:
            pass
            
    except Exception:
        pass
    return info_data

def check_earnings_alert(earnings_date_str):
    if not earnings_date_str or earnings_date_str == "N/A":
        return False, "N/A"
    try:
        earnings_date = datetime.strptime(earnings_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_diff = (earnings_date - today).days
        if 0 <= days_diff <= 7:
            return True, f"即将发布 ({days_diff} 天后: {earnings_date_str})"
        return False, earnings_date_str
    except Exception:
        return False, earnings_date_str

def main():
    parser = argparse.ArgumentParser(description="U.S. Quant Strategy Stock Scanner")
    parser.add_argument("--out", dest="out_path", help="Output path for Markdown report")
    args = parser.parse_args()

    print("Step 1: Loading scan universe symbols...")
    symbols = load_universe_symbols()
    print(f"Loaded {len(symbols)} symbols from constituents + watchlist.")

    # Include benchmarks & sector ETFs
    download_list = sorted(list(set(symbols + ["SPY", "QQQ", "SMH", "^VIX"])))

    print("\nStep 2: Fetching 1-year historical data via yfinance...")
    # Multi-threaded download is very fast
    data = yf.download(
        tickers=download_list,
        period="1y",
        auto_adjust=True,
        progress=False,
        threads=True
    )

    if data.empty:
        print("Error: Downloaded data is empty.")
        sys.exit(1)

    # Align columns
    close = data["Close"]
    
    # Check VIX separately (sometimes ^VIX is downloaded as VIX)
    vix_col = "^VIX" if "^VIX" in close.columns else ("VIX" if "VIX" in close.columns else None)
    
    # Clean data: drop rows where SPY is NaN (non-trading days)
    if "SPY" in close.columns:
        close = close.dropna(subset=["SPY"])
    # Forward fill to handle any temporary alignment NaNs
    close = close.ffill().bfill()
    
    print(f"Data shape after cleaning: {close.shape[0]} rows, {close.shape[1]} columns.")
    
    # Calculate indicators
    print("\nStep 3: Calculating technical indicators...")
    latest_dt = close.index[-1]
    print(f"Latest market close date: {latest_dt.strftime('%Y-%m-%d')}")

    ma50 = close.rolling(50, min_periods=30).mean()
    ma200 = close.rolling(200, min_periods=120).mean()
    mom21 = close / close.shift(21) - 1.0
    mom63 = close / close.shift(63) - 1.0
    mom126 = close / close.shift(126) - 1.0
    # Daily returns volatility over last 126 days
    daily_ret = close.pct_change()
    vol126 = daily_ret.rolling(126, min_periods=80).std()

    # Slicing the latest row values
    p_last = close.loc[latest_dt]
    ma50_last = ma50.loc[latest_dt]
    ma200_last = ma200.loc[latest_dt]
    mom21_last = mom21.loc[latest_dt]
    mom63_last = mom63.loc[latest_dt]
    mom126_last = mom126.loc[latest_dt]
    vol126_last = vol126.loc[latest_dt]

    # Calculate SPY drawdown
    spy_c = close["SPY"]
    spy_max_63 = spy_c.iloc[-63:].max()
    spy_dd_63 = (spy_c.iloc[-1] / spy_max_63) - 1.0

    # Calculate Market Fear Gate
    vix_val = p_last[vix_col] if vix_col else np.nan
    
    fear_points = 0
    if pd.notna(vix_val):
        if vix_val >= 35: fear_points += 4
        elif vix_val >= 30: fear_points += 3
        elif vix_val >= 22: fear_points += 2
        elif vix_val >= 16: fear_points += 1
        
    if spy_dd_63 <= -0.12: fear_points += 3
    elif spy_dd_63 <= -0.08: fear_points += 2
    elif spy_dd_63 <= -0.04: fear_points += 1
    
    spy_p = p_last["SPY"]
    spy_ma200 = ma200_last["SPY"]
    if pd.notna(spy_ma200) and spy_p < spy_ma200: fear_points += 3
    
    qqq_p = p_last["QQQ"]
    qqq_ma200 = ma200_last["QQQ"]
    if pd.notna(qqq_ma200) and qqq_p < qqq_ma200: fear_points += 3

    # Define Fear Regime
    if fear_points >= 9:
        fear_regime = "panic"
        risk_mult = 0.20
    elif fear_points >= 5:
        fear_regime = "stress"
        risk_mult = 0.50
    elif fear_points >= 3:
        fear_regime = "elevated"
        risk_mult = 0.75
    else:
        fear_regime = "normal"
        risk_mult = 1.00

    print(f"Cboe VIX: {vix_val:.2f}, SPY 63d DD: {spy_dd_63:.2%}")
    print(f"Fear Gate Score: {fear_points}/14, Active Regime: {fear_regime.upper()} (Risk Multiplier: {risk_mult:.0%})")

    # Step 4: V6 Multi-Factor Screen
    print("\nStep 4: Running V6 Multi-Factor Screen...")
    v6_pool = []
    benchmarks_and_etfs = {"SPY", "QQQ", "VTV", "IWD", "SCHD", "SMH", "^VIX", "VIX"}
    
    for symbol in symbols:
        if symbol in benchmarks_and_etfs or symbol not in p_last:
            continue
            
        p = p_last[symbol]
        m50 = ma50_last[symbol]
        m200 = ma200_last[symbol]
        m21 = mom21_last[symbol]
        m63 = mom63_last[symbol]
        m126 = mom126_last[symbol]
        v126 = vol126_last[symbol]
        
        if pd.isna(p) or pd.isna(m50) or pd.isna(m200) or pd.isna(m21) or pd.isna(m63) or pd.isna(m126) or pd.isna(v126):
            continue
            
        # Price and Trend Filter
        if p >= 5.0 and p > m50 and p > m200 and m63 > 0:
            quality_mom = m126 / v126 if v126 > 0 else 0
            v6_pool.append({
                "symbol": symbol,
                "price": p,
                "ma50": m50,
                "ma200": m200,
                "mom21": m21,
                "mom63": m63,
                "mom126": m126,
                "vol126": v126,
                "quality_mom": quality_mom
            })

    print(f"Found {len(v6_pool)} stocks satisfying V6 trend filters.")

    # Calculate V6 Scores using Z-scores
    v6_ranked = []
    if len(v6_pool) > 0:
        q_moms = [x["quality_mom"] for x in v6_pool]
        m63s = [x["mom63"] for x in v6_pool]
        m21s = [x["mom21"] for x in v6_pool]
        
        z_q = z_score(q_moms)
        z_m63 = z_score(m63s)
        z_m21 = z_score(m21s)
        
        for idx, item in enumerate(v6_pool):
            score = (0.4 * z_q[idx]) + (0.4 * z_m63[idx]) - (0.2 * z_m21[idx])
            item["score"] = score
            v6_ranked.append(item)
            
        v6_ranked.sort(key=lambda x: x["score"], reverse=True)

    # Step 5: V7 Double-Radar Screen
    print("\nStep 5: Running V7 Double-Radar Screen...")
    radar_pool = []
    
    # Radar Gate: QQQ > QQQ_MA200 and QQQ 126d mom > 0
    qqq_mom126 = mom126_last["QQQ"]
    radar_gate_open = qqq_p > qqq_ma200 and qqq_mom126 > 0
    
    print(f"Radar Gate status: {'OPEN' if radar_gate_open else 'CLOSED'} (QQQ vs MA200: {qqq_p:.2f}/{qqq_ma200:.2f}, QQQ 126d Mom: {qqq_mom126:.2%})")

    if radar_gate_open:
        for symbol in symbols:
            if symbol in benchmarks_and_etfs or symbol not in p_last:
                continue
                
            p = p_last[symbol]
            m50 = ma50_last[symbol]
            m200 = ma200_last[symbol]
            m21 = mom21_last[symbol]
            m63 = mom63_last[symbol]
            m126 = mom126_last[symbol]
            v126 = vol126_last[symbol]
            
            if pd.isna(p) or pd.isna(m50) or pd.isna(m200) or pd.isna(m21) or pd.isna(m63) or pd.isna(m126) or pd.isna(v126):
                continue
                
            vol_ann = v126 * np.sqrt(252)
            ext50 = (p / m50) - 1.0
            
            # Radar Rules: Close > MA50 & MA200, mom63 > 15%, mom126 > 25%, Vol_ann > 40%, Ext50 < 35%
            if (p >= 5.0 and p > m50 and p > m200 and 
                m63 > 0.15 and m126 > 0.25 and vol_ann > 0.40 and ext50 < 0.35):
                radar_pool.append({
                    "symbol": symbol,
                    "price": p,
                    "ma50": m50,
                    "ma200": m200,
                    "mom21": m21,
                    "mom63": m63,
                    "mom126": m126,
                    "vol_ann": vol_ann,
                    "ext50": ext50
                })
                
        print(f"Found {len(radar_pool)} stocks satisfying Double-Radar filters.")
        
        # Calculate Radar Scores using Z-Scores
        radar_ranked = []
        if len(radar_pool) > 0:
            r_m126 = [x["mom126"] for x in radar_pool]
            r_m63 = [x["mom63"] for x in radar_pool]
            r_vol = [x["vol_ann"] for x in radar_pool]
            r_m21 = [x["mom21"] for x in radar_pool]
            r_ext = [x["ext50"] for x in radar_pool]
            
            z_r_m126 = z_score(r_m126)
            z_r_m63 = z_score(r_m63)
            z_r_vol = z_score(r_vol)
            z_r_m21 = z_score(r_m21)
            z_r_ext = z_score(r_ext)
            
            for idx, item in enumerate(radar_pool):
                score = (0.5 * z_r_m126[idx]) + (0.25 * z_r_m63[idx]) + (0.15 * z_r_vol[idx]) - (0.1 * z_r_m21[idx]) - (0.1 * z_r_ext[idx])
                item["score"] = score
                radar_ranked.append(item)
                
            radar_ranked.sort(key=lambda x: x["score"], reverse=True)
    else:
        radar_ranked = []

    # Get Top Candidates
    top_v6 = v6_ranked[:10]
    top_radar = radar_ranked[:5]

    # Combine unique symbols for fundamental checks
    final_symbols = list(set([x["symbol"] for x in top_v6] + [x["symbol"] for x in top_radar]))
    
    print(f"\nStep 6: Fetching earnings dates and fundamentals for {len(final_symbols)} top candidates...")
    fundamentals = {}
    for idx, s in enumerate(final_symbols, start=1):
        print(f"[{idx}/{len(final_symbols)}] Fetching {s} info...")
        fundamentals[s] = fetch_earnings_and_fundamentals(s)
        time.sleep(0.3)

    # Attach fundamentals to candidates
    for item in top_v6:
        item["fundamentals"] = fundamentals[item["symbol"]]
    for item in top_radar:
        item["fundamentals"] = fundamentals[item["symbol"]]

    # Save to JSON
    output_data = {
        "observed_at": latest_dt.strftime("%Y-%m-%d"),
        "fear_gate": {
            "score": fear_points,
            "regime": fear_regime,
            "risk_multiplier": risk_mult,
            "vix": vix_val,
            "spy_dd_63": spy_dd_63
        },
        "v6_candidates": top_v6,
        "radar_candidates": top_radar
    }
    
    work_dir = Path("D:/code/AI-Memory/domains/quant-strategy/work")
    work_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = work_dir / "latest_scan_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"\nScan results successfully saved to JSON: {json_path}")

    # Generate Markdown Report (Chinese)
    md_lines = [
        f"# 美股量化策略选股扫描报告 ({latest_dt.strftime('%Y-%m-%d')})",
        "",
        "本报告根据 V5/V6/V7 量化策略要求，对美股核心板块及自选监控池进行了筛选。",
        "",
        "## 1. 市场风控状态 (Market Fear Gate)",
        "",
        f"- **恐慌得分：** `{fear_points}/14`",
        f"- **市场所处状态：** **{fear_regime.upper()}** (风险乘数：`{risk_mult:.0%}`)",
        f"- **Cboe VIX 指数：** `{vix_val:.2f}`",
        f"- **标普500近期最大回撤 (63d DD)：** `{spy_dd_63:.2%}`",
        "",
        "> [!NOTE]",
        f"当前市场环境为 **{fear_regime.upper()}**。新买入开仓应严格乘以 `{risk_mult:.0%}` 的风险乘数，如风控乘数较低或处于 PANIC，应暂停任何新买入操作，优先保留现金。",
        "",
        "## 2. V6 多因子核心候选股 (Top 10)",
        "筛选条件：Price >= $5.0，站上 MA50 和 MA200，mom63 > 0。按横截面 Z-Score 排序（+40% 质量动能，+40% 原始动能，-20% 短期反转）。",
        "",
        "| 排名 | 代码 | 现价 | mom63 | mom126 | 波动率 (126d) | 评分 | 预估下期财报日 | 营收增速 | 毛利率 | 警示状态 |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, item in enumerate(top_v6, start=1):
        s = item["symbol"]
        p = item["price"]
        m63 = item["mom63"]
        m126 = item["mom126"]
        v126 = item["vol126"]
        score = item["score"]
        
        fund = item["fundamentals"]
        e_date = fund["earnings_date"]
        rev_g = f"{fund['revenue_growth']:.2%}" if fund["revenue_growth"] is not None else "N/A"
        g_marg = f"{fund['gross_margin']:.2%}" if fund["gross_margin"] is not None else "N/A"
        
        is_alert, alert_text = check_earnings_alert(e_date)
        alert_flag = "⚠️ 财报前规避" if is_alert else "正常"
        
        md_lines.append(
            f"| {idx} | **{s}** | ${p:.2f} | {m63:.2%} | {m126:.2%} | {v126:.2%} | {score:.2f} | {alert_text} | {rev_g} | {g_marg} | {alert_flag} |"
        )

    md_lines.extend([
        "",
        "## 3. V7 双雷达高波段卫星股 (Top 5)",
        f"双雷达门槛 (Radar Gate)：**{'打开 (OPEN)' if radar_gate_open else '关闭 (CLOSED)'}**",
        "筛选条件：站上 MA50 和 MA200，mom63 > 15%，mom126 > 25%，年化波动率 > 40%，均线偏离度 < 35%。",
        "",
        "| 排名 | 代码 | 现价 | mom63 | mom126 | 年化波动率 | 偏离MA50 | 评分 | 预估下期财报日 | 营收增速 | 毛利率 | 警示状态 |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    if radar_gate_open and top_radar:
        for idx, item in enumerate(top_radar, start=1):
            s = item["symbol"]
            p = item["price"]
            m63 = item["mom63"]
            m126 = item["mom126"]
            vol_a = item["vol_ann"]
            ext50 = item["ext50"]
            score = item["score"]
            
            fund = item["fundamentals"]
            e_date = fund["earnings_date"]
            rev_g = f"{fund['revenue_growth']:.2%}" if fund["revenue_growth"] is not None else "N/A"
            g_marg = f"{fund['gross_margin']:.2%}" if fund["gross_margin"] is not None else "N/A"
            
            is_alert, alert_text = check_earnings_alert(e_date)
            alert_flag = "⚠️ 财报前规避" if is_alert else "正常"
            
            md_lines.append(
                f"| {idx} | **{s}** | ${p:.2f} | {m63:.2%} | {m126:.2%} | {vol_a:.2%} | {ext50:.2%} | {score:.2f} | {alert_text} | {rev_g} | {g_marg} | {alert_flag} |"
            )
    else:
        md_lines.append("| - | 没有符合条件的股票或雷达门槛关闭 | - | - | - | - | - | - | - | - | - | - |")

    md_lines.extend([
        "",
        "---",
        "**说明：** 本报告通过 yfinance 实时获取当日收盘及基本面财务数据进行动态过滤，所有个股需配合账户限额（HKD 40,000）、止损要求及 AI 定性财报分析方能正式执行交易建议。"
    ])

    report_content = "\n".join(md_lines) + "\n"
    
    if args.out_path:
        with open(args.out_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Markdown report saved to: {args.out_path}")
    else:
        default_md = work_dir / "latest_scan_results.md"
        with open(default_md, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Markdown report saved to default: {default_md}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
