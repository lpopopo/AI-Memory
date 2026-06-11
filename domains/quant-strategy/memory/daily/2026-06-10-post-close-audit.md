# 2026-06-10 Post-Close Audit

审计对象：2026-06-09 美股常规交易正式收盘。
运行时间：2026-06-10 Asia/Shanghai。
范围：正式收盘触发、组合风险审计、模型组合净值核对、institutional overlay replay 更新检查。

本记录不登录券商、不提交真实订单、不虚构真实成交。真实账户只承认用户或券商回报；当前唯一已确认真实成交仍为 `MRVL` 1 股，成交价 `USD 252.00`。

## 1. 已读取资料

- `memory/summary.md`
- `memory/decisions.md`
- `memory/daily-summaries.md`
- 最近 daily：`2026-06-10-details.md`、`2026-06-10-us-stock-premarket-strategy.md`、`2026-06-10-realtime-public-institutional-monitor.md`、`2026-06-10-real-position-start.md`、`2026-06-09-details.md`、`2026-06-09-us-stock-premarket-strategy.md`
- 当天策略建议：`2026-06-10-us-stock-premarket-strategy.md`
- 执行清单：`memory/trades/2026-06-10-trade-plan.md`
- 盘中/当日复盘：`memory/daily/2026-06-10-details.md`
- 最新组合快照：`memory/portfolio/2026-06-10-portfolio-summary.md`、`memory/portfolio/2026-06-10-real-portfolio-summary.md`
- 近期交易记录：`memory/trades/2026-06-10-real-fill.md`、`memory/trades/2026-06-10-trade-plan.md`、`memory/trades/2026-06-09-trade-plan.md`
- references：`market-fear-technical-framework.md`、`portfolio-concentration-rules.md`、`daily-market-monitoring-framework.md`、`institutional-overlays-daily-checklist.md`、`institutional-overlay-scorecard.md`、`ai-quality-capex-cycle-classification.md`、`institutional-overlay-replay-protocol.md`

## 2. 收盘数据与质量

主要来源：StockAnalysis quote pages，正式收盘时间为 2026-06-09 16:00 EDT；盘后价为辅助观察，不用于正式 NAV。VIX 来源为 MarketWatch 2026-06-09 盘中报道，记录 VIX 反转至约 `21.80`，不是官方收盘结算价，因此只用于维持 elevated 风险，不用于精确 VIX/VIX3M 计算。

| 标的 | 正式收盘 | 日变动 | 盘后/补充 | 数据时间 | 数据质量 |
| --- | ---: | ---: | ---: | --- | --- |
| MRVL | 266.88 | -7.61% | 263.96 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高；盘后中等 |
| AMD | 475.51 | -3.02% | 471.02 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高；盘后中等 |
| WDC | 517.72 | -1.75% | 513.37 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高；盘后中等 |
| STX | 846.01 | -3.51% | 837.50 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高；盘后中等 |
| SPY | 737.05 | -0.29% | 735.70 | 2026-06-09 16:00/20:00 EDT | StockAnalysis 正式收盘高 |
| QQQ | 707.83 | -1.15% | 706.67 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高 |
| SMH | 591.01 | -1.20% | 587.43 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高 |
| SOXX | 562.14 | -1.63% | 559.00 | 2026-06-09 16:00/19:59 EDT | StockAnalysis 正式收盘高 |
| VIX | 约 21.80 | +15.2% 盘中报道 | n/a | 2026-06-09 盘中报道 | MarketWatch 盘中报道；非正式收盘 |
| VIX/VIX3M | n/a | n/a | n/a | n/a | 未取得可靠收盘，不能下调风险 |
| RSP | 209.19 | +0.76% | 209.05 | 2026-06-09 16:00/20:00 EDT | StockAnalysis 正式收盘高 |
| RSP/SPY | 0.28382 | 日内相对改善 | n/a | 2026-06-09 close | 宽度优于 cap-weight，但与持仓主题背离 |
| HYG | 79.66 | +0.15% | n/a | 2026-06-09 14:47 EDT | 盘中快照；不能作为正式信用收盘 |
| LQD | 108.06 | -0.10% | 108.14 premarket | 2026-06-08 close / 2026-06-09 premarket | 过期，不能计算 HYG/LQD |
| HYG/LQD | n/a | n/a | n/a | n/a | 两腿时间不匹配，不能下调风险 |
| IWM | 285.02 | +0.32% | 284.20 | 2026-06-09 16:00/20:00 EDT | StockAnalysis 正式收盘高 |
| IWM/SPY | 0.38670 | 小盘相对改善 | n/a | 2026-06-09 close | 宽度改善，但 AI/semis 持仓承压 |

## 3. 市场恐慌门控

正式判定：

```text
fear_regime: elevated, stress-leaning
estimated_fear_score: 8/14
risk_multiplier: 70%
framework_cash_floor: 25%
operational_cash_target: 60%-70%
max_new_buy_exposure: 0% for this audit
```

理由：VIX 报道值 `21.80` 处于 elevated 上沿并接近 `22` stress 阈值，且出现盘中 sharp U-turn；QQQ、SMH、SOXX 明显弱于 SPY，持仓主题比宽基指数更脆弱；RSP 和 IWM 相对更强，说明不是全面 panic；HYG/LQD 与 VIX/VIX3M 数据不足，不能用于下调风险。因此 regime 不升级为正式 `stress`，但操作上禁止新买入。

## 4. Stop-Trigger Table

