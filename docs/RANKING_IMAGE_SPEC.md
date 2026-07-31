# Ranking image specification

Snapshot: **2026-07-31**

## Purpose

The numerical comparisons must be visible in the published explanation, not
available only as CSV files or interactive tables.

## Published assets

Each asset is rendered in English and Simplified Chinese as PNG and SVG:

1. `04_token_efficiency_ranking`
   - all eligible core and limited-evidence models;
   - aggregate full-curve Token efficiency shown as a percentage;
   - the highest observed core model is normalized to `100%`.
2. `05_api_cost_ranking`
   - the 15 lowest API costs per task;
   - exact USD per task, cost percentage, and Intelligence Index score;
   - the cheapest configuration reaching each score threshold.
3. `05_api_cost_ranking_full`
   - all 68 API-cost configurations;
   - exact USD per task, cost percentage, and score.
4. `06_subscription_cost_ranking`
   - the 15 lowest subscription-first costs per task;
   - exact USD per task, cost percentage, and score;
   - the cheapest configuration reaching each score threshold.
5. `06_subscription_cost_ranking_full`
   - all 46 subscription-first configurations;
   - exact USD per task, cost percentage, and score.

## Calculation and presentation rules

- Images read the dated ranking CSV files; displayed values are not copied by
  hand.
- Token-efficiency display percentage:

  ```text
  display percentage =
      model aggregate Token-efficiency index
      / highest observed core index
      × 100
  ```

- The percentage is a within-snapshot relative display. It does not replace the
  aggregate index definition in `RANKING_METHOD.md`.
- Cost images always show the exact USD-per-task value. They do not use a
  logarithmic axis or a derived score-to-cost ratio.
- Within each cost ranking, the most expensive included configuration is the
  `100%` cost reference:

  ```text
  cost percentage =
      configuration cost per task
      / highest cost per task in the same ranking
      × 100
  ```

- The `100%` reference configuration and its USD cost are printed on every cost
  image. API and subscription-first rankings use their own references and are
  not mixed.
- Raw cost order and score-threshold leaders remain separate because the
  cheapest raw configuration can have a low Intelligence Index score.
- Core and limited-evidence Token rankings remain visually separated.

## Placement

- `README.md`: the three concise ranking images.
- `docs/CHART_GUIDE.md`: concise images plus the two complete cost-ranking
  images.
- GitHub Pages: the three concise images before the interactive ranking tables.
- Snapshot Release: all bilingual PNG/SVG ranking images and updated
  documentation.

## Rendering structure

`scripts/render_ranking_charts.py` owns all ranking-image rendering. It reads:

- `rankings/<date>/token_efficiency_ranking.csv`;
- `rankings/<date>/api_cost_ranking.csv`;
- `rankings/<date>/subscription_cost_ranking.csv`;
- `rankings/<date>/score_threshold_leaders.csv`.

The renderer writes only to `charts/en/` and `charts/zh-CN/`. Language strings,
formatting rules, dimensions, and output names are defined explicitly in the
renderer and can be overridden through command-line arguments where relevant.

Rendering dependencies are pinned in `requirements-render.txt` and installed in
the repository-local `.venv`.
