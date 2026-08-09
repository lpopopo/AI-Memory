# 2026-07-16 美股盘后正式审计

运行时间：2026-07-17 Asia/Shanghai；审计对象为 2026-07-16 美股常规交易收盘。未登录券商、未提交订单、未假设成交；真实持仓、现金、费用、FX 与结算均以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 运行 Node Quote Workflow Smoke Test；`StockService.fetchQuotes(['MRVL','AMD','SPY','QQQ','SMH'])` 成功，扩展请求也为全部所需股票/ETF 返回非空、结构化的 `Tencent (Primary)` quote objects。该客户端的传输兜底未使流程失效；不将 Yahoo Chart 先前的 404 误写为本地 workflow 不可用。

| 标的 | 2026-07-16 收盘/可靠收盘报价 | 日变动 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 188.30 | -8.71% | Tencent (Primary)，中等；结构化对象 |
| AMD | 500.94 | -5.33% | Tencent (Primary)，中等；结构化对象 |
| WDC | 466.81 | -9.15% | Tencent (Primary)，中等；结构化对象 |
| STX | 745.49 | -10.00% | Tencent (Primary)，中等；结构化对象 |
| SPY / QQQ | 750.72 / 705.94 | -0.54% / -1.64% | Tencent (Primary)，中等；结构化对象 |
| SMH / SOXX | 568.92 / 530.50 | -3.70% / -4.46% | Tencent (Primary)，中等；SMH 由公开历史收盘表交叉一致 |
| VIX | 16.58 | +5.81% | Stocknear 渲染的 2026-07-16 15:59 ET close，低中等；该值与 Cboe/FRED 已发布的 7 月 15 日 15.67 连续 |
| VIX3M | 18.91（2026-07-15） | n.a. | FRED/Cboe 日频收盘，日期错配；不作为当日同期期限结构结论 |
| RSP / SPY | 215.06 / 750.72 | +0.98% / -0.54% | Tencent (Primary)，中等；等权相对占优 |
| HYG / LQD | 79.80 / 107.50 | -0.01% / -0.07% | Tencent (Primary)，中等；信用代理基本稳定 |
| IWM / SPY | 295.59 / 750.72 | -0.06% / -0.54% | Tencent (Primary)，中等；小盘相对占优 |

数据查询于本审计运行时完成。VIX3M 的 7 月 15 日值来自 FRED/Cboe，故 `VIX/VIX3M = 0.877` 仅为日期错配参考，未计入恐慌分数。公开交叉资料：<https://www.financialcontent.com/quote/NQ%3ASMH/historical>、<https://stocknear.com/index/%5EVIX/history>、<https://fred.stlouisfed.org/series/VXVCLS>。

## Market Fear Gate

| 信号 | 结论 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 16.58，处于 elevated 区间 | 1 |
| 5 日 VIX 变化 | 相对 7 月 10 日 15.03 约 +10.3%，未达 +15% 阈值 | 0 |
| VIX/VIX3M | VIX3M 日期错配，不伪造同期判断 | 0 |
| 半导体风险 | SMH/SOXX 明显弱于 SPY/QQQ，且 AI-capex 名称同步下挫 | 2 |
| 既有半导体回撤/趋势压力 | SMH 自近期高点的深度回撤仍在、当日再跌 | 2 |
| 宽度/信用 | RSP、IWM 相对占优，HYG/LQD 稳定；不加分 | 0 |

**正式保守门控：`elevated 5/14`。** 风险乘数 **70%**，最大总股票敞口 **75%**，现金底线 **25%**，框架新买入上限 **25%**。实际新买入/摊低上限仍为 **0%**：四项确认真实持仓同属 AI-capex/common-factor，趋势入场破坏，且已有风险复核项未解除。

## Stop-trigger table

