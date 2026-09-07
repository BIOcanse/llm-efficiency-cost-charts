import { InteractiveScatterChart } from "./interactive-scatter.js?v=20260907-quota-copy-1";

const REVISION = "20260907-quota-copy-1";
const text = {
  "zh-CN": {
    title: "编码 Agent 性价比与效率", lead: "",
    active: "持续更新", frozen: "最终快照", version: "测试集版本", snapshot: "数据快照", captured: "采集时间（UTC）",
    charts: "三项对比", rankings: "数据与性价比排名", method: "计算口径与来源", upperLeft: "左上更好",
    costFrontier: "性价比前沿", tokenFrontier: "Token 效率前沿", showFrontier: "显示前沿线", frontierList: "前沿配置", frontierCsv: "完整名单 CSV",
    costFrontierHint: "只看成功率与成本，前沿之外的配置没有经济优势。", tokenFrontierHint: "线外配置均有 Token 消耗不高、成功率不低的更优替代项。",
    frontierOrder: "按消耗递增", frontierCount: "个配置", frontierMissing: "该版缺少消耗数据，仅列成功率，无法计算前沿。",
    chartHint: "点＝模型＋Agent＋思考档位；竖线＝95% 区间。",
    subscription: "套餐折算成本", api: "API 成本", token: "Token 消耗", success: "成功率",
    subscriptionLead: "按历史实测或官方额度折算；无适用套餐时采用 API 成本。",
    apiLead: "评测公布的实际 API 成本，包含失败尝试。",
    tokenLead: "完成任务所用的总 Token，包含输入、缓存、推理和回答。",
    subscriptionAxis: "美元 / 尝试（套餐折算，越低越好）", apiAxis: "美元 / 尝试（API，越低越好）", tokenAxis: "百万 Token / 尝试（越低越好）",
    yAxis: "任务成功率（%，越高越好）", provider: "模型提供商", allProviders: "全部提供商", agent: "Agent", allAgents: "全部 Agent",
    zoomIn: "放大", zoomOut: "缩小", reset: "重置视图", interact: "滚轮缩放，拖动平移；点击点查看，空白处或 Esc 取消。", readout: "指向或点击一个配置查看数据。",
    unknown: "未公布", attempt: "每次尝试", resolved: "每个成功任务", trials: "尝试数", taskCount: "题目数", runtime: "平均耗时", confidence: "折算置信度", unverified: "上游标记未核验", verification: "上游核验标志",
    access: "使用方式", source: "官方记录", download: "成图 / 数据下载", images: "打开成图", data: "原始数据", csv: "下载 CSV",
    scoreMin: "成功率不低于（%）", scoreMax: "成功率不高于（%）", metric: "排序指标", apply: "筛选后重排", clear: "清除筛选",
    rankingHint: "按总成本 ÷ 成功数排序，失败尝试的成本也计入。",
    tokenRankingHint: "按总 Token ÷ 成功数排序。",
    successRankingHint: "按任务成功率排序，保留官方区间与尝试数。", missingConsumptionHint: "该版缺少可核实的消耗汇总，仅比较成功率。",
    rank: "排名", model: "模型 · 档位", rate: "成功率 · 95% 区间", perAttempt: "消耗 / 尝试", perSuccess: "消耗 / 成功任务", relativeCost: "相对最高消耗", relativeValue: "相对性价比", details: "明细",
    empty: "该筛选条件下没有可用配置。", rangeError: "成功率区间应在 0–100% 内，且下限不高于上限。", visible: "个配置", close: "关闭",
    estimate: "估算", published: "官方运行数据", medium: "中", low: "低", unavailable: "不可折算",
    noUsage: "该版官方汇总缺少可核实的 Token / 成本数据。最终成图保留成功率，不补猜测值。",
    versionPolicy: "TB 4 持续更新；旧版保留最终快照。",
    productionTitle: "任务成本", productionBody: "每次尝试成本＝总成本 ÷ 尝试数；每个成功任务成本＝总成本 ÷ 成功数，包含失败尝试。",
    tokenTitle: "Token 效率", tokenBody: "同一任务、成功率相近时，Token 消耗越低，效率越高。参数量接近、Agent 与预算可比时，更能反映模型技术效率；参数规模本身也会影响该指标。",
    quotaTitle: "套餐折算", quotaBody: "采用官方额度或可信实测，按充分使用折算。估算日期、适用限制和置信度见下方套餐依据。",
    scopeTitle: "评测范围", scopeBody: "比较同一版 Terminal-Bench 的模型＋Agent＋配置。结果不代表所有实际任务，分数差距需结合 95% 区间看。",
    percentage: "相对消耗以筛选后最高者为 100%；相对性价比以每成功任务消耗最低者为 100%。",
    exclusions: "未进入套餐图的配置", evidence: "套餐依据与日期", rawTokens: "官方总 Token", rawCost: "官方总 API 成本", tokenFields: "Token 字段口径", missingVersion: "上游未公布 Agent 构建版本", offpeak: "GLM 全非高峰估计 / 尝试", monthly: "GLM 月付估计 / 尝试", rawInput: "原字段 uncached_input_tokens", rawCache: "原字段 cached_input_tokens", rawOutput: "原字段 output_tokens",
    rawWarning: "部分 uncached_input_tokens 字段在数值上已包含缓存；该图使用官方 total_tokens，不把三项再次相加。GLM 的缓存拆分是显式建模假设。",
    statuses: {missing_or_unreliable_benchmark_cost: "该次运行缺少可信成本", exact_checkpoint_no_longer_supported_by_current_plan: "当前套餐不再提供该精确旧模型", plan_credit_formula_known_benchmark_components_missing: "套餐公式已知，但评测缺少 Token 分类", official_request_quota_but_benchmark_model_request_count_missing: "官方请求额度已知，但评测缺少模型请求数", applicable_plan_conversion_unavailable: "有适用套餐，缺少可信折算分母", cursor_models_pool_not_api_pool_quota: "Cursor 自有模型池不可套用 API 池额度"},
  },
  en: {
    title: "Coding agents: cost and efficiency", lead: "",
    active: "Actively updated", frozen: "Final snapshot", version: "Benchmark version", snapshot: "Data snapshot", captured: "Captured (UTC)",
    charts: "Three comparisons", rankings: "Data and cost-performance rankings", method: "Method and sources", upperLeft: "Upper left is better",
    costFrontier: "Cost-performance frontier", tokenFrontier: "Token-efficiency frontier", showFrontier: "Show frontier", frontierList: "Frontier configurations", frontierCsv: "Full list CSV",
    costFrontierHint: "On success rate and cost alone, configurations outside the frontier offer no economic advantage.", tokenFrontierHint: "Outside the frontier, a better alternative offers at least as much success with no more Tokens.",
    frontierOrder: "Lowest consumption first", frontierCount: "configurations", frontierMissing: "Consumption data is missing. Only success rates are available; no frontier can be calculated.",
    chartHint: "Point = model + agent + effort; whiskers = 95% interval.",
    subscription: "Subscription-equivalent cost", api: "API cost", token: "Token consumption", success: "Success rate",
    subscriptionLead: "Historical measurements or official allowances at full use; API cost where no applicable plan exists.",
    apiLead: "Reported API spending, including failed attempts.", tokenLead: "Total task Tokens: input, cache, reasoning and answers.",
    subscriptionAxis: "USD / attempt · subscription-equivalent · lower is better", apiAxis: "USD / attempt · API · lower is better", tokenAxis: "Million Tokens / attempt · lower is better",
    yAxis: "Task success rate (%) · higher is better", provider: "Model provider", allProviders: "All providers", agent: "Agent", allAgents: "All agents",
    zoomIn: "Zoom in", zoomOut: "Zoom out", reset: "Reset view", interact: "Scroll to zoom, drag to pan; click a point for details, blank space or Esc to clear.", readout: "Hover or select a configuration to inspect its data.",
    unknown: "Not reported", attempt: "Per attempt", resolved: "Per successful task", trials: "Attempts", taskCount: "Tasks", runtime: "Mean time", confidence: "Conversion confidence", unverified: "Unverified upstream", verification: "Upstream verification flag",
    access: "Access", source: "Official record", download: "Charts / data downloads", images: "Open chart", data: "Source data", csv: "Download CSV",
    scoreMin: "Success rate at least (%)", scoreMax: "Success rate at most (%)", metric: "Rank by", apply: "Recalculate after filtering", clear: "Clear filters",
    rankingHint: "Ranked by total cost / successes, including failed attempts.",
    tokenRankingHint: "Ranked by total Tokens / successes.", successRankingHint: "Ranked by success rate, with uncertainty and attempt counts.", missingConsumptionHint: "Consumption data is missing. Compare success rates only.",
    rank: "Rank", model: "Model · effort", rate: "Success · 95% interval", perAttempt: "Usage / attempt", perSuccess: "Usage / success", relativeCost: "% of highest usage", relativeValue: "Value index", details: "Details",
    empty: "No configurations match these filters.", rangeError: "Use a 0–100% interval with the lower bound no greater than the upper bound.", visible: "configurations", close: "Close",
    estimate: "Estimate", published: "Owner-reported run", medium: "Medium", low: "Low", unavailable: "Unavailable",
    noUsage: "The official summary lacks verifiable aggregate Token / cost data. Final exports retain success rates without invented consumption.",
    versionPolicy: "TB 4 receives updates; earlier versions retain their final snapshots.",
    productionTitle: "Task cost", productionBody: "Cost per attempt = total cost / attempts. Cost per successful task = total cost / successes, including failed attempts.",
    tokenTitle: "Token efficiency", tokenBody: "On the same tasks at similar success rates, fewer Tokens mean higher efficiency. At comparable parameter scale, agent setup and budget, this better reflects technical efficiency. Model scale itself also affects the metric.",
    quotaTitle: "Subscription conversion", quotaBody: "Official allowances or credible measurements, assuming full utilization. Evidence dates, limits and confidence appear below.",
    scopeTitle: "Benchmark scope", scopeBody: "Model + agent + configuration on the same Terminal-Bench version. Results do not cover every workload; read score gaps alongside the 95% intervals.",
    percentage: "Highest filtered consumption = 100%. Best resources per success = 100% value.",
    exclusions: "Configurations excluded from the subscription chart", evidence: "Subscription evidence and dates", rawTokens: "Published total Tokens", rawCost: "Published total API cost", tokenFields: "Token field semantics", missingVersion: "Agent build not published upstream", offpeak: "GLM all-off-peak estimate / attempt", monthly: "GLM monthly-plan estimate / attempt", rawInput: "Raw uncached_input_tokens", rawCache: "Raw cached_input_tokens", rawOutput: "Raw output_tokens",
    rawWarning: "Some fields named uncached_input_tokens arithmetically include cache. Charts use the published total_tokens, not a new three-field sum. GLM's cache split is explicitly modeled.",
    statuses: {missing_or_unreliable_benchmark_cost: "Missing or unreliable run cost", exact_checkpoint_no_longer_supported_by_current_plan: "Exact old checkpoint no longer offered by current plan", plan_credit_formula_known_benchmark_components_missing: "Plan formula known; benchmark token categories missing", official_request_quota_but_benchmark_model_request_count_missing: "Official request allowance known; model-request count missing", applicable_plan_conversion_unavailable: "Applicable plan, no credible conversion denominator", cursor_models_pool_not_api_pool_quota: "Cursor Models pool cannot inherit the API-pool allowance"},
  },
};
const EFFORT_ZH = {low: "低", medium: "中", high: "高", xhigh: "超高", max: "Max", none: "无", minimal: "最低", ultra: "Ultra", not_reported: "未公布"};
const METRICS = ["subscription", "api", "token"];
const X_KEYS = {subscription: "subscription_per_attempt", api: "api_per_attempt", token: "total_tokens_million"};
const RANK_KEYS = {subscription: "subscription_per_success", api: "api_per_success", token: "tokens_per_success"};
const escape = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
const usd = (value) => value == null ? "—" : `$${Number(value).toFixed(value < 0.001 ? 6 : 4)}`;
const millions = (value) => value == null ? "—" : `${(value / 1e6).toFixed(3)}M`;
const utc = (value) => new Date(value).toISOString().slice(0, 19).replace("T", " ") + " UTC";

