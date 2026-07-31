# Coding-agent chart-suite specification

Snapshot date: **2026-07-31**

## Analytical question

For coding-agent variants evaluated on the same Artificial Analysis coding
suite, how do total Token consumption, pay-per-token API cost, and
subscription-first effective task cost relate to observed task success?

This is a separate scenario from the three Intelligence Index v4.1 charts. It
must never reuse the label `Intelligence Index`, merge the two scores, or imply
that an agent result measures the underlying model independently of its harness
and settings.

## Scenario navigation

The site exposes two same-level, large scenario pages:

- `general`: the existing Intelligence Index v4.1 model-level suite;
- `coding`: the Coding Agent Index v1.3 agent-system suite.

The scenario control changes all three visible charts in place without a page
reload. `?view=general` and `?view=coding` are stable, shareable URLs. Language,
snapshot, and scenario selections remain independent.

Each scenario displays exactly three charts in this reading order:

1. total Token consumption;
2. subscription-first effective cost per task;
3. pay-per-token API cost per task.

## Shared chart contract

- Family: relationship / labelled scatter.
- Observation grain: one evaluated `agent harness + model + setting` variant.
- Y axis: Artificial Analysis Coding Agent Index v1.3 score multiplied by 100;
  higher is better.
- X axes: linear, zero-based, and lower is better.
- Reading direction: upper left is better.
- Lines: connect settings only when the agent harness and underlying model
  family are both the same. Different harnesses using the same model are not
  connected.
- Outline: the dark outline marks the observed Pareto frontier for the visible
  metric and filter state.
- Filters: model developer and coding-agent harness.
- Tooltip/readout: agent, model and setting, Coding Agent Index, the active
  horizontal metric, total Token use, active agent wall time, model developer,
  API route, and access method where applicable.
- Palette: reuse the site's explicit series palette; labels and line grouping
  carry identity so color is not the only distinction.

The expected current source table contains 52 variants. All rows must have
finite non-negative cost/Token/time values and a unique Artificial Analysis
result id. Fifty-one rows materialize all three component evaluations. The
source currently retains `Claude Code · Opus 4.6 (medium)` with two materialized
components; it remains visible as a clearly marked partial observation and is
not described as complete 321-task coverage.

## Chart 1: total Token consumption

- X axis: pooled average total Tokens per coding task attempt, shown in
  millions.
- Total Tokens use Artificial Analysis's published `totalTokens` aggregate. The
  page separately exposes input, cache-write, cache-read, and output fields;
  provider-specific reasoning accounting is not reconstructed as a separate
  category when the source does not publish one.
- Inclusion: all 52 complete variants.
- Interpretation: this is task-level Token use by the entire evaluated agent
  system. It is not a model-only Token-efficiency score because harness policy,
  tool calls, context reuse, and termination behavior also affect consumption.

## Chart 2: subscription-first effective cost per task

- X axis: effective USD per coding task under the best quantifiable applicable
  subscription; lower is better.
- Inclusion hierarchy:
  1. use a relevant subscription when a usable API-equivalent allowance
     estimate exists;
  2. exclude the evaluated variant when a relevant plan exists but its usable
     quota cannot be quantified;
  3. use the observed API cost only when no applicable subscription exists for
     that evaluated agent route.
- OpenAI Codex variants use the dated ChatGPT Pro 20x API-value estimate.
- Anthropic models evaluated through Claude Code use the dated Claude Max 20x
  estimate; Fable fallback keeps its separately measured allowance ratio.
- Cursor CLI uses the official guaranteed value of Cursor Ultra: $200/month
  with $400/month of included Agent API usage. Unquantified bonus usage is not
  counted, so the dated API-value ratio is a conservative 2x.
- Gemini CLI, Grok Build, and Kimi Code CLI rows are excluded until a usable
  plan allowance estimate is available.
- Third-party models used through Claude Code and models used through OpenCode
  remain API-only because the measured Claude/Codex plan is not the access path
  evaluated by those rows.
- Expected current count: 49 variants.

## Chart 3: API cost per task

