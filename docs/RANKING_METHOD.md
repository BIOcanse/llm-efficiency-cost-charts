# Ranking methodology

Snapshot: **2026-07-24**

## Why there is no single score-to-cost ratio

Dividing Intelligence Index score directly by Token consumption or cost would treat the benchmark score as a true ratio-scale quantity with a meaningful zero. That assumption is not justified. It would also over-reward low-score configurations and mix capability with efficiency.

The published rankings therefore separate:

1. aggregate Token efficiency across a model's observed reasoning levels;
2. raw API cost per task;
3. raw subscription-first cost per task;
4. the lowest-cost configuration that reaches selected score thresholds.

## Aggregate Token-efficiency index

The aggregate index evaluates the full observed curve rather than selecting one favorable reasoning level.

### Reference frontier

1. Use all configurations with complete total-Token data.
2. Construct the global Token Pareto frontier: no retained point can be matched or exceeded in score by another point using fewer Tokens.
3. Interpolate `log(total Tokens)` between adjacent frontier points as a function of score.

### Per-model curve

1. Group configurations by exact model name and order them by raw score.
2. Interpolate `log(total Tokens)` across the model's observed score range.
3. At equal score values, compare the model curve with the global frontier.
4. Integrate the log Token overhead uniformly over score, then convert it back to a geometric-mean multiplier.

```text
Token overhead = geometric mean(model Tokens / frontier Tokens at the same score)
Aggregate Token-efficiency index = 100 / Token overhead
```

An index of 100 means the model curve lies on the observed global frontier throughout its covered score range. An index of 50 means it uses a geometric mean of twice the frontier Tokens at matched scores.

The published ranking image additionally normalizes the highest observed core
model to `100%` for quick within-snapshot comparison:

```text
Displayed percentage = model index / highest observed core index × 100
```

This display percentage is relative to the current snapshot. The CSV retains
the original frontier-based index and Token-overhead multiplier.

### Eligibility and confidence

- Core ranking: at least 4 observed reasoning levels and at least an 8-point score span.
- Limited-evidence ranking: 2–3 levels or a score span below 8.
- Single-point models do not receive an aggregate rank.

The table always shows level count and covered score range. Models with different score coverage remain useful to compare against the same-score frontier, but the index does not claim that a lower-capability model is more capable.

## API cost ranking

Sort configurations by the API cost of one Intelligence Index task. Every original model uses one fixed provider and price schedule across its reasoning levels. The table also reports score, provider, total Tokens, and model configuration.

Ranking images also show each configuration's cost as a percentage of the most
expensive included API configuration. The most expensive API configuration is
`100%`; exact USD per task remains visible beside the percentage.

## Subscription-first cost ranking

Sort the 46 included configurations by effective cost per Intelligence Index task.

Inclusion order:

1. use the best-value applicable subscription when a usable quota estimate exists;
2. exclude providers with a relevant subscription but no sufficiently reliable quota measurement;
3. use API only when no applicable subscription exists.

The table reports the exact effective task cost, score, plan or API access mode, and confidence level.

Ranking images also show each configuration's cost as a percentage of the most
expensive included subscription-first configuration. This percentage uses a
separate reference from the API ranking, and exact USD per task remains visible.

## Score-threshold leaders

Raw cheapest rankings are naturally dominated by low-score configurations. To answer the more useful question, "What is the cheapest way to reach at least this score?", separate tables select the lowest-cost configuration meeting each score threshold.

Current thresholds: 40, 45, 50, 55, 58, and 60.
