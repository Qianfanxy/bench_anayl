# agent.md — chloehxy 分支相对 master 的全部改动

> 基线：`master` @ `50ccba5`（两分支同点，本文件描述的即当前工作区相对 master 的完整增量）
> 范围：17 个文件，+2727 / −233
> 一句话：给评测端加上**「改已有 Figma 文件」这一整条链路**——截图拉框标注 → 计划（Plan）预演 → 带标注/计划的轨迹生成 → 质检口径适配；顺带清掉遗留的澄清弹窗。

---

## 符号约定

| 符号 | 含义 | | 符号 | 含义 |
|:---:|---|---|:---:|---|
| `✚` | 新增文件 | | `⟨DB⟩` | SQLite 表结构 |
| `✎` | 修改文件 | | `⟨API⟩` | HTTP 接口 |
| `✖` | 删除的代码单元 | | `⟨PRM⟩` | 送进模型的提示词 |
| `⚑` | 行为变更，会影响线上既有数据 | | `⟨UI⟩` | 前端界面 |
| `⚠` | 已知问题 / 未收尾 | | `⟨QC⟩` | 轨迹质检 |

---

## 一、改动清单（按文件）

### ✚ 新增

| 文件 | 行数 | 作用 |
|---|---:|---|
| `server/annotations.mjs` | 169 | ⟨PRM⟩ 标注数据的规范化与提示词段落生成。导出 `ANNOTATION_QUERY_LINE = "修改区域为图片标红部分"`，作为标注段落首行 |
| `server/plan_options.mjs` | 177 | ⟨PRM⟩ Plan 提示词 `planPrompt()`；`normalizeBox()`（0–1 夹取 + 四位小数）、`normalizeFrame()`（1-based→0-based，非法置 `null`） |
| `src/FrameAnnotator.jsx` | 405 | ⟨UI⟩ 截图拉框标注器（矩形 / 折线，SVG 归一化坐标） |
| `scripts/seed-edit-queries.mjs` | 100 | 把 16 条编辑需求灌进 `tests` 表，支持 `--only B-01`、`--dry-run` |
| `tests/annotations.test.mjs` | 136 | — |
| `tests/plan_options.test.mjs` | 163 | — |
| `0_query_fix_example.md` | 60 | 16 条编辑需求的原始输入（含各自目标 Figma 文件 URL），留档以便复现 seed |

### ✎ 修改

| 文件 | 增减 | 关键改动 |
|---|---:|---|
| `src/App.jsx` | +822 | ⟨UI⟩ 主战场，见 §3 |
| `server/index.mjs` | +400 | ⟨DB⟩⟨API⟩ 见 §2 |
| `src/styles.css` | +237 | 标注层、Plan 栏、任务简介卡、编辑标；`✖` 删 `.plan-zoom*` / `.plan-option-row` |
| `server/direct_sglang_runner.py` | +120 | 直连链路支持随首轮 user 消息发标注图，见 §4 |
| `server/figma_binding.mjs` | +54 | ⟨PRM⟩ `figmaSystemPrompt(binding, teamName, { direct, editTarget })` 增加编辑模式 |
| `server/runner_args.mjs` | +29 | `appendSections()` / `clarificationSection()` / `withAnnotationArgs()` |
| `server/trajectory_quality.mjs` | +12 | ⟨QC⟩ `requireNewFile` 开关 |
| `tests/figma_binding.test.mjs` | +37 | — |
| `tests/trajectory_quality.test.mjs` | +29 | — |
| `tests/runner_args.test.mjs` | +10 | — |

测试总数 **222**，pass 218 / fail 0 / skip 4；`npm run build` 通过。

---

## 二、后端 `server/index.mjs`

### ⟨DB⟩ 新增列（均走 `ensureColumn`，旧库原地升级，无需迁移脚本）

```
tests.base_figma_url     TEXT ''    ⚑ 非空即「编辑已有文件」任务
tests.annotation         TEXT ''       标注图形（JSON）
tests.plan_options       TEXT '[]'     Plan 生成出的候选项
tests.plan_selection     TEXT ''       用户勾定的项
runs.base_figma_url      TEXT ''       起跑时的目标文件快照
runs.annotation_file     TEXT ''       本轮实际带进去的标注图
runs.plan_selection      TEXT ''       本轮实际带进去的计划
models.vision            INT  1        该模型能否吃图
```

