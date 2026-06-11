# 2026-06-10 Trade Plan

生成时间：2026-06-10 Asia/Shanghai。

口径：每日美股执行清单与持仓记账；这是盘中/盘前执行准备，不替代 04:15 美股收盘后正式审计。不得视为真实券商订单。本自动化未登录券商、未提交订单、未撤单；真实成交只以用户或券商成交回报为准。

## 1. 数据来源与质量

本地资料读取：

- 已读取 `summary.md`、`decisions.md`、`daily-summaries.md`、最近 daily 记录、2026-06-10 每日美股策略报告、2026-06-10 实时资讯与机构研究监控产物、2026-06-09 每日美股策略报告、最新 portfolio/trades、2026-06-10 真实仓位起始记录，以及要求的 institutional overlay references。
- 2026-06-10 盘前策略已将风险定为 `stress-leaning elevated`，本清单是在该口径下把策略转成执行和记账动作。
- 真实账户新增已确认成交：用户确认 `MRVL` 买入 `1` 股，成交价 `USD 252.00`。这是真实账户起始仓位，独立于此前 USD 20,000 模型组合。

最新市场数据：

| 标的 | 6/9 收盘 | 6/9 盘后 | 数据时间 | 数据质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 266.88 | 264.00 | 2026-06-09 16:00 / 19:59 EDT | StockAnalysis；可用于执行准备；盘后流动性较弱 |
| AMD | 475.51 | 470.58 | 2026-06-09 16:00 / 19:53 EDT | StockAnalysis；可用于止损/减仓复核 |
| WDC | 517.72 | 514.01 | 2026-06-09 16:00 / 19:07 EDT | StockAnalysis；可用于 near-stop 复核 |
| STX | 846.01 | 839.00 | 2026-06-09 16:00 / 19:09 EDT | StockAnalysis；接近 835 风险线 |
| SPY | 737.05 | 735.69 | 2026-06-09 16:00 / 19:59 EDT | StockAnalysis； broad market 仍偏弱 |
| QQQ | 707.83 | 706.70 | 2026-06-09 16:00 / 19:59 EDT | StockAnalysis；科技成长弱于 SPY |
| SMH | 591.01 | 586.00 | 2026-06-09 16:00 / 19:52 EDT | StockAnalysis；半导体链回落 |
| VIX | 约 21.80 盘中读数 | n/a | MarketWatch 2026-06-09 盘中报道 | 非官方收盘；足以维持 elevated，不足以精确计算 term structure |

数据缺口：

- 未取得真实账户完整现金、可用 USD/HKD、佣金、税费、滑点和所有挂单状态。
- VIX/VIX3M、HYG/LQD、RSP/SPY、期权/ETF flow 没有完整可验证收盘数据。
- 无法确认旧 MRVL `315` 真实限价卖单是否仍存在；只能列为用户侧复核项。

## 2. 风险状态与机构 Overlay

执行结论：

- 市场状态：`stress-leaning elevated`，比 2026-06-09 盘前更偏防御。
- 新买入：模型组合禁止新增买入；真实账户不追加 MRVL，不新增 WDC/STX/AMD/MU/SNDK。
- 现金目标：模型组合继续维持 `55%-65%` 高现金；按 6/9 收盘估算为 `60.22%`。
- 优先事项：真实 MRVL 小仓止损线复核；AMD 继续 `reduce-review`；WDC/STX 保持 `defensive hold / near-stop review`；MRVL 禁止追高。

Institutional overlay scorecard:

- `flow_fragility_score`: `11/14`，`elevated / acute watch`。MRVL 盘中高低波动大、SMH 下跌、QQQ 弱于 SPY、VIX 盘中回到约 `21.80`，说明 AI/半导体反弹仍脆弱。
- `trend_aligned_entry_score`: `1/5`，`trend_broken`。市场 fear gate 不允许新增买入，MRVL/AMD 未确认趋势修复，WDC/STX 只是高于硬止损。
- `AI_quality/capex_cycle`: MRVL、AMD、WDC、STX 均为高 capex-cycle 敏感；真实 MRVL 只能是小仓 starter，不是加仓信号。
- `factor_macro_flags`: `growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high; consumer_backstop_fragility; VIX_data_gap; credit_data_gap`。
- `action impact`: 阻止所有新买入；优先止损/near-stop/旧挂单复核；禁止把 MRVL 事件波动解读为追高许可。

## 3. 执行清单

