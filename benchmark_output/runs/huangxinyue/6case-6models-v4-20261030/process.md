# 6case-6models-v4-20261030 进度

最后更新：2026-11-03 17:39:56（每 5 分钟自动刷新）

**已评分 29/36** · 推理中 0 · 有产物 34 · 无交付 0 · 评分失败 2 · 阶段 `running_or_waiting_resources`

## 结果矩阵

| 模型 | 可用 | StockWave | Nectar | Stylish | Chat Bot AI | FinX | Fruit Hub | 均分 |
|---|---|---|---|---|---|---|---|---|
| Opus 5.5（三方A） | ✅ | ✅ 45/53 | ✅ 47/53 | ✅ 42/53 | ✅ 51/53 | ✅ 44/53 | ✅ 49/53 | 46.3（n=6） |
| Fable 5.1 | ✅ | ✅ 44/53 | ✅ 38/53 | ✅ 32/53 | ✅ 38/53 | ✅ 35/53 | ✅ 42/53 | 38.2（n=6） |
| GLM-5.3 Flash | ✅ | ✅ 40/53 | ✅ 44/53 | ✅ 35/53 | ✅ 44/53 | ✅ 33/53 | 🔍 待评分 | 39.2（n=5） |
| Gemini 3.5 Flash | ✅ | ✅ 40/53 | ✅ 40/53 | 🔍 待评分 | ✅ 42/53 | ✅ 40/53 | ✅ 44/53 | 41.2（n=5） |
| Kimi K3 | ✅ | ✅ 39/53 | ⚠️ 评分失败 | ✅ 31/53 | ⚠️ 评分失败 | ✅ 36/53 | 结果不完整 | 35.3（n=3） |
| gpt-6-astra | ✅ | ✅ 42/53 | 结果不完整 | ✅ 36/53 | ✅ 46/53 | ✅ 37/53 | 结果不完整 | 40.2（n=4） |

## 当前问题