`runs.*` 三列是**快照**而非外键：事后复盘「这轮为什么跑歪」，第一件事是问它当时带了什么，
而 test 上的标注/计划随时会被改掉。

### ⟨API⟩ 新增接口

```
PUT    /api/tests/:testId/annotation          保存标注（图形 + base64 图）
DELETE /api/tests/:testId/annotation          清除
GET    /api/tests/:testId/annotation/image    取标注图
GET    /api/runs/:runId/annotation/image      取「那一轮」用的标注图（路径做了包含性校验）
POST   /api/tests/:testId/plan/generate       让模型读图出计划
PUT    /api/tests/:testId/plan                勾定计划项
```

### 关键内部函数

- `resolveTestBaseImage(test)` → `{ source: "annotation"|"run", frames:[{index,file,url,page_name}] }`
  run 分支取 `derivePagePreviews(...) + fetchedFramePages(run.run_dir)`，**与 `normalizeRun().preview_files` 严格同源**——
  否则 Plan 里的 `frame` 下标和前端翻页对不上，框会画到另一张图上。
- `planVisionInputs(test, model)` → `{ annotation, baseImage, frames, imagePaths, section }`
- `publicBaseImage(test)` → 前端首屏用的 Figma 预览（即便一轮都没跑过也有图）

### ⚑ 提示词组装口径变更

```js
const fullQuery = appendSections(test.query, [
  annotationPromptSection(annotation, { mode: annotationMode, imagePath: annotationFile }),
  planPromptSection(planSelection),
]);
```

`✖ clarificationSection` 已从组装链路移除（澄清弹窗废弃，见 §3）。
`appendSections` 在所有段落为空时**原样返回 query，一个字节都不多**——
几百条历史 run 的首轮提示词就是裸 query，多一个换行，跨版本比基线就不干净了。

### 其他

- `✎` 两处硬编码 `/usr/local/bin/python3` → `pythonBin`（`UI_EVAL_PYTHON`）。原环境无此路径，质检必 ENOENT。
- `⚑` seed 不再把 ARC-001 绑到 `model_claude_api`，改为 `null`。**见 §6。**

---

## 三、前端 `src/App.jsx`

### ✚ 新增组件

| 组件 | 作用 |
|---|---|
| `EditBadge` | 列表/详情标出「UI 编辑」，与从零生成区分（两者判分口径不同） |
| `RunInputTags` | 某轮带没带标注图、带没带计划 |
| `AnnotationOverlay({shapes})` | SVG `viewBox="0 0 1 1"` + `vectorEffect="non-scaling-stroke"`，**叠在普通预览上**，不再只有进标注器才看得见 |
| `HighlightBox` / `PreviewImage` | Plan 项 hover 时在原图上高亮对应区域 |
| `TaskBrief` | 首屏「干净态」：左侧原始任务 + 红色追加行 `修改区域为图片标红部分` |

### ✖ 删除

- `ClarificationPanel`（183 行）与 `DECIDE_FOR_ME` — 「开跑前，先把这几件事定下来」弹窗，
  确认为历史遗留，废弃。⚠ 服务端 `/api/clarifications` 路由仍在，**未清理**。

### ⚑ 行为变更

1. **首屏干净**：`runFromHistory` 状态提升到 `App()`；只有点历史记录 / 打开评分 / 主动起跑才预览轨迹，
   `selectTest` 时置 `false`。初次打开一条数据 = 左边任务 + 右边 Figma 预览，不自动铺历史轨迹。
2. **起跑不再串场**：`startRun` 先 `setSelectedRunId("")` 再 `setRunning(true)`。
   否则 POST 返回前的那几秒，`selectedRun` 还是上一轮，页面会把旧的 10 个轮次连同
   「模型正在继续下一步…」一起渲染出来，3 秒后再闪成空白。**这是前端时序，不是后端逻辑**——
   后端每次都新建 run 行、新目录、新进程。
   配套：`EmptyPreview` 增加 `running && !run` 分支，显示「正在启动新一轮」。
