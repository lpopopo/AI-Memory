# 2026-07-10 23:18 盘中执行准备

盘中快照，不是正式收盘审计；不得用作 completed-close 触发或正式 NAV。当地 Node `StockService.fetchQuotes` 于 `2026-07-10T15:18:32.798Z` 返回 31/31 个交易自选和市场锚点，均为 `Tencent (Primary)`，无数据缺口；用户券商报价优先。

市场：SPY `752.66 (+0.13%)`，QQQ `722.86 (-0.06%)`，SMH `607.03 (-0.12%)`，SOXX `577.49 (-0.72%)`，RSP `214.42 (+0.43%)`，IWM `295.42 (-0.61%)`。指数平稳但半导体/小盘偏弱；7 月 9 日正式 Fear Gate `normal 2/14` 仅作最近正式参考。

| 标的 | 价格/涨跌 | 主题与 RS/状态 | 持仓相关 | 今日动作 |
|---|---:|---|---|---|
| DRAM | 63.24/-1.74% | 存储/AI-capex；弱，已卖出 | 高 | 暂不碰 |
| MU | 978.86/-1.29% | 存储/AI-capex；弱 | 高 | 暂不碰 |
| WDC | 578.24/+0.03% | 存储/AI-capex；稳定 | 高 | 可观察不追 |
| STX | 915.31/+2.83% | 存储/AI-capex；最强反弹 | 高 | 可观察不追 |
| SNDK | 1885.00/+1.44% | 存储/AI-capex；强、高波动 | 高 | 可观察不追 |
| MRVL | 236.11/-2.92% | 互连/AI-capex；弱 | 高/持仓 | 必须风险处理 |
| AVGO | 399.50/-0.40% | 互连/AI-capex；近似 SMH | 高 | 等待回踩确认 |
| ALAB | 408.78/-2.08% | 互连/AI-capex；弱 | 高 | 暂不碰 |
| COHR | 320.52/-2.06% | 光互连/AI-capex；弱 | 高 | 等待回踩确认 |
| LITE | 778.23/-0.96% | 光互连/AI-capex；略弱 | 高 | 可观察不追 |
| AAOI | 115.97/-5.11% | 光互连/AI-capex；弱 | 高 | 暂不碰 |
| MXL | 90.85/-5.17% | 光互连/AI-capex；异常弱 | 高/持仓 | 必须风险处理 |
| AXTI | 56.11/-10.30% | 光互连/AI-capex；异常下跌 | 高 | 暂不碰 |
| CRDO | 256.38/-3.49% | 互连/AI-capex；弱 | 高 | 暂不碰 |
| SMCI | 28.76/+1.84% | 服务器/AI-capex；相对强 | 高 | 候选但需二次确认 |
| ORCL | 140.75/-2.07% | 云/AI-capex；弱 | 高 | 暂不碰 |
| TER | 355.42/-2.02% | 半导体测试/AI-capex；弱 | 高 | 等待回踩确认 |
| ASML | 1795.39/-0.49% | 设备/AI-capex；近似 SMH | 高 | 可观察不追 |
| AMAT | 597.74/+1.54% | 设备/AI-capex；相对强 | 高 | 等待回踩确认 |
| KLAC | 228.22/-0.57% | 设备/AI-capex；近似 SMH | 高 | 可观察不追 |
| LRCX | 348.44/-1.34% | 设备/AI-capex；弱 | 高 | 可观察不追 |
| RKLB | 80.24/-2.80% | 航天；弱 | 低 | 暂不碰 |
| RDW | 10.13/-3.30% | 航天；弱 | 低 | 暂不碰 |
| TSLA | 407.85/+0.32% | 物理 AI；略强 | 中 | 候选但需二次确认 |
| QCOM | 188.37/-1.43% | 边缘推理；高于 185 | 高/持仓 | 可观察不追 |
| NVDA | 207.61/+2.38% | 算力/AI-capex；强 | 高 | 可观察不追 |
| AMD | 550.14/+0.63% | 算力/AI-capex；较强 | 高 | 可观察不追 |
| INTC | 109.08/-3.07% | 算力/代工；弱 | 高 | 暂不碰 |
| GLW | 188.39/-2.08% | 光网络/AI-capex；弱 | 高/持仓 | 必须风险处理 |
| NOK | 12.36/-4.22% | 网络基础设施；弱 | 中 | 暂不碰 |
| TTMI | 145.33/-3.09% | PCB/AI-capex；弱 | 高 | 暂不碰 |

| Top strength | Top weakness | Unusual movers |
|---|---|---|
| STX +2.83%、NVDA +2.38%、SMCI +1.84%、AMAT +1.54%、SNDK +1.44% | AXTI -10.30%、MXL -5.17%、AAOI -5.11%、NOK -4.22%、CRDO -3.49% | AXTI 深跌，MXL/AAOI 光链走弱；STX/NVDA/AMAT 逆势反弹，均非买点 |

账户风险优先级：MXL 6（超常规卫星规模）、MRVL 4（最大单名）、GLW 2（核心首仓）、QCOM 2（185 观察，completed close <182 复核）。DRAM 已真实卖出。所有 AI 硬件、存储、光互连和设备合并为一个 `ai_capex` 共因子；强反弹只可作减压/观察窗口，非新买信号。

Institutional overlay：`flow_fragility=elevated`；`trend_aligned_entry=mixed/trend_broken`；`AI_quality/capex_cycle=高敏感周期供应链`；`factor_macro_flags=theme_overlap_high,sleeve_correlation_high,momentum_reversal_high`；`bottleneck_watch=存储、光互连、设备`；行动为组合级相关风险复核、零新增。

V9：SMCI、AMAT、TSLA、NVDA、STX、SNDK仅为盘中相对强候选，未验证 70 分、两日完成确认、RS、追高过滤、市场门控或主题上限；其余亦不合格。数据为盘中 partial，V9 不授权买入。
