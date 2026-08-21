# 2026-08-20 美股盘后正式审计

审计完成于 `2026-08-21 08:57 Asia/Shanghai`。8/20 美股常规盘已结束，故使用完成收盘而非盘中价；未登录券商、未提交真实订单，未虚构订单或成交，真实账户以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展至持仓、半导体、广度和信用代理。两次均返回非空 `Tencent (Primary)` structured quote objects：本地 workflow 可用（Tencent -> Yahoo Chart -> Sina；传输回退为 node:https -> PowerShell WebClient -> fetch）。随后以同一 Node 客户端的 Yahoo Chart 6 个月日线核验 8/20 completed bar，权益/ETF 均相符。Tencent VIX 为陈旧 `21.67` 且无 VIX3M，未采用；波动率使用 Cboe 官方 daily-price CSV。

| 标的 | 8/20 收盘 | 相对 8/19 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 251.01 / 469.46 | +5.79% / +0.65% | Tencent Primary `price` + Yahoo completed bar / 中高 |
| WDC / STX | 469.05 / 850.24 | +1.51% / +2.12% | 同上 / 中高 |
| SPY / QQQ | 762.60 / 710.93 | -0.84% / -0.72% | 同上 / 中高 |
| SMH / SOXX | 562.65 / 522.35 | +0.31% / +0.52% | 同上 / 中高 |
| VIX / VIX3M | 16.01 / 19.06 | +7.52% / +2.64% | Cboe 官方 daily-price CSV / 高 |
| RSP / SPY | 220.28 / 762.60 | -0.81% / -0.84% | Tencent Primary + Yahoo 日线 / 中高 |
| HYG / LQD | 79.56 / 106.06 | -0.19% / -0.48% | 同上 / 中高 |
| IWM / SPY | 297.67 / 762.60 | -1.34% / -0.84% | 同上 / 中高 |

技术与代理：按 V9 canonical equity-session calendar，SPY 高于 MA20/MA50 `760.99/750.72`、63 日回撤 `-1.96%`；QQQ 高于 MA20 `707.73`、低于 MA50 `712.94`、回撤 `-4.62%`。SMH 低于 MA20/MA50 `562.98/589.51`、回撤 `-15.89%`；SOXX 低于 `525.47/559.19`、回撤 `-20.25%`。21 日相对变化：RSP/SPY `+1.50%`，HYG/LQD `+0.68%`，IWM/SPY `-0.70%`，SMH/QQQ `-4.89%`，SOXX/QQQ `-6.71%`；半导体弱势仍锐化。VIX 五日 `+9.43%`，VIX/VIX3M=`0.840`，期限结构正常。

已读取当天策略建议、执行清单和盘中复盘：无新的用户或券商确认策略建议、委托、成交或账户变化。8/20 公开来源监控和 7/10 历史计划均不替代交易事实。

## 市场恐慌门控

**elevated 7/14**：使用 `v9_fear_gate.py` 的唯一 canonical completed-close 计算。计分为 VIX level `+1`、QQQ 63 日轻度回撤 `+1`、QQQ 跌破 MA50 `+1`、SMH 63 日深回撤 `+3`、SMH 跌破 MA50 `+1`；VIX 五日变化、期限结构、SPY、IWM/SPY、RSP/SPY 与 HYG/LQD 均 `+0`。SOXX 和 SMH/QQQ 作为组合风险说明，但不重复加入 canonical 分数。期权、ETF 流、CTA、单股隐含相关缺失，不计作低风险。

- 风险乘数 **70%**；现金底线 **25%**；框架新买入上限 **25%**（最大股票敞口 75%）。
- 实际 AI-capex 相关新增/摊低：**0%**。真实四项持仓是一条共同因子 sleeve，GLW/MXL 的已触发复核未闭环，SMH/SOXX 趋势破坏；门控上限不授权相关加仓。

## Stop-trigger table

| 标的 | 8/20 收盘 | 既有风险线 / 条件 | 结果 | 下一步 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 151.45 | completed-week `<166-167` | 已触发，低于带至少 8.7% | **reduce-review / defensive hold / no add**；待用户/券商确认处置 |
| MXL（真实 6 股） | 65.28 | completed-close `<78` | 已触发，低于线 16.31% | **reduce-review / defensive hold / no add** |
| MRVL（真实 4 股） | 251.01 | completed-week `<223`；利润保护 | 在带上，但半导体趋势未修复、单名权重上升 | **profit-protection / defensive hold / no add**；禁止反弹追高 |
| QCOM（真实 2 股） | 160.74 | 7/27 长期持有覆盖；新增需约 182、两次收盘不创新低及 sleeve 容量 | 覆盖有效；新增条件未满足 | long-term hold / no add / thesis review |
| AMD（replay/watch） | 469.46 | `<492` | **已触发，低于线 4.58%** | **reduce-review / no buy** |
| WDC（replay/watch） | 469.05 | `<500` | **已触发，低于线 6.19%** | **reduce-review / no buy** |
| STX（replay/watch） | 850.24 | `<835` | 未触发，但仅高于线 1.83% 且低于 MA20/MA50 | **defensive hold / near-stop review / no buy** |

AMD、WDC、STX 只用于 replay/watch，不推断真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 6/14 -> medium (proxy-based)`：VIX 低于 VIX3M、RSP/SPY 与 HYG/LQD 健康，但半导体深回撤/相对走弱、存储仍在风险线下和单 sleeve 持仓维持脆弱性。0DTE、单股隐含相关、杠杆 ETF 流、买回窗口、CTA 均 `unavailable`。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：仅 Fear Gate 允许有限暴露；SMH/SOXX 均低于 MA20/MA50，半导体相对强度恶化，没有确认的回踩或趋势收复。
- `AI_quality/capex_cycle`：GLW diversified supplier / medium；QCOM diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX cyclical supplier / high；MXL speculative bottleneck / high。没有新增已验证盈利、订单或指引证据。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; semiconductor_relative_weakness_sharp; unresolved_GLW_MXL_risk_review`。
- `bottleneck_watch`：MRVL/WDC/STX 的反弹未修复 SMH/SOXX 趋势或存储风险线；单日反弹不是基本面或新买点证据。
- `action impact`：因 `theme_overlap_high` 和 `sleeve_correlation_high` 已完成组合级复核，四项真实持仓按一个 AI-capex sleeve 管理，相关新增/摊低维持 **0%**。

## 模型组合净值核对

只使用既有用户/券商确认的工作现金 USD `3,756.49` 与 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 按本收盘标记；未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 / 工作 NAV | USD 2,020.10 / USD 5,776.59 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.03%；USD 2,020.10 / 34.97% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 1,004.04 / 17.38% |

现金高于 elevated 的 25% 底线；MRVL 超 normal 15% 单名上限，维持 no-add 与风险复核。冻结 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘为 **USD 20,139.55**；overlay NAV 和差额留空，因没有可验证的执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-20 收盘行，未预填未来日期。单日价格反弹、单日 replay 或单日警报均不足以更新稳定规则，故不更新 `memory/decisions.md`。
