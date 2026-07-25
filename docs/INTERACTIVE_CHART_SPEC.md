# Interactive chart specification

Snapshot baseline: **2026-07-24**

## Goal

The GitHub Pages site must render the three analysis charts from machine-readable
snapshot data instead of displaying pre-rendered PNG files. PNG and SVG assets
remain available only as downloadable, citable snapshot artifacts.

The site remains a static GitHub Pages deployment. It has no application server,
database, account system, or third-party runtime dependency.

## Data flow

```text
data/<snapshot>/model_efficiency.csv
data/<snapshot>/subscription_first_task_cost.csv
  -> scripts/build_rankings.py
  -> site/data/rankings.json
  -> site/assets/interactive-scatter.js
  -> client-side SVG
```

`site/data/rankings.json` must contain three chart datasets:

- `charts.token`: all 73 configurations with complete Token data;
- `charts.subscription`: all 46 subscription-first configurations;
- `charts.api`: all 68 configurations with comparable API cost.

The published reading order is total Token consumption, subscription-first
task cost, then API task cost. Subscription cost comes first because
subscriptions are the common access path for the included frontier models; API
cost remains available for metered and volume workloads.

The site must not manually duplicate plotted values.

## Component structure

- `site/assets/interactive-scatter.js`
  - owns SVG axes, points, same-model lines, permanent point labels,
    collision-aware label layout, frontier marks, tooltip, selection, pan, and
    zoom;
  - accepts localized labels and number formatters from the page application;
  - contains no snapshot-specific model values.
- `site/assets/app.js`
  - loads the static JSON payload;
  - provides the three metric configurations;
  - updates chart language without navigating or reloading the page;
  - continues to own ranking tables and the page-level language state.
- `site/assets/styles.css`
  - owns the desktop chart surface, controls, tooltip, and selected-state
    presentation.

## Interaction

Each chart provides:

1. pointer and keyboard inspection of every point;
2. a tooltip and persistent readout containing model, reasoning level, score,
   horizontal value, and provider or access method when applicable;
3. click or Enter to pin a point;
4. a model selector that highlights one model without deleting the comparison
   context;
5. wheel zoom, drag pan, explicit zoom buttons, and reset view;
6. same-model lines ordered by reasoning level;
7. a full model-and-reasoning-level label next to every point in the overview;
8. label placement recalculated after zoom, pan, language changes, and model
   highlighting, with labels kept close to their points while avoiding points,
   lines, axes, and one another;
9. Pareto-frontier points with a distinct outline;
10. immediate Chinese/English updates on the same URL.

The horizontal scales remain linear. Interactivity provides close inspection
without changing the cost comparison to a logarithmic axis.

## Desktop layout and accessibility

- Every SVG has a localized accessible name and description.
- Points are keyboard focusable and expose localized accessible labels.
- The selected-point readout mirrors tooltip information.
- Controls use native buttons and select elements.
- The published experience targets desktop screens only. The page keeps a
  1440 px desktop minimum width instead of compressing the chart into a mobile
  layout.
- Each chart preserves the 16:9 visual proportions and information density of
  the released static chart.
- Reduced-motion preferences disable nonessential transitions.

## Acceptance criteria

- No PNG is used as the visible chart body on GitHub Pages.
- All 73 / 68 / 46 expected configurations render from JSON.
- Chinese and English update chart titles, axes, controls, tooltips, and
  accessibility text in place.
- Selecting a model changes point and line emphasis.
- The default overview shows all full point labels without overlap; highlighting
  or zooming must not remove labels for visible points.
- Labels remain visibly associated with their points and must not cover points,
  same-model lines, axes, or each other.
- Zoom, pan, reset, pointer inspection, click pinning, and keyboard inspection
  work.
- Existing PNG/SVG download links remain valid.
- Ranking tables retain exact USD values and cost percentages.
