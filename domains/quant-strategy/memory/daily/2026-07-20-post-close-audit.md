# 2026-07-20 美股盘后正式审计

审计运行时间：2026-07-21 23:21 Asia/Shanghai（对应 2026-07-20 美股常规交易已收盘）。本记录仅核对公开行情和工作组合；未登录券商、未提交订单，且不把建议或模型计算写成真实成交。

## 读取与报价工作流

已读取策略摘要、稳定决策、日汇总、最近日内监控、最近组合/交易记录，以及恐慌、集中度、日监控、institutional overlay、AI 质量和 replay 规则与 Quote Workflow Smoke Test。2026-07-20 当天未发现独立的策略建议或执行清单文件；仅有盘中/公共来源监控，且其中没有可提升为交易事实的新高证据。

先按工具 README 运行本地 Node smoke test。`StockService.fetchQuotes` 对 MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、RSP、HYG、LQD、IWM、GLW、MXL、QCOM 返回了结构化 `Tencent (Primary)` 对象，因此本地 quote workflow **可用**；客户端的传输 fallback 无需升级。运行时这些对象已进入 2026-07-21 盘中，故其 `yesterdayClose` 被明确作为 2026-07-20 的已完成收盘，而非将实时 `price` 误记为前一日收盘。

VIX Tencent 对象仍为无可用当日 OHLC/变动细节的陈旧 `21.67`，不采用。作为单 ticker sanity check，Google Finance 渲染页面在 2026-07-21 09:59 GMT-5 可见 VIX `17.48`、`-1.17 (-6.27%)`；据页面可见数值反推 2026-07-20 前一收盘为 `18.65`。此项标为 `Google browser-visible snapshot / medium`，不是把跳转 HTML 当作行情。VIX3M 本地结果为空，未填补、未构造同步期限结构。

## 正式收盘/可靠收盘快照

| 标的 | 2026-07-20 收盘 | 相对 7/17 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 194.94 | +3.32% | Node `Tencent (Primary).yesterdayClose`；中等，完成日 close-like 字段 |
| AMD | 503.57 | +1.58% | 同上；中等 |
| WDC | 487.42 | +2.14% | 同上；中等 |
| STX | 802.45 | +1.88% | 同上；中等 |
| SPY / QQQ | 742.09 / 696.06 | -0.16% / +0.10% | 同上；中等 |
| SMH / SOXX | 558.83 / 524.14 | +0.41% / +0.45% | 同上；中等 |
| VIX | 18.65 | -13.94% vs 7/17 的 21.67 | Google browser-visible snapshot 反推前收；中等 |
| VIX3M | unavailable | n/a | Node 空结果；不计入期限结构 |
| RSP / SPY | 212.42 / 742.09 | -0.45% / -0.16% | Tencent；中等 |
| HYG / LQD | 79.68 / 107.15 | +0.04% / -0.38% | Tencent；中等 |
| IWM / SPY | 292.31 / 742.09 | -0.59% / -0.16% | Tencent；中等 |

限制：股票/ETF 只有本地结构化 completed-close 字段，未得到第二个完成日 OHLC 源；VIX3M 缺失。因此本审计不对期限结构、期权流、CTA 或杠杆 ETF 流作事实性断言。

## Market Fear Gate

| 信号 | 判定 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 18.65，`elevated` 区间 | 1 |
| VIX 突升 | 相对 7/17 回落，不计突升 | 0 |
| VIX/VIX3M | VIX3M 缺失，不计分 | 0 |
| 当日半导体相对表现 | SMH/SOXX 略跑赢 SPY，不加分 | 0 |
| 已有半导体趋势损伤 | 7/17 前的破位/周线风险复核尚未由一次反弹修复 | 2 |
| 广度/信用 | 单日 RSP/IWM 偏弱但未达到 21 日恶化阈值；信用不构成新压力 | 0 |

**正式门控：`normal 3/14`。** 风险乘数 `100%`，现金底线 `5%`，最大总股票敞口 `95%`，框架新买上限 `50%`。这只是框架上限；实际新增/摊低上限仍为 **0%**，因为四个真实持仓仍是一个 AI-capex 共因子篮子，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 与既有风险复核尚未闭环。不得因单日反弹追高。

