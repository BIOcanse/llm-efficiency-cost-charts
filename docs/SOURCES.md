# Sources

Snapshot date: **2026-07-31**

## Benchmark methodology and model results

- [Artificial Analysis models](https://artificialanalysis.ai/models)
- [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
- [Artificial Analysis Intelligence Index v4.1](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1/)
- [Artificial Analysis trends](https://artificialanalysis.ai/trends/)
- [Artificial Analysis Data API documentation](https://artificialanalysis.ai/data-api/docs)

Every model configuration's direct Artificial Analysis page is stored in the `source_url` or `benchmark_source_url` column of the dated CSV files.

## Coding-agent benchmark

- [Artificial Analysis Coding Agent benchmarks](https://artificialanalysis.ai/agents/coding-agents)
- [Coding Agent Index methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking)
- [DeepSWE](https://deepswe.datacurve.ai/)
- [Terminal-Bench v2](https://www.tbench.ai/benchmarks/terminal-bench-2)
- [SWE-Atlas-QnA](https://labs.scale.com/leaderboard/sweatlas-qna)

The coding-agent snapshot stores the source observation time and SHA-256 of the
downloaded page. Its Coding Agent Index v1.3 score and pooled task cost are not
mixed with Intelligence Index v4.1 values.

## Coding-agent access paths

- [Cursor models and pricing](https://docs.cursor.com/account/pricing)
- [Grok Build launch and subscription access](https://x.ai/news/grok-build-cli)
- [Grok shared weekly usage-pool FAQ](https://docs.x.ai/grok/faq)

The coding-agent subscription chart uses Cursor Ultra's official guaranteed
$400/month Agent API allowance against its $200/month price, a conservative 2x
API-value ratio that excludes unquantified bonus usage. Grok Build is available
through paid plans, but the shared weekly pool is published only as percentages,
so its result is excluded rather than replaced by API pricing.

## OpenAI

- [Codex pricing and usage limits](https://learn.chatgpt.com/docs/pricing)
- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [Codex rate card](https://help.openai.com/en/articles/20001106)
- [SemiAnalysis subscription-limit measurement](https://x.com/semianalysis_/status/2064815044085318040)
- [Tom's Hardware report on the same measurement](https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-costs-spike-as-subscriptions-hit-pricing-wall-firms-turn-towards-chinese-llms-open-source-models-to-extend-budget)

The 2026-07-31 snapshot applies the official July 30 standard API prices:
GPT-5.6 Luna is 80% lower and GPT-5.6 Terra is 20% lower. Current Codex
credit rates remain proportional to those API prices. The subscription chart
therefore keeps the independently measured 70x API-value ratio and reprices
the affected tasks; it does not treat that estimate as an official Token quota.

## Anthropic

- [Claude plans and pricing](https://claude.com/pricing)
- [Claude Code usage limits](https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [Claude Opus 5 announcement](https://www.anthropic.com/news/claude-opus-5)
- [Claude Fable 5 plan announcement](https://x.com/claudeai/status/2078302415804379218)
- [Expired +50% promotion context](https://www.bleepingcomputer.com/news/artificial-intelligence/claude-fable-5-stays-free-for-paid-users-until-july-19-as-anthropic-buys-more-time/)
- [Independent Claude allowance measurement tool](https://github.com/iteebz/ccmeter)

The current chart uses the post-promotion standard allowance estimate only. The expired +50% promotion is retained as source context but is not plotted.

## Other included subscription or API sources

- [Xiaomi MiMo Token Plan](https://mimo.mi.com/docs/zh-CN/tokenplan/Token%20Plan/subscription)
- [Z.AI subscription plans](https://z.ai/subscribe)
- [ZCode plan configuration](https://zcode.z.ai/en/docs/configuration)
- [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/)
- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Amazon Nova 2 documentation](https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html)
- [Meta Muse Spark 1.1 / Meta Model API](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- [NVIDIA Nemotron 3 Ultra model card](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b/modelcard)
- [HyperNova 60B 2605](https://multiversecomputing.com/resources/introducing-hypernova-60b-2605)
- [CompactifAI API pricing](https://docs.compactif.ai/pricing/)

## Plans excluded because usable quota data is unavailable

- [xAI Grok FAQ](https://docs.x.ai/grok/faq)
- [Google Gemini Apps usage limits](https://support.google.com/gemini/answer/16275805?hl=en-GB)
- [Kimi membership pricing](https://www.kimi.com/help/membership/membership-pricing)
- [Kimi Code membership](https://www.kimi.com/code/docs/en/kimi-code/membership.html)
- [Alibaba Model Studio Token Plan](https://www.alibabacloud.com/help/en/model-studio/token-plan-overview)
- [MiniMax Token Plan](https://platform.minimax.io/subscribe/token-plan?tab=individual__monthly)
- [Mistral pricing](https://mistral.ai/pricing/)

These providers are not replaced by API pricing in the subscription-first chart because a relevant subscription exists but its usable quota cannot currently be quantified with sufficient confidence.
