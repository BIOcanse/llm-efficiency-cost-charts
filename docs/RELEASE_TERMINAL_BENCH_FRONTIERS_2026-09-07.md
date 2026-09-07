# Terminal-Bench：左上前沿与配置列表 / Pareto frontiers and configuration lists

[中文网页](https://biocanse.github.io/llm-efficiency-cost-charts/?lang=zh-CN&view=terminal&tb=4.0) · [English site](https://biocanse.github.io/llm-efficiency-cost-charts/?lang=en&view=terminal&tb=4.0)

数据仍为 **2026-09-05 UTC** 快照。本次增加分析图和名单，不改模型数据、套餐依据或原始成图。

套餐、API、Token 各自画左上前沿（斩杀线）：不存在另一个配置能同时做到消耗不高、成功率不低，并至少一项更好。同坐标配置全部保留；按图中点值计算，不代表统计显著领先。各版独立比较，虚线台阶不代表模型插值。

| 测试集版本 | 套餐前沿配置 | API 前沿配置 | Token 前沿配置 |
| --- | ---: | ---: | ---: |
| Terminal-Bench 4.0 | 5 | 5 | 4 |
| Terminal-Bench 3.0 | 4 | 4 | 5 |
| Terminal-Bench 2.1 | 5 | 5 | 5 |
| Terminal-Bench 2.0 | 缺消耗数据 | 缺消耗数据 | 缺消耗数据 |
| Terminal-Bench 1.0 | 缺消耗数据 | 缺消耗数据 | 缺消耗数据 |

网页每张图下方列出完整的模型＋Agent＋档位、成功率及区间、每次尝试和每个成功任务的消耗。厂商与 Agent 筛选后同步重算；缩放不改变名单。套餐表保留使用方式与折算置信度。

新增中英文 28 张 4800×2700 PNG、28 份 SVG，以及各版三项前沿 CSV 和汇总 CSV。原有图表与数据一并保留；2.0、1.0 的附加说明图明确标注前沿数据缺失，成功率最终图不受影响。

完整包中的 `charts/terminal-bench/<version>/2026-09-05/<language>/` 包含 `07_subscription_frontier`、`08_api_frontier`、`09_token_frontier` 和 `10_frontier_list_01`；CSV 位于对应的 `rankings/terminal-bench/` 版本目录。

## English

The data snapshot remains **September 5, 2026 UTC**. This edition adds analysis figures and lists without changing model measurements, subscription evidence or original charts.

Subscription, API and Token charts have separate upper-left Pareto frontiers. A configuration is retained when no other configuration uses no more resources and achieves no less success, with at least one strict improvement. Equal-coordinate ties remain. Selection uses point estimates, not a test of statistical significance. Benchmark versions stay separate; dashed steps do not interpolate between models.

Frontier counts (subscription / API / Token): **TB4: 5 / 5 / 4; TB3: 4 / 4 / 5; TB2.1: 5 / 5 / 5**. TB2 and TB1 lack verifiable consumption data, so no frontier is calculated; their final success-rate charts remain available.

Each chart has a visible list with model, agent, effort, success and uncertainty, resources per attempt and per successful task. Provider and agent filters recalculate the frontier; zoom does not change membership. Subscription lists retain access method and conversion confidence.

The complete bundle adds **28 bilingual 4800×2700 PNGs, 28 SVGs, and per-version frontier CSVs**, while retaining the existing charts and data. Files numbered `07`–`09` are frontier charts; `10_frontier_list_01` is the combined list. See the bilingual Terminal-Bench guides for definitions and sources. ZIP integrity is covered by `SHA256SUMS.txt`.
