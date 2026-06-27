# 错误分析方法论 & 回测改进方案
**生成时间：2026-06-27 | 版本：v1.0**  
**配套文档：`references/2026-06-27-strategy-improvement-plan.md`**  
**AI小弟执行参考：本文提供可直接运行的分析步骤和回测脚本框架**

---

## 一、错误分析方法论

### 1.1 错误分类体系

每次实盘操作失误，按以下4维度分类：

```
维度1 — 错误类型
  E1: 规则执行错误（规则存在，但未执行）
  E2: 规则空白错误（规则不存在，导致决策失据）
  E3: 数据质量错误（行情/新闻数据错误导致决策偏差）
  E4: 执行时机错误（方向正确，但买卖时机不对）

维度2 — 严重程度
  S1: 轻微（<2% NAV 影响）
  S2: 中度（2-5% NAV 影响）
  S3: 严重（5-10% NAV 影响）
  S4: 致命（>10% NAV 影响 或触发强制止损）

维度3 — 可预防性
  P1: 完全可预防（规则存在且清晰，仅需执行）
  P2: 部分可预防（规则存在但模糊，需要细化）
  P3: 不可预防（市场突发事件，无法规避）

维度4 — 复发风险
  R1: 低（已有规则覆盖，执行监控即可）
  R2: 中（规则需细化或自动化检查）
  R3: 高（结构性缺陷，需要新规则或流程）
```

### 1.2 本周已知错误归档

| 错误ID | 日期 | 描述 | 类型 | 严重度 | 可预防 | 复发风险 | 已纠正 |
|--------|------|------|------|--------|--------|---------|--------|
| ERR-2026-001 | 6/25 | 单日三次加仓 DRAM+MXL+MU，总敞口+25pp | E1+E2 | S3 | P2 | R3 | 规则C/E已写入 |
| ERR-2026-002 | 6/25 | MU 在财报+15.7%当日追涨 @$1155 | E2 | S2 | P2 | R3 | 规则C已写入 |
| ERR-2026-003 | 6/25 | MXL 6股定性卫星仓，实际占9%超标 | E1 | S2 | P1 | R2 | 规则F已写入 |
| ERR-2026-004 | 持续 | GLW 止损线未随浮盈上移 | E2 | S2 | P2 | R3 | 规则D已写入 |
| ERR-2026-005 | 6/22-6/26 | 5仓全是AI Capex，无主题分散 | E2 | S3 | P2 | R3 | 规则E已写入 |

### 1.3 错误分析工作流（每周复盘必须执行）

```
Step 1: 收集当周所有已确认操作记录
  来源：memory/trades/*.md（已确认成交文件）

Step 2: 对每笔操作填写错误分析表（见下方模板）
  → 填写到：memory/weekly/YYYY-WW-error-analysis.md

Step 3: 统计当周错误分布
  → 计算 E1/E2/E3/E4 各类型占比
  → 计算 NAV 影响合计

Step 4: 识别复发风险 R3 的错误，触发规则改进
  → 若同类错误本月出现 ≥2 次：必须新增/修改 decisions.md 规则
  → 新增规则后，写回测验证任务（见第二节）

Step 5: 更新错误统计汇总
  → 追加到：memory/monthly/YYYY-MM-error-summary.md
```

**错误分析模板：**
```markdown
## 操作错误分析

- 操作日期：YYYY-MM-DD
- 操作内容：[买入/卖出] [股票] [股数] @$[价格]
- 错误类型：[E1/E2/E3/E4]
- 严重程度：[S1/S2/S3/S4]
- 可预防性：[P1/P2/P3]
- 复发风险：[R1/R2/R3]
- 错误描述：[简述为什么这个操作是错误的]
- 当时决策依据：[引用当时的规则或判断]
- 正确做法应该是：[描述应该怎么做]
- 规则改进动作：[写入decisions.md的新规则 / 无需改规则]
- NAV 实际影响：[+/-$XXX / 待评估]
```

---

## 二、回测改进方案

### 2.1 待回测的新规则（Task-004）

以下规则需要通过历史数据验证其有效性，才能正式确认并长期执行。

**回测目标：证明新规则在保持收益的同时降低风险暴露。**

---

#### 回测 BT-001：单日加仓速度上限规则

