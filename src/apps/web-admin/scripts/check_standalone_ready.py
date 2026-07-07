#!/usr/bin/env python3
"""W-11 standalone 迁出前置自检 — vendor · 双路径 · simulate 脚本。

作用：迁出前最后一英里门禁子项。
业务关联：devkit.manifest.standalone.yaml · vendor/factoryos-contracts。
上游：contracts_paths · devkit.profile standalone_ready
下游：check_harness · simulate_standalone_activate.sh
"""
from __future__ import annotations

import sys
from pathlib import Path

from contracts_paths import (
  app_root_from_here,
  is_standalone_mode,
  resolve_openapi_path,
  vendor_contracts_root,
  vendor_openapi_path,
)

APP_ROOT = app_root_from_here(__file__)
PIN_FILE = vendor_contracts_root(APP_ROOT) / "PIN"
CODEGEN_CHECK = APP_ROOT / "scripts" / "check_codegen_fresh.py"
SIMULATE = APP_ROOT / "scripts" / "simulate_standalone_activate.sh"
STANDALONE_MANIFEST = APP_ROOT / "devkit.manifest.standalone.yaml"


def main() -> int:
  errors: list[str] = []

  if not STANDALONE_MANIFEST.is_file():
    errors.append("missing devkit.manifest.standalone.yaml")

  vendor_root = vendor_contracts_root(APP_ROOT)
  openapi_dir = vendor_root / "openapi"
  if not openapi_dir.is_dir():
    errors.append("missing vendor/factoryos-contracts/openapi/")
  elif not list(openapi_dir.glob("*.yaml")) and not list(openapi_dir.glob("*.yml")):
    errors.append("vendor/factoryos-contracts/openapi/ is empty")

  if not PIN_FILE.is_file() or not PIN_FILE.read_text(encoding="utf-8").strip():
    errors.append("vendor/factoryos-contracts/PIN unreadable")

  if not CODEGEN_CHECK.is_file():
    errors.append("missing scripts/check_codegen_fresh.py")
  else:
    text = CODEGEN_CHECK.read_text(encoding="utf-8")
    if "vendor" not in text or "factoryos-contracts" not in text:
      errors.append("check_codegen_fresh.py must reference vendor/factoryos-contracts")

  vendor_openapi = vendor_openapi_path(APP_ROOT)
  if not vendor_openapi.is_file():
    errors.append(f"missing vendor OpenAPI: {vendor_openapi.relative_to(APP_ROOT)}")

  if not (APP_ROOT / "scripts" / "run_codegen_api.py").is_file():
    errors.append("missing scripts/run_codegen_api.py")

  if not (APP_ROOT / "scripts" / "sync_error_registry.py").is_file():
    errors.append("missing scripts/sync_error_registry.py")

  if not (APP_ROOT / "scripts" / "py.sh").is_file():
    errors.append("missing scripts/py.sh")

  if not (APP_ROOT / "scripts" / "requirements.txt").is_file():
    errors.append("missing scripts/requirements.txt")

  if not (APP_ROOT / "scripts" / "check_error_registry_sync.py").is_file():
    errors.append("missing scripts/check_error_registry_sync.py")

  if not SIMULATE.is_file():
    errors.append("missing scripts/simulate_standalone_activate.sh")

  if errors:
    print("standalone_ready FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    return 1

  if is_standalone_mode(APP_ROOT):
    resolved = resolve_openapi_path(APP_ROOT)
    if "vendor" not in str(resolved):
      print(f"FAIL: standalone mode but OpenAPI resolved to {resolved}", file=sys.stderr)
      return 1

  print("OK: standalone_ready (vendor pin · codegen dual-path · simulate script)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
