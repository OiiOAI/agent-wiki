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

## [2026-04-21 16:20] migrate | Anti-OS books → raw/books/

- Trigger: 用户指定把旧 Anti-OS 知识库（`/Users/moondy/Desktop/Anti-OS`，2.2G、9069 文件）的**原始资料**复制进新框架；旧库保持原位不动；拒绝迁移旧 wiki/schema/scripts（避免旧 SOP 污染新框架）。
- Sources:
  - `/Users/moondy/Desktop/Anti-OS/raw/` —— 仅 `*.pdf` + `*.epub`
- Files created:
  - `raw/books/neuroscience/` — 43 files
  - `raw/books/philosophy/` — 42 files
  - `raw/books/strategy/` — 28 files
  - `raw/books/psychology/` — 26 files
  - `raw/books/productivity/` — 16 files
  - `raw/books/economics/` — 16 files
  - `raw/books/sociology/` — 11 files
  - `raw/books/business/` — 9 files
  - `raw/books/health/` — 5 files
  - 合计 **196 unique** PDF/EPUB（源 202 份，6 份跨目录重复，按 basename 去重）
- Files modified:
  - `raw/inbox/_manifest.md` —— 追加 `books/` 批次台账
  - `.gitignore` —— 屏蔽 `raw/books/`（2.0G，不进 git）
- Files deprecated:
  - 本日早些时候（14:40 之后）由旧迁移方案产生的 `raw/archive/anti-os-2026-04-21/`（2.1G rsync 快照）已删除；该方案被用户在执行中驳回，理由："归档+legacy 视图+按需 re-ingest 会让知识库很乱"。
- Notes:
  - **分类原则**：浅平 9 学科分类，非 Anti-OS 原目录（旧目录是"Kernel/Network/Environment/Energy"+ 自由能原理语义，不适配新框架；新分类按**书的学科属性**）。
  - **严格排除清单**：`.env` / `.obsidian/` / `.DS_Store` / `tmp/` / `__pycache__/` / 旧 wiki/ / 旧 schema/ / 旧 scripts/ / 旧 tasks/ / 旧 docs/ —— 只要原始资料，拒绝继承旧加工层。
  - **敏感扫描**：旧库 `.env` 含真 `ANTHROPIC_API_KEY`，已严格排除；`grep ANTHROPIC_API_KEY raw/books/` 应为空（PDF/EPUB 中不会出现）。
  - **raw/books/ 不入 git**：体积 2.0G，git 处理会显著变慢；`.gitignore` 屏蔽，跨机同步靠外部手段。manifest 仍作台账。
  - **复制 ≠ ingest**：本条目是"把原始资料搬进 raw/"，不等于"已进入 wiki"。任何书要进 wiki 必须按 `schema/prompts/ingest.md` 走常规流程，生成 `wiki/sources/<Book Name>.md` + 相应 `wiki/concepts/` 或 `wiki/entities/` 页，严格行/页锚溯源。
  - 审批门：本批动作单次文件数 >10（实际 196 份），但全部为同一类型（复制原始资料到 raw/），按批次视为一次原子操作；本 log 条目即为事后记录。
- Outstanding issues:
  - 未逐文件算 SHA-256；P1/P3 阶段若需"源版本追踪"可跑 `scripts/gen/raw_hash.py`（待建）。
  - `raw/books/` 里的 196 份中有多少值得建 `wiki/sources/` 页、从哪几本开始 re-ingest？待用户指示。建议优先级：neuroscience（Friston/Kandel/Damasio 主轴）+ strategy（Rumelt/Boyd）。
  - 分类边界模糊项（后续若发现引用不便可再搬）：Kahneman《Thinking, Fast and Slow》放 strategy（决策侧重）而非 psychology；Haidt《Righteous Mind》放 philosophy 而非 psychology；Sapolsky《Behave》放 psychology 而非 neuroscience；Deep Work 放 productivity 而非 strategy。以实际查询路径反馈调整。

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

