# _manifest.md

Track files copied into raw/inbox with original path, reason for inclusion, and notes.

> Books batch 登记在本文件末尾的 `## books/` 章节 —— 体积较大（~2.0G），按 `.gitignore` 策略不入 git，但 manifest 仍作为全量台账。

## karpathy-llm-wiki.md

- Original path: https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/llm-wiki.md
- Fetched: 2026-04-21 via `curl`
- SHA-256: `dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401`
- Author: Andrej Karpathy
- Reason for inclusion: 本项目的原始思想来源；作为第一份正式 ingest 的种子源。
- Notes: gist 原文未标注日期；已按 WIKI_SOP 复制进 inbox 后即视为只读。

## books/ (批次 2026-04-21)

- Source: `/Users/moondy/Desktop/Anti-OS/raw/` 全部 PDF/EPUB（旧 Anti-OS 知识库的原始资料层）；旧库 **保持原位、完全不动**。
- Copied: 196 unique files（含跨目录去重 6 份）到 `raw/books/<discipline>/`
- Excluded: `.env` / `.obsidian/` / `.DS_Store` / `tmp/` / `__pycache__/` / 旧 wiki/ / 旧 schema/ / 旧 scripts/ / 旧 tasks/ / 旧 docs/ —— 仅保留**原始资料**，旧的 Anti-OS 加工层（wiki/schema 等）一律不迁入。
- Classification（9 个学科，浅分类，非 Anti-OS 原分类）:
  - `neuroscience/` — 43（Kandel, Damasio, LeDoux, Dehaene, Seth, Hawkins, Friston 等）
  - `philosophy/` — 42（含 42 份中西哲学：红楼梦 / 道德经 / 周易 / 坛经 / 传习录 / 佛经 / 荀子 / 王德峰讲《道庄》/ 二十世纪西方哲学经典 / Rawls / Frankl / Campbell / Pirsig / Carse / 赵汀阳 / 葛兆光 等）
  - `strategy/` — 28（Rumelt, Boyd, Klein, Cynefin, Taleb, Meadows, Pearl, Kahneman, Munger, Pascal Fisher, 孙子 不在此处 —— 归 philosophy；此处含 Getting to Yes / Never Split / How to Measure Anything / Algorithms to Live By / Thinking in Bets / Book of Why / Checklist Manifesto 等）
  - `psychology/` — 26（Freud, Kahneman 已在 strategy, 此处含 Barrett, Cialdini, Haidt, Kishimi, Rosenberg, Tolle, Perel, Frankl 已在 philosophy, Sapolsky, DBT 等）
  - `productivity/` — 16（Clear, Newport, Forte, Allen, Ahrens, McKeown, Kleon, Guise, Fogg, Williams 等）
  - `economics/` — 16（萨缪尔森 / 凯利森 / 凯恩斯 / 弗里德曼 / 斯蒂格利茨 / 鲍默尔 / 阿罗 / 舒尔茨 / 欧根 / 阿特金森 / 加比希 / 贝纳西 / 雷诺兹 / 法伊格 / 布莱克 等）
  - `sociology/` — 11（乡土中国 / 置身事内 / 社会学·上·下 / 社会学的想象力 / 吉登斯《亲密关系的变革》《失控的世界》/ Fukuyama《Trust》/ 瑞泽尔《现代社会学理论》/ 《全球化压力下的世界文化》/ 方正证券 ChatGPT 研报）
  - `business/` — 9（High Output Management / Team Topologies / E-myth / Lean Startup / Profit First / Rework / SPEED of Trust / Boundaries / 兼并与收购）
  - `health/` — 5（Outlive / Sleep / Spark / Built to Move / Genius Foods）
- SHA 追踪：本批未逐文件算 SHA（~2.0G），后续 P1/P3 若需可跑 `scripts/gen/raw_hash.py`（待实施）。
- Notes: 本批仅是**原始资料复制**，不等于 ingest —— 任何 book 要进入 wiki 必须按 `schema/prompts/ingest.md` 单独 re-ingest。路径锚点形如 `raw/books/<discipline>/<filename>#p<N>`（PDF 按页）。
- Outstanding:
  - 去重 6 份（Antifragile / Finite and Infinite Games / Never Split / Naval / Feeling of What Happens / Thinking Fast and Slow）—— 源文件有重复副本，目标只保留一份；若将来要引用，源目录的版本不同需再辨别。
  - `raw/books/` 已加入 `.gitignore`，**不进 git**；如需跨机同步靠外部（rsync / 云盘）。
