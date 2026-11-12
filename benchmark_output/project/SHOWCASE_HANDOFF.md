# 发布会展示页 /showcase — 交接说明（2026-10-17）

## 观众登录 Figma（2026-10-19 更新，以此为准）

Figma 已不再给新客户端开放动态注册（只放行 MCP Catalog 里的客户端，任何网络注册都返回 403），
但生成端 2026-07-22 注册的**共享客户端**一直可用——所有账号都是复用它授权的。展示页同样复用它：
服务端从评测端自己的 Figma 凭据（或 `storage/private/showcase-oauth-client.json`）里取 client_id/secret，
secret 不下发浏览器；换 token / 刷新 token 从服务器都能通。

观众点「使用 Figma 登录」→ 弹窗里登录 Figma 并点允许 → 两种收尾（`showcase.json` 的 `oauth_redirect`，改了即时生效）：
- `server`（默认）：跳回本服务 `/api/showcase/figma/callback`，服务端换 token、whoami 验证、弹窗自关，全自动。
- `loopback`：若 Figma 只认回环回跳（生成端脚本用的就是 `http://127.0.0.1:<端口>/callback`），弹窗停在「无法访问」，
  观众把弹窗地址栏粘回页面一次，服务端完成兑换。

先用默认 `server` 试；弹窗里 Figma 报 redirect_uri 不合法时，切到 loopback：
`curl -X PUT -H 'content-type: application/json' -d '{"oauth_redirect":"loopback"}' http://127.0.0.1:4173/api/showcase/config`

## 最新进展（2026-10-17 晚，覆盖下文中过时的部分）

**3 个 showcase 已生成并选定**（ckpt-270，评测端常规 cc 单 agent 链路，轨迹照常记录在各自 run 目录）：

| 样例 | test | run | 轮数 / 用时 | 结果 |
|---|---|---|---|---|
| 周末短途旅行 App | TEST-112 | `run_4541f06f48a14e74` | 15 / 7.7 分钟 | 3 屏 + 7 条原型连线 |
| 个人记账理财 App | TEST-115 | `run_e56d17d526004e6e` | 18 / 12 分钟 | 3 屏，无重叠；连线因配额未写入 |
| 电商运营看板 Web | TEST-114 | `run_5b5b487a81034181` | 14 / 9.7 分钟 | 2 屏 + 6 条原型连线 |

- 提示词按评测端成功 query 的格式写，题材参考 Figma 社区同类热门 UI Kit；原文在 `/tmp/sft-showcase-cases/*.json`（TEST-115 是 TEST-113 的改进版：切换条单独一行、不用背景模糊、涨跌标签放数字旁）。
- 淘汰的版本：`run_9061bc8f17844fc4`（撞配额只做 1 屏）、`run_fb90bfd1d7f44953`（层叠问题）、`run_c00780e7b496480a`（图标空白）。
- **最大的不稳定因素是评测账号 xinya-old 的 Figma Education 每分钟调用上限**：模型一撞上就按平台规则如实报告并收工。演示建议换 Professional 付费席位账号。

**作品墙配置** `storage/private/showcase.json`（已写好，重启后生效）：3 个样例置顶；模型 = ckpt-270 + `model_sglang_arc`；隐藏 12 件（老 checkpoint 空白/调试/过稀 9 件 + 上面 3 个淘汰版本）。预览实例实测：39 件作品、452 屏。

**观众登录 + SFT 新建**（代码已完成，未上线）：
- 现场页「新建设计 / 改我的文件」两种模式；新建在观众自己的团队建文件，query 自动带训练集同款收口句（≤3 画板、只截一次图）。
- 登录改为**浏览器端 OAuth**（`src/showcase/figmaOAuth.mjs`）：服务器调 api.figma.com 注册/换 token 实测 403，但这两个接口 CORS 放开；PKCE 由 `GET /api/showcase/figma/pkce` 生成（http 内网地址没有 crypto.subtle）；回跳地址 `<origin>/showcase.html`。
- 未验证：Figma 是否接受 `http://<内网IP>:4173/showcase.html` 作为回跳地址（只能在真实浏览器点一次）；服务器无法刷新观众 token，过期需重新登录。失败时页面会引导「粘贴授权凭据」。

**仍需人工**：4173 后端未重启（重启命令被权限拦截）。确认没有运行中的 run 后执行：
`tmux kill-session -t ui_eval_platform && bash scripts/ui-eval-watchdog.sh`
重启后：打开 `/showcase` 看作品墙（应有 39 件、3 件置顶），再用一个 Figma 账号试一次「使用 Figma 登录 → 新建设计」。

---


按计划 `/root/.claude/plans/sft-figma-figma-sft-snazzy-meerkat.md` 实现。代码全部在本仓库（评测端，端口 4173），**未提交**；仓库里原本就有别人的未提交改动（`server/local_model_runtime.mjs`、`tests/local_model_runtime.test.mjs`、`src/App.jsx` 里 ArcRuntimePanel 那两行），没有动它们。

> 本仓库 git 需要：`git -c safe.directory=$PWD ...`

## 当前状态

| 项 | 状态 |
|---|---|
| 前端构建 | ✅ 已 `npm run build`，`dist/showcase.html` 已生成，评测端侧栏「发布会展示 ↗」已可见 |
| 测试 | ✅ 新增 `tests/showcase.test.mjs` 11/11；全量 `npm test` 308/308 |
| 真实数据预览 | ✅ 用真实库的快照起了临时实例（127.0.0.1:4199，已停）截图检查：首页/作品墙/详情/现场改稿/手机宽度均正常；作品墙 16 件、294 屏 |
| 后端上线 | ❌ **4173 还没重启**，`/showcase` 和 `/api/showcase/*` 在旧进程里不存在 |
| 真实 Figma 登录 + 真实改稿 | ❌ 未端到端验证（需要真实观众凭据 + 重启后的后端） |

