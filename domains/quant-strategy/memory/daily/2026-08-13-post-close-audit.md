# 2026-08-13 美股盘后正式审计

审计完成于 `2026-08-15 09:18 Asia/Shanghai`。当时美股 `2026-08-14` 常规盘仍在交易；因此本记录严格以本地结构化行情的 `yesterdayClose` 作为已完成的 `2026-08-13` 收盘，未将 8/14 盘中数据写成收盘。未登录券商、未提交订单、未虚构成交；真实账户以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 运行 Node Quote Workflow Smoke Test（`MRVL/AMD/SPY/QQQ/SMH`），再扩展至持仓、指数、波动率和广度/信用代理。两次调用均返回非空 `Tencent (Primary)` 结构化 quote objects；本地工作流可用，且其内置链路为 Tencent -> Yahoo Chart -> Sina，含 `node:https -> PowerShell WebClient -> fetch` 传输兜底。对权益/ETF 使用本地 Yahoo Chart 6 个月日线的 8/13 completed bar 交叉核对，数值一致。腾讯 VIX `21.67` 明显陈旧且无 VIX3M，未采用；VIX/VIX3M 使用 Cboe 官方 daily-price CSV。

| 标的 | 8/13 收盘 | 日变动 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 222.18 / 483.01 | +2.35% / +0.02% | Tencent Primary `yesterdayClose` + 本地 Yahoo Chart completed bar / 中高 |
| WDC / STX | 487.29 / 921.37 | +7.31% / +4.92% | 同上 / 中高 |
| SPY / QQQ | 777.88 / 732.07 | +0.70% / +1.16% | 同上 / 中高 |
| SMH / SOXX | 589.12 / 550.74 | +0.73% / +0.76% | 同上 / 中高 |
| VIX / VIX3M | 14.63 / 18.61 | +0.55% / +0.43% | Cboe 官方 daily-price CSV / 高 |
| RSP / SPY | 222.73 / 777.88 | +0.75% / +0.70% | Tencent Primary + 本地 Yahoo Chart / 中高 |
| HYG / LQD | 79.79 / 106.55 | +0.23% / +0.41% | 同上 / 中高 |
| IWM / SPY | 303.50 / 777.88 | +0.26% / +0.70% | 同上 / 中高 |

技术与代理复核：SPY 在 MA20/MA50 `754.54/748.48` 上方、距 63 日高点 `-0.19%`；QQQ 在 `702.34/713.21` 上方、距高点 `-2.22%`。SMH 在 MA20 `562.54` 上方但低于 MA50 `592.49`，距 63 日高点 `-12.31%`，且 21 日相对 QQQ 约 `-2.23%`。VIX 五日约 `-3.43%`，VIX/VIX3M=`0.786`，期限结构正常；21 日 RSP/SPY、HYG/LQD、IWM/SPY 相对变化约 `+1.48%/+0.94%/-0.43%`，未触发广度或信用恶化阈值。当天盘中/策略建议与执行清单没有新增、已确认的经纪商事实；最近公开来源监控仅提供主题拥挤度的低确定性观察，不能覆盖价格或风险规则。

## 市场恐慌门控

正式判定：**normal 4/14**。低 VIX、正常期限结构、SPY/QQQ 趋势和广度/信用健康抵消了风险；SMH 深度回撤、低于 MA50、相对 QQQ 偏弱保留扣分。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**
- 实际 AI-capex 相关新增/摊低上限：**0%**。四个真实持仓仍是一条共同因子 sleeve，SMH 未重回 MA50，且 GLW/MXL/MRVL 风险复核未闭环；`normal` 不构成相关加仓授权。

## Stop-trigger table

| 标的 | 8/13 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 158.54 | completed-week `<166-167` 复核带 | 低于复核带；本周尚未完成收盘 | defensive hold / completed-week reduce-review / no add |
| MXL（真实 6 股） | 76.65 | completed-close `<78` | **已触发，低于线 1.73%** | reduce-review / defensive hold / no add |
| MRVL（真实 4 股） | 222.18 | completed-week `<223`；利润保护与长期底部复核 | **低于复核带 0.37%，near-stop** | defensive hold / completed-week reduce-review / no add；禁止因事件反弹自动追高 |
| QCOM（真实 2 股） | 164.79 | 7/27 长期持有覆盖；未来加仓需收复约 182、两次收盘不创新低和 sleeve 容量 | 覆盖有效；新增条件未满足 | long-term hold / no add / thesis review |
| AMD（replay/watch，非真实持仓） | 483.01 | completed-close `<492` | **已触发，低于线 1.83%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 487.29 | `<500` | **已触发，低于线 2.54%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 921.37 | `<835` | 在线上 10.34%，但仍是高波动修复 | defensive hold / risk-line recovery review / no buy |

AMD、WDC、STX 只用于 replay/watch，不推断为真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 4/14 -> medium (proxy-based)`：广度和信用代理健康，但指数接近高点而半导体仍低于 MA50、相对 QQQ 落后；期权、杠杆 ETF 流量、隐含相关性和 CTA 数据不可得，未被伪装为零风险。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许暴露得 1 分；SMH 未收复 MA50、相对强度未修复，且没有可验证的新催化剂/有序重建确认。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。单日反弹不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连、定制芯片、存储仍共享 AI-capex 周期；WDC/STX 的反弹尚不足以证明存储链完成趋势重建。
- `action impact`：`theme_overlap_high` 与 `sleeve_correlation_high` 已触发组合级相关风险复核。GLW/MXL/MRVL/QCOM 按一条有效 sleeve 管理；在 SMH 重回 MA50、相对强度修复且现有复核闭环前，相关新增/摊低维持 **0%**。

## 模型组合净值核对

仅使用已确认工作现金 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 标记；未假设新委托、成交、费用或 FX 变化。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,995.28 |
| 工作 NAV | USD 5,751.77 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.31%；USD 1,995.28 / 34.69% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 888.72 / 15.45% |

现金高于 normal 5% 底线；MRVL 高于 normal 15% 单名上限，因此不加仓并继续完成周度复核。冻结的 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘标记为 **USD 20,196.85**；overlay NAV 与差额留空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-13 收盘行，未预填未来日期。单日价格、replay 或警报不足以升级为稳定规则，故不更新 `memory/decisions.md`。
