# 2026-07-17 美股盘后正式审计

审计运行时间：2026-07-18 09:18 Asia/Shanghai（美股 2026-07-17 常规交易已收盘）。本记录只做公开行情与工作组合复核；不登录券商、不提交订单，也不把建议或模型计算写成真实成交。

## 读取与行情工作流

已先读取策略摘要、稳定决策、日汇总、最近审计/组合/待办、近期真实成交与盘中执行记录、恐慌/集中度/日监控/机构 overlay/AI 质量/回放协议，以及 `tools/README.md` 的 Quote Workflow Smoke Test。

先运行本地 Node smoke test：`StockService.fetchQuotes` 请求 MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、VIX、RSP、HYG、LQD、IWM 及真实持仓。返回了结构化对象，全部可用报价的 `source` 为 `Tencent (Primary)`；因此本地 workflow **可用**。运行发生在 2026-07-18 09:18 +08:00，股票/ETF 对象含 7 月 17 日 OHLC/成交量，按收盘后可靠 close-like snapshot 使用，质量为中等。`VIX3M` 未返回对象；不填补、不伪造同步期限结构。

## 正式收盘/可靠收盘快照

| 标的 | 2026-07-17 收盘/快照 | 日变动 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 188.68 | +0.20% | Tencent (Primary) 结构化对象；中等 |
| AMD | 495.76 | -1.03% | Tencent (Primary) 结构化对象；中等 |
| WDC | 477.22 | +2.23% | Tencent (Primary) 结构化对象；中等 |
| STX | 787.66 | +5.66% | Tencent (Primary) 结构化对象；中等 |
| SPY / QQQ | 743.29 / 695.33 | -0.99% / -1.50% | Tencent (Primary)；中等 |
| SMH / SOXX | 556.53 / 521.81 | -2.18% / -1.64% | Tencent (Primary)；中等 |
| VIX | 21.67 | 传输对象显示 0.00% | Tencent (Primary)；低至中等：有结构化值但未给可用当日 OHLC/变动，以下仅将水平及相对 7/16 已核对的 16.58 的跃升作保守风险信号 |
| VIX3M | unavailable | n/a | 本次 Node 结果未返回；不作为同步期限结构或分数输入 |
| RSP / SPY | 213.37 / 743.29 | -0.79% / -0.99% | Tencent (Primary)；中等；等权相对抗跌 |
| HYG / LQD | 79.65 / 107.56 | -0.19% / +0.06% | Tencent (Primary)；中等；信用代理轻微走弱 |
| IWM / SPY | 294.04 / 743.29 | -0.52% / -0.99% | Tencent (Primary)；中等；小盘相对抗跌 |

数据限制：没有 VIX3M 同步读数，也没有独立完成日线交叉源；不能据此声称完整的期限结构、期权流或 CTA 事实。VIX 从前日已核对的 16.58 到本次 21.67 约升 30.7%，虽需等待独立数据复核，仍按风险优先原则计作保守压力信号。

## Market Fear Gate

| 信号 | 判断 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 21.67，处于 elevated 区间 | 1 |
| VIX 突升 | 相对 7/16 的 16.58 约 +30.7%，按 stress-spike 保守计分 | 2 |
| VIX/VIX3M | VIX3M 缺失，不计分 | 0 |
| 半导体风险 | SMH/SOXX 分别落后 SPY 约 1.19/0.65 个百分点，AI-capex 同步承压 | 2 |
| 既有半导体趋势压力 | SMH 再跌，AMD/MRVL/MXL 弱势且 WDC/STX 虽反弹仍未收复既有风险线 | 2 |
| 宽度/信用 | RSP、IWM 相对抗跌；HYG/LQD 仅轻微转弱，不加分 | 0 |

