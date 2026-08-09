# 2026-08-04 美股盘后正式审计

审计完成时间：2026-08-05 19:59 Asia/Shanghai。审计对象为已完成的 2026-08-04 美国常规交易日。未登录券商、未提交订单、未假设任何真实成交；真实账户、现金和成交仅以用户或券商回报为准。

## 收盘数据、来源与质量

首先依照 `tools/README.md` 运行 Node Quote Workflow Smoke Test（MRVL、AMD、SPY、QQQ、SMH），再扩展至风险代理和四个已确认持仓；两次均返回非空 `Tencent (Primary)` 结构化对象。随后以 Yahoo Chart 的 2026-08-04 completed daily bars 交叉验证，权益/ETF 全部一致。腾讯的 VIX 仍为无有效 OHLC/变动的陈旧 `21.67`，VIX3M 无对象，均未采用；Yahoo Chart 给出 VIX `16.50` 与 VIX3M `19.34`，后者历史序列不完整，故波动率数据为中等质量。未将 Google 跳转 HTML 作为报价。

| 标的 | 8/04 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 218.59 / 518.58 | +12.81% / +7.00% | Tencent Primary + Yahoo Chart completed close / 中高 |
| WDC / STX | 548.56 / 845.35 | +4.05% / +1.72% | 同上 / 中高 |
| SPY / QQQ | 771.33 / 723.85 | +1.80% / +3.40% | 同上 / 中高 |
| SMH / SOXX | 575.71 / 542.21 | +5.55% / +6.80% | 同上 / 中高 |
| VIX / VIX3M | 16.50 / 19.34 | +4.04% / 不可靠日变动 | Yahoo Chart completed snapshot；腾讯 VIX 陈旧、VIX3M 缺失 / 中等 |
| RSP / SPY | 220.23 / 771.33 | +1.44% / +1.80% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.55 / 106.76 | +0.30% / +0.61% | 同上 / 中高 |
| IWM / SPY | 301.71 / 771.33 | +1.85% / +1.80% | 同上 / 中高 |

完成日线诊断：SPY 处于 63 日高点且在 MA20/MA50（747.20/745.89）上方；QQQ 在 MA20/MA50（700.60/715.01）上方、距 63 日高点 -2.99%；SMH 收于 MA20 `568.40` 上方但仍低于 MA50 `595.94`、距 63 日高点 -13.93%。VIX 五日变化约 -9.39%，VIX/VIX3M 为 `0.853`，期限结构正常；RSP/SPY、HYG/LQD、IWM/SPY 未取得可验证的同步 21 日比率序列，不强行计入广度/信用恶化分数。

## 市场恐慌门控

正式判定：**normal 4/14**。VIX 处于 16--22 的温和抬升区间，SMH 63 日深度回撤是主要扣分；VIX 五日未上冲、期限结构正常，SPY/QQQ 不构成恐慌型回撤。风险乘数 **100%**，现金底线 **5%**，框架新买入上限 **50%**（最大总股票敞口 95%）。

这不是买入许可。实际相关新增/摊低上限仍为 **0%**：四个真实持仓仍是一条 AI-capex / semiconductor common-factor sleeve，SMH 尚未重回 MA50，且 MXL 风险复核未闭环；8/04 的急涨不构成趋势确认或追高理由。

## Stop-trigger table

| 标的 | 8/04 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 159.89 | completed-week `<166--167` 复核 | 仍低于复核区；历史短线单仅 planning-only | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 72.72 | completed-close `<78` | 已触发，低于线 6.77% | reduce-review / defensive hold / no add；等待用户或券商回报核对实际处置 |
| MRVL（真实 4 股） | 218.59 | completed-week `<223`；利润保护和长期底部复核 | 仍低于周线复核；单日 +12.81% 不授权追高 | defensive hold / completed-week reduce-review / no add |
| QCOM（真实 2 股） | 162.67 | 7/27 长期覆盖；只有基本面完整、非 stress/panic、两日不创新低、收盘重回约 182 且有 sleeve 容量才可评估加一股 | 覆盖仍有效，恢复条件未齐备 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 518.58 | completed-close `<492` | 未触发，高于线 5.40%；刚脱离此前触发 | repair watch / no buy（不因反弹自动解除复核） |
| WDC（replay/watch，非真实持仓） | 548.56 | `<500` | 未触发，高于线 9.71% | defensive hold / risk-line review / no buy |
| STX（replay/watch，非真实持仓） | 845.35 | `<835` | 未触发但仅高于线 1.24% | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅为历史 replay/watch，不得据此推断真实持仓或订单。

## Institutional overlay 与组合级复核

- `flow_fragility_score: 5/14 -> elevated (proxy-based)`：QQQ/SMH 分别跑赢 RSP 约 1.96/4.11 个百分点，半导体从深回撤中出现高波动急弹；8/04 公开机构监测记录的科技/半导体去杠杆、单股高波动和杠杆 ETF 收缩仍是背景。缺少 0DTE、期权偏斜、杠杆 ETF 逐日流量和隐含相关性点时数据，不强行补分。
- `trend_aligned_entry_score: 2/5 -> cheap_but_unconfirmed`：QQQ 已回到 MA20/MA50，SMH 仅回到 MA20且仍低于 MA50；单日反弹没有完成相对强度、支撑回收和独立催化确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_repair_unconfirmed; unresolved_MXL_risk_review`。
- `bottleneck_watch`：光互连、定制芯片、存储仍是同一 AI-capex 链的高敏感环节；8/04 已记录的研究材料只是观察日历与待验证架构线索，尚无足以改变分类的独立订单、收入、毛利或现金流证据。
- `action impact`：因 `flow_fragility=elevated`、`theme_overlap_high` 和 `sleeve_correlation_high` 已执行组合级相关风险复核，不只看单股。GLW/MXL/MRVL/QCOM 按一个有效 sleeve 管理；新增与摊低仍为 `0%`，先等待 MXL 风险闭环及 SMH MA50/相对强度确认。

## 模型组合净值核对

沿用用户确认的工作现金 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2`，不假设新订单、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,955.80 |
| 工作 NAV | USD 5,712.29 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.76%；USD 1,955.80 / 34.24% |
| 持仓数量 / 有效主题数 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 874.36 / 15.31% |

现金高于 normal 的 5% 底线。MRVL 略高于普通 15% 单股权重，因趋势和相关风险约束不构成加仓授权，并纳入下一次正式审计的权重复核。冻结 institutional-replay baseline 以本收盘复算为 **USD 20,387.58**；无可验证的 overlay 执行假设，overlay NAV 和差额继续留空。

## Replay 与记忆边界

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一行完成的 2026-08-04 收盘，未预填未来日期。单日反弹、单日回放或单日流动性警报不构成稳定规则，`memory/decisions.md` 未更新。
