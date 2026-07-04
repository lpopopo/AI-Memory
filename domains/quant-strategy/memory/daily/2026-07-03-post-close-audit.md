# 2026-07-03 美股盘后正式审计（休市）

运行时间：2026-07-04 05:57 Asia/Shanghai / 2026-07-03 17:57 ET。审计对象：2026-07-03 美股时段。NYSE 与 Nasdaq 因美国独立日补休而全天休市，因此不存在 2026-07-03 常规交易收盘价、日内触发或新的模型净值变动；本报告正式携带最近有效的 2026-07-02 已审计收盘。

## 结论

市场恐慌门控维持 `normal 4/14`，风险乘数 `100%`、框架现金底线 `5%`、框架新买入上限 `50%`。但五个真实账户工作持仓均已在最近有效收盘跌破既有风险线，且 `flow_fragility=11/14 acute`、`theme_overlap_high`、`sleeve_correlation_high`，所以组合级覆盖后的实际新买入上限仍为 `0%`。不得因休市、事件反弹预期或宽基门控正常而延后止损、摊低成本或追高 MRVL。

本次未登录券商、未提交订单、未虚构成交。真实持仓、现金、费用、FX、XLI 状态及止损成交均以用户或券商回报为准。

## 1. 正式收盘数据、来源与质量

先按 `tools/README.md` 执行本地 Node Quote Workflow Smoke Test。2026-07-04 05:57 Asia/Shanghai 抓取时，Tencent 返回结构化 quote objects；因 7 月 3 日休市，这些对象仍对应 2026-07-02 完整 OHLC/成交量。它们与既有 Yahoo completed daily bars 一致。VIX/VIX3M 由 Cboe 官方日线 CSV 再核验；Tencent VIX `21.67` 因无开高低、昨收等于现值且明显陈旧而排除。

| 标的 | 最近有效收盘（2026-07-02） | 日涨跌 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 245.29 | -9.84% | Tencent structured object + Yahoo completed bar / high |
| AMD | 517.82 | -4.26% | Tencent structured object + Yahoo completed bar / high |
| WDC | 539.00 | -9.92% | Tencent structured object + Yahoo completed bar / high |
| STX | 820.16 | -10.38% | Tencent structured object + Yahoo completed bar / high |
| SPY | 744.78 | -0.13% | Tencent structured object + Yahoo completed bar / high |
| QQQ | 712.60 | -1.73% | Tencent structured object + Yahoo completed bar / high |
| SMH | 592.29 | -4.54% | Tencent structured object + Yahoo completed bar / high |
| SOXX | 566.32 | -5.57% | Tencent structured object + Yahoo completed bar / high |
| VIX | 16.15 | -2.65% | Cboe official daily CSV / high |
| VIX3M | 19.04 | -0.63% | Cboe official daily CSV / high |

补充代理同样携带 2026-07-02 正式审计值：`VIX/VIX3M=0.8482`；`RSP/SPY=0.28856`，21 日约 `+4.35%`；`HYG/LQD=0.73371`，21 日约 `+0.02%`；`IWM/SPY=0.39955`，21 日约 `+4.06%`。数据质量为 high。NYSE 与 Nasdaq 官方日历均确认 2026-07-03 休市；因此没有可追加的 7 月 3 日行情行。

## 2. 市场恐慌门控

无新交易日，正式门控维持 2026-07-02 的 `4/14 -> normal`：

- VIX `16.15`、五日变化约 `-14.51%`、VIX/VIX3M `0.8482`：0 分。
- SPY/QQQ/SMH 63 日回撤约 `-1.95%/-4.50%/-11.45%`：4 分。
- 三者仍高于 MA50/MA200：0 分。
- IWM/SPY、RSP/SPY、HYG/LQD 的 21 日变化未达到恶化阈值：0 分。

框架参数：风险乘数 `100%`、最大总敞口 `95%`、现金底线 `5%`、最大新买入敞口 `50%`。组合硬覆盖：实际新买入上限 `0%`，直至所有已触发风险项及券商事实完成核对。

## 3. 真实持仓 stop-trigger table

