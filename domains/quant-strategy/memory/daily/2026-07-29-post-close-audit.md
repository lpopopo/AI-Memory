# 2026-07-29 美股盘后正式审计

审计完成于 2026-07-30 21:41 Asia/Shanghai（美东 7/30 09:41、下一交易日盘中）。仅使用本地结构化报价的 yesterdayClose 作为 7/29 已完成常规交易日收盘；不将当日盘中 price 写作收盘。未登录券商、未提交订单、未假设真实成交；真实账户以用户或券商回报为准。

## 收盘数据、来源与质量

先按 tools/README.md 的 Node Quote Workflow Smoke Test 请求 MRVL、AMD、SPY、QQQ、SMH，再扩展至 WDC、STX、SOXX、RSP、HYG、LQD、IWM 及实际持仓。两次均返回非空、带 source: Tencent (Primary) 的结构化对象，因此本地 quote workflow 可用；无需 Python 兜底。

权益/ETF 使用 2026-07-30 21:41 运行时对象的 yesterdayClose，即 7/29 completed close，质量为 medium（单一但可追溯的本地结构化来源）。本地 VIX 是陈旧 21.67 且无有效 OHLC/成交量，VIX3M 无对象，未采用。Google Finance 渲染可见卡片：VIX 于 7/30 GMT-5 08:21 为 18.82、-1.84（-8.91%），反推 7/29 收盘 20.66；VIX3M 于 7/29 GMT-5 15:15 为 21.50、+1.64（+8.26%）。两者均为 Google browser-visible snapshot / medium，不是跳转 HTML。

| 标的 | 7/29 收盘 | 相对 7/28 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 163.40 / 429.56 | -6.35% / -5.51% | Node Tencent Primary yesterdayClose / medium |
| WDC / STX | 462.04 / 764.43 | -0.32% / +2.29% | 同上 |
| SPY / QQQ | 729.46 / 661.73 | -1.54% / -2.04% | 同上 |
| SMH / SOXX | 504.22 / 465.00 | -4.79% / -5.38% | 同上 |
| VIX / VIX3M | 20.66 / 21.50 | +13.45% / +8.26% | Google browser-visible snapshot / medium |
| RSP / SPY | 215.73 / 729.46 | -0.90% / -1.54% | Tencent Primary / medium |
| HYG / LQD | 79.24 / 106.22 | -0.23% / -0.57% | Tencent Primary / medium |
| IWM / SPY | 288.57 / 729.46 | -1.64% / -1.54% | Tencent Primary / medium |

## 市场恐慌门控

正式、保守的可得数据评分为 elevated 6/14：VIX 位于 16–22 的 elevated 区间且单日上升 13.45%，但 VIX/VIX3M 为 0.961、无近端倒挂；SPY/QQQ 下跌有限，而 SMH/SOXX 的 -4.79%/-5.38% 与 AI-capex 篮子同步走弱构成主要风险分。RSP 相对 SPY 略稳、HYG 相对 LQD 未显示额外信用恶化，故不升级为 stress；缺失 5/21 日完整序列不强行加分。

风险乘数 70%；现金底线 25%；框架最大新增买入敞口 25%（最大总股票敞口 75%）。实际账户新增/摊低上限仍为 0%，因为四个真实持仓有一个 AI-capex/半导体共同因子、trend_broken、theme_overlap_high、sleeve_correlation_high，且 MXL 风险复核未闭环。

## Stop-trigger table

| 标的 | 7/29 收盘 | 既有线/约束 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 124.05 | 长期重分类；completed-week <166–167 复核 | 复核持续；旧 stop 仅 planning-only | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 57.25 | completed-close <78 | 已触发，距线 -26.60% | reduce-review / defensive hold / no add；须用户/券商核对真实处置 |
| MRVL（真实 4 股） | 163.40 | completed-week <223；利润保护和长期底部复核 | 复核持续 | defensive hold / completed-week reduce-review / no add；反弹不追高 |
| QCOM（真实 2 股） | 155.68 | 原 <182 已被 7/27 长期核心重分类覆盖 | 非自动卖出；财报后两次不创新低及重回约 182 未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch） | 429.56 | completed close <492 | 已触发，-12.69% | reduce-review / no buy |
| WDC（replay/watch） | 462.04 | <500 | 已触发，-7.59% | reduce-review / defensive hold / no buy |
| STX（replay/watch） | 764.43 | <835 | 已触发，-8.45% | reduce-review / defensive hold / no buy |

AMD、WDC、STX 是 replay/watch，非真实持仓或订单推定。GLW/MRVL 的历史短线 stop-market 建议未提交，且已由长期重分类替代。

## Institutional overlay scorecard 与组合级复核

- flow_fragility_score：5/14，medium（proxy-based）。AI/半导体同步弱于宽基、领导层/小盘广度分化和 VIX 抬升计分；期权、CTA、杠杆 ETF、回购窗口直接数据 unavailable，不强行填充。
- trend_aligned_entry_score：1/5，trend_broken。只有 Fear Gate 允许缩减风险后的敞口得分；趋势、相对强度、回撤质量和已验证催化均未通过。
- AI_quality/capex_cycle：GLW diversified_supplier / medium；QCOM diversified_supplier + edge inference / medium-high；MRVL/AMD/WDC/STX cyclical_supplier / high；MXL speculative_bottleneck / high。
- factor_macro_flags：growth_duration_high；theme_overlap_high；sleeve_correlation_high；AI_capex_cycle_high；semiconductor_basket_unwind；unresolved_risk_review。
- bottleneck_watch：光互连/定制硅与存储链同步承压；没有经验证的新订单、收入、毛利或独立资金流事实改变分类。
- action impact：已执行组合级相关风险复核。GLW/MXL/MRVL/QCOM 按一个有效 AI-capex sleeve 管理；禁止相关新增或摊低，优先等待 MXL 用户/券商风险闭环及 QCOM 财报后两次 completed-session 条件。

theme_overlap_high 或 sleeve_correlation_high 已足以要求组合级复核，不因 flow_fragility 仅为 medium 而解除。

## 组合净值核对

沿用已确认现金 USD 3,756.49、真实持仓 GLW 2、MXL 6、MRVL 4、QCOM 2；未假设新增订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,556.56 |
| 工作 NAV | USD 5,313.05 |
| 现金 / 股票敞口 | USD 3,756.49 / 70.70%；USD 1,556.56 / 29.30% |
| 持仓数 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 653.60 / 12.30% |

最大单股低于正常 15% 上限、现金高于 elevated 25% 底线，但不构成加仓许可。冻结的历史 institutional-replay baseline（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401、现金 USD 12,323.96）按本日收盘复算为 USD 19,033.36；没有经过验证的 overlay 自动执行假设，overlay NAV 与差额为空。

## Replay 与记忆边界

已向迁移后的 strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv 仅追加完成的 2026-07-29 收盘行；原 experiments 路径不存在，未创建重复台账，也未预填未来日期。单日警报或单日 replay 不构成稳定规则，故不更新 memory/decisions.md。