3. **标注白屏**：`) : annotating && selectedRun ? (` 守卫。`FrameAnnotator` 在没有 run 时崩，
   effect 拦不住同一次 render 的崩溃，只能在 render 分支上挡。
4. **Plan 不再每项配图**：`splitStage = Boolean(selectedRun) && !annotating && hasVisual`，
   打开 Plan 时右侧 Figma 图**保持在原位**；hover 某项 → `highlightPlanRegion()` 设高亮并跳到对应页。
   `.canvas-stage.split:has(.plan-column)` 用 `8fr / 5fr`。
   ⚑ 之前给每项单独裁图，`aspect-ratio` + `height` + `max-width` 打架导致图被拉伸。
5. **⟨UI⟩ 按钮文案**：`新一轮测试` → **`运行`**（顶栏主按钮与失败态重跑按钮各一处）。
   ⚠ 同一按钮在「还没有任何 run」时仍显示 `开始测试`，未一并改，需要的话可统一。

---

## 四、直连链路 `server/direct_sglang_runner.py`

新增 `--query-image`（可重复）。不传 = **完全是老行为**，首轮内容仍是裸字符串。

三处必须同时改，少一处标注图就白送：

1. `anthropic_to_openai_body()` — 顶层 `image` / `text` 块原本只认 `tool_result`，
   `⚠` 漏收会让**整条 user 消息进不了 messages**，需求正文凭空消失，模型上来就问「你要我做什么」。
2. `prune_history()` — 补 `index == 0` 条件。带图时首轮是 content 列表，
   会掉进压缩分支被 `_clip` 砍到 300 字，需求本身被砍没。
3. `load_query_images()` — 读不出来的图**跳过而非报错**：正文里还有一份文字清单，
   为一张图让几十分钟的生成不启动不划算。

图排在文字前面：先看见圈了哪儿，再读要求，和人的阅读顺序一致。`self_test()` 覆盖以上三条。

---

## 五、编辑模式的提示词与质检

### ⟨PRM⟩ `figmaSystemPrompt(..., { editTarget })`

编辑模式下：

- `✖` 禁用 `create_new_file`（工具白名单层面），必须改目标文件本身
- 先读后写：改之前要 `get_metadata` / `get_screenshot` 看清现状
- 保留既有原型连线，不得因为改一屏把跳转关系打断
- ⚑ 逐屏规则原文：**「长得像的屏不是同一屏……绝不要把一屏的偏移量照搬到另一屏。」**
  这条是实跑出来的——模型会把 A 屏量到的 y 值直接套到 B 屏上。

### ⟨QC⟩ `trajectory_quality.mjs`

新增 `requireNewFile` 选项；编辑轨迹豁免 `MISSING_NEW_FILE = "Figma create_new_file was not called"`。
不豁免的话，所有编辑任务都会被判「没建文件」而整批不合格。

---

## 六、⚑⚠ 运行约束（接手必读）

**模型一律选「服务器 Opus 5」，不要选「API Claude Code」（`model_claude_api`）。**
后者用的是个人 API Key 和额度，不是团队服务器登录态，批量评测会直接花个人的钱。
种子数据历史上把它设成了默认模型，**不能依赖默认值**，脚本里要显式写模型 id。

服务器登录态的 Opus 5 在 runner 注入「Reasoning summary:」采集指令时会被防护判成
`reasoning_extraction` 而整条拒答（首轮即拒，约 7 秒失败）。不需要采集推理的任务用
`reasoning_mode=none` 的那条配置（`model_claude_opus5_edit`「服务器 Opus 5（编辑任务·不采集推理）」），
它同样是服务器登录态。

---

## 七、⚠ 已知未收尾

| 项 | 说明 |
|---|---|
| `/api/clarifications` | 前端面板已删，服务端路由与 `server/clarifications.mjs` 仍在，可单独清理 |
| `开始测试` 文案 | 见 §3.5，未与 `运行` 统一 |
| B-01 `01b_定位失败态` | 模型引入的重叠回归，已知未修 |
| `run_486246599fa24791` | 调试期误起的一轮（TEST-013 / B-02），记录已删除，**无法回溯确认它是否对 B-02 产生过局部写入**。要确认需重新补图比对 |
