# 2026-07-07 组合摘要

运行时间：2026-07-08 09:36 Asia/Shanghai。正式收盘估算；未登录券商，真实现金、费用、FX、结算和持仓状态以用户或券商回报为准。

假设：沿用 2026-07-06 working cash `USD 3,884.69`；MU 已按用户确认卖出；GLW/DRAM/MXL/MRVL 尚未收到后续卖出确认；XLI 未计入。

| 持仓 | 股数 | 收盘价 | 市值 | NAV 权重 | 分类 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 185.38 | 370.76 | 6.25% | triggered exit/reduce |
| DRAM | 4 | 60.59 | 242.36 | 4.08% | triggered exit |
| MXL | 6 | 85.82 | 514.92 | 8.68% | triggered reduce/exit |
| MRVL | 4 | 230.70 | 922.80 | 15.55% | triggered exit/reduce-review |

- 估算股票市值：`USD 2,050.84`
- 估算 NAV：`USD 5,935.53`
- 估算现金：`USD 3,884.69 / 65.45%`
- 股票敞口：`34.55%`
- 持仓数：`4`
- 有效大主题数：`1`，全部为 AI-capex 共同因子
- 最大单股：MRVL `15.55%`，高于 normal core 15% 附近且趋势失败

市场与组合判断：Market Fear Gate 正式上调为 `elevated 5/14`，框架风险乘数 `70%`、现金底线 `25%`、框架新买入上限 `25%`。真实账户仍有四个 completed-close stop 未闭环，账户级实际新买入上限为 `0%`。`theme_overlap_high` 与 `sleeve_correlation_high` 继续成立。

退休历史模型/replay 口径：固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金占位 `USD 12,323.96`。按 2026-07-07 收盘估算 NAV `USD 20,372.93`，现金 `60.49%`，股票 `39.51%`。这不是当前真实账户。
