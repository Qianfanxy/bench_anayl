# Figma 模型行为与失败分析

fixed_v4 的 **22 个计分项**是本分析的子维度，另有一个前置门槛 G0。新增 13 道设计任务 × 10 模型共 130 个组合，其中 **111 份通过 G0 且有完整分项，9 份未通过 G0，10 份未评分**。通过门槛的稿件中，业务数据和状态前后不一致、卡片和功能块压叠、控件难以识别是最常见的扣分表现。未通过门槛的稿件则集中在画板有名无内容、正文被裁切或覆盖两种情形。

历史 29 题分两组参照。历史六模型有 170 份按 Arena 的评分记录 ID 和运行 ID 对齐的完整分项。另四份 Arena 候选只有总分或门槛记录，其中一份 G0 未通过。新增四模型有 87 份通过 G0 并有完整分项，5 份 G0 未通过，24 份未评分。三组分别统计。主样本的十份未评分记录中，任务汇总记录八份为推理成功、一份超时、一份延后，均无可用 CC 分项。

## 常见错误与具体表现

频次指**新增 13 题主样本中该题项低于满分的份数**，同一处缺陷可以触发多个题项。示例说明缺陷长什么样，细分症状的发生率需要逐条编码。下面的归纳还查看了 B3、D2、A2 各题评分最低的记录，每题每项取一份，同分时按模型名排序。其中 B3 和 D2 各 13 段，A2 有 12 段扣分证据，另 1 题在该项全部满分。

| 错误类型 | 相关题项 | 具体表现与证据 |
| --- | --- | --- |