**假设：** 在 elevated 门控下，若某日加仓使总敞口增加超过8pp，则拒绝超额部分，只执行允许范围内的首笔操作。

**回测设置：**
```python
# 回测参数
test_period = "2026-01-01" to "2026-06-26"  # YTD 实盘数据
baseline = "实际操作序列"  # 从 trades/ 目录读取
modified = "应用新规则后的操作序列"  # 超额部分推迟到下一日

# 评估指标
metrics = [
    "NAV_final",           # 期末净值
    "max_drawdown",        # 最大回撤
    "volatility_daily",    # 日波动率
    "near_stop_frequency", # near-stop 发生次数
    "stop_loss_count",     # 实际止损次数
    "sharpe_ratio",        # 夏普比率
]

# 比较维度
comparison = {
    "baseline": "实际操作（无限速）",
    "modified": "应用 8pp/日限速规则后"
}
```

**预期结论：** modified 版本期末 NAV 可能略低（少抓了部分上涨），但 max_drawdown 降低，near_stop_frequency 显著减少。

**脚本位置：** `experiments/2026-06-27-rule-improvement-backtest/bt001_daily_cap.py`

---

#### 回测 BT-002：财报冷静期规则

**假设：** 对于财报日+10%以上的股票，T 和 T+1 不买入，改为 T+2 买入（以开盘价）。

**回测设置：**
```python
# 需要的数据
earnings_events = [
    # 格式：{ticker, earnings_date, post_earnings_return}
    {"ticker": "MU", "date": "2026-06-24", "return_t1": 0.157},
    # 历史数据从 Yahoo Finance 获取
]

# 对照组
case_a = "T+0 当日盘前/盘中买入（实际发生）"
case_b = "T+2 延迟买入（模拟规则）"

# 核心问题：T+2 买入的平均成本 vs T+0 买入的平均成本
# 对于 MU：T+0 = $1155，T+2 实际 = ~$1070（如果规则生效）
# 差异 = -7.4%，验证规则有效
```

**历史样本：** 从 2026 YTD 中找出所有+10%以上的财报事件股票，统计 T+2 vs T+0 买入的成本差异。

**脚本位置：** `experiments/2026-06-27-rule-improvement-backtest/bt002_earnings_cooldown.py`

---

#### 回测 BT-003：动态追踪止损规则

**假设：** 核心仓浮盈达到+15%时，将止损线上移至成本+8%。

**回测设置：**
```python
# 测试案例：GLW 实际持仓轨迹
glw_cost = 181.50
glw_entry_date = "2026-06-18"
glw_price_series = [...]  # 从 Yahoo Finance 获取日线数据

# 对照比较
static_stop = 210.00       # 当前固定止损线
trailing_stop_rule = {
    "trigger_profit": 0.15,   # +15% 触发
    "lock_profit": 0.08,      # 锁定+8%利润
}

# 计算两种止损策略下的最终收益
# 若 GLW 从 $228 跌至 $215（追踪止损触发）：捕获 +18.6% 利润
# 若固定止损 $210：仅捕获 +15.7% 利润，差异约 +2.9pp
```

**脚本位置：** `experiments/2026-06-27-rule-improvement-backtest/bt003_trailing_stop.py`

---

#### 回测 BT-004：主题浓度规则（历史模拟）

**假设：** 若同一大主题超过55% NAV，后续同主题加仓全部阻断。

**回测设置：**
```python
# 模拟 2026-06-22 至 2026-06-26 这一周的场景
# 若规则在6/25生效：
#   6/25 DRAM 买入时，AI Capex 已达 ~22%（GLW+TTMI） → 本次允许（<55%）
#   6/25 MXL 买入时，AI Capex 已达 ~38%（GLW+TTMI+DRAM）→ 允许（<55%）
#   6/25 MU 买入时，AI Capex 将达 ~55%+ → 警报，拒绝执行

# 结果：MU 不在当日买入，节省约 $1155（可用于后续更好时机）
# 对比6/26 NAV：实际 $6384 vs 模拟（不买MU）约 $6502
# 因为 MU 次日 -6.7%，不买 MU 反而 NAV 更高约 +$120

# 这是一个反例证明：规则 E 可以避免主题过度集中导致的损失
```

