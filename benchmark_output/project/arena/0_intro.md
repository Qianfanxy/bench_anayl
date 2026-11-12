



## 背景
Human Arena 本身就提供了一种直接的、具有实际意义的相对能力评价。它不需要先通过 Rubrics 才具有价值。Rubric-based VLM Evaluation 可以在更多任务和模型上自动执行（可扩展性的评估），并且解释具体缺陷。
因此，导师建议我们采用一种不完全对称、但相互关联的双轨评价体系：
- Human Arena：独立的专家评价参照，用于直接衡量专业设计师对不同产物的相对判断。
- Rubric-based VLM Evaluation：可扩展、细粒度、可解释的自动评价。
- Agreement Analysis（第三部分）：检验自动评价体系与人类判断的一致程度。 

# arena
因为我不是负责arena设计的人，所以我对一些细节不太清楚。但是我被安排进行后续的结果分析，哎。
arena的后台评审网站在：http://10.210.6.10:19102/arena-v2/?view=admin
我把结果导出来了：/mnt/afs_design/huangxinyue/projects/benchmark-design/arena/sorting.json
好像目前只有一个设计评审完了，你先检查一下整体结果。

