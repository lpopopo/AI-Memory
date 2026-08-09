# 2026-07-21 美股盘后正式审计

审计运行时间：2026-07-23 01:04–01:15 Asia/Shanghai（2026-07-22 美东盘中）。因此本次只审计最近一个**已经完成**的美股常规交易日 2026-07-21；绝不把 7/22 的盘中价格视为正式收盘。

已按要求读取策略摘要、稳定决策、日汇总、最近盘后/盘中记录、持仓与交易快照、恐慌/集中度/日监控/overlay/AI-cycle/replay 框架，以及 `tools/README.md` 的 Quote Workflow Smoke Test。7/21 没有独立策略建议或执行清单；最近公共来源监控不包含可升级为订单、收入或成交事实的新证据。

## 数据工作流与正式收盘快照

先按 Quote Workflow Smoke Test 运行本地 Node `StockService.fetchQuotes`，请求 MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、VIX、VIX3M、RSP、HYG、LQD、IWM 及实际持仓。2026-07-22 17:03Z 返回了全部股票/ETF 的结构化 `Tencent (Primary)` 对象；由于当时美股 7/22 仍在盘中，以下权益/ETF 使用其 `yesterdayClose` 作为 2026-07-21 的 completed close。工作流可用，未把 Node 的传输兜底或任何单一报错误判为工作流不可用，故无需调用 Python 兜底。

Tencent 的 VIX 对象仍为陈旧的 21.67 且无有效 OHLC，未采用。作为允许的单 ticker sanity check，Google Finance **渲染可见**页面在 2026-07-22 11:47–11:50 GMT-5 显示：VIX 16.76、-0.29（-1.70%），VIX3M 19.56、-0.030（-0.15%）。因此反推 7/21 收盘为 VIX 17.05、VIX3M 19.59；标为 `Google browser-visible snapshot / medium`，不是跳转 HTML 数据。

| 标的 | 2026-07-21 收盘 | 相对 7/20 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 207.96 | +6.68% | Node `Tencent (Primary).yesterdayClose`；中等 |
| AMD | 544.43 | +8.12% | 同上；中等 |
| WDC | 548.39 | +12.51% | 同上；中等 |
| STX | 891.83 | +11.14% | 同上；中等 |
| SPY / QQQ | 748.28 / 708.97 | +0.83% / +1.85% | 同上；中等 |
| SMH / SOXX | 584.08 / 552.69 | +4.52% / +5.45% | 同上；中等 |
| VIX / VIX3M | 17.05 / 19.59 | -8.58% / 同步值可用 | Google browser-visible snapshot 反推；中等 |
| RSP / SPY | 212.76 / 748.28 | +0.16% / +0.83% | Tencent；中等 |
| HYG / LQD | 79.65 / 106.85 | -0.04% / -0.28% | Tencent；中等 |
| IWM / SPY | 296.54 / 748.28 | +1.45% / +0.83% | Tencent；中等 |

限制：权益/ETF 尚无第二个 completed-OHLC 交叉源；VIX/VIX3M为可见页面的前收盘反推。未把它们扩展为期权流、CTA、杠杆 ETF 或 buyback 的事实判断。

## 正式 Market Fear Gate

| 信号 | 判定 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 17.05，`elevated` 区间 | 1 |
| VIX 突升 | 较 7/20 回落 8.58%，不计突升 | 0 |
| VIX/VIX3M | 0.870，正常期限结构 | 0 |
| 半导体相对表现 | SMH/SOXX 强于 SPY，但不是恐慌分 | 0 |
| 已有半导体趋势损伤 | 反弹尚未构成 MA/周线修复确认 | 2 |
| 广度/信用 | RSP 落后 SPY、信用略软，但没有 21 日恶化证据 | 0 |

**正式门控：`normal 3/14`**。框架风险乘数 `100%`、现金底线 `5%`、最大总股票敞口 `95%`、框架新买入上限 `50%`。但实际新增/摊低上限仍为 **0%**：四个确认持仓是一个 AI-capex 共同因子篮子，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 和既有风险复核均未闭环；正常市场门控不能覆盖账户级未解决风险。

## Stop-trigger table

