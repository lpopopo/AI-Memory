# 2026-07-09 美股盘后正式审计

运行时间：2026-07-10 04:20 Asia/Shanghai。审计对象：2026-07-09 美股常规交易收盘。未登录券商，未提交真实订单，未虚构真实成交；真实持仓、现金、费用、FX、结算和 XLI 状态仍以用户或券商回报为准。

## 结论

本地 quote workflow 可用。按 `tools/README.md` 的 Node smoke test，`StockService.fetchQuotes` 返回结构化 `Tencent (Primary)` 对象；随后用 Yahoo Chart completed daily bars 交叉核对股票/ETF 收盘价。Tencent 的 VIX 仍是低质量占位，未用于正式 VIX。Cboe 官方 VIX 历史 CSV 运行时仍停在 2026-07-08；2026-07-09 VIX 使用 Cboe VIX 产品页官方延迟报价 `$15.84` 并以 Yahoo Chart `15.86` 交叉核对。VIX3M 使用 Yahoo Chart/Google Finance browser-visible snapshot `19.00`；Cboe/FRED 历史序列尚未更新到 2026-07-09。

Market Fear Gate 从 2026-07-08 的 `elevated 5/14` 回落为 `normal 2/14`：VIX 回到 16 下方，VIX/VIX3M 约 `0.834`，SPY/QQQ 均在 MA50 上方；但 SMH 63 日回撤仍约 `-9.15%`，保留 2 分 stress 记分。框架风险乘数 `100%`、现金底线 `5%`、最大新买入敞口 `50%`。真实账户层面仍被 `GLW/DRAM/MXL/MRVL` 未闭环完成收盘止损覆盖，且 `flow_fragility=elevated/near-acute`、`theme_overlap_high`、`sleeve_correlation_high` 仍为真，所以实际新买入上限继续为 `0%`。

若 GLW `2`、DRAM `4`、MXL `6`、MRVL `4` 仍未卖出，且 QCOM `2 @ 187.50` 仍持有，估算 NAV 为 `USD 6,081.29`，现金 `USD 3,508.69 / 57.70%`，股票敞口 `42.30%`，最大单股 MRVL `16.00%`。这只是工作估算，不替代券商回报。

## 1. 收盘数据、来源与质量

| 标的 | 2026-07-09 收盘 | 日涨跌 | 主来源 | 交叉核验 | 质量 |
| --- | ---: | ---: | --- | --- | --- |
| MRVL | 243.27 | +4.99% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-09 20:00Z` | high |
| AMD | 546.72 | +5.67% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| WDC | 578.05 | +5.04% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| STX | 890.09 | +3.50% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| SPY | 751.71 | +0.85% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| QQQ | 723.28 | +1.66% | Yahoo Chart completed daily bar | Node Tencent `723.23` within rounding | high |
| SMH | 607.73 | +2.48% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| SOXX | 581.70 | +3.50% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar | high |
| VIX | 15.84 | -6.27% | Cboe VIX official product page, as of July 9, 2026 | Yahoo Chart daily bar `15.86`; Cboe history CSV not yet updated | medium-high |
| VIX3M | 19.00 | about -2.36% | Yahoo Chart completed daily bar / Google browser-visible snapshot | Google Finance visible price `19.00`, time `Jul 9, 3:04:16 PM GMT-5` | medium-high |

数据时间戳：股票/ETF Yahoo `regularMarketTime` 为 `2026-07-09T20:00:00Z` 附近；Cboe VIX 产品页显示 `as of July 9, 2026`，页面 market data 为 `7/9/2026`；Google Finance VIX3M 页面显示 `Jul 9, 3:04:16 PM GMT-5`。源 URL：`https://query1.finance.yahoo.com/v8/finance/chart/`、`https://www.cboe.com/tradable-products/vix/`、`https://www.google.com/finance/beta/quote/VIX3M%3AINDEXCBOE`。

补充代理：

| 指标 | 2026-07-09 | 21 日变化 | 解读 |
| --- | ---: | ---: | --- |
| VIX/VIX3M | 0.834 | n/a | 正常 contango，未进入近端恐慌 |
| RSP/SPY | 0.28402 | +1.13% | 等权相对未恶化 |
| HYG/LQD | 0.74041 | +0.59% | 信用风险偏好未破坏 |
| IWM/SPY | 0.39546 | +2.89% | 小盘相对改善 |

## 2. 市场恐慌门控

`normal 2/14`：

- VIX `15.84`，低于 16，计 0 分；5 日变化未触发压力；VIX/VIX3M `0.834`，未倒挂。
- SPY 63 日回撤约 `-1.03%`，收盘高于 MA50。
- QQQ 63 日回撤约 `-3.07%`，收盘高于 MA50。
- SMH 63 日回撤约 `-9.15%`，虽收回 MA50，但仍属于 meaningful stress，计 2 分。
- RSP/SPY、HYG/LQD、IWM/SPY 的 21 日相对变化均未触发恶化阈值。

框架参数：风险乘数 `100%`，最大总敞口 `95%`，现金底线 `5%`，最大新买入敞口 `50%`。组合覆盖：由于 unresolved-stop veto、`flow_fragility=elevated/near-acute`、`theme_overlap_high` 和 `sleeve_correlation_high`，真实账户实际新买入上限为 `0%`。

## 3. 真实账户 stop-trigger table