| 持仓 | 股数 | 收盘 | 既有止损/减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 196.79 | completed-close trailing stop `227` | 是，低 13.31% | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；若仍持有，下一可交易日开盘前 15 分钟规则优先 |
| DRAM | 4 | 60.63 | hard protection `70.50` | 是，低 14.00% | 否，已深度触发 | `maximum-severity mandatory exit`；禁止摊低成本 |
| MXL | 6 | 93.12 | monotonic trailing stop `113.38` | 是，低 17.87% | 否，已深度触发 | `maximum-severity mandatory reduce/exit` |
| MU | 1 | 975.56 | hard reference `1090` / close line `1100` | 是，低 10.50% / 11.31% | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；不得用高信念例外覆盖 |
| MRVL | 4 | 245.29 | completed-close failure line `260` | 是，低 5.66%；相对成本 263.80 为 -7.02% | 否，已触发 | `mandatory exit at next session open`；禁止加仓、追事件反弹或下调风险线 |

休市不产生新触发，也不清除 7 月 2 日已触发状态。所有卖出仍需用户/券商确认后才能记为真实成交。

## 4. MRVL / AMD / WDC / STX replay 风险复核

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| MRVL | 245.29 | `260` | 已跌破 | `reduce-review / model exit trigger`；禁止事件反弹自动追高 |
| AMD | 517.82 | `492` | 高 5.25%，未触发 | `repair/defensive watch`；不标为 active reduce-review，但趋势修复前不买 |
| WDC | 539.00 | `500` | 高 7.80%，未触发 | `defensive hold / near-stop review` |
| STX | 820.16 | `835` | 低 1.78%，已触发 | `reduce-review / model exit trigger` |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 11/14 -> acute
trend_aligned_entry_score: 1/5 -> trend_broken for AI-capex
AI_quality/capex_cycle:
  GLW diversified supplier / medium sensitivity / about 7/10;
  MRVL cyclical supplier + bottleneck / high sensitivity / about 6/10;
  MXL speculative bottleneck / high sensitivity / about 4/10;
  MU cyclical supplier / high sensitivity / about 6/10;
  DRAM thematic memory basket / high sensitivity / about 5/10
factor_macro_flags:
  theme_overlap_high; sleeve_correlation_high; momentum_reversal_high;
  growth_duration_high; AI_capex_cycle_high; semiconductor_basket_unwind
bottleneck_watch:
  optical/interconnect and memory/storage remain price-rejected;
  no new session or evidence can override the completed-close stops
action impact:
  block all new buys; treat the whole equity sleeve as one AI-capex basket;
  reconcile and execute stops before diversification or re-entry
```

组合级相关风险复核：五个持仓虽分属光互连、内存与 ETF 子主题，但 `100%` 股票敞口仍是同一 AI-capex 周期风险。MRVL/GLW/MXL 合计约占 NAV `32.08%`，超过单一子主题 `25%` 上限；全股票敞口为 `52.29%`，且每个持仓均有硬风险问题。因此只能先降相关风险，不能用新增相关标的伪装分散。

## 6. 组合净值核对

假设 GLW `2`、DRAM `4`、MXL `6`、MU `1`、MRVL `4` 均未收到后续成交回报，且 XLI 未计入：

- 股票市值：`USD 3,151.54`。
- 工作现金：`USD 2,875.69`，占 `47.71%`。
- 估算 NAV：`USD 6,027.23`；股票敞口 `52.29%`。
- 持仓数 `5`；名义子主题 `2`；有效大主题 `1`（AI capex）。
- 最大单股为 MRVL `16.28%`，其次 MU `16.19%`；均高于 normal core `15%` 上限且趋势已破坏。

历史模型无新交易日、无新模拟成交：NAV 维持 `USD 20,507.02`，现金 `60.10%`、股票敞口 `39.90%`、持仓 `4`、最大单股 AMD `11.64%`。`overlay_portfolio_value` 继续留空，因为协议没有明确历史成交假设。

## 7. 记忆与 replay 处理

- 不向 replay ledger 追加 2026-07-03 行；该日无完成收盘，且 2026-07-02 行已经存在，禁止重复或预填未来日期。
- 更新 2026-07-03 组合摘要与待办，保留五项止损及 XLI/券商事实核对。
- `decisions.md` 不变：休市携带与单日警报不构成新的稳定规则。

非投资建议。
