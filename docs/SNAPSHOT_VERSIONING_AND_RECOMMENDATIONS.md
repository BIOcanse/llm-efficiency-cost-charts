# Snapshot versioning and personal recommendations

## Scope

Add two reader-facing features without changing the benchmark calculations:

1. a compact personal-recommendation section that is explicitly separated
   from the objective charts and rankings;
2. an in-place snapshot selector for the interactive page.

## Personal recommendation contract

The recommendation section is subjective and applies to the latest
2026-07-31 snapshot only. It must be labelled as personal opinion and must not
be presented as a generated ranking.

### SOTA models

1. GPT-5.6 Sol
2. Claude Opus 5
3. Kimi K3

### Value models

1. GPT-5.6 Luna
2. DeepSeek V4 Pro

Do not add more models to make either list look more complete. The charts and
numerical rankings remain the place for exhaustive comparison.

## Snapshot selector contract

- The selector switches the complete interactive payload without navigating
  or reloading the page.
- The selected version updates all three charts, all numerical rankings,
  threshold tables, coverage counts, chart-download links, ranking CSV links,
  current-data link, and Release link together.
- Each option displays a human-readable version name. The adjacent metadata
  displays the exact Release publication time in Coordinated Universal Time.
- UTC timestamps:
  - `2026-07-24`: `2026-07-25T03:06:13Z`
  - `2026-07-31`: `2026-07-31T05:55:55Z`
- The latest snapshot is the default. A reader-selected snapshot is stored
  locally and remains reversible.
- Personal recommendations stay tied to 2026-07-31 and carry a visible badge;
  switching to a historical chart does not rewrite those opinions.

## Published assets

```text
site/data/snapshots.json
site/data/snapshots/2026-07-24.json
site/data/snapshots/2026-07-31.json
charts/archive/2026-07-24/{en,zh-CN}/*.{png,svg}
```

The current charts remain under `charts/{en,zh-CN}`. The archive directory
contains the exact static chart files from the corresponding published
Release, not newly reconstructed artwork.

## Validation

- Both versions load 73 / 68 / 46 configurations and pass the existing data
  shape checks.
- Version changes preserve the chosen language and reset no unrelated user
  controls.
- Both languages show the correct UTC timestamp and recommendation wording.
- Every selected-version PNG, SVG, CSV, data, and Release link returns 200.
- Desktop layout and browser console are checked after switching in both
  directions.