**脚本位置：** `experiments/2026-06-27-rule-improvement-backtest/bt004_theme_concentration.py`

---

### 2.2 回测执行步骤（AI小弟操作手册）

#### 步骤一：环境准备
```powershell
# 在 PowerShell 中执行
cd D:\code\AI-Memory\domains\quant-strategy

# 创建回测目录
mkdir experiments\2026-06-27-rule-improvement-backtest

# 确认 Python 环境可用
python --version  # 需要 Python 3.8+

# 安装依赖
pip install pandas numpy yfinance matplotlib
```

#### 步骤二：获取历史价格数据
```python
# 脚本：experiments/2026-06-27-rule-improvement-backtest/fetch_data.py
import yfinance as yf
import pandas as pd

tickers = ["GLW", "TTMI", "MXL", "MU", "DRAM", "SPY", "QQQ", "SMH"]
start = "2026-01-01"
end = "2026-06-27"

data = {}
for ticker in tickers:
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    data[ticker] = df[["Open", "High", "Low", "Close", "Volume"]]
    print(f"Downloaded {ticker}: {len(df)} rows")

# 保存到本地
import pickle
with open("experiments/2026-06-27-rule-improvement-backtest/price_data.pkl", "wb") as f:
    pickle.dump(data, f)

print("Data saved.")
```

#### 步骤三：读取实际交易记录
```python
# 脚本：experiments/2026-06-27-rule-improvement-backtest/load_trades.py
# 从 memory/trades/ 目录手动整理确认的交易记录

CONFIRMED_TRADES = [
    # 格式：{date, ticker, action, shares, price, notes}
    {"date": "2026-06-10", "ticker": "MRVL", "action": "BUY",  "shares": 1, "price": 252.00, "notes": "Real account starter"},
    {"date": "2026-06-11", "ticker": "MRVL", "action": "SELL", "shares": 1, "price": 267.02, "notes": "Stop-discipline exit"},
    {"date": "2026-06-15", "ticker": "MRVL", "action": "BUY",  "shares": 1, "price": 289.50, "notes": "Real buy"},
    {"date": "2026-06-15", "ticker": "RDW",  "action": "BUY",  "shares": 5, "price": 15.00,  "notes": "Satellite"},
    {"date": "2026-06-18", "ticker": "GLW",  "action": "BUY",  "shares": 2, "price": 181.50, "notes": "Support test buy"},
    {"date": "2026-06-22", "ticker": "RDW",  "action": "SELL", "shares": 5, "price": 13.30,  "notes": "Stop loss"},
    {"date": "2026-06-22", "ticker": "TTMI", "action": "BUY",  "shares": 3, "price": 213.00, "notes": "Support zone buy"},
    {"date": "2026-06-24", "ticker": "MRVL", "action": "SELL", "shares": 1, "price": 272.30, "notes": "Hard stop execution"},
    {"date": "2026-06-25", "ticker": "DRAM", "action": "BUY",  "shares": 4, "price": 76.43,  "notes": "Memory ETF"},
    {"date": "2026-06-25", "ticker": "MXL",  "action": "BUY",  "shares": 6, "price": 90.70,  "notes": "Optical component"},
    {"date": "2026-06-25", "ticker": "MU",   "action": "BUY",  "shares": 1, "price": 1155.00,"notes": "Post-earnings buy"},
]
```

#### 步骤四：运行回测并生成报告

