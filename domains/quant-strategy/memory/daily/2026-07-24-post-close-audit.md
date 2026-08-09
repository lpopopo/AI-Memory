# 2026-07-24 美股盘后正式审计

审计完成时间：2026-07-25 11:35 Asia/Shanghai。仅使用已经完成的 2026-07-24 美国常规交易收盘数据；未登录券商、未提交订单、未假设任何真实成交。真实账户状态以用户或券商回报为准。

已先复核策略摘要、稳定决策、日汇总、近期审计/盘中复盘、执行清单、组合及交易快照，以及 Fear Gate、集中度、日度监控、institutional overlay、AI capex 分类、replay 协议和 Quote Workflow Smoke Test。

## 正式收盘数据与质量

- 按 `tools/README.md` 先运行 Node Quote Workflow Smoke Test；MRVL、AMD、SPY、QQQ、SMH 及扩展清单均返回结构化 `Tencent (Primary)` 对象，故本地 quote workflow **可用**。当前为周六，Node `price` 为已完成的 7/24 常规收盘，不使用 `yesterdayClose`。
- VIX 的本地对象仍为陈旧 `21.67`，VIX3M 未返回对象，均不采用。浏览器可见 Google Finance 卡片在 7/24 GMT-5 15:15:01 显示 VIX/VIX3M `18.58/20.51`；记录为 `Google browser-visible snapshot`，非跳转 HTML。
- 运行时间为 2026-07-25 11:xx Asia/Shanghai。股票/ETF 为单一结构化本地来源，质量 `medium`；VIX/VIX3M 为可见卡片，质量 `medium`。没有独立日线交叉验证，不把缺失的 5 日/21 日序列强制计分。

| 标的 | 7/24 收盘 | 来源 / 质量 |
| --- | ---: | --- |
| MRVL / AMD | 194.23 / 521.95 | Node `Tencent (Primary).price` / medium |
| WDC / STX | 519.80 / 851.69 | 同上 / medium |
| SPY / QQQ | 738.93 / 684.23 | 同上 / medium |
| SMH / SOXX | 561.19 / 527.01 | 同上 / medium |
| VIX / VIX3M | 18.58 / 20.51 | Google browser-visible snapshot（7/24 GMT-5 15:15）/ medium |
| RSP / SPY | 213.57 / 738.93 | Node Tencent / medium |
| HYG / LQD | 79.23 / 106.23 | Node Tencent / medium |
| IWM / SPY | 291.17 / 738.93 | Node Tencent / medium |

## Market Fear Gate

| 信号 | 判定 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 18.58，处于 elevated 区间 | 1 |
| VIX 5 日变化 | 无完整、已核验序列；不强行计分 | 0 |
| VIX/VIX3M | 0.906，正常期限结构 | 0 |
| 半导体相对表现 | SMH `-3.27%`、SOXX `-4.40%`，明显弱于 SPY `+0.10%` | 2 |
| 既有半导体趋势损伤 | 反弹修复未确认，且本日同步下跌 | 2 |
| 广度 / 信用 | RSP 强于 SPY；HYG/LQD 基本稳定；IWM 略弱但无 21 日确认恶化 | 0 |

正式门控为 **`elevated 5/14`**：风险乘数 `70%`、现金底线 `25%`、框架新买入上限 `25%`、最大总股票敞口 `75%`。实际新增/摊低上限仍为 **`0%`**：四项已确认持仓仍是一篮子 AI-capex/半导体共因子，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high`，且 QCOM/MXL 等风险处置未由用户或券商回报闭环。

## Stop-trigger table

| 标的 | 7/24 收盘 | 既有止损 / 减仓线 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 146.65 | completed-week `<166–167` 复核；新增需重回 200–205 且守住 190 | 仍低于 completed-week 复核带 | `defensive hold / completed-week reduce-review / no add` |
| MXL（真实 6 股） | 71.59 | completed-week `<78` 复核；新增需 `>97` | **触发 `<78`** | `reduce-review / defensive hold / no add`；等待用户或券商确认实际风险处置 |
| MRVL（真实 4 股） | 194.23 | completed-week `<223`；利润保护；新增需 250–260 且权重 `<12%` | 仍低于 223；本日 `-7.21%` | `defensive hold / completed-week reduce-review / no add`；禁止因事件反弹追高 |
| QCOM（真实 2 股） | 166.97 | completed close `<182` 失败入场复核 | **持续触发 `<182`** | `reduce-review`，未获成交回报前不得假定卖出；下次开盘优先由用户/券商核对处置 |
| AMD（replay/watch） | 521.95 | completed close `<492` | 未触发，距线 `+6.09%`，但半导体同步走弱 | `defensive repair watch / no buy`；下一收盘 `<492` 必须 `reduce-review` |
| WDC（replay/watch） | 519.80 | `<500` | 未跌破，距线 `+3.96%`，**near-stop** | `defensive hold / near-stop review / no buy` |
| STX（replay/watch） | 851.69 | `<835` | 未跌破，距线 `+2.00%`，**near-stop** | `defensive hold / near-stop review / no buy` |

## Institutional overlay scorecard 与组合级相关风险复核

```text
flow_fragility_score: 4/14 -> medium (proxy-based)
  窄广度 1：RSP 当日相对较强，但 Nasdaq/半导体领导层不稳；
  AI/半导体集中 2：SMH/SOXX 与持仓篮子同步急跌；
  systematic/vol-control 1：低于 VIX3M 的表面平静与趋势破坏并存；
  期权、CTA、买回窗口、杠杆 ETF 直接数据 unavailable，不强行计分。
trend_aligned_entry_score: 1/5 -> trend_broken
  Fear Gate 允许缩减风险后的敞口 1；价格趋势、相对强度、回撤质量、已确认催化均为 0。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high。
  本日没有把产品、生态或叙事线索升级为订单、收入、毛利或价格确认。
factor_macro_flags:
  growth_duration_high; theme_overlap_high; sleeve_correlation_high;
  AI_capex_cycle_high; semiconductor_basket_unwind; unresolved_risk_review.
bottleneck_watch:
  光互连、网络、存储仍仅为待验证观察线；7/24 无新订单、收入、毛利或独立资金流事实。
action impact:
  因 theme_overlap_high 与 sleeve_correlation_high 已执行组合级相关风险复核：
  GLW/MXL/MRVL/QCOM 按一个有效 AI-capex 主题管理，禁止相关主题新增或摊低；
  先闭环 QCOM 与 MXL 风险复核，再评估任何风险预算。
```

## 组合净值核对

沿用已确认现金基线 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2`；没有新增订单、成交、费用或 FX 假设。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,833.70 |
| 工作 NAV | **USD 5,590.19** |
| 现金 / 股票敞口 | USD 3,756.49 / **67.20%**；USD 1,833.70 / **32.80%** |
| 持仓数 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 776.92 / **13.90%** |
| 历史 baseline replay model value | **USD 20,115.43** |

最大单股仍低于正常 15% 上限，现金也高于 elevated 25% 底线；这不解除共因子与未闭环风险复核，不能授权加仓。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 仅追加已完成的 2026-07-24 收盘行；原 `experiments/` 路径不存在，未创建重复台账，也未预填未来日期。单日警报和单日 replay 不构成稳定规则，故不更新 `memory/decisions.md`。