- Opus 5.5（三方A） × Nectar：Figma 产物尚未核验，不能将参考页截图视为有效交付
- Fable 5.1 × Stylish：Figma MCP 额度持续受限，已停止无效推理；已有设计与轨迹已保留，属于资源阻塞
- GLM-5.3 Flash × StockWave：质检未通过：ShareGPT conversion failed: invalid role 'function_call' at conversation index 104
- GLM-5.3 Flash × Stylish：质检未通过：missing or invalid PNG: TEST-025_1793391367744/task-000001/media/ff77ccea1ca6f179494582706c093f1e1e83b2fcefc61dc7a95560f18c69708c.jpg; ShareGPT conversion failed: invalid role 'function_call' at
- GLM-5.3 Flash × Chat Bot AI：质检未通过：ShareGPT conversion failed: invalid role 'function_call' at conversation index 216
- Gemini 3.5 Flash × Nectar：Figma 产物尚未核验，不能将参考页截图视为有效交付
- Gemini 3.5 Flash × Stylish：Figma 产物尚未核验，不能将参考页截图视为有效交付；质检未通过：no screenshot <image> tag
- Kimi K3 × StockWave：Figma 产物尚未核验，不能将参考页截图视为有效交付
- Kimi K3 × Nectar：运行超时被中断；已有设计与实际轨迹保留，等待按重跑策略处理
- Kimi K3 × Chat Bot AI：Figma MCP 额度持续受限，已停止无效推理；已有设计与轨迹已保留，属于资源阻塞
- Kimi K3 × Fruit Hub：Figma MCP 额度持续受限，已停止无效推理；已有设计与轨迹已保留，属于资源阻塞
- gpt-6-astra × Nectar：Figma MCP 额度耗尽，Workspace 未交付产品画板；这是资源阻塞，不能计作模型能力失败；质检未通过：no screenshot <image> tag
- gpt-6-astra × Chat Bot AI：质检未通过：no screenshot <image> tag
- gpt-6-astra × FinX：Figma 产物尚未核验，不能将参考页截图视为有效交付；质检未通过：no screenshot <image> tag
- gpt-6-astra × Fruit Hub：Figma MCP 额度耗尽，Workspace 未交付产品画板；这是资源阻塞，不能计作模型能力失败；质检未通过：Figma use_figma was not called; no screenshot <image> tag
- 取证 run_22738d74fd994327：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_0887c97e15f54b45：这条正在「补图中」，等它结束再补图
- 取证 run_9af1095a3c1b4d1a：这条正在「补图中」，等它结束再补图
- 取证 run_3cd3a95545ef4da3：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_388f216a027d4234：这条正在「补图中」，等它结束再补图
- 取证 run_86fe6fbebb504b04：You've reached the Figma MCP tool call limit for your Full seat on the Enterprise plan. Upgrade your seat or plan for more tool calls. Use the whoami tool for m
- 取证 run_a618e4f4329241ea：这条正在「补图中」，等它结束再补图
- 取证 run_c9780c2cfa9f43c3：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_d01ea21a16fb4203：这条正在「补图中」，等它结束再补图
- 取证 run_4f9446f398ba4022：这条正在「补图中」，等它结束再补图
- 取证 run_5d0ba1fcfc644339：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_ad7c2694e2804c40：You've reached the Figma MCP tool call limit for your Full seat on the Enterprise plan. Upgrade your seat or plan for more tool calls. Use the whoami tool for m
- 取证 run_e384d89f39b64a6f：这条正在「补图中」，等它结束再补图
- 取证 run_754970d9eda9486d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_260581d84aed4544：用户已关闭后续截图；已有图片保留
- 取证 run_f024d96282944413：这条正在「补图中」，等它结束再补图
- 取证 run_f5c4306035b340fb：You've reached the Figma MCP tool call limit for your Full seat on the Enterprise plan. Upgrade your seat or plan for more tool calls. Use the whoami tool for m
- 取证 run_7cd221e5b4ee430a：fetch failed
- 取证 run_d85c99bd1a2b4165：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_d6c5a13a534a45a8：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_2f4364ab7f6e421b：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_c2fcac9282d84095：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_5aba68eb765b4e3e：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_37c32ad383e64ac8：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_3f2f41ee87aa4e86：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_d77bf96e022e4c6d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_6427a5ceaf7549a3：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_ef454c8a5cb84920：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_d0733a840a304113：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_417f43d09f254835：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_3091effa604a4aa8：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_5be17ac36753417d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_ef8ee50e6036462d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_946137f892ab48c3：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_07df7eb404fe4925：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_28230593d2144b83：The operation was aborted due to timeout
- 取证 run_ae0a6b6a96c649a5：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_13e76c30ed0b4445：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_b3a9011569f3435a：You've reached the Figma MCP tool call limit for your Full seat on the Enterprise plan. Upgrade your seat or plan for more tool calls. Use the whoami tool for m
- 取证 run_dd24b89a9f904183：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_34a4fdc1f1774a18：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_7ffe4f9d7a00494d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_20ad1e40ba94404a：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_add610f7648b4eed：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_d856c26913474fff：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_49141601915448fb：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_42f933296c7b47e6：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_1afcb1b4f9a340c5：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_888705f71082479e：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_8c9959c4fe41439d：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_752dfb3aa2dc4799：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_350b9d6287cb42ee：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_96e99c5644774dd1：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_3c1cc7d97b2c483e：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_3da81191030e4303：You've reached the Figma MCP tool call limit for your Full seat on the Enterprise plan. Upgrade your seat or plan for more tool calls. Use the whoami tool for m
- 取证 run_1b66f6f80dcf4016：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_a8d9cdd35d604ac2：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_5a4253da24684adc：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_5e3575455eb344f0：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复
- 取证 run_e716a3cb348240c5：Figma MCP 调用额度受限；模型尚未启动，等待资源恢复

## 副本链接（链接文字为副本所在账号）