| 标的 | 收盘 | 既有止损/减仓线 | 触发/near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（2） | 158.39 | 完成周收 `<166-167` 复核；加仓需重回 200-205 并守住 190 | 本周中已低于周线风险带，周线尚未完成 | `defensive hold / weekly-risk review / no add` |
| MXL（6） | 74.40 | 完成周收 `<78` 复核；加仓需 `>97` | 本周中低于风险线 | `reduce-review pending weekly confirmation / no add` |
| MRVL（4） | 188.30 | 完成周收 `<223` 复核；加仓需 250-260 且权重 `<12%` | 本周中显著低于 223，周线尚未完成 | `reduce-review pending weekly confirmation / no add`；事件反弹不得追高 |
| QCOM（2） | 170.61 | 185 观察线；完成收盘 `<182` 为失败入场复核 | **继续触发** `<182` | **`reduce-review`**；下次人工/券商对账先确认持仓，非自动成交 |
| AMD（历史 replay/watch） | 500.94 | 完成收盘 `<492` | 未触发；日内低点 491.80、收盘距线 +1.8%，near-stop | `repair watch / near-stop / no buy`；若后续收盘 `<492`，必须 `reduce-review` |
| WDC（历史 replay/watch） | 466.81 | `<500` | **触发** | `reduce-review`；无真实持仓推定或订单 |
| STX（历史 replay/watch） | 745.49 | `<835` | **触发** | `reduce-review`；无真实持仓推定或订单 |

GLW/MXL/MRVL 旧短线保护建议从未提交，且已被 2026-07-10 长期重分类取代；本表不构成券商订单。AMD、WDC、STX 仅为历史 replay/watch 风险状态，非当前真实账户持仓断言。

## Institutional overlay 与相关风险复核

```text
flow_fragility_score: 6/14 -> medium（proxy-based）
  宽度 1：RSP/IWM 相对占优，非全面窄幅风险；半导体/AI 集中 2：SMH/SOXX 及相关名称同步领跌；
  系统性/vol-control 1：VIX 上升但仍处中低位；杠杆/主题拥挤 2：一篮子 AI-capex 同跌且真实组合为单一有效主题。
  期权、CTA、回购窗与杠杆 ETF 的直接数据缺失，未当作事实。
trend_aligned_entry_score: 1/5 -> trend_broken（仅 fear gate 尚允许有限风险；价格趋势、RS、回撤质量和催化剂均未获价格确认）
AI_quality/capex_cycle: GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high；全数 price rejected。
factor_macro_flags: growth_duration_high; semiconductor_basket_unwind; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; long_term_bottom_unconfirmed
bottleneck_watch: 光互连与存储叙事未获得价格确认；补充订单、客户、利润率和 RS 证据前不提升行动等级。
action impact: 禁止追高、关联加仓和摊低；优先完成 QCOM 与周线风险复核。
```

已执行组合级相关风险复核：GLW、MXL、MRVL、QCOM 虽分属光互连、组件与边缘推理，仍共同暴露于 AI-capex、半导体估值与资金流冲击，按 **一个有效主题** 管理。`theme_overlap_high` 与 `sleeve_correlation_high` 本身已触发本次复核；股票敞口低于 Gate 上限不构成放宽理由。

## 模型组合净值核对

以用户确认的现金基线 USD 3,756.49 和上述收盘报价计算：

| 项目 | 金额 / 比例 |
| --- | ---: |
| GLW 2 / MXL 6 / MRVL 4 / QCOM 2 股票市值 | USD 1,857.60 |
| 工作 NAV | **USD 5,614.09** |
| 现金 / 股票敞口 | USD 3,756.49 / **66.91%**；USD 1,857.60 / **33.09%** |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL USD 753.20 / **13.42%** |

历史 institutional-replay 基线模型按冻结数量 MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401 与现金 USD 12,323.96 复算为 **USD 19,537.62**。没有已验证的自动成交假设，overlay NAV 与差额留空。

## Replay 与记忆边界

已向迁移后的 replay ledger 追加 2026-07-16 完成收盘行，未预填未来日期。单日市场警报与单日 replay 均不构成稳定规则，故 **未更新 `decisions.md`**。未记录或推断任何真实订单、成交或经纪账户动作。
