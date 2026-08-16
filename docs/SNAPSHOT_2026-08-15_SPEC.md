# 2026-08-15 general-model snapshot

## Scope

Publish a new general-model snapshot without modifying the already released
2026-07-24 and 2026-07-31 snapshots or the independently versioned Coding
Agent Index scenario.

The new snapshot uses Artificial Analysis Intelligence Index **v4.1.1** for
every score, Token observation, and weighted task-cost observation. Values from
the earlier v4.1 snapshots must not be copied into the new chart when a current
v4.1.1 observation is unavailable.

## Model selection

- Refresh every retained configuration from its current Artificial Analysis
  model page.
- Replace the DeepSeek V4 Pro / Flash preview points with the released dated
  models. Do not connect a released model to its preview predecessor.
- Add newly released frontier models and material regional representatives
  when AA publishes complete score and Token data for the same v4.1.1 suite.
- Remove a superseded point from the current view when its purpose is fully
  covered by the released successor. Historical points remain available in the
  older immutable snapshots.
- A quantized endpoint is a separate model. It is included only when AA
  publishes sufficiently complete benchmark data and the label identifies the
  quantization explicitly.

## Data contract

Each included configuration must preserve:

- model, developer, country/region, release date, and reasoning level;
- raw Intelligence Index v4.1.1 score;
- canonical input, reasoning, answer, and output Token counts;
- complete-suite Token consumption;
- AA's raw weighted cost per task;
- one consistently selected API route and its input/cache/output prices;
- direct model and pricing source URLs.

The normalized API task cost continues to use the measured per-task Token
composition and the selected route's prices. All reasoning levels of one
original model use the same provider and endpoint. A cheaper quantized route
must not be substituted for the benchmarked original model.

## Subscription-first contract

- Reuse a subscription only when it is still applicable to the exact model and
  a usable allowance estimate exists.
- Recalculate the effective task cost from the refreshed API task cost; do not
  treat the allowance estimate as a fixed Token quota.
- Exclude a model when an applicable subscription exists but its allowance
  cannot be quantified.
- Fall back to API pricing only when no applicable subscription exists.

The 2026-08-15 evidence snapshot must record the source date, confidence, and
whether a value is official or a third-party full-limit estimate.

## Publication

- Add `2026-08-15` to the in-place snapshot selector and show its exact Release
  publication timestamp in UTC.
- Keep the earlier snapshots and their benchmark labels unchanged.
- The current page, downloads, ranking CSVs, and Release links must switch as a
  single versioned payload.
- Generate bilingual PNG/SVG analysis charts and ranking images, a complete
  Release archive, and the interactive desktop payload.
- Personal recommendations are explicitly subjective and must carry the
  snapshot they were written against.

## Validation gates

- Every new point has a current direct AA source and belongs to v4.1.1.
- No preview DeepSeek model appears in the current snapshot.
- Score, Token components, total Token consumption, API price, and cost fields
  reconcile before charts are rendered.
- Static chart labels have no collisions or bounds violations.
- Snapshot, language, provider, frontier, score-range, and ranking controls work
  without reloading the page.
- The current and both historical general-model snapshots retain their own
  benchmark version, counts, links, and UTC publication time.
