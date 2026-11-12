# Figma benchmark 工作流

实现保存在 `benchmark-design` 分支。当前 21 题仍使用自己的数据库、运行目录和恢复监督器；后续通用批次使用独立目录和端口。

## 固定约定

1. 输入是 N 个原始 Figma URL、可选的原始 query，以及 M 个待评模型。数量不再固定为 7×3；90×8 展开为 720 个任务。
2. 原始文件是只读模板。原始 URL、query 和 case_id 存入带校验值的数据集，导入、重试和导出不会替换它们。已有数据集发生变化时，必须使用新目录和版本。
3. 每个“题目×模型×本轮评测”使用独立 Figma 文件。调用 Figma 原生 File → Duplicate，保留完整规范、组件和素材；不由模型重建模板。
4. 模型只能访问自己被分配的副本。MCP 代理在调用 Figma 前检查 `fileKey`，拒绝原始文件、其他模型副本和没有明确目标文件的调用。模型不能新建其他交付文件。
5. 模型读取 `00 · Start Here`、`01 · Foundations`、`02 · Components`；有 `04 · Media` 时也读取。只在副本的 `03 · Workspace` 创作。Workspace 可以不存在或为空，不能复用已有设计。
6. 只给 URL 时，使用 `benchmarks/templates/initial-design.zh.txt` 生成 query。给了 query 时逐字保存。推理时只将其中出现一次的原始 URL 换成当前副本 URL，不增加产品要求或改写其余正文。
7. rubric 固定使用 `fixed-v4`（方法名 `fixed_v4`）：G0 门槛加 22 道计分题，满分 53。用户体验 A1–A4、可交付性 G1–G2、一致性 E1–E2、视觉表达 F1–F5 每题 0–2；信息组织 B1–B5、布局质量 D1–D4 每题 0–3。题目、评分标准、提示词、图层证据要求和截图上限均锁定在 `benchmarks/rubrics/fixed-v4.json`。当前判官默认沿用 Opus；每轮锁定判官和候选模型配置，不能中途换通道或改 rubric。
8. 继续使用原后端的生成、轨迹收尾、补图和多量表评分实现，评分方法显式指定 `fixed_v4`。单次生成全局串行，MCP 共享账号限流；评分可以与生成并行，但截图只读且串行。额度不足进入资源等待，不编造 0 分。

“有产物”“完整交付”“已评分”“G0 通过”分别记录。无产物、轨迹失败或评分失败都保留原因；没有正式分数时导出 null，不以 0 代替。原 rubric 没有定义的通过分数线不会自行添加。

## 目录与输入

每轮使用 `storage/benchmarks/<run-id>/`：

| 文件 | 用途 |
| --- | --- |
| `dataset.json` | 固定的原始 URL、query、case_id、页面约定和校验值 |
| `plan.json` | 模型配置、判官、rubric 版本和 N×M 任务矩阵 |
| `rubric.json` | 本轮冻结的完整 rubric |
| `copies.json` | 可恢复的原生复制记录及源 URL→独立副本映射 |
| `sources-preflight.json`、`copy-preflight/` | 只读检查原始模板及副本的页面、引用页和空 Workspace |
| `inputs.json` | 已锁定的执行分配表，记录原始 query 和仅换 URL 后的推理 query |
| `ui-eval.sqlite3`、`runs/` | 原后端的任务、轨迹、图层统计、截图和评分记录 |
| `progress.json`、`complete.json` | 进度及本轮收尾状态；`all_scored` 单独表示是否全部取得正式分数 |
| `exports/` | JSON、CSV、Excel 结果及横评汇总 |

题目支持 CSV、XLSX、JSON、JSONL 或每行一个 URL 的 TXT。表格列为 `case_id`（可省略）、`figma_url`、`query`（可省略）、`title`（可省略），也接受导出表中的 `source_figma_url`、`source_query`。一个原始文件在同一数据集中只出现一次。缺少 query 的行按固定模板生成。

```csv
case_id,figma_url
case-001,https://www.figma.com/design/OriginalFileA/
case-002,https://www.figma.com/design/OriginalFileB/
```

模型文件支持现有模型 ID 列表（通过 `--models-api` 从已有配置解析），也支持完整配置。完整配置字段沿用原后端：`id/name/connection_mode/model_id/base_url/api_format/api_key_env/reasoning_mode` 等；额外的 `generation_mode` 可指定 cc/direct。`judge` 指定固定判官。JSON 里禁止保存明文 API Key；继续使用环境变量名或 0600 私有密钥存储。

## 操作入口

以下路径是示例；90 个真实原始 URL 和 8 个模型尚未提供时，只准备和验证流程，不提交 720 次真实推理。

```bash
# 1. 固定原始数据；已有 query 不改写，只有 URL 则生成 query。
npm run bench -- import --dir storage/benchmarks/run-001 \
  --input tasks.xlsx --id design-bench-v1

# 2. 固定模型矩阵与当前 rubric。
npm run bench -- plan --dir storage/benchmarks/run-001 \
  --models models.json --models-api http://127.0.0.1:18174 --id run-001

# 3. 原生复制，核验副本。认证路径指向已授权账号的现有配置。
# 可先加 --limit 1 验证一份；再次执行会接着处理未完成副本。
npm run bench -- copy --dir storage/benchmarks/run-001 \
  --browser-config /absolute/path/to/private/browser-config.json \
  --mcp-config /absolute/path/to/global-figma-mcp.json \
  --python /absolute/path/to/venv/bin/python

# 4. 启动本轮独立的原后端，不使用旧网页 URL。
npm run bench -- start --dir storage/benchmarks/run-001 \
  --runtime-config /absolute/path/to/runtime-config.json --port 18184 \
  --credentials /absolute/path/to/private/model_api_keys.json

# 5. 幂等导入并启动后台生成和原 rubric 评分。
npm run bench -- run --dir storage/benchmarks/run-001 --background

# 6. 查看状态及随时导出，不等待整轮结束。
npm run bench -- status --dir storage/benchmarks/run-001
npm run bench -- export --dir storage/benchmarks/run-001 --output storage/benchmarks/run-001/exports
```

