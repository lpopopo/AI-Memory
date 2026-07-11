# 2026-07-08 美股盘后正式审计

运行时间：2026-07-09 20:11 Asia/Shanghai。审计对象：2026-07-08 美股常规交易收盘。未登录券商，未提交真实订单，未虚构真实成交；真实持仓、现金、费用、FX、结算和 XLI 状态仍以用户或券商回报为准。

## 结论

本地 quote workflow 可用。按 `tools/README.md` 的 Node smoke test，`StockService.fetchQuotes` 返回结构化 `Tencent (Primary)` 对象；随后用 Yahoo Chart completed daily bars 交叉核对股票/ETF 收盘价，用 Cboe 官方历史 CSV 核对 VIX/VIX3M。未调用 Python fallback，也不需要 Google browser-visible snapshot。

Market Fear Gate 维持 `elevated 5/14`：VIX `16.90` 仍只是温和 elevated，VIX/VIX3M `0.868` 未倒挂，但 QQQ 仍低于 MA50，QQQ 63 日回撤约 `-4.65%`，SMH 63 日回撤仍约 `-11.35%`。框架风险乘数 `70%`，现金底线 `25%`，框架最大新买入敞口 `25%`。真实账户层面仍被 `GLW/DRAM/MXL/MRVL` 未闭环 completed-close stops 覆盖，实际新买入上限继续为 `0%`。

若 GLW `2`、DRAM `4`、MXL `6`、MRVL `4` 仍未卖出，估算 NAV 为 `USD 5,944.05`，现金 `USD 3,884.69 / 65.35%`，股票敞口 `34.65%`，最大单股 MRVL `15.59%`。这只是工作估算，不替代券商回报。

## 1. 收盘数据、来源与质量

| 标的 | 2026-07-08 收盘 | 日涨跌 | 主来源 | 交叉核验 | 质量 |
| --- | ---: | ---: | --- | --- | --- |
| MRVL | 231.71 | +0.44% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| AMD | 517.41 | +0.25% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| WDC | 550.30 | +3.42% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| STX | 860.02 | +3.91% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| SPY | 745.40 | -0.31% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| QQQ | 711.44 | +0.28% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| SMH | 593.00 | +1.99% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| SOXX | 562.03 | +1.87% | Node local quote workflow `Tencent (Primary)` | Yahoo Chart daily bar `2026-07-08` | high |
| VIX | 16.90 | +4.77% | Cboe official history CSV `07/08/2026` | Yahoo Chart consistent with Cboe close area | high |
| VIX3M | 19.46 | +2.37% | Cboe official history CSV `07/08/2026` | Yahoo latest metadata consistent | high |

数据时间戳：Yahoo 股票/ETF `regularMarketTime` 为 `2026-07-08T20:00:00Z` 附近；Cboe CSV 最后一行已更新到 `07/08/2026`。Tencent 返回的 `source` 均保留为 `Tencent (Primary)`；VIX 的 Tencent 结构化对象仍为低质量占位，不用于正式 VIX。

补充代理：

| 指标 | 2026-07-08 | 21 日变化 | 解读 |
| --- | ---: | ---: | --- |
| VIX/VIX3M | 0.868 | n/a | 正常 contango，未进入近端恐慌 |
| RSP/SPY | 0.28468 | +1.03% | 等权相对未恶化 |
| HYG/LQD | 0.73985 | +0.76% | 信用风险偏好未明显破坏 |
| IWM/SPY | 0.39372 | +3.10% | 小盘相对改善，非广义崩盘 |

## 2. 市场恐慌门控

`elevated 5/14`：

- VIX `16.90`：1 分；5 日变化未达到 +15%，VIX/VIX3M 未倒挂。
- SPY：63 日回撤约 `-1.87%`，仍在 MA50/MA200 之上。
- QQQ：63 日回撤约 `-4.65%`，且仍低于 MA50，计 2 分。
- SMH：63 日回撤约 `-11.35%`，虽然收回 MA50，但仍属于 meaningful stress，计 2 分。
- RSP/SPY、HYG/LQD、IWM/SPY 的 21 日相对变化没有触发恶化阈值。

框架参数：风险乘数 `70%`，最大总敞口 `75%`，现金底线 `25%`，最大新买入敞口 `25%`。组合覆盖：由于 unresolved-stop veto、`flow_fragility=11/14 acute`、`theme_overlap_high` 和 `sleeve_correlation_high`，真实账户实际新买入上限为 `0%`。

## 3. 真实账户 stop-trigger table

