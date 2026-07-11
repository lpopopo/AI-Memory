# 日K突破形态回测实验

> **状态（2026-07-03 复核后）：** 原始总结已被稳健性复核推翻，不得直接用于
> `decisions.md` 或实盘。当前权威结论见
> [`results/robustness_report.md`](results/robustness_report.md)，机器可读证据见
> [`results/robustness_metrics.json`](results/robustness_metrics.json)。

**路径：** `experiments/2026-07-03-breakout-pattern-backtest/`  
**目的：** 用约 20 年美股日K数据验证 A 股技术形态（图2/3/4/5/6/9）的美股适配版是否有效

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `run_backtest.py` | 主回测脚本 |
| `optimize_strategy.py` | 修正成交语义、消融、样本外、bootstrap 与多仓位组合评估 |
| `test_backtest.py` | 成交与止损语义回归测试 |
| `README.md` | 本文件 |
| `data_cache/` | yfinance 下载缓存（首次运行后生成） |
| `results/backtest_summary.md` | 中文结论报告 |
| `results/metrics.json` | 结构化指标与样本交易 |

---

## 快速开始

```bash
cd domains/quant-strategy/experiments/2026-07-03-breakout-pattern-backtest
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy yfinance tabulate
python run_backtest.py
python -m unittest -v test_backtest.py
python optimize_strategy.py
```

---

## 回测设计

### 股票池（52 只）

- ETF：SPY、QQQ、SMH
- 半导体/AI 链：NVDA、AMD、MU、MRVL、GLW、TTMI、MXL、WDC、STX 等
- 大盘蓝筹：AAPL、MSFT、GOOGL、AMZN、META、JPM、V 等
- 覆盖 2006-01-01 至 2025-12-31（yfinance 自动调整收盘价）

### 入场形态

| 代号 | 形态 | 核心规则 |
|------|------|----------|
| **A** | 突破+回踩（图3/9） | 20日窄幅整理 → 放量突破 → 10日内缩量回踩 → 收复突破位/MA20 入场 |
| **B** | 温和小阳突破（图2） | 整理后连续小阳线 → 放量突破平台上沿 |
| **C** | 假摔黄金坑（图4） | MA50 上方趋势 → 2-3 日跌破 MA20 → 5 日内收复 MA20 入场 |

### 出场 / 风控

- 止损：回踩低点或 -8%
- 时间止损：入场后 5 日无跟进（<2% 涨幅）退出
- 假突破退出：突破 20 日高后 3 日内收盘跌回（图5）
- 射击之星：20 日新高 + 上影线 >2×实体 → 收紧止损
- 追踪止损：+15% → 成本+8%；+25% → 成本+15%（对齐 decisions.md 规则 D）

### 对比基准

1. **SPY 买入持有**
2. **无回踩突破**（图1 简化：突破即入场）
3. **随机入场**（同股票池、同出场规则）

### 指标

每笔交易统计：胜率、均收益、中位收益、Sharpe（近似）、假突破率；策略序列复利得 CAGR 与最大回撤。

**交易成本：** 单边 0.1%

---

## 稳健性验收标准

| 指标 | 验证通过门槛 |
|------|-------------|
| 样本量 | ≥ 30 笔 |
| 样本外均收益 | 股票聚类 bootstrap 95% CI 下界 > 0 |
| 多仓位组合 | 限制 10 个并发仓位、逐日盯市后 Sharpe > 0 |
| 稳定性 | 多数样本外年份不依赖单一股票或单一年度 |
| vs SPY | 同期比较 CAGR、最大回撤和 Sharpe，不混用串行复利 |
| 规则有效性 | 必须通过单规则消融；“使用了规则”不等于“验证了规则” |

---

## 局限性

- 幸存者偏差（含 ARM/CRDO 等新上市标的）
- 等权串行复利，非真实多仓位
- 信号基于收盘确认，假设次日可成交
- 未建模滑点
- 当前股票池是事后选择的存活证券；这是候选研究而非最终实盘证明
- 2019–2025 已被本轮查看，后续参数变更不能继续把它称为全新样本外

---

*不构成投资建议。*
