#!/usr/bin/env python3
"""h5-worker DevKit harness — 阶段 2 脚手架门禁。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]


def _resolve_repo_root() -> Path:
  env = os.environ.get("FACTORYOS_ROOT")
  if env:
    return Path(env).resolve()
  current = APP_ROOT.resolve()
  while True:
    if (current / "devkit.manifest.yaml").is_file():
      return current
    if current.parent == current:
      break
    current = current.parent
  return APP_ROOT


REPO_ROOT = _resolve_repo_root()

def _resolve_scripts_dir() -> Path:
  local = APP_ROOT / "scripts"
  if (local / "devkit" / "frontend_contract_lib.py").is_file():
    return local
  env = os.environ.get("FACTORYOS_ROOT")
  if env:
    candidate = Path(env).resolve() / "scripts"
    if (candidate / "devkit" / "frontend_contract_lib.py").is_file():
      return candidate
  umbrella = REPO_ROOT / "scripts"
  if (umbrella / "devkit" / "frontend_contract_lib.py").is_file():
    return umbrella
  return local


SCRIPTS = _resolve_scripts_dir()

if str(SCRIPTS) not in sys.path:
  sys.path.insert(0, str(SCRIPTS))

from devkit.frontend_contract_lib import (  # noqa: E402
  HEADER_EXCLUDE_FILENAMES,
  REQUIRED_FILE_HEADER_LABELS,
  parse_file_header,
)

SRC = APP_ROOT / "src"
SCAN_SUFFIXES = {".ts", ".tsx"}


def _errors() -> list[str]:
  errors: list[str] = []
  for name in ("README.md", "ENGINEERING.md", "devkit.profile.yaml"):
    if not (APP_ROOT / name).is_file():
      errors.append(f"missing {name}")
  if SRC.is_dir():
    labels = " · ".join(REQUIRED_FILE_HEADER_LABELS)
    for path in sorted(SRC.rglob("*")):
      if path.suffix not in SCAN_SUFFIXES:
        continue
      if path.name in HEADER_EXCLUDE_FILENAMES:
        continue
      header, missing = parse_file_header(path.read_text(encoding="utf-8"))
      if header is None:
        errors.append(f"{path.relative_to(APP_ROOT)} missing file header ({labels})")
      elif missing and "FORBIDDEN_COMMENT_CLOSE" not in missing:
        errors.append(f"{path.relative_to(APP_ROOT)} file header missing: {', '.join(missing)}")
  return errors


def main() -> int:
  errors = _errors()
  if errors:
    print("h5-worker DevKit harness FAIL:", file=sys.stderr)
    for e in errors:
      print(f"  - {e}", file=sys.stderr)
    return 1
  print("OK: h5-worker DevKit harness (scaffold · file headers when src present)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
