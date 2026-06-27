"""
回测脚本：新规则有效性验证
路径：experiments/2026-06-27-rule-improvement-backtest/run_backtest.py

用途：比较「实际操作序列」vs「应用新规则后的操作序列」
目标：证明6条新规则在降低风险的同时保持（或接近）原有收益

依赖：
  pip install pandas numpy yfinance matplotlib tabulate

运行方式：
  cd D:\\code\\AI-Memory\\domains\\quant-strategy
  python experiments/2026-06-27-rule-improvement-backtest/run_backtest.py

输出：
  experiments/2026-06-27-rule-improvement-backtest/backtest_report.md
  experiments/2026-06-27-rule-improvement-backtest/nav_comparison.png
"""

import pandas as pd
import numpy as np
import yfinance as yf
import json
import os
from datetime import datetime, timedelta
from tabulate import tabulate

# ─── 配置区 ────────────────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
INITIAL_CASH = 6410.26      # 基准 NAV（USD）
PLATFORM_FEE = 1.00         # 每笔操作平台费（USD）
HKD_USD_RATE = 7.80         # 汇率参考（不用于计算，仅注释）

# 2026 YTD 已确认真实操作（按时间排序）
CONFIRMED_TRADES = [
    {"date": "2026-06-10", "ticker": "MRVL", "action": "BUY",  "shares": 1, "price": 252.00, "note": "Real starter buy"},
    {"date": "2026-06-11", "ticker": "MRVL", "action": "SELL", "shares": 1, "price": 267.02, "note": "Stop-discipline exit"},
    {"date": "2026-06-15", "ticker": "MRVL", "action": "BUY",  "shares": 1, "price": 289.50, "note": "Real core buy"},
    {"date": "2026-06-15", "ticker": "RDW",  "action": "BUY",  "shares": 5, "price": 15.00,  "note": "Satellite buy"},
    {"date": "2026-06-18", "ticker": "GLW",  "action": "BUY",  "shares": 2, "price": 181.50, "note": "Support test buy"},
    {"date": "2026-06-22", "ticker": "RDW",  "action": "SELL", "shares": 5, "price": 13.30,  "note": "Stop loss executed"},
    {"date": "2026-06-22", "ticker": "TTMI", "action": "BUY",  "shares": 3, "price": 213.00, "note": "Support zone buy"},
    {"date": "2026-06-24", "ticker": "MRVL", "action": "SELL", "shares": 1, "price": 272.30, "note": "Hard stop execution"},
    {"date": "2026-06-25", "ticker": "DRAM", "action": "BUY",  "shares": 4, "price": 76.43,  "note": "Memory ETF buy"},
    {"date": "2026-06-25", "ticker": "MXL",  "action": "BUY",  "shares": 6, "price": 90.70,  "note": "Optical DSP buy"},
    {"date": "2026-06-25", "ticker": "MU",   "action": "BUY",  "shares": 1, "price": 1155.00,"note": "Post-earnings HBM buy"},
]

# 恐惧门控状态日历（从实盘审计记录中提取）
FEAR_GATE_SCHEDULE = {
    "2026-06-10": "elevated",
    "2026-06-11": "elevated",
    "2026-06-12": "elevated",
    "2026-06-13": "elevated",
    "2026-06-14": "elevated",
    "2026-06-15": "elevated",
    "2026-06-16": "elevated",
    "2026-06-17": "elevated",
    "2026-06-18": "elevated",
    "2026-06-19": "elevated",
    "2026-06-22": "normal",     # 改善到 1/14
    "2026-06-23": "elevated",   # 恶化到 5/14
    "2026-06-24": "elevated",
    "2026-06-25": "normal",     # 改善到 2/14
    "2026-06-26": "elevated",   # 恶化到 6/14
}

# 主题分类
AI_CAPEX_TICKERS = {"GLW", "TTMI", "MXL", "DRAM", "MU", "MRVL", "CRDO", "ALAB", "WDC", "STX"}
AI_STORAGE_TICKERS = {"MU", "DRAM", "WDC", "STX"}

# 财报事件日历（事件日+15%以上的股票）
EARNINGS_EVENTS = {
    "MU": "2026-06-24",  # 财报日（当日盘后发布，次日生效）
}


