#!/usr/bin/env python3
"""Cursor postToolUse：业务 .py 编辑后强传感器（L4 P1）。

作用：调用 sensor_scoped_check，把 py_compile/ruff 结果以「修复说明书」注入上下文。
业务关联：替代仅「建议跑 harness」的弱提示；错误即下一步动作。
上游：.cursor/hooks.json postToolUse
下游：Agent 下一轮；税则 FT-SENSOR-LINT
关联文档：.cursor/factoryos/HARNESS-EVAL.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from sensor_scoped_check import is_business_py, scoped_check  # noqa: E402


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

  norm = path.replace("\\", "/").lstrip("./")
  # 兼容绝对路径
  try:
    abs_p = Path(norm)
    if abs_p.is_absolute():
      norm = str(abs_p.resolve().relative_to(ROOT)).replace("\\", "/")
  except (ValueError, OSError):
    pass

  if not is_business_py(norm):
    # monorepo：转发 web-admin / 前端 App src 到 WEB 传感器
    if (
      norm.startswith("src/apps/")
      and "/src/" in norm
      and norm.endswith((".ts", ".tsx", ".js", ".jsx", ".mjs"))
    ):
      parts = norm.split("/")
      if len(parts) >= 3:
        app_scripts = ROOT / "src" / "apps" / parts[2] / "scripts"
        if (app_scripts / "web_sensor_scoped_check.py").is_file():
          sys.path.insert(0, str(app_scripts))
          from web_sensor_scoped_check import scoped_check as web_scoped  # noqa: E402

          _ok, msg = web_scoped(norm)
          if msg:
            print(json.dumps({"additional_context": msg}, ensure_ascii=False))
            return
    print("{}")
    return

  _ok, msg = scoped_check(norm)
  if not msg:
    print("{}")
    return
  print(json.dumps({"additional_context": msg}, ensure_ascii=False))


if __name__ == "__main__":
  main()
