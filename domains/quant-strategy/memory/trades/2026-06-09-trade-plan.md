# 2026-06-09 Trade Plan

生成时间：2026-06-09 09:10 Asia/Shanghai。

口径：策略跟踪模拟组合，不是券商真实账户；不得视为已提交或已成交订单。真实成交只以用户或券商成交回报为准。本次是盘中/盘前执行准备，不替代 04:15 美股收盘后正式审计。

## 1. 数据来源与质量

本地资料读取：

- 已读取 `memory/summary.md`、`memory/decisions.md`、`memory/daily-summaries.md`、最近 daily 记录、2026-06-08 每日美股策略报告、`references/realtime-public-source-tracker.md`、最新 portfolio/trades 记录，以及机构 overlay 相关 references。
- 未找到 2026-06-09 当日“每日美股策略建议”报告。
- 未找到 2026-06-09 20:30“实时资讯与机构研究监控”产物；2026-06-08 同类产物也仍缺失。

最新市场数据：

| 标的 | 6/8 收盘 | 6/8 盘后 | 数据时间 | 数据质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 288.85 | 287.35 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于执行准备；盘后流动性较弱 |
| AMD | 490.33 | 489.57 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于止损复核 |
| WDC | 526.93 | 526.59 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于防御持仓复核 |
| STX | 876.77 | 877.50 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于防御持仓复核 |
| SPY | 739.22 | 738.72 | 2026-06-08 16:00 / 20:00 EDT | StockAnalysis，可用于 broad market 方向 |
| QQQ | 716.07 | 715.41 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于 tech 方向 |
| SMH | 598.16 | 597.65 | 2026-06-08 16:00 / 19:59 EDT | StockAnalysis，可用于 semiconductor 方向 |
| VIX | 缺少 2026-06-08 收盘确认 | n/a | 最新可靠本地值仍为 2026-06-05 close 21.51 | 数据缺口；不下调 fear gate |

数据缺口：

- 无真实账户持仓、现金、成交回报、税费、佣金和滑点。
- 无 2026-06-09 当日策略报告和 20:30 实时资讯产物。
- 无 2026-06-08 VIX/VIX3M、HYG/LQD、RSP/SPY 完整确认。
- 未确认 MRVL 旧 315 限价卖单是否仍在真实券商端存在。

## 2. 风险状态与机构 Overlay

执行结论：

- 市场状态：`elevated` 防御复核，不恢复新买入。
- 现金目标：维持约 `55%-65%`，当前模型现金约 `59.21%`。
- 新买入：全部禁止，直到 fear gate 与 trend-aligned entry 同时改善。
- 优先事项：AMD 继续 `reduce-review`；MRVL 不追高；WDC/STX 维持 `defensive hold / near-stop review`。

Institutional overlay scorecard:

- `flow_fragility_score`: `7/14`，`elevated`。理由：AI/半导体/存储在 6/5 同步回撤，6/8 反弹集中在同一拥挤主题，仍缺少宽度和 VIX/信用确认。
- `trend_aligned_entry_score`: `2/5`，`cheap_but_unconfirmed`。fear gate 不允许新增买入，AMD 收盘仍低于止损线，MRVL 未确认 310-315 重新突破，WDC/STX 只是远离硬止损。
- `AI_quality/capex_cycle`: MRVL、AMD、WDC、STX 均为高 capex-cycle 敏感；AMD 为 active reduce-review，MRVL 为 profit-protection bias，WDC/STX 为 defensive hold。
- `factor_macro_flags`: `growth_duration_high; momentum_reversal_high; theme_overlap_high; sleeve_correlation_high; VIX_data_gap`。
- `action impact`: 阻止所有新买入；先处理止损/近止损与旧挂单；只允许观察或撤单/减仓复核，不允许追涨 MRVL。

## 3. 待执行清单

