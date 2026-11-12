# benchmark-design

本分支适配“在指定 Figma 文件内完成首次设计”的评测任务。原分支和上一轮独立运行目录保持原样；本轮改动通过 `UI_EVAL_BENCHMARK_DESIGN=1` 启用。

## 执行口径

1. 打开分配给当前模型的文件，读取 `00 · Start Here` 的具体任务。
2. 参考 `01 · Foundations` 的视觉规范，复用 `02 · Components` 的组件及 `04 · Media` 的素材。
3. 在同一文件的 `03 · Workspace` 从零完成全部页面、状态和原型。没有这个 page 时创建它；保留四个参考页及其中的原有节点。
4. 对所有必需画面截图检查，修复问题后再检查，完成任务再结束。最终提供原文件链接、Workspace 和画板 ID，并如实说明未完成事项。

这是用户授权的工作副本。文件内部沿用的“源文件只读、另建文件交付”文案不适用于本轮 Workspace 的交付位置；参考页仍予以保留。2026-10-26 起使用用户提供的 fresh 表格及新副本，不复用上一轮文件，也不清空或重置已有产物。

## 提示词调整

| 原来的冲突 | 本分支的调整 |
| --- | --- |
| 旧表格的任务名称与文件不符 | 改用用户已修正的 fresh 表格；query 逐字导入，不替换品牌、不追加说明 |
| 填入原文件链接就套用二轮编辑，禁止从零搭建 | 显式使用初次设计模式，允许在 Workspace 创建页面、组件、画板及原型 |
| 文件任务说明要求另建文件 | 明确在用户指定的同一个工作副本中交付，四个参考页保留 |
| 强制只用 Inter | 按 Foundations 的实际字体和颜色执行 |
| 禁止渐变、阴影及模糊 | 在 API 支持、任务适用时正常使用 |
| 截到一张非空图就立即结束 | 检查全部必需画面，允许修复后多次截图，以任务完成作为收尾条件 |
| GPT 读取旧训练样本中的超长系统上下文 | direct runner 使用独立的完整 system 文件，不读取训练样本或混入旧记忆 |
| CC 会话复制个人 skills/plugins/记忆，暴露大量无关工具 | benchmark 会话不装入这些上下文；仅开放四个 Figma 工具 |

工具口径统一为 `whoami`、`get_metadata`、`use_figma`、`get_screenshot`。不开放新建 Figma 文件的工具。direct runner 的 MCP 工具声明及执行校验都使用这份口径，避免“提示词要求 get_metadata、实际执行器却不允许”的矛盾。

公共任务提示词在 `server/benchmark_design.mjs`。模型原有的推理摘要采集配置继续保留：需要摘要时附加相同的简短可见决策摘要格式；未采集摘要的模型不加该段。CC runner 自带的基础系统指令仍存在，因此不能称各模型的整个请求逐字相同。这里统一的是设计任务指令和 Figma 工具范围。

原轨迹保存、归一化、量表和评分实现保持原有路径。既有文件无需新建文件的审计分支继续沿用，并以本轮 run 保存的目标 URL 检查文件归属；没有放宽截图或其它轨迹质检项。

## Fresh 表格与原始 query

源目录：`/mnt/afs/gaoyongyong/code/new_bench/data_syn/figma_tasks_7_excels_fresh_20261026/`。

文件名为 `figma_tasks_01_fresh.xlsx` 至 `figma_tasks_07_fresh.xlsx`。同名 ZIP 可用于核对，执行时读取目录中的工作簿。

7 个文件的 F2–F4 对应同样的 3 道题，每个模型的文件 URL 不同，共 21 次运行。脚本只读取工作簿，不写回 Excel：

```bash
python scripts/prepare-benchmark-design.py
```

输出到 `storage/benchmark-design/inputs.json`，每行保存原始 query、来源文件/单元格、文件 URL 和 SHA-256。`query` 与 `original_query` 逐字相同，包括空格、换行及标点，两个 SHA-256 也相同。脚本校验 21 个独立文件、与旧文件及源模板不重合，以及同题跨模型除 URL 外完全一致。

表格正文如下，各行使用各自的文件 URL：

```text
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/<本行文件 ID>/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

具体题目由各文件的 00 页指定；不通过替换 query 中的产品名区分题目。7 个模型继续各做 3 题。输入准备脚本只导出清单，不自动提交推理任务。

## 初始文件检查

可先只读检查整轮文件：

```bash
python scripts/check-benchmark-design.py --mcp-config /path/to/figma-mcp.json
```

结果保存到 `storage/benchmark-design/fresh-preflight-20261026.json`。服务端在每次启动模型前还会实时检查：四个参考页必须存在且非空，03 可以缺失或为空；已有设计、重复页面或其它遗留页面会阻止启动。每个副本只能在本轮使用一次。检查不会创建或修改任何 Figma 节点。

## 启动与输入留档

安装 Node 依赖后，独立启动：

```bash
npm ci
npm run benchmark-design
```

当前机器可复用上一轮已经安装的 runner、Python、Claude Code 和 MCP 认证路径：

```bash
npm run benchmark-design -- --runtime-config \
  /mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap/storage/standalone-original-20261025/runtime-config.json
