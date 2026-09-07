# Terminal-Bench data and website contract

## Copy and quota review, 2026-09-07

The cost charts call the upper-left line the **cost-performance frontier**
(性价比前沿). The Token chart calls it the **Token-efficiency frontier**.
The visible explanation states the useful comparison, not the implementation:
outside the frontier, another measured configuration offers at least as much
success for no more cost or Tokens, with an improvement in one measure.
The mathematical membership rule is unchanged. Do not repeat statistical
warnings, step-interpolation notes, filter behavior, or raw-field diagnostics
beside every figure. Keep only essential units and scope in the main view;
retain evidence, assumptions and exact rules in Method/Details and the guide.

Recheck current official plan pricing, allowances and model-specific caps, plus
the strongest dated empirical conversion evidence. A price or credit rate is
not an included weekly allowance. Retain a historical estimate when no better
supported replacement exists, and preserve its measurement date. Record the
review date separately. Do not invent a change merely to make the snapshot
appear fresh. TB4 receives a new dated snapshot after review; frozen versions,
previous TB4 data and their published figures stay unchanged.

Implementation uses the existing `terminal-bench.js` copy, shared interactive
renderer, `render.py` figure text, dated access-policy file, and snapshot
builder. Update the current bilingual guides, README entry and Release. No
new dashboard runtime or changes to axes, filters, palettes or model identity.

Decision date: 2026-09-05. This supersedes the current-site recommendation and
AA-first requirements. Existing AA snapshots remain historical records.

## User direction

The site publishes data without personal model recommendations. Its primary
question is how much completed agent work a subscription or an API budget buys.
Token efficiency remains a separate technical metric. When model scale and
test conditions are comparable, higher Token efficiency is useful evidence of
technical efficiency; the site does not invent parameter counts or attribute
all differences in an agent-system result to model architecture.

Terminal-Bench 4 is the actively maintained benchmark series. Earlier versions
receive a final sourced snapshot and bilingual chart set, then remain frozen.
"Final" means this project's frozen capture, not a claim that upstream can no
longer correct a leaderboard. Benchmark versions never share a score axis or
form one aggregate ranking.

## Plain-language data flow

The importer reads an identified official leaderboard revision and saves the
source and retrieval time. It converts each submitted run into one complete
record with its model, agent, version, reasoning setting, results, resource
usage, and evidence. A dated access policy converts the run's measured API
cost into an applicable subscription estimate. The builder creates plots,
rankings, CSV files, and a JSON payload from those records. The website selects
one benchmark version and one snapshot at a time; every count, link, figure,
and table follows that selection.

Missing values remain missing. Zero means a measured zero. A run with no
comparable cost can appear in the Token view if its Token data is complete,
but never receives an invented price. Different dataset versions, task
subsets, custom resource budgets, or incomplete runs remain distinguishable.

## Measurement contract

- Observation: model checkpoint + agent + agent version + reasoning setting
  + published execution configuration. Source submission/job id is unique.
- Only settings of the same evaluated model and agent/version are connected.
  A quantized checkpoint or multi-model route retains its explicit identity.
- Y axis: task resolution rate, 0–100%, with the owner's published confidence
  interval when available. No conversion into absolute intelligence.
- Main plots, in order: subscription-first cost per attempted task, API cost
  per attempted task, total Tokens per attempted task. All axes are linear;
  the overview starts both axes at zero, and the Y axis extends to 100%.
- Total Tokens include the input/cache/output categories exposed by the run.
  Reasoning already included in output is not counted twice. Preserve missing
  components and the source's reported aggregate separately.
- API cost is the cost of the evaluated route. A cheaper provider is not
  substituted for an agent-system observation without a matching run.
- Cost rankings use average cost per attempt divided by resolution rate as a
  fraction. Failed attempts contribute to cost. At zero resolution the cost
  per completed task is undefined/infinite and cannot win the value ranking.
