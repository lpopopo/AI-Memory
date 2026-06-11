# 2026-06-11 Trade Plan

生成时间：2026-06-11 Asia/Shanghai

口径：每日美股执行清单与持仓记账；这是盘中/盘前执行准备，不替代 04:15 美股盘后正式审计。本记录不登录券商、不提交订单、不撤单、不虚构成交。真实成交只以用户或券商回报为准。

## 1. 数据来源与质量

已读取本地资料：

- `memory/summary.md`、`memory/decisions.md`、`memory/daily-summaries.md`
- 最近 daily 记录：2026-06-10 premarket strategy、realtime/institutional monitor、post-close audit、details、real-position records
- 当天 2026-06-11 “每日美股策略建议”报告：未找到
- 当天 20:30 “实时资讯与机构研究监控”产物：未找到
- 最新真实组合快照：`memory/portfolio/2026-06-10-real-portfolio-summary.md`
- 近期交易记录：`2026-06-10-real-fill.md`、`2026-06-10-trade-plan.md`
- 必读 references：`us-stock-daily-strategy-report-template.md`、`institutional-overlay-scorecard.md`、`ai-quality-capex-cycle-classification.md`、`institutional-overlay-replay-protocol.md`

最新可得行情：

| 标的 | 最新可用价格 | 时间 | 质量 |
| --- | ---: | --- | --- |
| MRVL | 266.88 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| AMD | 475.51 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| WDC | 517.72 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| STX | 846.01 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| SPY | 737.05 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| QQQ | 707.83 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| SMH | 591.01 | 2026-06-09 16:00 EDT 正式收盘 | 本地 2026-06-10 post-close audit 已验证；高 |
| VIX | 约 21.80 | 2026-06-09 盘中报道 | 非正式收盘；仅用于维持 elevated 风险 |

数据缺口：

- 外部实时行情刷新失败；`stooq.com` 当前环境无法连接，网页行情工具未返回可用数据。
- 未取得 2026-06-10 美股正式收盘价；本任务不预填盘后审计数据。
- 未取得 VIX/VIX3M、HYG/LQD、完整账户现金、USD/HKD 实际成交汇率、费用、税费、滑点、真实挂单状态。
- 2026-06-11 本地 daily strategy 与 20:30 monitor 未找到；新买入默认无效。

## 2. 风险状态与 Institutional Overlay

```text
market_regime: elevated, stress-leaning
flow_fragility_state: elevated / acute watch
trend_aligned_entry_state: trend_broken
AI_quality/capex_cycle: MRVL/AMD/WDC/STX 均为 high capex-cycle sensitive
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high; consumer_backstop_fragility; VIX_data_gap; credit_data_gap; live_quote_gap
action impact: 禁止新增 AI/semiconductor/storage 买入；真实 MRVL 仅持有复核；AMD 继续 reduce-review；WDC/STX 继续 defensive hold / near-stop review；MRVL 禁止事件后追高
```

新买入必须通过 trend_aligned_entry。本次没有候选达到 `trend_aligned`，因此所有新买入、加仓和追高订单状态均为 `仅观察` 或 `无效`。

## 3. 执行清单

