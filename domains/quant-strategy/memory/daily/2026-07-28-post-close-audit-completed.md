# 2026-07-28 美股盘后正式审计（补做完成）

审计于 2026-07-30 02:57 Asia/Shanghai（2026-07-29 14:57 EDT，下一交易日仍盘中）完成。仅使用其 `yesterdayClose` 作为 2026-07-28 的已完成常规交易收盘；没有将 7/29 的盘中 `price` 计入本记录。未登录券商、未提交订单、未假设真实成交；真实账户以用户或券商回报为准。

## 收盘数据、来源与质量

先按 `tools/README.md` 的 Node Quote Workflow Smoke Test 运行 `StockService.fetchQuotes`。MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、RSP、HYG、LQD、IWM、GLW、MXL、QCOM 均返回非空、结构化 `Tencent (Primary)` quote objects；工作流可用，未使用裸 `python.exe`。

运行时美股 7/29 仍在交易，所以下表股票/ETF 严格使用对象的 `yesterdayClose`，即 7/28 completed close，质量为 `medium`（单一但结构化、带来源字段的本地源）。腾讯 VIX 为无可用 OHLC/成交量细节的陈旧 `21.67`，且无 VIX3M 对象，未采用。Google Finance **渲染可见**卡片在 7/29 GMT-5 13:33–13:43 显示 VIX `18.00`、`-0.21 (-1.15%)` 和 VIX3M `19.83`、`-0.030 (-0.15%)`；反推 7/28 close 为 `18.21/19.86`，质量 `medium`，不是跳转 HTML 数据。

| 标的 | 2026-07-28 收盘 | 来源 / 质量 |
| --- | ---: | --- |
| MRVL / AMD | 174.47 / 454.62 | Tencent `yesterdayClose` / medium |
| WDC / STX | 463.51 / 747.30 | Tencent `yesterdayClose` / medium |
| SPY / QQQ | 740.86 / 675.49 | Tencent `yesterdayClose` / medium |
| SMH / SOXX | 529.60 / 491.46 | Tencent `yesterdayClose` / medium |
| VIX / VIX3M | 18.21 / 19.86 | Google browser-visible prior-close inference / medium |
| RSP / SPY | 217.69 / 740.86 | Tencent `yesterdayClose` / medium |
| HYG / LQD | 79.42 / 106.83 | Tencent `yesterdayClose` / medium |
| IWM / SPY | 293.37 / 740.86 | Tencent `yesterdayClose` / medium |

## Market Fear Gate

正式门控为 **elevated 5/14**（保守的代理评分）：VIX 处于 16–22 的 elevated 区间，VIX/VIX3M 约 `0.917`、期限结构正常；但半导体篮子仍弱于广义风险资产，现有 AI-capex sleeve 的趋势与相对强度未修复，且相关风险项没有闭环。框架风险乘数 **70%**、现金底线 **25%**、框架最大新增敞口 **25%**。

账户实际新增/摊低上限仍为 **0%**：四个确认持仓均暴露于一个 AI-capex/半导体共同因子，`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 仍有效，并且弱仓复核未关闭。

## Stop-trigger table

| 标的 | 7/28 收盘 | 既有线 / 约束 | 判定 | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实持仓 2） | 126.01 | 旧短线止损建议未提交，已由长期重分类取代 | 非自动触发 | defensive hold / completed-week reduce-review / no add |
| MXL（真实持仓 6） | 58.94 | 风险线 `78` | **触发** | reduce-review / defensive hold / no add；不得摊低 |
| MRVL（真实持仓 4） | 174.47 | 利润保护与长期底部复核；旧短线单未提交且已被重分类取代 | 风险复核持续 | defensive hold / completed-week reduce-review / no add；事件反弹不追高 |
| QCOM（真实持仓 2） | 162.88 | 旧 `<182` 线已被 7/27 长期核心重分类覆盖 | 非自动卖出 | long-term hold / no add；等待财报及其后两日不创新低、重回约 182 的 completed-close 条件 |
| AMD（历史 replay/watch） | 454.62 | 风险线 `492` | **触发** | reduce-review；非真实持仓或订单推定 |
| WDC（历史 replay/watch） | 463.51 | 风险线 `500` | **触发** | reduce-review / defensive hold；非真实持仓或订单推定 |
| STX（历史 replay/watch） | 747.30 | 风险线 `835` | **触发** | reduce-review / defensive hold；非真实持仓或订单推定 |

MXL 的 completed-close 风险线触发须在下一交易时段由用户/券商确认实际账户事实后处理；本审计不创建、暗示或替代任何真实订单。GLW/MRVL 的旧 stop-market 方案均为 planning-only，不可写作挂单。

## Institutional overlay 与组合级相关风险复核

- `flow_fragility_score`: **5/14, medium（proxy-based）**；直接期权、CTA、杠杆 ETF 流和买回窗口数据未取到，不强行填充。
- `trend_aligned_entry_score`: **1/5, trend_broken**；AI-capex 价格趋势、相对强度与有序回踩确认均不足。
- `AI_quality/capex_cycle`: GLW 为 diversified supplier / medium；QCOM 为 diversified supplier/edge inference / medium-high；MRVL、WDC、STX、AMD 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。
- `factor_macro_flags`: `growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_basket_unwind; unresolved_risk_review`。
- `bottleneck_watch`: optical/interconnect（GLW/MRVL/MXL）与 memory/storage（WDC/STX）同步敏感；本轮无已核验的新订单、收入或价格确认可改变分类。
- `action impact`: 已执行组合级相关风险复核。四项真实持仓名义上是四个代码、但按一个有效 AI-capex sleeve 处理；停止所有相关新增和摊低，优先处理 MXL 风险复核，MRVL 不因事件反弹追高。

## 净值与集中度核对

真实账户工作快照沿用已确认数量和现金：GLW `2`、MXL `6`、MRVL `4`、QCOM `2`；现金 USD `3,756.49`（准确现金仍以券商为准）。

| 指标 | 7/28 结果 |
| --- | ---: |
| 工作 NAV | **USD 5,385.79** |
| 现金 / 股票敞口 | **69.75% / 30.25%** |
| 持仓数 / 有效主题数 | **4 / 1** |
| 最大单股 | MRVL USD 697.88 / **12.96%** |

冻结的历史 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金 USD `12,323.96`）复算为 **USD 19,204.88**。它不是当前真实账户；overlay 没有经过验证的自动成交假设，overlay NAV 与差额保持空白。

## Replay、记忆与边界

已向 replay ledger 追加一行已完成的 2026-07-28 close；未预填未来日期。已新增组合快照、更新日汇总与待办。没有出现经过重复验证的稳定规则，故 **未更新 `memory/decisions.md`**。
