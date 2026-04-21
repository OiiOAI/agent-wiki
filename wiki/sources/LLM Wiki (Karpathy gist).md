---
id: src-karpathy-llm-wiki
title: LLM Wiki (Karpathy gist)
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
source_kind: article
source_path: raw/inbox/karpathy-llm-wiki.md
source_origin: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_date: 
source_author: Andrej Karpathy
reliability: high
sources:
  - raw/inbox/karpathy-llm-wiki.md
tags:
  - seed-source
  - karpathy
  - llm-wiki-pattern
---

# LLM Wiki (Karpathy gist)

## Source metadata

- Kind: article（idea/opinion essay，gist 形式）
- Original path: `raw/inbox/karpathy-llm-wiki.md`
- Original URL or origin: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Author / owner: Andrej Karpathy
- Date: 未知。gist 原文无标注日期；抓取时间 2026-04-21。
- Format: Markdown，75 行。
- Reliability assessment: **high** —— 作者是 ML/AI 领域公认权威；文章为模式/观点而非实证研究，高度内部自洽。作为"模式描述"可靠；作为"效用断言"（如规模阈值）则需更多实践交叉验证。

## Executive summary

- LLM Wiki 是一种个人知识库模式：LLM **增量地构建并维护**一个互联 Markdown 仓库，替代每次查询重新检索的 RAG 范式。 [raw/inbox/karpathy-llm-wiki.md#L9-L13]
- 三层架构：**raw**（只读源）/ **wiki**（LLM 拥有的编译层）/ **schema**（如 CLAUDE.md 的规则文件）。 [raw/inbox/karpathy-llm-wiki.md#L29-L33]
- 三个核心操作：**Ingest**（消化新源）、**Query**（答疑并可回填 wiki）、**Lint**（体检与一致性维护）。 [raw/inbox/karpathy-llm-wiki.md#L37-L41]
- 两个特殊文件：**index.md**（内容目录）+ **log.md**（时间流水）；中等规模（~数百页）下 index 足够做 routing，无需 embedding 基础设施。 [raw/inbox/karpathy-llm-wiki.md#L47-L49]
- 典型用法：LLM agent 一侧 + Obsidian 一侧；Obsidian 是 IDE、LLM 是程序员、wiki 是 codebase。 [raw/inbox/karpathy-llm-wiki.md#L15]
- 思想源流：呼应 Vannevar Bush 1945 的 Memex —— 私人、主动策划、文档间有关联轨迹的知识库。 [raw/inbox/karpathy-llm-wiki.md#L70]

## Extractable facts

- RAG 系统（NotebookLM、ChatGPT 文件上传等）在每次查询时从头检索；"nothing is built up"。 [raw/inbox/karpathy-llm-wiki.md#L9]
- 作者日常工作流：LLM agent 一侧、Obsidian 图视图一侧，边聊边浏览 wiki 更新。 [raw/inbox/karpathy-llm-wiki.md#L15]
- 单次 ingest 可能触及 10-15 个 wiki 页面。 [raw/inbox/karpathy-llm-wiki.md#L37]
- 推荐的可选搜索工具：qmd（本地 BM25+向量混合搜索，含 MCP server）。 [raw/inbox/karpathy-llm-wiki.md#L53]
- 推荐的 Obsidian 辅助：Obsidian Web Clipper（剪藏）、Marp（幻灯片）、Dataview（frontmatter 查询）。 [raw/inbox/karpathy-llm-wiki.md#L57-L61]
- wiki 本身就是 git repo，自带版本与分支能力。 [raw/inbox/karpathy-llm-wiki.md#L62]

## Key entities

- [[Andrej Karpathy]] —— 作者，本次建页。
- [[Obsidian]] —— 推荐的 wiki 浏览/编辑端（未建页）。
- [[Memex]] —— 思想先驱（未建页）。
- [[NotebookLM]] / [[ChatGPT]] —— 对比基线（未建页）。
- [[qmd]] —— 推荐的可选搜索工具（未建页）。
- [[Tolkien Gateway]] —— 作为传统 fan-wiki 的类比（未建页）。

## Key concepts

- [[LLM Wiki]] —— 本 gist 定义的核心模式，本次建页。
- [[Retrieval-Augmented Generation]] —— 对比基线（未建页）。
- Ingest / Query / Lint —— 三大操作模式；已在 `schema/AGENT_PROTOCOL.md` 中被定义为操作名，尚未作为独立 concept 页（可推迟到出现更多相关源再建）。

## Potential ingest targets

- 应新建的页面（**本次已建**）：
  - [[LLM Wiki]]（concept）
  - [[Andrej Karpathy]]（entity）
- 应新建但**本次未建**（等更多源支撑再独立建页）：
  - [[Retrieval-Augmented Generation]]（concept）
  - [[Memex]]（concept 或 entity）
  - [[Obsidian]]（entity / tool）
- 可建立的双链：
  - LLM Wiki ↔ RAG（adjacent，对比概念）
  - LLM Wiki ↔ Memex（adjacent，思想先驱）

## Conflicts or caveats

- 与既有资料的潜在冲突：无（本项目原本即围绕此思想而建）。
- 内部潜在张力：
  - 作者强调"LLM 写 wiki、人只负责 sourcing/asking"；本项目 `schema/AGENT_PROTOCOL.md` 在此基础上引入了更严格的审批门与冲突协议，**比原文更保守**。
  - gist 未日期化；`source_date` 留空是刻意选择，不建议猜测。

## Quality assessment

- Parsing quality: 极佳（纯文本 Markdown，无 OCR 问题）。
- OCR / formatting issues: 无。
- Missing sections: 无；文末作者自注"document is intentionally abstract"，不期待覆盖实现细节。
- Whether this source is safe to ingest directly: 安全；为**种子源**，建议未来所有涉及"agent-wiki 模式"的新源都引用回此页。

## Provenance notes

- 本次使用行号区间 `#L<n>-<m>` 作为引用锚点。
- gist raw 原文相对稳定（GitHub gist 有 commit history）；但若源被编辑，行号可能漂移。缓解：同步记录了 SHA-256（见 `raw/inbox/_manifest.md`），可做内容版本指纹。

## Change notes

- 2026-04-21 — 页面初始化；作为第一份真实 ingest 的种子源。
