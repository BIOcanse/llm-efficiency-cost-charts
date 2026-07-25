const translations = {
  en: {
    brand: "LLM Efficiency & Cost",
    navCharts: "Charts",
    navRankings: "Rankings",
    navMethod: "Method",
    snapshotLabel: "Snapshot · 2026-07-24",
    heroTitle: "LLM efficiency and task cost, with the numbers shown",
    heroCopy:
      "Three matched-benchmark charts plus full numerical rankings. Every point is one model and reasoning level; upper left is better.",
    viewRankings: "View rankings",
    downloadRelease: "Download complete set",
    openRepository: "Open repository",
    tokenConfigurations: "Token configurations",
    apiConfigurations: "API-cost configurations",
    subscriptionConfigurations: "Subscription-first configurations",
    chartSectionEyebrow: "Matched benchmark · three views",
    chartSectionTitle: "Charts and detailed explanations",
    chartSectionCopy:
      "All three charts use the same Intelligence Index v4.1 score. The horizontal metric changes, so the conclusions must remain separate.",
    chart1Title: "Total Token consumption vs. score",
    chart1Lead:
      "How many input, reasoning, and final-answer Tokens are needed to complete the same suite.",
    chart2Title: "API cost per task vs. score",
    chart2Lead:
      "Fixed-provider prices combined with the actual Token composition of one benchmark task.",
    chart3Title: "Subscription-first cost per task vs. score",
    chart3Lead:
      "The best quantifiable plan is used first; API is used only when no applicable plan exists.",
    rankingEyebrow: "Actual values · not estimated from plot positions",
    rankingTitle: "Numerical rankings",
    rankingCopy:
      "Cost tables show exact USD per task. Token efficiency aggregates the full observed reasoning-level curve instead of selecting one favorable point.",
    tabSubscription: "Subscription cost",
    tabToken: "Aggregate Token efficiency",
    tabApi: "API cost",
    subscriptionRankingTitle: "Subscription-first cost ranking",
    subscriptionRankingCopy:
      "All 46 included configurations, sorted by effective USD per Intelligence Index task. Score is shown separately.",
    downloadCsv: "Download CSV",
    subscriptionThresholdTitle:
      "Lowest subscription-first cost at each score threshold",
    thresholdCopy:
      "This avoids calling the cheapest low-score configuration the best overall value.",
    tokenRankingTitle: "Aggregate full-curve Token efficiency",
    tokenRankingCopy:
      "100 means the model curve matches the observed same-score Token frontier. Lower values mean more Token overhead.",
    limitedEvidenceTitle: "Limited-evidence models",
    limitedEvidenceCopy:
      "These models have only two or three observed levels, or cover less than eight score points. They are listed separately.",
    apiRankingTitle: "API cost ranking",
    apiRankingCopy:
      "All 68 configurations with comparable API prices, sorted by recalculated USD per task.",
    apiThresholdTitle: "Lowest API cost at each score threshold",
    methodEyebrow: "Scope and evidence",
    methodTitle: "What these rankings do and do not mean",
    chartGuideLink: "Detailed chart guide",
    rankingMethodLink: "Ranking methodology",
    sourcesLink: "Sources",
    dataLink: "Current data",
    footerNote:
      "Personal data compilation based on public benchmark and pricing information. Snapshot results do not represent every workload.",
    showAll: (count) => `Show all ${count}`,
    showTop: "Show top 15",
    statusLanguage: "Language changed to English",
    table: {
      rank: "Rank",
      model: "Model",
      level: "Reasoning level",
      score: "Score",
      cost: "USD / task",
      access: "Access",
      confidence: "Confidence",
      levels: "Levels",
      scoreRange: "Score range",
      index: "Efficiency index",
      overhead: "Token overhead",
      provider: "Provider",
      totalTokens: "Total Tokens",
      threshold: "Minimum score",
    },
    tokenMethod:
      "<strong>Method:</strong> compare each model’s interpolated full-level curve with the observed global Token frontier at the same scores. The index is 100 divided by the score-range-weighted geometric mean Token overhead. Core ranking requires at least four levels and an eight-point score span.",
    chartDetails: [
      [
        {
          title: "Axes and marks",
          body:
            "<ul><li>Y: Intelligence Index v4.1 score.</li><li>X: complete-suite Tokens in millions.</li><li>One point: model + reasoning level.</li><li>Same-color line: levels of one model.</li></ul>",
        },
        {
          title: "Calculation",
          body:
            "<p>Total Tokens = input + reasoning + final answer. The black outline marks configurations that are not beaten on both score and Token consumption.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>This measures a model-and-level configuration, not a model independently of its inference budget. It does not imply API or subscription cost, and equally named levels can use different budgets.</p>",
        },
      ],
      [
        {
          title: "Axes and marks",
          body:
            "<ul><li>Y: Intelligence Index v4.1 score.</li><li>X: USD to complete one benchmark task.</li><li>68 configurations have comparable cost data.</li></ul>",
        },
        {
          title: "Calculation",
          body:
            "<p>Standard input, cache reads/writes, reasoning, and final-answer Tokens are multiplied by one fixed provider price schedule per original model. Quantized endpoints do not replace original models.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>This combines Token price and Token consumption for this benchmark. Cache rates, answer length, and task difficulty can change real-world costs. Four models without comparable cost data are excluded.</p>",
        },
      ],
      [
        {
          title: "Inclusion order",
          body:
            "<ol><li>Use the best quantifiable applicable plan.</li><li>Exclude plans without reliable quota data.</li><li>Use API only when no applicable model plan exists.</li></ol>",
        },
        {
          title: "Evidence",
          body:
            "<p>OpenAI and Claude use medium-confidence API-equivalent estimates from exhausting limits. MiMo uses official quota rules; GLM uses an official multiplier plus a reproducible reconstruction. Claude uses the current standard post-promotion estimate only.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>This is effective cost per benchmark task, not a provider-promised monthly Token quota. Grok, Gemini, Kimi, Qwen, MiniMax, Mistral, and others are excluded because their plan quota cannot be quantified reliably.</p>",
        },
      ],
    ],
    methodCards: [
      {
        title: "One benchmark, not every workload",
        body:
          "The Intelligence Index v4.1 suite emphasizes relatively difficult coding and scientific tasks. Rankings can change on lightweight, repetitive, or latency-sensitive workloads.",
      },
      {
        title: "Capability and cost stay separate",
        body:
          "Raw cost tables always show score beside cost. Threshold tables answer the more useful question: the cheapest configuration that reaches at least a chosen score.",
      },
      {
        title: "Estimated quotas remain estimates",
        body:
          "OpenAI and Claude subscription values are third-party API-equivalent estimates, not fixed Token quotas promised by the providers. Confidence is displayed in the table.",
      },
    ],
  },
  "zh-CN": {
    brand: "大模型效率与成本",
    navCharts: "图表",
    navRankings: "排名",
    navMethod: "方法",
    snapshotLabel: "数据快照 · 2026-07-24",
    heroTitle: "大模型效率与任务成本，直接列出实际数据",
    heroCopy:
      "三张同口径统计图，加上完整数值排名。每个点代表一个模型和思考档位，越靠左上越好。",
    viewRankings: "查看排名",
    downloadRelease: "下载整套成图",
    openRepository: "打开仓库",
    tokenConfigurations: "Token 消耗配置",
    apiConfigurations: "API 成本配置",
    subscriptionConfigurations: "套餐优先配置",
    chartSectionEyebrow: "同一套评测 · 三种指标",
    chartSectionTitle: "图表与详细说明",
    chartSectionCopy:
      "三张图使用同一套 Intelligence Index v4.1 分数，但横轴指标不同，因此 Token 效率、API 成本和套餐成本必须分别解读。",
    chart1Title: "完整 Token 消耗与跑分",
    chart1Lead: "完成同一套评测需要多少输入、推理和最终回答 Token。",
    chart2Title: "API 单位任务成本与跑分",
    chart2Lead: "按统一供应商价格和每项任务的实际 Token 构成计算。",
    chart3Title: "套餐优先单位任务成本与跑分",
    chart3Lead: "优先使用可核算的最优套餐；只有不存在适用套餐时才使用 API。",
    rankingEyebrow: "直接列数值 · 不再从散点位置估算",
    rankingTitle: "数值排名",
    rankingCopy:
      "成本表直接列出每项任务的美元成本。Token 效率综合同一模型的完整档位曲线，不挑单个最好看的点。",
    tabSubscription: "套餐成本",
    tabToken: "综合 Token 效率",
    tabApi: "API 成本",
    subscriptionRankingTitle: "套餐优先单位任务成本排名",
    subscriptionRankingCopy:
      "列出全部 46 个纳入配置，按每个 Intelligence Index 任务的有效成本从低到高排序，分数单独展示。",
    downloadCsv: "下载 CSV",
    subscriptionThresholdTitle: "达到不同分数门槛的最低套餐优先成本",
    thresholdCopy: "避免把分数很低但最便宜的配置直接称为整体性价比最高。",
    tokenRankingTitle: "综合全档位 Token 效率",
    tokenRankingCopy:
      "100 代表整条档位曲线处于同分数全局 Token 前沿；数值越低，平均额外 Token 越多。",
    limitedEvidenceTitle: "有限样本模型",
    limitedEvidenceCopy:
      "这些模型只有两至三个已测档位，或覆盖不到 8 个分数点，因此单独列出，不参与核心排名。",
    apiRankingTitle: "API 单位任务成本排名",
    apiRankingCopy: "列出 68 个存在可比 API 价格的配置，按重算后的任务成本排序。",
    apiThresholdTitle: "达到不同分数门槛的最低 API 成本",
    methodEyebrow: "范围与证据",
    methodTitle: "排名能够说明什么，不能说明什么",
    chartGuideLink: "图片详细说明",
    rankingMethodLink: "排名计算方法",
    sourcesLink: "数据来源",
    dataLink: "当前数据",
    footerNote:
      "个人根据公开评测与价格资料整理。快照结果只代表同一套评测，不代表所有实际任务。",
    showAll: (count) => `显示全部 ${count} 项`,
    showTop: "只显示前 15 项",
    statusLanguage: "已切换为中文",
    table: {
      rank: "排名",
      model: "模型",
      level: "思考档位",
      score: "分数",
      cost: "美元 / 任务",
      access: "获取方式",
      confidence: "置信度",
      levels: "档位数",
      scoreRange: "覆盖分数",
      index: "效率指数",
      overhead: "Token 倍率",
      provider: "供应商",
      totalTokens: "完整 Token",
      threshold: "最低分数",
    },
    tokenMethod:
      "<strong>计算方法：</strong>将每个模型的完整档位曲线与同分数下的全局最省 Token 前沿比较，在覆盖分数区间内计算几何平均额外 Token。效率指数等于 100 除以该倍率。核心榜至少需要 4 个档位并覆盖 8 分。",
    chartDetails: [
      [
        {
          title: "坐标与标记",
          body:
            "<ul><li>纵轴：Intelligence Index v4.1 分数。</li><li>横轴：整套评测完整 Token，单位为百万。</li><li>每点：模型与思考档位。</li><li>同色线：同一模型的不同档位。</li></ul>",
        },
        {
          title: "计算方法",
          body:
            "<p>完整 Token = 输入 + 推理 + 最终回答。黑色外圈表示当前纳入配置的 Pareto 前沿，即没有其他点能够同时消耗更少 Token 并达到相同或更高分数。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>该图衡量模型与档位的组合，不能脱离推理预算视为模型本体的绝对效率；也不能直接推出 API 或套餐成本。不同厂商名称相同的档位不等于相同预算。</p>",
        },
      ],
      [
        {
          title: "坐标与标记",
          body:
            "<ul><li>纵轴：Intelligence Index v4.1 分数。</li><li>横轴：完成一个评测任务的美元成本。</li><li>当前 68 个配置存在可比成本数据。</li></ul>",
        },
        {
          title: "计算方法",
          body:
            "<p>按普通输入、缓存读写、推理和最终回答 Token 构成，乘以每个原始模型统一选定的供应商价格。同一模型各档位不混用不同低价供应商，量化端点也不替代原模型。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>该图同时包含 Token 单价和消耗量，只代表该套评测。真实任务的缓存比例、输出长度和难度都会改变成本。另有 4 个模型因缺少可比成本数据而排除。</p>",
        },
      ],
      [
        {
          title: "纳入顺序",
          body:
            "<ol><li>存在可核算额度时使用最优适用套餐。</li><li>有套餐但额度无法可靠核算时排除。</li><li>只有不存在适用模型套餐时才使用 API。</li></ol>",
        },
        {
          title: "数据证据",
          body:
            "<p>OpenAI 与 Claude 使用第三方跑满限额的 API 等价值估算；MiMo 使用官方额度；GLM 使用官方倍率和可复核反推。Claude 只保留活动结束后的当前标准额度，不再绘制 +50% 活动期。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>该图表示评测任务的有效成本，不是厂商承诺的固定月度 Token 配额。Grok、Gemini、Kimi、Qwen、MiniMax、Mistral 等因套餐额度无法可靠换算而排除。</p>",
        },
      ],
    ],
    methodCards: [
      {
        title: "只代表同一套评测",
        body:
          "Intelligence Index v4.1 以较难的编码和科学任务为主。轻量、重复、低延迟或其他类型任务中的排名可能不同。",
      },
      {
        title: "能力与成本分开",
        body:
          "原始成本排名始终同时列出分数；门槛表回答更实际的问题：至少达到某个分数时，哪个配置成本最低。",
      },
      {
        title: "估算仍然是估算",
        body:
          "OpenAI 与 Claude 的套餐数据是第三方 API 等价值估算，不是厂商承诺的固定 Token 配额，表格中会同时显示置信度。",
      },
    ],
  },
};

