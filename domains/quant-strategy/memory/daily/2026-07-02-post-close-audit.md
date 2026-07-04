# 2026-07-02 美股盘后正式审计

运行时间：2026-07-03 15:38 Asia/Shanghai / 2026-07-03 03:38 ET。审计对象：2026-07-02 美股常规交易完整收盘。2026-07-03 为独立日观察假期休市，下一常规交易日为 2026-07-06。

## 结论

广义市场恐慌门控为 `normal 4/14`，但这不是允许加仓的信号。半导体与 AI-capex 篮子继续发生与大盘脱钩的同步下跌，`flow_fragility = 11/14 acute`，真实账户五个确认持仓均已跌破既有风险线。组合级覆盖结论：实际新买入上限 `0%`；先处理止损和券商事实核对，不得摊低成本或用事件反弹叙事覆盖价格规则。

本次未登录券商、未提交订单、未推定任何卖出成交。真实现金、费用、FX、XLI 状态及止损成交均以用户/券商回报为准。

## 1. 正式收盘数据与质量

先按 `tools/README.md` 执行本地 Node quote workflow。Tencent 返回结构化 quote objects；随后使用同一客户端传输层读取 Yahoo Chart completed daily bars，以下股票与 ETF 收盘逐项一致。VIX 使用 Cboe 官方日线；Tencent VIX `21.67` 因缺少开高低且价格陈旧而排除。

| 标的 | 2026-07-02 收盘 | 日涨跌 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 245.29 | -9.84% | Tencent + Yahoo completed bar / high |
| AMD | 517.82 | -4.26% | Tencent + Yahoo completed bar / high |
| WDC | 539.00 | -9.92% | Tencent + Yahoo completed bar / high |
| STX | 820.16 | -10.38% | Tencent + Yahoo completed bar / high |
| SPY | 744.78 | -0.13% | Tencent + Yahoo completed bar / high |
| QQQ | 712.60 | -1.73% | Tencent + Yahoo completed bar / high |
| SMH | 592.29 | -4.54% | Tencent + Yahoo completed bar / high |
| SOXX | 566.32 | -5.57% | Tencent + Yahoo completed bar / high |
| VIX | 16.15 | -2.65% | Cboe official daily CSV / high |
| VIX3M | 19.04 | -0.63% | Cboe official daily CSV / high |

补充代理：`VIX/VIX3M = 0.8482`，期限结构正常；`RSP/SPY = 0.28856`，21 日约 `+4.35%`；`HYG/LQD = 0.73371`，21 日约 `+0.02%`；`IWM/SPY = 0.39955`，21 日约 `+4.06%`。来源为 Tencent 收盘对象及 Yahoo completed bars，质量 high。数据抓取时间为 2026-07-03 15:29-15:38 Asia/Shanghai；Cboe 文件：[VIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv)、[VIX3M](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv)。

## 2. 市场恐慌门控

正式评分 `4/14 -> normal`：

- VIX `16.15`：1 分；五日变化约 `-14.51%`：0 分；VIX/VIX3M `0.8482`：0 分。
- SPY 63 日回撤 `-1.95%`：0 分；QQQ `-4.50%`：1 分；SMH `-11.45%`：2 分。
- SPY、QQQ、SMH 均仍高于 MA50 与 MA200：0 分。
- IWM/SPY、RSP/SPY、HYG/LQD 的 21 日变化均未恶化：0 分。

框架参数：风险乘数 `100%`，最大总敞口 `95%`，现金底线 `5%`，框架最大新买入敞口 `50%`。组合级硬覆盖：因五个止损待处理、`flow_fragility acute`、`theme_overlap_high` 与 `sleeve_correlation_high`，实际新买入上限为 `0%`。

## 3. 真实持仓 stop-trigger table

| 持仓 | 股数 | 收盘 | 既有止损/减仓线 | 触发 | near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 196.79 | completed-close trailing stop `227` | 是，低 13.31%；前一日已触发且未确认执行 | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；2026-07-06 开盘前 15 分钟规则优先，成交仍需券商确认 |
| DRAM | 4 | 60.63 | hard protection `70.50` | 是，低 14.00%；前一日已触发 | 否，已深度触发 | `maximum-severity mandatory exit`；禁止摊低成本 |
| MXL | 6 | 93.12 | +40% 利润阈值后的 completed-close trailing stop `113.38` | 是，低 17.87%；前一日已触发 | 否，已深度触发 | `maximum-severity mandatory reduce/exit` |
| MU | 1 | 975.56 | hard reference `1090` / completed-close line `1100` | 是，分别低 10.50% / 11.31%；前一日已触发 | 否，已深度触发 | `maximum-severity mandatory exit/reduce`；不得以高信念例外覆盖 |
| MRVL | 4 | 245.29 | 本次成交计划的 completed-close failure line `260` | 是，低 5.66%；相对成本 263.80 为 -7.02% | 否，已触发 | `mandatory exit at next session open`；禁止加仓、事件反弹追高或下调风险线 |

