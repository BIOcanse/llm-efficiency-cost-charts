# Terminal-Bench · 2026-09-05 UTC

[中文网页](https://biocanse.github.io/llm-efficiency-cost-charts/?lang=zh-CN&view=terminal) · [English site](https://biocanse.github.io/llm-efficiency-cost-charts/?lang=en&view=terminal)

网站默认改为 Terminal-Bench，取消主观推荐。分别列出套餐折算成本、API 成本、Token 消耗与任务成功率；排名可按厂商、Agent、成功率区间重算，并显示每次尝试和每个成功任务的实际消耗。

TB 4.0 为持续更新版本，本次有 18 个配置，套餐图纳入 16 个。3.0、2.1、2.0、1.0 为本项目的最终快照。2.0 和 1.0 缺少可核实的消耗汇总，仅输出成功率排名，不补估算。不同版本不混排。

完整包包含中英文共 60 张 4800×2700 PNG、60 份 SVG、CSV 排名、官方原始记录、日期化套餐证据、计算与网页源代码，以及原有 AA 存档。所有新图的标签／表格碰撞与越界检查均为 0；通过 7 项数据与产物测试、55 项桌面浏览器检查。

套餐折算是充分使用额度的估计，保留证据日期与置信度，不是厂商承诺的固定 Token 额度，也不是本月跑满重测。失败尝试计入成本；每个成功任务的平均消耗不表示反复重试必然成功。Token 对比保留模型规模、Agent、档位与预算的比较边界。

---

Terminal-Bench is now the default view, without subjective model picks. Subscription-equivalent cost, API cost, and Token consumption are compared separately with task success. Rankings show actual resources per attempt and per success, with provider, agent, and success-rate filters.

TB 4.0 remains active: 18 configurations, including 16 with usable subscription-first costs. Versions 3.0, 2.1, 2.0, and 1.0 are frozen project snapshots. TB 2.0 and 1.0 have no verifiable aggregate consumption, so their final exports contain success-rate rankings only. Benchmark versions are not pooled.

The full bundle includes 60 bilingual 4800×2700 PNGs, 60 SVGs, CSV rankings, original owner data, dated quota evidence, calculation and website source, and existing AA archives. All new chart/table collision and bounds checks are zero. Seven data/artifact tests and 55 desktop browser checks passed.

Subscription costs assume full utilization of dated allowance estimates, not promised Token quotas or fresh exhaustion tests. Failed attempts count toward cost. Resources per success describe the evaluated workload, not guaranteed success after retries. Token comparisons retain the model-scale, agent, effort, and budget limitations.

方法与来源 / Method and sources:

- [中文说明](https://github.com/BIOcanse/llm-efficiency-cost-charts/blob/main/docs/TERMINAL_BENCH_GUIDE.zh-CN.md)
- [English guide](https://github.com/BIOcanse/llm-efficiency-cost-charts/blob/main/docs/TERMINAL_BENCH_GUIDE.en.md)
- [Terminal-Bench](https://www.tbench.ai/)
- [原始数据与校验值 / Original data and hashes](https://github.com/BIOcanse/llm-efficiency-cost-charts/tree/main/data/terminal-bench)

Download the `-full.zip` asset and verify it against `SHA256SUMS.txt`. GitHub's automatically generated source archives are not the named full bundle.