const chartAssets = {
  en: [
    "charts/en/01_total_token_consumption_vs_score",
    "charts/en/02_api_task_cost_vs_score",
    "charts/en/03_subscription_first_task_cost_vs_score",
  ],
  "zh-CN": [
    "charts/zh-CN/01_total_token_consumption_vs_score",
    "charts/zh-CN/02_api_task_cost_vs_score",
    "charts/zh-CN/03_subscription_first_task_cost_vs_score",
  ],
};

const chartAlt = {
  en: [
    "Total Token consumption versus Intelligence Index score",
    "API cost per task versus Intelligence Index score",
    "Subscription-first task cost versus Intelligence Index score",
  ],
  "zh-CN": [
    "完整 Token 消耗与 Intelligence Index 跑分",
    "API 单位任务成本与 Intelligence Index 跑分",
    "套餐优先单位任务成本与 Intelligence Index 跑分",
  ],
};

const effortLabels = {
  en: {
    instant: "Instant",
    "non-reasoning": "Non-reasoning",
    low: "Low",
    medium: "Medium",
    default: "Default",
    high: "High",
    xhigh: "Xhigh",
    max: "Max",
  },
  "zh-CN": {
    instant: "Instant",
    "non-reasoning": "非推理",
    low: "低",
    medium: "中",
    default: "默认",
    high: "高",
    xhigh: "超高",
    max: "Max",
  },
};

