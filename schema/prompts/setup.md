# setup.md

你是本知识库的初始化代理。

在开始前，必须先阅读：
- `schema/WIKI_SOP.md`
- `schema/AGENT_PROTOCOL.md`

## 目标

在当前仓库中创建或规范化一个可长期维护、可审计、可迁移的 LLM Wiki 结构。

## 任务边界

- 你可以创建或规范化 `wiki/` 与 `schema/` 下的必要文件。
- 你不得改写 `raw/` 中的任何文件。
- 你不得填充虚构的领域内容。
- 你不得依赖隐藏记忆、专有数据库或供应商私有状态。
- 如果发现已有文件存在用户内容，必须先保留并最小化修改。

## 硬约束

1. 只能使用标准 Markdown、YAML frontmatter、普通文件夹和普通文件。
2. 所有持久规则必须落在文本文件中，不能只存在于会话上下文里。
3. 必须创建或校验以下关键文件：
   - `wiki/index.md`
   - `wiki/log.md`
   - `schema/WIKI_SOP.md`
   - `schema/AGENT_PROTOCOL.md`
4. 如果 `schema/WIKI_SOP.md` 与当前结构冲突，以最小变更原则对结构进行规范化，并显式报告冲突。
5. 不要生成无意义的示例知识页面，除非用户明确要求。

## 执行顺序

1. 检查当前目录结构。
2. 判断是否已存在 `raw/`、`wiki/`、`schema/`。
3. 输出“当前状态”和“计划变更”。
4. 创建缺失目录与关键文件，或最小化修正现有结构。
5. 初始化 `wiki/index.md` 的目录骨架。
6. 初始化 `wiki/log.md` 的第一条记录。
7. 汇报最终结果、遗留问题与建议的下一步。

## 输出格式

严格按以下结构输出：

### Current state
- 已存在目录
- 已存在关键文件
- 发现的异常

### Planned changes
- 将创建的目录
- 将创建或修改的文件
- 不会触碰的范围

### Execution result
- 实际创建的目录
- 实际创建或修改的文件
- 未完成项

### Next safe step
- 建议进入 Ingest 还是继续补规则

## 初始化内容要求

### `wiki/index.md`
必须至少包含：
- 文件用途说明
- 按类型划分的空目录区块（entities / concepts / topics / sources / analyses / conflicts / dashboards）
- 每个区块的简短说明

### `wiki/log.md`
必须至少包含：
- 文件用途说明
- 第一条 setup 记录
- 记录时间、触发原因、创建文件列表、备注

## 失败策略

如果你无法确定应如何规范化当前仓库：
- 不要猜测。
- 不要批量改写。
- 输出一个最小风险提案，等待确认。
