# 2026-07-07 美股盘后正式审计

运行时间：2026-07-08 09:36 Asia/Shanghai。审计对象：2026-07-07 美股常规交易收盘。未登录券商，未提交真实订单，未虚构真实成交；真实持仓、现金、费用、FX、结算和 XLI 状态仍以用户或券商回报为准。

## 结论

本地 quote workflow 可用。Node smoke test 先返回 MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、RSP、HYG、LQD、IWM、GLW、DRAM、MXL 等结构化 `Tencent (Primary)` 对象；随后用同一 `StockService` 本地传输栈读取 Yahoo Chart completed daily bars 交叉核验。VIX/VIX3M 使用 Cboe 官方历史 CSV，并由 Yahoo Chart 日线一致确认。

广义 Market Fear Gate 从盘中估计的 `normal` 上调为 `elevated 5/14`：VIX 仍不高，但 QQQ 与 SMH 跌破 50 日线，SMH 63 日回撤扩大到约 `-13.07%`。框架风险乘数 `70%`，现金底线 `25%`，框架最大新买入敞口 `25%`。真实账户层面仍有 GLW、DRAM、MXL、MRVL 四个未解决 completed-close 风险项，且全部属于同一个 AI-capex 高相关篮子；账户级 unresolved-stop veto 后，实际新买入上限仍为 `0%`。

MU 继续按用户确认 `1 @ USD 1,010.00` 已卖出并从活跃持仓移除。本次估算只把这笔已确认成交计入现金，不假设 GLW/DRAM/MXL/MRVL 已成交退出。

## 1. 收盘数据、来源与质量

| 标的 | 2026-07-07 收盘 | 日涨跌 | 主要来源 | 质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 230.70 | -7.45% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| AMD | 516.11 | -6.51% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| WDC | 532.10 | -7.86% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| STX | 827.64 | -4.68% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SPY | 747.71 | -0.48% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| QQQ | 709.43 | -1.85% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SMH | 581.45 | -3.78% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SOXX | 551.69 | -5.13% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| VIX | 16.13 | +3.60% | Cboe official history CSV；Yahoo Chart daily bar 交叉确认 | high |
| VIX3M | 19.01 | +1.22% vs 2026-07-06 Cboe close | Cboe official history CSV；Yahoo Chart daily bar 交叉确认 | high |

补充代理：

| 指标 | 2026-07-07 | 21 日变化 | 解读 |
| --- | ---: | ---: | --- |
| VIX/VIX3M | 0.848 | n/a | 正常 contango，未进入近端恐慌 |
| RSP/SPY | 0.28718 | +3.13% | 等权相对改善，广度未确认恐慌 |
| HYG/LQD | 0.73934 | +0.81% | 信用风险偏好稳定 |
| IWM/SPY | 0.39613 | +2.70% | 小盘 21 日相对改善，但当日仍弱于 SPY |

数据时间戳：Yahoo Chart 股票/ETF `regularMarketTime` 多为 `2026-07-07T20:00:00Z` 附近，VIX/VIX3M 为 `2026-07-07T20:15:01Z`；Cboe CSV 最后一行已更新到 `07/07/2026`。本轮不需要 Python fallback 或 Google browser-visible snapshot。

## 2. 市场恐慌门控

`elevated 5/14`：

- VIX `16.13`，5 个交易日变化约 `-1.95%`；VIX/VIX3M `0.848`，无波动率倒挂。
- SPY 63 日回撤约 `-1.56%`，仍高于 MA50/MA200。
- QQQ 63 日回撤约 `-4.92%`，跌破 MA50 但仍高于 MA200。
- SMH 63 日回撤约 `-13.07%`，跌破 MA50 但仍高于 MA200，是本轮主要风险点。
- RSP/SPY、HYG/LQD、IWM/SPY 的 21 日变化未触发恶化阈值。

框架参数：风险乘数 `70%`，最大总敞口 `75%`，现金底线 `25%`，最大新买入敞口 `25%`。组合覆盖：由于未解决 completed-close stops、`flow_fragility=12/14 acute`、`theme_overlap_high`、`sleeve_correlation_high`，真实账户实际新买入上限为 `0%`。

## 3. 真实账户 stop-trigger table

| 持仓 | 股数 | 2026-07-07 收盘 | 既有止损/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 185.38 | completed-close trailing stop `227` | 是，低约 18.34% | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；若仍持有，优先确认/执行 |
| DRAM | 4 | 60.59 | hard protection `70.50` | 是，低约 14.06% | 否，已触发 | `mandatory exit`；禁止摊低成本 |
| MXL | 6 | 85.82 | monotonic trailing stop `113.38`；core line `91-92` | 是，低约 24.31% / 5.7%-6.7% | 否，已触发 | `mandatory reduce/exit`；收盘低于 core line，不能维持普通持有 |
| MRVL | 4 | 230.70 | completed-close failure line `260` | 是，低约 11.27% | 否，已触发 | `mandatory exit/reduce-review`；禁止因事件或反弹自动追高 |

