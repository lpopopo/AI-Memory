# 新规则回测实验 — README

**路径：** `experiments/2026-06-27-rule-improvement-backtest/`  
**目的：** 验证 2026-06-27 新增的6条稳定规则是否有效降低风险并保持收益

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `run_backtest.py` | 主回测脚本（完整逻辑，直接运行） |
| `backtest_report.md` | 回测报告（运行后自动生成） |
| `README.md` | 本文件 |

---

## 快速开始（AI小弟执行步骤）

### 步骤1：安装依赖
```powershell
pip install pandas numpy yfinance tabulate matplotlib
```

### 步骤2：运行回测
```powershell
cd D:\code\AI-Memory\domains\quant-strategy
python experiments/2026-06-27-rule-improvement-backtest/run_backtest.py
```

### 步骤3：查看报告
```powershell
# 报告生成后自动保存到：
notepad experiments\2026-06-27-rule-improvement-backtest\backtest_report.md
```

---

## 回测逻辑说明

### 比较对象
| 版本 | 说明 |
|------|------|
| **基准版（baseline）** | 完全按实际 2026-06-10 至 2026-06-26 的真实操作序列执行 |
| **改进版（improved）** | 同一操作序列，但在执行前通过规则引擎过滤 |

### 规则引擎检查的规则

| 规则 | 触发条件 | 动作 |
|------|---------|------|
| **规则A** | elevated状态下单日总新增敞口>8pp | 拒绝超额操作 |
| **规则B** | 同日同AI Capex主题新增>5% NAV | 拒绝超额操作 |
| **规则C** | 财报当日或次日买入+10%财报股 | 拒绝，等到T+2 |
| **规则D** | 追踪止损分析（不拦截买入，用于对比分析） | 分析报告中体现 |
| **规则E** | AI Capex总敞口≥55% NAV时新增同主题 | 拒绝 |

### 预期结果

根据 2026-06-25 操作分析，改进版预期：
- **MU 买入（$1155）将被规则C拦截**（T+1 财报日禁止）
- **MXL 买入可能被规则B拦截**（同日同主题第3笔）
- 期末 NAV 在6/26后对比：改进版因未持有MU而NAV更高约+$22-30

---

## 验收标准

回测完成后，以下指标应满足：

| 指标 | 预期 |
|------|------|
| 被拦截操作数量 | ≥ 2 次（MU、可能MXL） |
| 期末 NAV 差异 | 改进版 ≥ 基准版（因MU次日跌6.7%，不买更好） |
| 规则C拦截节省 | 约 $22-75（MU当日浮亏+费用） |
| 规则A/B拦截影响 | 视MXL是否被拦截而定 |

---

## 后续扩展回测计划

完成本次 YTD 验证后，下一步：

1. **BT-V5-Rules**：在 V5 Optimal 20年回测中加入规则过滤层
   - 需要：历史财报日历数据、GICS行业分类
   - 脚本：待创建 `bt_v5_with_rules.py`

2. **BT-TrailingStop-Long**：在26年历史数据上验证追踪止损的长期效果
   - 对比：固定-10%止损 vs 动态追踪止损
   - 预期：追踪止损在趋势行情中显著改善收益

3. **BT-ThemeConcentration**：主题浓度限制的历史回测
   - 模拟：在历史上的行业暴跌日（2022科技崩溃、2020疫情等），
     主题浓度限制是否有效减少损失