```

入口固定使用本工作目录中的 `storage/benchmark-design` 数据库、runs 和干净 cwd，监听 `127.0.0.1:18174`。即便复用依赖配置，也会覆盖旧配置中的存储路径，避免写回上一轮结果。此入口不会创建评测批次。

每次实际生成前保存：

- `benchmark-system.txt`：本次公共任务系统指令，direct 模式将它作为完整 system 使用；CC 模式将其附加到客户端基础 system。
- `benchmark-input.json`：实际 query、目标文件、模型、摘要模式及工具列表。
- `benchmark-baseline.json`：模型开始前的页面名称、ID 及直接子节点数，证明输入文件的初始状态。
- 原 runner 的 API trace 和轨迹：供核对客户端最终真正发出的完整请求。

后台运行使用以下入口，不访问原来的网页地址：

```bash
python scripts/import-benchmark-design.py
python scripts/launch-benchmark-design.py --runtime-config \
  /mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap/storage/standalone-original-20261025/runtime-config.json
```

导入脚本只向独立数据库写入本轮 7 个模型、21 条 fresh query，沿用上一轮各题的 20 条评分项；源数据库只读。启动器可加 `--services-only` 只启动依赖，便于连接测试。后台监督器先验证整轮输入及页面快照，提交六个 API 模型的批次，再等待本轮 GPU 服务的真实模型与连接检查通过后提交 checkpoint 的三题。每批并发为 1，推理、轨迹收尾、质检和评分仍调用原服务的接口及实现。

GPT 使用独立端口 18185 上的 TokenHub Responses 兼容层，保留文本、图像、工具结果及推理密文的连续传递。CuDNN 修复安装在本轮 `gpu/overlay`，不修改上一轮 Python 环境。checkpoint 仍为 ckpt-270，模型服务与转发使用本轮端口 18013。GPU 作业的 describe JSON 保存在 `gpu/job.json`；本轮 worker 执行 `benchmark-ckpt270-worker.sh`，三题结束后通过 `gpu/release.json` 释放自身进程。

当前状态写入 `storage/benchmark-design/progress.json`，批次 ID 写入 `submission-state.json`。`等待评分`、`结果不完整`、`生成失败` 等真实状态直接保留；生成收尾写入 `generation-complete.json`，`complete.json` 仅在 21 个逻辑用例都取得真实评分后生成，不表示 21 次都通过质量评测。

## 验证

```bash
node --test tests/benchmark_design.test.mjs tests/figma_binding.test.mjs \
  tests/runner_args.test.mjs tests/trajectory_quality.test.mjs

