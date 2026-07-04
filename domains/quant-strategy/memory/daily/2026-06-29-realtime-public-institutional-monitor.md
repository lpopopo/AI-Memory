# 2026-06-29 实时公开来源与机构研究监控

## 运行边界

- 运行时间：2026-06-29 21:30-22:12（北京时间）。
- 严格窗口：`2026-06-26T13:59:00.000Z` 至本次核验结束。该起点来自自动化记忆中最近一次成功落盘，不把 2026-06-29 21:14 的检查器中间产物误当作成功运行。
- 范围：仅公开可见、只读核验；未读取 cookies、密码、本地存储、私信、通知或账号设置；未关注、点赞、评论、转发、发帖、登录券商或提交订单。
- 本报告不生成直接买卖建议，不记录或推断未确认成交。

## 结论摘要

### 公开事实

1. 小红书出现一篇新非置顶 Cerebras 深度笔记，ID `6a41e1fd00000000170095e6`。页面显示“编辑于 7 小时前 美国”、正文和作者置顶评论；轮播共 `26` 张，浏览器已逐张经过并加载出 `26` 个原图资源，其中 `24` 张成功导出复核，`2` 张原图下载失败。
2. `@Kay2289123` 严格窗口内至少有四条高相关可见帖子：内存墙、多层替代路径、Optical HBM、Google/Meta 算力配额，以及三星/SK 海力士扩产的二次评论。
3. `@nvidia` 严格窗口内可见新内容包括 Nemotron 3 Ultra 的第三方任务榜单转发、Zaha Hadid 本地计算/微调/OpenUSD 案例，以及本次运行时刚发布的 NPS/DGX/Omniverse 教育与合成数据案例。
4. `@elonmusk` 可见一条 Grok 栈将用 C/C++ 简化并针对 GB300 精确映射的原帖，以及一条 Starlink 新西兰农村宽带份额转述；其余窗口内容主要是政治/文化评论或转发。
5. `@realDonaldTrump` 主页可读，但可见最新内容仍为 2026-06-21 及更早；严格窗口内可核验项目为 `0`。
6. AQR、Citadel Securities、GMO、Man Institute 列表页与候选详情均可读；四家严格窗口内 `post_window_verified=0`，因此不提炼新机构框架。

### 我的推断

- Cerebras 不是“替代全部 GPU”的单一叙事，更适合拆成 `decoder_latency_specialist`：低延迟、长 Agent 工具链和实时任务可能有真实价值，但单芯片 SRAM 容量、集群扩展、并发吞吐、良率、生态、客户集中和利润分成决定其商业质量。
- “内存墙”来源把 HBF、CXL、预测分层、SRAM 推理芯片和 Optical HBM 放进同一替代集合。它们更可能是互补路线而非单一赢家；必须比较端到端延迟、容量、功耗、软件改造、可靠性与总拥有成本。
- Google/Meta 算力配额与 NVIDIA 本地/定制案例共同支持“算力稀缺与工作负载专用化并存”，但不证明 neocloud、光互连或任一芯片公司的收入会自动兑现。
- 三星/SK 海力士扩产同时提高上游设备/材料需求与中期供给过剩风险，应纳入 `capex_cycle` 双向检查，而不是只读作利好。

## 已核验公开源项目

