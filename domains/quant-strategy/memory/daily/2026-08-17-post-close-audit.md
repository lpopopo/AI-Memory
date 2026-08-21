# 2026-08-17 美股盘后正式审计

审计完成于 `2026-08-18 22:55 Asia/Shanghai`。运行时美股 8/18 常规盘正在交易，因此本报告严格采用本地结构化行情的 `yesterdayClose` 作为最近已完成的 `2026-08-17` 收盘；不把当日盘中 `price` 写作正式收盘。未登录券商、未提交真实订单、未虚构成交；真实账户状态以用户或券商回报为准。

## 收盘数据、来源与质量

先依照 `tools/README.md` 完成 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展到持仓、半导体、广度及信用代理。两次调用均返回非空 `Tencent (Primary)` 结构化 quote objects；本地 workflow 可用，含 Tencent -> Yahoo Chart -> Sina 的来源回退以及 node:https -> PowerShell WebClient -> fetch 的传输回退。腾讯 VIX 为陈旧 `21.67`，VIX3M 无对象，未采用；同步的 VIX/VIX3M 改用 Cboe 官方 daily-price 表。Yahoo 6 个月日线本次最后可见的完成 bar 是 8/14、随后为 8/18 盘中 bar，未提供可日期匹配的 8/17 bar，因此不虚构该交叉核对；权益/ETF 收盘质量相应记为中等，而非中高。

| 标的 | 8/17 收盘 | 相对 8/14 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 234.33 / 506.00 | +5.54% / -1.63% | Tencent Primary `yesterdayClose` / 中等 |
| WDC / STX | 536.01 / 994.79 | +5.35% / +2.19% | 同上 / 中等 |
| SPY / QQQ | 772.67 / 729.87 | -0.47% / -0.16% | 同上 / 中等 |
| SMH / SOXX | 594.07 / 559.12 | +1.06% / +1.58% | 同上 / 中等 |
| VIX / VIX3M | 15.19 / 19.04 | +6.60% / +3.14% | Cboe 官方 daily-price CSV / 高 |
| RSP / SPY | 220.79 / 772.67 | -0.89% / -0.47% | Tencent Primary `yesterdayClose` / 中等 |
| HYG / LQD | 79.61 / 105.70 | -0.13% / -0.40% | 同上 / 中等 |
| IWM / SPY | 304.06 / 772.67 | -0.34% / -0.47% | 同上 / 中等 |

技术及代理复核（以 Tencent 8/17 收盘接入 Yahoo 至 8/14 的完成历史计算）：SPY 在 MA20/MA50 `757.73/749.24` 上方、63 日回撤 `-0.67%`；QQQ 在 `705.82/712.74` 上方、回撤 `-2.18%`。SMH 在 `565.87/590.82` 上方、但仍距 63 日高 `-11.19%`；SOXX 仍略低于 MA50 `561.20`，距高 `-14.64%`。21 日相对变化为 RSP/SPY `-0.25%`、HYG/LQD `+1.46%`、IWM/SPY `-0.06%`、SMH/QQQ `+1.00%`，无广度或信用的 `-2.5%` 恶化触发。VIX 五日 `-1.75%`、VIX/VIX3M=`0.798`，期限结构正常。

当天策略建议、执行清单与盘中复盘：最近可读的盘中执行清单停留在 7/10，8/14 公开来源监控不包含任何用户或券商确认的订单/成交；本次未发现 8/17 或 8/18 新增的已确认策略建议、执行或盘中账户事实，故不推断交易。

## 市场恐慌门控

正式判定：**normal 3/14**。低 VIX、五日未扩张、正常期限结构、SPY/QQQ 趋势以及广度/信用代理健康；扣分仅来自半导体仍有 `-11%/-15%` 的 63 日回撤及 SOXX 未收复 MA50。分数为半导体回撤 `2` 加 SOXX 趋势 `1`；不将缺失的期权、ETF 流量或 CTA 数据强行记作零风险。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**
- 实际 AI-capex 相关新增/摊低上限：**0%**。真实四持仓仍是一条共同因子 sleeve，8/14 完成周收盘已触发 GLW/MRVL 的周度复核，MXL 的既有止损复核未闭环；单日修复不授权相关加仓。

## Stop-trigger table

| 标的 | 8/17 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 173.21 | completed-week `<166-167` 复核带 | 8/14 完成周收盘 `165.99` 已跌破；8/17 反弹不撤销复核 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 84.76 | completed-close `<78` | 8/13 的既有触发已修复至线上，但未闭环 | defensive hold / post-breach reduce-review / no add |
| MRVL（真实 4 股） | 234.33 | completed-week `<223`；利润保护 | 8/14 完成周收盘 `222.02` 已跌破；8/17 反弹不能自动解除或追高 | defensive hold / completed-week reduce-review / no add |
| QCOM（真实 2 股） | 162.18 | 7/27 长期持有覆盖；新增需收复约 182、两次收盘不创新低及 sleeve 容量 | 覆盖有效；新增条件未满足 | long-term hold / no add / thesis review |
| AMD（replay/watch，非真实持仓） | 506.00 | completed-close `<492` | 在线上 2.85%，此前触发后的修复未确认 | repair watch / no buy |
| WDC（replay/watch，非真实持仓） | 536.01 | `<500` | 在线上 7.20%，不是 near-stop；高回撤后的反弹未确认 | defensive recovery review / no buy |
| STX（replay/watch，非真实持仓） | 994.79 | `<835` | 在线上 19.14%，不是 near-stop；高波动修复 | defensive recovery review / no buy |

AMD、WDC、STX 仅用于 replay/watch，不推断为真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：SPY/QQQ 贴近高位、但半导体仍有深回撤且 SOXX 未收复 MA50；VIX 温和、广度/信用未恶化。期权期限、单股隐含相关性、杠杆 ETF 流、买回窗口及 CTA 直接数据为 `unavailable`，未伪装为低风险。
- `trend_aligned_entry_score: 2/5 -> trend_broken`：Fear Gate 允许暴露和 SMH 相对 QQQ 的短期改善各得一分；SMH 的 MA50 收复仅一日、SOXX 仍未确认、无可验证催化剂/有序回踩确认，故不形成新增条件。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。8/17 反弹不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_repair_unconfirmed; unresolved_GLW_MXL_MRVL_risk_review`。
- `bottleneck_watch`：光互连、定制芯片及存储同步修复，但均未完成趋势重建；不把高 beta 反弹当作需求或盈利质量确认。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high`，已执行组合级相关风险复核；GLW/MXL/MRVL/QCOM 按一条有效 sleeve 管理。无论 normal 门控，相关新增/摊低维持 **0%**，直到周度/止损复核闭环及半导体相对强弱稳定。

## 模型组合净值核对

仅用用户/券商既有确认的工作现金 USD `3,756.49` 与 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 按本收盘标记；未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 2,116.66 |
| 工作 NAV | USD 5,873.15 |
| 现金 / 股票敞口 | USD 3,756.49 / 63.96%；USD 2,116.66 / 36.04% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 937.32 / 15.96% |

现金高于 normal 5% 底线；MRVL 高于 normal 15% 单名上限，故维持 no-add 与周度复核。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘为 **USD 20,744.61**；overlay NAV 与差额为空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-17 收盘行，未预填任何未来日期。此为单次日度审计及 experimental replay，不更新 `memory/decisions.md`。