安装和模型运行依赖仍通过现有 `runtime-config.json` 提供，包括 Python、Claude Code、claude-tap、转换器及 Figma MCP 认证路径。本地模型使用原后端的 runtime 配置与连接检测，先保证相应 checkpoint 服务就绪；外部模型通过已配置的 API/兼容层运行。工作流不会借用或停止别人的 GPU 作业。浏览器配置结构见 `benchmarks/examples/browser.example.json`；浏览器与 MCP 应使用同一个已授权账号。

已有经过核验的独立副本时，也可以 `bench bind --dir ... --input copies.xlsx` 导入映射；每行须有 `case_id/model_id/target_figma_url` 或 `assignment_id/target_figma_url`，必须覆盖矩阵且不能指向原始文件或复用另一任务的副本。实际运行前仍进行原后端的空 Workspace 检查。

## 重复执行与恢复

- 再次导入相同内容不会生成重复题目；修改原始数据、模型矩阵或 rubric 时必须显式创建新版本/新轮次。
- `run` 可以再次执行并接续已导入任务；已提交批次、已产生的设计和已有基准分不会重复生成或覆盖。使用同一轮目录，不会因为程序重启而重复提交。
- 复制请求返回不明确时保留 `duplicate_requested/ambiguous` 记录，停止自动复制，先核对现有副本后再继续，防止重复创建文件。
- API 额度或服务暂不可用时低频复测，资源等待与模型失败分开；Figma 限额前置检查不创建假失败运行。
- 已中断且实时检查仍完全空白的副本，才允许基础设施重试；只要留下任何部分设计，保留产物，不清空重做。
- 轨迹格式转换错误会保留在原运行状态中。若实际设计可以核验，则独立补齐只读截图及图层证据，再交给原 rubric 评分。
- 图像或图层证据未齐全时不提交评分。评分接口错误保留错误信息，不填假分数；所有真实评分结束前，不能宣称全量评分完成。

`complete.json` 的 `finished` 表示所有任务都有明确结局，`all_scored` 表示全部拿到正式分数；存在真正无交付或不可评分结果时，两者可能不同。基础设施仍在等待恢复时，不写完成标记。

## 导出与横评

导出包括：

- `dataset.json`、`cases.csv/xlsx`：固定的 N 条原始 URL 和 query，用于下次重新导入。推荐原样保留封存的 `dataset.json`，它也包含 query 模板版本。
- `results.json/csv/xlsx`：N×M 行，分别记录源 URL、源 query、副本 URL、推理 query、模型、尝试次数、运行状态、A1–A4、B1–B5、G1–G2、D1–D4、E1–E2、F1–F5、G0、总分、评分错误和时间。JSON 另含逐题证据与全部尝试记录。
- `rubric.json`：本次采用的完整 rubric 及校验值。
- `summary.json/csv/xlsx`：每个模型的已评数量、覆盖率对应的分母、已评分均分，以及所有模型共同已评分题目的均分。

未完成时可以导出。全量均分与共同题目均分分别展示，避免部分覆盖的模型被当作已经完成同一套横评。新一轮使用新的 run-id 和新副本，继续引用同一个原始数据集；原始 N 个 URL 不随轮次或模型变化。

## 验证

```bash
node --test tests/benchmark_protocol.test.mjs tests/benchmark_suite.test.mjs \
  tests/benchmark_runtime.test.mjs tests/benchmark_fixture.test.mjs
python tests/benchmark_table_test.py
```

验证覆盖 90×8 展开、只替换 URL、原始文件保护、00/01/02 加可选 04、复制中断不重复执行、幂等导入、断点续跑、原 rubric 评分与 JSON/CSV/Excel 导出。外部模型或 Figma 的可用额度以真实运行时的资源检查为准。

## 2026-10-26 正式量表切换

用户明确指定使用固定型评测 v4。旧 `fixed20`（20 题、40 分）结果只保留为历史，不参与本轮或后续正式排名；不能将旧分数折算成 v4 分数。评分必须重新读取实际截图和图层证据，按 v4 原题与各题标准逐项判断。判官仍为已配置的 Opus 5.5。

当前 21 题的恢复监督器显式提交 `fixed_v4`，复用现有设计、截图及图层，不为更换量表重新生成设计。正式口径保存于 `storage/benchmark-design/scoring-policy.json`，`progress.json` 带方法、题数、满分和 rubric 校验值；旧进度与分数归档到 `history/fixed20-superseded-20261026/`。只有 21 个逻辑题目都取得 v4 正式分数，才生成新的完成标记。

通用新批次默认也使用 v4。原先封存的 v1 计划不原地篡改校验值；需要显式建立 v4 版本。本分支前端、后端默认评分方法为 v4，历史量表可以显式查看。
