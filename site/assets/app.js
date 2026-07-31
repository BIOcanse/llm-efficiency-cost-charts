import { InteractiveScatterChart } from "./interactive-scatter.js?v=20260731-coding-agent-suite";

const ASSET_REVISION = "20260731-coding-agent-suite";

const translations = {
  en: {
    brand: "LLM Efficiency & Cost",
    navRecommendations: "My picks",
    navCharts: "Charts",
    navRankings: "Rankings",
    navMethod: "Method",
    snapshotLabel: "Snapshot",
    snapshotVersion: "Snapshot version",
    snapshotPublishedAt: "Snapshot published (UTC)",
    heroTitle: "Same score. How many Tokens? How much money?",
    heroCopy:
      "Each point represents one model and reasoning level. Lines of the same color connect levels of the same model. Upper left is better.",
    viewRankings: "View rankings",
    viewCharts: "View charts",
    downloadRelease: "Download complete set",
    openRepository: "Open repository",
    motionLabel: "Motion",
    motionFull: "Full",
    motionReduced: "Reduced",
    tokenConfigurations: "Token configurations",
    apiConfigurations: "API-cost configurations",
    subscriptionConfigurations: "Subscription-first configurations",
    scenarioEyebrow: "Choose the comparison scenario",
    scenarioTitle: "General capability or actual coding-agent work",
    scenarioGeneralTitle: "General benchmark",
    scenarioGeneralCopy: "Intelligence Index v4.1 · model + reasoning level",
    scenarioCodingTitle: "Actual coding-agent benchmark",
    scenarioCodingCopy: "Coding Agent Index v1.3 · agent + model + setting",
    codingHeroTitle: "What changes when the models actually work inside coding agents?",
    codingHeroCopy:
      "Each point is an agent harness, model, and setting on Coding Agent Index v1.3. Upper left is better.",
    recommendationEyebrow: "Personal opinion",
    recommendationTitle: "Model picks",
    recommendationCopy:
      "Only models with a clear reason to choose them are included.",
    recommendationSnapshot:
      "Based on the 2026-07-31 snapshot",
    sotaRecommendationsTitle: "Frontier SOTA",
    valueRecommendationsTitle: "Value picks",
    recommendations: {
      sota: [
        {
          model: "GPT-5.6 Sol",
          body:
            "First choice. It combines frontier-level capability with unusually strong value.",
        },
        {
          model: "Claude Opus 5",
          body:
            "Its absolute intelligence is slightly higher. It costs more, but that capability edge still leaves it a narrow niche under Sol's pressure.",
        },
        {
          model: "Kimi K3",
          body:
            "The strongest open model and relatively inexpensive, but it cannot match Sol on overall capability or value, so it has no clear practical niche here.",
        },
      ],
      value: [
        {
          model: "GPT-5.6 Luna",
          body:
            "First choice. After the repricing, it reaches a higher score than DeepSeek V4 Pro (Preview) at lower task cost on this benchmark.",
        },
        {
          model: "DeepSeek V4 Pro (Preview)",
          body:
            "Second choice. It remains inexpensive, but the new Luna pricing creates a clear gap.",
        },
      ],
    },
    chartSectionEyebrow: "Matched benchmark · three metrics",
    chartSectionTitle: "Token consumption, subscription cost, and API cost",
    chartSectionCopy:
      "Token efficiency is not the same thing as low cost.",
    chart1Title: "Total Token consumption vs. score",
    chart1Lead:
      "The total Tokens consumed to complete the same benchmark suite.",
    chart2Title: "Subscription-first cost per task vs. score",
    chart2Lead:
      "Use a quantifiable plan when available; otherwise use API pricing.",
    chart3Title: "API cost per task vs. score",
    chart3Lead:
      "The API cost of completing the same benchmark task.",
    codingChartSectionEyebrow: "Coding Agent Index v1.3 · three metrics",
    codingChartSectionTitle:
      "Token consumption, subscription cost, and API cost in coding-agent work",
    codingChartSectionCopy:
      "These are agent-system results, not model-only scores.",
    codingChart1Title: "Total Token consumption vs. Coding Agent Index",
    codingChart1Lead:
      "Average total Tokens consumed by one coding-task attempt.",
    codingChart2Title:
      "Subscription-first cost per task vs. Coding Agent Index",
    codingChart2Lead:
      "Use an applicable quantifiable plan first; otherwise follow the published inclusion rules.",
    codingChart3Title: "API cost per task vs. Coding Agent Index",
    codingChart3Lead:
      "Observed pay-per-token API cost for one coding-task attempt.",
    rankingEyebrow: "USD per task · relative cost · Token efficiency",
    rankingTitle: "Full numerical rankings",
    rankingCopy:
      "Set a score range and the cost-performance rankings update with it.",
    tabSubscription: "Subscription cost",
    tabSubscriptionValue: "Subscription value",
    tabToken: "Aggregate Token efficiency",
    tabApi: "API cost",
    tabApiValue: "API value",
    subscriptionRankingTitle: "Subscription-first cost ranking",
    subscriptionRankingCopy:
      "Sorted by USD per task, with score and relative cost shown alongside it.",
    downloadCsv: "Download CSV",
    subscriptionThresholdTitle:
      "Lowest subscription-first cost at each score threshold",
    subscriptionValueTitle: "Filtered subscription cost-performance",
    subscriptionValueCopy:
      "Set a score range and recalculate. The interval leader is 100%.",
    thresholdCopy:
      "For each minimum score, select the lowest-cost qualifying configuration.",
    tokenRankingTitle: "Aggregate full-curve Token efficiency",
    tokenRankingCopy:
      "100 means the model curve matches the observed same-score Token frontier. Lower values mean more Token overhead.",
    limitedEvidenceTitle: "Limited-evidence models",
    limitedEvidenceCopy:
      "These models have only two or three observed levels, or cover less than eight score points. They are listed separately.",
    apiRankingTitle: "API cost ranking",
    apiRankingCopy:
      "All 68 configurations with comparable API prices, sorted by USD per task.",
    apiThresholdTitle: "Lowest API cost at each score threshold",
    apiValueTitle: "Filtered API cost-performance",
    apiValueCopy:
      "Set a score range and recalculate. The interval leader is 100%.",
    minimumScore: "Minimum score",
    maximumScore: "Maximum score",
    valueMethod:
      "Value index = (score ÷ USD per task) ÷ the best filtered result × 100%.",
    invalidScoreRange:
      "Minimum score must not be greater than maximum score.",
    noValueResults: "No configurations fall inside this score interval.",
    methodEyebrow: "Benchmark · evidence · exclusions",
    methodTitle: "Scope and limitations",
    chartGuideLink: "Detailed chart guide",
    rankingMethodLink: "Ranking methodology",
    sourcesLink: "Sources",
    dataLink: "Current data",
    footerNote:
      "Personal data compilation based on public benchmark and pricing information. Snapshot results do not represent every workload.",
    showAll: (count) => `Show all ${count}`,
    showTop: "Show top 15",
    statusLanguage: "Language changed to English",
    statusSnapshot: (label) => `Snapshot changed to ${label}`,
    statusScenario: (scenario) =>
      scenario === "coding"
        ? "Switched to the coding-agent benchmark"
        : "Switched to the general benchmark",
    statusMotion: (mode) =>
      mode === "reduced" ? "Motion set to reduced" : "Motion set to full",
    interactive: {
      providerControl: "Model provider",
      allProviders: "All providers",
      modelScopeControl: "Frontier model filter",
      allModelsScope: "All models",
      frontierModelsScope: "Best model in each provider tier",
      zoomIn: "Zoom in",
      zoomOut: "Zoom out",
      reset: "Reset view",
      interactionHint:
        "Hover for values · click to pin or clear",
      readoutHint: "No point selected",
      scoreAxis: "Intelligence Index v4.1 score",
      xAxis: {
        token: "Total Token consumption (million)",
        api: "API cost per task (USD)",
        subscription: "Subscription-first cost per task (USD)",
      },
      title: {
        token: "Interactive total Token consumption versus score",
        api: "Interactive API cost per task versus score",
        subscription:
          "Interactive subscription-first cost per task versus score",
      },
      score: "Score",
      totalTokens: "Total Tokens",
      apiCost: "API cost",
      subscriptionCost: "Effective cost",
      developer: "Model provider",
      provider: "Provider",
      access: "Access",
      pointAction: "Press Enter to pin this point",
    },
    codingInteractive: {
      providerControl: "Model provider",
      allProviders: "All providers",
      agentControl: "Agent harness",
      allAgents: "All agent harnesses",
      zoomIn: "Zoom in",
      zoomOut: "Zoom out",
      reset: "Reset view",
      interactionHint: "Hover for values · click to pin or clear",
      readoutHint: "No point selected",
      scoreAxis: "Coding Agent Index v1.3 score",
      xAxis: {
        token: "Average total Tokens per task (million)",
        api: "API cost per coding task (USD)",
        subscription: "Subscription-first cost per coding task (USD)",
      },
      title: {
        token: "Interactive coding-agent Token consumption versus score",
        api: "Interactive coding-agent API task cost versus score",
        subscription:
          "Interactive coding-agent subscription-first task cost versus score",
      },
      score: "Score",
      totalTokens: "Total Tokens",
      apiCost: "API cost",
      subscriptionCost: "Effective cost",
      developer: "Model provider",
      provider: "API route",
      access: "Access",
      agent: "Agent harness",
      wallTime: "Agent wall time",
      components: "Benchmark components",
      partialComponents: "2/3 (partial)",
      completeComponents: "3/3",
      pointAction: "Press Enter to pin this point",
    },
    table: {
      rank: "Rank",
      model: "Model",
      modelAndLevel: "Model / reasoning level",
      level: "Reasoning level",
      score: "Score",
      cost: "USD / task",
      costPercent: "Cost vs. max",
      access: "Access",
      confidence: "Confidence",
      levels: "Levels",
      scoreRange: "Score range",
      index: "Efficiency index",
      overhead: "Token overhead",
      provider: "Provider",
      totalTokens: "Total Tokens",
      threshold: "Minimum score",
      valueIndex: "Value index",
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
            "<p>OpenAI and Claude use medium-confidence API-equivalent estimates from exhausting limits. OpenAI keeps the measured 70x ratio and applies the July 30 Luna/Terra prices. MiMo uses official quota rules; GLM uses an official multiplier plus a reproducible reconstruction. Claude uses the current standard post-promotion estimate only.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>This is effective cost per benchmark task, not a provider-promised monthly Token quota. Grok, Gemini, Kimi, Qwen, MiniMax, Mistral, and others are excluded because their plan quota cannot be quantified reliably.</p>",
        },
      ],
    ],
    codingChartDetails: [
      [
        {
          title: "Axes and marks",
          body:
            "<ul><li>Y: Coding Agent Index v1.3 score.</li><li>X: average total Tokens per coding-task attempt.</li><li>One point: agent harness + model + setting.</li><li>Same-color line: settings of the same agent and model.</li></ul>",
        },
        {
          title: "Calculation",
          body:
            "<p>The source pools Token use across DeepSWE, Terminal-Bench v2, and SWE-Atlas-QnA. Harness policy, tool calls, context reuse, and stopping behavior all affect this number.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>Fifty-one rows contain all three components. Claude Code · Opus 4.6 (medium) has two published components and is retained with a † marker.</p>",
        },
      ],
      [
        {
          title: "Inclusion order",
          body:
            "<ol><li>Use an applicable plan when its allowance can be quantified.</li><li>Exclude a relevant plan whose allowance cannot be converted.</li><li>Use API only when the evaluated route has no applicable subscription.</li></ol>",
        },
        {
          title: "Current access evidence",
          body:
            "<p>Codex uses the dated ChatGPT Pro 20x estimate; Anthropic models in Claude Code use the Claude Max 20x estimate. Cursor Ultra uses its official guaranteed $400 Agent API allowance for $200, a conservative 2x ratio that ignores bonus usage.</p>",
        },
        {
          title: "Excluded here",
          body:
            "<p>Gemini CLI, Grok Build, and Kimi Code CLI have applicable plans but no stable task or Token conversion, so their three rows are excluded instead of being replaced by API pricing.</p>",
        },
      ],
      [
        {
          title: "Axes and marks",
          body:
            "<ul><li>Y: Coding Agent Index v1.3 score.</li><li>X: observed pay-per-token API cost per coding task.</li><li>All 52 source-table configurations are included.</li></ul>",
        },
        {
          title: "Calculation",
          body:
            "<p>Artificial Analysis applies the evaluated API route's uncached input, cache-read/write, and output pricing to the pooled task traces. The chart does not substitute a cheaper provider.</p>",
        },
        {
          title: "Read with care",
          body:
            "<p>This is the observed cost of the full agent system on this suite. It excludes engineering overhead and does not predict every repository, cache pattern, or supervision policy.</p>",
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
    codingMethodCards: [
      {
        title: "A coding-agent benchmark, not a model-only test",
        body:
          "Each point combines a harness, model, setting, caching behavior, and tool workflow. A difference cannot automatically be attributed to model weights.",
      },
      {
        title: "321 tasks, three components",
        body:
          "The index equally weights DeepSWE, Terminal-Bench v2, and SWE-Atlas-QnA. Each task is attempted three times and averaged at task level.",
      },
      {
        title: "One partial row and estimated plan values",
        body:
          "The Opus 4.6 medium row has two materialized components. OpenAI and Anthropic plan values remain third-party API-equivalent estimates; Cursor uses an official guaranteed allowance.",
      },
    ],
  },
  "zh-CN": {
    brand: "大模型效率与成本",
    navRecommendations: "个人推荐",
    navCharts: "图表",
    navRankings: "排名",
    navMethod: "方法",
    snapshotLabel: "数据快照",
    snapshotVersion: "快照版本",
    snapshotPublishedAt: "快照发布时间（UTC）",
    heroTitle: "同样的跑分，要消耗多少 Token，花多少钱？",
    heroCopy:
      "每个点代表一个模型和思考档位，同色线连接同一模型的不同档位。左上更优。",
    viewRankings: "查看排名",
    viewCharts: "查看图表",
    downloadRelease: "下载完整套图",
    openRepository: "打开仓库",
    motionLabel: "动效",
    motionFull: "正常",
    motionReduced: "减弱",
    tokenConfigurations: "Token 消耗配置",
    apiConfigurations: "API 成本配置",
    subscriptionConfigurations: "套餐优先配置",
    scenarioEyebrow: "选择对比场景",
    scenarioTitle: "通用能力，还是 Agent 实际编码",
    scenarioGeneralTitle: "通用场景",
    scenarioGeneralCopy: "Intelligence Index v4.1 · 模型＋思考档位",
    scenarioCodingTitle: "Agent 实际编码场景",
    scenarioCodingCopy: "Coding Agent Index v1.3 · Agent 工具链＋模型＋档位",
    codingHeroTitle: "模型放进 Agent 里实际写代码，效率和成本会怎样？",
    codingHeroCopy:
      "每个点是一种 Agent 工具链、模型和档位组合，统一使用 Coding Agent Index v1.3。左上更优。",
    recommendationEyebrow: "个人观点",
    recommendationTitle: "模型推荐",
    recommendationCopy: "只列仍有明确选择理由的模型。",
    recommendationSnapshot: "基于 2026-07-31 快照",
    sotaRecommendationsTitle: "顶级 SOTA",
    valueRecommendationsTitle: "性价比模型",
    recommendations: {
      sota: [
        {
          model: "GPT-5.6 Sol",
          body: "首选。顶级能力和性价比同时成立。",
        },
        {
          model: "Claude Opus 5",
          body:
            "绝对智力略高，成本也还能接受；在 Sol 的压迫下仍勉强保留了自己的生态位。",
        },
        {
          model: "Kimi K3",
          body:
            "最强开源模型，成本也比较低；但综合能力和性价比都无法与 Sol 相比，因此实际没有形成明确生态位。",
        },
      ],
      value: [
        {
          model: "GPT-5.6 Luna",
          body:
            "首选。降价后，在该评测中可以用低于 DeepSeek V4 Pro（预览版）的任务成本达到更高分数。",
        },
        {
          model: "DeepSeek V4 Pro（预览版）",
          body: "次选。任务成本仍低，但和新价格下的 Luna 已拉开明显差距。",
        },
      ],
    },
    chartSectionEyebrow: "同一套评测 · 三项指标",
    chartSectionTitle: "Token 消耗、套餐成本与 API 成本",
    chartSectionCopy:
      "Token 效率高，不等于实际成本低。",
    chart1Title: "完整 Token 消耗与跑分",
    chart1Lead: "完成同一套评测实际消耗多少 Token。",
    chart2Title: "套餐优先单位任务成本与跑分",
    chart2Lead: "有可核算套餐时优先使用套餐，否则使用 API。",
    chart3Title: "API 单位任务成本与跑分",
    chart3Lead: "完成同一评测任务需要多少 API 成本。",
    codingChartSectionEyebrow: "Coding Agent Index v1.3 · 三项指标",
    codingChartSectionTitle: "实际编码中的 Token 消耗、套餐成本与 API 成本",
    codingChartSectionCopy: "这里比较的是完整 Agent 系统，不是单独的模型。",
    codingChart1Title: "总 Token 消耗与 Coding Agent Index",
    codingChart1Lead: "平均完成一次编码任务实际消耗多少 Token。",
    codingChart2Title: "套餐优先单任务成本与 Coding Agent Index",
    codingChart2Lead: "优先使用可核算的适用套餐，再按统一规则决定纳入或排除。",
    codingChart3Title: "API 单任务成本与 Coding Agent Index",
    codingChart3Lead: "按量 API 完成一次编码任务的实测成本。",
    rankingEyebrow: "美元/任务 · 相对成本 · Token 效率",
    rankingTitle: "完整数值排名",
    rankingCopy:
      "限定分数区间后，套餐和 API 性价比会重新排序。",
    tabSubscription: "套餐成本",
    tabSubscriptionValue: "套餐性价比",
    tabToken: "综合 Token 效率",
    tabApi: "API 成本",
    tabApiValue: "API 性价比",
    subscriptionRankingTitle: "套餐优先单位任务成本排名",
    subscriptionRankingCopy:
      "按单位任务成本从低到高排序，同时列出分数和相对成本。",
    downloadCsv: "下载 CSV",
    subscriptionThresholdTitle: "达到不同分数门槛的最低套餐优先成本",
    subscriptionValueTitle: "按分数区间重算套餐性价比",
    subscriptionValueCopy:
      "限定分数区间后重新计算，区间第一名为 100%。",
    thresholdCopy: "给定最低分数后，选择单位任务成本最低的配置。",
    tokenRankingTitle: "综合全档位 Token 效率",
    tokenRankingCopy:
      "100 代表整条档位曲线处于同分数全局 Token 前沿；数值越低，平均额外 Token 越多。",
    limitedEvidenceTitle: "有限样本模型",
    limitedEvidenceCopy:
      "这些模型只有两至三个已测档位，或覆盖不到 8 个分数点，因此单独列出，不参与核心排名。",
    apiRankingTitle: "API 单位任务成本排名",
    apiRankingCopy: "列出 68 个存在可比 API 价格的配置，按单位任务成本排序。",
    apiThresholdTitle: "达到不同分数门槛的最低 API 成本",
    apiValueTitle: "按分数区间重算 API 性价比",
    apiValueCopy:
      "限定分数区间后重新计算，区间第一名为 100%。",
    minimumScore: "最低分数",
    maximumScore: "最高分数",
    valueMethod:
      "性价比指数 =（分数 ÷ 美元/任务）÷ 当前筛选结果最高值 × 100%。",
    invalidScoreRange: "最低分数不能高于最高分数。",
    noValueResults: "该分数区间内没有可用配置。",
    methodEyebrow: "评测 · 证据 · 排除项",
    methodTitle: "口径与限制",
    chartGuideLink: "图片详细说明",
    rankingMethodLink: "排名计算方法",
    sourcesLink: "数据来源",
    dataLink: "当前数据",
    footerNote:
      "个人根据公开评测与价格资料整理。快照结果只代表同一套评测，不代表所有实际任务。",
    showAll: (count) => `显示全部 ${count} 项`,
    showTop: "只显示前 15 项",
    statusLanguage: "已切换为中文",
    statusSnapshot: (label) => `已切换至 ${label}`,
    statusScenario: (scenario) =>
      scenario === "coding"
        ? "已切换至 Agent 实际编码场景"
        : "已切换至通用场景",
    statusMotion: (mode) =>
      mode === "reduced" ? "动效已设为减弱" : "动效已设为正常",
    interactive: {
      providerControl: "模型提供商",
      allProviders: "全部提供商",
      modelScopeControl: "最前沿模型筛选",
      allModelsScope: "全部模型",
      frontierModelsScope: "各家各定位最强",
      zoomIn: "放大",
      zoomOut: "缩小",
      reset: "恢复完整视图",
      interactionHint:
        "悬停查看数值 · 点击固定或取消",
      readoutHint: "未选择点位",
      scoreAxis: "Intelligence Index v4.1 分数",
      xAxis: {
        token: "完整 Token 消耗（百万）",
        api: "API 单位任务成本（美元）",
        subscription: "套餐优先单位任务成本（美元）",
      },
      title: {
        token: "完整 Token 消耗与跑分交互图",
        api: "API 单位任务成本与跑分交互图",
        subscription: "套餐优先单位任务成本与跑分交互图",
      },
      score: "分数",
      totalTokens: "完整 Token",
      apiCost: "API 成本",
      subscriptionCost: "有效成本",
      developer: "模型提供商",
      provider: "供应商",
      access: "获取方式",
      pointAction: "按 Enter 可固定该点",
    },
    codingInteractive: {
      providerControl: "模型提供商",
      allProviders: "全部提供商",
      agentControl: "Agent 工具链",
      allAgents: "全部 Agent 工具链",
      zoomIn: "放大",
      zoomOut: "缩小",
      reset: "恢复完整视图",
      interactionHint: "悬停查看数值 · 点击固定或取消",
      readoutHint: "未选择点位",
      scoreAxis: "Coding Agent Index v1.3 分数",
      xAxis: {
        token: "平均单任务总 Token（百万）",
        api: "API 单任务成本（美元）",
        subscription: "套餐优先单任务成本（美元）",
      },
      title: {
        token: "实际编码 Agent 总 Token 消耗交互图",
        api: "实际编码 Agent API 单任务成本交互图",
        subscription: "实际编码 Agent 套餐优先单任务成本交互图",
      },
      score: "分数",
      totalTokens: "总 Token",
      apiCost: "API 成本",
      subscriptionCost: "折算成本",
      developer: "模型提供商",
      provider: "API 路由",
      access: "获取方式",
      agent: "Agent 工具链",
      wallTime: "Agent 执行时间",
      components: "子评测覆盖",
      partialComponents: "2/3（部分）",
      completeComponents: "3/3",
      pointAction: "按 Enter 可固定该点",
    },
    table: {
      rank: "排名",
      model: "模型",
      modelAndLevel: "模型 / 思考档位",
      level: "思考档位",
      score: "分数",
      cost: "美元 / 任务",
      costPercent: "相对最贵",
      access: "获取方式",
      confidence: "置信度",
      levels: "档位数",
      scoreRange: "覆盖分数",
      index: "效率指数",
      overhead: "Token 倍率",
      provider: "供应商",
      totalTokens: "完整 Token",
      threshold: "最低分数",
      valueIndex: "性价比指数",
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
            "<p>OpenAI 与 Claude 使用第三方跑满限额的 API 等价值估算；OpenAI 沿用实测 70 倍比例，并按 7 月 30 日 Luna / Terra 新价格更新。MiMo 使用官方额度；GLM 使用官方倍率和可复核反推。Claude 只保留活动结束后的当前标准额度。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>该图表示评测任务的有效成本，不是厂商承诺的固定月度 Token 配额。Grok、Gemini、Kimi、Qwen、MiniMax、Mistral 等因套餐额度无法可靠换算而排除。</p>",
        },
      ],
    ],
    codingChartDetails: [
      [
        {
          title: "坐标与标记",
          body:
            "<ul><li>纵轴：Coding Agent Index v1.3 分数。</li><li>横轴：平均每次编码任务的总 Token。</li><li>每个点：Agent 工具链＋模型＋档位。</li><li>同色线：同一 Agent 和模型的不同档位。</li></ul>",
        },
        {
          title: "计算方法",
          body:
            "<p>Token 消耗来自 DeepSWE、Terminal-Bench v2 和 SWE-Atlas-QnA 的任务轨迹汇总。Agent 策略、工具调用、上下文复用和停止条件都会影响结果。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>51 个配置覆盖三项子评测；Claude Code · Opus 4.6（medium）只公开了两项，图中以 † 单独标记。</p>",
        },
      ],
      [
        {
          title: "纳入顺序",
          body:
            "<ol><li>有可核算额度时使用适用套餐。</li><li>有适用套餐但额度无法换算时排除。</li><li>只有该评测路径不存在适用套餐时才使用 API。</li></ol>",
        },
        {
          title: "当前套餐口径",
          body:
            "<p>Codex 使用 ChatGPT Pro 20x 的快照估算；Claude Code 中的 Anthropic 模型使用 Claude Max 20x 估算。Cursor Ultra 官方明确 $200/月包含至少 $400 Agent API 用量，因此保守按 2 倍折算，不计无法量化的额外赠送。</p>",
        },
        {
          title: "排除项",
          body:
            "<p>Gemini CLI、Grok Build 和 Kimi Code CLI 虽有适用套餐，但额度无法稳定换算为任务或 Token，因此排除这 3 个点，不用 API 价格替代。</p>",
        },
      ],
      [
        {
          title: "坐标与标记",
          body:
            "<ul><li>纵轴：Coding Agent Index v1.3 分数。</li><li>横轴：按量 API 完成一次编码任务的成本。</li><li>纳入当前榜单全部 52 个配置。</li></ul>",
        },
        {
          title: "计算方法",
          body:
            "<p>Artificial Analysis 按实际评测路由，将普通输入、缓存读写和输出用量乘以对应价格。不会为了压低成本改用另一个便宜供应商。</p>",
        },
        {
          title: "注意事项",
          body:
            "<p>该图反映整套 Agent 系统在这组任务中的成本，不含工程和人工监督开销，也不能直接代表所有代码库、缓存方式或工作流。</p>",
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
    codingMethodCards: [
      {
        title: "这是 Agent 系统评测",
        body:
          "每个点同时受到工具链、模型、档位、缓存和工具调用流程影响，差异不能一概归因于模型本体。",
      },
      {
        title: "321 个任务，三项组成",
        body:
          "指数等权汇总 DeepSWE、Terminal-Bench v2 和 SWE-Atlas-QnA；每个任务运行三次，再按任务计算平均通过率。",
      },
      {
        title: "一项部分数据，部分套餐为估算",
        body:
          "Opus 4.6 medium 只公开两项子评测。OpenAI 与 Anthropic 套餐仍是第三方 API 等价值估算；Cursor 使用官方保证额度。",
      },
    ],
  },
};

const chartAssetStems = {
  en: [
    "en/01_total_token_consumption_vs_score",
    "en/03_subscription_first_task_cost_vs_score",
    "en/02_api_task_cost_vs_score",
  ],
  "zh-CN": [
    "zh-CN/01_total_token_consumption_vs_score",
    "zh-CN/03_subscription_first_task_cost_vs_score",
    "zh-CN/02_api_task_cost_vs_score",
  ],
};

const codingChartAssetStems = {
  en: [
    "en/07_coding_agent_total_tokens_vs_index",
    "en/08_coding_agent_subscription_cost_vs_index",
    "en/09_coding_agent_api_cost_vs_index",
  ],
  "zh-CN": [
    "zh-CN/07_coding_agent_total_tokens_vs_index",
    "zh-CN/08_coding_agent_subscription_cost_vs_index",
    "zh-CN/09_coding_agent_api_cost_vs_index",
  ],
};

const effortLabels = {
  en: {
    instant: "Instant",
    "non-reasoning": "Non-reasoning",
    low: "Low",
    medium: "Medium",
    default: "Default",
    fast: "Fast",
    thinking: "Thinking",
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
    fast: "快速",
    thinking: "思考",
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
  motion: "full",
  scenario: "general",
  rankings: null,
  snapshotManifest: null,
  snapshot: null,
  snapshotLoadSequence: 0,
  coding: null,
  codingSnapshotManifest: null,
  codingSnapshot: null,
  codingSnapshotLoadSequence: 0,
  expanded: {
    subscription: false,
    subscriptionValue: false,
    api: false,
    apiValue: false,
  },
  valueRanges: {
    subscription: { minimum: 0, maximum: 100 },
    api: { minimum: 0, maximum: 100 },
  },
};

const chartInstances = new Map();
const generalInteractiveChartSpecs = [
  {
    scenario: "general",
    instanceKey: "general-token",
    metric: "token",
    dataKey: "token",
    containerId: "chart1-interactive",
    xKey: "total_tokens_million",
  },
  {
    scenario: "general",
    instanceKey: "general-subscription",
    metric: "subscription",
    dataKey: "subscription",
    containerId: "chart2-interactive",
    xKey: "cost_usd_per_task",
  },
  {
    scenario: "general",
    instanceKey: "general-api",
    metric: "api",
    dataKey: "api",
    containerId: "chart3-interactive",
    xKey: "cost_usd_per_task",
  },
];

const codingInteractiveChartSpecs = [
  {
    scenario: "coding",
    instanceKey: "coding-token",
    metric: "token",
    dataKey: "token",
    containerId: "coding-chart1-interactive",
    xKey: "total_tokens_million",
  },
  {
    scenario: "coding",
    instanceKey: "coding-subscription",
    metric: "subscription",
    dataKey: "subscription",
    containerId: "coding-chart2-interactive",
    xKey: "cost_usd_per_task",
  },
  {
    scenario: "coding",
    instanceKey: "coding-api",
    metric: "api",
    dataKey: "api",
    containerId: "coding-chart3-interactive",
    xKey: "cost_usd_per_task",
  },
];

function browserLanguage() {
  const requested = new URL(window.location.href).searchParams.get("lang");
  if (requested === "en" || requested === "zh-CN") {
    return requested;
  }
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

function scenarioPreference() {
  const requested = new URL(window.location.href).searchParams.get("view");
  if (requested === "general" || requested === "coding") {
    return requested;
  }
  try {
    const saved = window.localStorage.getItem("llm-efficiency-scenario");
    if (saved === "general" || saved === "coding") {
      return saved;
    }
  } catch {
    // The visible scenario control still works when storage is disabled.
  }
  return "general";
}

function motionPreference() {
  try {
    const saved = window.localStorage.getItem("llm-efficiency-motion");
    if (saved === "full" || saved === "reduced") {
      return saved;
    }
  } catch {
    // Local storage may be disabled; the visible motion buttons still work.
  }
  return window.matchMedia?.("(prefers-reduced-motion: reduce)").matches
    ? "reduced"
    : "full";
}

function setMotion(mode, remember = true) {
  if (mode !== "full" && mode !== "reduced") {
    return;
  }
  state.motion = mode;
  document.documentElement.dataset.motion = mode;
  if (remember) {
    try {
      window.localStorage.setItem("llm-efficiency-motion", mode);
    } catch {
      // The control remains functional for the current page without storage.
    }
  }
  document.querySelectorAll("[data-motion-choice]").forEach((button) => {
    button.setAttribute(
      "aria-pressed",
      String(button.dataset.motionChoice === mode),
    );
  });
  if (remember) {
    document.getElementById("status").textContent =
      translations[state.language].statusMotion(mode);
  }
}

function savedSnapshotId(defaultSnapshot) {
  const requested = new URL(window.location.href).searchParams.get("snapshot");
  if (requested) {
    return requested;
  }
  try {
    return window.localStorage.getItem("llm-efficiency-snapshot") || defaultSnapshot;
  } catch {
    return defaultSnapshot;
  }
}

function savedCodingSnapshotId(defaultSnapshot) {
  const requested = new URL(window.location.href).searchParams.get(
    "coding-snapshot",
  );
  if (requested) {
    return requested;
  }
  try {
    return (
      window.localStorage.getItem("llm-efficiency-coding-snapshot") ||
      defaultSnapshot
    );
  } catch {
    return defaultSnapshot;
  }
}

function syncUrlState() {
  const url = new URL(window.location.href);
  url.searchParams.set("lang", state.language);
  url.searchParams.set("view", state.scenario);
  if (state.snapshot) {
    url.searchParams.set("snapshot", state.snapshot.id);
  }
  if (state.codingSnapshot) {
    url.searchParams.set("coding-snapshot", state.codingSnapshot.id);
  }
  window.history.replaceState(null, "", url);
}

function snapshotOptionLabel(snapshot) {
  return snapshot.label?.[state.language] || snapshot.id;
}

function formatUtcTimestamp(value) {
  return value.replace("T", " ").replace("Z", " UTC");
}

function renderSnapshotMetadata() {
  const manifest =
    state.scenario === "coding"
      ? state.codingSnapshotManifest
      : state.snapshotManifest;
  const snapshot =
    state.scenario === "coding" ? state.codingSnapshot : state.snapshot;
  if (!manifest || !snapshot) {
    return;
  }
  const text = translations[state.language];
  const select = document.getElementById("snapshot-select");
  select.replaceChildren(
    ...manifest.snapshots.map((candidate) => {
      const option = document.createElement("option");
      option.value = candidate.id;
      option.textContent = snapshotOptionLabel(candidate);
      return option;
    }),
  );
  select.value = snapshot.id;

  document.querySelector('[data-i18n="snapshotLabel"]').textContent =
    `${text.snapshotLabel} · ${snapshot.id}`;
  const time = document.getElementById("snapshot-time");
  time.dateTime = snapshot.published_at_utc;
  time.textContent = formatUtcTimestamp(snapshot.published_at_utc);

  document.getElementById("selected-release-link").href =
    snapshot.release_url;
  document.getElementById("selected-data-link").href = snapshot.data_url;
  if (state.scenario === "general") {
    document.getElementById("subscription-ranking-csv").href =
      `${snapshot.ranking_base}/subscription_cost_ranking.csv`;
    document.getElementById("token-ranking-csv").href =
      `${snapshot.ranking_base}/token_efficiency_ranking.csv`;
    document.getElementById("api-ranking-csv").href =
      `${snapshot.ranking_base}/api_cost_ranking.csv`;
  }
}

function renderRecommendations() {
  const recommendations = translations[state.language].recommendations;
  for (const [key, targetId] of [
    ["sota", "sota-recommendations"],
    ["value", "value-recommendations"],
  ]) {
    document.getElementById(targetId).innerHTML = recommendations[key]
      .map(
        (item, index) => `
          <li class="recommendation-item">
            <span class="recommendation-rank">${index + 1}</span>
            <div>
              <h4>${escapeHtml(item.model)}</h4>
              <p>${escapeHtml(item.body)}</p>
            </div>
          </li>`,
      )
      .join("");
  }
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
  [0, 2, 1].forEach((detailIndex, chartIndex) => {
    const blocks = text.chartDetails[detailIndex];
    const target = document.getElementById(`chart${chartIndex + 1}-details`);
    target.innerHTML = blocks
      .map(
        (block) =>
          `<section class="detail-block"><h4>${block.title}</h4>${block.body}</section>`,
      )
      .join("");
  });

  const chartBase = state.snapshot?.chart_base || "charts";
  chartAssetStems[state.language].forEach((stem, index) => {
    const base = `${chartBase}/${stem}`;
    const chartNumber = index + 1;
    document.getElementById(`chart${chartNumber}-png`).href = `${base}.png`;
    document.getElementById(`chart${chartNumber}-svg`).href = `${base}.svg`;
  });

  text.codingChartDetails.forEach((blocks, index) => {
    const target = document.getElementById(`coding-chart${index + 1}-details`);
    target.innerHTML = blocks
      .map(
        (block) =>
          `<section class="detail-block"><h4>${block.title}</h4>${block.body}</section>`,
      )
      .join("");
  });
  const codingChartBase = state.codingSnapshot?.chart_base || "charts";
  codingChartAssetStems[state.language].forEach((stem, index) => {
    const base = `${codingChartBase}/${stem}`;
    const chartNumber = index + 1;
    document.getElementById(`coding-chart${chartNumber}-png`).href = `${base}.png`;
    document.getElementById(`coding-chart${chartNumber}-svg`).href = `${base}.svg`;
  });
}

function renderMethodCards() {
  const translationsForLanguage = translations[state.language];
  const cards =
    state.scenario === "coding"
      ? translationsForLanguage.codingMethodCards
      : translationsForLanguage.methodCards;
  document.getElementById("method-grid").innerHTML = cards
    .map(
      (card) =>
        `<article class="method-card"><h3>${card.title}</h3><p>${card.body}</p></article>`,
    )
    .join("");
}

function renderMetricCounts() {
  const payload = state.scenario === "coding" ? state.coding : state.rankings;
  if (!payload?.counts) {
    return;
  }
  document.getElementById("token-count").textContent =
    payload.counts.token_configurations;
  document.getElementById("api-count").textContent =
    payload.counts.api_cost_configurations;
  document.getElementById("subscription-count").textContent =
    payload.counts.subscription_first_configurations;
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

function formatCostPercent(value, reference) {
  return `${((Number(value) / Number(reference)) * 100).toFixed(2)}%`;
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

function formatInteractiveAxis(metric, value) {
  const numeric = Number(value);
  if (metric === "token") {
    return new Intl.NumberFormat(state.language, {
      maximumFractionDigits: numeric < 100 ? 1 : 0,
    }).format(numeric);
  }
  if (numeric === 0) {
    return "$0";
  }
  if (numeric < 0.1) {
    return `$${numeric.toFixed(3)}`;
  }
  return `$${numeric.toFixed(2)}`;
}

function formatInteractiveValue(metric, value) {
  return metric === "token" ? formatTokens(value) : formatUsd(value);
}

function interactiveValueLabel(metric, text) {
  if (metric === "token") {
    return text.totalTokens;
  }
  if (metric === "api") {
    return text.apiCost;
  }
  return text.subscriptionCost;
}

function interactiveAccess(metric, row, text) {
  if (metric === "token") {
    return [text.developer, row.developer];
  }
  if (metric === "api") {
    return [text.provider, row.provider];
  }
  return [text.access, accessLabel(row)];
}

function formatDuration(seconds) {
  const numeric = Number(seconds);
  if (numeric < 120) {
    return `${numeric.toFixed(0)} s`;
  }
  return `${(numeric / 60).toFixed(1)} min`;
}

function interactiveChartConfig(spec, pointCount) {
  const isCoding = spec.scenario === "coding";
  const text = isCoding
    ? translations[state.language].codingInteractive
    : translations[state.language].interactive;
  const valueLabel = interactiveValueLabel(spec.metric, text);
  const pointLabel = (row) =>
    `${row.data_scope === "partial" ? "†" : ""}${row.model} · ${effortLabel(row.effort)}`;
  const rowSummary = (row) =>
    `${pointLabel(row)} · ${text.score} ${formatScore(row.score)} · ${valueLabel} ${formatInteractiveValue(spec.metric, row[spec.xKey])}`;
  const snapshot = isCoding ? state.codingSnapshot : state.snapshot;
  const tooltipRows = (row) => {
    const rows = [
      [text.score, formatScore(row.score)],
      [valueLabel, formatInteractiveValue(spec.metric, row[spec.xKey])],
    ];
    if (!isCoding) {
      rows.push(interactiveAccess(spec.metric, row, text));
      return rows;
    }
    rows.push(
      [text.agent, row.agent],
      [text.developer, row.developer],
      spec.metric === "subscription"
        ? [text.access, accessLabel(row)]
        : [text.provider, row.provider],
      [text.wallTime, formatDuration(row.agent_wall_time_sec)],
      [
        text.components,
        row.data_scope === "partial"
          ? text.partialComponents
          : text.completeComponents,
      ],
    );
    return rows;
  };
  return {
    metric: spec.instanceKey,
    dataRevision: `${spec.scenario}:${snapshot?.id || "unloaded"}`,
    xKey: spec.xKey,
    providerControlLabel: text.providerControl,
    allProvidersLabel: text.allProviders,
    modelScopeControlLabel: isCoding
      ? text.agentControl
      : text.modelScopeControl,
    allModelsScopeLabel: isCoding ? text.allAgents : text.allModelsScope,
    frontierModelsScopeLabel: text.frontierModelsScope,
    scopeMode: isCoding ? "field" : "frontier",
    scopeField: isCoding ? "agent" : "",
    zoomInLabel: text.zoomIn,
    zoomOutLabel: text.zoomOut,
    resetLabel: text.reset,
    interactionHint: text.interactionHint,
    readoutHint: text.readoutHint,
    xAxisLabel: text.xAxis[spec.metric],
    yAxisLabel: text.scoreAxis,
    accessibleTitle: text.title[spec.metric],
    accessibleDescription: `${pointCount} points. ${text.interactionHint}.`,
    effortLabel,
    formatScoreTick: (value) => Number(value).toFixed(0),
    formatXAxisTick: (value) => formatInteractiveAxis(spec.metric, value),
    pointLabel,
    tooltipRows,
    readoutText: rowSummary,
    pointAriaLabel: (row) => `${rowSummary(row)}. ${text.pointAction}.`,
  };
}

function renderInteractiveCharts() {
  [...generalInteractiveChartSpecs, ...codingInteractiveChartSpecs].forEach(
    (spec) => {
      if (spec.scenario !== state.scenario) {
        return;
      }
      const payload = spec.scenario === "coding" ? state.coding : state.rankings;
      if (!payload?.charts) {
        return;
      }
      const rows = payload.charts[spec.dataKey];
      let chart = chartInstances.get(spec.instanceKey);
      if (!chart) {
        chart = new InteractiveScatterChart(
          document.getElementById(spec.containerId),
        );
        chartInstances.set(spec.instanceKey, chart);
      }
      chart.update(rows, interactiveChartConfig(spec, rows.length));
    },
  );
}

function tableHeader(targetId, columns) {
  const labels = translations[state.language].table;
  document.getElementById(targetId).innerHTML = `<tr>${columns
    .map((column) => `<th scope="col">${labels[column]}</th>`)
    .join("")}</tr>`;
}

function modelLevelCell(row) {
  return `<span class="model-level-wrap">
    <strong>${escapeHtml(row.model)}</strong>
    <span>${escapeHtml(effortLabel(row.effort))}</span>
  </span>`;
}

function renderSubscriptionRanking() {
  const rows = state.rankings.subscription_cost;
  const visibleRows = state.expanded.subscription ? rows : rows.slice(0, 15);
  const referenceCost = Math.max(
    ...rows.map((row) => Number(row.cost_usd_per_task)),
  );
  tableHeader("subscription-head", [
    "rank",
    "modelAndLevel",
    "score",
    "cost",
    "costPercent",
    "access",
    "confidence",
  ]);
  document.getElementById("subscription-body").innerHTML = visibleRows
    .map(
      (row) => `<tr>
        <td class="rank-cell">${row.rank}</td>
        <td class="model-level-cell">${modelLevelCell(row)}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${formatCostPercent(row.cost_usd_per_task, referenceCost)}</td>
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
  const referenceCost = Math.max(
    ...rows.map((row) => Number(row.cost_usd_per_task)),
  );
  tableHeader("api-head", [
    "rank",
    "modelAndLevel",
    "score",
    "cost",
    "costPercent",
    "provider",
    "totalTokens",
  ]);
  document.getElementById("api-body").innerHTML = visibleRows
    .map(
      (row) => `<tr>
        <td class="rank-cell">${row.rank}</td>
        <td class="model-level-cell">${modelLevelCell(row)}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${formatCostPercent(row.cost_usd_per_task, referenceCost)}</td>
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

function renderThresholdTable(rows, headId, bodyId, referenceCost) {
  tableHeader(headId, [
    "threshold",
    "modelAndLevel",
    "score",
    "cost",
    "costPercent",
    "access",
  ]);
  document.getElementById(bodyId).innerHTML = rows
    .map(
      (row) => `<tr>
        <td>≥ ${row.score_threshold}</td>
        <td class="model-level-cell">${modelLevelCell(row)}</td>
        <td>${formatScore(row.score)}</td>
        <td>${formatUsd(row.cost_usd_per_task)}</td>
        <td>${formatCostPercent(row.cost_usd_per_task, referenceCost)}</td>
        <td>${escapeHtml(row.plan_name || row.provider)}</td>
      </tr>`,
    )
    .join("");
}

function calculateValueRanking(metric) {
  const sourceRows =
    metric === "subscription"
      ? state.rankings.subscription_cost
      : state.rankings.api_cost;
  const range = state.valueRanges[metric];
  if (
    !Number.isFinite(range.minimum) ||
    !Number.isFinite(range.maximum) ||
    range.minimum > range.maximum
  ) {
    return { valid: false, rows: [] };
  }
  const rows = sourceRows
    .filter((row) => {
      const score = Number(row.score);
      return score >= range.minimum && score <= range.maximum;
    })
    .map((row) => ({
      ...row,
      raw_value:
        Number(row.cost_usd_per_task) > 0
          ? Number(row.score) / Number(row.cost_usd_per_task)
          : 0,
    }))
    .sort(
      (left, right) =>
        right.raw_value - left.raw_value ||
        Number(left.cost_usd_per_task) - Number(right.cost_usd_per_task) ||
        Number(right.score) - Number(left.score) ||
        left.model.localeCompare(right.model),
    );
  const bestValue = rows.length ? rows[0].raw_value : 0;
  return {
    valid: true,
    rows: rows.map((row, index) => ({
      ...row,
      rank: index + 1,
      value_index: bestValue > 0 ? (row.raw_value / bestValue) * 100 : 0,
    })),
  };
}

function renderValueRanking(metric) {
  const isSubscription = metric === "subscription";
  const idPrefix = isSubscription ? "subscription-value" : "api-value";
  const expandedKey = isSubscription ? "subscriptionValue" : "apiValue";
  const result = calculateValueRanking(metric);
  const text = translations[state.language];
  const message = document.getElementById(`${idPrefix}-message`);
  const body = document.getElementById(`${idPrefix}-body`);
  tableHeader(
    `${idPrefix}-head`,
    isSubscription
      ? [
          "rank",
          "modelAndLevel",
          "score",
          "cost",
          "valueIndex",
          "access",
          "confidence",
        ]
      : [
          "rank",
          "modelAndLevel",
          "score",
          "cost",
          "valueIndex",
          "provider",
          "totalTokens",
        ],
  );

  if (!result.valid) {
    message.textContent = text.invalidScoreRange;
    body.innerHTML = `<tr><td colspan="7">${text.invalidScoreRange}</td></tr>`;
  } else if (!result.rows.length) {
    message.textContent = text.noValueResults;
    body.innerHTML = `<tr><td colspan="7">${text.noValueResults}</td></tr>`;
  } else {
    message.textContent = "";
    const visibleRows = state.expanded[expandedKey]
      ? result.rows
      : result.rows.slice(0, 15);
    body.innerHTML = visibleRows
      .map(
        (row) => `<tr>
          <td class="rank-cell">${row.rank}</td>
          <td class="model-level-cell">${modelLevelCell(row)}</td>
          <td>${formatScore(row.score)}</td>
          <td>${formatUsd(row.cost_usd_per_task)}</td>
          <td class="value-index-cell">${Number(row.value_index).toFixed(2)}%</td>
          <td>${escapeHtml(isSubscription ? accessLabel(row) : row.provider)}</td>
          <td>${
            isSubscription
              ? escapeHtml(
                  confidenceLabels[state.language][row.confidence] ||
                    row.confidence,
                )
              : formatTokens(row.total_tokens_million)
          }</td>
        </tr>`,
      )
      .join("");
  }

  const toggle = document.querySelector(
    `[data-table-toggle="${expandedKey}"]`,
  );
  toggle.hidden = !result.valid || result.rows.length <= 15;
  toggle.textContent = state.expanded[expandedKey]
    ? text.showTop
    : text.showAll(result.rows.length);
}

function renderRankings() {
  if (!state.rankings) {
    return;
  }
  renderSubscriptionRanking();
  renderValueRanking("subscription");
  renderTokenRanking();
  renderApiRanking();
  renderValueRanking("api");
  renderThresholdTable(
    state.rankings.thresholds.subscription_first,
    "subscription-threshold-head",
    "subscription-threshold-body",
    Math.max(
      ...state.rankings.subscription_cost.map((row) =>
        Number(row.cost_usd_per_task),
      ),
    ),
  );
  renderThresholdTable(
    state.rankings.thresholds.api,
    "api-threshold-head",
    "api-threshold-body",
    Math.max(
      ...state.rankings.api_cost.map((row) => Number(row.cost_usd_per_task)),
    ),
  );
}

function renderScenarioUi() {
  const text = translations[state.language];
  const isCoding = state.scenario === "coding";
  document.documentElement.dataset.scenario = state.scenario;
  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.setAttribute(
      "aria-selected",
      String(button.dataset.scenario === state.scenario),
    );
  });
  document.querySelectorAll("[data-scenario-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.scenarioPanel !== state.scenario;
  });
  document.querySelectorAll("[data-scenario-nav='general']").forEach((link) => {
    link.hidden = isCoding;
  });

  document.querySelector('[data-i18n="heroTitle"]').textContent = isCoding
    ? text.codingHeroTitle
    : text.heroTitle;
  document.querySelector('[data-i18n="heroCopy"]').textContent = isCoding
    ? text.codingHeroCopy
    : text.heroCopy;
  const chartLink = document.getElementById("nav-charts-link");
  chartLink.href = isCoding ? "#coding-charts" : "#charts";
  const primaryLink = document.getElementById("primary-content-link");
  primaryLink.href = isCoding ? "#coding-charts" : "#rankings";
  primaryLink.textContent = isCoding ? text.viewCharts : text.viewRankings;

  renderSnapshotMetadata();
  renderMetricCounts();
  renderMethodCards();
}

function setScenario(scenario, remember = true) {
  if (scenario !== "general" && scenario !== "coding") {
    return;
  }
  state.scenario = scenario;
  if (remember) {
    try {
      window.localStorage.setItem("llm-efficiency-scenario", scenario);
    } catch {
      // The visible control remains functional without local storage.
    }
  }
  syncUrlState();
  renderScenarioUi();
  renderChartDetails();
  renderInteractiveCharts();
  if (remember) {
    document.getElementById("status").textContent =
      translations[state.language].statusScenario(scenario);
  }
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
  syncUrlState();
  translateStaticText();
  renderRecommendations();
  renderChartDetails();
  renderInteractiveCharts();
  renderRankings();
  renderScenarioUi();
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

function validateRankingsPayload(payload, snapshotId) {
  if (
    payload.snapshot !== snapshotId ||
    !payload.charts ||
    payload.charts.token.length !== 73 ||
    payload.charts.api.length !== 68 ||
    payload.charts.subscription.length !== 46 ||
    !Number.isInteger(payload.counts.frontier_position_models) ||
    payload.counts.frontier_position_models <= 0 ||
    !Object.hasOwn(payload.charts.token[0], "frontier_position") ||
    !Object.hasOwn(payload.charts.api[0], "frontier_position") ||
    !Object.hasOwn(
      payload.charts.subscription[0],
      "frontier_position",
    )
  ) {
    throw new Error("Interactive chart data is incomplete");
  }
}

function validateCodingPayload(payload, snapshotId) {
  const partialRows = payload?.charts?.token?.filter(
    (row) => row.data_scope === "partial",
  );
  if (
    payload.snapshot !== snapshotId ||
    payload.benchmark !== "Coding Agent Index v1.3" ||
    !payload.charts ||
    payload.charts.token.length !== 52 ||
    payload.charts.api.length !== 52 ||
    payload.charts.subscription.length !== 49 ||
    payload.counts.complete_configurations !== 51 ||
    payload.counts.partial_configurations !== 1 ||
    partialRows.length !== 1 ||
    partialRows[0].agent !== "Claude Code" ||
    partialRows[0].base_model !== "Opus 4.6" ||
    !payload.charts.token.every(
      (row) => row.agent && row.developer && row.host_model_slug,
    )
  ) {
    throw new Error("Coding-agent chart data is incomplete");
  }
}

async function loadSnapshot(snapshotId, remember = true) {
  const snapshot = state.snapshotManifest?.snapshots.find(
    (candidate) => candidate.id === snapshotId,
  );
  if (!snapshot) {
    throw new Error(`Unknown snapshot: ${snapshotId}`);
  }
  const loadSequence = ++state.snapshotLoadSequence;
  const select = document.getElementById("snapshot-select");
  if (state.scenario === "general") {
    select.disabled = true;
  }
  try {
    const response = await fetch(
      `${snapshot.payload_url}?v=${ASSET_REVISION}`,
    );
    if (!response.ok) {
      throw new Error(`Snapshot data request failed: ${response.status}`);
    }
    const payload = await response.json();
    validateRankingsPayload(payload, snapshot.id);
    if (loadSequence !== state.snapshotLoadSequence) {
      return;
    }
    state.snapshot = snapshot;
    state.rankings = payload;
    if (remember) {
      try {
        window.localStorage.setItem("llm-efficiency-snapshot", snapshot.id);
      } catch {
        // The selector remains functional for the current page without storage.
      }
    }
    syncUrlState();
    renderSnapshotMetadata();
    renderChartDetails();
    renderInteractiveCharts();
    renderRankings();
    renderMetricCounts();
    if (remember) {
      document.getElementById("status").textContent =
        translations[state.language].statusSnapshot(snapshotOptionLabel(snapshot));
    }
  } finally {
    if (
      loadSequence === state.snapshotLoadSequence &&
      state.scenario === "general"
    ) {
      select.disabled = false;
    }
  }
}

async function loadSnapshotManifest() {
  const response = await fetch(
    `data/snapshots.json?v=${ASSET_REVISION}`,
  );
  if (!response.ok) {
    throw new Error(`Snapshot manifest request failed: ${response.status}`);
  }
  const manifest = await response.json();
  if (
    !Array.isArray(manifest.snapshots) ||
    manifest.snapshots.length < 2 ||
    !manifest.snapshots.some((snapshot) => snapshot.id === manifest.current)
  ) {
    throw new Error("Snapshot manifest is incomplete");
  }
  state.snapshotManifest = manifest;
  const requestedSnapshot = savedSnapshotId(manifest.current);
  const initialSnapshot = manifest.snapshots.some(
    (snapshot) => snapshot.id === requestedSnapshot,
  )
    ? requestedSnapshot
    : manifest.current;
  await loadSnapshot(initialSnapshot, false);
}

async function loadCodingSnapshot(snapshotId, remember = true) {
  const snapshot = state.codingSnapshotManifest?.snapshots.find(
    (candidate) => candidate.id === snapshotId,
  );
  if (!snapshot) {
    throw new Error(`Unknown coding-agent snapshot: ${snapshotId}`);
  }
  const loadSequence = ++state.codingSnapshotLoadSequence;
  const select = document.getElementById("snapshot-select");
  if (state.scenario === "coding") {
    select.disabled = true;
  }
  try {
    const response = await fetch(
      `${snapshot.payload_url}?v=${ASSET_REVISION}`,
    );
    if (!response.ok) {
      throw new Error(
        `Coding-agent snapshot request failed: ${response.status}`,
      );
    }
    const payload = await response.json();
    validateCodingPayload(payload, snapshot.id);
    if (loadSequence !== state.codingSnapshotLoadSequence) {
      return;
    }
    state.codingSnapshot = snapshot;
    state.coding = payload;
    if (remember) {
      try {
        window.localStorage.setItem(
          "llm-efficiency-coding-snapshot",
          snapshot.id,
        );
      } catch {
        // The selector remains functional for the current page without storage.
      }
    }
    syncUrlState();
    renderSnapshotMetadata();
    renderChartDetails();
    renderInteractiveCharts();
    renderMetricCounts();
    if (remember) {
      document.getElementById("status").textContent =
        translations[state.language].statusSnapshot(
          snapshotOptionLabel(snapshot),
        );
    }
  } finally {
    if (
      loadSequence === state.codingSnapshotLoadSequence &&
      state.scenario === "coding"
    ) {
      select.disabled = false;
    }
  }
}

async function loadCodingSnapshotManifest() {
  const response = await fetch(
    `data/coding-agents.json?v=${ASSET_REVISION}`,
  );
  if (!response.ok) {
    throw new Error(
      `Coding-agent manifest request failed: ${response.status}`,
    );
  }
  const manifest = await response.json();
  if (
    !Array.isArray(manifest.snapshots) ||
    manifest.snapshots.length < 1 ||
    !manifest.snapshots.some((snapshot) => snapshot.id === manifest.current)
  ) {
    throw new Error("Coding-agent manifest is incomplete");
  }
  state.codingSnapshotManifest = manifest;
  const requestedSnapshot = savedCodingSnapshotId(manifest.current);
  const initialSnapshot = manifest.snapshots.some(
    (snapshot) => snapshot.id === requestedSnapshot,
  )
    ? requestedSnapshot
    : manifest.current;
  await loadCodingSnapshot(initialSnapshot, false);
}

function bindControls() {
  document.querySelectorAll("[data-language]").forEach((button) => {
    button.addEventListener("click", () => {
      setLanguage(button.dataset.language);
    });
  });
  document.querySelectorAll("[data-motion-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      setMotion(button.dataset.motionChoice);
    });
  });
  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.addEventListener("click", () => {
      setScenario(button.dataset.scenario);
    });
  });
  document.getElementById("snapshot-select").addEventListener("change", (event) => {
    const loader =
      state.scenario === "coding" ? loadCodingSnapshot : loadSnapshot;
    loader(event.target.value).catch((error) => {
      document.getElementById("status").textContent = String(error);
      console.error(error);
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
  document.querySelectorAll("[data-value-metric]").forEach((input) => {
    const updateValueRange = () => {
      const metric = input.dataset.valueMetric;
      const bound = input.dataset.valueBound;
      const value = Number(input.value);
      if (
        (metric !== "subscription" && metric !== "api") ||
        (bound !== "minimum" && bound !== "maximum") ||
        !Number.isFinite(value)
      ) {
        return;
      }
      state.valueRanges[metric][bound] = value;
      renderValueRanking(metric);
    };
    input.addEventListener("input", updateValueRange);
    input.addEventListener("change", updateValueRange);
  });
}

async function main() {
  bindControls();
  setMotion(motionPreference(), false);
  setLanguage(browserLanguage(), false);
  setScenario(scenarioPreference(), false);
  selectRankingTab("subscription");
  try {
    await Promise.all([loadSnapshotManifest(), loadCodingSnapshotManifest()]);
  } catch (error) {
    document.getElementById("status").textContent = String(error);
    console.error(error);
  }
}

main();
