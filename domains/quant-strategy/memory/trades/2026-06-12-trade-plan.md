# 2026-06-12 Trade Plan

Run time: 2026-06-12 23:05 Asia/Shanghai / 11:05 ET.

Scope: 美股盘中/盘前执行准备与组合记账；不是正式美股收盘审计，不登录券商，不提交真实订单，不虚构成交。

## 账户与成交边界

| 类别 | 状态 |
| --- | --- |
| 真实账户已确认持仓 | 无 |
| 最近真实成交 | `MRVL` 1 股，买入 `USD 252.00`，卖出 `USD 267.020`，毛利润约 `USD +15.020` / `+5.96%` |
| 今日新增真实成交 | 无 |
| 等待用户确认订单 | 无立即可下单项；仅保留观察/条件清单 |
| 模型组合模拟成交 | 无新增模拟成交 |
| 现金/费用/汇率 | 真实账户现金、手续费、FX、税费仍未由券商或用户确认 |

## 数据质量

| 数据 | 时间 | 来源 | 质量 | 缺口 |
| --- | --- | --- | --- | --- |
| 股票/ETF 盘中快照 | 2026-06-12 23:04 Asia/Shanghai / 11:04 ET 附近 | 本地 Node `StockService.fetchQuotes`，source=`Tencent (Primary)` | 中高；可用于执行准备 | 不是正式收盘价；需收盘审计确认 |
| Python 报价路径 | 同次运行 | Codex bundled Python + `ResilientStockClient` | 不可用 | 本次命令超时，未作为主数据源 |
| VIX | Tencent 返回 `21.67`，字段 open/high/low/volume 为 0 | Tencent | 低 | 疑似旧/不完整快照；不得据此把风险降为 `normal` |
| VIX/VIX3M | 未取得同步 term structure | n/a | 缺口 | 风险门控仍保守 |
| 真实账户现金/订单 | 未同步券商 | 用户/券商待确认 | 缺口 | 不记录任何真实新订单或成交 |

关键快照：

| Ticker | 参考价 | 日内变化 | 开盘 | 高 | 低 | 交易量 | 状态用途 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 284.58 | +1.38% | 270.07 | 287.54 | 267.31 | 17,522,048 | watch only / no chase |
| AMD | 511.65 | +4.75% | 499.69 | 517.80 | 494.00 | 13,151,551 | 已盘中重回 492 上方，但需收盘确认 |
| WDC | 560.14 | +5.83% | 541.99 | 572.29 | 531.96 | 2,489,788 | defensive hold / repair review |
| STX | 921.08 | +6.10% | 880.19 | 939.90 | 868.14 | 1,293,962 | defensive hold / repair review |
| SPY | 742.10 | +0.59% | 740.71 | 742.98 | 735.05 | 15,625,280 | broad repair |
| QQQ | 720.80 | +0.51% | 717.61 | 721.89 | 711.28 | 19,443,491 | growth repair |
| SMH | 618.70 | +1.52% | 607.95 | 620.49 | 602.24 | 3,246,128 | semiconductor repair, high beta |
| HYG | 79.92 | -0.03% | 79.94 | 79.95 | 79.80 | 9,001,188 | credit neutral/slight soft |
| LQD | 108.94 | -0.13% | 108.88 | 108.97 | 108.64 | 8,639,306 | credit/rate proxy slight soft |
| IWM | 295.08 | +1.61% | 291.63 | 295.42 | 290.31 | 11,976,488 | breadth repair |
| RSP | 211.90 | +1.03% | 210.70 | 212.11 | 209.66 | 5,876,063 | equal-weight repair |

## Market Gate

```text
market_regime: elevated / repair watch
fear_score: 5-6 / 14, not normal because VIX/VIX3M is incomplete
risk_multiplier: about 70%
real_account_equity_exposure: 0% confirmed
new_buy_permission: blocked for immediate execution; only trend-aligned watch conditions
cash_target: real account remains cash/no confirmed equity holdings; historical model target remains 60%-70% cash
```

判断：广度、半导体和小盘继续修复，但这是压力后的第二段反弹确认过程。AI/半导体/存储同主题仍高 beta，不能因为 MRVL/AMD/WDC/STX 日内强势就追高。

## Institutional Overlay 摘要

```text
flow_fragility_state: elevated
flow_fragility_score: 7/14
trend_aligned_entry_state: cheap_but_unconfirmed for new buys; AMD/WDC/STX repair is encouraging but still requires close confirmation
AI_quality/capex_cycle: MRVL/AMD/WDC/STX remain high capex-cycle sensitive; ADBE/ORCL remind that AI demand must convert into revenue/cash-flow quality
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; VIX_term_structure_data_gap; token_cost_elasticity
action_impact: no chase buys; stop/reduce reviews before new exposure; any new buy must wait for support/reclaim and user confirmation
```

## 持仓与观察标记