| 平台/来源 | 账号 | ID / 可见时间（北京时间） | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 | `6a41e1fd00000000170095e6`；编辑于约 7 小时前 | https://www.xiaohongshu.com/explore/6a41e1fd00000000170095e6 | 长文轮播 | 正文区分 prefill/decoder，描述 WSE-3、片上 SRAM 和低延迟推理；作者置顶评论说明文章修改后重新上线 | Cerebras 是长链 Agent/实时任务的“法拉利”，技术方向成立但最快不等于最好生意 | `AI bottleneck watch`、`AI_quality/capex_cycle`、`replay/backtest plan` | 高：标题/正文/相对时间/作者评论；图片 `24/26` 可导出复核，2 张缺口；技术与财务断言中等 | 官方财报/招股材料、客户与收入集中、良率、44GB/集群扩展、并发吞吐、毛利/OCF-CapEx、与 Groq/NVDA 的可比基准 |
| X | `@Kay2289123` | `2071359522791473185`；2026-06-29 06:26 | https://x.com/Kay2289123/status/2071359522791473185 | 原帖 | 将 HBF、CXL、预测分层、SRAM 推理列为内存墙路径 | 内存短缺是结构性墙，重点应从价格周期转向“少用 DRAM”的新标准 | `AI bottleneck watch`、`theme crowding` | 高：状态页/作者/ID/时间/正文可见；产业断言中等 | HBM 晶圆占用、2027 wafer-start 比例、各路线量产/采用/TCO |
| X | `@Kay2289123` | `2071423413944734166`；2026-06-29 10:40 | https://x.com/Kay2289123/status/2071423413944734166 | 原帖+图片 | 提出 Optical HBM：以光互连把远端内存拉回计算侧 | Optical HBM 可能重分配 MRVL/MU 等角色 | `AI bottleneck watch`、`portfolio concentration` | 中高：可见帖事实高；架构与受益映射中等偏低 | 标准、光 I/O/封装路线、延迟/功耗/可靠性、厂商订单与收入 |
| X | `@Kay2289123` | `2071479718315168032`；2026-06-29 14:23 | https://x.com/Kay2289123/status/2071479718315168032 | 原帖+FT 引用 | 可见引用称 Google 限制 Meta 使用 Gemini 模型的算力 | 已锁定算力的 ORCL/CRWV/NBIS 只获益“一半”，稀缺也会推动替代与议价 | `flow_fragility`、`AI_quality/capex_cycle` | 高：帖与引用可见；商业传导中等 | FT 原文、配额性质/持续期、外部算力订单、利用率、融资与毛利 |
| X | `@Kay2289123` | `2071488648776958136`；2026-06-29 14:59 | https://x.com/Kay2289123/status/2071488648776958136 | 原帖+图片 | 继续评论三星/SK 海力士十年扩产新闻 | 新闻发酵不改变需同时看扩产受益与周期风险 | `capex_cycle`、`theme crowding` | 中高：帖子可见；扩产金额/项目需官方核验 | 两家公司官方 capex、建设节奏、WFE 订单、供给释放与价格反应 |
| X | `@nvidia` | `2070602795737035252`；2026-06-27 04:19 | https://x.com/NVIDIAAI/status/2070602795737035252 | 官方相关账号转发 | NVIDIA 主账号转发 NVIDIA AI：Nemotron 3 Ultra 在 AA-Briefcase 长任务榜单表现靠前 | 推广开放模型在真实复杂 Agent 项目中的能力 | `AI_quality/capex_cycle` | 中高：官方转发与正文可见；第三方榜单需复核 | 榜单方法、成本/延迟、可复现性、真实采用与收入 |
| X | `@nvidia` | `2070597978826449174`；2026-06-27 04:00 | https://x.com/nvidia/status/2070597978826449174 | 官方原帖 | Zaha Hadid 使用本地计算、微调模型和 NVIDIA/OpenUSD 工具 | 定制、本地部署可加速设计并保护专有数据 | `AI_quality/capex_cycle`、`factor_macro_exposure` | 高：官方帖事实；投资传导中等 | 部署规模、硬件/软件收入、单位经济与可复制性 |
| X | `@nvidia` | `2071594539500921283`；2026-06-29 22:00 | https://x.com/nvidia/status/2071594539500921283 | 官方原帖 | NPS/DGX/Omniverse 用于合成数据、定制基础模型和学生应用 | 教育/研究 AI 基础设施继续扩展 | `AI bottleneck watch` | 高：官方帖；需求规模中等偏低 | 项目金额、GPU 数量、持续采购与外部可复制性 |
| X | `@elonmusk` | `2071385784154759468`；2026-06-29 08:10 | https://x.com/elonmusk/status/2071385784154759468 | 原帖/回复 | 称约三个月内训练/推理栈将以 C/C++ 简化并针对 GB300 精确映射 | 软件层删除和软硬协同将带来大幅性能提升 | `AI_quality/capex_cycle`、`AI bottleneck watch` | 高：原帖可见；时间表/收益未核验 | 三个月交付、基准、吞吐/成本、GB300 供给、软件稳定性 |
| X | `@elonmusk` | `2071550422079177070`；2026-06-29 19:04 | https://x.com/elonmusk/status/2071550422079177070 | 原帖+第三方引用 | 转述 Starlink 新西兰农村宽带份额 27%、连接数增长 | Starlink 农村市场渗透扩大 | `factor_macro_exposure`、卫星观察池 | 中：原帖/引用可见；数字来自第三方账户 | 新西兰官方/公司数据、ARPU、终端补贴、盈利能力 |