**正式保守门控：`elevated 7/14`。** 风险乘数 **70%**；最大总股票敞口 **75%**；现金底线 **25%**；框架新买入上限 **25%**。实际新增买入/摊低上限仍为 **0%**：四个确认持仓是同一 AI-capex/common-factor，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high`，并且 QCOM 与本周完成后的 GLW/MXL/MRVL 都处于风险复核状态。

## Stop-trigger table

| 标的 | 收盘 | 既有止损/减仓线 | 触发/near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 154.61 | 完成周收盘 `<166-167` 风险复核；加仓需重回 200-205 并守住 190 | 周线已完成且低于风险带 | `defensive hold / completed-week reduce-review / no add`；旧短线 stop 未提交且已被长线重分类取代，不自动假设卖出 |
| MXL（真实 6 股） | 71.84 | 完成周收盘 `<78` 风险复核；加仓需 `>97` | 周线已完成且低于线 | `reduce-review / no add`；维持高风险卫星超规模复核 |
| MRVL（真实 4 股） | 188.68 | 完成周收盘 `<223` 风险复核；既有利润保护/风险复核；加仓需 250-260 且权重 `<12%` | 周线已完成且显著低于 223 | `reduce-review / no add`；不得因 CXL/事件叙事或反弹追高 |
| QCOM（真实 2 股） | 171.78 | 185 观察线；完成收盘 `<182` 为失败入场复核 | **持续触发** `<182` | **`reduce-review`**；下次人工/券商对账先确认仍持有，未假设成交 |
| AMD（历史 replay/watch） | 495.76 | 完成收盘 `<492` | 未触发；仅高于线约 0.76%，盘中低点 460.21 | `repair watch / near-stop / no buy`；后续收盘 `<492` 必须 `reduce-review` |
| WDC（历史 replay/watch） | 477.22 | `<500` | **触发**，虽当日反弹但未收复 | `reduce-review`；非真实账户持仓或订单断言 |
| STX（历史 replay/watch） | 787.66 | `<835` | **触发**，虽当日反弹但未收复 | `reduce-review`；非真实账户持仓或订单断言 |

## Institutional overlay 与组合相关风险复核

```text
flow_fragility_score: 6/14 -> medium (proxy-based)
  领导广度 1：RSP/IWM 相对抗跌，非全面窄幅风险；
  半导体/AI 同步脆弱性 2：SMH/SOXX 明显落后且持仓相关名称弱；
  系统性/vol-control 1：VIX 跃升提示去风险，但无直接仓位数据；
  主题拥挤 2：同一 AI-capex 叙事与价格同步受压；期权、buyback、杠杆 ETF 直接数据缺失而记 0。
trend_aligned_entry_score: 1/5 -> trend_broken
  仅 fear gate 尚未完全禁止风险；价格趋势、RS、回撤质量、催化剂价格确认均未满足。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high；全部为 price rejected。
factor_macro_flags:
  growth_duration_high; volatility_shock; semiconductor_basket_unwind; theme_overlap_high;
  sleeve_correlation_high; AI_capex_cycle_high; long_term_bottom_unconfirmed; unresolved_risk_review.
bottleneck_watch:
  CXL/内存池化、存储与光互连仍只属待验证线索；本次没有可提升为订单、客户、毛利或资金流事实的新独立证据。
action impact:
  禁止追高、关联加仓和摊低；把四个真实持仓按一个有效 AI-capex 风险篮子管理，优先完成 QCOM 和已完成周线的 GLW/MXL/MRVL 人工风险复核。
```

已执行组合级相关风险复核：GLW、MXL、MRVL、QCOM 虽位于光互连、组件和边缘推理，仍共同暴露于 AI-capex、半导体估值和流动性冲击，故按 **1 个有效主题** 管理。`theme_overlap_high` 与 `sleeve_correlation_high` 本身已足以触发此复核；低股票敞口不构成放宽相关新买入的理由。

## 工作组合净值核对

以用户确认现金基线 USD 3,756.49 和本次收盘快照计算：

| 项目 | 金额 / 比例 |
| --- | ---: |
| GLW 2 / MXL 6 / MRVL 4 / QCOM 2 股票市值 | USD 1,838.54 |
| 工作 NAV | **USD 5,595.03** |
| 现金 / 股票敞口 | USD 3,756.49 / **67.14%**；USD 1,838.54 / **32.86%** |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL USD 754.72 / **13.49%** |

历史 institutional-replay 冻结数量（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401）及现金 USD 12,323.96 复算的 baseline model value 为 **USD 19,649.66**。没有经验证的自动成交假设，overlay NAV 与差额保持空白。

## Replay 与记忆边界

已向迁移后的 replay ledger 追加 2026-07-17 完成收盘行；未预填未来日期。单日市场警报、单日 CXL 社媒线索或单日 replay 均不构成稳定规则，因此 **未更新 `decisions.md`**。真实账户以用户/券商回报为准；本审计不记录或推断任何新订单、成交或经纪账户操作。
