# 套餐额度核查 / Subscription allowance review

核查日期 / Reviewed: **2026-09-07 UTC**。条款核查日期不等于额度实测日期。 / A terms review is not a new quota measurement.

## 当前结论 / Current findings

| 套餐 / Plan | 本次核查 / Finding | 当前折算 / Current conversion |
|---|---|---|
| ChatGPT Pro 20x | $200/月；官方未公布每周包含的绝对积分。近期有额度下降反馈，但无同条件跑满周限额数据。 / $200/month; absolute weekly credits remain unpublished. Recent reduction reports lack comparable full-week calibration. | 保留 6 月 70× 历史估值，当前置信度降至低。 / Retain June's historical 70× estimate; current confidence lowered to low. |
| Claude Max 20x | $200/月；+50% Claude Code 周额度活动持续至 9 月 13 日 23:59 PT。 / $200/month; the +50% Claude Code weekly boost continues through September 13, 11:59 PM PT. | 保留 6 月报道的 40× 历史估值，实际测量窗口未披露，不额外叠加或扣除活动倍率；置信度低。 / Retain June's reported 40× estimate. Measurement dates are undisclosed; no extra promotion multiplier or removal is justified. Low confidence. |
| Fable on Max | 最多占同一周额度的 50%，不是额外额度。近期高缓存实测不足以建立通用 API 等价值。 / Up to 50% of the shared weekly pool, not extra allowance. Cache-heavy tests do not establish a universal API-value conversion. | 保留 40× × 50% = 20× 建模情景，置信度低。 / Retain the modeled 40× × 50% = 20× scenario; low confidence. |
| GLM Max | 140,000 积分/周、28,000/5小时；GLM-5.3 输入/缓存/输出每万 Token 的积分仍为 6.9/1.7/24。 / Allowances and GLM-5.3 weights unchanged. | 年付 $1,411.20，月均 $117.60，标准时段；非高峰半价另列。 / $1,411.20 annual payment, $117.60/month equivalent, standard hours; off-peak half-rate shown separately. |

Claude 官方宣布 9 月 14 日起，Claude Code 标准周额度改为永久增加 25%。相比当前活动的 1.5 倍，这是 1.25 / 1.5 = **83.33%** 的额度；若其余计量不变，每任务折算成本会增加 **20%**。这是未来条款的条件计算，未套入 9 月 7 日图表。

Claude announced a permanent 25% Claude Code standard-weekly increase starting September 14. Relative to the current 1.5× promotion, that is **83.33%** of the allowance, implying **20%** higher task cost if all other metering stays equal. This conditional future calculation is **not applied** to September 7 charts.

Codex 的每 API 美元 25 积分是消耗单价，不能反推套餐每周送多少积分。一次性额度重置也不计入持续周额度。近期 Pro 5x 的额度下降反馈和 Pro 20x 的短时百分比观测，不能拼成一次 Pro 20x 跑满周限额实测。

Codex's 25 credits per API dollar is a consumption rate, not the number of included weekly credits. One-time resets are not recurring quota. Pro 5x reduction reports and short-window Pro 20x percentage observations do not form a full-week Pro 20x measurement.

补充核查：Gemini CLI 的官方额度仍按每日请求数提供，评测缺少对应请求数时不换算成 Token。Cursor 仍区分自有模型池与其他模型 API 池，但当前页面未明确确认历史 $400 配额；旧版快照不改写。

Also checked: Gemini CLI publishes daily request allowances, not Tokens; conversion requires matching request counts. Cursor separates first-party and other-model pools, but its current page does not explicitly confirm the historical $400 pool. Older snapshots remain unchanged.

## 依据 / Evidence

- [OpenAI 套餐与 Codex 积分 / Plans and credits](https://learn.chatgpt.com/docs/pricing) · [API pricing](https://developers.openai.com/api/docs/pricing)
- [Pro 5x 用户跨周记录 / User's multiweek observations](https://community.openai.com/t/codex-rate-limits-discussion-thread/1378553/487) · [Pro 20x 短时反馈 / Short-window report](https://github.com/openai/codex/issues/38367) · [Astra/Sol 混合使用反馈 / Mixed usage report](https://github.com/openai/codex/issues/43222)
- [Claude plans](https://claude.com/pricing) · [当前 +50% 活动 / Current boost](https://support.claude.com/en/articles/15910845-claude-code-may-august-2026-weekly-limits-promotion) · [9 月 14 日调整公告 / September 14 announcement](https://x.com/ClaudeDevs/status/2093742321473065266)
- [Fable 共享额度 / Shared allowance](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) · [9 月高缓存实测 / September cache-heavy test](https://github.com/ww-w-ai/super-token-saver/blob/431b87fd3174cf79a5b4cd791a5e280e481ec8e9/guides/fable-5-1-vs-opus-5-cost-analysis.md)
- [6 月跑满额度报告 / June full-use reporting](https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-costs-spike-as-subscriptions-hit-pricing-wall-firms-turn-towards-chinese-llms-open-source-models-to-extend-budget) · [ccmeter 4 月校准（早于活动） / April calibration, pre-promotion](https://github.com/iteebz/ccmeter/blob/1484b439e0789e2eb7b070d478f6f19f539305ef/README.md)
- [GLM 额度与权重 / Allowances and weights](https://docs.z.ai/devpack/overview) · [套餐价格 / Plan prices](https://z.ai/subscribe) · [当前价格配置 / Current price configuration](https://static.bigmodel.cn/z-ai-website/_next/static/chunks/8519-b0eeed0c70db38cb.js)
- [Gemini CLI quotas](https://geminicli.com/docs/resources/quota-and-pricing/) · [Cursor pricing](https://cursor.com/docs/models-and-pricing) · [Cursor 历史额度 / Historical allowance](https://forum.cursor.com/t/how-much-usage-is-available-on-the-200-subscription/163309/5)
