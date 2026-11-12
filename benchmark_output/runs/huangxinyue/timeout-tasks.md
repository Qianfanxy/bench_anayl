# 推理超时题目清单

更新：2026-11-03 09:37（数据来自 6case、10case 原轮次及全部补跑轮次的数据库）

## 口径

- **超时 = 推理超时**，不是评分超时。评分阶段没出现过超时。
- Claude Code 驱动的模型（Opus、Fable、GLM、Kimi、Gemini）由 runner 在 **90 分钟**时中断，平台记为“运行超时被中断”。
- GPT-6 Astra 走直连 API 模式，没有 90 分钟的内部超时，而是在 **95 分钟**（90 分钟 + 5 分钟宽限）被后端硬截止。退出码为空，平台只记了“运行失败，原因未记录”，实际也是超时。
- 被中断时已经画在副本里的设计会保留，照常截图、核验轨迹、评分。只有轨迹因中断而不完整（工具调用有请求、没回执）时才评不了分。
- 有两题差一点超时、但都是自己正常结束的（退出码 0），**不算超时**，没有列入：6case GLM × Fruit Hub（89.6 分钟）、10case Kimi × Workout Class 补跑（89.9 分钟）。
- GPT 的补跑还没跑完（Fitness App、Workout Class、Budget），这份清单跑完后会再更新一次。

## 超时原因（11-02 排查结论）

**主要不是题目、也不是模型，而是 Figma 截图服务从 11-01 凌晨开始间歇性卡死。**

- 10case 的 28 条超时里，**27 条**都有至少一次 `get_screenshot` 调用卡住：Figma 既不返回也不报错。
  - Claude Code 驱动的模型每次卡满 **30 分钟**才中止，卡 2～3 次 90 分钟就用完了。
  - GPT 走直连模式，没有 30 分钟中止，一次卡死就一直等到 95 分钟被截止。
- 按时间看（北京时间）：11-01 03:00–05:00 截图卡死 0 次（0/144）。05:00 以后开始出现，07:00–14:00 有 20%～40% 的截图调用卡死，到深夜仍偶有发生。6case（10-31 凌晨）一次都没有。返回 base64 和返回下载链接两种方式都会卡，和参数无关。
- **为什么看起来像题目的问题**：同一模型的题目按固定顺序跑（Investment Wallet → … → Budget）。排在后面的 Vulcan Invest、Fitness App、Workout Class、Budget 正好落在卡死高发时段，所以几乎所有模型都在这几题超时。例如 Opus：07:00 以前开始的 6 题都没超时，之后开始的 4 题全部超时。
- **为什么看起来像模型的问题**：截图调用越多、单题越慢的模型，碰上卡死的机会越多（Fable、Kimi）。Gemini 很少截图、十几分钟就交付，所以一次也没超时。
- **唯一一条与卡死无关的超时**：10case Kimi × Investment Wallet（原轮次）。它在 90 分钟里调了 129 次 Figma 工具，其中 38 次报错，属于模型自己反复试错。6case 的 Kimi × Nectar 也是同类情况（184 次调用）。
- **对结果的影响**：这 27 题都是“被基础设施卡掉了大部分时间之后、只拿到半成品”去评的分，分数偏低，而且对截图多的模型更不利。
- **已执行的应对（11-02，受 gaoyongyong 委托）**：在 Figma MCP 代理 `server/figma_mcp_stdio_proxy.py` 里给每次远端调用加了 **120 秒**总时限，可以用环境变量 `FIGMA_MCP_CALL_TIMEOUT` 调整。Claude Code 和 GPT 直连两条链路都走这个代理，所以一次改动两边都生效。超时后模型会立刻收到“Figma 远端 xxx 在 120 秒内没有响应，本次调用已中止”的报错，可以重试；用量日志里记为 transport_error/TimeoutError。实测 1 万多次正常调用最长只要 15 秒。
  - 从 11-02 02:51（北京时间）之后启动的任务开始生效，已经在跑的任务不受影响。原文件备份在 `/mnt/afs/huangxinyue/bench-private/figma_mcp_stdio_proxy.py.bak-20261102`。
- **待定**：是否用新副本重跑这 27 题，需要你提供副本；也可以只重跑会影响排名的部分。

## 10case：最终结果里的超时情况

| 模型 | 最终计分题数 | 其中超时 | 超时率 | 超时题均分 | 未超时题均分 |
|---|---|---|---|---|---|
| Fable 5.1 | 10 | 7 | 70% | 42.1 | 47.0 |
| GLM-5.3 Flash | 10 | 3 | 30% | 44.3 | 44.4 |
| Gemini 3.5 Flash | 10 | 0 | 0% | — | 33.1 |
| Kimi K3 | 10 | 6 | 60% | 39.7 | 43.2 |
| Opus 5.5（三方A） | 10 | 4 | 40% | 47.0 | 50.5 |
| gpt-6-astra | 10 | 5 | 50% | 45.6 | 46.6 |