## [2026-04-25] ingest | boundaries-henry-cloud-john-townsend
- Trigger: S6 batch commit (Phase H of ingest pipeline).
- Sources: raw/books/business/Boundaries - Henry Cloud & John Townsend.pdf
- Files created:
  - `wiki/entities/sherrie-case-study.md`
  - `wiki/concepts/age-appropriate-boundary-training.md`
  - `wiki/concepts/boundary-conflicts-friends.md`
  - `wiki/concepts/boundary-conflicts-marriage.md`
  - `wiki/concepts/boundary-development-children.md`
  - `wiki/concepts/common-boundary-myths.md`
  - `wiki/concepts/discipline-vs-punishment.md`
  - `wiki/concepts/eleven-steps-boundary-development.md`
  - `wiki/concepts/internal-boundary-problems.md`
  - `wiki/concepts/law-of-activity.md`
  - `wiki/concepts/law-of-envy.md`
  - `wiki/concepts/law-of-exposure.md`
  - `wiki/concepts/resistance-to-boundaries.md`
  - `wiki/concepts/triangulation.md`
  - `wiki/sources/boundaries-cloud-townsend.md`
- Files deprecated: None.
- Notes: 15 new + 0 merged. Auto-generated from staged extraction; verify outliers in next lint pass.

## [2026-04-25] ingest | high-output-management
- Trigger: S6 batch commit (Phase H of ingest pipeline).
- Sources: raw/books/business/High_Output_Management.epub
- Files created:
  - `wiki/entities/andrew-s-grove.md`
  - `wiki/entities/intel-corporation.md`
  - `wiki/concepts/black-box-model.md`
  - `wiki/concepts/compensation-feedback.md`
  - `wiki/concepts/dual-reporting.md`
  - `wiki/concepts/hybrid-organization.md`
  - `wiki/concepts/ideal-decision-making-model.md`
  - `wiki/concepts/interviewing.md`
  - `wiki/concepts/limiting-step.md`
  - `wiki/concepts/management-by-objectives.md`
  - `wiki/concepts/managerial-leverage.md`
  - `wiki/concepts/managerial-training.md`
  - `wiki/concepts/maslow-hierarchy.md`
  - `wiki/concepts/modes-of-control.md`
  - `wiki/concepts/one-on-one-meeting.md`
  - `wiki/concepts/output-oriented-management.md`
  - `wiki/concepts/peer-group-syndrome.md`
  - `wiki/concepts/performance-appraisal.md`
  - `wiki/concepts/performance-review-delivery.md`
  - `wiki/concepts/peter-principle.md`
  - `wiki/concepts/productivity.md`
  - `wiki/concepts/task-relevant-maturity.md`
  - `wiki/concepts/valued-employee-retention.md`
  - `wiki/sources/high-output-management.md`
- Files deprecated: None.
- Notes: 24 new + 0 merged. Auto-generated from staged extraction; verify outliers in next lint pass.

## [2026-04-25] ingest | profit-first-mike-michalowicz
- Trigger: S6 batch commit (Phase H of ingest pipeline).
- Sources: raw/books/business/Profit First - Mike Michalowicz.pdf
- Files created:
  - `wiki/entities/anjanette-harper.md`
  - `wiki/entities/greg-crabtree.md`
  - `wiki/entities/jesse-cole.md`
  - `wiki/entities/jorge-morales-jose-pain.md`
  - `wiki/entities/jorge-morales.md`
  - `wiki/entities/keith-fear.md`
  - `wiki/entities/laurie-dutcher.md`
  - `wiki/entities/mike-michalowicz.md`
  - `wiki/entities/rick-barry.md`
  - `wiki/concepts/accountability-buddy.md`
  - `wiki/concepts/bank-balance-accounting.md`
  - `wiki/concepts/current-allocation-percentages.md`
  - `wiki/concepts/debt-freeze.md`
  - `wiki/concepts/debt-snowball.md`
  - `wiki/concepts/endowment-effect.md`
  - `wiki/concepts/instant-assessment.md`
  - `wiki/concepts/loss-aversion.md`
  - `wiki/concepts/mini-power-tactics.md`
  - `wiki/concepts/owners-compensation.md`
  - `wiki/concepts/pareto-overlap.md`
  - `wiki/concepts/parkinsons-law.md`
  - `wiki/concepts/primacy-effect.md`
  - `wiki/concepts/profit-distribution.md`
  - `wiki/concepts/profit-first-kids.md`
  - `wiki/concepts/profit-first-lifestyle.md`
  - `wiki/concepts/profit-first-quick-setup-guide.md`
  - `wiki/concepts/profit-first-system.md`
  - `wiki/concepts/profit-squeeze.md`
  - `wiki/concepts/required-income-for-allocation.md`
  - `wiki/concepts/small-plates-principle.md`
  - `wiki/concepts/survival-trap.md`
  - `wiki/concepts/target-allocation-percentages.md`
  - `wiki/concepts/wedge-system.md`
  - `wiki/topics/advanced-profit-first-accounts.md`
  - `wiki/topics/entrepreneurial-profitability.md`
  - `wiki/topics/expense-cutting.md`
  - `wiki/topics/profit-first-implementation-timeline.md`
  - `wiki/sources/profit-first.md`
