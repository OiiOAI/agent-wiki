# first_setup_prompt.md

将以下内容整体发送给你的 Agent：

```text
你现在处于 LLM Wiki 的首次初始化阶段。

先读取以下文件：
- schema/WIKI_SOP.md
- schema/AGENT_PROTOCOL.md
- schema/prompts/setup.md

任务：
1. 检查当前仓库结构是否符合协议。
2. 若缺失关键目录或关键文件，则按最小变更原则补齐。
3. 校验 `wiki/index.md`、`wiki/log.md`、`schema/`、`schema/prompts/` 是否存在且位置正确。
4. 不要修改 `raw/`。
5. 不要创建任何虚构的领域知识页面。
6. 若发现协议文件与目录结构冲突，先输出冲突点与最小修正提案，再执行低风险修正。

输出时严格按以下结构：
### Current state
### Planned changes
### Execution result
### Next safe step

如果无法安全判断，不要猜测，直接停止并输出最小可逆提案。
```
