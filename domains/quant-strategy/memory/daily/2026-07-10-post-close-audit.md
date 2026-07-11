# 2026-07-10 美股盘后正式审计

运行时间：2026-07-11 10:21 Asia/Shanghai。审计对象：2026-07-10 美股常规交易收盘。未登录券商、未提交订单、未虚构成交；真实账户、现金、费用、FX 与结算以用户或券商回报为准。

## 结论

本地 Node Quote Workflow 可用：按 `tools/README.md` 的 smoke test，`StockService.fetchQuotes` 对 MRVL、AMD、SPY、QQQ、SMH 及扩展标的返回结构化 `Tencent (Primary)` quote objects。其价格与 7 月 9 日收盘字段衔接，故作为 7 月 10 日收盘后快照使用。Yahoo Chart 日线交叉请求在本轮连续返回 HTTP 404；这不是本地 workflow 不可用，且未写作“local quote workflow unavailable”。Bundled Python 的市场恐慌脚本因环境缺少 `yfinance` 未能作为第二条日线来源；不使用裸 `python.exe`。

VIX 的 Tencent 值 `21.67` 是停滞占位，不用于正式恐慌计算。公开 VIX 历史页显示 2026-07-10 收盘 `22.22`（日变动 `+11.83%`，中等质量）；Cboe 产品页/历史页本轮可见数据仅到 7 月 8 日。VIX3M 无本轮同日可验证收盘，采用上一次已验证的 7 月 9 日 `19.00` 作期限结构近似，明确标为日期错配、低一档质量。故采用保守的 `stress 9/14`：VIX 水平 2 分、VIX 相对 7 月 2 日 `16.15` 的五日约 `+37.6%` 计 2 分、约 `VIX/VIX3M=1.17` 计 3 分、SMH 仍约处 63 日 `-8%` 至 `-9%` 回撤区间计 2 分。缺失的日线趋势/广度字段不追加乐观抵扣。

框架参数：风险乘数 `40%`、最大总股票敞口 `55%`、现金底线 `45%`、最大新买入敞口 `10%`。实际新增买入上限仍为 `0%`：压力门控下没有有效趋势确认，且当前四只持仓仍高度暴露于同一 AI-capex/半导体共同因子。

## 1. 收盘数据、来源与质量

