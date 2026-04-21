---
id: concept-llm-wiki
title: LLM Wiki
type: concept
status: active
created: 2026-04-21
updated: 2026-04-21
sources:
  - raw/inbox/karpathy-llm-wiki.md
confidence: high
tags:
  - pattern
  - knowledge-base
  - agent-managed
related:
  broader: []
  narrower: []
  adjacent: []
---

# LLM Wiki

## Definition

LLM Wiki 指一种个人知识库**模式**：由 LLM agent 主动、增量地在 raw sources 之上构建并维护一个互联的 Markdown 仓库，使知识被**编译一次、持续保鲜**，而非在每次查询时从原始文档重新检索与综合。 [raw/inbox/karpathy-llm-wiki.md#L11]

## Why it matters

- 本 agent-wiki 项目的**全部设计动机**直接来自此概念；`schema/WIKI_SOP.md` 的三层契约、`schema/AGENT_PROTOCOL.md` 的维护者角色均是对该模式的具体化。
- 它解决的不是"检索召回"问题，而是"知识积累 / 维护"问题：RAG 让 LLM 每次重算答案；LLM Wiki 让答案自身变成可复用资产。 [raw/inbox/karpathy-llm-wiki.md#L9-L13]

## Core claims

- 三层架构：**raw**（immutable）/ **wiki**（LLM 写）/ **schema**（配置文件如 CLAUDE.md）。 [raw/inbox/karpathy-llm-wiki.md#L29-L33]
- 三个核心操作：**Ingest** / **Query** / **Lint**；好的 Query 答案应能 fileback 为 durable wiki 页面。 [raw/inbox/karpathy-llm-wiki.md#L37-L41]
- 两个特殊文件驱动导航：**index.md**（内容目录，query 的第一入口）与 **log.md**（时间流水，append-only）。 [raw/inbox/karpathy-llm-wiki.md#L47-L49]
- 中等规模下 index.md 已够做 routing，无需 embedding 基础设施；大规模时再引入本地搜索（如 qmd）。 [raw/inbox/karpathy-llm-wiki.md#L47, #L53]
- 人机分工：人负责 sourcing、探索、提问；LLM 负责 summarizing / cross-referencing / bookkeeping。 [raw/inbox/karpathy-llm-wiki.md#L15, #L68]
- wiki 自身是 git repo，版本与分支能力天然具备。 [raw/inbox/karpathy-llm-wiki.md#L62]

## Boundaries

- **不是 RAG**。核心区别在于：生成过的综合、交叉引用、冲突标注**被物化保存**，不随 session 消失。 [raw/inbox/karpathy-llm-wiki.md#L11-L13]
- **不是全自动系统**。人仍然决定 source 纳入、分析方向、何时裁决冲突。 [raw/inbox/karpathy-llm-wiki.md#L68]
- **不规定具体工具 / 目录 / 模板**。原文明确是"abstract idea file"，具体实现由用户与其 agent 协同演化。 [raw/inbox/karpathy-llm-wiki.md#L75]

## Distinctions

- 与 **[[Retrieval-Augmented Generation]]**（未建页）：RAG 只在 query 时检索与生成；LLM Wiki 在 ingest 时就完成编译，query 只读。 [raw/inbox/karpathy-llm-wiki.md#L9-L13]
- 与 **传统人工 wiki**（如 Tolkien Gateway）：传统 wiki 靠人类志愿者维护；LLM Wiki 把维护成本降到趋近于零。 [raw/inbox/karpathy-llm-wiki.md#L21, #L66]
- 与 **[[Memex]]**（未建页）：思路血缘上接近 —— 私人、策划、文档间关联轨迹；差异在于 Memex 未解决"谁来维护连接"，LLM 补上了这块。 [raw/inbox/karpathy-llm-wiki.md#L70]

## Examples

原文列举了五类典型场景：

- **Personal**：日记、文章、播客笔记 → 自我追踪。 [raw/inbox/karpathy-llm-wiki.md#L19]
- **Research**：数周/数月的主题深潜。 [raw/inbox/karpathy-llm-wiki.md#L20]
- **Reading a book**：为角色 / 主题 / 情节线建页，类 fan-wiki。 [raw/inbox/karpathy-llm-wiki.md#L21]
- **Business/team**：Slack、会议转录、客户通话的内部 wiki。 [raw/inbox/karpathy-llm-wiki.md#L22]
- **其他**：竞品分析、尽调、旅行计划、课程笔记、爱好深研。 [raw/inbox/karpathy-llm-wiki.md#L23]

## Inference

- Inference: 本项目 agent-wiki 相较原文引入了更严格的审批门（review gates）、冲突保留协议、强制溯源格式。可理解为对"个人使用 + 可审计"的保守化扩展；目标动词与原文完全一致，只是规则化程度更高。依据：`schema/WIKI_SOP.md` 与 `schema/AGENT_PROTOCOL.md` 明显比 gist 的 informal 描述严格。

## Uncertainties

- Uncertain: 原文给出的规模阈值"moderate scale (~100 sources, ~hundreds of pages)"下 index.md 够用 —— 是作者个人经验，未给出实测延迟或 token 消耗数据。 [raw/inbox/karpathy-llm-wiki.md#L47]
- Uncertain: "单次 ingest 触及 10-15 页" 的数量级是否适配所有领域？原文为作者工作流观察，并无数据支持。 [raw/inbox/karpathy-llm-wiki.md#L37]

## Related pages

- Broader: _（待补：Agent-Managed Knowledge Base 等上位概念可在后续源中建立）_
- Narrower: _（待补：Ingest / Query / Lint 作为独立概念页）_
- Adjacent: [[Retrieval-Augmented Generation]]（未建）、[[Memex]]（未建）

## Evidence and provenance

- Key sources:
  - [[LLM Wiki (Karpathy gist)]] —— 种子源
- Weak spots in evidence:
  - 目前仅一份源。所有主张均未被其他源交叉验证；需更多实践报告 / 对比文章来巩固或挑战。

## Change notes

- 2026-04-21 — 页面初始化；从 [[LLM Wiki (Karpathy gist)]] 提取。
