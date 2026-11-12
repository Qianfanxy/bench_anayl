# v2 结果预检（设计师评审前）

检查日期：2026-11-04　范围：交付包 177 份结果（manifest.json）
脚本：`tools/qa_check.py`（全量明细见 `qa/qa-issues.json`）；可疑格已逐张人工看图核对。

## 一、需要处理（会影响评审有效性）

| # | 题目 | 模型 | 分数 | 问题 | 核对结论 | 建议 |
|---|---|---|---|---|---|---|
| 1 | 6case Chat Bot AI | GPT-6 Astra | 46 | 需求 12 屏只交付 4 屏（缺 05–12），推理 2.5 分钟、9 轮就停 | 判官只按已交付的 4 屏打分，G0 判通过，分数虚高 | 换新副本重跑，或评审时剔除 |
| 2 | 10case Fitness App | Gemini 3.5 Flash | 33 | 03 页有 3 套同名画板共 15 张，前两套 10 张是空白或半成品残留 | 第 3 套（18:13–18:17）完整；判官把残留也算进去扣分 | 重跑；或评审只展示第 3 套并重新打分 |
| 3 | 6case Fruit Hub | GLM-5.3 Flash | 41 | 两套同名画板共 20 张（第一套 Splash 是纯橙色空屏） | 两套内容接近，第二套更完整 | 评审只保留第二套，或重跑 |
| 4 | 10case Investment Wallet | Gemini 3.5 Flash | 42 | 01_Wallet、02_Discovery 各两版 | 两版几乎一样，是模型迭代后没删旧版 | 评审保留新版（node 8:20、9:23），或重跑 |
| 5 | 3case Balance | Qwen3.8 ckpt-270 | 42 | 需求 11 屏只交付 2 屏 | 同 #1，分数虚高 | Qwen 参评的话需处理 |
| 6 | 3case Paradise Invest | Qwen3.8 ckpt-270 | 35 | 需求 11 屏缺 07–09 三屏 | 同上 | 同上 |

## 二、0 分的 4 格（都是 Gemini，判官判定正确）

| 题目 | 截图核对 |
|---|---|
| 3case Balance | 第 2–11 屏只有标题，正文全空 |
| 10case Budget | 只交付 1 屏（需求 3 屏），而且几乎全空，只有一行测试文字 |
| web10 Foodieland | 5 屏大部分是空白和空色块，只有页脚订阅区有内容 |
| web10 ABM Developer Portfolio | 只有 1 屏，头像、项目卡、经历卡挤压裁切，内容无法辨认 |

都是模型自己没做完或排版崩坏，不是截图或评分环节的问题。需要决定：保留（如实反映失败），还是不放进设计师对战（空白稿必输，浪费评审票）。

## 三、次要问题

- **规范/组件板被当成了交付屏**，有 11 格，例如 GPT Furniro 的「Furniro · UI system」（1280×8000 空白板）、Fable Foodgo 的「Assets」板、Kimi Budget 的「UI Kit」。设计师会看到这些板；GPT Furniro 的 34 分可能因此偏低。
- Gemini × Nectar 缺 09_My_Cart 一屏（38 分）。
- 26 个 run 的状态显示「结果不完整 / 生成失败」，报错内容都是轨迹转换或截图标签质检，交付稿本身已核验，不影响设计结果。
- 自动检查标出的约 40 张「近似纯色」截图，大部分是 Splash 启动页（整屏品牌色），属于正常设计。

## 四、流程上的缺口

判官只看已交付的屏，不知道需求要求多少屏。所以缺屏的稿子只要已交付的部分没崩，G0 就能通过（#1、#5、#6）。
建议在评审前加一道「需求屏数 / 画板名」核对作为门槛，`tools/qa_check.py` 已经实现了这一步。

## 五、轨迹分析补充（2026-11-04）

### Gemini 4 个 0 分
| 题目 | 结论 | 依据 |
|---|---|---|
| 3case Balance | **我们的问题**（Figma 额度） | 第 23 次调用碰到账号 MCP 调用上限，只做完 01_Sign_Up，模型被迫收工；delivery 记录了 infrastructure_blocked=true，平台仍然打了分 |
| 10case Budget | 模型问题 | 构建代码写成 async 函数后只调用 `run()` 没有 await，脚本先结束，改动没落到画布上；又用 throw 打印调试信息，导致改动回滚；4 次重写都踩同一个坑 |
| web10 Foodieland | 模型问题 | 最后一步一次性重建 5 屏，各区块内容丢失；它自己截到的 5 张图也是空白，仍然报告交付完成 |
| web10 ABM | 模型问题 | 连续 4 次 API 用法错误（layoutFlex、往 instance 里 appendChild 等），最后一版布局塌陷，只截了 1 张图，5 分钟就结束 |

### 额度问题被评分（平台缺口）
23 格的 delivery 标记了 `infrastructure_blocked=true`（期间碰到过 Figma 额度上限），但 `ready_for_scoring` 仍是 true，照常出了分。其中交付因此被截断的有 4 格：
- 3case Balance × Gemini（0 分）
- 6case Chat Bot AI × GPT（4/12 屏）
- 3case Balance × Qwen（2/11 屏）
- 3case Paradise Invest × Qwen（8/11 屏）

另外 19 格虽然碰过额度上限，但屏数完整，影响较小：3case Balance × GLM、Paradise Invest × Gemini/GLM/Kimi、Foodgo × Kimi/Qwen；6case StockWave × Opus/GLM/Kimi、Nectar × GLM、Stylish × Opus/GLM/Kimi、Chat Bot AI × GLM、Fruit Hub × Opus；10case Payment Wallet × Kimi、Vulcan Invest × Kimi、Workout Class × GLM、Budget × Kimi。
