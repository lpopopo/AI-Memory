# 2026-07-23 美股盘后正式审计

审计完成时间：2026-07-24 19:56 Asia/Shanghai（美国常规交易日 2026-07-23 已完成）。本记录只使用已完成收盘；未登录券商、未提交订单、未假设任何真实成交。真实账户状态仍以用户或券商回报为准。

已先读取策略摘要、稳定决策、日汇总、近期盘中/盘后记录、策略执行清单、组合与交易快照，以及恐慌门控、集中度、日度监控、institutional overlay、AI-capex、replay 和 Quote Workflow Smoke Test 规则。7/23 的公开来源/机构监控只提供研究线索，没有形成新的可交易催化剂或执行清单变更。

## 报价工作流与正式收盘快照

- 按 `tools/README.md` 的 Node Quote Workflow Smoke Test 运行本地 `StockService.fetchQuotes`。MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、RSP、HYG、LQD、IWM，以及真实持仓 GLW、MXL、QCOM 均返回结构化 `Tencent (Primary)` 对象；本地 quote workflow **可用**。
- 运行时为 2026-07-24 美股盘中，因此表中股票/ETF 使用这些对象的 `yesterdayClose`，即 2026-07-23 completed close；不使用当时盘中 `price`。质量为 `medium`：单一结构化本地来源、但符号及 completed-close 字段可追溯。
- Tencent 的 VIX 对象仍为陈旧 `21.67`，VIX3M 未返回对象，均未采用。Google Finance 渲染可见卡片显示：VIX 于 7/24 GMT-5 06:38 为 `18.87`、当日 `+2.23`，反推 7/23 close `16.64`；VIX3M 卡片于 7/23 GMT-5 15:15 显示 `20.60`、当日 `+1.06`。记录为 `Google browser-visible snapshot / medium`，不是跳转 HTML。

| 标的 | 2026-07-23 收盘 | 来源/质量 |
| --- | ---: | --- |
| MRVL | 210.99 | Node `Tencent (Primary).yesterdayClose` / medium |
| AMD | 552.33 | 同上 / medium |
| WDC | 556.67 | 同上 / medium |
| STX | 908.10 | 同上 / medium |
| SPY / QQQ | 747.41 / 705.35 | 同上 / medium |
| SMH / SOXX | 586.91 / 555.52 | 同上 / medium |
| VIX / VIX3M | 16.64 / 20.60 | Google browser-visible snapshot / medium |
| RSP / SPY | 212.70 / 747.41 | Node Tencent / medium |
| HYG / LQD | 79.52 / 106.67 | Node Tencent / medium |
| IWM / SPY | 293.79 / 747.41 | Node Tencent / medium |

限制：未取得独立的 5 日 VIX 或 21 日 ratio 完整序列；期权流、CTA、杠杆 ETF 流与 buyback 窗口也未验证，不能把缺口强行计分。7/22 的延期审计不以本次可得数据回填；本次正式行只对应已可靠取得的 7/23 close。

## Market Fear Gate

| 信号 | 判定 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 16.64，位于 elevated 区间 | 1 |
| VIX 5 日突升 | 无完整已核验序列，不强行计分 | 0 |
| VIX/VIX3M | 0.808，正常期限结构 | 0 |
| 半导体相对表现 | 相对 7/21，SMH +0.48%、SPY -0.12%；不是恐慌型广泛下跌 | 0 |
| 已有半导体趋势损伤 | 反弹仍未取得 MA/周线修复确认 | 2 |
| 广度/信用 | RSP/SPY 近两收盘基本平、IWM/SPY 轻微走弱、HYG/LQD 基本平；无已验证 21 日恶化 | 0 |

