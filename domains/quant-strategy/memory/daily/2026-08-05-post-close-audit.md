# 2026-08-05 美股盘后正式审计

审计完成时间：2026-08-06 21:13 Asia/Shanghai。审计对象为已完成的 2026-08-05 美国常规交易日。未登录券商、未提交订单、未假设任何真实成交；真实账户、现金和成交仅以用户或券商回报为准。

## 收盘数据、来源与质量

按 `tools/README.md` 先执行 Node Quote Workflow Smoke Test，并扩展至风险代理与四个确认持仓。所有权益/ETF 返回非空 `Tencent (Primary)` 结构化对象；其中 `price` 与 Yahoo Chart 的 2026-08-05 completed daily bar 一致。Node Tencent 的 VIX 仍是陈旧 `21.67`，VIX3M 无对象，故未采用；Cboe 官方 daily-price CSV 提供同步 VIX/VIX3M 收盘 `15.81/18.95`。记录时点为 2026-08-06 21:13 Asia/Shanghai（下一交易日开盘前），故权益/ETF `price` 是 8/05 已完成收盘，而不是盘中值。

| 标的 | 8/05 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 211.02 / 482.05 | -3.46% / -7.04% | Tencent Primary + Yahoo Chart completed bar / 中高 |
| WDC / STX | 519.17 / 837.66 | -5.36% / -0.91% | 同上 / 中高 |
| SPY / QQQ | 769.79 / 717.30 | -0.20% / -0.90% | 同上 / 中高 |
| SMH / SOXX | 569.70 / 530.70 | -1.04% / -2.12% | 同上 / 中高 |
| VIX / VIX3M | 15.81 / 18.95 | -4.18% / -2.02% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 219.73 / 769.79 | -0.23% / -0.20% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.52 / 106.74 | -0.04% / -0.02% | 同上 / 中高 |
| IWM / SPY | 299.77 / 769.79 | -0.64% / -0.20% | 同上 / 中高 |

技术与代理复核：SPY 高于 MA20/MA50 `748.41/746.37`，距 63 日高点仅 -0.20%；QQQ 高于 MA20 `700.89`、略高于 MA50 `715.01`，距 63 日高点 -3.87%；SMH 高于 MA20 `567.24` 但仍低于 MA50 `595.81`，距 63 日高点 -14.83%。VIX/VIX3M 为 `0.834`，期限结构正常；VIX 五日变化约 -7.5%。21 日 RSP/SPY、HYG/LQD、IWM/SPY 相对变化分别为 -0.61%、+0.76%、-1.69%，均未达到 -2.5% 的广度或信用恶化阈值。

## 市场恐慌门控

正式判定：**normal 4/14**。SMH 的深度 63 日回撤构成主要扣分；VIX 低于 16、期限结构正常、SPY/QQQ 未出现压力型回撤，广度与信用代理也未触发恶化阈值。风险乘数 **100%**，现金底线 **5%**，框架新买入上限 **50%**（最大总股票敞口 95%）。

这不是买入许可。实际 AI-capex 相关新增/摊低上限仍为 **0%**：四个真实持仓是一条共同因子 sleeve，SMH 未修复 MA50，MXL 风险复核未闭环，且当日半导体/存储下跌不构成确认后的支撑或突破。

## Stop-trigger table

| 标的 | 8/05 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 156.70 | completed-week `<166–167` 复核 | 仍低于复核区 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 67.46 | completed-close `<78` | 已触发，低于线 13.51% | reduce-review / defensive hold / no add；仅待用户或券商回报核对实际处置 |
| MRVL（真实 4 股） | 211.02 | completed-week `<223`；利润保护与长期底部复核 | 仍低于周线复核区；当日下跌不改变长期规则 | defensive hold / completed-week reduce-review / no add；禁止因先前事件反弹追高 |
| QCOM（真实 2 股） | 157.53 | 7/27 长期覆盖；未来加一股仍需约 182 收盘重回、两日不创新低及 sleeve 容量 | 长期覆盖有效；加仓条件不齐 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 482.05 | completed-close `<492` | **已触发**，低于线 2.02% | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 519.17 | `<500` | 未触发，但仅高于线 3.83% | defensive hold / near-stop review / no buy |
| STX（replay/watch，非真实持仓） | 837.66 | `<835` | 未触发，但仅高于线 0.32% | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅为历史 replay/watch，不能据此推断真实持仓、订单或成交。

## Institutional overlay 与组合级相关风险复核

- `flow_fragility_score: 5/14 -> medium（proxy-based）`：RSP/SPY 与 IWM/SPY 的 21 日相对表现偏弱但未达恶化阈值；SMH 五日仍较 QQQ 强约 4.6 个百分点、内部个股却出现高波动下跌。缺少 0DTE、期权偏斜、杠杆 ETF 逐日流量和隐含相关性数据，不强行补分。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许风险，但 SMH 在 MA50 下、AMD/WDC/STX 与持仓均未给出干净的相对强度和支撑回收确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。持仓价格确认均为 rejected 或 mixed，未形成新增依据。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review`。
- `bottleneck_watch`：光互连/定制芯片、存储吞吐仍是同一 AI-capex 链的高敏感环节；没有新的、已验证的收入、毛利、订单或现金流证据来改变分类。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high`，已执行组合级（非单股）复核：GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理。相关新增与摊低维持 `0%`，先等待 MXL 风险闭环、SMH 重新站稳 MA50，以及相对强度确认。

## 模型组合净值核对

以用户确认的工作现金 USD `3,756.49` 和确认持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 计算；不假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,877.30 |
| 工作 NAV | USD 5,633.79 |
| 现金 / 股票敞口 | USD 3,756.49 / 66.68%；USD 1,877.30 / 33.32% |
| 持仓数量 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 844.08 / 14.98% |

现金高于 normal 的 5% 底线；MRVL 已回到正常 15% 单名上限以内，但仍不授权加仓。冻结 institutional-replay baseline 按既有静态持仓标记为 **USD 20,032.78**；overlay NAV 与差额继续留空，因为没有可验证的 overlay 执行假设。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一行 2026-08-05 完成收盘；未预填未来日期。单日下跌、单日 replay 或流动性警报不构成稳定规则，`memory/decisions.md` 未更新。