| 股票代码 | 账户口径 | 方向 | 数量 | 目标金额 | 组合占比 | 参考价格 | 触发条件 | 止损价 | 失效条件 | 策略理由 | 风险点 | 状态 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| MRVL | 真实账户 | 持有；不加仓 | 1 股 | 已成交 USD 252.00；6/9 收盘市值 USD 266.88 | 约 HKD 20,000 账户的 10% 左右，具体取决于 FX/费用 | 266.88 close / 264.00 AH | 已有小仓可继续观察；若 SMH/QQQ 不再创新低且 MRVL 站回 275-280，才从防御观察转为普通持有复核 | 收盘 `<245` 切换为减仓/退出复核；盘中跌向 `235` 且 SMH 转弱视为 starter thesis failed | 跌破 245 或 235 风险线；或用户确认实际资金/汇率使仓位超出可承受范围 | 小仓真实试单已确认，成本有缓冲；但价格远低于旧 310-315 趋势区，不能追高 | 高 beta、指数纳入后回吐、半导体链拥挤、账户小导致单股仓位粒度粗 | core hold / starter defensive review；真实成交已记录 |
| MRVL | 模型组合 | 持有；旧挂单复核 | 0 | 0 | 10.48% | 266.88 close / 264.00 AH | 若真实券商端仍有旧 `315` 限价卖单，用户需确认是否撤销/修改；模型不新增卖出 | 模型收盘 `<260` 减仓复核；`<245` 深度风险警告 | 重新站回 310-315 且 SMH/QQQ 修复后，才复核利润保护 | S&P 500 纳入事件仍在，但价格确认失败；不追高 | 事件溢价回吐；高波动导致旧挂单逻辑失效 | core hold / profit-protection review；无新模型成交 |
| AMD | 模型组合 | 减仓复核 | 等待用户确认；候选模型减 `1.00` 股 | 约 USD 475.51 | 10.71% | 475.51 close / 470.58 AH | 6/9 再次低于既有 `492` 收盘止损线，且盘后继续弱 | 日收盘 `<492` 已触发；若继续弱于 QQQ/SMH，维持优先 reduce-review | 连续 1-2 个收盘重新站回 492-500，才可降级为 defensive hold | AMD 已连续未修复旧止损，不能称为普通持有 | 减仓后若快速反弹会错失恢复；不减则纪律失效 | reduce-review；待用户确认；无真实/模型新成交 |
| WDC | 模型组合 | 持有；防御观察 | 0 | 0 | 9.33% | 517.72 close / 514.01 AH | 不加仓；若收盘接近或跌破 500，进入更严格减仓复核 | 日收盘 `<500` | 连续收盘远离 500 且存储链 RS 修复，才可普通持有 | AI storage 需求仍支持，但同主题承压 | 盘中振幅大；主题拥挤回撤会同步传导 | defensive hold / near-stop review；无订单 |
| STX | 模型组合 | 持有；防御观察 | 0 | 0 | 9.26% | 846.01 close / 839.00 AH | 不加仓；盘后 839 已接近 835 风险线，下一正式收盘必须重点复核 | 日收盘 `<835` | 连续收盘远离 835 且 WDC/STX/MU/SNDK 同步修复，才可普通持有 | 存储主题仍强，但高位波动和估值压力更明显 | 距离硬止损很近；若盘后弱势延续，可能触发 exit/reduce-review | defensive hold / near-stop review；near-stop priority |
| AMD/WDC/STX/MU/SNDK/AVGO/NVDA/GLW/AI 应用池 | 真实账户与模型组合 | 仅观察 | 0 | 0 | 0 | n/a | 需要 fear gate 降级、trend_aligned_entry 达到 `4-5/5`、且现有止损复核完成 | 个股另定 | 今日规则失效：elevated + trend_broken | 主题有效但买点未通过 | 追涨会扩大 AI capex/crowding 暴露 | watch only |

## 4. 真实成交、待执行与模型成交区分

- 真实成交：
  - 已确认：2026-06-10 Asia/Shanghai，`MRVL` 买入 `1` 股，成交价 `USD 252.00`。
  - 未确认：没有其他真实买入、卖出、撤单或挂单成交回报。
- 待用户确认：
  - 真实账户：MRVL 是否设置/调整止损纪律；是否仍存在旧 `315` 限价卖单。
  - 模型组合：AMD 是否按既有 `<492` 收盘止损规则记录 `1.00` 股模型减仓。
- 模型组合模拟成交：
  - 今日不新增。
  - 继续沿用 2026-06-02 MRVL 25% 模型减仓和 2026-06-04 MRVL 1.50 股模型减仓。
- 撤单：
  - 仅提示用户侧复核 MRVL 旧真实挂单；本自动化未登录券商、未撤单。

## 5. 执行优先级

| 优先级 | 动作 | 标的 | 触发 | 数量 | 备注 |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 真实持仓风控复核 | MRVL | 真实账户已持有 1 股，6/9 close 266.88；若收盘跌破 245 或盘中跌向 235 且 SMH 弱，复核退出 | 1 股 | 小仓持有，不加仓 |
| 2 | 用户确认/模型减仓复核 | AMD | 6/9 close 475.51，继续低于 492 | 1.00 股候选 | 只记录待确认，不虚构成交 |
| 3 | near-stop review | STX | AH 839 接近 835，下一正式收盘重点复核 | 0 | 不加仓，必要时转 reduce-review |
| 4 | defensive hold | WDC | close 517.72，高于 500 但仍承压 | 0 | 不加仓 |
| 5 | 旧挂单复核 | MRVL | 若真实券商端仍有旧 315 限价单 | 未知 | 用户侧确认/撤改 |
| 6 | 仅观察 | 新 AI/半导体/存储/应用候选 | 需要 fear gate 和 trend-aligned entry 双确认 | 0 | 今日无新买入 |

## 6. Replay 协议

2026-06-09 close 已属于 2026-06-05 事件后的已完成交易日，因此 replay 协议适用。已将 2026-06-09 close 行追加到 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`，未预填未来日期。Overlay portfolio value 仍留空，因为没有用户确认 AMD 模型减仓，也没有明确定义 overlay 自动成交假设。

## 7. Sources

- StockAnalysis: MRVL, AMD, WDC, STX, SPY, QQQ, SMH quote pages，观察到 2026-06-09 close/after-hours。
- MarketWatch: 2026-06-09 VIX 盘中反转至约 21.80 的报道。
- Local memory: 2026-06-10 daily strategy, 2026-06-10 realtime/institutional monitor, 2026-06-09 portfolio/trade plan, 2026-06-10 real-position-start, institutional overlay references。
