# first_ingest_prompt.md

将以下内容整体发送给你的 Agent：

```text
你现在处于 LLM Wiki 的首次摄入阶段。

先读取以下文件：
- schema/WIKI_SOP.md
- schema/AGENT_PROTOCOL.md
- schema/prompts/ingest.md
- wiki/index.md
- wiki/log.md

任务：
1. 扫描 `raw/inbox/` 中待处理的原始资料。
2. 选取其中最适合首次摄入的一份资料进行处理；如果有多份，先列出候选并说明排序依据。
3. 完整阅读该资料后，提取核心事实、概念、实体、关键定义、潜在冲突。
4. 在 `wiki/` 中创建或更新最少但足够的页面，不做无关重构。
5. 更新 `wiki/index.md`。
6. 在 `wiki/log.md` 追加一条 ingest 记录。
7. 对每个新增事实附来源；对推断标记 `Inference:`；对证据不足处标记 `Uncertain:`。

输出时严格按以下结构：
### Sources to process
### Extraction summary
### Planned wiki changes
### Execution result
### Outstanding issues

如果本轮资料过大、过乱或存在明显格式问题，不要硬写入 wiki，改为先生成 source summary 或 repair proposal。
```