const confidenceLabels = {
  en: { high: "High", medium: "Medium", low: "Low", "": "—" },
  "zh-CN": { high: "高", medium: "中", low: "低", "": "—" },
};

const state = {
  language: "en",
  rankings: null,
  expanded: {
    subscription: false,
    api: false,
  },
};

function browserLanguage() {
  try {
    const saved = window.localStorage.getItem("llm-efficiency-language");
    if (saved === "en" || saved === "zh-CN") {
      return saved;
    }
  } catch {
    // Local storage may be disabled; the visible language buttons still work.
  }
  const languages = Array.isArray(navigator.languages)
    ? navigator.languages
    : [navigator.language || "en"];
  return languages.some((language) => language.toLowerCase().startsWith("zh"))
    ? "zh-CN"
    : "en";
}

function translateStaticText() {
  const text = translations[state.language];
  document.documentElement.lang = state.language;
  document.title =
    state.language === "zh-CN"
      ? "大模型效率与任务成本图"
      : "LLM Efficiency & Cost Charts";
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (typeof text[key] === "string") {
      element.textContent = text[key];
    }
  });
  document.querySelectorAll("[data-language]").forEach((button) => {
    const selected = button.dataset.language === state.language;
    button.setAttribute("aria-pressed", String(selected));
  });
}

