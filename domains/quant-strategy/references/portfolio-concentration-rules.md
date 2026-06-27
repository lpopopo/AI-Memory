# Portfolio Concentration Rules

Purpose: define practical portfolio construction constraints for the USD 20,000 US-stock strategy.

The user prefers a concentrated portfolio rather than holding too many names at once. Daily recommendations should therefore prioritize a small number of high-conviction positions across two or three clear themes.

## Core Rules

- Target active holdings: 4 to 6 stocks.
- Hard maximum active holdings: 8 stocks.
- Target themes at one time: 2 to 3.
- Hard maximum themes at one time: 3.
- Maximum normal single-stock weight: 15%.
- Maximum high-conviction single-stock weight: 20%, only when market fear regime is `normal` and stock-level trend is strong.
- Speculative or lower-quality tactical positions: 3% to 5% maximum.
- Avoid owning multiple names that express the exact same subtheme unless one is a core leader and the other is a small satellite.

## Theme Budgeting

For current AI infrastructure strategy:

- Core theme 1: AI interconnect / optical / custom silicon.
- Core theme 2: memory / storage bottleneck.
- Optional theme 3: AI compute / inference platform.

Example allocation under `normal` fear regime:

- 35% to 45% across 2 to 3 core names.
- 10% to 20% across 1 to 2 satellite names.
- 35% to 55% cash when the leading theme is extended.

## Selection Priority

Daily recommendation ranking should prefer:

1. Strongest theme with confirmed price-volume leadership.
2. One or two best stocks per theme.
3. Better liquidity and cleaner trend over extreme small-cap upside.
4. Lower extension when two names have similar theme quality.
5. Existing position quality over adding a new ticker.

## Recommendation Format

Daily reports should explicitly show:

- Theme count.
- Holdings count.
- Core positions.
- Satellite/speculative positions.
- Names rejected due to overlap or overcrowding.

If more than 6 names qualify, the report must explain why only the top names are selected and place the rest on watchlist.

---

## 2026-06-27 升级：量化浓度硬约束（新增）

以下规则基于 2026-06-22 至 2026-06-27 实盘复盘问题新增，与 `memory/decisions.md` 2026-06-27 节点同步。

### 主题浓度硬上限

- 单一子主题（如"AI HBM存储"：MU + DRAM）总仓位不得超过 NAV **25%**。
- 单一大主题（如"AI Capex"：GLW + TTMI + MXL + DRAM + MU 等）合计不得超过 NAV **55%**。
- 若同一大主题下仓位已达 **40%**，任何来自该主题的新买入申请必须同时减仓等量的同主题既有仓位方可执行。
- 规则以已确认真实持仓计算，不含挂单。

### 同日同主题新增上限

- 同一大主题下，单一交易日内新增仓位（按买入市值计）合计不得超过 NAV **5%**。
- 本规则叠加在单日总加仓速度规则之上，取更严格的一方约束。
- 实际案例（2026-06-25 教训）：DRAM + MXL + MU 同日买入使 AI Capex 主题从 22% 跳至 47%，违反本规则。

### 卫星仓与核心仓规模定义（HKD 50,000 账户适用）

| 分类 | 目标权重 | NAV 金额区间 | 每笔股数参考（$90股） | 止损标准 |
|------|---------|------------|------------------|---------|
| 卫星仓 | 3%-6% | $195-$390 | 约 2-4 股 | 成本价 -12% 至 -15% |
| 核心仓 | 8%-15% | $520-$975 | 约 6-10 股 | 成本价 -8% 至 -10% |
| 高信念核心 | 15%-20% | $975-$1300 | 约 1 股（$1000+价位） | 成本价 -5% 至 -8% |

若某持仓当前市值超出其定义分类的上限：
- 须在下次正式盘后审计时重新定性。
- 止损线须同步调整为新分类对应的标准。

**当前待处理（2026-06-27）：**
- MXL 6股 @$90.70 = $544 = NAV 9.08%：应重新定性为核心仓，止损线从 $86 上移至 $91-92。