## Stop-trigger table

| 标的 | 收盘 | 既有风险线 | 触发/near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 162.33 | 完成周收盘 `<166-167` 复核；加仓须重回 200-205 且守住 190 | 上周已低于复核带；本日反弹未恢复周线 | `defensive hold / completed-week reduce-review / no add` |
| MXL（真实 6 股） | 84.48 | 完成周收盘 `<78` 复核；加仓须 `>97` | 本日回到 78 上方，但上周复核与高风险卫星超规模问题未闭环 | `defensive hold / reduce-review / no add` |
| MRVL（真实 4 股） | 194.94 | 完成周收盘 `<223` 风险复核；利润保护；加仓须 250-260 且权重 `<12%` | 仍显著低于 223；无自动追高理由 | `defensive hold / completed-week reduce-review / no add` |
| QCOM（真实 2 股） | 174.05 | 185 观察；完成收盘 `<182` 为失败入场复核 | **持续触发** `<182` | `reduce-review`；先由用户/券商回报确认状态，不假设成交 |
| AMD（replay/watch） | 503.57 | 完成收盘 `<492` | 未触发；仅高于线 2.35%，属 near-stop | `repair watch / near-stop / no buy`；后续收盘 `<492` 必为 `reduce-review` |
| WDC（replay/watch） | 487.42 | `<500` | **触发** | `reduce-review`；不声明真实持仓或订单 |
| STX（replay/watch） | 802.45 | `<835` | **触发** | `reduce-review`；不声明真实持仓或订单 |

## Institutional overlay 与组合相关风险复核

```text
flow_fragility_score: 5/14 -> medium (proxy-based)
  窄广度 1：RSP/IWM 当日相对 SPY 偏弱；半导体/AI 集中 1：持仓仍为同一 AI-capex 链；
  systematic/vol-control 1：此前波动冲击后的去风险尚未由趋势确认修复；
  主题拥挤 2：四个真实持仓和 replay 名称高度共因子。期权、CTA、杠杆 ETF、buyback 的直接数据缺失，均记 0。
trend_aligned_entry_score: 1/5 -> trend_broken
  仅 market fear gate 允许框架风险；20/50 日趋势、相对强度、回撤质量和可验证催化剂均不足。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high。
  一日反弹只把价格确认标为 mixed，未升级为 confirmed。
factor_macro_flags:
  growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  long_term_bottom_unconfirmed; unresolved_risk_review.
bottleneck_watch:
  光互连、CXL/内存池化、存储仍为待验证线索；2026-07-20 监控没有可升级为订单、客户、毛利或资金流事实的新证据。
action impact:
  已执行组合级相关风险复核；把真实四仓按一个有效主题管理，阻断相关主题新买/摊低和事件反弹追高，保留 QCOM、GLW/MXL/MRVL 的人工风险闭环优先级。
```

`flow_fragility` 为 medium，但 `theme_overlap_high` 和 `sleeve_correlation_high` 已独立触发组合级复核：名称分散不等于风险分散，任何减仓/加仓判断必须先比较整个 AI-capex 篮子敞口，而非只看单股权重。

## 工作组合与模型组合净值核对

真实账户以用户或券商回报为准。沿用已确认现金基线 USD 3,756.49 和持仓 GLW 2、MXL 6、MRVL 4、QCOM 2：

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,959.40 |
| 工作 NAV | **USD 5,715.89** |
| 现金 / 股票敞口 | USD 3,756.49 / **65.72%**；USD 1,959.40 / **34.28%** |
| 持仓数 / 有效主题数 | 4 / 1（AI-capex 共因子） |
| 最大单股 | MRVL USD 779.76 / **13.64%** |

历史 institutional-replay 的冻结数量（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401）加现金 USD 12,323.96，按本次收盘复算 baseline model value 为 **USD 19,806.72**。无经验证的自动执行假设，overlay NAV 与差额继续留空。

## Replay 与记忆边界

已向 replay ledger 追加仅有 2026-07-20 已完成收盘的一行；未预填未来日期。单日回升、单日 VIX 变化和单日监控均不构成稳定规则，因此**未更新 `decisions.md`**。真实账户不应据本审计自动下单；状态与成交仅以用户或券商回报为准。