未纳入策略项目：Elon 的政治/文化帖子与转发；Trump 的窗口外旧帖；NVIDIA 的同主题链接补充帖不重复计数。

## 机构研究核验

检查器：`institutional-research-checker.js --since 2026-06-26T13:59:00.000Z --max-items 8`。Markdown 与 JSON 均已读取。

| 机构 | 列表页 | 详情页 | 严格窗口新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR | 可读 | 8 个候选详情可读，稳定日期均早于窗口 | 0 | 不新增 `trend_aligned_entry` 框架 |
| Citadel Securities | 可读 | 5 个稳定日期详情可读且早于窗口；3 个分类页仅日期不可验证 | 0 | 来源可用；分类页不提炼框架 |
| GMO | 可读 | 8 个候选详情可读，稳定日期均早于窗口 | 0 | 不新增 `AI_quality/capex_cycle` 框架 |
| Man Institute | 可读 | 8 个候选详情可读，最新稳定日期为 2026-06-23、早于窗口 | 0 | 不新增 `factor_macro_exposure` 框架 |

## 策略映射

- `market fear gate`：本报告没有新的 VIX、宽度或信用数据，不能改变 2026-06-26 的 `elevated` 基线；公开源只增加开盘前需复核的事件负荷。
- `trend_aligned_entry`：所有来源项目必须等待价格趋势与相对强度确认；不使用“内存墙/算力稀缺”叙事覆盖趋势门槛。
- `flow_fragility`：内存、光互连、neocloud 和 NVDA/GB300 指向同一 AI-capex 因子；相关持仓不可按 ticker 数量误判为分散。
- `AI_quality/capex_cycle`：新增 `decoder_latency_specialist`、`memory_substitution_stack`、`compute_rationing`、`capex_supply_response` 四个观察字段。
- `factor_macro_exposure`：Starlink 渗透和本地 AI 案例只作行业采用证据；政治内容不直接映射宏观交易。
- `AI bottleneck watch`：重点比较 SRAM/CXL/HBF/Optical HBM 的端到端 TCO，而非只比较单点峰值。
- `theme crowding`：三星/SK 海力士扩产既可能利好设备材料，也可能压低中期稀缺溢价；记录双向风险。
- `portfolio concentration`：MRVL、MU、DRAM、MXL、GLW、TTMI 相关叙事均可能暴露于同一 AI-capex/内存/互连篮子，开盘准备必须重新计算主题集中度。
- `replay/backtest plan`：建立来源事件样本，跟踪 5/20/60 日相对 QQQ/SMH 收益；分别标注“叙事发布日、官方确认日、订单/收入确认日”。

## 数据缺口与需用户确认的访问问题

1. 小红书轮播 `24/26` 原图可导出复核，2 张原图下载失败；页面已逐张经过，但不能宣称 `26/26` 完整 OCR。
2. 小红书只显示相对编辑时间，未暴露绝对发布时间；正文经历审核后修改，初始版本不可核验。
3. X 的 Kay 主页只覆盖当前可见最新范围；Articles/Media 未发现需要单独展开的新框架，本轮未穷举更深历史。
4. Trump X 时间线显示旧内容，不能据此证明其在其他平台或不可见范围没有新政策声明。
5. Citadel 三个分类页日期不可验证，但详情候选和列表均可读；不能写成“来源不可用”。
6. 无需用户当前修改登录或隐私设置；公开页访问可用。若要补齐小红书 2 张原图，只需后续在同一已登录页面重试，不需要提供账号凭据。

## 后续开盘准备重点读取

1. `memory/daily/2026-06-29-realtime-public-institutional-monitor.md`（本文件）
2. `memory/daily/2026-06-26-post-close-audit.md`
3. `memory/portfolio/2026-06-26-portfolio-summary.md`
4. `memory/todos/2026-06-26-strategy-todos.md`
5. `references/daily-market-monitoring-framework.md`
6. `references/ai-quality-capex-cycle-classification.md`
7. `work/institutional-research-latest.md` 与 `work/institutional-research-latest.json`

## 记忆处置

- 已更新 realtime tracker、H5 假设和 daily summaries。
- `decisions.md` 不变：本轮均为单日社媒/来源观察，尚未经过历史 replay 或反复验证。

## 2026-06-30 小红书续读：ORCL AI Token 推理工厂错配