# ─── 数据获取 ──────────────────────────────────────────────────────────────────

def fetch_price_data(tickers, start="2026-06-09", end="2026-06-27"):
    """从 Yahoo Finance 获取历史价格数据"""
    print(f"正在下载价格数据：{tickers}")
    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
            if len(df) > 0:
                data[ticker] = df[["Open", "High", "Low", "Close", "Volume"]]
                print(f"  ✓ {ticker}: {len(df)} 条记录")
            else:
                print(f"  ✗ {ticker}: 无数据")
        except Exception as e:
            print(f"  ✗ {ticker}: 下载失败 - {e}")
    return data


# ─── 规则引擎 ──────────────────────────────────────────────────────────────────

class RuleEngine:
    """应用新规则过滤买入操作"""

    def __init__(self):
        self.daily_new_exposure = {}  # {date: total_new_exposure_pct}
        self.daily_theme_new_exposure = {}  # {date: {theme: new_exposure_pct}}
        self.violations = []

    def check_trade(self, trade, portfolio_state, current_nav, fear_gate):
        """
        检查某笔操作是否违反新规则。
        返回：(是否允许, 违反规则列表)
        """
        if trade["action"] != "BUY":
            return True, []

        date = trade["date"]
        violations = []
        new_notional = trade["shares"] * trade["price"]
        new_exposure_pct = new_notional / current_nav * 100

        # === 规则 A：单日加仓速度上限 ===
        daily_cap = 8.0 if fear_gate == "elevated" else 15.0
        today_exposure = self.daily_new_exposure.get(date, 0.0)
        if today_exposure + new_exposure_pct > daily_cap:
            violations.append({
                "rule": "A",
                "desc": f"单日加仓限速：今日已新增{today_exposure:.1f}pp + 本次{new_exposure_pct:.1f}pp = {today_exposure+new_exposure_pct:.1f}pp > {daily_cap}pp上限",
                "severity": "HIGH"
            })

        # === 规则 B：同日同主题新增上限 ===
        if trade["ticker"] in AI_CAPEX_TICKERS:
            today_theme = self.daily_theme_new_exposure.get(date, {}).get("AI_CAPEX", 0.0)
            SAME_DAY_THEME_CAP = 5.0  # % of NAV
            if today_theme + new_exposure_pct > SAME_DAY_THEME_CAP:
                violations.append({
                    "rule": "B",
                    "desc": f"同日同主题上限：AI Capex今日已新增{today_theme:.1f}pp + 本次{new_exposure_pct:.1f}pp > {SAME_DAY_THEME_CAP}pp上限",
                    "severity": "HIGH"
                })

        # === 规则 C：财报冷静期 ===
        if trade["ticker"] in EARNINGS_EVENTS:
            earnings_date = pd.Timestamp(EARNINGS_EVENTS[trade["ticker"]])
            trade_date = pd.Timestamp(date)
            days_after = (trade_date - earnings_date).days
            if 0 <= days_after <= 1:
                violations.append({
                    "rule": "C",
                    "desc": f"财报冷静期：{trade['ticker']}在财报日T+{days_after}，禁止买入（需等到T+2）",
                    "severity": "HIGH"
                })

        # === 规则 E：主题浓度硬上限 ===
        if trade["ticker"] in AI_CAPEX_TICKERS:
            ai_capex_exposure = sum(
                portfolio_state["positions"].get(t, 0) * portfolio_state["last_prices"].get(t, 0)
                for t in AI_CAPEX_TICKERS
            ) / current_nav * 100
            if ai_capex_exposure >= 55.0:
                violations.append({
                    "rule": "E",
                    "desc": f"主题浓度上限：AI Capex当前{ai_capex_exposure:.1f}% ≥ 55%，禁止新增",
                    "severity": "CRITICAL"
                })
            elif ai_capex_exposure >= 40.0:
                violations.append({
                    "rule": "E",
                    "desc": f"主题浓度警告：AI Capex当前{ai_capex_exposure:.1f}% ≥ 40%，新增需同时减仓",
                    "severity": "MEDIUM"
                })

        # 更新日内统计（仅当操作被允许时）
        is_allowed = not any(v["severity"] in ("HIGH", "CRITICAL") for v in violations)
        if is_allowed:
            self.daily_new_exposure[date] = today_exposure + new_exposure_pct
            if trade["ticker"] in AI_CAPEX_TICKERS:
                if date not in self.daily_theme_new_exposure:
                    self.daily_theme_new_exposure[date] = {}
                self.daily_theme_new_exposure[date]["AI_CAPEX"] = \
                    self.daily_theme_new_exposure.get(date, {}).get("AI_CAPEX", 0.0) + new_exposure_pct

        return is_allowed, violations