- X axis: pooled average pay-per-token API cost per coding task in USD; lower is
  better.
- Inclusion: all 52 complete variants.
- Cost uses the source treatment of uncached input, cached input, cache writes,
  reasoning, and output for the evaluated API route.
- The chart does not replace an evaluated route with a cheaper provider.

## Benchmark scope

Artificial Analysis Coding Agent Index v1.3 combines three equally weighted
task-normalized pass@1 components:

- DeepSWE: 113 long-horizon software-engineering tasks;
- Terminal-Bench v2: 84 agentic terminal tasks after five incompatible tasks
  are excluded;
- SWE-Atlas-QnA: 124 repository-understanding questions.

Each task is attempted three times. The index covers 321 tasks, while cost,
Token usage, and execution time are pooled per-task-attempt averages over the
same public benchmark suite.

## Inclusion and naming rules

- Include rows from the current v1.3 source table with `indexComponentCount ==
  3` and complete pooled efficiency metrics. Preserve `evalCount` and mark any
  row with fewer than three materialized component evaluations as partial.
- Preserve the evaluated agent harness. A Claude Code, Codex, Cursor CLI,
  Gemini CLI, Grok Build, Kimi Code CLI, or OpenCode result is an agent-system
  result, not a model-only result.
- Preserve reasoning or thinking settings as separate points.
- DeepSeek V4 Pro keeps the `(Preview)` suffix until Artificial Analysis
  publishes a production-checkpoint retest.
- An explicitly quantized route is labelled as a separate model variant. The
  current Novita `GLM-5.2` row is therefore displayed as `GLM-5.2 (FP8)`.
- Fable fallback behavior stays in the visible model name because it changes
  the evaluated system.

## Interpretation limits

- The score summarizes the published mix of repository modification, terminal
  work, and repository Q&A. It is not an absolute coding-ability value and does
  not represent every codebase or workflow.
- Harness, model, settings, caching behavior, tool use, and execution policy can
  all affect a point. Do not attribute every difference to model weights.
- Subscription costs are benchmark-specific estimates, not provider-promised
  raw Token quotas.
- API cost excludes subscription pricing, infrastructure, supervision, and
  engineering overhead.
- Average task values do not show variance across task difficulty. Exact source
  percentile fields are retained only when published and are not used as axes.

## Data and output structure

```text
Artificial Analysis coding-agent page
  -> scripts/snapshot_coding_agents.py
  -> data/coding-agents/2026-07-31/coding_agent_results.csv
  -> data/coding-agents/2026-07-31/subscription_access_policy.csv
  -> scripts/build_coding_agent_charts.py
  -> data/coding-agents/2026-07-31/subscription_first_task_cost.csv
  -> site/data/coding-agents/2026-07-31.json
  -> charts/{en,zh-CN}/07_coding_agent_total_tokens_vs_index.{png,svg}
  -> charts/{en,zh-CN}/08_coding_agent_subscription_cost_vs_index.{png,svg}
  -> charts/{en,zh-CN}/09_coding_agent_api_cost_vs_index.{png,svg}
```

The independent manifest at `site/data/coding-agents.json` records the current
coding-agent snapshot, benchmark version, and source-observation time. Switching
the Intelligence Index snapshot does not silently relabel or replace this
separate benchmark.

## Acceptance criteria

- Token/API charts contain all 52 source-table variants; the subscription chart
  contains 49 rows under the dated policy; all ids are unique. Fifty-one rows
  are complete and the single two-component source row is visibly marked.
- The stored index equals the mean of the three published benchmark component
  scores when all components are materialized in the source payload.
- No cost, Token, time, or score value is negative or non-finite.
- The interactive and static charts use Coding Agent Index labels throughout;
  no `Intelligence Index` axis appears in this scenario.
- Model-developer and agent-harness filters both work and clear pinned state.
- Full labels are visible without overlap at the supported desktop width.
- Chinese and English static exports are visually inspected at final size.
- The scenario switch updates all three charts in place and preserves language.
- Source page, methodology URL, observation time, source SHA-256, and access
  policy are stored with the snapshot.