function renderChartDetails() {
  const text = translations[state.language];
  text.chartDetails.forEach((blocks, chartIndex) => {
    const target = document.getElementById(`chart${chartIndex + 1}-details`);
    target.innerHTML = blocks
      .map(
        (block) =>
          `<section class="detail-block"><h4>${block.title}</h4>${block.body}</section>`,
      )
      .join("");
  });

  chartAssets[state.language].forEach((base, index) => {
    const chartNumber = index + 1;
    const png = `${base}.png`;
    const svg = `${base}.svg`;
    const image = document.getElementById(`chart${chartNumber}-image`);
    image.src = png;
    image.alt = chartAlt[state.language][index];
    document.getElementById(`chart${chartNumber}-link`).href = png;
    document.getElementById(`chart${chartNumber}-png`).href = png;
    document.getElementById(`chart${chartNumber}-svg`).href = svg;
  });
}

function renderMethodCards() {
  const cards = translations[state.language].methodCards;
  document.getElementById("method-grid").innerHTML = cards
    .map(
      (card) =>
        `<article class="method-card"><h3>${card.title}</h3><p>${card.body}</p></article>`,
    )
    .join("");
}

function formatScore(value) {
  return Number(value).toFixed(2);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatUsd(value) {
  const numeric = Number(value);
  if (numeric < 0.01) {
    return `$${numeric.toFixed(6)}`;
  }
  if (numeric < 1) {
    return `$${numeric.toFixed(4)}`;
  }
  return `$${numeric.toFixed(3)}`;
}

function formatTokens(value) {
  return `${Number(value).toFixed(1)}M`;
}

function effortLabel(value) {
  return effortLabels[state.language][value] || value;
}

function accessLabel(row) {
  if (row.access_mode && row.access_mode.startsWith("subscription_")) {
    return row.plan_name;
  }
  return "API";
}

function tableHeader(targetId, columns) {
  const labels = translations[state.language].table;
  document.getElementById(targetId).innerHTML = `<tr>${columns
    .map((column) => `<th scope="col">${labels[column]}</th>`)
    .join("")}</tr>`;
}

function renderSubscriptionRanking() {
  const rows = state.rankings.subscription_cost;
  const visibleRows = state.expanded.subscription ? rows : rows.slice(0, 15);
  tableHeader("subscription-head", [
    "rank",
    "model",
    "level",
    "score",
    "cost",
    "access",
    "confidence",
  ]);
  document.getElementById("subscription-body").innerHTML = visibleRows
    .map(
      (row) => `<tr>
        <td class="rank-cell">${row.rank}</td>
        <td class="model-cell">${escapeHtml(row.model)}</td>
        <td>${escapeHtml(effortLabel(row.effort))}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${escapeHtml(accessLabel(row))}</td>
        <td>${escapeHtml(confidenceLabels[state.language][row.confidence] || row.confidence)}</td>
      </tr>`,
    )
    .join("");
  const toggle = document.querySelector('[data-table-toggle="subscription"]');
  toggle.textContent = state.expanded.subscription
    ? translations[state.language].showTop
    : translations[state.language].showAll(rows.length);
}

function renderTokenRankingTable(rows, headId, bodyId) {
  tableHeader(headId, [
    "rank",
    "model",
    "levels",
    "scoreRange",
    "index",
    "overhead",
  ]);
  document.getElementById(bodyId).innerHTML = rows
    .map(
      (row) => `<tr>
        <td class="rank-cell">${row.rank}</td>
        <td class="model-cell">${escapeHtml(row.model)}</td>
        <td>${row.levels}</td>
        <td>${formatScore(row.score_min)}–${formatScore(row.score_max)}</td>
        <td>${Number(row.efficiency_index).toFixed(2)}</td>
        <td>${Number(row.token_overhead_vs_frontier).toFixed(2)}×</td>
      </tr>`,
    )
    .join("");
}

function renderTokenRanking() {
  const token = state.rankings.token_efficiency;
  document.getElementById("token-method-callout").innerHTML =
    translations[state.language].tokenMethod;
  renderTokenRankingTable(token.core, "token-head", "token-body");
  renderTokenRankingTable(
    token.limited,
    "token-limited-head",
    "token-limited-body",
  );
}

function renderApiRanking() {
  const rows = state.rankings.api_cost;
  const visibleRows = state.expanded.api ? rows : rows.slice(0, 15);
  tableHeader("api-head", [
    "rank",
    "model",
    "level",
    "score",
    "cost",
    "provider",
    "totalTokens",
  ]);
  document.getElementById("api-body").innerHTML = visibleRows
    .map(
      (row) => `<tr>
        <td class="rank-cell">${row.rank}</td>
        <td class="model-cell">${escapeHtml(row.model)}</td>
        <td>${escapeHtml(effortLabel(row.effort))}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${escapeHtml(row.provider)}</td>
        <td>${formatTokens(row.total_tokens_million)}</td>
      </tr>`,
    )
    .join("");
  const toggle = document.querySelector('[data-table-toggle="api"]');
  toggle.textContent = state.expanded.api
    ? translations[state.language].showTop
    : translations[state.language].showAll(rows.length);
}

function renderThresholdTable(rows, headId, bodyId) {
  tableHeader(headId, ["threshold", "model", "level", "score", "cost", "access"]);
  document.getElementById(bodyId).innerHTML = rows
    .map(
      (row) => `<tr>
        <td>≥ ${row.score_threshold}</td>
        <td class="model-cell">${escapeHtml(row.model)}</td>
        <td>${escapeHtml(effortLabel(row.effort))}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${escapeHtml(row.plan_name || row.provider)}</td>
      </tr>`,
    )
    .join("");
}

function renderRankings() {
  if (!state.rankings) {
    return;
  }
  const counts = state.rankings.counts;
  document.getElementById("token-count").textContent =
    counts.token_configurations;
  document.getElementById("api-count").textContent =
    counts.api_cost_configurations;
  document.getElementById("subscription-count").textContent =
    counts.subscription_first_configurations;
  renderSubscriptionRanking();
  renderTokenRanking();
  renderApiRanking();
  renderThresholdTable(
    state.rankings.thresholds.subscription_first,
    "subscription-threshold-head",
    "subscription-threshold-body",
  );
  renderThresholdTable(
    state.rankings.thresholds.api,
    "api-threshold-head",
    "api-threshold-body",
  );
}

function setLanguage(language, remember = true) {
  if (language !== "en" && language !== "zh-CN") {
    return;
  }
  state.language = language;
  if (remember) {
    try {
      window.localStorage.setItem("llm-efficiency-language", language);
    } catch {
      // The control remains functional for the current page without storage.
    }
  }
  translateStaticText();
  renderChartDetails();
  renderMethodCards();
  renderRankings();
  document.getElementById("status").textContent =
    translations[state.language].statusLanguage;
}

function selectRankingTab(tabName) {
  document.querySelectorAll("[data-tab]").forEach((button) => {
    const selected = button.dataset.tab === tabName;
    button.setAttribute("aria-selected", String(selected));
  });
  document.querySelectorAll("[data-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.panel !== tabName;
  });
}

async function loadRankings() {
  const response = await fetch("data/rankings.json");
  if (!response.ok) {
    throw new Error(`Ranking data request failed: ${response.status}`);
  }
  state.rankings = await response.json();
  renderRankings();
}

function bindControls() {
  document.querySelectorAll("[data-language]").forEach((button) => {
    button.addEventListener("click", () => {
      setLanguage(button.dataset.language);
    });
  });
  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      selectRankingTab(button.dataset.tab);
    });
  });
  document.querySelectorAll("[data-table-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const key = button.dataset.tableToggle;
      state.expanded[key] = !state.expanded[key];
      renderRankings();
    });
  });
}

async function main() {
  bindControls();
  setLanguage(browserLanguage(), false);
  selectRankingTab("subscription");
  try {
    await loadRankings();
  } catch (error) {
    document.getElementById("status").textContent = String(error);
    console.error(error);
  }
}

main();