正式门控为 **`normal 3/14`**：风险乘数 `100%`，现金底线 `5%`，框架新买入上限 `50%`，最大总股票敞口 `95%`。但账户实际新增/摊低上限继续为 **`0%`**：四个确认持仓构成一个 AI-capex 共因子主题，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high`，且 QCOM 和 GLW/MXL/MRVL 的既有复核未闭环。市场门控不覆盖账户级风险约束。

## Stop-trigger table

| 标的 | 7/23 收盘 | 既有止损/减仓线 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 154.06 | completed-week `<166–167` 复核；新增需重回 200–205 且守住 190 | 仍低于 completed-week 复核带 | `defensive hold / completed-week reduce-review / no add` |
| MXL（真实 6 股） | 86.80 | completed-week `<78` 复核；新增需 `>97` | 未跌破 78，但高风险仓位与既有复核未闭环 | `defensive hold / reduce-review / no add` |
| MRVL（真实 4 股） | 210.99 | completed-week `<223`；利润保护；新增需 250–260 且权重 `<12%` | 仍低于 223；事件/反弹不构成追高理由 | `defensive hold / completed-week reduce-review / no add` |
| QCOM（真实 2 股） | 175.63 | 185 观察；completed close `<182` 失败入场复核 | **持续触发** `<182` | `reduce-review`；仅能由用户/券商回报闭环，不假设成交 |
| AMD（replay/watch） | 552.33 | completed close `<492` | 未触发，距线 +12.26% | `repair watch / no buy`；后续收盘 `<492` 必须 `reduce-review` |
| WDC（replay/watch） | 556.67 | `<500` | 未触发，距线 +11.33% | `defensive hold / repair watch / no buy` |
| STX（replay/watch） | 908.10 | `<835` | 未触发，距线 +8.75% | `defensive hold / repair watch / no buy` |

WDC/STX 已恢复在历史风险线之上，不能虚称本日触发；但它们仍是与 AI-capex 高相关的 defensive repair watch。MRVL 不因反弹自动追高；AMD 未低于 492，故没有规则覆盖或错误标注为 reduce-review 的理由。

## Institutional overlay scorecard 与组合级复核

```text
flow_fragility_score: 4/14 -> medium（proxy-based）
  窄广度 1：RSP/SPY 未恶化但未显示明确扩散；
  半导体/AI 集中 1：SMH 相对 7/21 强于 SPY，仍须警惕主题集中；
  systematic/vol-control 1：此前反弹与低 VIX 背景下趋势修复尚未验证；
  hedging complacency 1：正常期限结构，且无直接期权数据；其余直接流数据 unavailable，不强行计分。
trend_aligned_entry_score: 2/5 -> trend_broken
  仅 market-fear 可承受与半导体相对修复提供分数；无已验证 MA reclaim、干净回撤质量或已确认基本面催化剂。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high。
  7/23 公开监控线索未把价格确认提升为 confirmed。
factor_macro_flags:
  growth_duration_high; theme_overlap_high; sleeve_correlation_high;
  AI_capex_cycle_high; semiconductor_rebound_but_unconfirmed; unresolved_risk_review.
bottleneck_watch:
  光互连、网络/定制硅、存储仍为待验证观察线；没有新的订单、收入、毛利或独立资金流事实。
action impact:
  theme_overlap_high 与 sleeve_correlation_high 已触发组合级相关风险复核。四个真实持仓按一个有效主题管理，禁止相关主题新增/摊低；优先等待 QCOM 与 GLW/MXL/MRVL 的人工风险闭环。
```

## 组合净值核对

沿用已确认现金基线 USD 3,756.49 与真实持仓 GLW 2、MXL 6、MRVL 4、QCOM 2；不假设新增订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 2,024.14 |
| 工作 NAV | **USD 5,780.63** |
| 现金 / 股票敞口 | USD 3,756.49 / **64.98%**；USD 2,024.14 / **35.02%** |
| 持仓数 / 有效主题数 | 4 / 1（AI-capex common factor） |
| 最大单股 | MRVL USD 843.96 / **14.60%** |
| 历史 baseline replay model value | **USD 20,652.50** |

最大单股仍低于正常 15% 上限，但不授权加仓。历史 replay 的持仓数量和现金沿用冻结基线（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401、现金 USD 12,323.96）；没有经验证的 overlay 自动执行假设，因此 overlay NAV 与差额保持空白。

## Replay 与记忆边界

已只追加完成的 2026-07-23 收盘行到迁移后的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv`；原 `experiments/` 路径不存在，未创建重复台账。单日价格、反推 VIX 收盘和一次 overlay 告警均不构成稳定规则，故不更新 `memory/decisions.md`。