| 模型 | StockWave | Nectar | Stylish | Chat Bot AI | FinX | Fruit Hub |
|---|---|---|---|---|---|---|
| Opus 5.5（三方A） | [huangxinyue](https://www.figma.com/design/6A76LajyrMFNXzfkp2i7QL/) | [hejiatong](https://www.figma.com/design/UlgozbXKKfkCkJL2xcXBBr/) | [huangxinyue](https://www.figma.com/design/hKV1sOFfScKnDJe17PlYzc/) | [gaoyongyong](https://www.figma.com/design/qYmJPYhan4qnoskPJ57RhI/) | [zuohaosheng](https://www.figma.com/design/u3CeLQQamlk8bCGoFIwrxM/) | [hejiatong](https://www.figma.com/design/G2HC4jdOIMGram1qNF53gG/) |
| Fable 5.1 | [zuohaosheng](https://www.figma.com/design/qeLSUsUZzxgdj23JDXIOJ0/) | [zuohaosheng](https://www.figma.com/design/1oPizmZzd4fjneLUff0gxt/) | [huangxinyue](https://www.figma.com/design/Clh3ZJg2e2JHumrov2kQBL/) | [zhengyaozhi](https://www.figma.com/design/9heKhkdl3nBs0098pOlkYl/) | [zhengyaozhi](https://www.figma.com/design/ns1vu1jAfNex4AphVlb18K/) | [gaoyongyong](https://www.figma.com/design/5I7PlvtoC7GX1zbReFo1tr/) |
| GLM-5.3 Flash | [hejiatong](https://www.figma.com/design/Itxddx2V02O0earQP7dsPY/) | [huangxinyue](https://www.figma.com/design/aBJm2MvkIZqCV7cu0O7PHX/) | [zhengyaozhi](https://www.figma.com/design/tB1sUry3dJDspx8uxl0ftc/) | [zhengyaozhi](https://www.figma.com/design/S5iN4noHDacG8jTW5ILkwU/) | [zuohaosheng](https://www.figma.com/design/MoQG8UU1zIAlfnI9lRfjNZ/) | [hejiatong](https://www.figma.com/design/F7EFiqH5QRNemXAQ84a7wc/) |
| Gemini 3.5 Flash | [gaoyongyong](https://www.figma.com/design/yxXcYheOJMwoQleZezxzb8/) | [huangxinyue](https://www.figma.com/design/ogFM9dNm7sETUXE1zc1yEL/) | [hejiatong](https://www.figma.com/design/4c4DogTUfpgQKiS0h6RJMg/) | [gaoyongyong](https://www.figma.com/design/cXJnd8eSox3K8D7zd1ZogL/) | [gaoyongyong](https://www.figma.com/design/Cj3Mqd74nwX2NBBm3kp05M/) | [gaoyongyong](https://www.figma.com/design/jiYwYdVVeh1sSSwCPVx5uG/) |
| Kimi K3 | [zhengyaozhi](https://www.figma.com/design/rF6FqZfcky33oJ2DdQwg0a/) | [zuohaosheng](https://www.figma.com/design/HmTYf0TxPAghlGoRNAJEsf/) | [zhengyaozhi](https://www.figma.com/design/gy7Y1r5tsWp5YRcrXvqUCN/) | [hejiatong](https://www.figma.com/design/Y2NPUoCZuaavUnHvRAjZRI/) | [zuohaosheng](https://www.figma.com/design/taESNi0IFEkMvTSOVrS6K7/) | [hejiatong](https://www.figma.com/design/FgsayAFUkqNiDSaemuire1/) |
| gpt-6-astra | [gaoyongyong](https://www.figma.com/design/L6fZ2WNwG9l8CoVK9cyoN3/) | [huangxinyue](https://www.figma.com/design/xLaz5ZvyS07aaPSymGqIzr/) | [zuohaosheng](https://www.figma.com/design/R6y8tUnBHVmIRsWpGbvTh1/) | [zhengyaozhi](https://www.figma.com/design/xTJFR3UiUaVrxMlnYbpLsk/) | [hejiatong](https://www.figma.com/design/dgUZThlh51rLkaGJhbaDjz/) | [huangxinyue](https://www.figma.com/design/r5hAFzw7YSv8210CtQkeOz/) |

## 事件日志（最新在前）

- 2026-11-03 16:18:21 gpt-6-astra 资源可用
- 2026-11-03 16:12:54 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-03 15:34:18 gpt-6-astra 资源可用
- 2026-11-03 15:27:50 gpt-6-astra 资源不可用：openai_error
- 2026-11-03 14:06:01 Gemini 3.5 Flash 资源可用
- 2026-11-03 14:00:39 Gemini 3.5 Flash 资源不可用：The operation was aborted due to timeout
- 2026-11-03 13:12:13 Gemini 3.5 Flash 资源可用
- 2026-11-03 13:06:48 Opus 5.5（三方A） 资源可用
- 2026-11-03 13:06:48 Gemini 3.5 Flash 资源不可用：The operation was aborted due to timeout
- 2026-11-03 13:01:26 Opus 5.5（三方A） 资源不可用：operation error Bedrock Runtime: InvokeModel, https response error StatusCode: 4
- 2026-11-03 12:23:51 gpt-6-astra 资源可用
- 2026-11-03 12:18:29 gpt-6-astra 资源不可用：The operation was aborted due to timeout
- 2026-11-03 11:56:56 gpt-6-astra 资源可用
- 2026-11-03 11:51:33 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-03 06:44:22 gpt-6-astra 资源可用
- 2026-11-03 06:38:59 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-03 01:15:59 gpt-6-astra 资源可用
- 2026-11-03 01:10:34 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-03 00:38:15 gpt-6-astra 资源可用
- 2026-11-03 00:32:51 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 23:28:08 gpt-6-astra 资源可用
- 2026-11-02 23:22:45 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 22:49:54 Opus 5.5（三方A） 资源可用
- 2026-11-02 22:22:57 Opus 5.5（三方A） 资源不可用：The operation was aborted due to timeout
- 2026-11-02 22:06:48 gpt-6-astra 资源可用
- 2026-11-02 22:01:26 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 21:56:05 Kimi K3 资源可用
- 2026-11-02 21:50:46 Kimi K3 资源不可用：The model service is currently busy or has reached its serving capacity limit. P
- 2026-11-02 21:50:46 gpt-6-astra 资源可用
- 2026-11-02 21:45:26 gpt-6-astra 资源不可用：The operation was aborted due to timeout
- 2026-11-02 21:13:16 gpt-6-astra 资源可用
- 2026-11-02 21:02:30 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 20:19:23 gpt-6-astra 资源可用
- 2026-11-02 20:14:01 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 20:08:37 gpt-6-astra 资源可用
- 2026-11-02 20:03:14 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 17:16:24 gpt-6-astra 资源可用
- 2026-11-02 17:00:14 gpt-6-astra 资源不可用：system memory overloaded (current: 91.7%, threshold: 90%)
- 2026-11-02 16:33:18 Opus 5.5（三方A） 资源可用
- 2026-11-02 16:27:55 Opus 5.5（三方A） 资源不可用：No available channel for model claude-opus-5-5 under group aws带5.1 可蒸馏 (distribu
- 2026-11-02 16:17:10 Opus 5.5（三方A） 资源可用
- 2026-11-02 16:11:47 Opus 5.5（三方A） 资源不可用：The operation was aborted due to timeout
- 2026-11-02 15:44:56 gpt-6-astra 资源可用
- 2026-11-02 15:39:35 gpt-6-astra 资源不可用：system memory overloaded (current: 91.7%, threshold: 90%)
- 2026-11-02 13:23:52 Opus 5.5（三方A） 资源可用
- 2026-11-02 13:18:28 Opus 5.5（三方A） 资源不可用：Insufficient user quota, remaining quota: ¥-6.732696 (request id: 20261102051746
- 2026-11-02 10:42:43 gpt-6-astra 资源可用
- 2026-11-02 10:37:22 gpt-6-astra 资源不可用：credit_precharge_registration_unconfirmed
- 2026-11-02 03:07:02 GLM-5.3 Flash × Fruit Hub：📸 截图取证 → 🔍 待评分
- 2026-11-02 03:01:40 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-02 03:01:40 GLM-5.3 Flash × Fruit Hub：🔍 待评分 → 📸 截图取证
- 2026-11-02 02:56:19 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-02 02:50:57 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-02 02:45:35 Kimi K3 × Fruit Hub：📸 截图取证 → 结果不完整
- 2026-11-02 02:45:35 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-02 02:40:13 Kimi K3 × Fruit Hub：结果不完整 → 📸 截图取证
- 2026-11-02 02:29:30 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-02 02:18:45 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-02 02:13:24 Kimi K3 × Fruit Hub：📸 截图取证 → 结果不完整
- 2026-11-02 02:13:24 Fable 5.1 × FinX：⚠️ 评分失败 → ✅ 35/53
- 2026-11-02 02:02:37 Kimi K3 × Fruit Hub：结果不完整 → 📸 截图取证
- 2026-11-02 01:57:15 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-02 01:51:53 GLM-5.3 Flash × Fruit Hub：📸 截图取证 → 🔍 待评分
- 2026-11-02 01:46:31 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-02 01:46:31 GLM-5.3 Flash × Fruit Hub：🔍 待评分 → 📸 截图取证
- 2026-11-02 01:30:26 GLM-5.3 Flash × Fruit Hub：📸 截图取证 → 🔍 待评分
- 2026-11-02 01:14:21 GLM-5.3 Flash × Fruit Hub：🔍 待评分 → 📸 截图取证
- 2026-11-02 00:52:54 GLM-5.3 Flash × Fruit Hub：📸 截图取证 → 🔍 待评分
- 2026-11-02 00:42:10 GLM-5.3 Flash × Fruit Hub：🔍 待评分 → 📸 截图取证
- 2026-11-02 00:26:03 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-02 00:20:39 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-02 00:04:33 Kimi K3 × Fruit Hub：📸 截图取证 → 结果不完整
- 2026-11-02 00:04:33 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-01 23:59:10 Kimi K3 × Fruit Hub：结果不完整 → 📸 截图取证
- 2026-11-01 23:59:10 Gemini 3.5 Flash × Stylish：🔍 待评分 → 📸 截图取证
- 2026-11-01 23:53:48 Kimi K3 × Fruit Hub：📸 截图取证 → 结果不完整
- 2026-11-01 23:48:26 GLM-5.3 Flash × Fruit Hub：📸 截图取证 → 🔍 待评分
- 2026-11-01 23:43:06 Kimi K3 × Fruit Hub：结果不完整 → 📸 截图取证
- 2026-11-01 23:37:43 Gemini 3.5 Flash × Stylish：📸 截图取证 → 🔍 待评分
- 2026-11-01 23:37:43 GLM-5.3 Flash × Fruit Hub：🔍 待评分 → 📸 截图取证

## 准备阶段记录
- 10-31 02:39 导入 6 题（StockWave/Nectar/Stylish/Chat Bot AI/FinX/Fruit Hub，query 与上轮同一模板），计划 6×6=36（不含 Qwen），fixed-v4，判官 Opus 5.5
- 10-31 02:39 绑定用户预先分发的 36 个副本（distribution-record.md）；每个副本用其所在账号运行（copy-accounts.json）
- 10-31 02:43 运行策略 r1：账号池 hejiatong/huangxinyue/zuohaosheng/gaoyongyong/zhengyaozhi，每账号同时 1 个任务，总并发 5
- 10-31 02:44 后端 :18197 启动，监督器开始推理与评分；自动重试（会新建副本）已关闭，失败任务另行处理

