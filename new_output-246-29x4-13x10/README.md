# 29×4 与 13×10 推理与评测结果

来源批次：`storage/benchmarks/distributed-246-20261109`
整理时间：2026-11-11T11:24:27

| cohort | 含义 | 条数 | 已有完成打分 |
|---|---|---:|---:|
| origin29 | 29 题 × 4 模型 | 116 | 92 |
| new13 | 13 题 × 10 模型 | 130 | 120 |

## 先看这些

- `summary.csv`：每条的模型、推理状态、时长、token、打分总分、G0。这是汇总表。
- `origin29/<task-id>/`、`new13/<task-id>/`：单条结果。
  - `trajectory.jsonl`：该次推理轨迹
  - `trajectory-attempt-*.jsonl`：同题后续重跑的轨迹
  - `inference-metrics.json`：这次推理的 token 和时长
  - `score.json`：评测打分（总分、G0、分项）。裁判原文在 `judge-raw.txt`
  - `screen-count-check.json`：屏数规则检查
  - `meta.json`：题目、模型和文件链接

`task-metrics.csv` 是原批次的推理汇总，`scoring-results.csv` 是原批次的打分汇总。

## 没有放进来的内容

- `private/`、`figma-mcp.json`：账号和密钥
- 评测截图（约 1.1GB PNG）和 `trace.sqlite3-wal`：不是分数、token、时长本身，仍在原批次目录
- 没能收进包的条目见 `missing.txt`。其中多数是打分还没有 `result.json`；个别 `result.json` 和任务状态文件仍是 600

推理状态计数：{('new13', 'success'): 124, ('new13', 'failed'): 5, ('new13', 'deferred'): 1, ('origin29', 'failed'): 54, ('origin29', 'pending'): 2, ('origin29', 'success'): 52, ('origin29', 'preparing_copy'): 2, ('origin29', 'running'): 6}
复制计数：{'trajectory': 323, 'metrics': 224, 'screen': 221, 'score': 212, 'missing_trajectory': 9, 'missing_score': 34}
