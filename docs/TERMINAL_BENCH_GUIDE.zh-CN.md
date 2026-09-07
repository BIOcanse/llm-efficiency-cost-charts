# Terminal-Bench 图表说明

每个点是模型＋Agent＋思考档位，同色线连接同名系统的不同档位。纵轴为任务成功率，竖线为 95% 区间。左上更好。

图 1：套餐折算成本与成功率。按历史实测或官方额度，估算跑满套餐后的每次尝试成本；没有适用套餐时使用 API 成本。

图 2：API 成本与成功率。每次尝试成本＝评测公布的总成本 ÷ 尝试数，包含失败尝试。

图 3：Token 消耗与成功率。每次尝试消耗＝评测公布的总 Token ÷ 尝试数，包含输入、缓存、推理及回答。

套餐与 API 图的虚线是性价比前沿。只看成功率与成本，前沿之外的配置没有经济优势。Token 图对应效率前沿，消耗不等于成本。

排名按总消耗 ÷ 成功数计算，支持厂商、Agent 和成功率区间筛选。相对消耗以最高者为 100%，相对性价比以每个成功任务消耗最低者为 100%。

套餐不是固定 Token 配额。Codex 70×、Claude 40×沿用 6 月报道的跑满额度 API 等价值，实际测量窗口未披露；Fable 20×另含共享额度上限假设，当前适用置信度均为低。GLM 使用官方积分公式，年付折合 $117.60/月、标准时段；缓存拆分的不确定性保留在明细中。[9 月 7 日额度核查](SUBSCRIPTION_REVIEW_2026-09-07.md)

TB4 最新采集日期为 2026-09-07 UTC，持续更新；旧版保留最终快照，2.0 / 1.0 仅有成功率数据。各版独立比较，结果针对同一测试集的模型＋Agent＋配置，分数差距结合 95% 区间看。

数据来源：

https://www.tbench.ai/
https://www.tbench.ai/news/terminal-bench-4-0
https://github.com/harbor-framework/terminal-bench-website/tree/130be8458294043b33bbde1c765f3180f5ba96fb
https://learn.chatgpt.com/docs/pricing
https://developers.openai.com/api/docs/pricing
https://claude.com/pricing
https://support.claude.com/en/articles/15910845-claude-code-may-august-2026-weekly-limits-promotion
https://x.com/ClaudeDevs/status/2093742321473065266
https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan
https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-costs-spike-as-subscriptions-hit-pricing-wall-firms-turn-towards-chinese-llms-open-source-models-to-extend-budget
https://docs.z.ai/devpack/overview
https://z.ai/subscribe
https://geminicli.com/docs/resources/quota-and-pricing/
https://cursor.com/docs/models-and-pricing