| 同一业务对象在各屏状态或数据不一致 | B3 107/111 | Run & Earn 的 Daily Goal 为 14,000/15,000，Today 卡为 2345/5000。Open Fashion 的支付卡尾号从 3698 变为 89。这类现象可按对象、字段和两处画板定位。 [Figma](https://www.figma.com/design/gZrydKAhA7a2IUOX552Wy3) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-0f7b3255257af51c/score.json)；[Figma](https://www.figma.com/design/fvuNQ4hT937gJWq8Mijfiq) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-7150eb775fc64dcb/score.json) |
| 功能组件内部压叠、溢出或裁切 | D2 101/111 | Self Care Clinic 第 9、11 屏的消息、电话、更多按钮覆盖医生姓名、科室和价格，D2 为 0/3。Hawkeye Travel 第 11 屏星期和日期挤成连串，无法匹配到单元格，D2 为 0/3。逐题抽取的 13 段 D2 扣分证据均出现压叠、溢出或裁切。 [Figma](https://www.figma.com/design/49CmNYFsE2CrrfkxZxjR03) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-884a93727488e7a3/score.json)；[Figma](https://www.figma.com/design/KdeF9tUrv65LdsHRFQvPLG/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-17dd105c2d3a7016/score.json) |
| 控件文字、图标或字段提示互相干扰 | D1 96/111 · A4 93/111 | Audio Shop 的登录与搜索框图标下残留 Emai/Ema，筛选价格框占位文字重影。同一处缺陷影响控件内部布局与输入含义，分别对应 D1 和 A4。 [Figma](https://www.figma.com/design/yTT8DaeGfOqu9ki8vxXI6F/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b93330d65e01ea0/score.json) |
| 当前位置或流程反馈错位 | A2 86/111 | Cyber Phone Store 的购物车与结账页仍高亮 Home，结账步骤条也看不出前两步已完成。MindfulMentor 的进度和选中态只保留了需求说明式文字。 [Figma](https://www.figma.com/design/xSNrLv7LZ8JOOmaKEixsV4) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-21ea860ece69cbc4/score.json)；[Figma](https://www.figma.com/design/njtnNYC5TSWoQW1u8sC3td) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-680bbdea80074441/score.json) |
| 同类控件有多套规则 | E1 82/111 | Run & Earn 前几屏返回键用长箭头，后几屏改用尖括号。Self Care Clinic 的高分对照中，医生卡结构、评分徽章、主按钮和单选卡选中态在相关屏中保持一致。 [Figma](https://www.figma.com/design/gZrydKAhA7a2IUOX552Wy3) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-0f7b3255257af51c/score.json)；[Figma](https://www.figma.com/design/2ZgNzvHwkDLibFPyYene1j) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-51b0ef2ee9b3214f/score.json) |
| 视觉功能区与 Figma 图层结构脱节 | G2 72/111 | Audio Shop 的 05_Explore_Products 和 07_Product_Overview 各有 57、56 个节点，最大嵌套深度均为 1。评审可辨认商品区和评价区，但两区在文件里缺少相应的父级容器。 [Figma](https://www.figma.com/design/yTT8DaeGfOqu9ki8vxXI6F/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b93330d65e01ea0/score.json) |


B3、D2 在三组都反复出现。历史六模型分别为 **146/170、135/170**，原题新增四模型分别为 **72/87、80/87**。按各项满分归一化后，四个布局题项合计失分率分别为 **28.0%、34.9%、41.4%**，在三组中均为失分率最高的大维度。F5 的整体精致度也常被扣分，新 13 题为 **92/111**。解释 F5 时优先追溯已标记的压叠、素材适配和留白问题，避免重复计算同一缺陷。

## G0 未通过的九份产物

画板数量、工具返回成功和最终交付可用性应分别核查。按评分证据的主要表现归类，六份是空壳或需求说明占位，三份是画板或区块裁切、覆盖。下表均链接到实际评分版本。

| 类型 | 任务与模型 | 可观察表现 | 证据 |
| --- | --- | --- | --- |
| 裁切或覆盖 | Cyber Phone Store · Gemini 3.5 Flash | 七屏画板高度均为100，只露出页头，主体内容全部被裁切，主流程不可见 | [Figma](https://www.figma.com/design/i2qgkcpB1GZyKvwEgC7qyv) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-0d7f6f7db6d4ffe3/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-0d7f6f7db6d4ffe3-9a43a00f02481dac7c79__benchmark-layers.json) |
| 裁切或覆盖 | Inkline Blog · Fable 5.1 | 八屏普遍存在区块高度裁切，列表、卡片、表单与正文被截断，主流程内容无法辨认 | [Figma](https://www.figma.com/design/BU6VKoU1alwDejmQNwwzIl) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-1d2284c5ec540ce2/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-1d2284c5ec540ce2-5d1966ffabc0a987b03b__benchmark-layers.json) |
| 裁切或覆盖 | Inkline Blog · Gemini 3.5 Flash | 8屏页脚均覆盖页面顶部，导航与首屏内容缺失，下方大面积空白 | [Figma](https://www.figma.com/design/QnacWGledXqMZAvsTuyFHC) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-44d06c1c5e7f0411/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-44d06c1c5e7f0411-2389c981b41a2e2af54b__benchmark-layers.json) |
| 空壳或占位 | Musium · GPT 6.1 Sol | 17屏均只有标题和需求说明文字，没有绘制任何界面，不能作为设计基础 | [Figma](https://www.figma.com/design/8CRhp2bveQaKmKc2SXhgEa) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-45a2f0198971854b/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-45a2f0198971854b-6a337163e919b60e6523__benchmark-layers.json) |
| 空壳或占位 | Hawkeye Travel · GPT 6.1 Sol | 18屏均只有需求说明文字和零散文本标签，无任何界面元素，不可作为继续工作的基础 | [Figma](https://www.figma.com/design/DCkAtToTyss96cKUAiMRDN) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-df29688af3c8264b/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-df29688af3c8264b-78564c61fc05fbf98475__benchmark-layers.json) |
| 空壳或占位 | MindfulMentor · Gemini 3.5 Flash | 12屏均只有状态栏与底部指示条，主体全空白，主流程内容完全缺失 | [Figma](https://www.figma.com/design/xgW3kqDqVqrf28zi8R81eO/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-4976baef178385ac/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-4976baef178385ac-b7f209b68ba6332240d3__benchmark-layers.json) |
| 空壳或占位 | Placoo Rental · Gemini 3.5 Flash | 14屏中11屏仅为灰底文字说明加紫色热区块，主页、筛选、详情、预订等主流程均未设计 | [Figma](https://www.figma.com/design/SXEjfMGL7mvLHDkK8UBBmu) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-9a1a092485c5146d/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-9a1a092485c5146d-0301f32d34bd45c176c1__benchmark-layers.json) |
| 空壳或占位 | Magic Coffee · Gemini 3.5 Flash | 20屏中19屏几乎全空白，仅剩画板名文字，主流程页面实际缺失 | [Figma](https://www.figma.com/design/VUkMrBwbJvs0S2niANbVie/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-c2308d7b9c87a9ff/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-c2308d7b9c87a9ff-58982bb13dfae081dc28__benchmark-layers.json) |
| 空壳或占位 | Open Fashion · Gemini 3.5 Flash | 20屏中19屏仅有页头且主体空白，第7、8屏几乎全黑，主流程页面缺失 | [Figma](https://www.figma.com/design/sitVQOkAgY6fjDdKndJFsQ) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-e4c1fea42e52cd68/score.json) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-e4c1fea42e52cd68-ec95f71f2025a3a2bdd7__benchmark-layers.json) |

## 哪些行为与结果连得上

### Cyber Phone Store 画板高度写入后没有被修正

Gemini 3.5 Flash 得 **0/53**。评分对应的重跑轨迹先创建 7 张桌面画板，随后多个组装调用把画板设为 `1440×100`。这些调用返回组装成功，评分版本的图层快照却显示 **7/7 画板高度均为 100 px**。首页有 230 个节点，说明内容节点已存在，评分证据记录的是可见画板只露出页头。轨迹末尾完成了原型连线。这里能把 **几何尺寸写入 → 最终尺寸 → 主流程不可见** 连起来。[Figma](https://www.figma.com/design/i2qgkcpB1GZyKvwEgC7qyv) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-0d7f6f7db6d4ffe3/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-0d7f6f7db6d4ffe3/trajectory-attempt-1-restart-20261110-095732.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-0d7f6f7db6d4ffe3-9a43a00f02481dac7c79__benchmark-layers.json)

同题 Opus 5.5 得 **50/53**。首次连线检查的返回值报告四处购物车行找不到详情页点击目标，随后把链接移到名称图层并回查。末次调用逐屏核对所需文案、画板尺寸和链接，图层快照也保留了实际尺寸，例如首页高 4492 px。这组对照说明回读可以发现执行层成功状态之外的问题。[Figma](https://www.figma.com/design/s7TbYf4ItSFEuisVWRMmKk) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b9873c0371f396b/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b9873c0371f396b/trajectory.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-5b9873c0371f396b-e6eccf5220de083ca226__benchmark-layers.json)

### Musium 和 Hawkeye Travel 有画板目录，主体内容未完成

Musium 的 GPT 6.1 Sol 首次整批写入收到响应丢失提示，随后回读未找到画板，再创建 17 张骨架。给骨架补充媒体和导航的调用触发 `reactions` 参数校验失败。评分图层显示 **17 张画板每张都只有 4 个节点**，与状态栏、底部指示条和文字占位一致。这里同时有链路中断记录和脚本校验失败记录。[Figma](https://www.figma.com/design/8CRhp2bveQaKmKc2SXhgEa) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-45a2f0198971854b/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-45a2f0198971854b/trajectory.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-45a2f0198971854b-6a337163e919b60e6523__benchmark-layers.json)

Hawkeye Travel 的同一模型尝试对 Frame 写入不支持的 `description`，工具返回类型错误。后续调用返回了 18 张画板的目录，评分快照中每张只有 **2–5 个节点**，评审记录仅有需求说明和零散文字。两案可共同支持「骨架创建完成后，缺少主体交付验收」这一观察。[Figma](https://www.figma.com/design/DCkAtToTyss96cKUAiMRDN) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-df29688af3c8264b/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-df29688af3c8264b/trajectory.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-df29688af3c8264b-78564c61fc05fbf98475__benchmark-layers.json)

### Audio Shop 通过门槛后的差距来自局部修整

Fable 5.1 得 **40/53**，D1 和 D2 均为 **1/3**。输入框残字、购物车品名换行盖住价格等问题进入了评分产物。该评分版本轨迹完成页面构建和原型连线，未见针对这些缺陷的修正记录。[Figma](https://www.figma.com/design/yTT8DaeGfOqu9ki8vxXI6F/) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b93330d65e01ea0/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-5b93330d65e01ea0/trajectory-attempt-1-restart-20261110-095732.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-5b93330d65e01ea0-b08f18137d85f2e48195__benchmark-layers.json)

Opus 5.5 得 **50/53**，D1 和 D2 均为 **3/3**。轨迹显示它读取商品卡内部尺寸、调整照片高度和卡片变体，并把两张产品详情画板从 812 px 调整到 1593 px 和 950 px，随后核对最终画板。它的 B3 仍为 **2/3**，商品列表与详情页评论数不一致。几何修整和跨屏业务数据校验需要不同的检查。[Figma](https://www.figma.com/design/uZp3pPaHfsdGifE4ZPOcX7) · [评分证据](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-549e01e88b512257/score.json) · [评分版本轨迹](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/new13/task-549e01e88b512257/trajectory.jsonl) · [评分版本图层](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/layers-only/task-549e01e88b512257-3edc2eb1a65c31c3167e__benchmark-layers.json)

### 图层扁平是可核查的交付风险

在 111 份通过 G0 的新题稿件里，G2 为 0/2 的 23 份中，19 份至少一半画板最大嵌套深度只有 1 层。G2 为 1/2 的 49 份中有 14 份符合该条件，G2 满分的 39 份中为 0 份。这里用同一评分版本的快照核对题项表现。评审也参考了该摘要，因此这些数量用于核验判分的一致性。浅层结构本身需要结合页面功能区判断。

## 模型在新增 13 题中的失败分布

| 模型 | G0 通过 | G0 未过 | 未评分 | 通过 G0 后 D2 扣分 | 通过 G0 后 G2 扣分 |
| --- | ---: | ---: | ---: | ---: | ---: |

| DeepSeek V4 Flash | 7 | 0 | 6 | 7/7 | 7/7 |
| Fable 5.1 | 12 | 1 | 0 | 11/12 | 8/12 |
| GLM-5.3 Flash | 12 | 0 | 1 | 12/12 | 9/12 |
| GPT 6.1 Sol | 10 | 2 | 1 | 10/10 | 10/10 |
| Gemini 3.5 Flash | 7 | 6 | 0 | 7/7 | 5/7 |
| Kimi K3 | 13 | 0 | 0 | 13/13 | 11/13 |
| Opus 5.5（三方A） | 12 | 0 | 1 | 8/12 | 1/12 |
| Qwen 3.8 Max | 12 | 0 | 1 | 12/12 | 6/12 |
| Sonnet 5.5 | 13 | 0 | 0 | 10/13 | 3/13 |
| gpt-6-astra | 13 | 0 | 0 | 11/13 | 12/13 |


Gemini 的 6 次 G0 未通过集中在本批次，同时在 Run & Earn 得到 37/53。GPT 6.1 Sol 在 Musium 和 Hawkeye Travel 交付骨架，也在 Audio Shop 得到 43/53。把这些案例用作对同一模型何时完成、何时失效的对照。因果归因只落到已核验的调用、返回和产物，模型级差异保留题目和批次范围。

## 22 个子维度逐项结果

每个分数表示产物在该项低于满分的次数与分母。失分率为「实际失分总和 ÷ 可得总分」，以处理 2 分和 3 分题项。新题覆盖表示 13 道设计任务中至少一份通过 G0 的产物在该项扣分。

| 题项 | 维度 | 观察对象 | 新 13 题扣分 | 新 13 题归一化失分 | 新题覆盖 | 原题新四模型扣分 | 原题历史六模型扣分 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |

| A1 | 用户体验 | 页面用途与对象识别 | 36/111 | 16.2% | 10/13 | 12/87 | 21/170 |
| A2 | 用户体验 | 当前位置、步骤与状态 | 86/111 | 43.2% | 12/13 | 48/87 | 87/170 |
| A3 | 用户体验 | 核心内容与操作可发现性 | 55/111 | 32.9% | 13/13 | 35/87 | 41/170 |
| A4 | 用户体验 | 控件可识别与标签 | 93/111 | 48.6% | 13/13 | 58/87 | 92/170 |
| B1 | 信息组织 | 分组关系 | 60/111 | 20.1% | 12/13 | 36/87 | 58/170 |
| B2 | 信息组织 | 阅读与判断顺序 | 44/111 | 14.4% | 12/13 | 24/87 | 41/170 |
| B3 | 信息组织 | 信息与业务逻辑自洽 | 107/111 | 48.3% | 13/13 | 72/87 | 146/170 |
| B4 | 信息组织 | 图标语义 | 101/111 | 40.2% | 13/13 | 62/87 | 111/170 |
| B5 | 信息组织 | 主次与危险操作 | 60/111 | 20.7% | 13/13 | 41/87 | 58/170 |
| G1 | 可交付性 | 命名 | 35/111 | 15.8% | 12/13 | 34/87 | 75/170 |
| G2 | 可交付性 | 父子层级与功能区 | 72/111 | 42.8% | 13/13 | 56/87 | 55/170 |
| D1 | 布局质量 | 控件内部布局 | 96/111 | 43.2% | 13/13 | 62/87 | 106/170 |
| D2 | 布局质量 | 功能组件内部布局 | 101/111 | 49.2% | 13/13 | 80/87 | 135/170 |
| D3 | 布局质量 | 页面模块布局 | 99/111 | 39.0% | 13/13 | 72/87 | 114/170 |
| D4 | 布局质量 | 全页有效空间 | 91/111 | 33.9% | 13/13 | 56/87 | 99/170 |
| E1 | 一致性 | 同类控件一致性 | 82/111 | 36.9% | 13/13 | 56/87 | 93/170 |
| E2 | 一致性 | 跨页设计规则 | 44/111 | 19.8% | 11/13 | 21/87 | 30/170 |
| F1 | 视觉表达质量 | 文字层级与可读性 | 43/111 | 22.1% | 13/13 | 26/87 | 37/170 |
| F2 | 视觉表达质量 | 主辅色角色 | 15/111 | 6.8% | 9/13 | 8/87 | 6/170 |
| F3 | 视觉表达质量 | 状态语义色 | 16/111 | 7.2% | 9/13 | 7/87 | 17/170 |
| F4 | 视觉表达质量 | 中性色层级 | 19/111 | 9.0% | 9/13 | 12/87 | 25/170 |
| F5 | 视觉表达质量 | 整体协调与精致度 | 92/111 | 43.2% | 13/13 | 68/87 | 107/170 |


## 证据与统计口径

- 最新批次分项取每条 `score.json` 的 `values`、`evidence` 与 G0。图层以候选的 `revision` 匹配。同次轨迹按评分运行目录匹配主轨迹或重跑文件。[批次汇总](/Users/hxyh/Documents/figma_bench/new_output-246-29x4-13x10/summary.csv) · [图层快照清单](/Users/hxyh/Documents/figma_bench/distributed-246-layers-only/manifest.csv)
- 历史批次以 Arena 候选的 `cc_score_id` 联结各轮 `ui-eval.sqlite3` 的 `scale_scores`，逐条校验评分记录的 `run_id`、评测方法和 CC 总分。[Arena 快照](/Users/hxyh/Documents/figma_bench/benchmark_output/arena.sqlite3) · [22 个计分项和 G0 的冻结量表](/Users/hxyh/Documents/figma_bench/benchmark_output/project/benchmarks/rubrics/fixed-v4.json)
- 判官证据指向具体画板和控件。图层快照可核查画板尺寸、节点及深度。轨迹支持已观察到的操作及其返回。画布级细节的表述来自评分证据，未逐帧独立复评。频次为描述性计数，题项之间可能共用同一缺陷。