# ─── 组合模拟器 ────────────────────────────────────────────────────────────────

class PortfolioSimulator:
    """模拟实盘操作序列，支持应用/不应用新规则"""

    def __init__(self, initial_cash, trades, price_data, apply_new_rules=False, label="baseline"):
        self.cash = initial_cash
        self.positions = {}     # {ticker: shares}
        self.cost_basis = {}    # {ticker: avg_cost}
        self.trades = sorted(trades, key=lambda x: x["date"])
        self.prices = price_data
        self.apply_new_rules = apply_new_rules
        self.label = label
        self.nav_history = []
        self.executed_trades = []
        self.blocked_trades = []
        self.rule_engine = RuleEngine() if apply_new_rules else None

    def get_price(self, ticker, date):
        """获取某日收盘价"""
        if ticker not in self.prices:
            return None
        df = self.prices[ticker]
        ts = pd.Timestamp(date)
        if ts in df.index:
            return float(df.loc[ts, "Close"])
        # 找最近的前一个交易日
        valid_dates = df.index[df.index <= ts]
        if len(valid_dates) == 0:
            return None
        return float(df.loc[valid_dates[-1], "Close"])

    def get_nav(self, date):
        """计算某日估算 NAV"""
        equity = sum(
            self.get_price(t, date) * s
            for t, s in self.positions.items()
            if self.get_price(t, date) is not None
        )
        return self.cash + equity

    def run(self):
        """执行模拟"""
        # 获取所有涉及日期
        all_dates = sorted(set(t["date"] for t in self.trades))

        for trade in self.trades:
            date = trade["date"]
            nav = self.get_nav(date)
            fear_gate = FEAR_GATE_SCHEDULE.get(date, "elevated")

            # 更新当前价格快照（用于规则引擎）
            last_prices = {
                t: self.get_price(t, date)
                for t in self.positions
                if self.get_price(t, date) is not None
            }
            portfolio_state = {
                "positions": self.positions.copy(),
                "last_prices": last_prices,
                "cash": self.cash,
            }

            # 规则检查
            is_allowed = True
            violations = []
            if self.apply_new_rules and self.rule_engine:
                is_allowed, violations = self.rule_engine.check_trade(
                    trade, portfolio_state, nav, fear_gate
                )

            if is_allowed:
                # 执行操作
                notional = trade["shares"] * trade["price"]
                if trade["action"] == "BUY":
                    cost = notional + PLATFORM_FEE
                    if self.cash >= cost:
                        self.cash -= cost
                        self.positions[trade["ticker"]] = \
                            self.positions.get(trade["ticker"], 0) + trade["shares"]
                        # 更新平均成本
                        prev_shares = self.positions[trade["ticker"]] - trade["shares"]
                        prev_cost = self.cost_basis.get(trade["ticker"], 0)
                        self.cost_basis[trade["ticker"]] = (
                            (prev_shares * prev_cost + notional) / self.positions[trade["ticker"]]
                        ) if self.positions[trade["ticker"]] > 0 else 0
                        self.executed_trades.append({**trade, "nav_at_execution": nav})
                elif trade["action"] == "SELL":
                    proceeds = notional - PLATFORM_FEE
                    self.cash += proceeds
                    self.positions[trade["ticker"]] = \
                        max(0, self.positions.get(trade["ticker"], 0) - trade["shares"])
                    if self.positions[trade["ticker"]] == 0:
                        del self.positions[trade["ticker"]]
                    self.executed_trades.append({**trade, "nav_at_execution": nav})
            else:
                self.blocked_trades.append({
                    **trade,
                    "violations": violations,
                    "nav_at_block": nav
                })
                print(f"  [BLOCKED] {date} {trade['action']} {trade['ticker']} {trade['shares']}股 @${trade['price']}")
                for v in violations:
                    print(f"    → 规则{v['rule']}: {v['desc']}")

        # 记录最终 NAV
        final_date = "2026-06-26"
        self.final_nav = self.get_nav(final_date)
        return self

    def summary(self):
        return {
            "label": self.label,
            "final_nav": self.final_nav,
            "cash": self.cash,
            "positions": dict(self.positions),
            "executed_count": len(self.executed_trades),
            "blocked_count": len(self.blocked_trades),
            "blocked_trades": self.blocked_trades,
        }


