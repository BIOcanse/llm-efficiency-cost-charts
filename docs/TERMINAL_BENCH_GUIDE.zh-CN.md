# Terminal-Bench 图表说明

每个点是模型＋Agent＋思考档位。连线连接同名系统的不同档位，Agent 构建版本未公布时仍标为未知。纵轴是任务成功率，竖线为评测方公布的 95% 区间。

图 1：套餐折算成本与成功率。按跑满适用套餐额度估算每次任务尝试的成本。有套餐但缺少可核实换算条件的配置不进入该图；只有评测工具链没有适用套餐时才使用 API 成本。

图 2：API 成本与成功率。每次尝试成本＝该次运行公布的总成本 ÷ 尝试数。保留评测时使用的供应商和计价，不用另一家的低价替换。

图 3：Token 消耗与成功率。采用官方公布的总 Token ÷ 尝试数，包含缓存输入、推理及回答所计入的消耗，不重复加算。部分原始输入字段命名有歧义，分类字段保留原值，图中总量不受影响。

左上前沿（斩杀线）：没有其他配置能同时做到消耗不高、成功率不低，并至少一项更好。三项指标分别计算，每版独立列出模型＋Agent＋档位及实际数值，同坐标配置全部保留。网页名单随该图的厂商和 Agent 筛选更新，缩放不改变名单。虚线台阶表示已观测到的预算边界，不是两点之间的模型插值；按点值入选不代表统计显著领先。2.0、1.0 缺少消耗数据，无法计算前沿。

成本排名按平均每个成功任务的成本排序，即总成本 ÷ 成功数，失败尝试的消耗也计入。未公布成功数时采用公布的成功率折算。可按厂商、Agent 和成功率区间筛选；相对成本以筛选后最高者为 100%，相对性价比以每个成功任务消耗最低者为 100%。该比值不是无限重试必然成功的保证。

Token 效率与价格是两个指标。完成相同任务、成功率相近时，消耗越少效率越高；参数规模接近、Agent 与预算可比时，更能反映模型技术效率。参数规模本身也会影响 Token 效率，不能把所有差异都归因于架构。

套餐折算保留估算日期和置信度。Codex 70×、Claude 40×采用 2026 年 6 月的第三方跑满额度结果，并非 9 月重新实测。Fable 20×还假设相同内部折算规则，再应用官方 50% 共享周额度上限。GLM Max 使用官方积分公式，年付 $1,411.20（折合 $117.60/月），标准时段；月付 $168 和全非高峰半价在明细中另列。GLM 的输入／缓存拆分为明示的残差建模假设，未公布的工具调用费用不补猜测值。

数据采集于 2026-09-05 UTC。TB 4 持续收录新快照；3.0、2.1、2.0、1.0 保存本项目的最终成图，不再跟随更新。2.0、1.0 缺少可核实的消耗汇总，仅保留成功率。不同测试集版本不混排；旧版的“最终”不代表上游永不修订。TB 2.1 Opus 4.7 的评测计数为 447、试验关联数为 445，保留双方并采用评测计数，差异原因未核实。

数据来源：

https://www.tbench.ai/
https://www.tbench.ai/news/terminal-bench-4-0
https://www.tbench.ai/news/terminal-bench-3-0
https://www.tbench.ai/news/terminal-bench-2-1
https://github.com/harbor-framework/terminal-bench-website/tree/130be8458294043b33bbde1c765f3180f5ba96fb
https://github.com/harbor-framework/terminal-bench/releases/tag/v4.0.0
https://learn.chatgpt.com/docs/pricing
https://developers.openai.com/api/docs/pricing
https://claude.com/pricing
https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan
https://github.com/iteebz/ccmeter/blob/1484b439e0789e2eb7b070d478f6f19f539305ef/README.md
https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-costs-spike-as-subscriptions-hit-pricing-wall-firms-turn-towards-chinese-llms-open-source-models-to-extend-budget
https://docs.z.ai/devpack/overview
https://z.ai/subscribe
https://static.bigmodel.cn/z-ai-website/_next/static/chunks/8519-b0eeed0c70db38cb.js
https://geminicli.com/docs/resources/quota-and-pricing/
https://cursor.com/docs/models-and-pricing
https://forum.cursor.com/t/how-much-usage-is-available-on-the-200-subscription/163309/5
