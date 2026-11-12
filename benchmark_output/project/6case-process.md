# 6 题 × 6 模型 汇总进度（含补跑）

最后更新：2026-11-02 02:57:19（每 5 分钟自动刷新）

**已出分 35/36**

标 🔁 的格子来自补跑轮次（用户 10-31 提供的新副本），已替换原轮次结果。

## 结果矩阵

| 模型 | StockWave | Nectar | Stylish | Chat Bot AI | FinX | Fruit Hub | 均分 |
|---|---|---|---|---|---|---|---|
| Opus 5.5（三方A） | ✅ 45/53 | ✅ 47/53 | ✅ 42/53 | ✅ 51/53 | ✅ 44/53 | ✅ 49/53 | 46.3（n=6） |
| Fable 5.1 | ✅ 44/53 | ✅ 38/53 | 🔁 ✅ 35/53 | ✅ 38/53 | ✅ 35/53 | ✅ 42/53 | 38.7（n=6） |
| GLM-5.3 Flash | ✅ 40/53 | ✅ 44/53 | ✅ 35/53 | ✅ 44/53 | ✅ 33/53 | 🔁 ✅ 41/53 | 39.5（n=6） |
| Gemini 3.5 Flash | ✅ 40/53 | 🔁 ✅ 38/53 | 🔁 🔍 待核验/评分 | ✅ 42/53 | ✅ 40/53 | ✅ 44/53 | 40.8（n=5） |
| Kimi K3 | ✅ 39/53 | 🔁 ✅ 41/53 | ✅ 31/53 | 🔁 ✅ 40/53 | ✅ 36/53 | 🔁 ✅ 44/53 | 38.5（n=6） |
| gpt-6-astra | ✅ 42/53 | 🔁 ✅ 46/53 | ✅ 36/53 | ✅ 46/53 | 🔁 ✅ 39/53 | 🔁 ✅ 44/53 | 42.2（n=6） |

## 补跑明细

| 模型 | 题目 | 账号 | 状态 | 推理时长 | 新副本 | 备注 |
|---|---|---|---|---|---|---|
| Fable 5.1 | Stylish | zuohaosheng | ✅ 35/53 | 35m | [打开](https://www.figma.com/design/t59Fpla3t3vTCJcBn4Rv7i/) |  |
| GLM-5.3 Flash | Fruit Hub | gaoyongyong | ✅ 41/53 | 60m | [打开](https://www.figma.com/design/l8MdQcWVFQcJw2Ix8PJk7h/) |  |
| Gemini 3.5 Flash | Nectar | zhengyaozhi | ✅ 38/53 | 16m | [打开](https://www.figma.com/design/uCZr4bpGdqwWmB3Jcmxt24/) |  |
| Gemini 3.5 Flash | Stylish | zuohaosheng | 🔍 待核验/评分 | 8m | [打开](https://www.figma.com/design/DLeCRz9ALmIJNyhZEjhOxT/) | Workspace 中没有交付产品画板，参考页截图不能作为设计产物；质检未通过：no screenshot <image> tag; ShareGPT conv |
| Kimi K3 | Nectar | zuohaosheng | ✅ 41/53 | 25m | [打开](https://www.figma.com/design/rOzSn1MkRakcwc5zqsVINX/) |  |
| Kimi K3 | Chat Bot AI | gaoyongyong | ✅ 40/53 | 36m | [打开](https://www.figma.com/design/lEwCWXljcAXgGd3yvwjAbG/) |  |
| Kimi K3 | Fruit Hub | zhengyaozhi | ✅ 44/53 | 32m | [打开](https://www.figma.com/design/efLfjtKOwnSEf9m0Xm0qel/) |  |
| gpt-6-astra | Nectar | zuohaosheng | ✅ 46/53 | 8m | [打开](https://www.figma.com/design/wl2R1YWEzuvrC0BJrjsr66/) |  |
| gpt-6-astra | FinX | gaoyongyong | ✅ 39/53 | 9m | [打开](https://www.figma.com/design/c1Da0Tk2eyI9zPyG1mTUd3/) |  |
| gpt-6-astra | Fruit Hub | zhengyaozhi | ✅ 44/53 | 5m | [打开](https://www.figma.com/design/h9e0xRb0UdbR1OFxc0vVuO/) |  |

## 未出分且有报错

- Gemini 3.5 Flash × Stylish（补跑）：Workspace 中没有交付产品画板，参考页截图不能作为设计产物；质检未通过：no screenshot <image> tag; ShareGPT conversion failed: summary reasoning was selected but is missing

## 说明

- 11-02 修复 Fable × FinX：平台截图环节竞态导致画板 19:183 的原始响应文件被覆盖（截图本身正确），经用户同意只读重截 10 张、凭据核对通过后重新评分 → 35/53；旧截图备份在原轮次 trace-finalization/TEST-021-figma-frames.bak-20261101
- 原轮次目录：`/mnt/afs/huangxinyue/bench-runs/6case-6models-v4-20261030/`（自身明细见其 process.md）
- 补跑目录：`/mnt/afs/huangxinyue/bench-runs/6case-rerun1-{glm,fable,gemini,kimi,gpt}/`
- 第二批（Kimi、GPT）：已启动 Sat Oct 31 05:39:50 UTC 2026
- 原轮次的原副本自动重启已停用；自动新建副本的重试未开启，失败题列出后由用户提供新副本。