- Relative cost: the most expensive included finite configuration is 100%.
  Relative value: the lowest cost per completed task is 100%. Both recalculate
  after provider, agent, or inclusive resolution-rate filters change.
- Show actual USD values, resolution rate, Token use, runtime when available,
  sample size, source, and subscription confidence beside derived rankings.
- The cost-per-completion ratio describes output from the tested workload;
  it is not an estimate that arbitrary retries solve every individual task.

## Subscription contract

Use the best supported applicable subscription estimate. Retain official
quota conversions and dated third-party full-limit estimates with their
evidence dates and confidence. Current official relative metering can update
a previous measured allowance only when its relationship is supported.
Applicable plans with no defensible conversion are explicitly excluded from
the subscription view. Use API only when no applicable subscription exists.
The evaluated agent path must actually support the plan. No private OAuth
workarounds or implicit first-party membership for unrelated harnesses.

## Version and output structure

```text
data/terminal-bench/<version>/<snapshot>/
  source.json                 pinned owner observations and provenance
  results.csv                 normalized observations
  access_policy.json          dated quota assumptions and sources
  subscription_costs.csv      included/excluded decisions
  validation.json             reconciliation and static-layout checks
site/data/terminal-bench.json  active/frozen versions and dated payload links
site/data/terminal-bench/<version>/<snapshot>.json
charts/terminal-bench/<version>/<snapshot>/{en,zh-CN}/
rankings/terminal-bench/<version>/<snapshot>/
scripts/terminal_bench/        import, derivation, rendering, validation
site/assets/terminal-bench.js  version selection, charts, numerical tables
```

The new view uses the existing static GitHub Pages layout and shared
InteractiveScatterChart/WebGPU renderer. AA general/coding scenarios remain
accessible as archives. Chinese and English switch in place. Benchmark
version, snapshot, and language are shareable URL state. Desktop chart
geometry, complete labels, close label association, and full/reduced motion
controls remain in use.

The importer refuses to replace a saved raw source or create a new date for a
frozen benchmark. Current TB4 updates
create a new dated snapshot; earlier TB4 snapshots remain reproducible.
Static exports include both language sets, three scatter plots, numerical
cost-ranking images, and CSV/JSON sources in a downloadable Release.

## Updating TB4

Review the current owner dataset and a new dated access-policy file first.
Run from the repository root (replace both date placeholders):

```text
python scripts/terminal_bench/build_snapshot.py --snapshot YYYY-MM-DD --versions 4.0 --access-policy scripts/terminal_bench/access-policy-YYYY-MM-DD.json --render
python -m unittest discover -s scripts/terminal_bench -p test_core.py
python scripts/build_release_bundle.py --benchmark terminal-bench --snapshot YYYY-MM-DD
```

A new snapshot requires explicit quota-policy selection; old estimates are
never silently promoted to a fresh measurement. Existing snapshots rebuild
from their saved source and policy. `retrieved_at_utc` is the source capture
time, while `built_at_utc` is the artifact build time, not a Release timestamp.
Run the browser bootstrap and smoke scripts with Playwright CLI `run-code
--filename`, review both languages at 1920 px and 1440 px, then publish the
checked source, static site, and Release bundle. Later snapshots do not alter
the frozen 3.0, 2.1, 2.0, or 1.0 captures.

## Acceptance

- Reconcile sample counts, rate, total/average Tokens and cost against owner
  data before rendering; preserve the raw source and hash.
- No recommendations or subjective model verdicts remain in the current UI.
- Every available legacy benchmark has a clearly frozen final chart set.
- Provider/agent filters, resolution interval, rank recomputation, version,
  snapshot, language, pin/clear, zoom and reset work on desktop.
- Confidence intervals and full labels remain readable without overlaps.
- Release contents, UTC timestamps, archive links and live deployment agree.

## Upper-left frontier, 2026-09-07

