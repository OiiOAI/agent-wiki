#!/usr/bin/env python3
"""PreToolUse hook：防止 Write/Edit 工具改动 raw/ 下的源文件。

WIKI_SOP 第 1 条：raw/ 是 source of truth，对 agent 只读。
例外：raw/inbox/_manifest.md 由 agent 在 ingest 流程维护，允许编辑。

新增源应通过 Bash 的 cp/mv 命令（保留原始文件元信息），而非 Write 生成内容。
"""
from __future__ import annotations

import json
import re
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0

    if re.search(r"/raw/inbox/_manifest\.md$", file_path):
        return 0

    if re.search(r"/raw/", file_path):
        print(
            f"BLOCKED by hook: WIKI_SOP 禁止直接写 raw/ 下的源文件。目标：{file_path}",
            file=sys.stderr,
        )
        print(
            "新增源应通过 Bash 的 cp/mv 命令从 workspace/intake 或外部路径复制进来，"
            "保留原始元信息；_manifest.md 是唯一允许编辑的例外。",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
