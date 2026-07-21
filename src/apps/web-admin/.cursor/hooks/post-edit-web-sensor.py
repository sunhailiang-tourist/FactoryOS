#!/usr/bin/env python3
"""web-admin postToolUse：TS/TSX 传感器（迁出后用本 hooks.json）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(APP_ROOT / "scripts"))
from web_sensor_scoped_check import scoped_check  # noqa: E402


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
  if not norm.endswith((".ts", ".tsx", ".js", ".jsx", ".mjs")):
    print("{}")
    return
  _ok, msg = scoped_check(norm)
  if not msg:
    print("{}")
    return
  print(json.dumps({"additional_context": msg}, ensure_ascii=False))


if __name__ == "__main__":
  main()
