# Figma 设计评测结果交付（人评 Arena 用）

交付日期：2026-11-03　整理人：huangxinyue
目录：`/mnt/afs/huangxinyue/projects/benchmark-design/deliver-20261103/`（约 376 MB）

## 一、范围

4 轮评测共 29 道题、7 个模型、**177 份结果，全部已出分**，截图共 1237 张。

| 轮次 | 题数 | 模型数 | 结果份数 | 说明 |
|---|---:|---:|---:|---|
| 3case | 3 | 7（含 Qwen） | 21 | 移动端 |
| 6case | 6 | 6 | 36 | 移动端 |
| 10case | 10 | 6 | 60 | 移动端 |
| web10 | 10 | 6 | 60 | 网页端 |

- **CC 分**：fixed_v4 量表，22 个分项，满分 53，先过 G0 准入门槛。判官是 Opus 5.5。
- **Qwen3.8-27B ckpt-270 只参加了 3case**，其余三轮都是 6 个模型。做同题抽签时，模型池按轮次区分。

## 二、目录结构

```
manifest.json         完整清单：每份结果一条，含分项、判官依据、截图列表与哈希
manifest.csv          同一份清单的表格版（UTF-8 BOM，Excel 可直接打开），每份结果一行
frames-sha256.txt     全部截图的 SHA-256，可用 sha256sum -c frames-sha256.txt 校验
frames/<轮次>/<题号-题名>/<模型>/NN_<画板名>.png
requirements/<轮次>/<题号-题名>.md   每题完整需求：00 设计任务页、01 视觉规范页的全部文字，英文原文
requirements/raw/<模板file_key>.json 同上的原始提取结果，含文字节点 id 和坐标
tools/                生成脚本，可重跑
```

## 三、清单字段（manifest.json → items[]）

| 字段 | 含义 |
|---|---|
| `round` `case_id` `title` | 轮次、题号、题名 |
| `source_figma_url` | 原始模板链接（只读） |
| `model_id` `model_name` | 模型 |
| `account` | 运行这次推理的 Figma 企业账号 |
| `copy_figma_url` `copy_file_key` | 模型实际作答的副本 |
| `workspace_page_id` | 副本里「03 · Workspace」页的 id，只有这一页是交付稿 |
| `workspace_top_level` | 03 页上全部顶层节点，包括组件板 |
| `score_total` `g0_pass` `g0_reason` | CC 总分、G0 是否通过、G0 理由 |
| `items` `item_evidence` | 22 个分项的分数，以及判官给出的逐项依据 |
| `frames[]` | 判官打分时看的截图：`label` 画板名、`node_id`、`file`、`width`/`height`、`sha256` |
| `run_id` `run_dir` `source_round_dir` `is_rerun` | 可追溯到原始 run；`is_rerun=true` 表示这份来自补跑 |
| `minutes` `turns` | 推理用时（分钟）和轮数 |

`meta` 里还有：模型列表、题目列表（含模型收到的提示词）、各轮的原始目录、取数规则。

## 四、取数规则（重要）

每道题、每个模型各取一份，规则是**这一格最后一次出分的 fixed_v4 结果**。

补跑目录按时间顺序覆盖主轮，但只在补跑出了分时才覆盖。177 份里有 64 份来自补跑，原因是超时、额度不够或网关报错，补跑时用的是新副本。被替换掉的旧 run 不在交付范围内，请不要直接从原始目录取数，否则会拿到旧结果。

本清单的分数已和 6case/10case/web10-process.md 的结果矩阵逐格核对，全部一致。

## 五、各模型均分（CC，满分 53）