The requested "斩杀线" is the observed Pareto frontier, separately for
subscription USD/attempt, API USD/attempt, and Tokens/attempt against success
rate. A configuration is on it when no other eligible configuration costs
less or the same and succeeds more or the same, with at least one strict
improvement. Equal-coordinate ties all remain in the list. Missing/non-finite
consumption is excluded, not zero. Compare the published unrounded coordinates;
this is not a statistical-significance test or a subjective recommendation.

Chart contract: retain each existing full scatter and named-system curves;
overlay a dark dashed, step-shaped frontier with outlined member points. The
steps represent the best observed success at or below a consumption budget,
not interpolation or a new model. Begin at the cheapest frontier point, end at
the highest-success point, and do not extend invented coordinates. This keeps
every nondominated point, not just a convex hull or a ratio-based top-N.
Show an exact lookup list below each interactive chart, in increasing
consumption order, with model, effort, agent, success interval, actual
consumption and applicable subscription confidence. Chart provider/agent
filters recalculate both the line and its adjacent list; zoom only changes the
view. The frontier overlay can be switched off without changing the data.

Delivery stays in the user-selected existing GitHub Pages application and
Matplotlib PNG/SVG exports. No replacement dashboard runtime or hosting system.
The existing model palette is retained; the frontier is distinguished by a
neutral dashed stroke and point outlines, not another model color. Static
figures remain 4800×2700 with linear axes from zero and success from 0–100%.
Label avoidance includes frontier segments. Validate at 1920px and 1440px.

Add frontier exports and a combined frontier list for every saved TB version
and snapshot. Preserve original images, raw observations, quota evidence and
capture times; an analytical/display supplement is not a new data snapshot.
TB1/TB2 lists explicitly state that all three frontiers are unavailable because
consumption is missing. AA archives are outside this TB-version supplement.

Implementation: `core.py` owns the export calculation; `interactive-scatter.js`
shares one equivalent frontier function between the overlay and live list.
`render.py` creates additional frontier plots/list pages; `build_snapshot.py`
provides a frontier-only export mode. Tests compare both implementations with
an independent pairwise oracle, ties, missing/zero values and each saved set.
Release supplements retain the original snapshot date and a separate release
date; older Release assets remain unchanged.

## Source audit, 2026-09-05

The owner's public Harbor leaderboard-read API supplies 18 TB4, 12 TB3,
22 TB2.1 and 142 migrated TB2 rows. Task/trial counts are 66/330, 74/370,
89/usually 445 respectively for the three modern versions. TB2.1 Opus 4.7
publishes metrics.n_trials=447 but 445 associated trials; both are retained,
the metrics count is used, and the cause is not inferred. TB2 has no trial-linked
consumption summaries; its zero trial association count is missing data, not
zero attempts. Legacy versions without consumption receive final success-rate
charts, not fabricated efficiency/cost figures.

All TB4 and five Astra TB2.1 records satisfy `total = named_uncached + output`;
other TB2.1 records satisfy the three-component sum. Use the published total.
GLM credit conversion, where available, is explicitly a residual-input modeled
scenario, not a claimed correction to the upstream schema. Current API records
omit agent versions; connected effort points represent the same *named* system,
not verified identical agent builds. The missing version is visible in details.

Subscription estimates retain dated full-use calibration: Codex 70x, Claude
40x, Fable 20x (40x times the official 50% shared-pool cap). The former Claude
26.67x relied on an unverified promotion overlap and is not the new baseline.
All of these are estimates, not September full-quota retests. Current GLM-5.3
Max publishes 140,000 credits/week and 28,000/5h; annual payment $1,411.20 is
explicitly labeled (effective $117.60/month; monthly commitment is $168).
Standard credit rates are the baseline; all-off-peak is a separate sensitivity,
not an assumed workload mix. Price evidence is the official V3 product config.
TB3 Grok 4.5 numeric cost is excluded per the owner's cost-reporting caveat.
