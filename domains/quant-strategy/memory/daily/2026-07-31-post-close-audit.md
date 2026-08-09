# 2026-07-31 美股盘后正式审计

审计运行于 2026-08-01 Asia/Shanghai（周六）；审计对象为已完成的 2026-07-31 美股常规交易日。未登录券商、未提交订单，未假设任何真实成交；真实账户、现金和订单状态仍以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展到 WDC、STX、SOXX、RSP、HYG、LQD、IWM 与四个确认持仓。两次调用均返回非空 `source: Tencent (Primary)` 结构化对象，故本地 workflow 可用，未需要 Python 兜底；Yahoo Chart `1d` completed bars 与权益/ETF 的 Node `price` 逐项相符。周六运行时该 `price` 是最近完成的 7/31 收盘，`yesterdayClose` 则是 7/30，未混用。

本地 VIX 对象仍为陈旧的 `21.67` 且 OHLC 为零，VIX3M 无对象，不能作为 7/31 收盘。渲染可见的 Google Finance 卡片在 7/31 15:15:01 GMT-5 显示 VIX `15.99`（`-1.10`, `-6.44%`）与 VIX3M `19.02`（`-0.48`, `-2.46%`）；记为 `Google browser-visible snapshot`，质量为中等，而非跳转 HTML。

| 标的 | 7/31 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 187.56 / 476.15 | +2.32% / -1.90% | Tencent Primary + Yahoo Chart completed-bar cross-check / 中高 |
| WDC / STX | 544.84 / 856.13 | +2.21% / +0.52% | 同上 |
| SPY / QQQ | 747.03 / 687.99 | +0.72% / +0.65% | 同上 |
| SMH / SOXX | 540.53 / 504.89 | +0.30% / +0.07% | 同上 |
| VIX / VIX3M | 15.99 / 19.02 | -6.44% / -2.46% | Google browser-visible snapshot / 中等 |
| RSP / SPY | 215.01 / 747.03 | -0.17% / +0.72% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.48 / 106.25 | +0.01% / -0.15% | Tencent Primary + Yahoo Chart / 中高 |
| IWM / SPY | 291.20 / 747.03 | -0.48% / +0.72% | Tencent Primary + Yahoo Chart / 中高 |

日线校验：SPY 距 63 日高点 `-1.65%`，QQQ `-7.80%`、SMH `-19.19%`；QQQ/SMH 均低于 MA20/MA50（`687.99/701.02/715.09`，`540.53/571.63/596.17`）。21 日相对变化为 RSP/SPY `+0.58%`、HYG/LQD `+1.94%`、IWM/SPY `-2.88%`。VIX/VIX3M 为 `0.841`，正向期限结构。

## 市场恐慌门控

正式判定：**normal 4/14**。VIX 低于 16、五日变化 `-13.94%`、期限结构正常、SPY 63 日回撤很浅，均不产生波动率/信用压力分；QQQ 温和回撤、SMH 深度回撤及 IWM/SPY 21 日相对走弱合计保留 4 分。风险乘数 **100%**，现金底线 **5%**，框架新买入上限 **50%**（最大总股票敞口 95%）。

这只是市场级门控，不是买入许可。实际相关新增/摊低上限仍为 **0%**：四个确认持仓是一个 AI-capex / semiconductor common-factor sleeve，`theme_overlap_high` 与 `sleeve_correlation_high` 持续，且 QQQ、SMH 和四个持仓均无趋势修复确认。

## Stop-trigger table

| 标的 | 7/31 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 138.25 | 长期重分类；completed-week `<166–167` 复核 | 复核持续；旧 stop 仅 planning-only | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 66.82 | completed-close `<78` | 已触发，低于线 14.33% | reduce-review / defensive hold / no add；待用户或券商回报核对实际处置 |
| MRVL（真实 4 股） | 187.56 | completed-week `<223`；利润保护和长期底部复核 | 复核持续；反弹不构成追高条件 | defensive hold / completed-week reduce-review / no add |
| QCOM（真实 2 股） | 147.61 | 7/27 长期覆盖；仅在两次不创新低、完成收盘重回约 182 等条件满足后评估加一股 | 覆盖理由有效；恢复条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 476.15 | completed-close `<492` | **已触发**，低于线 3.22% | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 544.84 | `<500` | 未触发；高于线 8.97%，仍作周期性防御复核 | defensive hold / risk-line review / no buy |
| STX（replay/watch，非真实持仓） | 856.13 | `<835` | 未触发；高于线 2.53%，near-stop | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅是历史 replay/watch，未被推断为真实持仓或订单。GLW/MXL/MRVL 的历史短线止损建议均未提交，且已由长期重分类取代。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：RSP/IWM 当日弱于 SPY（窄/混合参与度，1），半导体处于高波动且低于中期均线的修复失败区（1），VIX 单日大幅回落后的系统仓位转换风险（1），低 VIX 下的对冲自满仅作弱代理（1）。0DTE、偏斜、杠杆 ETF 流、回购窗口和隐含相关性无直接数据，不强行计分。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许风险敞口（1），但 QQQ/SMH 及现有持仓未站回关键短中期趋势，RS、回撤质量和可验证催化均不合格（其余 0）。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review`。
- `bottleneck_watch`：光互连、定制芯片和存储仍是同一 AI-capex 链的高敏感环节；本轮没有独立验证的订单、收入、毛利或资金流新证据。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high`，已完成组合级而非逐股的相关风险复核；GLW/MXL/MRVL/QCOM 作为一个有效 sleeve 管理。维持相关新增和摊低 `0%`，优先等待 MXL 风险闭环与趋势确认，不能用单日 VIX 回落解除约束。

## 组合净值核对

沿用用户确认的现金 USD `3,756.49`、持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2`；未假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,722.88 |
| 工作 NAV | USD 5,479.37 |
| 现金 / 股票敞口 | USD 3,756.49 / 68.56%；USD 1,722.88 / 31.44% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 750.24 / 13.69% |

现金高于 normal 5% 底线，最大单股低于普通 15% 上限；二者都不构成加仓授权。冻结的 institutional-replay baseline（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401、现金 USD 12,323.96）按本收盘复算为 **USD 19,953.05**；没有可验证的 overlay 执行假设，因此 overlay NAV 与差额留空。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一个已完成的 2026-07-31 close 行，没有预填未来日期。单日波动率回落、单日反弹或单日 replay 均未升级为稳定规则，`memory/decisions.md` 不更新。
