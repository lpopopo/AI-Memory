# 2026-08-10 美股盘后正式审计

审计完成于 2026-08-11 22:42 Asia/Shanghai（美东 10:42，8/11 常规盘中）。因此本审计严格使用本地报价对象的 `yesterdayClose` 作为 2026-08-10 已完成常规交易收盘；不将 8/11 盘中 `price` 当作收盘。本记录不登录券商、不提交订单、不虚构成交；真实账户、现金和委托以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test，并扩展至风险代理和已确认持仓。`Tencent (Primary)` 返回非空结构化 quote objects；其内部失败链为 Tencent -> Yahoo Chart -> Sina，且 Node 具有 `node:https -> PowerShell WebClient -> fetch` 传输兜底。随后通过同一本地 Node 客户端的 Yahoo Chart 日线端点核验 8/10 历史 bar。Tencent 的 VIX 为陈旧 `21.67`、没有 VIX3M 对象，未采用；改用 Cboe 官方 daily-price CSV。

| 标的 | 8/10 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 208.56 / 469.56 | -4.65% / -2.86% | Tencent Primary `yesterdayClose` + 本地 Yahoo Chart 完成日线核验 / 中高 |
| WDC / STX | 438.34 / 800.99 | +0.93% / -1.45% | 同上 / 中高 |
| SPY / QQQ | 773.03 / 720.87 | -0.03% / -0.30% | 同上 / 中高 |
| SMH / SOXX | 569.41 / 529.39 | -2.28% / -2.55% | 同上 / 中高 |
| VIX / VIX3M | 15.46 / 18.98 | +3.76% / +1.39% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 220.22 / 773.03 | +0.06% / -0.03% | Tencent Primary `yesterdayClose` + Yahoo 日线 / 中高 |
| HYG / LQD | 79.48 / 105.96 | -0.16% / -0.55% | 同上 / 中高 |
| IWM / SPY | 299.98 / 773.03 | -0.52% / -0.03% | 同上 / 中高 |

技术与代理复核：SPY 在 MA20/MA50 `751.37/747.56` 上方，距 63 日高点 `-0.03%`；QQQ 在 `700.80/714.27` 上方，距 63 日高点 `-3.39%`。SMH 虽在 MA20 `563.20` 上方但低于 MA50 `594.33`，距 63 日高点 `-14.87%`，且 21 日相对 QQQ 为 `-6.17%`。VIX 五日从 `15.86` 降至 `15.46`（`-2.52%`），VIX/VIX3M 为 `0.815`，期限结构正常。21 日 RSP/SPY、HYG/LQD、IWM/SPY 的相对变化约为 `+0.37%/+1.11%/-1.04%`，均未触发 -2.5% 的广度/信用恶化阈值。

当天不存在独立的 8/10 策略建议、执行清单或盘中复盘文件；已阅读的 8/10 公共来源监控只提供研究线索，明确不构成交易、订单、收入或价格确认。既有执行清单也不构成新的订单或成交事实。

## 市场恐慌门控

正式判定：**normal 4/14**。低位且正常期限结构的 VIX、SPY/QQQ 的趋势与未触发的广度/信用代理支持 normal；SMH 的深度回撤、低于 MA50 和相对弱势保留风险扣分。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（最大股票敞口 95%）
- 实际 AI-capex 相关新增/摊低上限：**0%**。四项真实持仓仍是一只有效的 AI-capex/common-factor sleeve；SMH 未修复 MA50，且 GLW/MXL/MRVL 风险复核未闭环。

## Stop-trigger table

| 标的 | 8/10 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 157.76 | completed-week `<166-167` 复核带 | 低于复核带；周内不能伪造周收盘 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 68.44 | completed-close `<78` | 已触发，低于线 12.26% | reduce-review / defensive hold / no add |
| MRVL（真实 4 股） | 208.56 | completed-week `<223`；利润保护与长期底部复核 | 低于线 6.48%；周内仅作风险复核 | defensive hold / completed-week reduce-review / no add；禁止因事件或反弹追高 |
| QCOM（真实 2 股） | 162.17 | 7/27 长期覆盖；未来加仓需收复约 182、两次收盘不创新低及 sleeve 容量 | 长期覆盖有效；加仓条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 469.56 | completed-close `<492` | **已触发，低于线 4.56%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 438.34 | `<500` | **已触发，低于线 12.33%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 800.99 | `<835` | **已触发，低于线 4.07%** | **reduce-review / no buy** |

AMD、WDC、STX 仅是 replay/watch，不能据此推断真实持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 5/14 -> medium (proxy-based)`：市场广度/信用代理健康，但 SMH/SOXX 与存储链相对弱势，已有主题集中；当日期权、0DTE、杠杆 ETF 流量和隐含相关性不可用，未强行计分。8/10 监控中的零售防御转移是来源特定、非价格确认的观察。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许敞口，但 SMH 低于 MA50，MRVL/GLW/MXL/QCOM 与存储链均未显示可验证的相对强度或收复确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。单日价格不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连、定制芯片和存储仍暴露同一 AI-capex 链；WDC/STX 的回撤和 SMH 相对弱势未提供链条修复证据。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high`，已完成组合级而非单股孤立复核。GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理；在 MXL 风险未闭环、SMH 未重回 MA50 且相对强度未确认前，相关新增/摊低保持 **0%**。

## 模型组合净值核对

按用户确认的工作现金 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 标记；未假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,884.74 |
| 工作 NAV | USD 5,641.23 |
| 现金 / 股票敞口 | USD 3,756.49 / 66.59%；USD 1,884.74 / 33.41% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 834.24 / 14.79% |

现金高于 normal 的 5% 底线；MRVL 已回到 normal 15% 单名上限内，但不构成加仓授权。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘标记为 **USD 19,575.20**；overlay NAV 与差额留空，因为不存在可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向实际存在的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条 2026-08-10 已完成收盘行；旧提示中的 `experiments/...` 路径在仓库中不存在。没有预填未来日期。单日下跌、单日 replay 或单日警报均不足以提升为稳定规则，故 **不更新 `memory/decisions.md`**。