已关闭项：MU `1` 已由用户确认在 2026-07-06 以 `USD 1,010.00` 卖出，估算卖出费 `USD 1.00`。本审计不再把 MU 列为活跃持仓。

## 4. AMD / WDC / STX replay 风险复核

这些不是当前真实账户活跃持仓，只用于历史模型、watchlist 和 replay 风险上下文。

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| AMD | 516.11 | 492 | 高约 4.90%，未触发 | `repair watch / no buy`；若后续收盘低于 492，必须转 `reduce-review` |
| WDC | 532.10 | 500 | 高约 6.42%，未触发但回撤剧烈 | `defensive watch / no buy`；同主题相关风险仍高 |
| STX | 827.64 | 835 | 低约 0.88%，触发历史风险线 | `reduce-review`；不得按普通 defensive hold 处理 |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 12/14 -> acute
trend_aligned_entry_score: 1/5 -> trend_broken for active AI-capex sleeve
AI_quality/capex_cycle:
  GLW diversified supplier / medium sensitivity / about 7/10, but price rejected;
  MRVL cyclical supplier + bottleneck / high sensitivity / about 6/10, stop failed;
  MXL speculative bottleneck / high sensitivity / about 4/10, stop failed;
  DRAM thematic memory basket / high sensitivity / about 5/10, hard protection failed;
  AMD/WDC/STX remain high-sensitivity watch/replay names, not authorized buys
factor_macro_flags:
  theme_overlap_high; sleeve_correlation_high; momentum_reversal_high;
  growth_duration_high; AI_capex_cycle_high; semiconductor_basket_unwind;
  defensive_rotation_visible
bottleneck_watch:
  Kay Kyber/Rubin/CPO framework remains an observation field, but 2026-07-07 price action rejected
  the AI-capex basket; bottleneck narrative does not override stops.
action impact:
  block all new buys; run portfolio-level correlated-risk review before any single-stock optimism;
  clear GLW/DRAM/MXL/MRVL stop facts and XLI order state before diversification or re-entry.
```

组合级相关风险复核：活跃股票敞口 `100%` 仍是 AI-capex 相关风险。GLW/MXL/MRVL 光互联/组件链合计约 `30.48%` NAV，超过单一子主题 `25%` 上限；加上 DRAM 后，AI-capex 总敞口约 `34.55%` NAV。MU 卖出降低了记忆/半导体单名风险，但没有清除主题重叠和 unresolved-stop veto。

## 6. 组合净值核对

真实账户工作估算，前提：沿用 2026-07-06 working cash `USD 3,884.69`；GLW/DRAM/MXL/MRVL 未假设已卖；XLI 未计入。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 185.38 | 370.76 | 6.25% | triggered exit/reduce |
| DRAM | 4 | 60.59 | 242.36 | 4.08% | triggered exit |
| MXL | 6 | 85.82 | 514.92 | 8.68% | triggered reduce/exit |
| MRVL | 4 | 230.70 | 922.80 | 15.55% | triggered exit/reduce-review |

- 估算股票市值：`USD 2,050.84`。
- 估算现金：`USD 3,884.69 / 65.45%`。
- 估算 NAV：`USD 5,935.53`。
- 股票敞口：`34.55%`。
- 持仓数量：`4`。
- 名义主题数量：`2`；有效大主题数量：`1`，AI capex。
- 最大单股权重：MRVL `15.55%`，高于 normal core 15% 附近且趋势失败。

退休历史模型/replay 口径：固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金占位 `USD 12,323.96`。按 2026-07-07 收盘估算股票市值 `USD 8,048.97`，NAV `USD 20,372.93`，现金 `60.49%`，股票 `39.51%`，持仓 `4`，最大单股 AMD 约 `11.67%`。这不是当前真实账户。

## 7. Replay 和记忆处理

- 向 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-07 已完成收盘行；未预填未来日期。
- 更新 `memory/portfolio/2026-07-07-portfolio-summary.md` 为正式收盘版。
- 更新 `memory/todos/2026-07-07-strategy-todos.md`。
- 向 `memory/daily-summaries.md` 追加一条简洁总结。
- `decisions.md` 不更新：本轮为单日审计和单日 AI-capex 同步下跌复核，没有新的稳定规则证据。

非投资建议。