| 标的 | 7/21 收盘 | 既有止损/减仓线 | 触发/near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 162.41 | completed-week `<166–167` 复核；加仓需重回 200–205 并守住 190 | 仍低于 completed-week 复核带 | `defensive hold / completed-week reduce-review / no add` |
| MXL（真实 6 股） | 86.06 | completed-week `<78` 复核；加仓需 `>97` | 未跌破 78，但超常规卫星规模与既有复核未闭环 | `defensive hold / reduce-review / no add` |
| MRVL（真实 4 股） | 207.96 | completed-week `<223` 风险复核；利润保护；加仓仅 `250–260` 且权重 `<12%` | 仍低于 223；反弹不能自动追高 | `defensive hold / completed-week reduce-review / no add` |
| QCOM（真实 2 股） | 173.50 | 185 观察；completed close `<182` 失败入场复核 | **持续触发** `<182` | `reduce-review`；仅由用户/券商回报闭环，不假设成交 |
| AMD（replay/watch） | 544.43 | completed close `<492` | 未触发，距风险线 +10.66% | `repair watch / no buy`；后续收盘 `<492` 必为 `reduce-review` |
| WDC（replay/watch） | 548.39 | `<500` | 未触发，已从此前风险线下方收复 | `defensive hold / repair watch / no buy` |
| STX（replay/watch） | 891.83 | `<835` | 未触发，已从此前风险线下方收复 | `defensive hold / repair watch / no buy` |

WDC/STX 的本次收盘高于风险线，故不虚称本日触发；但它们的历史触发与高相关篮子风险仍保留在 replay/复核状态。MRVL 的反弹也不构成新增仓理由。

## Institutional overlay 与组合级相关风险复核

```text
flow_fragility_score: 5/14 -> medium（proxy-based）
  窄广度 1：RSP +0.16% 落后 SPY +0.83%；
  半导体/AI 集中 2：SMH +4.52%、SOXX +5.45%，显著领先指数；
  systematic/vol-control 1：VIX 回落但此前趋势损伤尚未由 MA/周线确认修复；
  hedging complacency 1：VIX 回落，且直接期权/CTA/杠杆 ETF 数据缺失；其余缺口不强行计分。
trend_aligned_entry_score: 2/5 -> trend_broken
  仅市场门控许可与半导体相对强度改善得分；无已验证 MA reclaim、合格回撤质量或可验证催化剂确认。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high。
  本轮反弹的价格确认仅为 mixed，未升级为 confirmed。
factor_macro_flags:
  growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  semiconductor_rebound_but_unconfirmed; unresolved_risk_review.
bottleneck_watch:
  光互连、CXL/内存池化、存储仍是待验证线索；无 7/21 新订单、收入、毛利或资金流事实。
action impact:
  已完成组合级相关风险复核。将四个真实持仓按一个有效主题管理，阻断相关主题新增/摊低与事件反弹追高；优先等待 QCOM 与 GLW/MXL/MRVL 的人工风险闭环。
```

`theme_overlap_high` 与 `sleeve_correlation_high` 独立触发了组合级复核，即使 `flow_fragility` 仅为 medium；名称分散不等于风险分散，任何后续增减仓都必须先评价整个 AI-capex 篮子的总敞口。

## 组合净值核对

真实账户以用户或券商回报为准。本审计沿用已确认现金基线 USD 3,756.49 与持仓 GLW 2、MXL 6、MRVL 4、QCOM 2，不假设订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 2,020.02 |
| 工作 NAV | **USD 5,776.51** |
| 现金 / 股票敞口 | USD 3,756.49 / **65.03%**；USD 2,020.02 / **34.97%** |
| 持仓数 / 有效主题数 | 4 / 1（AI-capex common factor） |
| 最大单股 | MRVL USD 831.84 / **14.40%** |

历史 institutional-replay 的冻结数量（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401）加现金 USD 12,323.96，按本次收盘复算 baseline model value 为 **USD 20,524.75**。未建立经过验证的 overlay 自动执行假设，overlay NAV 与差额保持空白。

## Replay 与记忆边界

已向 replay ledger 仅追加完成的 2026-07-21 收盘行，未预填未来日期。单日反弹、VIX 回落和一次反推的期限结构均不构成稳定规则，故**不更新 `decisions.md`**。未登录券商、未提交订单、未虚构真实成交；真实账户状态仅以用户或券商回报为准。
