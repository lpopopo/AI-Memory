# 2026-07-28 美股盘后正式审计（延期）

本次自动化于 2026-07-29 00:03 Asia/Shanghai（2026-07-28 12:03 EDT）触发。纽约常规交易仍在进行，故本记录是可追溯的**正式审计延期**，不是 2026-07-28 收盘审计。未登录券商、未提交订单、未假设真实成交；真实账户以用户或券商回报为准。

## 先决资料与行情工作流

已复核策略摘要、稳定决策、日度汇总、近期日记、最新策略建议/执行清单/盘中复盘、最新组合与交易快照，以及 Fear Gate、集中度、每日监控、institutional overlay、AI 质量/资本开支分类、replay 协议与 `tools/README.md` 的 Quote Workflow Smoke Test。

按 README 先运行 Node Smoke Test：`MRVL/AMD/SPY/QQQ/SMH` 均返回结构化 `Tencent (Primary)` quote object；随后扩展请求对 `MRVL/AMD/WDC/STX/SPY/QQQ/SMH/SOXX/RSP/HYG/LQD/IWM/GLW/MXL/QCOM` 也均返回结构化对象。因此本地 quote workflow **可用**，无需降级到 Python 或浏览器。`VIX` 虽返回 `21.67`，但 `open/high/low/volume` 均为零且与当前盘中字段不一致，按陈旧/不可用于本次收盘；`VIX3M` 未返回对象。

## 盘中快照（不得作为收盘）

观察时间：2026-07-28 12:03 EDT；数据源：Node `Tencent (Primary).price`；质量：`intraday only`。成交量在两次请求之间继续递增，进一步确认不能将 `price` 或 `yesterdayClose` 写为本日正式收盘。

| 标的 | 盘中价 | 当日变化 | 备注 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 178.93 / 464.36 | -5.41% / -6.18% | Tencent 结构化盘中对象 |
| WDC / STX | 454.91 / 751.01 | -8.64% / -8.08% | Tencent 结构化盘中对象 |
| SPY / QQQ | 742.01 / 678.50 | +0.40% / -0.53% | Tencent 结构化盘中对象 |
| SMH / SOXX | 534.13 / 496.48 | -2.63% / -3.83% | Tencent 结构化盘中对象 |
| RSP / SPY | 217.58 / 742.01 | +1.11% / +0.40% | 盘中宽度代理；仅观察 |
| HYG / LQD | 79.39 / 106.92 | +0.15% / +0.38% | 盘中信用代理；仅观察 |
| IWM / SPY | 293.06 / 742.01 | +0.05% / +0.40% | 盘中小盘代理；仅观察 |
| VIX / VIX3M | 21.67 / 无对象 | 不适用 | VIX 陈旧，VIX3M 缺失；不计分 |

## 延期边界与既有风险约束

- 不计算 2026-07-28 正式 Fear Gate、风险乘数、现金底线或新买入上限；需要本日已完成收盘和可靠 VIX 数据。
- 不生成本日 stop-trigger table：`AMD <492`、`WDC <500`、`STX <835` 等仅可在 completed close 上判定。盘中 WDC/STX 已低于既有线、AMD 低于既有线，均只作为下一次收盘审计的高优先级复核项，不虚构触发或成交。
- 不重新计算真实账户 NAV、现金比例、股票敞口、持仓/主题数量或最大单股权重；最新已验证模型快照仍是 2026-07-24（NAV USD 5,590.19；现金 67.20%；四项持仓、一项有效 AI-capex 共因子主题）。
- 不填写本日正式 institutional overlay scorecard，也不写 replay ledger。既有 `theme_overlap_high` 与 `sleeve_correlation_high` 约束持续有效：四个持仓按一个相关 AI-capex 篮子看待，新增或摊低仍为 0%。QCOM 的 7/27 长期核心重分类仍有效，旧 `<182` 规则不自动卖出现有两股，且财报前不加仓。
- 不更新 `memory/decisions.md`：单一盘中警报或单一 replay 均不得升级稳定规则。

## 下次执行要求

待 2026-07-28 美股常规交易完成后，使用本地 Node workflow 的已完成收盘字段（或下一交易日盘中时的 `yesterdayClose`）补齐股票/ETF；VIX/VIX3M 必须另取可追溯的完成收盘数据。届时再计算 Fear Gate、stop-trigger table、overlay scorecard、组合 NAV，并且只为已完成日期追加 replay 行。