| 账户 | Ticker | 收盘价 | 既有止损/减仓线 | 是否触发 | Near-stop | 下一步状态 |
| --- | --- | ---: | --- | --- | --- | --- |
| Real | MRVL | 266.88 | close `<245` 减仓/退出复核；跌向 `235` 且 SMH/QQQ 弱则 thesis failed | 未触发 | 否 | `core hold / starter defensive review`；不加仓 |
| Model | MRVL | 266.88 | model close `<260` reduce-review；旧 profit-protection 需等 310-315 与 SMH/QQQ 修复 | 未触发 | 否 | `core hold / profit-protection review`；事件反弹不能追高 |
| Model | AMD | 475.51 | 既有 close `<492` 风险线 | 已触发且仍未修复 | 是 | `reduce-review`；不能写成普通 hold |
| Model | WDC | 517.72 | close `<500` reduce-review | 未触发 | 是，距风险线约 3.5% | `defensive hold / near-stop review`；不加仓 |
| Model | STX | 846.01 | close `<835` reduce-review | 未触发 | 是，距风险线约 1.3%；盘后 837.50 更近 | `defensive hold / near-stop review`，优先级上调 |

规则覆盖说明：没有覆盖 AMD `<492` 规则的稳定理由；AMD 必须维持 `reduce-review`。MRVL 的 S&P 500 纳入事件只能解释波动，不能覆盖 profit-protection 和不追高纪律。WDC/STX 虽未正式跌破硬线，但同主题相关性与盘后走弱要求组合级防御复核。

## 5. Institutional Overlay Scorecard

```text
flow_fragility_score: 11/14
flow_fragility_state: elevated / acute watch
trend_aligned_entry_score: 1/5
trend_aligned_entry_state: trend_broken
AI_quality/capex_cycle: MRVL/AMD/WDC/STX 均为 high capex-cycle sensitive；AMD/WDC/STX 不得升级为普通持有；MRVL 仅可作为小真实 starter 或模型 profit-protection hold
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high; consumer_backstop_fragility; VIX_data_gap; credit_data_gap
bottleneck_watch: AI memory/storage 与 interconnect 长期需求仍在，但 2026-06-09 价格拒绝追涨，watch only
action impact: block all new AI/semiconductor/storage adds; keep AMD reduce-review; keep WDC/STX defensive near-stop review; no MRVL chase
```

组合级相关风险复核：模型组合 4 个持仓全部暴露在 AI capex / semiconductor / storage / interconnect 高相关链条中。虽然单股权重均低于 15%，主题相关性高于单股风险，不能只看每只股票是否跌破硬止损。当前股票敞口 `39.78%` 可以接受，核心要求是保持现金、不新增同主题 beta、优先处理 AMD 和 STX。

## 6. 模型组合净值核对

模型组合继续沿用 2026-06-04 后的 USD 20,000 strategy-tracking ledger；无新增模型成交。

| Ticker | 股数 | 收盘价 | 市值 | 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 266.88 | 2,145.26 | 10.48% | core hold / profit-protection review |
| AMD | 4.6083 | 475.51 | 2,191.29 | 10.71% | reduce-review |
| WDC | 3.6880 | 517.72 | 1,909.35 | 9.33% | defensive hold / near-stop review |
| STX | 2.2401 | 846.01 | 1,895.15 | 9.26% | defensive hold / near-stop review |

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 8,141.05 |
| 现金 | USD 12,323.96 |
| 总资产 | USD 20,465.01 |
| 现金比例 | 60.22% |
| 股票敞口 | 39.78% |
| 持仓数量 | 4 |
| 主题数量 | 3，但高度重叠在 AI capex 链 |
| 最大单股权重 | AMD 10.71% |
| 累计收益 | USD 465.01 / +2.33% |

真实账户：用户确认的 `MRVL` 1 股成本 `252.00`，按 `266.88` 收盘估算市值 `USD 266.88`，未实现收益 `USD 14.88` / `+5.90%`，实际 HKD 权重、现金、费用、FX 仍以券商为准。

## 7. Replay Ledger

`experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 已存在 `2026-06-09,close` 行，未重复追加，未预填未来日期。该行已记录：

- close prices: MRVL `266.88`、AMD `475.51`、WDC `517.72`、STX `846.01`、SPY `737.05`、QQQ `707.83`、SMH `591.01`、VIX `21.80`
- baseline fear: `elevated`
- flow fragility: `11`, `elevated / acute watch`
- trend aligned entry: `1`, `trend_broken`
- baseline portfolio value: `20465.01`
- overlay portfolio value 留空，因为没有用户确认 AMD 模型减仓，也没有稳定的 overlay 自动成交假设。

## 8. 待办状态

- 关闭：`Complete formal U.S. post-close audit` 已由本文件完成。
- 继续打开：AMD `<492` reduce-review；STX near-stop priority；WDC defensive near-stop；真实账户 MRVL `<245`/`235` 风险线；旧 MRVL `315` 真实挂单是否存在仍需用户/券商确认；HYG/LQD 与 VIX/VIX3M 正式收盘数据源仍需修复。

## 9. 记忆更新边界

已更新/应同步：

- 创建本文件。
- 向 `daily-summaries.md` 追加简洁总结。
- 创建 `portfolio/2026-06-10-post-close-portfolio-summary.md`，保留正式收盘组合快照。
- 在 `todos/2026-06-10-strategy-todos.md` 标记正式盘后审计完成。

未更新 `decisions.md`：本次是单日 post-close 审计与 replay 观察，尚不足以升级为稳定规则。