真实账户当前无确认股票持仓。下表中 AMD/WDC/STX 的持仓语言只适用于历史模型/replay 风险复核，不代表真实账户持仓。

| Ticker | 账户范围 | 当前标记 | 参考价 | 触发/止损线 | 判断 |
| --- | --- | --- | ---: | --- | --- |
| MRVL | 真实账户已空仓；模型观察 | watch only | 284.58 | 旧真实账户 `<245/<235` 线因空仓失效；重入需新规则 | 事件拉升后未确认新趋势，禁止追高 |
| AMD | 历史模型/replay；真实账户 watch-only | reduce-review | 511.65 | 既有收盘止损线 `492` | 盘中重回上方，但上一正式收盘仍低于 492；必须等收盘确认后才能降级风险 |
| WDC | 历史模型/replay；真实账户 watch-only | defensive hold / near-stop repair review | 560.14 | 既有风险线 `500` | 已明显回到线上，但同主题承压史仍在；不新增 |
| STX | 历史模型/replay；真实账户 watch-only | defensive hold / near-stop repair review | 921.08 | 既有风险线 `835` | 已明显回到线上，但股价高、小账户单股金额不友好；不新增 |

## 待执行清单

| 状态 | Ticker | 方向 | 数量 | 目标金额 | 组合占比 | 参考价格 | 触发条件 | 止损价 | 失效条件 | 策略理由 | 风险点 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| 仅观察 | MRVL | 无买入 | 0 | USD 0 | 0% | 284.58 | 回踩并守住 267-270 区域，或突破后回踩确认；同时 QQQ/SMH 不反转 | 新重入规则待定；旧 `<245/<235` 不适用于空仓 | 高位继续上冲但无回踩确认；或跌回 267 下方 | AI interconnect/custom silicon 仍强，但卖出后重入必须重新建模 | 事件/CFO 催化后追高风险，capex-cycle 敏感 |
| 仅观察 / 收盘复核 | AMD | 无新增；历史模型 reduce-review | 0 | USD 0 | 0% real | 511.65 | 正式收盘站稳 492-500 上方且相对 QQQ 改善，才可把历史模型从 reduce-review 降为 repair watch | 历史模型线 492；真实账户无仓不触发 | 收盘跌回 492 下方 | 盘中修复强，但规则要求收盘确认 | AI compute 高 beta，前一正式收盘仍未修复止损线 |
| 仅观察 / 防守持有复核 | WDC | 无新增 | 0 | USD 0 | 0% real | 560.14 | 连续收盘守住 500 上方并跑赢 SMH/QQQ，才可重新进入候选排序 | 历史模型线 500 | 收盘跌回 500，或存储链与 SMH 同步转弱 | 存储链延续修复，主题仍有效 | 与 STX/MU 同主题拥挤，周期与估值波动高 |
| 仅观察 / 防守持有复核 | STX | 无新增 | 0 | USD 0 | 0% real | 921.08 | 连续收盘守住 835 上方并跑赢 SMH/QQQ；小账户需更严格价格基础 | 历史模型线 835 | 收盘跌回 835，或存储链转弱 | 存储链强修复 | 单股金额高，HKD 20,000 账户不适合追价 |
| 仅观察 | NVDA/AVGO/QCOM/NOK/ORCL/AI 应用层 | 无买入 | 0 | USD 0 | 0% | n/a | 需要个股技术位、RS、财报/现金流证据同步确认 | 按个股另设 | AI 叙事强但价格或质量证据不足 | 保持候选池完整 | 主题重叠、AI capex/token-cost/应用转化风险 |

## 撤单 / 减仓 / 加仓

- 撤单：未发现用户确认的有效待撤真实订单；若券商仍有旧 MRVL `315` 相关订单，需用户在券商端确认后才能记账。
- 卖出：真实账户无持仓，无卖出订单。
- 减仓：真实账户无持仓；历史模型层面 AMD 仍为第一优先 reduce-review，待正式收盘确认是否重新站上 `492`。
- 加仓：无。
- 买入：无立即买入；所有新买入均未通过 `trend_aligned_entry` 与技术价格基础双重要求。

## Replay Ledger

本次不更新 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`。原因：当前运行时间仍是 2026-06-12 美股盘中，不是完成的正式收盘数据；协议要求不要预填未来或未完成日期。下一次应由 04:15 盘后审计在取得 2026-06-12 close 后决定是否补 T5/后续行。

## 用户确认事项

- 是否有任何券商端未撤订单，尤其是旧 MRVL 限价单。
- 真实账户现金、结算、手续费、FX 与税费。
- 是否允许后续在 MRVL/AMD/WDC/STX 中择一建立 1 股 starter，而不是同时重建同主题篮子。

## 数据缺口

- VIX/VIX3M 同步 term structure。
- 正式 2026-06-12 美股收盘价。
- 真实账户现金与订单状态。
- 本次 Python 报价路径超时原因。
