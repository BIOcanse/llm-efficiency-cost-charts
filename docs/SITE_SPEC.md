# GitHub Pages specification

Published page: https://biocanse.github.io/llm-efficiency-cost-charts/

## Purpose

Publish the current bilingual charts, detailed chart explanations, and numerical rankings on one GitHub Pages URL.

## Language behavior

- Chinese and English switch instantly on the same page without navigating to another Markdown document.
- The first visit uses the browser language when available.
- A visible language control always lets the reader override the default.
- The explicit choice is stored locally in the browser and remains reversible.
- The document `lang`, button state, headings, chart images, detailed explanations, table headings, numbers, and accessibility labels update together.

## Information structure

1. Snapshot and metric summary.
2. Three chart sections.
3. A detailed explanation under each chart:
   - axes;
   - points and same-model lines;
   - formula;
   - inclusion and exclusion rules;
   - appropriate conclusions;
   - conclusions the chart does not support.
4. Numerical rankings:
   - aggregate full-curve Token efficiency;
   - subscription-first cost per task;
   - API cost per task;
   - lowest cost at selected score thresholds.
5. Methodology, limitations, source, data, and repository links.

## Data flow

```text
dated CSV snapshot
  -> scripts/build_rankings.py
  -> rankings/<date>/*.csv + site/data/rankings.json
  -> static GitHub Pages table rendering
```

The site must not contain manually duplicated ranking numbers. A snapshot update regenerates the rankings and both language views from the same machine-readable result.

## Hosting

- Static HTML, CSS, and JavaScript only.
- GitHub Pages deployment through the official Pages Actions.
- No account, analytics, cookies, remote fonts, or third-party runtime dependency.
- The Pages workflow publishes `site/` together with the current chart assets and ranking data.

## Published result

- The page switches Chinese and English in place without navigating to a second document.
- Subscription-first ranking is the default numerical view; all 46 rows can be expanded.
- API ranking contains all 68 comparable rows.
- Aggregate Token efficiency contains five core full-curve models and four limited-evidence models.
- Each chart includes visible axis, formula, inclusion, exclusion, and interpretation notes.
- GitHub Pages deployment is automatically updated from `main`.