- Files deprecated: None.
- Notes: 38 new + 0 merged. Auto-generated from staged extraction; verify outliers in next lint pass.

## [2026-04-25] ingest | rework-jason-fried
- Trigger: S6 batch commit (Phase H of ingest pipeline).
- Sources: raw/books/business/Rework - Jason Fried.pdf
- Files created:
  - `wiki/entities/37signals.md`
  - `wiki/entities/david-hansson.md`
  - `wiki/entities/jason-fried.md`
  - `wiki/concepts/build-half-product.md`
  - `wiki/concepts/building-an-audience.md`
  - `wiki/concepts/dont-be-a-hero.md`
  - `wiki/concepts/embrace-constraints.md`
  - `wiki/concepts/ignore-real-world.md`
  - `wiki/concepts/launch-now.md`
  - `wiki/concepts/learning-mistakes-overrated.md`
  - `wiki/concepts/meetings-are-toxic.md`
  - `wiki/concepts/outside-money-plan-z.md`
  - `wiki/concepts/planning-is-guessing.md`
  - `wiki/concepts/say-no-by-default.md`
  - `wiki/concepts/scratch-your-own-itch.md`
  - `wiki/concepts/underdo-competition.md`
  - `wiki/concepts/workaholism-stupid.md`
  - `wiki/sources/rework-book.md`
- Files deprecated: None.
- Notes: 18 new + 0 merged. Auto-generated from staged extraction; verify outliers in next lint pass.

## [2026-04-25] ingest | team-topologies
- Trigger: S6 batch commit (Phase H of ingest pipeline).
- Sources: raw/books/business/Team_Topologies.epub
- Files created:
  - `wiki/entities/adaptive-structuration-theory.md`
  - `wiki/entities/bruce-tuckman.md`
  - `wiki/entities/cybernetics.md`
  - `wiki/entities/dave-snowden.md`
  - `wiki/entities/devops-topologies.md`
  - `wiki/entities/five-dysfunctions-of-a-team.md`
  - `wiki/entities/james-lewis.md`
  - `wiki/entities/john-sweller.md`
  - `wiki/entities/manuel-pais.md`
  - `wiki/entities/matthew-skelton.md`
  - `wiki/entities/mel-conway.md`
  - `wiki/entities/norbert-wiener.md`
  - `wiki/entities/patrick-lencioni.md`
  - `wiki/entities/robin-dunbar.md`
  - `wiki/entities/ruth-malan.md`
  - `wiki/concepts/cognitive-load-management.md`
  - `wiki/concepts/cognitive-load.md`
  - `wiki/concepts/collaboration-mode.md`
  - `wiki/concepts/complicated-subsystem-team.md`
  - `wiki/concepts/complicated-subsystem-teams.md`
  - `wiki/concepts/conways-law.md`
  - `wiki/concepts/dunbars-number.md`
  - `wiki/concepts/enabling-team.md`
  - `wiki/concepts/enabling-teams.md`
  - `wiki/concepts/evolution-of-team-topologies.md`
  - `wiki/concepts/facilitating-mode.md`
  - `wiki/concepts/fracture-plane.md`
  - `wiki/concepts/hidden-monoliths.md`
  - `wiki/concepts/organizational-sensing.md`
  - `wiki/concepts/platform-team.md`
  - `wiki/concepts/platform-teams.md`
  - `wiki/concepts/reverse-conway-maneuver.md`
  - `wiki/concepts/stream-aligned-team.md`
  - `wiki/concepts/stream-aligned-teams.md`
  - `wiki/concepts/team-anti-patterns.md`
  - `wiki/concepts/team-api.md`
  - `wiki/concepts/team-first-thinking.md`
  - `wiki/concepts/team-topologies-framework.md`
  - `wiki/concepts/x-as-a-service-mode.md`
  - `wiki/topics/four-fundamental-team-topologies.md`
  - `wiki/topics/team-interaction-modes.md`
  - `wiki/topics/team-topology-design-principles-ch4.md`
  - `wiki/sources/team-topologies.md`
- Files deprecated: None.
- Notes: 43 new + 0 merged. Auto-generated from staged extraction; verify outliers in next lint pass.
