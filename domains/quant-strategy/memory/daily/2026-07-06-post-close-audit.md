# 2026-07-06 美股盘后正式审计

运行时间：2026-07-07 08:02 Asia/Shanghai。审计对象：2026-07-06 美股常规交易收盘。未登录券商，未提交真实订单，未虚构真实成交；真实持仓、现金、费用、FX、结算和 XLI 状态仍以用户或券商回报为准。

## 结论

本地 quote workflow 可用。Node smoke test 先返回 MRVL、AMD、WDC、STX、SPY、QQQ、SMH/SOXX、RSP、HYG、LQD、IWM 等结构化 `Tencent (Primary)` 对象；Yahoo completed daily bars 交叉确认 2026-07-06 收盘。VIX 未在 Tencent 批量对象中返回，使用 Yahoo Chart 日线和 Cboe VIX 页面可见快照交叉核验；Cboe VIX 历史 CSV 本轮仍停在 2026-07-03，标为待更新。VIX3M 使用 Cboe 官方历史 CSV 和 Yahoo Chart 一致值。

市场恐慌门控为 `normal 2/14`，风险乘数 `100%`，框架现金底线 `5%`，框架新买入上限 `50%`。但真实账户层面仍有 GLW、DRAM、MXL、MRVL 四个未解决 completed-close 风险项，且全部属于同一个 AI-capex 高相关篮子；账户级 unresolved-stop veto 后，实际新买入上限仍是 `0%`。

MU 已按用户确认 `1 @ USD 1,010.00` 卖出并从活跃持仓移除。本次估算只把这笔已确认成交计入现金，不假设 GLW/DRAM/MXL/MRVL 已成交退出。

## 1. 收盘数据、来源与质量

| 标的 | 2026-07-06 收盘 | 日涨跌 | 主要来源 | 质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 249.27 | +1.62% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| AMD | 552.05 | +6.61% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| WDC | 577.46 | +7.14% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| STX | 868.26 | +5.86% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SPY | 751.28 | +0.87% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| QQQ | 722.82 | +1.43% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SMH | 604.30 | +2.03% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| SOXX | 581.51 | +2.68% | Node local quote workflow `Tencent (Primary)`；Yahoo Chart daily bar 交叉确认 | high |
| VIX | 15.57 | -3.59% | Yahoo Chart completed daily bar；Cboe VIX product page visible snapshot；Cboe history CSV pending 7/6 update | medium-high |
| VIX3M | 18.78 | -1.37% | Cboe official VIX3M history CSV；Yahoo Chart daily bar cross-check | high |

补充代理：

| 指标 | 2026-07-06 | 21 日变化 | 解读 |
| --- | ---: | ---: | --- |
| VIX/VIX3M | 0.829 | n/a | 正常 contango，非近端恐慌 |
| RSP/SPY | 0.28618 | +3.15% | 等权相对不恶化，但当日 RSP 明显弱于 QQQ/SMH |
| HYG/LQD | 0.73498 | +0.19% | 信用风险偏好稳定 |
| IWM/SPY | 0.39785 | +4.31% | 小盘 21 日相对改善，但当日仍弱于 Nasdaq/半导体 |

数据时间戳：Yahoo Chart `regularMarketTime` 对股票/ETF 多为 `2026-07-06T20:00:00Z` 附近，VIX/VIX3M 为 `2026-07-06T20:15:01Z`。本轮不需要 Python fallback 或 Google browser-visible snapshot。

## 2. 市场恐慌门控

`normal 2/14`：

- VIX `15.57`，5 日变化约 `-15.43%`；VIX/VIX3M `0.829`，无波动率恐慌点。
- SPY/QQQ/SMH 63 日回撤约 `-1.09% / -3.13% / -9.66%`；SMH 仍处在有意义回撤区，贡献主要风险点。
- SPY、QQQ、SMH 均高于 MA50/MA200。
- RSP/SPY、HYG/LQD、IWM/SPY 的 21 日变化未触发恶化阈值。

框架参数：风险乘数 `100%`，最大总敞口 `95%`，现金底线 `5%`，最大新买入敞口 `50%`。组合覆盖：由于未解决 completed-close stops、`flow_fragility=11/14 acute`、`theme_overlap_high`、`sleeve_correlation_high`，真实账户实际新买入上限为 `0%`。

## 3. 真实账户 stop-trigger table

