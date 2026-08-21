# 2026-08-18 美股盘后正式审计

审计完成于 `2026-08-19 22:31 Asia/Shanghai`。运行时美股 8/19 常规盘正在交易，因此严格使用本地结构化行情的 `yesterdayClose` 作为最近已完成的 `2026-08-18` 收盘；不将当日盘中 `price` 写作正式收盘。未登录券商、未提交真实订单、未虚构成交；真实账户状态以用户或券商回报为准。

## 收盘数据、来源与质量

已先按 `tools/README.md` 完成 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展到持仓、半导体、广度及信用代理。两次均返回非空 `Tencent (Primary)` 结构化 quote objects，故本地 workflow 可用；其链路为 Tencent -> Yahoo Chart -> Sina，并含 node:https -> PowerShell WebClient -> fetch 传输回退。以本地 Node 请求 Yahoo Chart 的 6 个月 completed daily bars 交叉核验，权益及 ETF 的 8/18 收盘一致。腾讯 VIX 仍为陈旧 `21.67`、VIX3M 无对象，未采用；VIX/VIX3M 改取 Cboe 官方 daily-price CSV 的同步值。

| 标的 | 8/18 收盘 | 相对 8/17 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 216.00 / 484.39 | -7.82% / -4.27% | Tencent Primary `yesterdayClose`，本地 Yahoo Chart 日线交叉核验 / 中高 |
| WDC / STX | 496.16 / 903.68 | -7.43% / -9.16% | 同上 / 中高 |
| SPY / QQQ | 767.45 / 717.51 | -0.68% / -1.69% | 同上 / 中高 |
| SMH / SOXX | 569.77 / 531.39 | -4.09% / -4.96% | 同上 / 中高 |
| VIX / VIX3M | 15.84 / 19.27 | +4.28% / +1.21% | Cboe 官方 daily-price CSV / 高 |
| RSP / SPY | 219.79 / 767.45 | -0.45% / -0.68% | Tencent Primary `yesterdayClose`，Yahoo 日线核验 / 中高 |
| HYG / LQD | 79.53 / 105.84 | -0.10% / +0.13% | 同上 / 中高 |
| IWM / SPY | 300.23 / 767.45 | -1.26% / -0.68% | 同上 / 中高 |

技术及代理复核：SPY 在 MA20/MA50 `758.68/749.53` 上方，63 日回撤 `-1.34%`；QQQ 在 `706.24/712.84` 上方，回撤 `-3.73%`。SMH 在 MA20 `565.15` 上方但低于 MA50 `590.82`，63 日回撤 `-14.82%`；SOXX 在 MA20 `528.71` 上方但低于 MA50 `561.01`，回撤 `-18.87%`。21 日相对变化为 RSP/SPY `+0.05%`、HYG/LQD `+1.10%`、IWM/SPY `-0.68%`、SMH/QQQ `-1.09%`，未触发广度或信用 `-2.5%` 恶化阈值。VIX 五日变化 `+3.66%`，VIX/VIX3M=`0.822`，期限结构正常。

当天策略建议、执行清单与盘中复盘：8/18 仅发现公开来源/机构研究监控，未发现新的用户或券商确认的策略建议、执行清单、订单、成交或盘中账户事实；最近真实账户执行资料仍为 7/10 历史计划，不能替代新的交易事实。

## 市场恐慌门控

正式判定：**normal 4/14**。VIX 低于 16、五日未出现压力性扩张、期限结构正常，SPY/QQQ 趋势和广度/信用代理健康；扣分来自 SMH/SOXX 的深度 63 日回撤以及二者仍低于 MA50。缺少的期权、ETF 流量与 CTA 数据不被记作零风险。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（最大股票敞口 95%）
- 实际 AI-capex 相关新增/摊低上限：**0%**。四项真实持仓仍是一条共同因子 sleeve，GLW/MXL/MRVL 的既有风险复核均未闭环，且 SMH/SOXX 未重回 MA50；normal 门控不构成相关加仓授权。

## Stop-trigger table

| 标的 | 8/18 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 159.90 | completed-week `<166-167` 复核带 | 8/14 完成周收盘 `165.99` 已跌破，且现低于带 3.70% | **reduce-review / defensive hold / no add**；待用户/券商确认风控处置，不能推断订单 |
| MXL（真实 6 股） | 72.63 | completed-close `<78` | 已触发，低于线 6.88% | **reduce-review / defensive hold / no add** |
| MRVL（真实 4 股） | 216.00 | completed-week `<223`；利润保护 | 8/14 完成周已跌破，现仍低于带 3.14% | **reduce-review / defensive hold / no add**；禁止因事件反弹自动追高 |
| QCOM（真实 2 股） | 160.19 | 7/27 长期持有覆盖；新增需收复约 182、两次收盘不创新低及 sleeve 容量 | 覆盖有效，新增条件未满足 | long-term hold / no add / thesis review |
| AMD（replay/watch，非真实持仓） | 484.39 | completed-close `<492` | **已触发，低于线 1.55%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 496.16 | `<500` | **已触发，低于线 0.77%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 903.68 | `<835` | 在线上 8.22%，但单日大幅回撤后未确认修复 | defensive recovery / near-stop review / no buy |

AMD、WDC、STX 仅用于 replay/watch，本表不推断真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：广度与信用代理尚未恶化、VIX 温和，但半导体内部相对强度走弱、SMH/SOXX 深回撤且低于 MA50。期权期限、单股隐含相关、杠杆 ETF 流、买回窗口与 CTA 直接数据为 `unavailable`，未伪装为低风险。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：仅 Fear Gate 允许暴露得分；SMH/SOXX 均未重回 MA50，SMH/QQQ 21 日相对变化为负，且未有完成收盘确认的催化/有序回踩。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。单日下跌不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_downside_reacceleration; unresolved_GLW_MXL_MRVL_risk_review`。
- `bottleneck_watch`：光互连、定制芯片和存储在同日同步走弱；这说明共同 AI-capex 因子仍占主导，不构成需求或盈利质量改善证据。
- `action impact`：`theme_overlap_high` 与 `sleeve_correlation_high` 已触发组合级相关风险复核，而非只看单股。四项真实持仓仍按一条有效 sleeve 管理；在风险复核闭环及 SMH/SOXX 趋势确认前，相关新增/摊低维持 **0%**。

## 模型组合净值核对

仅以用户/券商既有确认的工作现金 USD `3,756.49` 与 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 按本收盘标记；未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,939.96 |
| 工作 NAV | USD 5,696.45 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.94%；USD 1,939.96 / 34.06% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 864.00 / 15.17% |

现金高于 normal 的 5% 底线；MRVL 仍略高于 normal 15% 单名上限，维持 no-add 与风险复核。冻结 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘为 **USD 20,146.62**；overlay NAV 和差额留空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-18 收盘行，未预填未来日期。单日价格、replay 或警报不足以升级为稳定规则，故不更新 `memory/decisions.md`。
