# 2026-06-26 美股盘后正式审计

运行时间：2026-06-27 08:24 Asia/Shanghai。  
审计对象：2026-06-26 美股常规交易收盘。真实账户只采用用户或券商已确认持仓；本次未登录券商、未提交订单、未推断任何新成交。

## 1. 结论

- Market Fear Gate：`elevated 6/14`；风险乘数 `70%`，最大总敞口 `75%`，框架新买入上限 `25%`，现金底线 `25%`。
- 操作覆盖：当前 `flow_fragility=10/14 elevated`，且 `theme_overlap_high`、`sleeve_correlation_high`；因此相关 AI/半导体/存储新增仓位的实际操作上限为 `0%`，先做组合级相关风险复核。
- 真实账户：估算 NAV `USD 6,384.66`，现金 `USD 3,368.64`（`52.76%`），股票 `USD 3,016.02`（`47.24%`），5 个持仓、2 个高度重叠主题，最大单股 MU `17.74%`。
- 正式触发：TTMI 收盘 `191.49 < 200`，进入 `reduce-review / near-stop`；但仍高于 `188` 完成收盘硬线，未触发强制退出。DRAM、MU 接近风险线；GLW、MXL 未触发。
- 历史 replay：AMD `521.58 > 492`，不属于 reduce-review；WDC `586.45 > 500`，STX `899.90 > 835`，但均处于同步深跌后的 defensive review；MRVL `266.77 > 260` 且 `<285`，只做利润保护/禁止追高复核。

## 2. 正式收盘数据与质量

本地行情工作流按 `tools/README.md` 先运行。Node `StockService.fetchQuotes` 返回结构化 `Tencent (Primary)` quote objects；随后以同一客户端的 Yahoo Chart 日线复核正式收盘。Tencent 原始字段时间多数为 `2026-06-26 16:00:00-02 ET`，Yahoo 日线日期为 `2026-06-26`，两者收盘一致。Node 路径成功，因此未使用 Python 或 Google fallback。

| 标的 | 正式收盘 | 日涨跌 | 来源 / 时间 | 质量 |
| --- | ---: | ---: | --- | --- |
| MRVL | 266.77 | -5.15% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| AMD | 521.58 | -2.06% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| WDC | 586.45 | -13.17% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| STX | 899.90 | -12.24% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| SPY | 728.99 | -0.72% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| QQQ | 706.52 | -1.38% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| SMH | 611.61 | -3.97% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| SOXX | 589.94 | -5.64% | Tencent + Yahoo Chart，16:00 ET | 高；双源一致 |
| VIX | 18.41 | -2.54% | Yahoo Chart 完成日线，16:15 ET | 中高；Cboe CSV 本次运行时尚缺 6/26 行 |
| VIX3M | 20.13 | -0.98% | Cboe 官方 CSV；Yahoo Chart 一致 | 高；官方收盘 |

补充代理：`VIX/VIX3M=0.915`；`RSP/SPY=0.28850`，21 日 `+4.34%`；`IWM/SPY=0.41130`，21 日 `+6.30%`；`HYG/LQD=0.72904`，21 日 `-0.89%`。代理来自 Yahoo Chart 2026-06-26 完成日线，质量高。宽度与信用未确认市场级恐慌，压力集中在半导体/AI capex 篮子。

## 3. 市场恐慌门控

| 信号 | 读数 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 18.41，处于 16-22 elevated 区间 | 1 |
| VIX 5 日变化 | 16.40 -> 18.41，`+12.26%`，未达 +15% | 0 |
| VIX 期限结构 | 0.915，正常 contango | 0 |
| SPY 63 日回撤 / 50DMA | `-4.03%`；728.99 < 734.35 | 2 |
| QQQ 63 日回撤 / 50DMA | `-5.31%`；706.52 > 702.79 | 1 |
| SMH 63 日回撤 / 50DMA | `-8.57%`；611.61 > 566.44 | 2 |
| 宽度 / 信用 21 日恶化 | RSP/SPY、IWM/SPY改善；HYG/LQD仅 -0.89% | 0 |
| **合计** | **elevated** | **6/14** |

风险参数：`risk_multiplier=70%`、`cash_floor=25%`、`max_gross_exposure=75%`、`max_new_buy_exposure=25%`。组合现金满足底线，但相关主题覆盖规则把 AI/半导体/存储的新买入降为 `0%`。

## 4. 活跃持仓 stop-trigger table

