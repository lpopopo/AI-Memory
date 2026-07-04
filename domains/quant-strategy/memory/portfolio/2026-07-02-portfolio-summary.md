# 2026-07-02 正式收盘组合摘要

审计对象：2026-07-02 美股常规交易收盘。运行时间：2026-07-03 15:38 Asia/Shanghai。价格由本地 Node workflow 的 Tencent 结构化 quote objects 获取，并由 Yahoo completed daily bars 交叉确认；VIX/VIX3M 使用 Cboe 官方日线。

## 真实账户工作估算

确认持仓口径：GLW `2`、DRAM `4`、MXL `6`、MU `1`、MRVL `4`。TTMI 已确认清仓；XLI 状态仍未知且未计入。费用前工作现金为 `USD 2,875.69`，未假定任何止损已成交。

| 持仓 | 收盘 | 市值 | 权重 | 正式状态 |
| --- | ---: | ---: | ---: | --- |
| GLW 2 | 196.79 | 393.58 | 6.53% | `<227`，maximum-severity mandatory exit/reduce |
| DRAM 4 | 60.63 | 242.52 | 4.02% | `<70.50`，maximum-severity mandatory exit |
| MXL 6 | 93.12 | 558.72 | 9.27% | `<113.38` trailing stop，maximum-severity mandatory reduce/exit |
| MU 1 | 975.56 | 975.56 | 16.19% | `<1090/1100`，maximum-severity mandatory exit/reduce |
| MRVL 4 | 245.29 | 981.16 | 16.28% | `<260` completed-close failure，next-session-open exit trigger |

- 估算 NAV：`USD 6,027.23`。
- 现金：`USD 2,875.69 / 47.71%`。
- 股票敞口：`USD 3,151.54 / 52.29%`。
- 持仓数：`5`；名义子主题 `2`，有效大主题 `1`（AI capex）。
- 最大单股：MRVL `16.28%`；MU `16.19%`。
- 光互连/互连子主题约 `32.08%`，超过 `25%` 子主题上限；整个股票袖套 `100%` 属于同一高相关 AI-capex 篮子。

## 历史模型核对

历史模型无新增模拟成交：NAV `USD 20,507.02`，现金 `60.10%`，股票敞口 `39.90%`，持仓 `4`，最大单股 AMD `11.64%`。仅用于 replay，不代表真实账户。

真实现金、费用、FX、XLI 状态和任何止损成交均以用户/券商回报为准。