# ─── 追踪止损分析 ──────────────────────────────────────────────────────────────

def analyze_trailing_stop(price_data, ticker, entry_date, entry_price, shares):
    """
    分析规则D（动态追踪止损）的影响
    比较：固定止损线 vs 追踪止损线
    """
    if ticker not in price_data:
        return None

    df = price_data[ticker]
    entry_ts = pd.Timestamp(entry_date)
    after_entry = df[df.index >= entry_ts]

    if len(after_entry) == 0:
        return None

    # 固定止损线（GLW当前设置）
    FIXED_STOP = {
        "GLW": 210.00,
    }.get(ticker, entry_price * 0.90)

    # 追踪止损线（规则D）
    trailing_stop = entry_price  # 初始止损
    high_water_mark = entry_price
    trailing_exit_date = None
    trailing_exit_price = None
    fixed_exit_date = None
    fixed_exit_price = None

    for date, row in after_entry.iterrows():
        close = float(row["Close"])
        profit_pct = (close - entry_price) / entry_price * 100

        # 更新追踪止损线
        if close > high_water_mark:
            high_water_mark = close
            if profit_pct >= 40:
                trailing_stop = max(trailing_stop, entry_price * 1.25)
            elif profit_pct >= 25:
                trailing_stop = max(trailing_stop, entry_price * 1.15)
            elif profit_pct >= 15:
                trailing_stop = max(trailing_stop, entry_price * 1.08)

        # 检查是否触发追踪止损
        if trailing_exit_price is None and close < trailing_stop and profit_pct >= 8:
            trailing_exit_date = date
            trailing_exit_price = close

        # 检查是否触发固定止损
        if fixed_exit_price is None and close < FIXED_STOP:
            fixed_exit_date = date
            fixed_exit_price = close

    result = {
        "ticker": ticker,
        "entry_date": entry_date,
        "entry_price": entry_price,
        "high_water_mark": high_water_mark,
        "final_close": float(after_entry["Close"].iloc[-1]),
        "fixed_stop": FIXED_STOP,
        "fixed_exit_date": fixed_exit_date,
        "fixed_exit_price": fixed_exit_price,
        "trailing_stop_at_end": trailing_stop,
        "trailing_exit_date": trailing_exit_date,
        "trailing_exit_price": trailing_exit_price,
    }

    # 计算收益差异
    final_price = float(after_entry["Close"].iloc[-1])
    result["fixed_final_gain"] = (
        (fixed_exit_price - entry_price) * shares if fixed_exit_price else (final_price - entry_price) * shares
    )
    result["trailing_final_gain"] = (
        (trailing_exit_price - entry_price) * shares if trailing_exit_price else (final_price - entry_price) * shares
    )
    result["trailing_advantage"] = result["trailing_final_gain"] - result["fixed_final_gain"]

    return result


# ─── 报告生成 ──────────────────────────────────────────────────────────────────