## 待办：重启 4173

- 计划要求在没有运行中的 run 时重启。写交接时还有 run `run_9bbaa0a3b62642f0` 在跑、一个评测批次为「运行中」。
- 当前 4173 进程（pid 3244527）是从终端 pts/0 前台启动的，不是看门狗的 tmux 会话 `ui_eval_platform`，所以没擅自停。
- 做法：确认空闲 → 停掉该进程 → 运行 `scripts/ui-eval-watchdog.sh`（健康检查失败后会在 tmux 里重新拉起服务）。
- 重启后检查：打开 `http://<host>:4173/showcase` → 作品墙加载 → 点进详情 → 「返回评测」。

## 改动文件

新增：
- `server/showcase.mjs` — 纯函数：配置归一化、作品卡片字段（标题拆名/标签）、轨迹→Figma 操作时间线、链接校验、凭据 JSON 校验、OAuth PKCE、改稿任务阶段/排队位置、作品墙排序
- `server/showcase_whoami.py` — 用观众凭据调 Figma `whoami`，返回身份与团队列表（复用生产端 `figma_auth.access_token` 刷新）
- `showcase.html`、`src/showcase/main.jsx`、`src/showcase/Showcase.jsx`、`src/showcase/showcase.css` — 独立前端入口
- `tests/showcase.test.mjs`

修改：
- `server/index.mjs`
  - 引入 showcase.mjs
  - `getBootstrap()`：`SHOW-*` 测试及其 run 不进评测端列表
  - `importRunResult()`：`SHOW-*` 不自动补图（评测端账号打不开观众的文件）
  - `/api/tests/:testId/run`：新增 `showcase_launch` 一次性 nonce，命中时本次 run 的 `figma-mcp.json` 换成观众凭据、系统提示词用观众身份；请求体里直接给路径不认
  - 抽出 `runTraceContext()` 供 trace 接口和展示页共用
  - 新增「发布会展示页」段：全部 `/api/showcase/*` 路由；`GET /showcase` 指向 `dist/showcase.html`（在 SPA 兜底之前）
- `vite.config.js` — `rollupOptions.input` 多入口（main + showcase）
- `src/App.jsx`、`src/styles.css` — 侧栏加「发布会展示 ↗」链接

## 接口一览

| 接口 | 作用 |
|---|---|
| `GET /api/showcase/gallery` | 作品墙：hero 文案、模型名、统计、作品列表 |
| `GET /api/showcase/works/:runId` | 作品详情 + Figma 操作时间线 + embed 链接 |
| `GET/PUT /api/showcase/config` | 展示配置，存 `storage/private/showcase.json` |
| `GET /api/showcase/me` | 登录状态、已用/上限次数、我的改稿列表 |
| `GET /api/showcase/figma/login`、`/callback` | 服务端 OAuth（发现端点→动态注册→PKCE） |
| `POST /api/showcase/figma/credential` | 备用登录：粘贴凭据 JSON |
| `POST /api/showcase/logout` | 退出并删除该浏览器的凭据目录 |
| `POST /api/showcase/edits` | 提交改稿 `{figma_url, prompt}` → 建 `SHOW-xxx` 编辑任务并入队 |
| `GET /api/showcase/edits/:id/stream` | SSE 进度（阶段、排队位置、操作步骤、实时截图、最终结果） |
| `POST /api/showcase/edits/:id/cancel` | 取消排队中的任务 |

## 配置默认值（`storage/private/showcase.json` 不存在时）

- 作品墙模型：`model_local_a282d9c9a73446c8`（Qwen3.8-27B Figma Edit · ckpt-270）
- 改稿模型：同上
- 上墙状态：`等待评分`（质检未过的「结果不完整」默认不上墙，可用 `pinned` 置顶指定 run）
- `hidden`：隐藏的 run id；`max_items` 48；每个浏览器改稿上限 `edits_per_session` 5

## 需要知道的行为

- **Figma 页内登录大概率不通**：从本机房 POST api.figma.com 的 OAuth 注册返回过 `Forbidden`（与 `figma_mcp_auth_mac.py` 注释一致）。失败时页面会提示改用「粘贴授权凭据」：观众在自己电脑运行 `figma_mcp_auth_mac.py`，把打印的 JSON 粘进来。
- **改稿只在观众给的文件里做**：走既有编辑模式（`base_figma_url` 非空 → 不给 `create_new_file`，提示词限定在该文件）。
- **排队**：本地模型并发有限且与评测批量共用，改稿任务在队列里等空位。
- **会话**：httpOnly cookie `showcase_sid`；凭据存 `storage/private/showcase-users/<sid>/`（0600）；改稿队列存 `storage/private/showcase-jobs.json`，重启后排队中的任务不丢。
- **测试编号**：评测端既有的建测试逻辑按测试总数编 `TEST-xxx`，每多一条 `SHOW-*` 会让下一个 TEST 编号跳一号（不会冲突）。
- **Figma 实时画布 iframe**：只有文件设为「知道链接的人可查看」才能显示，默认用截图。

## 演示快捷键

F 全屏；详情页 ←/→ 翻屏、空格自动轮播、Esc 回作品墙。页面不依赖外部字体/CDN。

## 后续可做

1. 空闲时重启 4173 并按上面的检查项走一遍。
2. 用一个测试 Figma 账号走完整流程：登录（或粘贴凭据）→ 贴自己文件链接 → 提交改稿 → 看 SSE 进度 → 确认原文件被修改。
3. 视需要在 `showcase.json` 里置顶/隐藏作品、改 hero 文案。
