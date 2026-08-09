# 2026-08-07 美股盘后正式审计

审计完成：2026-08-08 12:23 Asia/Shanghai（纽约 2026-08-08 凌晨，2026-08-07 常规交易已经收盘）。本记录不登录券商、不提交订单、不推断真实成交；真实账户、现金与任何委托仅以用户或券商回报为准。

## 收盘数据、来源与质量

先依照 `tools/README.md` 运行 Node Quote Workflow Smoke Test，并扩展至风险代理和四个已确认持仓。Node 首层返回非空 `Tencent (Primary)` 结构化 quote objects；为核验正式收盘，再直接运行本地客户端的 `Yahoo Chart (Fallback)` 路径，所有下表权益/ETF 的 2026-08-07 `price` 与 Tencent 一致。Node 客户端已依次具备 `node:https -> PowerShell WebClient -> fetch` 传输兜底；PowerShell 对 Yahoo 的直接日线请求返回 404 不构成 workflow 不可用，因为两条本地路径均返回了结构化对象。Tencent 的 VIX 是陈旧的 `21.67`，VIX3M 无对象，未采用；Cboe 官方 daily-price CSV 提供同步正式收盘。

| 标的 | 8/07 收盘 | 日变动 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 218.72 / 483.36 | +3.89% / -1.21% | Tencent Primary + Yahoo Chart Fallback 一致 / 中高 |
| WDC / STX | 434.30 / 812.76 | -3.81% / -4.71% | 同上 / 中高 |
| SPY / QQQ | 773.26 / 723.03 | +0.61% / +1.17% | 同上 / 中高 |
| SMH / SOXX | 582.70 / 543.27 | +1.96% / +2.02% | 同上 / 中高 |
| VIX / VIX3M | 14.90 / 18.72 | -1.65% / +0.16% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 220.09 / 773.26 | +0.69% / +0.61% | Tencent Primary + Yahoo Chart Fallback / 中高 |
| HYG / LQD | 79.61 / 106.55 | +0.19% / +0.18% | 同上 / 中高 |
| IWM / SPY | 301.56 / 773.26 | +1.11% / +0.61% | 同上 / 中高 |

技术与代理复核：SPY 位于 MA20/MA50 `750.17/747.19` 上方并创 63 日新高；QQQ 位于 MA20/MA50 `700.34/714.57` 上方、距 63 日高点 `-3.10%`；SMH 位于 MA20 `564.01` 上方但仍低于 MA50 `594.94`，距 63 日高点 `-12.89%`。VIX 五日由 `15.99` 降至 `14.90`（`-6.82%`），VIX/VIX3M 为 `0.796`，期限结构正常。21 日相对代理：RSP/SPY `+0.21%`、HYG/LQD `+0.91%`、IWM/SPY `-1.37%`，均未触发 `-2.5%` 广度/信用恶化阈值。

当天没有可用的 8/07 独立策略建议、执行清单或盘中复盘文件；已复核现有执行清单与 8/06 审计，均不构成订单或成交事实。

## 市场恐慌门控

正式判定：**normal 4/14**。低且回落的 VIX、正常期限结构、SPY/QQQ 趋势和未触发的广度/信用代理维持 normal；SMH 深度回撤且位于 MA50 下方保留四分风险扣分。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（总股票敞口上限 95%）
- 实际 AI-capex 相关新增加仓/摊低上限：**0%**。四个真实持仓仍为一个 AI-capex/common-factor sleeve；SMH 尚未修复 MA50，且 MXL、GLW、MRVL 的风险复核未闭环。

## Stop-trigger table

| 标的 | 8/07 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 165.68 | completed-week `<166–167` 复核 | 已低于复核区 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 74.98 | completed-close `<78` | 已触发，低于线 3.87% | reduce-review / defensive hold / no add；仅等用户或券商回报核对真实处置 |
| MRVL（真实 4 股） | 218.72 | completed-week `<223`；利润保护与长期底部复核 | 已低于线 1.92% | defensive hold / completed-week reduce-review / no add；不得因本日反弹追高 |
| QCOM（真实 2 股） | 167.86 | 7/27 长期覆盖；未来加 1 股仍需收复约 182、两日不创新低及 sleeve 容量 | 长期覆盖有效；加仓条件未齐 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 483.36 | completed-close `<492` | **已触发，低于线 1.76%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 434.30 | `<500` | **已触发，低于线 13.14%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 812.76 | `<835` | **已触发，低于线 2.66%** | **reduce-review / no buy** |

AMD、WDC、STX 仅用于历史 replay/watch，不能由此推断真实持仓、委托或成交。

## Institutional overlay 与组合级相关风险复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：指数、等权、信用和小盘代理并未同步恶化；但半导体内部修复仍不均衡，且 AI-capex 主题集中度未下降。缺少当日期权偏斜、0DTE、杠杆 ETF 流量和隐含相关性，未将缺失数据强行打分。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许敞口，但 SMH 仍低于 MA50；存储链 WDC/STX 继续下跌，未见可验证的新催化剂与完整相对强度/支撑收复，故不满足新增条件。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。收盘反弹或单日价格不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连/定制芯片与存储仍暴露于同一 AI-capex 链；WDC/STX 的同步下跌表明存储环节未修复。无经验证的收入、毛利、订单或现金流新证据可改变分类。
- `action impact`：因 `theme_overlap_high` 与 `sleeve_correlation_high`，已进行组合级而非单股孤立复核。GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理；在 MXL 风险闭环、SMH 重新站稳 MA50 且相对强度确认前，相关新增/摊低保持 `0%`。

## 模型组合净值核对

按用户确认的工作现金 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 标记，不假设订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,991.84 |
| 工作 NAV | USD 5,748.33 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.35%；USD 1,991.84 / 34.65% |
| 持仓数量 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 874.88 / 15.22% |

现金高于 normal 的 5% 底线。MRVL 比 normal 的 15% 单名上限高 `0.22` 个百分点，列入风险复核且不构成加仓授权。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘标记为 **USD 19,731.93**；overlay NAV 与差额保持空白，因为没有可验证的 overlay 执行假设。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-07 收盘行（仓库中不存在用户提示的旧 `experiments/...` 路径）。未预填未来日期。单日反弹、存储弱势或一次 replay 警报不足以成为稳定规则，`memory/decisions.md` 未更新。
