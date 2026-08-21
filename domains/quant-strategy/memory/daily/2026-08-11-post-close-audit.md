# 2026-08-11 美股盘后正式审计

审计完成于 2026-08-12 23:30 Asia/Shanghai（美东 2026-08-12 常规盘中）。因此本记录严格将本地报价对象的 `yesterdayClose` 作为 2026-08-11 的已完成常规交易收盘；未把 8/12 盘中 `price` 当作收盘。未登录券商、未提交订单、未虚构成交；真实账户与委托以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test，并扩展至持仓、指数、波动率及宽度/信用代理。Node 客户端返回非空 `Tencent (Primary)` 结构化 quote objects，说明本地 workflow 可用；其内置链路为 Tencent -> Yahoo Chart -> Sina，并含 `node:https -> PowerShell WebClient -> fetch` 传输兜底。随后通过同一本地 Node 客户端请求 Yahoo Chart 6 个月日线，核验每个权益/ETF 的 8/11 已完成日线。Tencent 的 VIX `21.67` 为陈旧值且未返回 VIX3M，均未采用；VIX/VIX3M 改用 Cboe official daily-price CSV。

| 标的 | 8/11 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 212.31 / 474.32 | +1.80% / +1.01% | Tencent Primary `yesterdayClose` + 本地 Yahoo Chart 已完成日线 / 中高 |
| WDC / STX | 437.93 / 820.52 | -0.09% / +2.44% | 同上 / 中高 |
| SPY / QQQ | 770.56 / 718.45 | -0.32% / -0.34% | 同上 / 中高 |
| SMH / SOXX | 572.93 / 534.20 | +0.62% / +0.91% | 同上 / 中高 |
| VIX / VIX3M | 15.28 / 18.91 | -1.16% / -0.37% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 220.69 / 770.56 | +0.21% / -0.32% | Tencent Primary `yesterdayClose` + 本地 Yahoo Chart / 中高 |
| HYG / LQD | 79.51 / 105.99 | +0.04% / +0.03% | 同上 / 中高 |
| IWM / SPY | 300.99 / 770.56 | +0.34% / -0.32% | 同上 / 中高 |

技术与代理复核：SPY 位于 MA20/MA50 `752.30/747.84` 上方，距 63 日高点 `-0.35%`；QQQ 位于 `700.73/713.88` 上方，距 63 日高点 `-3.71%`。SMH 虽在 MA20 `561.83` 上方，但低于 MA50 `593.81`、距 63 日高点 `-14.35%`，且 21 日 SMH/QQQ 相对变化约 `-3.10%`。VIX 五日由 `16.50` 降至 `15.28`（约 `-7.39%`），VIX/VIX3M 为 `0.808`，期限结构正常。21 日 RSP/SPY、HYG/LQD、IWM/SPY 相对变化约为 `+0.16%/+0.90%/-0.28%`，未触发宽度或信用恶化阈值。

当天无独立的 8/11 策略建议、执行清单或盘中复盘文件；已读取的最近公共来源/机构研究材料只提供研究线索，不能替代价格、风控或真实成交确认。

## 市场恐慌门控

正式判定：**normal 4/14**。低位且正常期限结构的 VIX、SPY/QQQ 的趋势与未触发的宽度/信用代理支持 normal；SMH 深度回撤、低于 MA50 和相对 QQQ 偏弱保留扣分。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（最大股票敞口 95%）
- 实际 AI-capex 相关新增/摊低上限：**0%**。真实四项持仓仍是一只有效 common-factor sleeve；SMH 未重回 MA50，GLW/MXL/MRVL 风控复核未闭环。

## Stop-trigger table

| 标的 | 8/11 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 159.19 | completed-week `<166-167` 复核带 | 已低于复核带；不能以周内价格伪造周收盘 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 69.02 | completed-close `<78` | 已触发，低于线 11.51% | reduce-review / defensive hold / no add |
| MRVL（真实 4 股） | 212.31 | completed-week `<223`；利润保护及长期底部复核 | 已低于复核带 4.79% | defensive hold / completed-week reduce-review / no add；禁止因事件反弹自动追高 |
| QCOM（真实 2 股） | 162.68 | 7/27 长期覆盖；未来加仓须收复 182、两次收盘不创新低及 sleeve 容量 | 覆盖仍有效；加仓条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 474.32 | completed-close `<492` | **已触发，低于线 3.59%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 437.93 | `<500` | **已触发，低于线 12.41%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 820.52 | `<835` | **已触发，低于线 1.73%** | **reduce-review / no buy** |

AMD/WDC/STX 仅是 replay/watch，不由本表推断真实持仓、委托或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 5/14 -> medium (proxy-based)`：宽度与信用代理健康，直接的 0DTE、单股隐含相关性、杠杆 ETF 流量与 CTA 数据不可用且未强行记分；SMH/SOXX 的趋势破坏、存储链下行和既有主题集中维持中等脆弱性。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 可容许敞口，但 SMH 在 MA50 下、相对 QQQ 弱，持仓与存储链无完成收复确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。单日价格不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连、定制芯片和存储仍共用 AI-capex 链；SMH 相对走弱且 WDC/STX 均处风险线下，没有链条修复证据。
- `action impact`：虽 flow fragility 不是 elevated/acute，但 `theme_overlap_high` 与 `sleeve_correlation_high` 已触发组合级复核。GLW/MXL/MRVL/QCOM 按一只有效 sleeve 管理；在风险复核闭环、SMH 重回 MA50 且相对强度确认前，相关新增/摊低维持 **0%**。

## 模型组合净值核对

按已确认工作现金 USD `3,756.49`、真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 标记，未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,907.10 |
| 工作 NAV | USD 5,663.59 |
| 现金 / 股票敞口 | USD 3,756.49 / 66.33%；USD 1,907.10 / 33.67% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 849.24 / 14.99% |

现金高于 normal 5% 底线，MRVL 在 normal 15% 单名上限内，但两者均不构成加仓授权。冻结 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘标记为 **USD 19,669.51**；overlay NAV 与差额留空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-11 收盘行，未预填未来日期。单日警报及单日 replay 不足以提升为稳定规则，因此**不更新 `memory/decisions.md`**。
