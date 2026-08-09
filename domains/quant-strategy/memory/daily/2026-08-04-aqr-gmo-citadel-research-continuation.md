# 2026-08-04 AQR / GMO / Citadel Securities 机构研究续查

核验时间：2026-08-04 22:21 Asia/Shanghai。增量起点：`2026-07-31T12:36:44.488Z`。本次只处理 AQR Research、GMO Research Library 和 Citadel Securities Market Insights 的公开页面；不涉及券商账户、私有研究、凭证、订单或真实交易信息。

官方核验入口：[AQR Research](https://www.aqr.com/Insights/Research)、[GMO Research Library](https://www.gmo.com/americas/research-library/)、[Citadel Securities Market Insights](https://www.citadelsecurities.com/news-and-insights/category/market-insights/)。同时读取三家官方 sitemap 以辅助增量筛选；结论仍以可核验详情页为准，不以搜索摘要代替正文。

## 核验状态

| 来源 | 窗口内可核验新增 | 页面核验结论 | 证据强度 |
| --- | ---: | --- | --- |
| AQR Research | 0 | 官方 Research 列表与候选详情页已读取；最新可见候选均早于增量起点。官方 sitemap 无 `lastmod`，因此结论仅覆盖当前列表和已读取候选，不表示站点绝对无变化。 | 中高：官方列表和详情可读；更新时间覆盖不完整。 |
| GMO Research Library | 0 | 官方 Research Library 与 sitemap 已读取；sitemap 在增量窗口内没有新的 `/americas/research-library/` 条目。 | 高：官方 sitemap 可读；动态列表本身不完整展示文章卡片。 |
| Citadel Securities | 2 | 官方 sitemap 给出两篇 2026-08-03 更新；两篇官方域名详情正文均通过只读 Reader 通道读取并核对标题、时间和正文。 | 高：官方域名详情正文可读；策略传导仅为中等证据。 |

## 公开事实

### Citadel Securities: August - After The Reset

- 发布时间：`2026-08-03T21:01:33Z`
- 链接：https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/august-after-the-reset/
- 类型：Global Market Intelligence / 市场结构与资金流观察。
- 文章陈述：7 月出现明显轮动、单股波动和去杠杆；其平台所见零售现金股票成交量较 6 月高点回落，科技、半导体和存储方向出现集中净卖出。
- 文章陈述：杠杆 ETF 资产从 6 月高点减少，科技和半导体杠杆产品降幅更大；半导体在标普 500 中的权重下降，股权融资利差从峰值回落。
- 文章陈述：单股/行业波动仍高而指数波动受低隐含相关性和板块轮动压低；半导体隐含波动仍需进一步正常化。
- 文章陈述：作者认为定位重置后，盈利修正、估值压缩和回购静默期结束可能让基本面与公司需求重新主导市场。
- 证据边界：上述零售流、杠杆 ETF、融资利差和波动数据主要来自 Citadel Securities 平台或其整理，尚未由独立公开点时数据逐项复现。

### Citadel Securities: From Forward Guidance to Market Guidance

- 发布时间：`2026-08-03T21:20:25Z`
- 链接：https://www.citadelsecurities.com/news-and-insights/macro-thoughts/from-forward-guidance-to-market-guidance/
- 类型：Macro Thoughts / 货币政策、AI 扩散与能源通胀观察。
- 文章陈述：减少前瞻指引可能让市场利率替央行完成部分金融条件收紧，但前端政策收紧与长端因通胀、期限溢价和反应函数不确定性上升并不等价。
- 文章陈述：若长端收益率上升压制久期股票、债券对冲同时失效，相关损失可能触发去杠杆，并进一步抬高期限和通胀溢价。
- 文章陈述：限制低成本开放权重模型会提高多次模型调用的代理式应用成本，减慢 AI 扩散；芯片、电力、数据中心建设、许可和地方反对已是现实瓶颈。
- 文章陈述：中东冲突的通胀传导不能只看 Brent，应同时观察柴油、汽油、LPG、炼化利润和产品裂解价差。
- 证据边界：监管、地缘局势及其市场传导是作者分析，不等于政策已经落地或因果关系已经验证。

## 可复用推断

- `flow_to_fundamentals_handoff_v2`：将“技术面重置完成”拆为零售净流、杠杆产品 AUM、融资利差、市场集中度、单股/指数波动差、盈利修正和回购资格比例。只有点时数据与后续价格共同确认，才记录为阶段性 handoff；不能作为买入信号。
- `market_guidance_reflexivity`：长端收益率、久期股票、债股相关性、去杠杆和金融条件可能形成反馈环。该字段归入 `factor_macro_exposure` 与 `flow_fragility`，不能代替 Fear Gate。
- `AI_diffusion_cost_policy`：代理式应用的调用密度使模型单位成本和可获得性成为应用层 ROI 输入；把“前沿能力管制”与“普通应用扩散成本”分开记录。
- `social_license_permitting_bottleneck`：在电力、冷却和互连之外，新增地方许可、社区接受度、建设暂停和并网排队字段，归入 `AI bottleneck watch`。
- `product_complex_inflation_pass_through`：能源冲击观察从原油扩展到成品油、LPG、炼化利润和裂解价差，归入 `factor_macro_exposure`，仅用于解释宏观压力来源。

## 映射到现有规则

| 现有模块 | 本轮映射 |
| --- | --- |
| 市场恐慌门控 | 不变。Citadel 对重置或长端反馈的判断只能作为 context；仍需完成收盘的 VIX/期限结构、广度、信用和趋势输入。 |
| 集中持仓 | 半导体/存储零售卖出、杠杆产品收缩和低指数相关性强化“指数平静不等于 AI-capex 篮子风险低”的复核要求；不自动改变仓位。 |
| AI 基建/应用层观察池 | 基建层补充许可/社区接受度；应用层补充低成本模型可得性、调用密度和单位智能成本。只有订单、部署、收入、毛利或现金流证据才可提升公司级证据。 |
| 机构 overlay | 保留 `flow_to_fundamentals_handoff`、`market_guidance_reflexivity`、`AI_diffusion_cost_policy` 和 `product_complex_inflation_pass_through` 为实验字段。 |
| replay 协议 | 冻结两篇文章首次可见时间；非回填比较 1/5/20/60 日 QQQ/SPY、SMH/QQQ、RSP/SPY、VIX/VIX3M、HYG/LQD、10Y/30Y、盈亏平衡通胀、债股相关性、半导体隐含/实现波动及能源产品价差。平台专有字段缺失时记 `unavailable`。 |
| trend-aligned entry | 即使定位已重置，也需完成收盘的支撑/收复、相对强度和盈利/指引确认；单日反弹、回购窗口或估值压缩均不足以授权入场。 |

## 未核验证据与待办

- Citadel 平台的零售净流、历史排名、杠杆 ETF AUM、融资利差和隐含波动结论，需用可获得的独立点时数据或稳定代理回放。
- “定位已正常化”“基本面重新主导”“结构性牛市未变”均为机构判断，不是公开事实或稳定策略结论。
- AI 模型限制、地方数据中心反对和中东产品通胀路径需与正式政策文本、许可记录、公司披露和公开商品数据交叉核验。
- AQR 与 GMO 本窗口无合格新增，因此不新增框架；这不是对其市场观点的否定。

`decisions.md` 与 `hypotheses.md` 均未更新。本记录只形成研究与 replay 输入，不构成交易建议。