| 持仓 | 股数 | 收盘 | 既有止损 / 减仓线 | 触发 | Near-stop | 下一步状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| GLW | 2 | 221.05 | 收盘 `<210` 利润保护；硬失败 `<180` | 否 | 否，距 210 `+5.26%` | `hold / profit-protection`；不加仓 |
| TTMI | 3 | 191.49 | 收盘 `<200` reduce review；`<188` exit review | **触发 200 线** | **是**，距 188 `+1.86%`；盘中低 187.10 但硬线为完成收盘 | `reduce-review / defensive near-stop`；下次开盘前优先复核，不摊低成本 |
| DRAM | 4 | 71.88 | 盘中保护线 `70.50` | 否；日低 71.33 | **是**，收盘距线 `+1.96%`、日低距线 `+1.18%` | `defensive hold / near-stop review`；确认券商保护单状态 |
| MXL | 6 | 96.60 | 风险线 `86.00` | 否 | 否，距线 `+12.33%` | `satellite hold / protect`；禁止追加 |
| MU | 1 | 1132.33 | 收盘线 `1100`；建议硬保护参考 `1090` | 否 | **是**，距 1100 `+2.94%` | `core defensive hold / near-stop`；禁止追加 |

上述状态不是实际订单或成交。真实持仓、现金、保护单与成交只以用户/券商回报为准。

## 5. 历史 replay 风险线复核

| 标的 | 收盘 | 历史线 | 判定 |
| --- | ---: | ---: | --- |
| MRVL | 266.77 | 利润保护 260；重入确认 285 | 未破 260，但仅高 2.60%；`profit-protection review / watch only`，事件反弹不得追高 |
| AMD | 521.58 | 风险线 492 | 高于 492；不标 reduce-review，维持 historical watch |
| WDC | 586.45 | 硬线 500 | 高于硬线，但单日 -13.17%、低于 20DMA 602.54；`defensive hold review` |
| STX | 899.90 | 硬线 835 | 高于硬线 7.77%，单日 -12.24%、低于 20DMA 950.86；`near-stop / defensive review` |

## 6. Institutional overlay scorecard

```text
flow_fragility_score: 10/14 -> elevated（proxy-based；options/CTA/buyback 直接数据缺失）
flow_fragility_state: elevated / near-acute
trend_aligned_entry_score: 1/5 -> trend_broken for new correlated-theme entries
AI_quality/capex_cycle:
  GLW: diversified_supplier / bottleneck, provisional 8/10, medium sensitivity
  TTMI: infrastructure_supplier / PCB-interconnect, provisional 6/10, medium-high sensitivity
  DRAM: thematic_etf / memory-storage basket, provisional 5/10, high sensitivity
  MXL: speculative_bottleneck / optical component, provisional 4/10, high sensitivity
  MU: cyclical_supplier / HBM-memory leader, provisional 7/10, high sensitivity
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high;
  sleeve_correlation_high; AI_capex_cycle_high; memory_concentration_high;
  semiconductor_basket_unwind
bottleneck_watch: optical/interconnect、HBM/memory 成本与上游扩产仍仅是研究字段，非买入信号
action impact: block all new correlated adds; run portfolio-level review; prioritize TTMI reduce-review;
  keep DRAM/MU near-stop review and protect GLW/MXL
```

组合级复核：GLW + TTMI + MXL 的 optical/interconnect 暴露为 `USD 1,596.17` / NAV `25.00%`；MU + DRAM 的 memory 暴露为 `USD 1,419.85` / `22.24%`。全部股票敞口 `47.24%` 实质上属于同一 AI capex 链，跨股票分散不足。现金充足不能成为继续加仓理由。

## 7. 组合净值核对

### 真实账户估算

| 指标 | 数值 |
| --- | ---: |
| 工作现金 | USD 3,368.64 |
| 股票市值 | USD 3,016.02 |
| 估算 NAV | USD 6,384.66 |
| 相对 USD 6,410.26 基线 | -USD 25.60 / -0.40% |
| 现金 / 股票敞口 | 52.76% / 47.24% |
| 持仓 / 主题数 | 5 / 2（高度相关） |
| 最大单股 | MU，17.74% |

### 已退休历史模型 / replay 核对

该模型不属于当前真实持仓。沿用 replay 固定持仓 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401` 与现金 `USD 12,323.96`：股票市值 `USD 8,726.67`，模型净值 `USD 21,050.63`，现金 `58.55%`、股票 `41.45%`，4 个持仓，最大单股 AMD 约 `11.42%`。本日无模型成交假设。

## 8. Replay 与记忆处理

- 已向 replay ledger 追加 2026-06-26 完成收盘行；未预填未来日期。
- 已更新正式组合快照、daily summaries 与 todos。
- 本次是单日警报 / replay 观察，不更新 `decisions.md`。

不构成投资建议。