- 来源：美研芒格君，《深入拆解甲骨文, AI Token推理工厂的错配》，ID `6a2b982f0000000017029b43`，https://www.xiaohongshu.com/explore/6a2b982f0000000017029b43 。
- 页面时间：编辑于 `06-12`，美国；正文、作者置顶评论与评论区作者补充可见。
- 轮播：`22/22` 张逐张读取并成功导出，未读缺口 `0`。
- 证据：高（页面、正文、评论、全部图片）；文中的财务数字、客户身份和未来预测仍只是作者二手归纳，必须回到 ORCL 财报、电话会和监管文件验证。

### 作者框架

作者用“餐厅扩建”比喻 OCI/AI 数据中心：传统数据库是老菜，SaaS 是套餐，OCI AI 算力是新开的 AI 大食堂。文章承认 AI 排队和长期 Token 需求真实，但把市场惩罚归因于扩建账单、融资与收入确认之间的错位。

1. `RPO_not_cash`：大额剩余履约义务是未来逐年兑现的合同，不等于当期现金；作者还指出约半数合同可能集中于单一大客户，该身份未经公司确认。
2. `powered_not_revenue_ready`：数据中心通电后折旧和运维立即开始，但 GPU 上架、布线、烧机、网络调优、客户验收和收入确认仍需数周至数月。
3. `capacity_ramp_margin_trough`：新容量批量交付时，成本呈阶跃式出现，利用率和收入呈斜坡式爬升，导致毛利率先下台阶；作者判断 FY27 更像利润率/现金流谷底，改善主要属于 FY28 以后。
4. `capex_financing_dilution`：文章称 ORCL 需要债务和 ATM 增发共同融资，需跟踪利息、摊薄与资本成本，而不能只看收入增速。
5. `utilization_quality`：作者区分“已签合同覆盖的 GPU 比例”和真实在线利用率；97.5% 口头指标不等于 97.5% 的 GPU 正在满负荷产生收入。
6. `customer_concentration_and_renewal`：若大客户占比高，合同沉默、续约率下降、客户自建算力或 GPU 换代都会放大终值风险。
7. `capex_BOM_transmission`：作者把约 900 亿美元 capex 估算拆为 GPU、内存/存储、网络/光互连、电力与机电，映射到 NVDA、MU/SNDK、AVGO/ALAB/MRVL、COHR/LITE；这是候选供应链地图，不是已验证订单。

### 我的判断与策略映射

- 这篇笔记最有价值的不是 ORCL 方向结论，而是 `capacity_to_revenue_lag`。对 ORCL、CRWV、NBIS 等 neocloud/AI 工厂都应按同一张表跟踪：签约容量 → 通电容量 → 已装 GPU → 验收容量 → 计费容量 → 利用率 → 收入 → 毛利 → 自由现金流。
- `AI_quality/capex_cycle`：将“需求真实”与“资本回报兑现”分离。强 RPO、强 capex 和 GPU 紧缺可以同时伴随毛利下滑、负自由现金流和融资稀释。
- `flow_fragility`：若 ORCL、CRWV、NBIS、NVDA、内存和光互连同时依赖同一批 AI capex，不能把它们视为独立主题。
- `factor_macro_exposure`：利率和信用利差会通过融资成本放大 capex 周期；需要跟踪净债务、利息覆盖、债务期限和 ATM 使用。
- `trend_aligned_entry`：文章的“FY27 谷底、FY28 改善”属于来源预测，不是入场规则；必须等待财报验证、毛利拐点和价格趋势共同确认。
- `replay/backtest plan`：对 ORCL/CRWV/NBIS 建立财报事件表，回放 capex 上修、RPO 上修、毛利下修、融资/增发、客户集中披露后 1/5/20/60 日相对收益。

### 待核验清单

- ORCL 最新 10-K/10-Q 中 capex、RPO、自由现金流、债务、股本和毛利口径。
- 电话会中 97.5% 的准确指标定义、GPU 部署到收入确认的周期、FY27/FY28 毛利指引。
- 单一客户约占一半 RPO、客户为 OpenAI 的说法是否有官方证据。
- 约 900-950 亿美元 capex 与 400 亿美元融资/ATM 的准确期间和授权规模。
- 供应链 BOM 比例以及 NVDA、MU、SNDK、AVGO、ALAB、MRVL、COHR、LITE 的真实订单/收入暴露。
