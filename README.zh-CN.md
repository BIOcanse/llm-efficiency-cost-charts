# 大模型 Token 效率与任务成本图

[English README](README.md)

持续更新主流大模型的 Intelligence Index 跑分、完整 Token 消耗、API 单位任务成本和套餐优先单位任务成本。

最新快照：**2026-07-24**  
评测：**Artificial Analysis Intelligence Index v4.1**  
当前覆盖：**73 个 Token 消耗配置 / 68 个 API 成本配置 / 46 个套餐优先配置**

每个点代表一个模型和思考档位，同色线连接同一模型的不同档位。纵轴越高、横轴越靠左越好。

## 1. 完整 Token 消耗与跑分

完整 Token 消耗包括完成同一套评测所需的输入、推理和最终回答 Token。

[PNG](charts/zh-CN/01_total_token_consumption_vs_score.png) · [SVG](charts/zh-CN/01_total_token_consumption_vs_score.svg)

![完整 Token 消耗与 Intelligence Index 跑分](charts/zh-CN/01_total_token_consumption_vs_score.png)

## 2. API 单位任务成本与跑分

按每项任务的 Token 构成和每个原始模型统一选定的供应商价格计算。量化版本只有在评测数据足够完整时才作为单独模型纳入。

[PNG](charts/zh-CN/02_api_task_cost_vs_score.png) · [SVG](charts/zh-CN/02_api_task_cost_vs_score.svg)

![API 单位任务成本与 Intelligence Index 跑分](charts/zh-CN/02_api_task_cost_vs_score.png)

## 3. 套餐优先单位任务成本与跑分

有套餐且存在可核算额度时使用性价比最高的适用套餐；有套餐但缺少可用额度数据时排除；只有不存在相关套餐时才使用 API。

[PNG](charts/zh-CN/03_subscription_first_task_cost_vs_score.png) · [SVG](charts/zh-CN/03_subscription_first_task_cost_vs_score.svg)

![套餐优先单位任务成本与 Intelligence Index 跑分](charts/zh-CN/03_subscription_first_task_cost_vs_score.png)

## 注意事项

- 结果只代表同一套 Intelligence Index v4.1 评测。该评测以较难的编码和科学任务为主，不代表所有实际使用场景。
- 每个点衡量的是**模型与思考档位的组合**，不能脱离推理预算直接视为模型本体的绝对效率。
- Intelligence Index 分数可以用于同口径连续比较，但不是严格的绝对智能值。
- OpenAI 和 Claude 的套餐 API 等价值来自第三方跑满限额的估算，不是厂商承诺的固定 Token 配额。
- 模型跑分、价格、套餐与额度行为都可能变化。每次更新均以 [`data/`](data/) 中的日期快照为准。

具体计算方法见[方法说明](docs/METHODOLOGY.md)，完整链接见[数据来源](docs/SOURCES.md)，当前数据见 [2026-07-24 快照](data/2026-07-24/)。

## 更新规则

每次更新必须同时更新数据快照、中英文两套图、快照日期和 [`PROGRESS.md`](PROGRESS.md)。旧版日期快照继续保留，方便比较变化。