| 持仓 | 股数 | 收盘价 | 既有止损/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 184.03 | completed-close trailing stop `227` | 是，低约 `18.93%` | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；若仍持有，优先确认/执行 |
| DRAM | 4 | 62.04 | hard protection `70.50` | 是，低约 `12.00%` | 否，已触发 | `mandatory exit`；禁止摊低成本 |
| MXL | 6 | 86.05 | monotonic trailing stop `113.38`；core line `91-92` | 是，低约 `24.11%` / 低于 core line | 否，已触发 | `mandatory reduce/exit`；不能维持普通持有 |
| MRVL | 4 | 231.71 | completed-close failure line `260` | 是，低约 `10.88%` | 否，已触发 | `mandatory exit/reduce-review`；禁止因事件反弹自动追高 |

MU `1` 已由用户确认于 2026-07-06 以 `USD 1,010.00` 卖出，本轮不列为活跃持仓。XLI 旧订单状态仍未知，不计入 NAV。

## 4. AMD / WDC / STX replay 风险复核

这些不是当前真实账户活跃持仓，只用于历史模型、watchlist 和 replay 风险上下文。

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| AMD | 517.41 | 492 | 高约 `5.16%`，未触发 | `repair watch / no buy`；若后续收盘低于 492，必须转 `reduce-review` |
| WDC | 550.30 | 500 | 高约 `10.06%`，未触发但 63 日回撤深 | `defensive watch / no buy`；同主题相关风险仍高 |
| STX | 860.02 | 835 | 高约 `3.00%`，但刚从 2026-07-07 风险线下方修复 | `near-stop review / no add`；不能把单日修复当成追买信号 |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 11/14 -> acute
trend_aligned_entry_score: 1/5 -> trend_broken for active AI-capex sleeve
AI_quality/capex_cycle:
  GLW diversified_supplier / medium sensitivity, but price remains below stop and MA50;
  MRVL cyclical_supplier + bottleneck / high sensitivity, stop still failed despite small rebound;
  MXL speculative_bottleneck / high sensitivity, below trailing and core risk lines;
  DRAM thematic memory basket / high sensitivity, below hard protection;
  AMD/WDC/STX are high-sensitivity watch/replay names, not authorized buys.
factor_macro_flags:
  theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  momentum_reversal_high; growth_duration_high; semiconductor_basket_unwind;
  unresolved_stop_veto.
bottleneck_watch:
  Kay GPT/token-intensity, MRVL path-compression, DeepSeek custom-chip and NVIDIA/Vera CPU
  observations remain monitoring fields only. They do not override price rejection or stops.
action impact:
  block all new buys; run portfolio-level correlated-risk review before single-stock optimism;
  clear GLW/DRAM/MXL/MRVL stop facts and XLI order state before any diversification or re-entry.
```

组合级相关风险复核：活跃股票敞口仍全部是 AI-capex / semiconductor-cycle / bottleneck-chain 风险。GLW/MXL/MRVL 光互联/组件链合计约 `30.47%` NAV，已超过单一子主题 `25%` 约束；加 DRAM 后，AI-capex 总敞口约 `34.65%` NAV。虽然市场从 2026-07-07 的半导体急跌中反弹，但这只是降低了当日跌速，没有解除未闭环止损或主题相关性。

## 6. 组合净值核对

真实账户工作估算，前提：沿用现金 `USD 3,884.69`；不假设 GLW/DRAM/MXL/MRVL 已卖出；XLI 未计入。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 184.03 | 368.06 | 6.19% | triggered exit/reduce |
| DRAM | 4 | 62.04 | 248.16 | 4.18% | triggered exit |
| MXL | 6 | 86.05 | 516.30 | 8.69% | triggered reduce/exit |
| MRVL | 4 | 231.71 | 926.84 | 15.59% | triggered exit/reduce-review |

- 估算股票市值：`USD 2,059.36`
- 估算现金：`USD 3,884.69 / 65.35%`
- 估算 NAV：`USD 5,944.05`
- 股票敞口：`34.65%`
- 持仓数量：`4`
- 名义主题数：`2`；有效大主题数：`1`，AI capex
- 最大单股权重：MRVL `15.59%`

退休历史模型/replay 口径：固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金占位 `USD 12,323.96`。按 2026-07-08 收盘估算股票市值 `USD 8,202.97`，NAV `USD 20,526.93`，现金 `60.04%`，股票 `39.96%`，最大单股 AMD 约 `11.62%`。这不是当前真实账户。

## 7. Replay 和记忆处理

- 向 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-08 已完成收盘行；未预填未来日期。
- 创建 `memory/portfolio/2026-07-08-portfolio-summary.md`。
- 创建 `memory/todos/2026-07-08-strategy-todos.md`。
- 向 `memory/daily-summaries.md` 追加一条简洁总结。
- `decisions.md` 不更新：本轮仍是单日审计、单日修复和未闭环风险延续，没有新的稳定规则证据。

非投资建议。
