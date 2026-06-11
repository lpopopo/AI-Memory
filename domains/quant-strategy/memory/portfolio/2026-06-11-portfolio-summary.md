# 2026-06-11 Portfolio Summary

范围：真实账户持仓摘要，另附旧模型/回放风险复核。2026-06-10 用户已指示 prior USD 20,000 strategy-tracking model portfolio 退出当前持仓跟踪；当前真实持仓只认用户确认。

## 1. 真实账户

| 项目 | 数值 |
| --- | ---: |
| 真实账户基准 | HKD 20,000 |
| 已确认股票持仓 | MRVL |
| 已确认现金余额 | 未确认 |
| 费用 / FX spread / 税费 | 未确认 |
| 融资 / 保证金 | 不使用 |

| Ticker | 股数 | 成本 | 最新可用快照 | 参考市值 | 未实现盈亏 | 组合占比 | 状态 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | USD 252.00 | USD 266.88，2026-06-09 美股正式收盘 | USD 266.88 | 约 USD +14.88 / +5.90%，未计费用/FX | 成本约 9.8%；参考市值约 10.4%，按 USD/HKD 7.8 粗估 | `core hold / starter defensive review` |

真实账户结论：

- 不新增 MRVL，不追高。
- MRVL official close `<245`：减仓/退出复核。
- MRVL 盘中或收盘靠近 `<235` 且 QQQ/SMH 弱：starter thesis failed，退出/重评。
- 若 MRVL 站回 275-280 且 SMH/QQQ 修复，只能从 defensive review 转为 hold review，不自动加仓。

## 2. 旧模型/回放口径

以下不是当前真实持仓，只用于延续规则复核和 replay：

| Ticker | 历史模型股数 | 2026-06-09 close | 历史模型市值 | 历史模型权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 266.88 | USD 2,145.26 | 10.48% | `core hold / profit-protection review`；禁止追高 |
| AMD | 4.6083 | 475.51 | USD 2,191.29 | 10.71% | `reduce-review`；既有 `<492` 收盘止损仍未修复 |
| WDC | 3.6880 | 517.72 | USD 1,909.35 | 9.33% | `defensive hold / near-stop review` |
| STX | 2.2401 | 846.01 | USD 1,895.15 | 9.26% | `defensive hold / near-stop review`；near-stop priority |

旧模型 2026-06-09 close 估算：股票市值 USD 8,141.05，现金 USD 12,323.96，总资产 USD 20,465.01，现金 60.22%，股票 39.78%。这些数字不作为真实账户资产。

## 3. 数据质量和缺口

- 最新可用正式收盘仍为 2026-06-09；未取得 2026-06-10 正式收盘。
- 外部实时行情连接失败，不能确认盘中价格、正式 VIX close、VIX/VIX3M、HYG/LQD。
- 真实账户现金、FX、费用、旧挂单和可用购买力未确认。
- 旧模型和真实账户必须继续分开，不得把 AMD/WDC/STX 记为真实持仓。
# 08:25 Supplement: 2026-06-10 close / after-hours snapshot

Public StockAnalysis pages later provided a usable 2026-06-10 official close and after-hours snapshot. This supersedes the earlier 2026-06-09 market-data reference for current risk review, while keeping all broker/account fields unconfirmed.

## Real account

| Ticker | Shares | Cost | 2026-06-10 close | Close P/L | After-hours warning | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | USD 252.00 | USD 252.59 | about USD +0.59 / +0.23% before fees/FX | USD 244.55, below 245 but not an official close trigger | starter defensive monitor; no add |

Risk lines remain:
- MRVL official close `<245`: cut-or-wait review.
- MRVL near `<235` with weak QQQ/SMH: starter thesis failed; exit/reassess.
- After-hours below 245 is warning evidence only, not a formal trigger.

## Historical model / replay only

| Ticker | 2026-06-10 close | Old risk line | Replay status |
| --- | ---: | --- | --- |
| AMD | 452.40 | 492 | reduce-review remains active |
| WDC | 490.09 | 500 | reduce-review in historical model/replay scope |
| STX | 815.99 | 835 | reduce-review in historical model/replay scope |

These are not current real holdings unless the user later confirms them from the broker account.

# Formal Post-Close Audit Addendum

Scope: 2026-06-10 U.S. regular-session close, audited during the 2026-06-11 post-close automation.

## Real Account

| Ticker | Shares | Cost | 2026-06-10 close | Close P/L | After-hours warning | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 1 | USD 252.00 | USD 252.59 | about USD +0.59 / +0.23% before fees/FX | USD 244.55, below 245 but not an official close trigger | starter defensive monitor / near-stop review |

No real-account add, sell, cancellation, or broker action is recorded.

## Retired Model Portfolio, Historical Audit Only

| Ticker | Shares | Close | Market value | Weight | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 252.59 | 2,030.39 | 10.11% | reduce-review |
| AMD | 4.6083 | 452.40 | 2,084.79 | 10.39% | reduce-review |
| WDC | 3.6880 | 490.09 | 1,807.45 | 9.00% | reduce-review |
| STX | 2.2401 | 815.99 | 1,827.90 | 9.11% | reduce-review |

| Metric | Value |
| --- | ---: |
| Equity market value | USD 7,750.54 |
| Cash | USD 12,323.96 |
| Total NAV | USD 20,074.50 |
| Cash ratio | 61.39% |
| Equity exposure | 38.61% |
| Holdings count | 4 |
| Theme count | 3 nominal, highly overlapping AI capex chain |
| Largest single-stock weight | AMD 10.39% |
| Cumulative P/L | USD +74.50 / +0.37% |

Risk state: `stress`; new buy exposure `0%`. AMD/WDC/STX are all `reduce-review`. MRVL real position remains above its official close trigger but requires priority review if the next official close confirms the after-hours weakness.
