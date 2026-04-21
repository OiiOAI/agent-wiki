# scripts/hooks/

Claude Code hook 脚本集合，由 `/.claude/settings.json` 调用。

## 现有

| 脚本 | 钩子 | 作用 |
|---|---|---|
| `block_raw_edits.py` | PreToolUse(Write\|Edit) | 阻止直接修改 `raw/` 下源文件（`_manifest.md` 例外） |

## 设计原则

- **fail-open**：hook 自身异常不阻断 agent 工作（避免基础设施故障扩大为流程故障）
- **快启动**：避免重依赖；标准库 Python 即可
- **语义清晰**：blocked 时 stderr 输出原因 + 建议替代路径

## 后续（P1 计划）

- `on_wiki_write.py`（PostToolUse）：wiki/ 被改动后提醒跑 `scripts/validate.sh`
- `log_guard.py`（PreToolUse）：阻止修改 wiki/log.md 历史条目（只允许 append）
