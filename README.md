# LLM Efficiency & Cost Charts

[中文说明](README.zh-CN.md)

Continuously maintained charts comparing LLM intelligence scores with total Token consumption, API task cost, and subscription-first task cost.

Latest snapshot: **2026-07-24**  
Benchmark: **Artificial Analysis Intelligence Index v4.1**  
Current coverage: **73 Token-consumption configurations / 68 API-cost configurations / 46 subscription-first configurations**

Each point represents one model and reasoning level. Lines of the same color connect reasoning levels of the same model. Higher scores and lower Token consumption or cost are better, so the upper-left region is preferred.

## 1. Total Token consumption vs. score

Total consumption includes input, reasoning, and final-answer Tokens used to complete the same benchmark suite.

[PNG](charts/en/01_total_token_consumption_vs_score.png) · [SVG](charts/en/01_total_token_consumption_vs_score.svg)

![Total Token consumption versus Intelligence Index score](charts/en/01_total_token_consumption_vs_score.png)

## 2. API cost per task vs. score

Task cost combines the per-task Token composition with one fixed provider price for each original model. Quantized variants are treated as separate models only when the underlying benchmark data is sufficiently complete.

[PNG](charts/en/02_api_task_cost_vs_score.png) · [SVG](charts/en/02_api_task_cost_vs_score.svg)

![API cost per task versus Intelligence Index score](charts/en/02_api_task_cost_vs_score.png)

## 3. Subscription-first cost per task vs. score

The best-value applicable subscription is used when both a plan and a usable quota estimate are available. Plans without quantifiable quota data are excluded. API pricing is used only when no applicable subscription exists.

[PNG](charts/en/03_subscription_first_task_cost_vs_score.png) · [SVG](charts/en/03_subscription_first_task_cost_vs_score.svg)

![Subscription-first task cost versus Intelligence Index score](charts/en/03_subscription_first_task_cost_vs_score.png)

## Important limitations

- Results apply only to the same Intelligence Index v4.1 benchmark suite, which emphasizes relatively difficult coding and scientific tasks.
- A point measures a **model + reasoning-level configuration**, not a model independently of its inference budget.
- Intelligence Index scores are treated as a useful continuous comparison, not an exact absolute measure of intelligence.
- OpenAI and Claude subscription API-equivalent values are third-party estimates based on exhausting usage limits. They are not fixed Token quotas promised by the providers.
- Pricing, plans, benchmark results, and quota behavior can change. Every release is tied to a dated snapshot under [`data/`](data/).

See the [detailed chart guide](docs/CHART_GUIDE.md), [methodology](docs/METHODOLOGY.md), [ranking methodology](docs/RANKING_METHOD.md), [sources](docs/SOURCES.md), and the [current data snapshot](data/2026-07-24/).

## Update policy

An update should change the data snapshot, both language chart sets, snapshot metadata, and [`PROGRESS.md`](PROGRESS.md) together. Previous dated data snapshots remain available for comparison.
