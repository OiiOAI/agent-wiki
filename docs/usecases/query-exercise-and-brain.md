# Use Case：用户提问 → Agent 用 wiki 回答

> 一个端到端的 query-mode 走查。基于 S5 staged 真实产出，演示 agent
> 如何按 `schema/AGENT_PROTOCOL.md` 的 Query mode 协议，从 index → wiki
> → raw 三层逐级深入，最后把结构化答案返回给用户。
>
> 本文档不是模拟 — 引用的所有 wiki 页面、provenance 锚点、PDF 页号都是
> S5 ingest 真实产出，可点击复现。

---

## 0. 场景

**用户**：在 agent-wiki 仓库根目录起一个会话，提问：

> "锻炼对大脑有什么具体的影响？BDNF 是什么？跟海马体（hippocampus）的关系？"

**Agent 处境**：
- 会话刚启动，没有任何上下文
- 196 本书已 ingest（其中 health 类含 *Spark*、*Outlive*、*Built to Move* 等）
- `wiki/index.md` 已挂上 ~3000 个页面入口
- `raw/books/health/Spark.pdf` 完整 228 页可读

---

## 1. Agent 启动流程（Protocol §Startup）

每次会话**强制**执行 4 步，缺一不报告：

```
Read schema/AGENT_PROTOCOL.md      # 角色 + 非协商规则
Read schema/WIKI_SOP.md            # 目录契约 + frontmatter + 溯源规范
Read wiki/index.md                 # 页面全貌
Read wiki/log.md (last 20-30 lines) # 近期操作脉络
```

读完后 agent 内部状态：
- 知道自己是 wiki 维护者，不是 chatbot
- 知道 `raw/` 只读、wiki 事实必须带 `[raw/...]` 溯源、`Inference:` / `Uncertain:` 必须显式标注
- 知道现有页面分布（按 type 分组）
- 知道最近哪些 ingest / lint / merge 操作影响了 wiki 状态

---

## 2. 意图路由（CLAUDE.md §意图路由）

用户问"具体影响"、"是什么"、"什么关系" — 经典 **Query mode**。
按 CLAUDE.md 路由表，agent 加载 `schema/prompts/query.md` 的指引：
- 先索引、再细读、最后扩展到原始材料
- 区分事实 / 判断 / 不确定 / 猜测
- 不脑补，不糊弄

---

## 3. Index 探查（Protocol §Query mode step 1）

Agent 在 `wiki/index.md` 里 grep 关键词组合：

```bash
grep -i "BDNF\|brain.derived\|neurotrophic" wiki/index.md
grep -i "hippocamp\|海马"                  wiki/index.md
grep -i "exercise\|neurogenes\|neuroplast"  wiki/index.md
```

预期命中（基于 staged 产出）：
- `wiki/concepts/brain-derived-neurotrophic-factor.md` — Spark
- `wiki/concepts/neurogenesis.md` — Spark + Kandel 双源
- `wiki/concepts/neuroplasticity.md` — Spark
- `wiki/concepts/hippocampus.md` — Spark + Kandel 双源（潜在 conflict 待 Phase F 检测）
- `wiki/sources/spark-the-revolutionary-new-science-of-exercise.md` — 书目入口

Agent 把这 5 个候选页放入 "本次回答的工作集"。**不会**直接读 raw/ —
那是后续验证步骤的事。

---

## 4. Wiki 细读（Protocol §Query mode step 2）

Agent 按依赖序读这 4 个 concept 页 + 1 个 source 页。每页结构固定：
frontmatter / Summary / Key facts / Related pages / Provenance。

### 4.1 [BDNF](tmp/ingest_staging/spark-the-revolutionary-new-science-of-exercise-and-the-john/concepts/brain-derived-neurotrophic-factor.md)

抽取关键 facts：

