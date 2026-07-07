#!/usr/bin/env python3
"""OpenAPI → api/generated（umbrella / vendor 双路径 · standalone 自给）。

作用：pnpm codegen:api 真源；与 check_codegen_fresh 同路径解析。
业务关联：vendor/factoryos-contracts · contracts_paths。
上游：devkit.manifest.yaml · WEB_PROFILE_STANDALONE
下游：src/api/generated/openapi.d.ts
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from contracts_paths import app_root_from_here, resolve_openapi_path

APP_ROOT = app_root_from_here(__file__)
GENERATED = APP_ROOT / "src" / "api" / "generated" / "openapi.d.ts"


def main() -> int:
  openapi = resolve_openapi_path(APP_ROOT)
  if not openapi.is_file():
    print(f"FAIL: OpenAPI not found: {openapi.resolve()}", file=sys.stderr)
    return 1
  GENERATED.parent.mkdir(parents=True, exist_ok=True)
  cmd = [
    "pnpm",
    "exec",
    "openapi-typescript",
    str(openapi.resolve()),
    "-o",
    str(GENERATED),
  ]
  result = subprocess.run(cmd, cwd=APP_ROOT)
  if result.returncode == 0:
    try:
      label = str(openapi.relative_to(APP_ROOT))
    except ValueError:
      label = str(openapi)
    print(f"OK: codegen → {GENERATED.relative_to(APP_ROOT)} ({label})")
  return result.returncode


if __name__ == "__main__":
  sys.exit(main())