| 持仓 | 股数 | 2026-07-06 收盘 | 既有止损/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 194.80 | completed-close trailing stop `227` | 是，低约 14.19% | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；若仍持有，优先确认/执行 |
| DRAM | 4 | 64.76 | hard protection `70.50` | 是，低约 8.14% | 否，已触发 | `mandatory exit`；禁止摊低成本 |
| MXL | 6 | 95.68 | monotonic trailing stop `113.38` | 是，低约 15.61% | 否，已触发 | `mandatory reduce/exit`；高点 104.34 仍远低于风险线 |
| MRVL | 4 | 249.27 | completed-close failure line `260` | 是，低约 4.13% | 否，已触发 | `mandatory exit/reduce-review`；盘中触及 260.46 不能替代收盘 reclaim，禁止因反弹追高或下调风险线 |

已关闭项：MU `1` 已由用户确认在 2026-07-06 以 `USD 1,010.00` 卖出，估算卖出费 `USD 1.00`。本审计不再把 MU 列为活跃持仓。

## 4. AMD / WDC / STX replay 风险复核

这些不是当前真实账户持仓，只用于历史模型和 watch/replay 风险上下文。

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| AMD | 552.05 | 492 | 高约 12.21%，未触发 | `repair watch / no buy`；不标 active reduce-review，但趋势确认前不追 |
| WDC | 577.46 | 500 | 高约 15.49%，未 near-stop | `defensive watch / no buy`；仍受同主题相关风险约束 |
| STX | 868.26 | 835 | 高约 3.98%，接近风险线 | `defensive hold / near-stop review`；不追高 |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 11/14 -> acute
trend_aligned_entry_score: 1/5 -> trend_broken for active AI-capex sleeve
AI_quality/capex_cycle:
  GLW diversified supplier / medium sensitivity / about 7/10;
  MRVL cyclical supplier + bottleneck / high sensitivity / about 6/10;
  MXL speculative bottleneck / high sensitivity / about 4/10;
  DRAM thematic memory basket / high sensitivity / about 5/10;
  MU closed, watch-only after stop-discipline sale
factor_macro_flags:
  theme_overlap_high; sleeve_correlation_high; momentum_reversal_high;
  growth_duration_high; AI_capex_cycle_high; semiconductor_rebound_but_concentrated
bottleneck_watch:
  storage/memory and AI interconnect rebounded, but MRVL remains below 260 and GLW remains weak;
  no new bottleneck evidence overrides completed-close stops
action impact:
  block all new buys; treat GLW/DRAM/MXL/MRVL as one AI-capex correlated basket;
  clear stop and broker-order facts before any diversification or re-entry
```

组合级相关风险复核：活跃股票敞口 `100%` 仍是 AI-capex 相关风险。GLW/MXL/MRVL 光互联/组件链合计约 `32.11%` NAV，超过单一子主题 `25%` 上限；加上 DRAM 后，AI-capex 总敞口约 `36.37%` NAV。MU 卖出降低了记忆/半导体单名风险，但没有清除主题重叠和 unresolved-stop veto。

## 6. 组合净值核对

真实账户工作估算，前提：2026-07-03 工作现金 `USD 2,875.69`；计入用户确认 MU 卖出净现金约 `USD 1,009.00`；GLW/DRAM/MXL/MRVL 未假设已卖；XLI 未计入。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 194.80 | 389.60 | 6.38% | triggered exit/reduce |
| DRAM | 4 | 64.76 | 259.04 | 4.24% | triggered exit |
| MXL | 6 | 95.68 | 574.08 | 9.40% | triggered reduce/exit |
| MRVL | 4 | 249.27 | 997.08 | 16.33% | triggered exit/reduce-review |

- 估算股票市值：`USD 2,219.80`。
- 估算现金：`USD 3,884.69 / 63.63%`。
- 估算 NAV：`USD 6,104.49`。
- 股票敞口：`36.37%`。
- 持仓数量：`4`。
- 名义主题数量：`2`；有效大主题数量：`1`，AI capex。
- 最大单股权重：MRVL `16.33%`，高于 normal core 15% 且趋势失败。

退休历史模型/replay 口径：固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金占位 `USD 12,323.96`。按 2026-07-06 收盘估算股票市值 `USD 8,622.38`，NAV `USD 20,946.34`，现金 `58.84%`，股票 `41.16%`，持仓 `4`，最大单股 AMD `12.15%`。这不是当前真实账户。

## 7. Replay 和记忆处理

- 向 `experiments/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-06 已完成收盘行；未预填未来日期。
- 创建 `memory/portfolio/2026-07-06-portfolio-summary.md`。
- 创建 `memory/todos/2026-07-06-strategy-todos.md`。
- 向 `memory/daily-summaries.md` 追加一条简洁总结。
- `decisions.md` 不更新：本轮为单日审计、单日反弹和未解决止损复核，没有新的稳定规则证据。

非投资建议。