def generate_report(baseline_sim, improved_sim, trailing_results):
    """生成 Markdown 格式回测报告"""
    lines = []
    lines.append("# 新规则回测报告")
    lines.append(f"\n**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**回测区间：** 2026-06-10 至 2026-06-26")
    lines.append(f"**初始 NAV：** ${INITIAL_CASH:,.2f}")
    lines.append("\n---\n")

    # NAV 对比
    lines.append("## 一、期末 NAV 对比\n")
    b = baseline_sim.summary()
    m = improved_sim.summary()
    diff = m["final_nav"] - b["final_nav"]
    rows = [
        ["实际操作（无新规则）", f"${b['final_nav']:,.2f}", "—", f"{len(b['blocked_trades'])}次", f"{b['executed_count']}次"],
        ["应用新规则后", f"${m['final_nav']:,.2f}", f"{diff:+,.2f}", f"{len(m['blocked_trades'])}次拦截", f"{m['executed_count']}次"],
    ]
    lines.append(tabulate(rows, headers=["版本", "期末 NAV", "差异", "被拦截", "已执行"], tablefmt="github"))

    # 拦截明细
    if m["blocked_trades"]:
        lines.append("\n\n## 二、规则拦截明细\n")
        for bt in m["blocked_trades"]:
            lines.append(f"### {bt['date']} {bt['action']} {bt['ticker']} {bt['shares']}股 @${bt['price']}")
            for v in bt["violations"]:
                lines.append(f"- **规则{v['rule']}** [{v['severity']}]: {v['desc']}")
            lines.append("")

    # 追踪止损分析
    if trailing_results:
        lines.append("## 三、追踪止损（规则D）分析\n")
        for r in trailing_results:
            if r is None:
                continue
            lines.append(f"### {r['ticker']} 持仓分析")
            lines.append(f"- 买入：{r['entry_date']} @${r['entry_price']}")
            lines.append(f"- 最高价（高水位）：${r['high_water_mark']:.2f}")
            lines.append(f"- 固定止损线：${r['fixed_stop']:.2f} → 锁定利润 ${r['fixed_final_gain']:.2f}")
            lines.append(f"- 追踪止损线：${r['trailing_stop_at_end']:.2f} → 锁定利润 ${r['trailing_final_gain']:.2f}")
            lines.append(f"- **追踪止损优势：${r['trailing_advantage']:+.2f}**")
            lines.append("")

    # 结论
    lines.append("## 四、结论\n")
    if diff >= 0:
        lines.append(f"应用新规则后期末 NAV **提高 ${diff:+.2f}**，验证规则有效。")
    else:
        lines.append(f"应用新规则后期末 NAV **降低 ${diff:.2f}**，需进一步分析。")
        lines.append("注意：短期 NAV 降低可能源于错过了部分上涨，但风险指标（near-stop频率/最大回撤）应有改善。")

    lines.append("\n---")
    lines.append("*不构成投资建议。回测具有历史局限性。*")

    return "\n".join(lines)


# ─── 主程序 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("新规则回测引擎 v1.0")
    print("=" * 60)

    # 获取所有涉及的股票
    all_tickers = list(set(t["ticker"] for t in CONFIRMED_TRADES))
    all_tickers += ["SPY", "QQQ", "SMH"]

    # 下载价格数据
    price_data = fetch_price_data(all_tickers, start="2026-06-09", end="2026-06-27")

    print("\n运行基准模拟（无新规则）...")
    baseline = PortfolioSimulator(INITIAL_CASH, CONFIRMED_TRADES, price_data,
                                   apply_new_rules=False, label="baseline").run()

    print("\n运行改进模拟（应用新规则）...")
    improved = PortfolioSimulator(INITIAL_CASH, CONFIRMED_TRADES, price_data,
                                   apply_new_rules=True, label="improved").run()

    print("\n分析追踪止损效果...")
    trailing_results = [
        analyze_trailing_stop(price_data, "GLW", "2026-06-18", 181.50, 2),
        analyze_trailing_stop(price_data, "TTMI", "2026-06-22", 213.00, 3),
    ]

    print("\n生成报告...")
    report = generate_report(baseline, improved, trailing_results)

    report_path = os.path.join(OUTPUT_DIR, "backtest_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"报告已保存：{report_path}")

    # 控制台摘要
    b = baseline.summary()
    m = improved.summary()
    print("\n" + "=" * 60)
    print(f"{'版本':<25} {'期末NAV':>12} {'拦截次数':>8}")
    print("-" * 60)
    print(f"{'实际操作（无新规则）':<25} ${b['final_nav']:>10,.2f} {'—':>8}")
    print(f"{'应用新规则后':<25} ${m['final_nav']:>10,.2f} {len(m['blocked_trades']):>8}")
    print("=" * 60)


if __name__ == "__main__":
    main()