MRVL 当日用户确认买入 `4 @ 263.80`，总额 `1,055.20`，约占收盘 NAV `17.51%`，超过 normal 单日总新增 `15% NAV` 速度上限；这是执行偏差，不改变真实成交事实，也不产生新的稳定规则。

## 4. MRVL / AMD / WDC / STX 模型 replay 风险表

| 标的 | 收盘 | 既有风险线 | 判定 | 状态 |
| --- | ---: | ---: | --- | --- |
| MRVL | 245.29 | 利润保护/失败线 `260` | 收盘已跌破 | `reduce-review / model exit trigger`；禁止因事件反弹自动追高 |
| AMD | 517.82 | 历史风险线 `492` | 仍高 5.25%，未触发 | `repair/defensive watch`；不保留错误的 active reduce-review，但趋势未修复前不买 |
| WDC | 539.00 | `500` | 未触发，仅高 7.80% | `defensive hold / near-stop review` |
| STX | 820.16 | `835` | 已低 1.78% | `reduce-review / model exit trigger` |

## 5. Institutional overlay scorecard

```text
flow_fragility_score: 11/14 -> acute
  narrow leadership 1; semiconductor/AI concentration and synchronized unwind 2;
  options/crowding proxy 1; systematic/vol-control exposure proxy 2;
  buyback transition risk 1; hedging complacency proxy 2; levered/thematic crowding 2
trend_aligned_entry_score: 1/5 -> trend_broken for AI-capex
  market fear gate permits 1; price trend 0; relative strength 0;
  pullback quality 0; catalyst confirmation 0
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
  optical/interconnect and memory/storage both suffered a second completed-close rejection;
  narrative evidence is not allowed to override stops or price confirmation
action impact:
  block all new buys; treat the entire equity sleeve as one AI-capex basket;
  execute/reconcile stops before any diversification or new setup
```

组合级相关风险复核：五个持仓虽分属光互连、内存与 ETF 子主题，但 `100%` 股票敞口仍是同一 AI-capex 周期风险。MRVL/GLW/MXL 合计约占 NAV `32.08%`，超过单一子主题 `25%` 上限；DRAM/MU 约 `20.21%`。全股票敞口约 `52.29%`，处于 broad-theme `50%-55%` 只能等额强弱轮换的区间，且所有持仓均有硬风险问题，所以不能旋转加仓，只能先降相关风险。

## 6. 组合净值核对

### 6.1 真实账户工作估算

以此前未核实工作现金 `3,930.89` 减去 MRVL 买入总额 `1,055.20`，得到费用前工作现金 `2,875.69`；未假定任何止损卖出。

| 持仓 | 市值 | 权重 | 成本 | 估算未实现盈亏 |
| --- | ---: | ---: | ---: | ---: |
| GLW 2 | 393.58 | 6.53% | 363.00 | +30.58 |
| DRAM 4 | 242.52 | 4.02% | 305.72 | -63.20 |
| MXL 6 | 558.72 | 9.27% | 544.20 | +14.52 |
| MU 1 | 975.56 | 16.19% | 1,155.00 | -179.44 |
| MRVL 4 | 981.16 | 16.28% | 1,055.20 | -74.04 |

- 股票市值：`USD 3,151.54`。
- 估算 NAV：`USD 6,027.23`，相对 `USD 6,410.26` 工作基准约 `-5.98%`。
- 现金：`USD 2,875.69 / 47.71%`；股票敞口：`52.29%`。
- 持仓数：`5`；名义子主题 `2`，有效大主题 `1`（AI capex）。
- 最大单股：MRVL `16.28%`，其次 MU `16.19%`，两者均高于 normal core `15%` 上限，且趋势已破坏。

### 6.2 历史模型组合 / replay

沿用模型股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401` 和现金 `USD 12,323.96`，无虚构模型成交：股票市值 `USD 8,183.06`，模型 NAV `USD 20,507.02`，现金 `60.10%`，股票敞口 `39.90%`，持仓 `4`，最大单股 AMD `11.64%`。`overlay_portfolio_value` 留空，因为协议没有明确历史成交假设。

## 7. 记忆与 replay 处理

- 已向 replay ledger 追加 2026-07-02 completed-close 行，未预填未来日期。
- 已更新 `memory/portfolio/2026-07-02-portfolio-summary.md`、`memory/todos/2026-07-02-strategy-todos.md`、`memory/daily-summaries.md` 与 `memory/summary.md`。
- `decisions.md` 不变：本次是单日急性事件、执行偏差与 replay 观察，不构成经过验证的新稳定规则。

非投资建议。