export function rankTerminalRows(rows, metric, {provider = "", agent = "", minimum = 0, maximum = 100} = {}) {
  if (!Number.isFinite(minimum) || !Number.isFinite(maximum) || minimum < 0 || maximum > 100 || minimum > maximum) return null;
  const key = RANK_KEYS[metric];
  const filtered = rows.filter(row => (!provider || row.developer === provider) && (!agent || row.agent === agent) && row.score >= minimum && row.score <= maximum && (metric === "success" || (Number.isFinite(row[key]) && row[key] >= 0)));
  filtered.sort((left, right) => metric === "success" ? right.score - left.score : left[key] - right[key] || right.score - left.score);
  if (!filtered.length) return [];
  const best = filtered[0][key], worst = filtered.at(-1)[key];
  return filtered.map((row, index) => ({...row, rank: index + 1, relativeCost: metric === "success" ? null : worst ? row[key] / worst * 100 : 100, relativeValue: metric === "success" ? null : row[key] ? best / row[key] * 100 : 100}));
}

export class TerminalBenchView {
  constructor(root) {
    this.root = root;
    this.language = "en";
    this.active = false;
    this.sequence = 0;
    this.charts = new Map();
    this.metric = "subscription";
    this.filters = {provider: "", agent: "", minimum: 0, maximum: 100};
    this.root.innerHTML = `
      <section class="section page-shell tb-version-section">
        <div class="tb-version-controls"><label><span data-tb="version"></span><select id="tb-version"></select></label><label><span data-tb="snapshot"></span><select id="tb-snapshot"></select></label><div><span data-tb="captured"></span><time id="tb-time"></time></div><span class="tb-state" id="tb-state"></span></div>
        <p class="tb-note" data-tb="versionPolicy"></p><p class="tb-error" id="tb-error" role="status"></p>
      </section>
      <section id="tb-charts" class="section page-shell"><div class="section-heading"><div><span class="eyebrow" data-tb="charts"></span><h2 data-tb="upperLeft"></h2></div><p data-tb="chartHint"></p></div><p class="tb-empty" id="tb-no-usage" hidden data-tb="noUsage"></p>
      ${METRICS.map((metric, i) => `<article class="chart-card" id="tb-card-${metric}"><div class="chart-heading"><span class="chart-number">0${i + 1}</span><div><h3 data-tb="${metric}"></h3><p data-tb="${metric}Lead"></p></div><a class="text-link" id="tb-image-${metric}" target="_blank" rel="noreferrer" data-tb="images"></a></div><div class="tb-frontier-controls"><span class="tb-frontier-key" data-tb="${metric === "token" ? "tokenFrontier" : "costFrontier"}"></span><label><input type="checkbox" id="tb-frontier-toggle-${metric}" checked><span data-tb="showFrontier"></span></label></div><div id="tb-chart-${metric}"></div><section class="tb-frontier-list"><div class="tb-frontier-heading"><h4 data-tb="frontierList"></h4><span id="tb-frontier-count-${metric}"></span><a id="tb-frontier-csv-${metric}" target="_blank" rel="noreferrer" data-tb="frontierCsv"></a></div><p class="tb-note" data-tb="${metric === "token" ? "tokenFrontierHint" : "costFrontierHint"}"></p><div class="table-wrap tb-table-wrap"><table class="tb-table tb-frontier-table" id="tb-frontier-table-${metric}"></table></div></section></article>`).join("")}</section>
      <section id="tb-rankings" class="section page-shell"><div class="section-heading"><h2 data-tb="rankings"></h2><a class="text-link" id="tb-csv" data-tb="csv"></a></div>
        <div class="tb-filters"><label><span data-tb="metric"></span><select id="tb-metric"></select></label><label><span data-tb="provider"></span><select id="tb-provider"></select></label><label><span data-tb="agent"></span><select id="tb-agent"></select></label><label><span data-tb="scoreMin"></span><input id="tb-min" type="number" min="0" max="100" step="0.1" value="0"></label><label><span data-tb="scoreMax"></span><input id="tb-max" type="number" min="0" max="100" step="0.1" value="100"></label><button class="button secondary" type="button" id="tb-clear" data-tb="clear"></button></div>
        <p class="tb-note" id="tb-ranking-hint"></p><p class="tb-note" data-tb="percentage"></p><p class="tb-result-count" id="tb-result-count" role="status"></p>
        <div class="table-wrap tb-table-wrap"><table class="tb-table"><thead id="tb-table-head"></thead><tbody id="tb-table-body"></tbody></table></div>
      </section>
      <section id="tb-method" class="section page-shell"><div class="section-heading"><h2 data-tb="method"></h2><a class="text-link" id="tb-source-data" target="_blank" rel="noreferrer" data-tb="data"></a></div><div class="method-grid">${["production", "token", "quota", "scope"].map(key => `<article class="method-card"><h3 data-tb="${key}Title"></h3><p data-tb="${key}Body"></p></article>`).join("")}</div>
        <details class="tb-disclosure"><summary data-tb="exclusions"></summary><div id="tb-exclusions"></div></details>
        <details class="tb-disclosure"><summary data-tb="evidence"></summary><div id="tb-evidence"></div></details>
        <details class="tb-disclosure"><summary data-tb="download"></summary><div id="tb-downloads"></div></details>
        <div class="tb-source-links" id="tb-sources"></div>
      </section><dialog id="tb-detail"><button type="button" class="button secondary tb-dialog-close" data-tb="close"></button><div id="tb-detail-content"></div></dialog>`;
    this.el = (id) => this.root.querySelector(`#${id}`);
    this.el("tb-version").addEventListener("change", event => this.select(event.target.value));
    this.el("tb-snapshot").addEventListener("change", event => this.select(this.version.id, event.target.value));
    this.el("tb-metric").addEventListener("change", event => {this.metric = event.target.value; this.renderRanking();});
    for (const [id, key] of [["tb-provider", "provider"], ["tb-agent", "agent"], ["tb-min", "minimum"], ["tb-max", "maximum"]]) {
      this.el(id).addEventListener("input", event => {this.filters[key] = ["minimum", "maximum"].includes(key) ? Number(event.target.value) : event.target.value; this.renderRanking();});
    }
    this.el("tb-clear").addEventListener("click", () => {this.filters = {provider: "", agent: "", minimum: 0, maximum: 100}; this.renderFilters(); this.renderRanking();});
    for (const metric of METRICS) this.el(`tb-frontier-toggle-${metric}`).addEventListener("change", () => this.renderCharts());
    this.el("tb-detail").querySelector("button").addEventListener("click", () => this.el("tb-detail").close());
    this.el("tb-detail").addEventListener("click", event => {if (event.target === this.el("tb-detail")) this.el("tb-detail").close();});
  }
  get t() { return text[this.language]; }
  effort(row) { return this.language === "zh-CN" ? EFFORT_ZH[row.effort] || row.effort : row.effort.replace("not_reported", "not reported"); }
  async load() {
    const response = await fetch(`data/terminal-bench.json?v=${REVISION}`);
    if (!response.ok) throw new Error(`Terminal-Bench manifest: ${response.status}`);
    this.manifest = await response.json();
    if (this.manifest.schema_version !== 1 || !this.manifest.versions?.length) throw new Error("Invalid Terminal-Bench manifest");
    const url = new URL(location.href);
    await this.select(url.searchParams.get("tb") || this.manifest.current_version, url.searchParams.get("tb-snapshot"));
  }
  async select(versionId, snapshotId) {
    const sequence = ++this.sequence;
    const version = this.manifest.versions.find(item => item.id === versionId) || this.manifest.versions.find(item => item.id === this.manifest.current_version);
    const snapshot = version.snapshots.find(item => item.id === snapshotId) || version.snapshots.find(item => item.id === version.current_snapshot);
    this.el("tb-error").textContent = "";
    this.el("tb-snapshot").disabled = true;
    try {
      const response = await fetch(`${snapshot.payload}?v=${REVISION}`);
      if (!response.ok) throw new Error(`Terminal-Bench ${version.id}: ${response.status}`);
      const payload = await response.json();
      if (sequence !== this.sequence) return;
      if (payload.schema_version !== 1 || payload.snapshot.benchmark_version !== version.id || payload.snapshot.id !== snapshot.id || !Array.isArray(payload.rows)) throw new Error("Terminal-Bench snapshot identity mismatch");
      this.version = version; this.payload = payload; this.snapshot = snapshot;
      if (this.metric !== "success" && !payload.counts[this.metric]) this.metric = "success";
      else if (this.metric === "success" && payload.counts.subscription) this.metric = "subscription";
      this.filters = {provider: "", agent: "", minimum: 0, maximum: 100};
      const url = new URL(location.href); url.searchParams.set("tb", version.id); url.searchParams.set("tb-snapshot", snapshot.id); history.replaceState(null, "", url);
      this.render();
    } catch (error) { if (sequence === this.sequence) this.el("tb-error").textContent = String(error); console.error(error); }
    finally { if (sequence === this.sequence) this.el("tb-snapshot").disabled = false; }
  }
  setActive(active, language) {
    this.active = active; this.language = language;
    if (!active && this.el("tb-detail").open) this.el("tb-detail").close();
    if (active) this.render();
  }
  renderShell() {
    if (!this.active) return;
    document.querySelector('[data-i18n="heroTitle"]').textContent = this.t.title;
    document.querySelector('[data-i18n="heroCopy"]').textContent = this.t.lead;
    document.querySelector('[data-i18n="snapshotLabel"]').textContent = this.payload?.benchmark || "Terminal-Bench";
    for (const metric of METRICS) document.getElementById(`${metric}-count`).textContent = this.payload?.counts[metric] ?? "—";
    if (this.snapshot) document.getElementById("selected-release-link").href = this.snapshot.release_url;
  }
  render() {
    this.root.querySelectorAll("[data-tb]").forEach(element => {if (typeof this.t[element.dataset.tb] === "string") element.textContent = this.t[element.dataset.tb];});
    this.renderShell();
    if (!this.payload) return;
    this.el("tb-version").replaceChildren(...this.manifest.versions.map(item => new Option(`Terminal-Bench ${item.id} · ${this.t[item.status]}`, item.id, false, item.id === this.version.id)));
    this.el("tb-snapshot").replaceChildren(...this.version.snapshots.map(item => new Option(item.id, item.id, false, item.id === this.snapshot.id)));
    this.el("tb-time").dateTime = this.snapshot.retrieved_at_utc;
    this.el("tb-time").textContent = utc(this.snapshot.retrieved_at_utc);
    this.el("tb-state").textContent = this.t[this.version.status];
    this.el("tb-state").dataset.state = this.version.status;
    this.el("tb-source-data").href = this.snapshot.data_url;
    this.el("tb-no-usage").hidden = Object.values(this.payload.counts).some(Boolean);
    if (!this.el("tb-no-usage").hidden) this.el("tb-no-usage").textContent = this.t.frontierMissing;
    this.renderFilters(); this.renderRanking(); this.renderCharts(); this.renderEvidence();
  }
  renderFilters() {
    const options = [...METRICS.filter(metric => this.payload.counts[metric]), "success"];
    this.el("tb-metric").replaceChildren(...options.map(metric => new Option(this.t[metric], metric, false, metric === this.metric)));
    for (const [id, key, field, all] of [["tb-provider", "provider", "developer", "allProviders"], ["tb-agent", "agent", "agent", "allAgents"]]) {
      const values = [...new Set(this.payload.rows.map(row => row[field]))].sort();
      this.el(id).replaceChildren(new Option(this.t[all], ""), ...values.map(value => new Option(value, value)));
      this.el(id).value = this.filters[key];
    }
    this.el("tb-min").value = this.filters.minimum; this.el("tb-max").value = this.filters.maximum;
  }
  renderCharts() {
    if (!this.active) return;
    for (const metric of METRICS) {
      const rows = this.payload.rows.filter(row => row[X_KEYS[metric]] != null);
      this.el(`tb-card-${metric}`).hidden = !rows.length;
      if (!rows.length) continue;
      const frontierStem = {subscription: "07_subscription_frontier", api: "08_api_frontier", token: "09_token_frontier"}[metric];
      this.el(`tb-image-${metric}`).href = `${this.snapshot.chart_base}/${this.language}/${frontierStem}.png`;
      this.el(`tb-frontier-csv-${metric}`).href = `${this.snapshot.ranking_base}/${metric}_frontier.csv`;
      let chart = this.charts.get(metric);
      if (!chart) {chart = new InteractiveScatterChart(this.el(`tb-chart-${metric}`)); this.charts.set(metric, chart);}
      const t = this.t, xKey = X_KEYS[metric];
      const displayValue = value => metric === "token" ? `${Number(value).toFixed(3)}M` : usd(value);
      const name = row => `${row.base_model} · ${this.effort(row)} · ${row.agent}`;
      chart.update(rows, {metric: `terminal-${metric}`, dataRevision: `${this.version.id}:${this.snapshot.id}`, xKey, yDomain: [0, 100], showConfidenceIntervals: true,
        showParetoFrontier: this.el(`tb-frontier-toggle-${metric}`).checked, paretoLabel: t[metric === "token" ? "tokenFrontier" : "costFrontier"],
        onFilteredRows: (filtered, frontier) => this.renderFrontierList(metric, frontier),
        providerControlLabel: t.provider, allProvidersLabel: t.allProviders, modelScopeControlLabel: t.agent, allModelsScopeLabel: t.allAgents, scopeMode: "field", scopeField: "agent",
        zoomInLabel: t.zoomIn, zoomOutLabel: t.zoomOut, resetLabel: t.reset, interactionHint: t.interact, readoutHint: t.readout,
        xAxisLabel: t[`${metric}Axis`], yAxisLabel: t.yAxis, accessibleTitle: `${this.payload.benchmark}: ${t[metric]}`, accessibleDescription: t.chartHint,
        effortLabel: effort => this.effort({effort}), formatScoreTick: value => `${Number(value).toFixed(0)}%`, formatXAxisTick: value => metric === "token" ? Number(value).toFixed(1) : `$${Number(value).toFixed(2)}`,
        pointLabel: name, tooltipRows: row => [[t.rate, this.rate(row)], [t.attempt, displayValue(row[xKey])], [t.resolved, metric === "token" ? millions(row.tokens_per_success) : usd(row[RANK_KEYS[metric]])], [t.trials, row.trials ?? t.unknown], [t.runtime, this.duration(row)], [t.access, metric === "subscription" ? row.access_label : "API"], ...(metric === "subscription" ? [[t.confidence, t[row.access_confidence] || row.access_confidence]] : [])],
        readoutText: row => `${name(row)} · ${this.rate(row)} · ${displayValue(row[xKey])}`,
        pointAriaLabel: row => `${name(row)}: ${this.rate(row)}, ${displayValue(row[xKey])}`,
      });
    }
  }
  renderFrontierList(metric, rows) {
    const t = this.t, format = metric === "token" ? millions : usd;
    this.el(`tb-frontier-count-${metric}`).textContent = `${rows.length} ${t.frontierCount} · ${t.frontierOrder}`;
    const headers = [t.model, t.agent, t.rate, t.attempt, t.resolved, t.trials, ...(metric === "subscription" ? [t.access, t.confidence] : []), t.details];
    this.el(`tb-frontier-table-${metric}`).innerHTML = `<thead><tr>${headers.map(value => `<th>${escape(value)}</th>`).join("")}</tr></thead><tbody>${rows.map(row => `<tr data-frontier-id="${escape(row.id)}"><td class="tb-model"><strong>${escape(row.base_model)}</strong><span class="tb-effort">${escape(this.effort(row))}</span></td><td>${escape(row.agent)}</td><td>${this.rate(row)}</td><td>${format(metric === "token" ? row.token_per_attempt : row[X_KEYS[metric]])}</td><td>${format(row[RANK_KEYS[metric]])}</td><td>${row.trials ?? "—"}</td>${metric === "subscription" ? `<td class="tb-frontier-access">${escape(row.access_label)}</td><td>${escape(t[row.access_confidence] || row.access_confidence)}</td>` : ""}<td><button class="tb-detail-button" type="button" data-result-id="${escape(row.id)}">${t.details}</button></td></tr>`).join("") || `<tr><td colspan="${headers.length}">${t.empty}</td></tr>`}</tbody>`;
    this.el(`tb-frontier-table-${metric}`).querySelectorAll("[data-result-id]").forEach(button => button.addEventListener("click", () => this.showDetails(button.dataset.resultId)));
  }
  rate(row) {return `${row.score.toFixed(2)}%${row.ci95_half_width == null ? "" : ` ± ${row.ci95_half_width.toFixed(2)}`}`;}
  duration(row) {return row.avg_trial_duration_sec == null ? "—" : `${(row.avg_trial_duration_sec / 60).toFixed(1)} min`;}
  renderRanking() {
    if (!this.payload) return;
    const t = this.t, successOnly = this.metric === "success";
    const rows = rankTerminalRows(this.payload.rows, this.metric, this.filters);
    const headers = [t.rank, t.model, t.agent, t.rate, t.trials, ...(!successOnly ? [t.perAttempt, t.perSuccess, t.relativeCost, t.relativeValue] : []), t.runtime, t.details];
    this.el("tb-table-head").innerHTML = `<tr>${headers.map(header => `<th scope="col">${escape(header)}</th>`).join("")}</tr>`;
    const successHint = Object.values(this.payload.counts).some(Boolean) ? "successRankingHint" : "missingConsumptionHint";
    this.el("tb-ranking-hint").textContent = t[successOnly ? successHint : this.metric === "token" ? "tokenRankingHint" : "rankingHint"];
    this.el("tb-result-count").textContent = rows === null ? t.rangeError : `${rows.length} ${t.visible}`;
    this.el("tb-csv").href = `${this.snapshot.ranking_base}/${successOnly ? "success_rate" : this.metric}_ranking.csv`;
    if (!rows?.length) {this.el("tb-table-body").innerHTML = `<tr><td colspan="${headers.length}">${escape(rows === null ? t.rangeError : t.empty)}</td></tr>`; return;}
    this.el("tb-table-body").innerHTML = rows.map(row => {
      const format = this.metric === "token" ? millions : usd;
      const attempt = this.metric === "token" ? row.token_per_attempt : row[X_KEYS[this.metric]];
      const costCells = successOnly ? "" : `<td>${format(attempt)}</td><td class="tb-primary-value">${format(row[RANK_KEYS[this.metric]])}</td><td>${row.relativeCost.toFixed(2)}%</td><td>${row.relativeValue.toFixed(2)}%</td>`;
      const access = this.metric === "subscription" ? `<small class="tb-access">${escape(row.access_label)} · ${escape(t[row.access_confidence] || row.access_confidence)}</small>` : "";
      const unverified = row.source_verified === false ? `<span class="tb-unverified">${t.unverified}</span>` : "";
      return `<tr><td>${row.rank}</td><td class="tb-model"><strong>${escape(row.base_model)}</strong><span class="tb-effort">${escape(this.effort(row))}</span>${unverified}${access}</td><td>${escape(row.agent)}</td><td>${this.rate(row)}</td><td>${row.trials ?? "—"}</td>${costCells}<td>${this.duration(row)}</td><td><button type="button" class="tb-detail-button" data-result-id="${escape(row.id)}">${t.details}</button></td></tr>`;
    }).join("");
    this.el("tb-table-body").querySelectorAll("[data-result-id]").forEach(button => button.addEventListener("click", () => this.showDetails(button.dataset.resultId)));
  }
  showDetails(id) {
    const row = this.payload.rows.find(item => item.id === id), t = this.t;
    if (!row) return;
    const fields = [[t.agent, `${row.agent} · ${row.agent_version || t.missingVersion}`], [t.rate, this.rate(row)], [t.trials, row.trials ?? t.unknown], [t.taskCount, row.task_count ?? t.unknown], [t.rawTokens, row.total_tokens?.toLocaleString("en-US") ?? "—"], [t.rawCost, usd(row.total_api_usd)], [t.rawInput, row.raw_named_uncached_input_tokens?.toLocaleString("en-US") ?? "—"], [t.rawCache, row.raw_cached_input_tokens?.toLocaleString("en-US") ?? "—"], [t.rawOutput, row.raw_output_tokens?.toLocaleString("en-US") ?? "—"], [t.tokenFields, row.component_semantics], [t.access, row.access_label || t.statuses[row.access_rule] || t.unavailable], [t.confidence, t[row.access_confidence] || row.access_confidence], [t.evidence, row.access_evidence_date || "—"]];
    fields.push([t.verification, row.source_verified == null ? t.unknown : String(row.source_verified)]);
    fields.push(["Record ID", row.id], [this.language === "zh-CN" ? "记录日期" : "Record date", row.submission_date || t.unknown]);
    if (row.trial_count_note.startsWith("metrics_count_preferred")) {
      fields.push([this.language === "zh-CN" ? "分母差异" : "Denominator discrepancy", `metrics.n_trials = ${row.raw_metrics_n_trials}; associations = ${row.raw_associated_n_trials}. ${this.language === "zh-CN" ? "采用评测计数；差异原因未核实。" : "Use the metrics count; discrepancy cause is unverified."}`]);
    }
    if (row.cost_note === "owner_cost_reporting_caveat") fields.push([t.rawCost, this.language === "zh-CN" ? "评测方提示成本上报不可靠，不纳入成本图。" : "Owner flags unreliable cost reporting; excluded from cost charts."]);
    if (row.subscription_offpeak_per_attempt != null) {fields.push([t.offpeak, usd(row.subscription_offpeak_per_attempt)], [t.monthly, usd(row.subscription_per_attempt * this.payload.access_policy.glm.month_to_month_usd / this.payload.access_policy.glm.monthly_usd)]);}
    this.el("tb-detail-content").innerHTML = `<h2>${escape(row.base_model)} · ${escape(this.effort(row))}</h2><dl>${fields.map(([key, value]) => `<dt>${escape(key)}</dt><dd>${escape(value)}</dd>`).join("")}</dl><p class="tb-note">${t.rawWarning}</p><p><a href="${escape(row.source_url)}" target="_blank" rel="noreferrer">${t.source}</a></p>${row.access_sources.map(source => `<p><a href="${escape(source)}" target="_blank" rel="noreferrer">${escape(source)}</a></p>`).join("")}`;
    this.el("tb-detail").showModal();
  }
  renderEvidence() {
    const t = this.t;
    const excluded = this.payload.rows.filter(row => row.access_kind === "excluded");
    this.el("tb-exclusions").innerHTML = `<ul>${excluded.map(row => `<li><strong>${escape(row.base_model)} · ${escape(row.agent)} · ${escape(this.effort(row))}</strong> — ${escape(t.statuses[row.access_rule] || row.access_rule)}</li>`).join("")}</ul>`;
    const rules = [...new Set(this.payload.rows.filter(row => row.access_kind === "subscription_estimate").map(row => row.access_rule))];
    const policies = Object.values(this.payload.access_policy).filter(value => typeof value === "object" && value !== null && rules.includes(value.id));
    this.el("tb-evidence").innerHTML = policies.map(rule => `<article><h3>${escape(rule.plan)}</h3><p>${escape(rule.evidence_date)} · ${escape(t[rule.confidence])}${rule.api_value_ratio ? ` · API-value ratio ${rule.api_value_ratio}×` : ""}</p><p>${escape(this.language === "zh-CN" ? rule.assumptions_zh || rule.assumptions : rule.assumptions)}</p>${rule.sources.map(source => `<a href="${escape(source)}" target="_blank" rel="noreferrer">${escape(new URL(source).hostname)}</a>`).join(" · ")}</article>`).join("");
    this.el("tb-downloads").innerHTML = `<a href="${escape(this.snapshot.release_url)}" target="_blank" rel="noreferrer">${t.download}</a><ul>${(this.payload.exports[this.language] || []).filter(name => name.endsWith(".png")).map(name => `<li><a href="${escape(`${this.snapshot.chart_base}/${this.language}/${name}`)}" target="_blank" rel="noreferrer">${escape(name)}</a></li>`).join("")}</ul>`;
    this.el("tb-sources").innerHTML = `<a href="${escape(this.payload.owner_url)}" target="_blank" rel="noreferrer">Terminal-Bench ${escape(this.version.id)}</a><a href="https://www.tbench.ai/news/terminal-bench-4-0" target="_blank" rel="noreferrer">Terminal-Bench 4.0 · ${t.method}</a><a href="${escape(this.snapshot.data_url)}" target="_blank" rel="noreferrer">JSON / CSV / SHA-256</a>`;
  }
}
