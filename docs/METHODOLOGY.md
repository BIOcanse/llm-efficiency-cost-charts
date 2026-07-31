# Methodology

Snapshot date: **2026-07-31**

## Shared benchmark

All scores and Token-consumption observations use Artificial Analysis Intelligence Index v4.1. Each point is one model and reasoning-level configuration.

The score is used as a continuous comparison under one benchmark. This is useful for relative analysis but is not an exact absolute measure of intelligence, especially near a benchmark's upper or lower bound.

## Chart 1: total Token consumption

For the full benchmark suite:

```text
total Tokens = input Tokens + reasoning Tokens + final-answer Tokens
```

The chart compares the complete Token consumption required to finish the same suite. Reasoning-level names are provider-facing labels and do not imply identical inference budgets across models.

## Chart 2: API cost per task

For each model, one provider and one original model endpoint are selected consistently across reasoning levels. The per-task calculation includes:

- standard input Tokens;
- cache-read and cache-write Tokens where priced separately;
- reasoning Tokens;
- final-answer Tokens.

The chart does not substitute a cheaper quantized endpoint for the original model. A quantized variant is treated as a separate model only when its benchmark data is sufficiently complete.

## Chart 3: subscription-first cost per task

Inclusion order:

1. Use the best-value applicable subscription when both a plan and a usable quota estimate exist.
2. Exclude a provider from this chart when a relevant plan exists but its quota cannot be quantified reliably.
3. Use API pricing only when no applicable model subscription exists.

For API-equivalent estimates, the effective task cost is derived from the plan cost, estimated API-equivalent allowance, and that configuration's API cost per task. Because different tasks use different Token types and quantities, the result is benchmark-specific rather than a general raw-Token quota.

OpenAI and Claude values are medium-confidence third-party estimates based on exhausting usage limits and applying current provider pricing. They are not fixed Token quotas promised by the providers. Claude uses the current standard allowance estimate; the expired +50% promotion is not plotted.

For the 2026-07-31 pricing refresh, GPT-5.6 Luna and Terra keep the existing OpenAI 70x API-value estimate. OpenAI's current Codex credit rates remain proportional to the new standard API prices, so their subscription-first task costs fall by the same 80% and 20% as their API task costs. This changes cost, not benchmark score or Token efficiency.

## Pareto frontier

The black outline marks configurations for which no other included point is both cheaper or lower in Token consumption and at least as high-scoring.

## Separate coding-agent chart suite

The coding-agent scenario uses Artificial Analysis Coding Agent Index v1.3
rather than Intelligence Index v4.1. Each point is one evaluated agent harness,
model, and setting. The Y value is the equally weighted mean of DeepSWE,
Terminal-Bench v2, and SWE-Atlas-QnA task-normalized pass@1 scores.

Its three X values are:

1. Artificial Analysis's pooled average `totalTokens` per coding task attempt;
2. subscription-first effective USD per task under the same inclusion hierarchy
   as the general chart;
3. pooled average pay-per-token API cost per task.

Subscription estimates apply only when the measured plan is an access path for
the evaluated agent/model combination. A plan with no usable allowance estimate
causes exclusion from the subscription chart; API is used only when the
evaluated route has no applicable subscription.

The public suite contains 321 tasks and three attempts per task. Of the 52 rows
currently published in the v1.3 table, 51 materialize all three components.
Artificial Analysis also retains one `Claude Code · Opus 4.6 (medium)` row with
two materialized components; the charts preserve it as a visibly marked partial
source observation. These charts measure the evaluated agent system, so
differences may come from the harness, model, reasoning setting, caching
behavior, or tool workflow. It is intentionally kept outside the three
model-level Intelligence Index charts and uses an independent snapshot cadence.

## Reproducibility

The dated CSV files preserve model names, reasoning levels, raw scores, Token composition, selected provider pricing, access mode, confidence, and direct source URLs used by the current release.
