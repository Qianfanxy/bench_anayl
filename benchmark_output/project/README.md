# UI Eval

`benchmark-design` 分支的批量 Figma 横评入口为 `npm run bench -- ...`；原始文件保护、独立副本、锁定 v4 rubric（22 题、53 分）、后台运行和导入导出见 [Figma benchmark 工作流](docs/benchmark-workflow.md)。

供团队内部使用的 Figma MCP 模型评测平台。打开网站后选择测试 Query 和模型，
运行模型，查看生成结果与 cc-tap 轨迹，再使用固定型评测 v4（22 题、53 分）完成评分。

平台只有两个页面：

- **评测工作台**：选择或新建 Query、测试模型连接、生成 Figma 结果、查看轨迹并评分。
- **评分结果**：查看所有评测人的独立评分，筛选结果并导出训练包。

## Quick Start

要求 Node.js 22.5 或更高版本。

```bash
npm install
npm run build
npm start
```

默认监听 `0.0.0.0:4176`。本机访问 `http://127.0.0.1:4176`。

## Shared Evaluation

- 第一次访问只填写姓名，不需要账号或密码。
- 浏览器本地保存随机评测人 ID 和显示姓名。
- 测试 Query、检查点、模型运行结果和评分统计保存在服务端 SQLite，所有访问者共享。
- 每位评测人在同一条测试上拥有独立评分，不会覆盖其他人的结果。
- 新测试默认由服务器 Claude Code 根据 Query 生成 100 个共享检查点，也可切换为通用模板。
- 新增或删除检查点后，旧评分会显示“需要补评”，补完后重新换算为 100 分。

## Server Configuration

复制 `.env.example` 为 `.env`，配置服务器路径：

```dotenv
UI_EVAL_HOST=0.0.0.0
UI_EVAL_PORT=4176
UI_EVAL_STORAGE_PATH=./storage
CLAUDE_CODE_PATH=/absolute/path/to/claude
CLAUDE_TAP_PATH=/absolute/path/to/claude-tap

PIPELINE_ROOT=/absolute/path/to/data_pipeline_of_distillation_from_claude_code_via_figma
CTTAP_RUNNER_PATH=/absolute/path/to/cttap_distill_runner.py
CTTAP_REPO_PATH=/absolute/path/to/claude-tap-converter
UI_EVAL_RUN_CWD=/absolute/path/to/agent/workspace
UI_EVAL_MCP_CONFIG_PATH=/absolute/path/to/private/figma-mcp.json
UI_EVAL_PERMISSION_MODE=acceptEdits
```

`CTTAP_REPO_PATH` 必须包含 `cttap/cli.py`。可通过健康检查确认：

```bash
curl http://127.0.0.1:4176/api/health
```

## Models

默认包含三类配置：

- 服务器已登录的 Claude Code，使用 `auth-mode auto`。
- 服务器 Opus 5 与 Fable 5，使用登录态 Claude Code 的完整模型 ID。
- API Claude Code，使用 Anthropic-compatible API。
- 服务器部署的 SGLang 模型。

选择 `ARC-SFT-27B` 后提供两种独立运行方式：

- **直接生成**：SGLang 直接执行多轮 Anthropic Messages 与 Figma MCP 工具循环，
  不启动 Claude Code、CC Switch 或 cc-tap。
- **CC 生成**：为当前运行创建独立 `CLAUDE_CONFIG_DIR`，由 Claude Code 连接本地
  SGLang，再通过 cc-tap reverse 模式捕获轨迹；不会修改终端的全局 CC Switch 配置。

两种方式共用 Query、澄清结果、Figma 账号和检查点，但会保存为两条独立运行记录，
评分也互不覆盖。直接生成仍会写出 canonical `trajectory.jsonl`、`trace.sqlite3`、
可见 reasoning、token、Figma URL 和截图；其来源标记为 `direct-sglang`。本地模型无法
生成 Anthropic 私有 thinking signature，因此直接模式只豁免该项，创建文件、写入、
原型连线、截图、URL 和 reasoning 仍按生产规则严格检查。

直接生成需要 `UI_EVAL_DIRECT_SYSTEM_DATA` 指向一份现有训练 JSONL，并要求
`UI_EVAL_PYTHON` 环境已安装 `mcp` 与 `httpx`。本地模型的 checkpoint、LoRA、GPU、
端口和 TP 可在网页模型设置中编辑，运行配置由 `UI_EVAL_LOCAL_MODEL_CONTROLLER`
指定的控制器管理。

“测试连接”会真实启动一次无工具 Claude Code 探针，不创建 Figma 文件，也不写入
训练轨迹。正式测试通过 cc-tap reverse 模式捕获请求，再进入内置兼容代理；代理会
移除部分上游不支持的 beta 参数，但不会记录请求头、正文或密钥。

服务器上的 Figma OAuth 可通过 `server/figma_mcp_stdio_proxy.py` 转为本地
stdio MCP。私有 MCP 配置只保存脚本路径和认证文件路径；认证文件与配置文件均应设为
`600`，并放在 `storage/` 等 Git 忽略目录中。

API Key 只从服务端环境变量读取。模型配置保存的是环境变量名称，例如
`ANTHROPIC_API_KEY`，不会保存真实密钥。

## Run And Export

```text
测试 Query
  -> 直接 SGLang 或 Claude Code
  -> direct trace 或 claude-tap / trace.sqlite3
  -> trajectory.jsonl / reasoning / signature
  -> Figma 截图与链接
  -> 多人独立评分
  -> training bundle
```

结果页支持：

- `ui-eval-ratings.jsonl`
- `ui-eval-training-bundle.zip`

Bundle 包含共享测试与检查点、所有评分、每条测试的 trajectory、SQLite 和媒体文件。
包内路径均为相对路径。

## Security

- `.env` 权限应设为 `600`。
- API Key 不进入网页、数据库、日志、导出包或 Git。
- `storage/`、SQLite、日志、依赖和构建产物均在 `.gitignore` 中。
- 提交前执行敏感信息扫描：

```bash
rg -n 'sk-[A-Za-z0-9_-]{16,}' . \
  --glob '!node_modules/**' --glob '!dist/**' --glob '!storage/**'
```
