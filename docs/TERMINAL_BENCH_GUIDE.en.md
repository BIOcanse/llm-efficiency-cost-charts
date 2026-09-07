# Terminal-Bench chart guide

Each point is a model + agent + reasoning setting. Same-color lines connect settings of the same named system. The Y axis is task success, with 95% intervals. Upper left is better.

Chart 1: Subscription-equivalent cost versus success. Historical measurements or official allowances estimate cost per attempt at full utilization. API cost applies where no applicable subscription exists.

Chart 2: API cost versus success. Cost per attempt = published total spending / attempts, including failed attempts.

Chart 3: Token consumption versus success. Tokens per attempt = published total Tokens / attempts, including input, cache, reasoning and answers.

On success rate and cost alone, configurations outside the cost-performance frontier offer no economic advantage. The Token chart instead shows an efficiency frontier; consumption is not cost.

Rankings use total resources / successes, with provider, agent and success-rate filters. Highest consumption = 100%; lowest resources per success = 100% value.

Subscriptions are not fixed Token quotas. Codex 70× and Claude 40× retain full-use API-equivalent estimates reported in June; exact measurement dates are undisclosed. Fable 20× additionally assumes a shared-pool cap; current applicability is low-confidence. GLM uses official weighted credits, annual payment equivalent to $117.60/month and standard hours. Cache-split uncertainty remains in Details. [September 7 allowance review](SUBSCRIPTION_REVIEW_2026-09-07.md)

TB4's latest capture is September 7, 2026 UTC, with ongoing updates. Earlier versions retain final snapshots; 2.0 / 1.0 have success-rate data only. Compare within the same benchmark version and model + agent + configuration setting, and read score gaps alongside the 95% intervals.

Sources:

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
