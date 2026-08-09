# 2026-07-30 美股盘后正式审计

审计完成于 2026-07-31 20:27 Asia/Shanghai（纽约 08:27；下一交易日盘前）。未登录券商、未提交订单、未假设任何真实成交；真实账户、现金和订单状态仍以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 运行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展至 WDC、STX、SOXX、RSP、HYG、LQD、IWM 和实际持仓。两次均返回非空、带 `source: Tencent (Primary)` 的结构化对象，因此本地 quote workflow 可用，未调用 Python 兜底。对象的 `price` 与 Yahoo Chart 2026-07-30 完整日线收盘逐项一致，故以此作为正式收盘；`yesterdayClose` 是 7/29 的前一日字段，未误作 7/30 收盘。

VIX 的 Tencent 对象仍为陈旧的 21.67 且无有效 OHLC；VIX3M 无本地对象。Google Finance 渲染可见卡片显示：VIX 于 7/31 07:07 GMT-5 为 17.06、日变动 -3.60（-17.42%），反推 7/30 收盘 20.66；VIX3M 卡片直接显示 7/30 15:15 GMT-5 收盘 19.50、-2.00（-9.30%）。两者均标为 `Google browser-visible snapshot`，不是跳转 HTML。权益/ETF 为 `Tencent (Primary) price + Yahoo Chart completed-bar cross-check`（中高质量）；波动率为 Google 可见快照（中等质量）。

| 标的 | 7/30 收盘 | 对 7/29 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 183.30 / 485.39 | +12.18% / +13.00% | Tencent Primary + Yahoo Chart / 中高 |
| WDC / STX | 533.04 / 851.68 | +15.37% / +11.41% | 同上 |
| SPY / QQQ | 741.69 / 683.55 | +1.68% / +3.30% | 同上 |
| SMH / SOXX | 538.90 / 504.53 | +6.88% / +8.50% | 同上 |
| VIX / VIX3M | 20.66 / 19.50 | 0.00% / -9.30% | Google browser-visible / 中等 |
| RSP / SPY | 215.38 / 741.69 | -0.16% / +1.68% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.47 / 106.41 | +0.29% / +0.18% | 同上 |
| IWM / SPY | 292.59 / 741.69 | +1.39% / +1.68% | 同上 |

市场解读：半导体强势反弹且显著跑赢 QQQ，SPY/QQQ 同步上行；RSP 相对 SPY 单日落后约 1.84 个百分点、IWM 相对 SPY 略落后，参与度仍不够均衡。HYG 略强于 LQD，未见当日信用恶化。VIX/VIX3M = 1.060，属于近端轻度倒挂；缺少完整 5/21 日相对比率，不强行补分。

## 市场恐慌门控

正式、保守判定为 **elevated 5/14**：VIX 处于 16–22 elevated 区间，且 VIX/VIX3M 超过 1.05；半导体反弹和信用代理稳定阻止升级为 stress。风险乘数 **70%**，现金底线 **25%**，框架新买入上限 **25%**（最大总股票敞口 75%）。

实际账户的新增/摊低上限仍为 **0%**：四个确认持仓仍是一条 AI-capex/半导体共同因子 sleeve，`theme_overlap_high`、`sleeve_correlation_high` 与未闭环的 MXL 风险复核仍在，且整体趋势尚未确认修复。

## Stop-trigger table

| 标的 | 7/30 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 135.22 | long-term 重分类；completed-week <166–167 复核 | 复核持续；旧 stop 仅 planning-only | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 66.92 | completed-close <78 | 已触发，低于线 14.21% | reduce-review / defensive hold / no add；待用户或券商核对实际处置 |
| MRVL（真实 4 股） | 183.30 | completed-week <223；利润保护与长期底部复核 | 复核持续；反弹不构成追高条件 | defensive hold / completed-week reduce-review / no add |
| QCOM（真实 2 股） | 151.60 | 7/27 long-term override；财报后两次 completed session 不创新低且收回约 182 才可评估加一股 | 当日低于 7/29 收盘，恢复条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 485.39 | completed-close <492 | 已触发，低于线 1.34% | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 533.04 | <500 | 高于线 6.61%，仍 near-stop 范围 | defensive hold / near-stop review / no buy |
| STX（replay/watch，非真实持仓） | 851.68 | <835 | 高于线 1.997%，near-stop | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅用于历史 replay/watch，未被推断为真实仓位或订单。GLW/MXL/MRVL 的历史短线 stop 建议均未提交，且已由 long-term 重分类取代。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 6/14 -> medium (proxy-based)`：半导体/AI 相对宽基的大幅领涨（2 分）、RSP 落后显示的混合广度（1 分）、VIX 仍 elevated 且期限结构倒挂（1 分）、短期急涨后的系统性仓位重建风险（1 分）、同主题拥挤（1 分）。0DTE、期权偏斜、杠杆 ETF 流、回购窗口与隐含相关性没有直接数据，均不强行填分。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 仅允许缩减后的风险敞口；20/50 日趋势、持续相对强度、回撤质量与经验证催化剂均未满足。单日反弹不是买入确认。
- `AI_quality/capex_cycle`：GLW diversified supplier / medium；QCOM diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX cyclical supplier / high；MXL speculative bottleneck / high。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_rebound_but_unconfirmed; unresolved_risk_review`。
- `bottleneck_watch`：光互连/定制芯片与存储链条同步反弹，但没有新、可归属且经独立验证的订单、收入、毛利或资金流证据。
- `action impact`：已执行组合级相关风险复核。由于 theme overlap 与 sleeve correlation 均为 high，GLW/MXL/MRVL/QCOM 按一个有效 AI-capex sleeve 管理；禁止相关新增或摊低，优先完成 MXL 真实账户风险闭环。即使 flow fragility 仅为 medium，也不解除该组合约束。

## 组合净值核对

沿用用户确认现金 USD 3,756.49 和真实持仓 GLW 2、MXL 6、MRVL 4、QCOM 2；未假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,708.36 |
| 工作 NAV | USD 5,464.85 |
| 现金 / 股票敞口 | USD 3,756.49 / 68.74%；USD 1,708.36 / 31.26% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 733.20 / 13.42% |

现金高于 elevated 25% 底线、最大单股低于正常 15% 上限，但这不是加仓许可。冻结的 institutional-replay baseline（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401；现金 USD 12,323.96）按本收盘复算为 **USD 19,907.90**（单日 +4.59%）；没有可验证的 overlay 执行假设，overlay NAV 与差额保持空白。

## Replay 与记忆边界

已向迁移后的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条完成的 2026-07-30 close 行。旧 `experiments/2026-06-08-institutional-overlay-replay/` 路径不存在，未创建重复账本，也未预填未来日期。

本次仅为单日收盘、单日反弹与实验 overlay 观察，不构成稳定规则验证；`memory/decisions.md` 不更新。