# 使用已安装 mcp/httpx 的 Python：
python tests/benchmark_direct_runner_test.py
python server/direct_sglang_runner.py --self-test
```

direct 测试通过离线 MCP 和模型协议替身验证真实 agent loop：紧凑 system、get_metadata 调用、工具结果回传、最终轨迹保存，以及拒绝 create_new_file。它不消耗模型或 Figma 配额，也不代表真实设计质量已经通过。

## 2026-10-26 链路故障归因与恢复

第一次运行的 21 个逻辑用例中，9 个没有启动模型，3 个因 Figma 限额没有交付产品画板，7 个正常结束且有画板，另 2 个虽异常退出仍留下画板。只读实查确认 9 份非空设计，共 127 个按任务名称编号的产品画板；不能把 11 条终止状态都算作模型能力失败，也不能把原来 10 条“等待评分”都算作成功。

确认并修复的链路缺陷：

- 各批 `concurrency=1` 没有限制跨批并发，实际六个模型共用同一账号并行。benchmark 现在对整台服务限制为一个生成任务，并对 MCP 子进程共用的账号预算加锁，以至少 4 秒间隔调度调用。
- 限额错误曾被直接交还给模型无限重试；GLM、Fable 轨迹分别出现 118、298 条明确的配额错误。现在仅对已明确被拒绝、未执行的配额调用退避重试，三次持续拒绝后熔断并保存已有产物。不会重放提交状态不明的写请求。
- 前置检查错误被丢失，然后写入一条“生成失败”的假 run。现在保留结构化原因和等待时间，检查失败只进入资源等待队列，不创建推理记录。
- 固定补图脚本只解析 XML，但 get_metadata 的真实页面列表是 `- 0:1: Page name` 文本。现在两种格式都支持，限额消息会直接保留原因。benchmark 只采集 03 的产品画板，不把参考板和组件板送去评分；也不会在失败后再启一个模型补图。
- 原质检只查轨迹、URL 和截图，参考页截图也能让空 Workspace 进入“等待评分”。现在核对真实 Workspace 和任务规定的画板名，未交付画板的资源阻塞单独记录。实际图层统计使用与原摘要相同的字段供 Q17–Q20 判断。
- GLM 最后请求已有约 190k 缓存上下文，最终返回网关 400；网关没有给出更具体原因，不能证明是模型服务无可用资源。恢复运行时为该网关别名设置 100k 自动压缩窗口，避免依赖 Sonnet 别名的上下文假设。Fable 的超时前有大量限额循环，不能只归因为任务计算慢。
- 原监督器把“所有批次收尾”写成 complete，且没有发起评分。现在生成阶段单独记录，恢复监督器只有在 21 个逻辑用例均取得真实评分后才写完整评测完成标记。

Figma Enterprise Full/Dev 仍有每分钟和每日读取额度；不同工具的豁免范围不能想当然。官方说明见 [Rate limits & access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)。本账号的 OAuth 只有 `mcp:connect`，REST 实测返回缺少 `file_content:read`，因此不会伪称已具备 REST 绕行能力，也没有静默切换账号。

恢复保留所有先前轨迹和已有设计，数据库备份在 `ui-eval-before-repair-20261026.sqlite3`。`recovery-plan.json` 区分 9 份保留的设计与 12 个可安全补跑的空文件；后者包含 3 个曾被配额挡住的空 Workspace。只有显式恢复模式且实时检查仍为空白、历史确有配额阻塞，才允许同一文件补跑，绝不清空已有设计。

```bash
node scripts/prepare-benchmark-recovery.mjs
python scripts/launch-benchmark-design.py --recovery --runtime-config /path/to/runtime-config.json
```

恢复监督器对保留的设计与后续产物调用用户指定的 `fixed_v4` 量表（22 题、53 分），统一使用已配置的 Opus 5.5 判官，并保留首轮资源中断标签。已有截图和图层数据的评分不再调用 Figma。`progress.json` 同时列出逻辑题数、尝试次数、首轮情况和已评分数量；两种次数不混为“成功率”。

恢复阶段又确认 TokenHub 项目个人额度阻塞：旧配置的 9 次判官请求均返回 403；用户随后提供的凭据也在 6 个配置通道全部返回同样错误，GPT 响应明确包含 `insufficient_user_quota`。接口未返回数值分数，这些记录不算模型设计能力失败。凭据仅保存在忽略版本管理的 `private/model_api_keys.json`（0600），验证证据在 `api-credential-validation-20261026.json`，不含密钥。

恢复监督器按模型连接检查，只提交接口可用的 API 任务；本地 checkpoint 独立继续。每五分钟低频复测，凭据变化立即复测，状态写入 `api-resource-status.json`。判官恢复后，只重试由额度错误中断且没有数值结果的评分，沿用原量表及判官；已有数值结果与非资源型评分错误不会自动覆盖。

本地 checkpoint 后续三题已收尾。第一题有 11 个产品画板。第二题会话因上下文溢出退出：SGLang 日志明确显示 84,934 tokens 超过本轮 H100 可用输入上限 84,878，客户端将其当作普通 500 重试；它仍留下 11 个画板，已只读保留并补截图。后续 benchmark 本地会话显式设置 `CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536` 与自动压缩窗口，为输出和工具结果留余量；此次已经结束的会话不伪称已恢复，也不清空重做产物。自定义模型容量配置依据 [Claude Code 官方说明](https://code.claude.com/docs/en/model-config#correct-the-window-for-a-gateway-or-custom-model-id)。

第三题只交付 6 个画面，且使用 `Status / ...` 名称、尺寸也偏离任务要求。按 `NN_` 命名筛选曾把这些真实画面误认为没有交付，现改为同时采集 Workspace 中具有页面尺寸的非组件库画板；规定名称的缺失仍完整记录，质量和完整性留给原量表。采图、图层统计和交付核验使用相同选择规则。补采只读取 Figma，不修正模型设计、命名或尺寸。

16:41（北京时间）用户再提供一套已授权凭据，6 个模型通道实测均恢复 HTTP 200，证据在 `api-new-credential-validation-20261026.json`。随后已恢复原量表评分与 Opus 空白题目的实际生成；已有 12 份设计的 155 张候选产品画板截图进入原评分队列，组件库和总览板排除且留档。调度器遇到暂时断连时先重新读取已保存批次和评分任务，避免重复提交或直接退出；输入校验和协议错误仍保留为明确故障。

GLM 第二题后续留下 11 个画板，但 ShareGPT 转换报 `invalid role 'function_call'`，原质检状态阻断了自动补图。恢复监督器现在会对已终止、目标文件匹配、真实产物已核验的运行独立补齐截图，随后沿用原量表评分；轨迹错误及原运行状态保留。只读恢复逐条串行执行，失败后至少等待五分钟再尝试，不中断正在进行的模型任务；空 Workspace、活跃运行和未核验产物不会触发这条路径。每次补采在运行目录写入 `benchmark-frame-recovery.json`。

## 正式评分版本：fixed_v4

2026-10-26 用户指定固定型评测 v4 为正式量表。此前 `fixed20` 的 40 分结果不再计入排名，已归档为历史；现有设计按 v4 重新评分，后续产物也只提交 v4。v4 包含 22 道计分题及 G0，满分 53，信息组织和布局质量每题 0–3，其余 0–2。完整冻结定义为 `benchmarks/rubrics/fixed-v4.json`；通用流程见 `docs/benchmark-workflow.md`。本文件上文的 20 条 criteria 和 Q17–Q20 仅描述历史任务检查点及旧量表，不作为 v4 计分题。