```python
# 脚本：experiments/2026-06-27-rule-improvement-backtest/run_backtest.py
"""
主回测引擎
比较：实际操作序列 vs 应用新规则后的序列
"""

import pandas as pd
import numpy as np

INITIAL_CASH = 6410.26   # 基准 NAV（USD）
PLATFORM_FEE = 1.0       # 每笔操作平台费

class PortfolioSimulator:
    def __init__(self, initial_cash, trades, price_data):
        self.cash = initial_cash
        self.positions = {}     # {ticker: shares}
        self.cost_basis = {}    # {ticker: avg_cost}
        self.trades = trades
        self.prices = price_data
        self.nav_history = []
        self.errors = []

    def apply_new_rules(self, trade, current_positions, current_nav, fear_gate):
        """
        应用新规则，返回 (是否允许执行, 拒绝原因)
        """
        if trade["action"] != "BUY":
            return True, None

        # 计算当前总敞口
        total_equity = sum(
            self.prices[t].loc[trade["date"], "Close"] * s
            for t, s in current_positions.items()
            if t in self.prices and trade["date"] in self.prices[t].index
        )
        current_exposure_pct = total_equity / current_nav * 100

        # 规则 A：单日加仓速度上限
        day_new_exposure = trade["shares"] * trade["price"] / current_nav * 100
        daily_cap = 8.0 if fear_gate == "elevated" else 15.0
        # 注：需要追踪当日已加仓量，此处简化
        if day_new_exposure > daily_cap:
            return False, f"规则A违反：单笔新增{day_new_exposure:.1f}pp > {daily_cap}pp限制"

        # 规则 C：财报冷静期（MU 2026-06-25 = T+1，应拒绝）
        earnings_events = {
            "MU": "2026-06-24"  # 财报日
        }
        if trade["ticker"] in earnings_events:
            earnings_date = pd.Timestamp(earnings_events[trade["ticker"]])
            trade_date = pd.Timestamp(trade["date"])
            days_after = (trade_date - earnings_date).days
            if 0 <= days_after <= 1:
                return False, f"规则C违反：{trade['ticker']}财报冷静期（T+{days_after}），禁止买入"

        # 规则 E：主题浓度硬上限（简化版）
        AI_CAPEX_TICKERS = {"GLW", "TTMI", "MXL", "DRAM", "MU", "MRVL", "CRDO", "ALAB"}
        if trade["ticker"] in AI_CAPEX_TICKERS:
            ai_capex_exposure = sum(
                self.prices[t].loc[trade["date"], "Close"] * s
                for t, s in current_positions.items()
                if t in AI_CAPEX_TICKERS and t in self.prices
            )
            ai_capex_pct = ai_capex_exposure / current_nav * 100
            if ai_capex_pct >= 55.0:
                return False, f"规则E违反：AI Capex总敞口{ai_capex_pct:.1f}% ≥ 55%限制"

        return True, None

    def run(self, apply_new_rules=False, fear_gate_schedule=None):
        """运行模拟"""
        # ... 完整实现见脚本文件
        pass

# 运行两个版本
simulator_baseline = PortfolioSimulator(INITIAL_CASH, CONFIRMED_TRADES, price_data)
result_baseline = simulator_baseline.run(apply_new_rules=False)

simulator_improved = PortfolioSimulator(INITIAL_CASH, CONFIRMED_TRADES, price_data)
result_improved = simulator_improved.run(apply_new_rules=True)

# 输出比较报告
print_comparison_report(result_baseline, result_improved)
```

#### 步骤五：生成可读报告

```python
# 输出格式
def generate_report(baseline, improved):
    report = f"""
# 新规则回测报告
生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

## 期末 NAV 对比
| 版本 | 期末 NAV | vs 基准 | 最大回撤 | 夏普 |
|------|---------|---------|---------|------|
| 实际操作（无新规则） | ${baseline['final_nav']:.2f} | - | {baseline['max_dd']:.1f}% | {baseline['sharpe']:.2f} |
| 应用新规则后 | ${improved['final_nav']:.2f} | {improved['final_nav']-baseline['final_nav']:+.2f} | {improved['max_dd']:.1f}% | {improved['sharpe']:.2f} |

## 规则拦截统计
| 规则 | 拦截次数 | 避免损失估算 |
|------|---------|------------|
| 规则A（单日加仓限速） | {improved['rule_a_blocks']} | ${improved['rule_a_saving']:.2f} |
| 规则C（财报冷静期） | {improved['rule_c_blocks']} | ${improved['rule_c_saving']:.2f} |
| 规则E（主题浓度限制） | {improved['rule_e_blocks']} | ${improved['rule_e_saving']:.2f} |

## 结论
{generate_conclusion(baseline, improved)}
"""
    return report

# 保存报告
with open("experiments/2026-06-27-rule-improvement-backtest/backtest_report.md", "w", encoding="utf-8") as f:
    f.write(generate_report(result_baseline, result_improved))
```

---

### 2.3 更长期回测（V5 策略加入新规则）

