离线评测工作包 2026-11-09

解压后先打开 START.html，或直接打开 project/results_eval 下的各报告 HTML。

内容
- results_eval 的全部原始文件与已生成分析、图表、证据；两个目录别名已实体化。
- 全部177个索引运行，加报告引用的1个历史运行；原始trajectory、trace抓包、media图片、完整run.log（存在的148份）、运行快照、交付图和判官输入。
- 27个轮次的评分数据库、题目/输入/量表配置，Arena数据库与排序快照、交付包及29题需求。
- 分析脚本、量表、过程文档、依赖版本、相对路径索引及逐文件SHA256。

本地工作步骤
1. 解压。先执行 python tools/verify_bundle.py 核对原始包文件。
2. 如需运行脚本或让报告中的服务器绝对路径指向本机，执行 python tools/prepare_local.py。
   它只转换 project 内文本里的已知原始路径；raw runs 不改写。修改前的文本另存 metadata/original_project_text。
   转换后 checksums.json 不再对应被修改的工作文本，这是预期现象；原始压缩包和备份保留不变。
3. 使用 Python 3.10+，按 requirements-analysis.txt 安装依赖。HTML浏览与数据读取可离线；包内不含Python环境和依赖wheel。
4. 从 project 目录运行 arena/analysis 下脚本。示例：python arena/analysis/workflow_analysis.py。
   本地只分析数据，不启动Figma/模型接口。云端Figma链接仍需网络及原有访问权限。

路径
project/：原项目结构；runs/huangxinyue/、runs/gaoyongyong/：原始运行及评分数据。
metadata/portable_run_index.csv：无需改路径即可读的相对路径索引。
metadata/file_inventory.csv：来源、包内路径、大小与打包动作。
metadata/path_map.json：服务器路径与本地目录的映射。

数据库
所有SQLite库使用在线backup接口生成一致性快照并通过quick_check；WAL内容已合入。
不复制-wal/-shm和写锁文件。快照数据库字节哈希可能与源库不同，属于正常情况。

边界与缺口
- Arena的20张历史候选图在现有本地资产中找不到精确SHA256匹配；见metadata/arena_image_inventory.csv。没有用别的版本替代。
- 本地没有原生.fig副本；Figma作答/模板URL、图层快照、媒体与截图均已保留，不能据此声称原生可编辑文件可离线打开。
- 4个历史Arena Gemini run的原始轨迹本地仍未知；不虚构补齐，版本差异见已有资产清单。
- Chat Bot AI旧GPT仅作为历史证据保留，分析排除规则不变。
- 按资产清单排除claude-config、private、账号/代理/MCP服务器配置、运行缓存和锁，不含登录凭据目录。
- 工作包是完整的私有研究材料，包含原始运行日志与人评数据库；不是为匿名公开发布整理的数据集。