| 标的 | 7 月 10 日收盘/快照 | 日变动 | 来源 | 数据质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 235.81 | -3.04% | 本地 Node `Tencent (Primary)` | medium-high |
| AMD | 557.89 | +2.04% | 本地 Node `Tencent (Primary)` | medium-high |
| WDC | 582.59 | +0.78% | 本地 Node `Tencent (Primary)` | medium-high |
| STX | 910.34 | +2.28% | 本地 Node `Tencent (Primary)` | medium-high |
| SPY | 754.95 | +0.43% | 本地 Node `Tencent (Primary)` | medium-high |
| QQQ | 725.51 | +0.31% | 本地 Node `Tencent (Primary)` | medium-high |
| SMH | 611.03 | +0.54% | 本地 Node `Tencent (Primary)` | medium-high |
| SOXX | 581.34 | -0.06% | 本地 Node `Tencent (Primary)` | medium-high |
| VIX | 22.22 | +11.83% | [Investing.com 历史收盘页](https://au.investing.com/indices/volatility-s-p-500-historical-data) | medium |
| VIX3M | 19.00（7 月 9 日最后已验证） | n/a | 上一正式审计的 Yahoo/Google browser-visible 交叉记录 | low-medium，日期错配 |
| RSP | 214.30 | +0.37% | 本地 Node `Tencent (Primary)` | medium-high |
| HYG | 79.71 | -0.05% | 本地 Node `Tencent (Primary)` | medium-high |
| LQD | 107.46 | -0.23% | 本地 Node `Tencent (Primary)` | medium-high |
| IWM | 295.99 | -0.42% | 本地 Node `Tencent (Primary)` | medium-high |

补充代理：当日 `RSP/SPY=0.28386`、`HYG/LQD=0.74177`、`IWM/SPY=0.39207`，但因完整 21 日序列交叉源本轮不可用，仅作横截面观察，不给其额外计分。收盘后本地 workflow 运行于 2026-07-11 10:21 Asia/Shanghai；其对象含 previous close、OHLC 与成交量。公开来源与本地行情均不替代券商成交回报。

## 2. 市场恐慌门控

`stress 9/14（保守、VIX3M 日期错配）`

- VIX `22.22`：进入 stress volatility 区间，2 分。
- VIX 五日约 `+37.6%`：大于 +30%，2 分。
- `VIX/VIX3M` 约 `1.17`：近端高于远端；VIX3M 非同日，仍按保守 3 分处理，下一正式收盘必须重新核验。
- SMH 较最近已验证的 63 日高位仍处约 `-8%` 至 `-9%` meaningful-stress 区间，2 分；SPY/QQQ 未见收盘趋势破坏的可信新证据，不加分也不作乐观覆盖。
- RSP/SPY、HYG/LQD、IWM/SPY 21 日变化：数据缺口，不计分。

这不是买入许可。即使框架上限为 10%，压力门控、共同因子集中和所有活跃仓位均未满足新一轮底部确认，故实际新买入 `0%`。

## 3. 活跃持仓 stop-trigger table

7 月 10 日用户的长期重分类覆盖了 GLW/MRVL/MXL 的旧短线 completed-close 退出线；下表不把未提交的 189.20/92.20/235.20 stop-market 建议写成真实订单。

| 持仓 | 股数 | 收盘 | 既有风险/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 190.89 | 长期加仓须 completed close `200-205` 上方并守住约 `190`；周线 `<166-167` 重验逻辑 | 否（旧 227 短线线已被规则覆盖） | 是，距 190 约 +0.47% | `near-support hold / no add`；若完成收盘失守 190，停止底部累积并复核 |
| MRVL | 4 | 235.81 | 不加仓，除非权重降至约 12% 以下且 close 稳在 `250-260`；周线 `<223` 重验 | 否（旧 260 线已被规则覆盖） | 是，距周线重验约 +5.7% | `near-weekly-risk review / no add`；不得因事件反弹追高 |
| MXL | 6 | 91.30 | 不加仓，除非权重约 6% 以下、业绩确认且 close 站稳 `97-100`；周线 `<78` 重验 | 否（旧 113.38 线已被规则覆盖） | 否（距周线重验约 +17.1%） | `defensive long-term hold / no add`；规模仍高于卫星仓常态 |
| QCOM | 2 | 189.16 | 盘中/收盘 `185` 下方升级观察；completed close `<182` 为失败入场复核 | 否 | 是，距 185 约 +2.25% | `near-stop review / hold-watch only`；不加仓 |

历史模型/观察池（非真实账户 active holdings）：AMD `557.89 > 492`，为 `repair watch / no buy`；若 future completed close 再低于 492，必须转 `reduce-review`。WDC `582.59 > 500`，为 `defensive watch / no buy`；STX `910.34 > 835`，仍为 `near-stop history / no add`，单日反弹不授权追买。DRAM 已由用户确认 `4 @ 62.20` 卖出，不列活跃持仓，也不作同日买回。

## 4. Institutional overlay scorecard

```text
flow_fragility_score: 10/14 -> elevated（proxy-based，接近 acute）
  narrow leadership 1/2；semi/AI 内部分化 1/2；SPY 上行但 VIX 急升的 spot-up-vol-up 2/2；
  systematic/vol-control 1/2；buyback window 1/2；hedging complacency 0/2；thematic crowding 2/2。
trend_aligned_entry_score: 1/5 -> trend_broken
  stress 门控不许可；活跃仓均未满足新一轮 MA/支撑 reclaim；无新确认催化。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium sensitivity；MRVL cyclical supplier+bottleneck / high；
  MXL speculative bottleneck / high；QCOM diversified supplier/edge inference / medium-high。
factor_macro_flags:
  growth_duration_high; volatility_shock; theme_overlap_high; sleeve_correlation_high;
  AI_capex_cycle_high; semiconductor_internal_dispersion; long_term_bottom_unconfirmed.
bottleneck_watch:
  storage（WDC/STX 强于盘面）与 optical/interconnect 均仍是高敏感共同因子；不是新增仓理由。
action impact:
  禁止新买入与摊低；先以共同因子审计组合，再等待同日 VIX3M、完整日线和至少两次 completed-close 的底部确认。
```

组合级相关风险复核已执行：GLW、MRVL、MXL 与 QCOM 名义为四只股票、两类子标签，但有效暴露仍为一个 AI-capex/半导体共同因子。股票敞口 `37.47%` 低于 stress 的 55% 总敞口上限，却没有形成第二低相关主题；MRVL `15.70%` 略高于常规 15% 单名上限，MXL `9.12%` 亦高于高风险卫星常态。因此不以单股 WDC/STX 上涨或 SPY 小幅上涨解释为整体风险恢复。

## 5. 真实账户工作估值与模型组合核对

真实账户工作估值前提：沿用 7 月 10 日已确认 DRAM 卖出后的现金 `USD 3,756.49`，不假设任何新增成交；费用、FX 与结算待券商回报。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 190.89 | 381.78 | 6.35% | long-term core starter / no add |
| MXL | 6 | 91.30 | 547.80 | 9.12% | oversized satellite / no add |
| MRVL | 4 | 235.81 | 943.24 | 15.70% | core-size ceiling / near-weekly-risk review |
| QCOM | 2 | 189.16 | 378.32 | 6.30% | hold/watch only |

- 股票市值：`USD 2,251.14`
- 工作 NAV：`USD 6,007.63`
- 现金：`USD 3,756.49 / 62.53%`
- 股票敞口：`37.47%`
- 持仓数：`4`；名义主题约 `2`，有效大主题 `1`；最大单股：MRVL `15.70%`

退休/历史模型 replay 固定股数（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401，现金 12,323.96）按本轮收盘的基线 NAV 为 `USD 20,978.24`，其中股票 `USD 8,654.28 / 41.25%`、现金 `58.75%`。这不是当前真实账户，也没有假定 overlay 成交，故 overlay NAV 留空。

## 6. Replay 与记忆处理

- 已向 replay ledger 追加仅限已完成的 `2026-07-10` 收盘行；没有预填未来日期。
- 已更新组合快照、待办、日汇总及 domain summary。
- `decisions.md` 不更新：本轮是单日波动率冲击、数据质量限制与既有长期重分类的执行，不构成稳定规则的新证据。

非投资建议。
