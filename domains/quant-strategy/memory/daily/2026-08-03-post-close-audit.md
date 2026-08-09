# 2026-08-03 美股盘后正式审计

审计运行于 2026-08-04 09:03 Asia/Shanghai（2026-08-03 21:03 America/New_York）。审计对象为已经完成的 2026-08-03 美股常规交易日。未登录券商、未提交订单、未假设任何真实成交；真实账户、现金、订单和成交继续以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 执行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展至 WDC、STX、SOXX、RSP、HYG、LQD、IWM 和四个确认持仓。两次调用均返回非空、`source: Tencent (Primary)` 的结构化对象，故本地 workflow 可用，无需 Python 兜底。随后使用同一 Node 客户端的 Yahoo Chart 日线交叉核验；权益和 ETF 的 2026-08-03 completed close 与 Tencent `price` 一致。

本地 Tencent 的 VIX 对象仍是无有效 OHLC/变动的陈旧 `21.67`，VIX3M 无对象，均未用作本日收盘。Yahoo Chart 完成日线（2026-08-03）给出 VIX/VIX3M `15.86/18.93`；两者仅有该公开日线来源，质量记为中等。没有把跳转 HTML 当作报价，也不需要浏览器卡片兜底。

| 标的 | 8/03 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 193.78 / 484.64 | +3.31% / +1.78% | Tencent Primary + Yahoo Chart completed-close cross-check / 中高 |
| WDC / STX | 527.22 / 831.06 | -3.23% / -2.93% | 同上 / 中高 |
| SPY / QQQ | 757.67 / 700.07 | +1.42% / +1.76% | 同上 / 中高 |
| SMH / SOXX | 545.46 / 507.68 | +0.91% / +0.55% | 同上 / 中高 |
| VIX / VIX3M | 15.86 / 18.93 | -0.81% / -7.84% | Yahoo Chart completed daily bars；Tencent VIX 陈旧、VIX3M 缺失 / 中等 |
| RSP / SPY | 217.11 / 757.67 | +0.98% / +1.42% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.31 / 106.11 | -0.21% / -0.13% | Tencent Primary + Yahoo Chart / 中高 |
| IWM / SPY | 296.22 / 757.67 | +1.72% / +1.42% | Tencent Primary + Yahoo Chart / 中高 |

完成日线诊断：SPY 距 63 日高点 `-0.25%`；QQQ 为 `-6.18%`，收于 MA20 `699.88` 之上但低于 MA50 `714.83`；SMH 为 `-18.46%`，低于 MA20/MA50 `568.69/595.79`。21 日相对变动为 RSP/SPY `-0.71%`、HYG/LQD `+1.83%`、IWM/SPY `-2.19%`；均未达框架的 `-2.5%` 恶化阈值。VIX 五日变动 `-15.05%`，VIX/VIX3M 为 `0.838`，期限结构正常。

## 市场恐慌门控

正式判定为 **normal 3/14**：低 VIX、五日 VIX 下行、正向期限结构和浅 SPY 回撤均不增加恐慌分；QQQ `-6.18%` 的中度回撤与 SMH `-18.46%` 的深度回撤共计 3 分。风险乘数 **100%**，现金底线 **5%**，框架新买入上限 **50%**（最大总股票敞口 95%）。

这不是买入许可。实际相关新增/摊低上限仍为 **0%**：四个确认持仓仍是一条 AI-capex / semiconductor common-factor sleeve，SMH 的趋势破坏未修复，MXL 风险复核也没有闭环。

## Stop-trigger table

| 标的 | 8/03 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 146.64 | 长期重分类；completed-week `<166–167` 复核 | 复核持续；历史短线 stop 仅为 planning-only | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 67.11 | completed-close `<78` | 已触发，低于线 13.96% | reduce-review / defensive hold / no add；等待用户或券商回报核对实际处置 |
| MRVL（真实 4 股） | 193.78 | completed-week `<223`；利润保护和长期底部复核 | 复核持续；反弹不构成追高或新增条件 | defensive hold / completed-week reduce-review / no add |
| QCOM（真实 2 股） | 151.57 | 7/27 长期覆盖；满足两次不创新低、completed close 重回约 182 等条件后才评估加一股 | 覆盖理由有效；恢复条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 484.64 | completed-close `<492` | **已触发**，低于线 1.50% | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 527.22 | `<500` | 未触发；高于线 5.44%，仍处风险线复核区 | defensive hold / risk-line review / no buy |
| STX（replay/watch，非真实持仓） | 831.06 | `<835` | **已触发**，低于线 0.47% | **reduce-review / no buy** |

AMD、WDC、STX 仅为历史 replay/watch，不能据此推断真实持仓或订单。GLW、MXL、MRVL 的历史短线止损建议均未被确认提交，且已由长期重分类替代。

## Institutional overlay scorecard 与组合级相关风险复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：QQQ 上涨快于 RSP（窄领导的弱代理，1）；半导体大幅低于中期均线、现有 sleeve 同因子（1）；VIX 五日快速压缩，系统化/波控回补风险为弱代理（1）；低于 16 的 VIX 只作为对冲自满弱代理（1）。没有直接的 0DTE、偏斜、杠杆 ETF 流、买回窗口或隐含相关性数据，不强行评分。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许风险敞口（1），但 QQQ 仍低于 MA50、SMH 低于 MA20/MA50，SMH 21 日显著落后 QQQ，回撤质量与独立催化确认均不合格（其余 0）。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review`。
- `bottleneck_watch`：光互连、定制芯片、存储仍是同一 AI-capex 链的高敏感环节；本轮未取得足以改变分类的独立订单、收入、毛利或资金流新证据。
- `action impact`：即使 flow fragility 仅为 medium，`theme_overlap_high` 与 `sleeve_correlation_high` 已触发组合级复核。GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理，相关新增和摊低继续为 `0%`；先等 MXL 风险闭环和 QQQ/SMH 趋势确认，不能因单日反弹或低 VIX 放宽限制。

## 组合净值核对

沿用用户确认的现金 USD `3,756.49` 和持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2`；不假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,774.20 |
| 工作 NAV | USD 5,530.69 |
| 现金 / 股票敞口 | USD 3,756.49 / 67.92%；USD 1,774.20 / 32.08% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 775.12 / 14.01% |

现金高于 normal 的 5% 底线，最大单股低于普通 15% 上限；两者均不构成加仓授权。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘复算为 **USD 19,921.03**。没有可验证的 overlay 执行假设，overlay NAV 与差额留空。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一行已完成的 2026-08-03 close；未预填未来日期。单日 VIX 下行、指数反弹或单日 replay 不构成稳定规则，`memory/decisions.md` 不更新。