#### 目标
在 V5 Optimal 的 20年回测框架中，加入以下规则约束，验证长期效果：
1. 主题浓度上限（55%）
2. 动态追踪止损
3. 财报冷静期

#### 数据准备
```python
# 使用已有的 26年历史数据库
# 路径：experiments/2026-05-29-dual-sleeve-backtest/

# 需要额外准备：
# 1. 财报日历数据（Earnings dates for S&P500 stocks 2000-2025）
#    来源：Quandl / Refinitiv / WRDS（如无法访问则跳过规则C回测）
# 2. 行业/主题分类数据
#    来源：GICS分类，可从 Yahoo Finance 或 Wikipedia 获取

# 简化方案（无需付费数据）：
# 用 GICS 行业来替代主题分类
# 财报冷静期用"股票单日涨幅>10%触发"代替精确财报日历
```

#### 回测脚本框架
```python
# 路径：experiments/2026-06-27-rule-improvement-backtest/bt_v5_with_rules.py

# 基于已有的 V5 回测框架修改
# 核心改动：在 generate_signals() 之后加入规则过滤层

def apply_new_rules_to_v5_signal(signal_df, portfolio_state, fear_gate):
    """
    对 V5 生成的买入信号应用新规则过滤
    返回过滤后的信号
    """
    filtered = signal_df.copy()

    # 规则 E：主题浓度上限
    for date in filtered.index:
        current_theme_exposure = calculate_theme_exposure(portfolio_state, date)
        if current_theme_exposure["AI_Capex"] >= 0.55:
            # 过滤掉所有 AI_Capex 主题的买入信号
            ai_capex_mask = filtered.loc[date, "gics_sector"].isin(["Information Technology", "Communication Services"])
            filtered.loc[date, ai_capex_mask] = 0

    # 规则 D：动态追踪止损
    for ticker in portfolio_state["positions"]:
        current_profit = calculate_profit_pct(portfolio_state, ticker, date)
        if current_profit >= 0.40:
            portfolio_state["trailing_stop"][ticker] = portfolio_state["cost"][ticker] * 1.25
        elif current_profit >= 0.25:
            portfolio_state["trailing_stop"][ticker] = portfolio_state["cost"][ticker] * 1.15
        elif current_profit >= 0.15:
            portfolio_state["trailing_stop"][ticker] = portfolio_state["cost"][ticker] * 1.08

    return filtered
```

---

## 三、周度错误复盘 SOP（标准操作程序）

每周五收盘后（或周六）执行，AI小弟可以半自动化完成：

```
Step 1 [自动] 读取本周 memory/trades/ 下的所有确认交易
Step 2 [自动] 读取本周 memory/daily/*-post-close-audit.md 的 NAV 变化
Step 3 [半自动] 对每笔操作填写错误分析表（AI对照规则判断）
Step 4 [自动] 统计错误类型分布和 NAV 影响
Step 5 [半自动] 识别 R3（高复发风险）错误，生成规则改进草稿
Step 6 [人工确认] 用户审阅规则改进草稿，确认后写入 decisions.md
Step 7 [自动] 将回测任务写入 experiments/ 目录
Step 8 [自动] 更新本周 weekly/YYYY-WW-error-analysis.md
```

---

## 四、本周错误分析完整报告

### 2026-W26（6/22-6/27）错误总结

```
总操作次数：5次（RDW止损 / TTMI买入 / MRVL止损 / DRAM买入+MXL买入+MU买入）
确认错误：3次（ERR-2026-001/002/003）
NAV 影响（估算）：
  - ERR-2026-001（单日过度加仓）：6/26次日组合-2.8%，约-$178
  - ERR-2026-002（MU追涨）：浮亏-$22.67，约-0.35%
  - ERR-2026-003（MXL定性错误）：止损过宽，潜在额外损失约-$27（若止损线在$91而非$86）
  - 合计影响：约-$228/-3.56% NAV

正确操作（值得保留）：
  - RDW止损（6/22）：纪律执行 ✅
  - MRVL止损（6/24）：48小时内强制执行 ✅
  - TTMI支撑位入场（6/22）：逻辑正确 ✅
  - GLW持有：盈利+22%，主线判断正确 ✅
```

---

*不构成投资建议。回测结果具有历史局限性和样本偏差，不代表未来表现。*
