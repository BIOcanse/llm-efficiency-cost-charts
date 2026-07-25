# Filtered cost-performance ranking specification

Snapshot baseline: **2026-07-24**

## Purpose

Keep the existing absolute USD-per-task rankings and add two recalculated
cost-performance views:

1. subscription-first cost-performance;
2. API cost-performance.

The intended use is to constrain the acceptable intelligence interval first,
then compare value inside that workload class. A volume workload can therefore
limit the range to lower or middle scores instead of mixing it with frontier
configurations.

## Inputs

Each cost-performance panel has two inclusive numeric filters:

- minimum Intelligence Index score;
- maximum Intelligence Index score.

The default range is 0 through 100. Invalid ranges where minimum exceeds
maximum show a visible validation message and no recalculated ranking. The two
panels keep independent ranges.

## Formula

For every included configuration inside the selected interval:

```text
raw value = Intelligence Index score / USD per task
value index = raw value / highest raw value in the filtered result × 100
```

Higher is better. The best included configuration in the current interval is
always 100%. The table also shows the original score and USD per task.

Subscription-first and API values are never mixed in one calculation.

## Interpretation boundary

The Intelligence Index is not a physical ratio-scale unit. The value index is a
practical ranking heuristic inside one explicitly selected score interval, not
an absolute statement that one model is a precise multiple as capable as
another. Index values from different score intervals must not be compared.

## Table layout

Absolute cost and cost-performance tables combine model name and reasoning
level into one compact adjacent cell. Exact cost, score, access/provider, and
confidence or Token consumption remain separate columns.

## Acceptance

- Changing either score bound immediately recalculates only the corresponding
  panel.
- Results are filtered inclusively and sorted by value index descending, then
  cost ascending, then score descending.
- The first row is 100% whenever the filtered result is non-empty.
- Raw cost tables remain unchanged in meaning.
- Chinese and English labels, validation text, and number formats update in
  place.
