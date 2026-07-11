# 2026-07-11 V9 回测 2026YTD：SPY / QQQ 收益

用最新 `v9-execution` 引擎回测 `2026-01-02` → `2026-07-10`。
报告：`strategies/v9-execution/results/v9_2026_ytd_spy_qqq_backtest.md`。

## 结果

| 模型 | 累计收益 | 最大回撤 | 资讯买入 |
| --- | ---: | ---: | ---: |
| buy_hold_SPY | 11.09% | -8.88% | 0 |
| buy_hold_QQQ | 18.61% | -11.72% | 0 |
| static_SPY_QQQ_50_50_daily | 14.86% | -10.30% | 0 |
| V8_equivalent_full_core | 10.38% | -7.00% | 0 |
| V9_index_core_70pct_cash_30pct | 7.28% | -4.96% | 0 |
| V9_current_70_30_point_in_time | 7.28% | -4.96% | 0 |

## 结论

- 同期买入持有：SPY **11.09%**，QQQ **18.61%**。
- 最新 V9（point-in-time）：**7.28%**，资讯买入 0 次。
- V8 等价全核心：**10.38%**。
- 若 V9 资讯交易为 0，YTD 收益主要由嵌入式 SPY/QQQ 核心 + 现金缓冲决定，通常低于满仓 QQQ。

不改正式规则；短样本年化指标仅供参考。
