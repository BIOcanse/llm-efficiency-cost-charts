# 2026-07-31 snapshot / 2026-07-31 数据快照

Pricing refresh for the existing Artificial Analysis Intelligence Index v4.1
benchmark snapshot.

现有 Artificial Analysis Intelligence Index v4.1 评测数据的价格更新版。

## Current snapshot changes / 本次快照变化

- GPT-5.6 Luna standard API pricing is 80% lower: input / cache read /
  cache write / output are now $0.20 / $0.02 / $0.25 / $1.20 per million
  Tokens.
- GPT-5.6 Luna 标准 API 价格下调 80%：每百万 Token 的普通输入、缓存读取、
  缓存写入、输出价格更新为 $0.20 / $0.02 / $0.25 / $1.20。
- GPT-5.6 Terra standard API pricing is 20% lower: input / cache read /
  cache write / output are now $2.00 / $0.20 / $2.50 / $12.00 per million
  Tokens.
- GPT-5.6 Terra 标准 API 价格下调 20%：每百万 Token 的普通输入、缓存读取、
  缓存写入、输出价格更新为 $2.00 / $0.20 / $2.50 / $12.00。
- GPT-5.6 Sol pricing and all benchmark scores and Token observations are unchanged.
- GPT-5.6 Sol 价格以及全部模型的评测分数、Token 消耗数据均未改变。
- API task costs and all affected rankings are recalculated from the complete
  per-task Token composition. OpenAI subscription-first estimates retain the
  existing 70x API-value ratio, so Terra and Luna effective task costs fall by
  the same percentages as their API prices.
- API 单位任务成本按完整任务 Token 构成重新计算。OpenAI 套餐优先成本沿用现有
  70 倍 API 等价值口径，因此 Terra 和 Luna 的折算任务成本也按相同比例下降。

## Method boundary / 口径边界

This is a pricing refresh, not a new benchmark run. The 70x OpenAI plan value
is a medium-confidence third-party estimate based on exhausting usage limits;
it is not a fixed Token quota promised by OpenAI. The current Codex credit rate
card stays proportional to the new standard API prices, so applying the same
measured allowance does not require inventing a new weekly Token limit.

本次只更新价格，不重新运行评测。OpenAI 套餐的 70 倍 API 等价值仍是基于跑满
限额所得的中等置信度第三方估算，不是 OpenAI 承诺的固定 Token 配额。当前 Codex
积分费率与新标准 API 价格保持同比例，因此在沿用同一实测额度时，无需虚构新的
每周 Token 限额。

## Primary pricing sources / 一手价格来源

- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/pricing
- https://learn.chatgpt.com/docs/pricing