## 6case：最终结果里的超时情况

| 模型 | 最终计分题数 | 其中超时 | 超时率 | 超时题均分 | 未超时题均分 |
|---|---|---|---|---|---|
| Fable 5.1 | 6 | 0 | 0% | — | 38.7 |
| GLM-5.3 Flash | 6 | 0 | 0% | — | 39.5 |
| Gemini 3.5 Flash | 5 | 0 | 0% | — | 40.8 |
| Kimi K3 | 6 | 0 | 0% | — | 38.5 |
| Opus 5.5（三方A） | 6 | 0 | 0% | — | 46.3 |
| gpt-6-astra | 6 | 0 | 0% | — | 42.2 |

> 超时题和未超时题是同一模型在不同题目上的表现，题目难度不同，两列均分不能直接当作“超时让分数下降了多少”。

## 10case：全部超时记录（29 条）

| 模型 | 题目 | 轮次 | 账号 | 推理时长 | 评分 | 是否计入最终结果 | 副本 |
|---|---|---|---|---|---|---|---|
| Fable 5.1 | Budget | 原轮次 | gaoyongyong | 90 分钟 | ✅ 44/53 | ✅ 计入 | [打开](https://www.figma.com/design/BeEg0lu9bBMJUWrNYuGHhS/) |
| Fable 5.1 | Expenio | 原轮次 | gaoyongyong | 90 分钟 | ✅ 44/53 | ✅ 计入 | [打开](https://www.figma.com/design/55GBNgR7C0fHb1EFjQB2Mh/) |
| Fable 5.1 | Fitness App | 原轮次 | gaoyongyong | 90 分钟 | ✅ 42/53 | ✅ 计入 | [打开](https://www.figma.com/design/AHMOGmt7pIOAFuZoLLnsg6/) |
| Fable 5.1 | Meet | 原轮次 | gaoyongyong | 90 分钟 | ✅ 40/53 | ✅ 计入 | [打开](https://www.figma.com/design/GlyrmsSXK4bZZZFPfgI4vD/) |
| Fable 5.1 | Payment Wallet | 原轮次 | gaoyongyong | 90 分钟 | ✅ 42/53 | ✅ 计入 | [打开](https://www.figma.com/design/U61Mq9ELZKbBVU7vOnWHMR/) |
| Fable 5.1 | Vulcan Invest | 原轮次 | gaoyongyong | 90 分钟 | ✅ 40/53 | ✅ 计入 | [打开](https://www.figma.com/design/8DGNh1LaHvvcacbstDxyc1/) |
| Fable 5.1 | Workout Class | 原轮次 | gaoyongyong | 90 分钟 | ✅ 43/53 | ✅ 计入 | [打开](https://www.figma.com/design/wdd0MJg6SDKnDDreRit1lP/) |
| GLM-5.3 Flash | Budget | 原轮次 | zhengyaozhi | 90 分钟 | ✅ 48/53 | ✅ 计入 | [打开](https://www.figma.com/design/S6kRnFOWrOB6X83gheQfh9/) |
| GLM-5.3 Flash | Fitness App | 原轮次 | zhengyaozhi | 90 分钟 | ✅ 41/53 | ✅ 计入 | [打开](https://www.figma.com/design/zWGWwXFFBe8G1TPXyCPovy/) |
| GLM-5.3 Flash | Workout Class | 原轮次 | zhengyaozhi | 90 分钟 | ✅ 44/53 | ✅ 计入 | [打开](https://www.figma.com/design/nazWWKPcEvzziDpXjc9ZUS/) |
| Kimi K3 | Budget | 原轮次 | huangxinyue | 90 分钟 | ❌ 未出分（轨迹被中断，未进入评分） | ↪ 已被补跑替换 | [打开](https://www.figma.com/design/IpBiFsuDuvkezxNgzdrMIn/) |
| Kimi K3 | Budget | 补跑 | huangxinyue | 90 分钟 | ✅ 46/53 | ✅ 计入 | [打开](https://www.figma.com/design/DNMnvlQxITvZJcaL8dstS1/) |
| Kimi K3 | Fitness App | 原轮次 | huangxinyue | 90 分钟 | ✅ 44/53 | ✅ 计入 | [打开](https://www.figma.com/design/BTO5IlnrbyGTV8hYgvPITw/) |
| Kimi K3 | Investment Wallet | 原轮次 | huangxinyue | 90 分钟 | ❌ 未出分（轨迹被中断，核验不通过） | ↪ 已被补跑替换 | [打开](https://www.figma.com/design/A5e6T0szS3PukIseQmMYfM/) |
| Kimi K3 | Investment Wallet | 补跑 | huangxinyue | 90 分钟 | ✅ 47/53 | ✅ 计入 | [打开](https://www.figma.com/design/nknPb38IOxy7Gue45nwW58/) |
| Kimi K3 | Meet | 原轮次 | huangxinyue | 90 分钟 | ✅ 36/53 | ✅ 计入 | [打开](https://www.figma.com/design/sVulJavnfPkoLkLl0p1Htc/) |
| Kimi K3 | Payment Wallet | 原轮次 | huangxinyue | 90 分钟 | ✅ 37/53 | ✅ 计入 | [打开](https://www.figma.com/design/tgCD2aPl6jVEDmz4KF2HHV/) |
| Kimi K3 | Vulcan Invest | 原轮次 | huangxinyue | 90 分钟 | ❌ 未出分（轨迹被中断，核验不通过） | ↪ 已被补跑替换 | [打开](https://www.figma.com/design/91GWrbnRWgBtJGadCT5ZIQ/) |
| Kimi K3 | Vulcan Invest | 补跑 | huangxinyue | 90 分钟 | ✅ 28/53 | ✅ 计入 | [打开](https://www.figma.com/design/LnfHexrlbV0kty6qMhv64z/) |
| Kimi K3 | Workout Class | 原轮次 | huangxinyue | 90 分钟 | ❌ 未出分（轨迹被中断，未进入评分） | ↪ 已被补跑替换 | [打开](https://www.figma.com/design/yjtv9ap8VrOcMJmrUYoX46/) |
| Opus 5.5（三方A） | Budget | 原轮次 | zuohaosheng | 90 分钟 | ✅ 48/53 | ✅ 计入 | [打开](https://www.figma.com/design/dbGtQQ7ZTm07kMt6rkMlVV/) |
| Opus 5.5（三方A） | Fitness App | 原轮次 | zuohaosheng | 90 分钟 | ✅ 48/53 | ✅ 计入 | [打开](https://www.figma.com/design/OaUnBLdkamUtyM90hh9vQ4/) |
| Opus 5.5（三方A） | Vulcan Invest | 原轮次 | zuohaosheng | 90 分钟 | ✅ 46/53 | ✅ 计入 | [打开](https://www.figma.com/design/nleW3IQT5kcuqxaf8wBwJ3/) |
| Opus 5.5（三方A） | Workout Class | 原轮次 | zuohaosheng | 90 分钟 | ✅ 46/53 | ✅ 计入 | [打开](https://www.figma.com/design/GyNHTzuJiehy9yvkayiE9N/) |
| gpt-6-astra | Fitness App | 补跑 | panzhengyuan | 95 分钟 | ✅ 45/53 | ✅ 计入 | [打开](https://www.figma.com/design/vxyePeGWL8IkS6aW04h1y1/) |
| gpt-6-astra | Investment Wallet | 补跑 | panzhengyuan | 95 分钟 | ✅ 45/53 | ✅ 计入 | [打开](https://www.figma.com/design/j7wCotjxFi95siNrGN4ANg/) |
| gpt-6-astra | Meet | 补跑 | panzhengyuan | 95 分钟 | ✅ 47/53 | ✅ 计入 | [打开](https://www.figma.com/design/Fgr6Vm4KsKkdf8kfkPzmmL/) |
| gpt-6-astra | Travelin | 补跑 | panzhengyuan | 95 分钟 | ✅ 49/53 | ✅ 计入 | [打开](https://www.figma.com/design/K8xBlbpYF8BIA5vE6jl93o/) |
| gpt-6-astra | Vulcan Invest | 补跑 | panzhengyuan | 95 分钟 | ✅ 42/53 | ✅ 计入 | [打开](https://www.figma.com/design/nu2Ny7b01aEHRzahb7VMtK/) |

## 6case：全部超时记录（1 条）

| 模型 | 题目 | 轮次 | 账号 | 推理时长 | 评分 | 是否计入最终结果 | 副本 |
|---|---|---|---|---|---|---|---|
| Kimi K3 | Nectar | 原轮次 | zuohaosheng | 90 分钟 | ❌ 未出分（轨迹被中断，核验不通过） | ↪ 已被补跑替换 | [打开](https://www.figma.com/design/HmTYf0TxPAghlGoRNAJEsf/) |

## 处理方式（现行）

1. **超时但已出分**：保留分数，计入最终结果，不重跑（11-01 确认）。
2. **超时且轨迹不完整、未出分**：需要新副本重跑。由你提供副本，平台不自动重试。
3. 10case Kimi 的 4 题（以及 6case Kimi × Nectar）就是第 2 种情况。10case 这 4 题用新副本重跑后，3 题又超时、1 题在 89.9 分钟时自己结束，但这次轨迹都完整，全部出了分。

## 待你决定

- 超时题现在和正常完成的题算在同一个均分里。可选做法：报告里单独列出超时率（即本文档的汇总表）；或者把推理时限放宽（比如 120 分钟），代价是整轮更慢、Figma 额度消耗更多。