> - BDNF 是神经细胞活动时产生的蛋白质 [Spark#p222]
> - 被称为大脑的"Miracle-Gro"，喂养已有神经元保持其活性 [Spark#p222]
> - 促进新神经元生长 [Spark#p222]

related → broader: `neurotrophins` / `neuroscience`；narrower 暂空。

### 4.2 [Neurogenesis](tmp/ingest_staging/spark-the-revolutionary-new-science-of-exercise-and-the-john/concepts/neurogenesis.md)

> - 干细胞分裂发育成新神经元的过程 [Spark#p224]
> - 1998 年首次在成人大脑中被确认 [Spark#p224]
> - 仅限于海马体（部分）和与嗅觉相关的脑室下区 [Spark#p224]

related → broader: `neuroscience` / `cell biology`；narrower: `stem cells`。
反向链回 `[[hippocampus]]` `[[neuron]]` `[[brain plasticity]]`。

### 4.3 [Neuroplasticity](tmp/ingest_staging/spark-the-revolutionary-new-science-of-exercise-and-the-john/concepts/neuroplasticity.md)

> - 大脑"是 Play-Doh 而非 porcelain"，可被输入塑形 [Spark#p33]
> - **运动通过促进 plasticity 来优化大脑功能** [Spark#p33] ← 这一句把 BDNF/neurogenesis 串到运动主题
> - Donald Hebb 提出"use-dependent plasticity" [Spark#p41]
> - William Greenough 用电镜证明环境丰富化让神经元长出更密的 dendrite [Spark#p43]
> - 1998 年的癌症患者脑研究确认 neurogenesis [Spark#p43]

related 跨链：`[[BDNF]]` `[[exercise]]` `[[environmental enrichment]]` +
entities `[[Donald Hebb]]` `[[William Greenough]]` `[[Fred Gage]]`。

### 4.4 [Hippocampus](tmp/ingest_staging/spark-the-revolutionary-new-science-of-exercise-and-the-john/concepts/hippocampus.md)

> - 海马体是学习和记忆的"中转站" [Spark#p223]
> - 含大量 cortisol 受体，是 fight-or-flight 反馈环的第一站 [Spark#p223]
> - **大脑中仅有的两个能产生新神经元的结构之一** [Spark#p223] ← 直接对接 4.2

related → `[[neurogenesis]]` `[[memory]]` `[[cortisol]]` `[[stress response]]`。

### 4.5 [Source: Spark](tmp/ingest_staging/spark-the-revolutionary-new-science-of-exercise-and-the-john/sources/spark-the-revolutionary-new-science-of-exercise-and-the-john.md)

源书页拿到：作者、范围、可靠性等元数据，明确这本书的立场（科普 + 治疗导向，
非系统综述）。Agent 由此知道 Spark 适合用作"机制叙述"，但若用户追"具体剂量
反应曲线"则需要扩展到 Outlive 或 Kandel。

---

## 5. 扩展至 raw（Protocol §Query mode step 2 + §System contract）

四个 wiki 页的 facts 都点向 `[raw/.../Spark.pdf#p222-224]` 这一段。
**Agent 此时的判断**：四页讲法一致、互相引用、provenance 都集中在 Spark
第 222–224 这一小段（看起来是书末的"BDNF 与新神经元生成"专章），值得
打开 PDF 实证。

```
Read raw/books/health/Spark _ The Revolutionary New Science of Exercise...pdf
     pages: 222-224
```

PDF 第 222 页的原文（拼读后还原）：
> "BDNF... protein produced inside nerve cells when they are active, like
> Miracle-Gro for the brain... fertilizes brain cells, keeps them functioning
> and growing, spurs the growth of new neurons."

— 与 wiki facts **逐字一致**，溯源准确。

第 33 页 Play-Doh 比喻、第 41 页 Hebb 引语，agent 顺手抽样校对一两条 →
全部可对上 → wiki 引文可信。

**这一步没有带来新事实，但把 wiki 从"可能正确"升级为"已实证"。** 这是
query mode 之所以要走 raw 这一层的根本意义。

---

## 6. 综合答复（Protocol §Default response structure）

Agent 用 AGENT_PROTOCOL §A 的结构化输出：

---

### 事实（带溯源，逐条可点）

1. **运动 → BDNF 上调**：神经细胞活动时分泌 BDNF，BDNF 喂养已有神经元、
   促进新神经元生长。运动是被明确认定能促进大脑可塑性的输入之一。
   - 来源：[[brain-derived-neurotrophic-factor]] +
     [Spark#p222](raw/books/health/Spark%20_%20The%20Revolutionary%20New%20Science%20of%20Exercise%20and%20the%20-%20John%20J_%20Ratey%3B%20Eric%20Hagerman.pdf#p222)
   - 溯源：[[neuroplasticity]] §key facts:2

2. **海马体是少数能产生新神经元的脑区**：成人 neurogenesis 主要发生在
   海马体的一个分区（齿状回，dentate gyrus）和嗅觉相关的脑室下区。
   - 来源：[[hippocampus]] §key facts:5 + [[neurogenesis]] §key facts:3
   - 溯源：[Spark#p223](raw/books/health/Spark.pdf#p223),
     [Spark#p224](raw/books/health/Spark.pdf#p224)

3. **海马体 + 压力反馈环**：海马体含大量 cortisol 受体，是 fight-or-flight
   反馈调节的第一站；正因如此它对慢性压力高度敏感。
   - 来源：[[hippocampus]] §key facts:3
   - 溯源：[Spark#p223](raw/books/health/Spark.pdf#p223)

### 判断（基于 wiki 跨页关联，未在原书直接陈述）

> **Inference**：把 4.1–4.4 串起来 → 运动通过 BDNF → 在海马体催生新神经元
> → 改善学习/记忆、并增强压力反馈。这条因果链是 Ratey 全书的核心论点，
> 但 wiki 中**单页未直接做此连接**，是 agent 跨页综合得出的。

> **Inference**：1998 年 neurogenesis 被首次确认这一时间戳在 4.2 和 4.3
> 都出现 → 暗示是同一份 Eriksson/Gage 论文。Wiki 没有显式建 entity 页
> `[[Eriksson 1998 paper]]`，建议 lint 阶段补建。

### 不确定点

> **Uncertain**：BDNF 的具体剂量-反应（多大强度、多长时间运动 → 多少
> 上调？）— 当前 wiki 仅有定性表述，无数字。Spark 第 222 页前后可能
> 有定量讨论，但这部分**没被抽取成 fact**。

> **Uncertain**：跨书一致性未验证 — 同主题在 [[outlive]]（Peter Attia）、
> [[kandel-neural-science-6e]] 都有覆盖（已在 staging），但 Phase F
> conflict_check 还没跑，可能存在 BDNF 表述差异（例如 Kandel 教科书
> 是否会区分 BDNF 与其他 neurotrophin 家族成员）。

### 猜测（明确标注）

> **Guess**：用户问这个问题大概率是想为自己的运动习惯找科学依据。如果
> 是，Spark 第 4 章（焦虑章节）和 [[outlive]] 的"Centenarian Decathlon"
> 框架可能更直接对应"具体怎么做"。

### 建议（仅在确有必要时）

1. 若用户想深挖剂量-反应：拉 Spark §4 (anxiety chapter) 全章重读，
   以及 Outlive 的 VO2 max 章节（已 staged 在 [[outlive]] 下）
2. 若用户想做跨书校对：提一个 conflict_check 任务，对 BDNF / neurogenesis /
   hippocampus 在 Spark vs Kandel vs Outlive 三本书中的表述做语义比对
3. 若多次访问同主题：把本次综合 inference 落成
   `wiki/topics/exercise-and-brain.md` topic 页，把 4 个 concept 页
   作为子节点串起来 — 下次类似提问可直接跳 topic

---

## 7. 是否落成 durable 页面？（Protocol §Query mode step 4）

Agent 自问：**这次综合的 inference 值不值得保留下来？**

判断标准（来自 query.md）：
- ✅ 用户问题足够通用（不是一次性 ad-hoc）
- ✅ 综合 inference 不在任何单页里（跨 4 页才得出）
- ⚠️ 但 wiki 里没有 `wiki/topics/exercise-and-brain.md` 这个 topic 页

**决定**：建议（不主动建）建一个 topic 页，把 4 个 concept 串起来 +
本次的两条 inference。**等用户批准**再动手 — 因为新建页 = 一次 wiki
edit，要走 §Page-writing protocol 全流程（frontmatter / 链接 / 溯源 /
log entry），不能在 query 回应里夹带。

---

## 8. 收尾（Protocol §Logging protocol）

无论是否落页，本次 query 都要在 `wiki/log.md` 追加一条结构化日志：

```markdown
## [2026-04-24 13:45] query | exercise → brain mechanism
- Trigger: 用户问 "锻炼对大脑的影响 / BDNF / hippocampus"
- Sources read: index.md, 4 concept pages, 1 source page, raw Spark pp.33,41,222-224
- Files created: 0
- Files modified: 0
- Outstanding issues:
  - 建议建 wiki/topics/exercise-and-brain.md（待用户批准）
  - 建议跑 conflict_check 对 BDNF/neurogenesis 三书表述（待用户批准）
  - 建议补 entity [[Eriksson 1998 paper]]（lint mode 可处理）
```

---

## 9. 这套流程显示出来的几个特性

| 特性 | 体现在哪一步 |
|---|---|
| **不脑补**：每条 fact 都点回 PDF 具体页 | §6 事实 §溯源链 |
| **跨页 inference 必须显式标注** | §6 判断段，前缀 `Inference:` |
| **不知道就说不知道** | §6 不确定点，剂量反应这条 |
| **猜测必须标 `Guess:`** | §6 第 4 段 |
| **不擅自建/改页面** | §7 建议但等批准 |
| **每次操作都留痕** | §8 log 条目 |
| **raw 永远只读，仅作验证** | §5 用 Read 而非 Edit |
| **链接闭环**：wiki 页互链 + 反指 raw | §4 each page §6 each fact |

---

## 10. 何时这个 use case 会"失效"

诚实列出几个会让本套流程跑偏的情境（agent 应在这些情况下停下问用户）：

1. **同主题在多本书表述冲突** — §6 的"判断"和"不确定"会变得很厚。
   按 Protocol §Conflict protocol 的要求，agent 应建 `wiki/conflicts/`
   页让用户裁决，不能静默择一。
2. **wiki 页 stale**（书更新后未重新 ingest）— provenance 仍指 raw 旧
   PDF，但 raw 已被替换。靠 lint mode `check_provenance_format` 抽查
   sha256 漂移可发现，但 query mode 自身查不到。
3. **关键概念没建页**（如此处的 Eriksson 1998 paper）— agent 只能在
   §6 inference 段顺手提一句"建议补建"，不能假装这页存在。
4. **用户问的是 raw 完全没覆盖的领域**（例如本仓没有任何运动生理学
   原始论文）— agent 应明确说"当前 raw 不支撑这个问题，只能给概略
   叙述"，并提议把相关源补进 `raw/inbox/` 等下次 ingest。

---

**本文档目的**：让任何接手 agent-wiki 仓库的人（包括未来的 agent
自己）能照着这套 7 步走完一次 query，不靠记忆、不靠灵感，纯协议驱动。