| 持仓 | 股数 | 收盘价 | 既有止损/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 192.53 | completed-close trailing stop `227` | 是，低约 `15.18%` | 否，已触发 | `maximum-severity mandatory exit/reduce`；若仍持有，优先确认/执行 |
| DRAM | 4 | 64.36 | hard protection `70.50` | 是，低约 `8.71%` | 否，已触发 | `mandatory exit`；禁止摊低成本 |
| MXL | 6 | 95.80 | monotonic trailing stop `113.38`；core line `91-92` | 是，低约 `15.51%`；已重新高于 core line | 否，已触发 | `mandatory reduce/exit`；反弹只能用于风险降低，不是加仓信号 |
| MRVL | 4 | 243.27 | completed-close failure line `260` | 是，低约 `6.43%` | 否，已触发 | `mandatory exit/reduce-review`；禁止因事件反弹自动追高 |
| QCOM | 2 | 191.11 | review below `185`; completed close `<182` = failed-entry review | 否 | 否 | `hold/watch only`；不加仓，继续核对券商费用和结算 |

MU `1` 已由用户确认于 2026-07-06 以 `USD 1,010.00` 卖出，本轮不列为活跃持仓。XLI 旧订单状态仍未知，不计入 NAV。

## 4. AMD / WDC / STX replay 风险复核

这些不是当前真实账户活跃持仓，只用于历史模型、watchlist 和 replay 风险上下文。

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| AMD | 546.72 | 492 | 高约 `11.12%`，未触发；仍高于 MA50 | `repair watch / no buy`；若后续收盘低于 492，必须转 `reduce-review` |
| WDC | 578.05 | 500 | 高约 `15.61%`，未触发，但 63 日回撤仍深 | `defensive watch / no buy`；同主题相关风险仍高 |
| STX | 890.09 | 835 | 高约 `6.60%`，但刚从 2026-07-07 风险线下方修复 | `near-stop history / no add`；单日修复不能当成追买信号 |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 10/14 -> elevated / near-acute
trend_aligned_entry_score: 1/5 -> trend_broken for active AI-capex sleeve
AI_quality/capex_cycle:
  GLW diversified_supplier / medium sensitivity, but price remains below completed-close stop;
  MRVL cyclical_supplier + bottleneck / high sensitivity, still below 260 failure line;
  MXL speculative_bottleneck / high sensitivity, below monotonic trailing stop despite rebound;
  DRAM thematic memory basket / high sensitivity, below hard protection;
  QCOM diversified_supplier / edge_inference, medium-high sensitivity, small confirmed hold but below MA50;
  AMD/WDC/STX are high-sensitivity watch/replay names, not authorized buys.
factor_macro_flags:
  theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  momentum_reversal_high; growth_duration_high; semiconductor_basket_repair;
  unresolved_stop_veto.
bottleneck_watch:
  optical/interconnect and memory/storage remain hot rebound pockets, but the public-source rerun
  added no new high-evidence event after the strict window.
action impact:
  keep zero new buys; run portfolio-level correlated-risk review before single-stock optimism;
  clear GLW/DRAM/MXL/MRVL stop facts and XLI order state before any diversification or re-entry.
```

组合级相关风险复核：活跃股票敞口几乎全部属于 AI-capex / semiconductor-cycle / bottleneck-chain 共同因子。GLW、MXL、MRVL、DRAM 与 QCOM 共同构成约 `42.30%` NAV 的相关科技/半导体敞口；QCOM 的 edge-inference 标签改善了单一 ticker 分散度，但没有解除 sleeve correlation。今天的反弹降低了当日跌速，没有解除未闭环止损或共同因子集中风险。

## 6. 组合净值核对

真实账户工作估算，前提：沿用盘中后现金 `USD 3,508.69`；不假设 GLW/DRAM/MXL/MRVL 已卖出；QCOM `2 @ 187.50` 已计入；XLI 未计入。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 192.53 | 385.06 | 6.33% | triggered exit/reduce |
| DRAM | 4 | 64.36 | 257.44 | 4.23% | triggered exit |
| MXL | 6 | 95.80 | 574.80 | 9.45% | triggered reduce/exit |
| MRVL | 4 | 243.27 | 973.08 | 16.00% | triggered exit/reduce-review |
| QCOM | 2 | 191.11 | 382.22 | 6.29% | hold/watch only |

- 估算股票市值：`USD 2,572.60`
- 估算现金：`USD 3,508.69 / 57.70%`
- 估算 NAV：`USD 6,081.29`
- 股票敞口：`42.30%`
- 持仓数量：`5`
- 名义主题数：`2`；有效大主题数：`1`，AI-capex / semiconductor
- 最大单股权重：MRVL `16.00%`

退休历史模型 replay 口径：固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金 `USD 12,323.96`。按 2026-07-09 收盘估算股票市值 `USD 8,600.67`，NAV `USD 20,924.63`，现金 `58.90%`，股票 `41.10%`，最大单股 AMD 约 `12.04%`。这不是当前真实账户。

## 7. Replay 和记忆处理

- 向 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-09 已完成收盘行；未预填未来日期。
- 更新 `memory/portfolio/2026-07-09-portfolio-summary.md`。
- 更新 `memory/todos/2026-07-09-strategy-todos.md`。
- 向 `memory/daily-summaries.md` 追加一条简洁总结。
- `decisions.md` 不更新：本轮是单日反弹、单日风险审计和既有止损延续，没有新的稳定规则证据。

非投资建议。
