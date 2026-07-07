#!/usr/bin/env python3
"""Verify api/generated/openapi.d.ts matches contracts OpenAPI (W-01 · W-11 双路径).

作用：校验 generated 与 OpenAPI 同步。
业务关联：codegen:api · vendor/factoryos-contracts · umbrella contracts。
上游：contracts_paths.resolve_openapi_path
下游：check_harness · pnpm codegen:check
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from contracts_paths import app_root_from_here, resolve_openapi_path, vendor_openapi_path

APP_ROOT = app_root_from_here(__file__)
GENERATED = APP_ROOT / "src" / "api" / "generated" / "openapi.d.ts"


def _run_codegen(openapi: Path, out_path: Path) -> None:
  cmd = [
    "pnpm",
    "exec",
    "openapi-typescript",
    str(openapi.resolve()),
    "-o",
    str(out_path),
  ]
  result = subprocess.run(cmd, cwd=APP_ROOT, capture_output=True, text=True)
  if result.returncode != 0:
    print(result.stdout, file=sys.stderr)
    print(result.stderr, file=sys.stderr)
    raise SystemExit(f"codegen failed: exit {result.returncode}")


def main() -> int:
  openapi = resolve_openapi_path(APP_ROOT)
  if not openapi.is_file():
    vendor_hint = vendor_openapi_path(APP_ROOT)
    print(
      f"FAIL: OpenAPI not found: {openapi.resolve()} "
      f"(vendor mirror: {vendor_hint})",
      file=sys.stderr,
    )
    return 1
  if not GENERATED.is_file():
    print(f"FAIL: missing {GENERATED.relative_to(APP_ROOT)} — run pnpm codegen:api", file=sys.stderr)
    return 1

  with tempfile.NamedTemporaryFile(suffix=".d.ts", delete=False) as tmp:
    tmp_path = Path(tmp.name)
  try:
    _run_codegen(openapi, tmp_path)
    expected = tmp_path.read_text(encoding="utf-8")
  finally:
    tmp_path.unlink(missing_ok=True)

  actual = GENERATED.read_text(encoding="utf-8")
  if actual != expected:
    print(
      "FAIL: api/generated/openapi.d.ts is stale — run `pnpm codegen:api` and commit",
      file=sys.stderr,
    )
    return 1

  try:
    label = str(openapi.relative_to(APP_ROOT))
  except ValueError:
    label = str(openapi)
  print(f"OK: openapi codegen fresh ({label})")
  return 0


if __name__ == "__main__":
  sys.exit(main())
