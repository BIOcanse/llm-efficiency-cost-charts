# Release and language access

## Goal

Make the current chart snapshot easy to read in either language and easy to
download as one complete, verifiable bundle.

## Language access

GitHub repository README files cannot run custom JavaScript. Popular
multilingual repositories therefore use one of two patterns:

1. links to separate language-specific README files; or
2. native `<details>` sections that expand inside one README.

This repository uses the second pattern on the repository home page so the
reader does not navigate to another Markdown document. The GitHub Pages site
remains the fully interactive view: its Chinese/English buttons replace all
text, charts, labels, and accessibility metadata on the same URL without a
page navigation.

## Snapshot release

Release tag:

`snapshot-2026-07-24`

Primary asset:

`llm-efficiency-cost-charts-2026-07-24-full.zip`

The archive contains:

- all three English charts as 4K PNG and editable SVG;
- all three Simplified Chinese charts as 4K PNG and editable SVG;
- the dated model, subscription-cost, and access-evidence CSV snapshots;
- all four numerical ranking CSV files;
- chart, methodology, ranking, source, and language-access documentation.

The release also attaches `SHA256SUMS.txt`. It records the SHA-256 digest of
the complete archive.

## Update rule

Every new dated snapshot gets a new `snapshot-YYYY-MM-DD` release. Existing
snapshot tags and assets remain available so published analysis stays
reproducible.
