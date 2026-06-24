#!/usr/bin/env python3
"""Cursor postToolUse hook: 业务路径编辑后提示跑 harness auto。"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        return

    tool_input = payload.get("tool_input") or payload.get("arguments") or {}
    path = ""
    if isinstance(tool_input, dict):
        path = str(tool_input.get("path") or tool_input.get("file_path") or "")

    norm = path.replace("\\", "/")
    if norm.startswith(("src/os_core/", "src/apps/", "src/integration/")) and norm.endswith(".py"):
        ctx = (
            "【Harness】已编辑业务 .py → 建议运行："
            "./scripts/harness --tier auto"
        )
        print(json.dumps({"additional_context": ctx}, ensure_ascii=False))
        return

    print("{}")


if __name__ == "__main__":
    main()
