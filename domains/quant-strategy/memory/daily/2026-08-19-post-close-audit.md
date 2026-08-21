# 2026-08-19 美股盘后正式审计

审计完成于 `2026-08-20 23:49 Asia/Shanghai`。当时 8/20 美股常规盘正在交易；因此所有正式价格严格采用本地结构化报价的 `yesterdayClose`，即最近完成的 `2026-08-19` 收盘，不把盘中 `price` 误记为收盘。未登录券商、未提交真实订单，且未虚构订单或成交；真实账户以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 运行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展至持仓、半导体、广度与信用代理。两次均返回非空 `Tencent (Primary)` 结构化 quote objects，故本地工作流可用；其来源顺序为 Tencent -> Yahoo Chart -> Sina，传输层亦有 `node:https -> PowerShell WebClient -> fetch` 回退。随后使用同一本地 Node 客户端请求 Yahoo Chart 6 个月日线，已逐项核对下表权益/ETF 的 8/19 completed bar 与 Tencent `yesterdayClose` 一致。Tencent VIX `21.67` 明显陈旧，且无 VIX3M 对象，未采用；VIX/VIX3M 改用 Cboe 官方 daily-price CSV 的同步收盘。

| 标的 | 8/19 收盘 | 相对 8/18 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 237.27 / 466.42 | +9.85% / -3.71% | Tencent Primary `yesterdayClose` + 本地 Yahoo Chart completed daily bar / 中高 |
| WDC / STX | 462.09 / 832.56 | -6.87% / -7.87% | 同上 / 中高 |
| SPY / QQQ | 769.06 / 716.08 | +0.21% / -0.20% | 同上 / 中高 |
| SMH / SOXX | 560.92 / 519.67 | -1.55% / -2.21% | 同上 / 中高 |
| VIX / VIX3M | 14.89 / 18.57 | -6.00% / -3.63% | Cboe 官方 daily-price CSV / 高 |
| RSP / SPY | 222.07 / 769.06 | +1.04% / +0.21% | Tencent Primary `yesterdayClose` + Yahoo 日线 / 中高 |
| HYG / LQD | 79.71 / 106.57 | +0.23% / +0.69% | 同上 / 中高 |
| IWM / SPY | 301.72 / 769.06 | +0.50% / +0.21% | 同上 / 中高 |

技术与代理复核：SPY 位于 MA20/MA50 `759.77/750.43` 上方，63 日回撤 `-1.13%`；QQQ 位于 `706.78/712.98` 上方，回撤 `-4.03%`。SMH 位于 MA20/MA50 `563.85/590.08` 下方，63 日回撤 `-16.14%`；SOXX 位于 `526.91/560.00` 下方，回撤 `-20.66%`。21 日相对变化为 RSP/SPY `+1.56%`、HYG/LQD `+0.34%`、IWM/SPY `-1.00%`、SMH/QQQ `-4.92%`；后者已达 sharp deterioration，前两项没有触发 `-2.5%` 的广度/信用恶化线。VIX 五日变化 `+2.34%`，VIX/VIX3M=`0.802`，期限结构正常。

当天策略建议、执行清单与盘中复盘：未发现 8/19 新的、由用户或券商确认的策略建议、执行清单、订单、成交或账户变化；最近记录是公开来源/机构研究监控与 7/10 历史计划，均不替代交易事实。

## 市场恐慌门控

正式判定：**elevated 5/14**。低 VIX、正常期限结构和 SPY 趋势限制了系统性风险得分；但 QQQ 刚进入轻度 63 日回撤，SMH/SOXX 的深回撤且跌破 MA20/MA50，以及 SMH/QQQ 21 日 `-4.92%` 的锐化相对弱势，使 normal 门控不再适用。缺失的期权、ETF 流、CTA 与单股隐含相关数据不被计作低风险。

- 风险乘数：**70%**
- 现金底线：**25%**
- 框架新买入上限：**25%**（最大股票敞口 75%）
- 实际 AI-capex 相关新增/摊低上限：**0%**。四项真实持仓仍是一条共同因子 sleeve；GLW/MXL/MRVL 风险复核未闭环，SMH/SOXX 趋势破坏，故 elevated 框架上限并不授权相关加仓。

## Stop-trigger table

| 标的 | 8/19 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 152.46 | completed-week `<166-167` 复核带 | 已触发，低于带至少 8.2% | **reduce-review / defensive hold / no add**；待用户/券商确认风控处置 |
| MXL（真实 6 股） | 66.43 | completed-close `<78` | 已触发，低于线 14.83% | **reduce-review / defensive hold / no add** |
| MRVL（真实 4 股） | 237.27 | completed-week `<223`；利润保护 | 价格暂回带上，但未完成风险复核、仍处半导体趋势破坏环境 | **profit-protection / defensive hold / no add**；禁止因单日反弹自动追高 |
| QCOM（真实 2 股） | 161.91 | 7/27 长期持有覆盖；新增需收复约 182、两次收盘不创新低及 sleeve 容量 | 覆盖有效；新增条件未满足 | long-term hold / no add / thesis review |
| AMD（replay/watch，非真实持仓） | 466.42 | completed-close `<492` | **已触发，低于线 5.20%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 462.09 | `<500` | **已触发，低于线 7.58%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 832.56 | `<835` | **已触发，低于线 0.29%** | **reduce-review / defensive hold / no buy** |

AMD、WDC、STX 只用于 replay/watch；本表不推断真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 6/14 -> medium (proxy-based)`：低 VIX 与健康的 RSP/SPY、HYG/LQD 缓和了系统性压力，但 SMH/SOXX 趋势破坏、SMH/QQQ 锐化走弱、存储同步下跌与既有单 sleeve 持仓维持拥挤/脆弱性。期权期限、0DTE、单股隐含相关、杠杆 ETF 流、买回窗口与 CTA 直接数据均为 `unavailable`，未伪装为低风险。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：仅 Fear Gate 允许有限暴露得分；SMH/SOXX 均低于 MA20/MA50，SMH/QQQ 相对强度恶化，已无可确认的有序回踩或趋势收复。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。没有新的已验证盈利、订单或指引证据，分类不因单日价格变化而升级。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; semiconductor_relative_weakness_sharp; unresolved_GLW_MXL_MRVL_risk_review`。
- `bottleneck_watch`：存储、定制芯片与半导体 ETF 同步走弱；MRVL 的单日反弹不能抵销供给链共同因子风险。8/19 已记录的云/推理/分发机构观点仍只是 replay 线索，不是订单、收入或趋势确认。
- `action impact`：`theme_overlap_high` 与 `sleeve_correlation_high` 已执行组合级相关风险复核：四项真实持仓按一条有效 AI-capex sleeve 管理，不因 MRVL 反弹拆分风险预算；相关新增/摊低维持 **0%**，优先等待已有风险复核闭环与半导体趋势确认。

## 模型组合净值核对

只以既有用户/券商确认的工作现金 USD `3,756.49` 与 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 按本收盘标记；未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,976.40 |
| 工作 NAV | USD 5,732.89 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.53%；USD 1,976.40 / 34.47% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 949.08 / 16.56% |

现金高于 elevated 的 25% 底线；MRVL 高于 normal 15% 单名上限，且当前门控为 elevated，维持 no-add 与风险复核。冻结 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘为 **USD 19,949.82**；overlay NAV 和差额留空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向实际存在的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-19 收盘行，未预填未来日期。单日反弹、单日价格或单日 replay 警报不足以升级为稳定规则，故不更新 `memory/decisions.md`。
