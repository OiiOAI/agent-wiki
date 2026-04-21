# log.md

This file is the append-only operational history of the wiki.

## [2026-04-10 14:36] setup | initial repository skeleton
- Trigger: Initial repository bootstrap.
- Sources: None.
- Files created:
  - `wiki/index.md`
  - `wiki/log.md`
  - directory skeleton under `raw/`, `wiki/`, and `schema/`
- Files modified: None.
- Files deprecated: None.
- Notes: Repository initialized with empty section structure and starter operational files.
- Outstanding issues:
  - `schema/WIKI_SOP.md` should be copied in if not already present.
  - `schema/AGENT_PROTOCOL.md` should be copied in if not already present.
  - task prompt files should be placed under `schema/prompts/`.

## [2026-04-21 14:30] setup | P0 infrastructure activation
- Trigger: 《agent-wiki 系统优化方案》P0 阶段实施（参见 `~/.claude/plans/partitioned-bouncing-piglet.md`）。
- Sources: 无（基础设施升级，非内容 ingest）。
- Files created:
  - `CLAUDE.md` — agent 入口文件，指向 SOP/Protocol 并给出意图路由
  - `.claude/settings.json` — Claude Code 权限与 hooks
  - `scripts/hooks/block_raw_edits.py` — PreToolUse 钩子，保护 `raw/` 不被 Write/Edit 直接修改（`_manifest.md` 例外）
  - `scripts/hooks/README.md`
- Files modified:
  - `.gitignore` — 扩展覆盖 Python 缓存、venv、加速层产物
- Files deprecated: 无。
- Notes:
  - 本仓库先前不是 git 项目；本次 `git init` 并完成 2 次提交（eedc537 初始、2e6191a 钩子）。
  - 钩子已做单元测试：raw/ 写入 → exit 2（阻止）；_manifest.md → exit 0；wiki/ → exit 0。
  - SessionStart hook 未单独添加 —— `CLAUDE.md` 会被 Claude Code 自动加载，已覆盖其职能。
  - `scripts/validate.sh` 的 PostToolUse 钩子留待 P1 脚本层实施后再补。
- Outstanding issues:
  - P1 脚本层（frontmatter / link / index_drift / provenance 校验脚本）未实施。
  - Dashboard 目前仍为手写；P1.2 将改为脚本生成。

## [2026-04-21 14:40] ingest | LLM Wiki (Karpathy gist)
- Trigger: P0.4 首次真实 ingest，跑通 collect → ingest → wiki 整条工作流。
- Sources:
  - `raw/inbox/karpathy-llm-wiki.md` （75 行，SHA-256 `dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401`，自 https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f 抓取）
- Files created:
  - `wiki/sources/LLM Wiki (Karpathy gist).md`
  - `wiki/concepts/LLM Wiki.md`
  - `wiki/entities/Andrej Karpathy.md`
- Files modified:
  - `wiki/index.md` — 新增 1 entity / 1 concept / 1 source 条目
  - `raw/inbox/_manifest.md` — 登记 karpathy-llm-wiki.md 的元信息与 SHA
- Files deprecated: 无。
- Notes:
  - 所有事实性断言均带 `[raw/inbox/karpathy-llm-wiki.md#Lx-y]` 溯源；推论用 `Inference:`，不确定用 `Uncertain:`。
  - **不建页**决策：RAG / Memex / Obsidian / NotebookLM / qmd / Tolkien Gateway 在此源中仅为对比或工具提及，信息量不足以独立建页；作为 `Potential ingest targets` 记在源页。
  - [[Andrej Karpathy]] 实体页严格遵守"无溯源不主张"，仅写 gist 内可直接推得的内容；不引入 OpenAI / Tesla / nanoGPT 等公共知识。
- Outstanding issues:
  - gist 无日期，`source_date` 留空；需要时间排序时可查 gist commit history 补。
  - 原文规模阈值 "~100 sources, ~hundreds of pages 下 index 够用" 缺乏实测，待后续实践或其他文献交叉验证。
  - [[LLM Wiki]] 页 `related.broader` 和 `.narrower` 暂空 —— 需要更多源才能定位其在知识图谱中的位置。

## Log entry template

```text
## [YYYY-MM-DD HH:MM] operation | short title
- Trigger:
- Sources:
- Files created:
- Files modified:
- Files deprecated:
- Notes:
- Outstanding issues:
```

## Rules

1. Append new entries; do not rewrite history except for obvious formatting fixes.
2. Record every ingest, major query-save, lint pass, merge, rename, rollback, or schema change.
3. Keep titles short and parseable.
4. If an operation is uncertain or partially failed, state that explicitly.