| 股票代码 | 账户口径 | 方向 | 数量 | 目标金额 | 组合占比 | 参考价格 | 触发条件 | 止损价 | 失效条件 | 策略理由 | 风险点 | 状态 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| MRVL | 真实账户 | 持有；不加仓 | 1 股 | 已成交 USD 252.00；参考市值 USD 266.88 | 成本约 HKD 20,000 账户 9.8%；参考市值约 10.4%，未计费用/FX | 266.88 | 仅当 SMH/QQQ 修复且 MRVL 重新站回 275-280 后，才从防御复核转为普通持有复核 | 日收盘 `<245` 触发减仓/退出复核；盘中靠近 `235` 且 SMH/QQQ 弱，视为 starter thesis failed | 跌破 245/235 风险线；或用户确认实际费用/汇率使仓位超预算 | 用户已确认小仓真实试单，仍有盈利缓冲；但趋势未恢复，不能追高 | 高 beta、半导体链拥挤、事件溢价回吐、账户小导致单股粒度粗 | `core hold / starter defensive review`；真实成交已记录 |
| MRVL | 旧模型/回放口径 | 持有；旧挂单复核 | 0 | 0 | 历史模型约 10.48%，不作为当前真实持仓 | 266.88 | 若券商端仍有旧 `315` 真实限价卖单，需用户确认是否存在及是否撤改 | 模型 close `<260` reduce-review；真实 starter 仍按 `<245`/`235` | 重新站回 310-315 且 SMH/QQQ 修复前，旧 profit-protection 逻辑失效 | S&P 500 纳入事件不等于趋势恢复 | 事件后回吐、旧模型与真实账户混淆 | `core hold / profit-protection review`；无新模型成交 |
| AMD | 旧模型/回放口径 | 减仓复核 | 待用户确认；候选模型减 1.00 股 | 约 USD 475.51 | 历史模型约 10.71%，不作为当前真实持仓 | 475.51 | 既有 `<492` 收盘止损已被触发且未修复 | 日收盘 `<492` 已触发 | 连续收盘重新站回 492-500 才可降级为 defensive hold | 规则纪律优先；AMD 不得写为普通持有 | 反弹错失 vs 不减仓导致规则失效 | `reduce-review`；等待用户确认，无真实/模型新成交 |
| WDC | 旧模型/回放口径 | 持有；防御观察 | 0 | 0 | 历史模型约 9.33%，不作为当前真实持仓 | 517.72 | 不加仓；若收盘接近或跌破 500，转更严格减仓复核 | 日收盘 `<500` | 连续收盘远离 500 且 storage basket RS 修复才可普通持有 | AI storage thesis 仍在，但价格与同主题压力不支持加仓 | 高位波动、主题拥挤、同链条回撤 | `defensive hold / near-stop review` |
| STX | 旧模型/回放口径 | 持有；防御观察 | 0 | 0 | 历史模型约 9.26%，不作为当前真实持仓 | 846.01 | 不加仓；因距 835 很近，下一个正式收盘需优先复核 | 日收盘 `<835` | 连续收盘远离 835 且 WDC/STX/MU/SNDK 同步修复才可普通持有 | 存储主题仍强，但风险线太近 | 距离硬止损近、价格高、小账户不适合新增 | `defensive hold / near-stop review`；near-stop priority |
| AMD/WDC/STX/MU/SNDK/NVDA/AVGO/GLW/AI 应用层 | 真实账户与模型 | 仅观察 | 0 | 0 | 0 | n/a | 必须满足 fear gate 降级、trend_aligned_entry `4-5/5`、现有止损复核完成 | 个股另定 | elevated + trend_broken 状态下全部新买入失效 | 主题可以观察，但买点未通过 | 追高会扩大 AI capex/crowding 暴露 | `watch only` |

## 4. 真实成交、待确认、模型模拟

真实成交：

- 已确认：2026-06-10 Asia/Shanghai，`MRVL` 买入 `1` 股，成交价 `USD 252.00`。
- 未确认：没有其他真实买入、卖出、撤单或挂单成交回报。

等待用户确认：

- 真实账户：MRVL 是否仍有旧 `315` 限价卖单；是否需要按 `<245`/`235` 纪律设置提醒或手动复核。
- 旧模型/回放：AMD 是否按既有 `<492` 收盘止损规则记录 `1.00` 股模型减仓。未经确认前不写入模拟成交。

模型组合模拟成交：

- 本次新增：无。
- 历史旧模型仅用于规则复核、回放和风险语言，不作为当前真实持仓。

撤单：

- 本自动化未登录券商、未撤单。只提示用户侧复核旧 MRVL `315` 真实挂单是否存在。

## 5. Replay 协议

`domains/quant-strategy/experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 已存在并已包含 2026-06-09 close 行。由于本次未取得 2026-06-10 正式收盘价，且本任务不是 04:15 正式收盘审计，不新增 replay 行，不预填未来日期。

## 6. 待复核事项

- 取得 2026-06-10 美股正式收盘价后，由 04:15 盘后审计任务更新止损触发、NAV 和 replay。
- 用户确认 MRVL 旧 `315` 限价单是否存在。
- 用户确认是否允许在旧模型/回放口径中记录 AMD `1.00` 股减仓模拟。
- 修复或替换实时行情路径，至少覆盖 MRVL/AMD/WDC/STX/SPY/QQQ/SMH/VIX/VIX3M/HYG/LQD。
