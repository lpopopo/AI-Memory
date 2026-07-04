# 2026-07-02 Strategy Todos

运行时间：2026-07-03 15:38 Asia/Shanghai。依据 2026-07-02 completed close；2026-07-03 休市，下一常规交易日为 2026-07-06。

## Priority 0 — 最大严重度止损待办

1. **GLW**：`196.79 < 227`，已连续第二个 completed close 低于 trailing stop；维持 `maximum-severity mandatory exit/reduce`，不得降级为普通 hold/review。
2. **DRAM**：`60.63 < 70.50`，维持 `maximum-severity mandatory exit`；禁止摊低成本。
3. **MXL**：`93.12 < 113.38`，维持 `maximum-severity mandatory reduce/exit`；不得下调 trailing stop。
4. **MU**：`975.56 < 1090/1100`，维持 `maximum-severity mandatory exit/reduce`；不得使用高信念例外覆盖。
5. **MRVL**：用户确认 `4 @ 263.80` 后正式收盘 `245.29 < 260`；按成交计划为 `mandatory exit at next session open`。禁止加仓、摊低成本、事件反弹追高或下调风险线。
6. 上述真实成交只以用户/券商回报记录。本自动化未登录券商、未提交订单、未虚构卖出成交。

## Priority 0 — 券商事实核对

7. 核对 GLW、DRAM、MXL、MU 是否已有券商止损成交，以及 MRVL 下一交易日执行结果；同时核对精确现金、费用、FX 和结算。
8. 核对 XLI 旧计划 `2 @ 183` 的状态：`never placed / cancelled / open / filled`。未确认前不计入持仓或现金。

## Priority 1 — 组合控制

9. 实际新买入上限保持 `0%`，直到所有已触发风险项完成并取得用户/券商确认。
10. 当前股票敞口 `52.29%` 全部属于同一 AI-capex 大主题；MRVL/GLW/MXL 光互连子主题约 `32.08%`，超过 `25%` 上限。不得用新增相关标的做“分散”。
11. MRVL 当日新增 `USD 1,055.20`，约为收盘 NAV `17.51%`，超过 normal 单日 `15% NAV` 速度上限；记录为执行偏差，后续复盘但不直接升级稳定规则。

## Priority 2 — replay / watch

12. 模型 MRVL `245.29 < 260` 与 STX `820.16 < 835` 均为 reduce-review / model exit trigger；WDC `539` 为 defensive near-stop review；AMD `517.82 > 492`，不标错误的 active reduce-review，但维持 repair/defensive watch。
13. 继续记录 2026-07-02 AI-capex 同步回撤 replay；不得预填未来行，不得虚构 overlay 成交。
14. `decisions.md` 不变，等待跨日/历史 replay 验证后再考虑稳定规则调整。
