# Terminal-Bench chart guide

Each point is a model + agent + reasoning setting. Lines connect effort levels of the same named system; unpublished agent builds remain unknown. The Y axis is task success, with the owner's reported 95% interval.

Chart 1: Subscription-equivalent cost versus success. Estimate cost per attempt at full utilization of an applicable plan. Known plans without a defensible conversion are excluded; API cost is used only where the evaluated harness has no applicable subscription.

Chart 2: API cost versus success. Cost per attempt = published total run cost / attempts. Retain the evaluated provider and pricing rather than substituting a cheaper endpoint.

Chart 3: Token consumption versus success. Published total Tokens / attempts, including cached input and billed reasoning/answer output without double-counting. Some raw input field names are inconsistent; preserve their original values and use the published total unchanged.

Upper-left Pareto frontier: no other configuration uses no more resources and achieves no less success, with at least one strict improvement. Each metric and benchmark version has its own list of model + agent + effort configurations and measured values. Equal-coordinate ties are retained. Lists follow each chart's provider and agent filters; zooming does not change membership. Dashed steps show observed budget limits, not interpolation between models. Membership based on point estimates does not establish statistically significant superiority. Versions 2.0 and 1.0 lack the consumption data needed to calculate a frontier.

Cost rankings use average cost per successful task: total cost / successes, including failed attempts. Where success counts are absent, use the published success rate. Provider, agent and success-rate filters recalculate rankings: the highest cost is 100% for relative cost; the lowest resources per success is 100% for value. This workload ratio is not a promise that unlimited retries solve every task.

Token efficiency and price are separate metrics. At similar success on the same tasks, fewer Tokens mean higher efficiency. Comparable parameter scale, agent setup and budgets make the result more informative about technical efficiency. Model scale itself affects Token efficiency; not every difference is attributable to architecture.

Subscription estimates retain evidence dates and confidence. Codex 70× and Claude 40× use third-party June 2026 exhaustion tests, not September retests. Fable 20× also assumes comparable internal metering and applies its official 50% shared-weekly-pool cap. GLM Max uses official weighted credits, $1,411.20 annual prepayment ($117.60/month equivalent), and standard credits. The $168 monthly plan and all-off-peak half-rate scenario appear separately in Details. GLM's input/cache split is an explicit arithmetic-residual model; unreported tool fees are not invented.

Captured September 5, 2026 UTC. TB4 receives new snapshots. Versions 3.0, 2.1, 2.0 and 1.0 retain this project's final charts; 2.0/1.0 lack verifiable consumption summaries and show success rates only. Versions are never pooled. “Final” does not imply that upstream can never revise a leaderboard. TB2.1 Opus 4.7 reports 447 metric attempts but 445 associated trials; both are retained and the metrics count is used, without inventing a cause.

Sources:

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
