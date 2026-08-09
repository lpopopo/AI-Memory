# 2026-08-06 美股盘后正式审计

审计完成：2026-08-08 00:00 Asia/Shanghai。对象为已完成的 2026-08-06 美国常规交易日。未登录券商、未提交订单、未假设真实成交；真实账户、现金和成交只以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），返回非空 `Tencent (Primary)` 结构化对象；再扩展至风险代理和四个确认持仓。运行时下一交易日已开盘，因此按这些对象的 `yesterdayClose` 记录 8/06 完成收盘，而非包含盘中成分的 `price`。PowerShell WebClient 获取的 Yahoo Chart 8/06 完整日线逐项一致。Tencent 的 VIX 仍为陈旧 `21.67`、VIX3M 无对象，均未采用；Cboe 官方 daily-price CSV 给出同步 VIX/VIX3M 收盘。

| 标的 | 8/06 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 210.54 / 489.28 | -0.23% / +1.50% | Tencent Primary `yesterdayClose` + Yahoo Chart completed bar / 中高 |
| WDC / STX | 451.52 / 852.95 | -13.03% / +1.83% | 同上 / 中高 |
| SPY / QQQ | 768.56 / 714.65 | -0.16% / -0.37% | 同上 / 中高 |
| SMH / SOXX | 571.48 / 532.52 | +0.31% / +0.34% | 同上 / 中高 |
| VIX / VIX3M | 15.15 / 18.69 | -4.17% / -1.37% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 218.58 / 768.56 | -0.52% / -0.16% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.46 / 106.36 | -0.08% / -0.36% | 同上 / 中高 |
| IWM / SPY | 298.25 / 768.56 | -0.51% / -0.16% | 同上 / 中高 |

技术与代理复核：SPY 在 MA20/MA50 `749.26/746.73` 上方，距 63 日高点 `-0.36%`；QQQ 在 MA20 `700.46` 上方、与 MA50 `714.70` 基本持平（低 `0.01%`），距 63 日高点 `-4.22%`；SMH 在 MA20 `565.43` 上方但仍低于 MA50 `595.20`，距 63 日高点 `-14.57%`。VIX 五日变动 `-11.35%`，VIX/VIX3M `0.811`，期限结构正常。21 日相对变化为 RSP/SPY `-0.10%`、HYG/LQD `+0.98%`、IWM/SPY `-1.44%`，均未到 `-2.5%` 恶化阈值。

## 市场恐慌门控

正式判定：**normal 4/14**。SMH 深度回撤及其 MA50 下方仍是主要扣分项；低 VIX、正常期限结构、SPY 高位、未触发的广度/信用阈值抵消了升级条件。QQQ 对 MA50 的 `0.01%` 边界偏离只作观察，不单独升级门控。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（最大总股票敞口 95%）
- 账户实际 AI-capex 相关新增/摊低上限：**0%**。四个真实持仓仍是一条有效的 AI-capex/common-factor sleeve；SMH 未修复 MA50，MXL 风险复核未闭环，且 WDC 的剧烈下跌不构成新的入场证据。

## Stop-trigger table

| 标的 | 8/06 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 157.18 | completed-week `<166–167` 复核 | 低于复核区 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 70.20 | completed-close `<78` | 已触发，低于线 10.00% | reduce-review / defensive hold / no add；仅等用户或券商回报核对实际处置 |
| MRVL（真实 4 股） | 210.54 | completed-week `<223`；利润保护与长期底部复核 | 低于复核区 | defensive hold / completed-week reduce-review / no add；禁止因事件反弹追高 |
| QCOM（真实 2 股） | 160.39 | 7/27 长期覆盖；未来加 1 股仍需约 182 收盘收复、两日不创新低及 sleeve 容量 | 长期覆盖有效；加仓条件未齐 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 489.28 | completed-close `<492` | **已触发，低于线 0.55%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 451.52 | `<500` | **已触发，低于线 9.70%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 852.95 | `<835` | 未触发，高于线 2.15% | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅为历史 replay/watch，不能由此推断真实持仓、订单或成交。

## Institutional overlay 与组合级相关风险复核

- `flow_fragility_score: 5/14 -> medium (proxy-based)`：小盘相对表现仍弱、广度日内偏弱，但 21 日广度/信用代理未达恶化阈值，且没有可验证的期权偏斜、0DTE 或杠杆 ETF 日流量来上调分数。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 未封闭，但 SMH 在 MA50 下方；持仓和 AMD/WDC/STX 均无干净的相对强度与支撑回收确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。价格未提供加仓所需的质量或趋势确认。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连/定制芯片/存储仍暴露于同一 AI-capex 链；WDC 单日 `-13.03%` 强化存储环节的周期敏感性，未看到可验证的新收入、利润率、订单或现金流证据改变分类。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high` 已执行组合级而非单股复核。GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理；在 MXL 风险闭环、SMH 重新站稳 MA50 及相对强度确认前，相关新增与摊低继续为 `0%`。

## 模型组合净值核对

按用户确认的工作现金 USD `3,756.49` 与确认持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 计算；不假设订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,898.50 |
| 工作 NAV | USD 5,654.99 |
| 现金 / 股票敞口 | USD 3,756.49 / 66.43%；USD 1,898.50 / 33.57% |
| 持仓数量 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 842.16 / 14.89% |

现金高于 normal 的 5% 底线，MRVL 在正常 15% 单名上限内，均不构成加仓授权。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金 USD `12,323.96`）按本收盘标记为 **USD 19,846.99**；overlay NAV 与差额保持空白，因为没有可验证的 overlay 执行假设。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-06 收盘行，未预填未来日期。单日 WDC 下跌、单日 replay 或流动性警报不构成稳定规则，`memory/decisions.md` 未更新。
