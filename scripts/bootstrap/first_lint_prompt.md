# first_lint_prompt.md

将以下内容整体发送给你的 Agent：

```text
你现在处于 LLM Wiki 的首次巡检阶段。

先读取以下文件：
- schema/WIKI_SOP.md
- schema/AGENT_PROTOCOL.md
- schema/prompts/lint.md
- wiki/index.md
- wiki/log.md

任务：
1. 对当前 wiki 做第一次健康检查。
2. 重点检查：
   - `index.md` 是否与实际页面一致；
   - 新增页面是否都有 frontmatter；
   - 事实陈述是否带来源；
   - 是否有孤立页、断链、重复页、明显漏建的概念页；
   - 是否存在应标记但未标记的冲突。
3. 低风险结构问题可直接修复。
4. 高风险语义问题只输出提案，不直接改。
5. 在 `wiki/log.md` 追加一条 lint 记录。

输出时严格按以下结构：
### Audit scope
### Findings
### Auto-fixes applied
### Proposals required
### Residual risk

若无法判断某问题属于自动修复还是高风险提案，默认按高风险处理。
```