| 股票代码 | 方向 | 数量 | 目标金额 | 组合占比 | 参考价格 | 触发条件 | 止损价 | 失效条件 | 策略理由 | 风险点 | 状态 |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| AMD | 减仓复核 | 等待用户确认；模型建议优先复核卖出 `1.00` 股 | 约 USD 490.33 | 10.86% | 490.33 close / 489.57 AH | 6/8 收盘仍 `<492`，延续 6/5 已触发的收盘止损；若用户确认执行，下一执行窗口按真实行情复核限价/止损单 | 日收盘 `<492` 已触发；若继续弱于 QQQ/SMH，维持 reduce-review | 日收盘重新站上 492 且后续 1-2 个收盘稳定，才可从 reduce-review 降级为 defensive hold | AI compute 相对 memory/storage 偏弱，既有风险线不能忽略 | 卖早可能错过反弹；不卖可能让弱势股拖累组合 | 待用户确认；无真实成交；无模型成交 |
| MRVL | 持有；旧条件单撤单/复核 | 0；若真实账户仍有 315 旧限价卖单，用户需确认是否撤销/修改 | 0 | 11.16% | 288.85 close / 287.35 AH | 不追买；只有重新站上 310-315 且 QQQ/SMH 稳定，才复核小额利润保护；若真实旧单仍在，应优先复核有效性 | 日收盘 `<260` 减仓复核；`<245` gap 失败警告；`<235` 主题止损 | 事件拉升后未确认趋势，禁止追高；若收盘跌回 280 下方且 SMH 转弱，进入更严格防御复核 | S&P 500 纳入支持事件反弹，但价格仍低于旧止盈区，且估值/拥挤风险高 | 指数纳入可能继续挤空，也可能回吐事件溢价 | core hold / profit-protection review；无新订单 |
| WDC | 持有；防御观察 | 0 | 0 | 9.34% | 526.93 close / 526.59 AH | 不加仓；若收盘接近 500 且存储主题继续承压，提前列入 near-stop review | 日收盘 `<500` | 连续收盘重新确认相对强度并远离止损，才可回到普通持有 | 存储主题仍有效，但同主题经历拥挤回撤 | 高 capex-cycle 敏感；若存储板块回落，容易触发相关性风险 | defensive hold / near-stop review；无订单 |
| STX | 持有；防御观察 | 0 | 0 | 9.44% | 876.77 close / 877.50 AH | 不加仓；若收盘接近 835 且 WDC/STX/MU/SNDK 同步转弱，提前复核减弱主题暴露 | 日收盘 `<835` | 连续收盘远离 835 且存储主题恢复相对强度，才可回到普通持有 | 存储主题仍保留，但 STX 高位波动大 | 高位估值和主题相关性；硬止损距离已较 6/5 改善但未解除 | defensive hold / near-stop review；无订单 |
| GLW/MU/SNDK/AVGO/AMAT/KLAC/NVDA/ARM/AI 应用池 | 仅观察 | 0 | 0 | 0 | n/a | 必须等待 fear gate 降级、trend_aligned_entry 达到 `4-5/5`、且不增加第四主题拥挤 | 个股另定 | 今日无效：elevated 风险状态 + 组合已有 3 个主题 | 相关主题强，但组合已表达 AI interconnect/compute/storage | 追涨扩大相关性和 capex-cycle 暴露 | watch only |

## 4. 真实成交、待执行与模型成交区分

- 真实成交：无用户或券商确认的新成交。
- 待用户确认：
  - AMD：是否允许按既有 `<492` 收盘止损规则复核卖出 `1.00` 股。
  - MRVL：真实账户是否仍有 2026-06-04 旧 `315` 限价卖单；若仍存在，是否撤销或改成新的收盘复核规则。
- 模型组合模拟成交：今日不新增。继续沿用 2026-06-02 MRVL 25% 模型减仓和 2026-06-04 MRVL 1.50 股模型减仓。
- 撤单：仅对“可能存在的 MRVL 旧真实挂单”提出用户侧复核；本自动化不登录券商、不撤单、不下单。

## 5. 执行优先级

| 优先级 | 动作 | 标的 | 触发 | 数量 | 备注 |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 用户确认/规则复核 | AMD | 6/8 close 490.33，仍低于 492 | 1.00 股候选 | 只记录待确认，不虚构成交 |
| 2 | 用户确认/撤单复核 | MRVL | 若真实券商端仍有旧 315 限价单 | 旧单数量未知 | 315 旧窗口已经过期，需按新状态复核 |
| 3 | 持有观察 | WDC | 收盘高于 500，但同主题仍 elevated | 0 | 防御持有，不加仓 |
| 4 | 持有观察 | STX | 收盘高于 835，但同主题仍 elevated | 0 | 防御持有，不加仓 |
| 5 | 仅观察 | 新 AI/半导体/存储/应用候选 | 需要 fear gate 和 trend-aligned entry 双确认 | 0 | 今日无新买入 |

## 6. Sources

- StockAnalysis: MRVL, AMD, WDC, STX, SPY, QQQ, SMH pages, observed 2026-06-09 Asia/Shanghai.
- Local memory: 2026-06-08 trade plan, portfolio summary, details, institutional overlay references.