| 模型 | 3case | 6case | 10case | web10 | 全部 |
|---|---|---|---|---|---|
| Opus 5.5（三方A） | 47.0 | 46.3 | 49.7 | 49.5 | 48.7（n=29） |
| gpt-6-astra | 41.3 | 42.2 | 46.9 | 45.6 | 44.9（n=29） |
| GLM-5.3 Flash | 38.0 | 39.5 | 44.5 | 45.2 | 43.0（n=29） |
| Fable 5.1 | 39.0 | 38.7 | 44.3 | 43.0 | 42.1（n=29） |
| Kimi K3 | 37.0 | 38.5 | 41.3 | 42.7 | 40.8（n=29） |
| Qwen3.8-27B Figma Edit · ckpt-270 | 36.0 | — | — | — | 36.0（n=3） |
| Gemini 3.5 Flash | 25.0 | 38.8 | 33.1 | 24.5 | 30.5（n=29） |

## 六、注意事项

1. **截图是判官实际看过的画板**，已经去掉模型自建的组件板（如 "Components"、"DS · components"）。因此截图张数可能少于 03 页的顶层节点数，这是正常的；完整节点列表见 `workspace_top_level`。个别结果的屏数本来就少，例如 GPT × Chat Bot AI 只有 4 个屏幕画板，其余 27 个都是组件。
2. **0 分的格子共 4 个**，全部没有通过 G0，设计基本空白或严重裁切：3case Gemini × Balance；10case Gemini × Budget；web10 Gemini × Foodieland、Gemini × ABM Developer Portfolio。是否让这 4 格参加人评，由 Arena 一方决定。
3. **匿名性**：
   - 副本是源文件逐字节复制的，文件名和原模板一样，不含模型名。
   - 但 6case/10case/web10 中**每个模型固定使用一个企业账号**（见 `account` 字段），所以副本的所有者会暴露模型身份。3case 全部用 fulinbo 一个账号，没有这个问题。
   - 如果要给评审 Figma 链接，需要先转移副本或另外复制一份，建议只展示截图。
   - 画布里有没有模型自己写进去的身份信息，没有逐张检查。
4. **需求是英文原文**，从原模板只读提取，没有截断。评测记录里的需求快照截断在 6500 字，大多数题都超过这个长度，不要用那份快照。中文译文需要 Arena 一方自己翻译，例如用 `scripts/translate-arena-requirements.mjs`。
5. 截图是 Figma 导出的原始 PNG，没有重新编码，可以用哈希校验。
6. 只做了 CC 评分，没有任何人评数据。

## 七、重新生成

```bash
python3 tools/build_manifest.py <输出目录>        # 只读各 run 目录，重新生成清单、截图和哈希
python3 tools/render_requirements.py              # 从 requirements/raw 重新生成需求 md
# 重新提取需求（只读调用 Figma，需要账号 MCP 配置）：
#   PYTHONPATH=<standalone>/vendor:server <venv python> tools/extract_briefs.py <figma-mcp.json> requirements/raw
```

## 八、2026-11-04/05 补跑更新

| 格子 | 处理 | 结果 |
|---|---|---|
| 3case Balance × Gemini 3.5 Flash | 原结果因账号 Figma 额度耗尽被截断，用新副本（zuohaosheng）重跑 | 仍为 0 分：模型做完 2 屏后没有再调用工具，直接结束（模型自身问题，结果有效） |
| 6case Chat Bot AI × GPT-6 Astra | 原结果因额度耗尽只交付 4 屏，用新副本（gaoyongyong）重跑 | 12 屏全部交付，**43 分**（原 46 分作废） |

**GPT 这格是单独打分的。** 交付完成后，runner 下载自查截图时网络断开并崩溃，轨迹里留下未返回的工具调用，平台的轨迹核验因此不放行。经用户批准，用平台同一套判官代码（Opus 5.5、fixed_v4 提示词、图片预处理、解析与计分）对这份产物单独打分，只跳过了轨迹核验这一步。清单里 `score_source` 字段标为「offline-judge（推理轨迹未核验，用户批准）」，打分输入和原始输出保存在 `bench-runs/6case-rerun3-gpt/offline-judge/`。其余 176 格都是平台正常打分（`score_source=platform`）。
