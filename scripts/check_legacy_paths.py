#!/usr/bin/env python3
"""Fail if legacy duplicate paths still exist under src/.

Usage:
  python scripts/check_legacy_paths.py

Exit 0 = clean; 1 = legacy paths found.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEGACY_PATHS = (
  "src/apps/api",
  "src/os_core",
  "src/db",
  "src/apps/edge-agent",
  "src/server/api/routes",
  "src/server/api/deps.py",
  "src/server/api/error_handlers.py",
)


def main() -> int:
  found = [rel for rel in LEGACY_PATHS if (ROOT / rel).exists()]
  if found:
    for rel in found:
      print(f"FAIL: legacy path still exists: {rel}", file=sys.stderr)
    return 1
  print("OK: no legacy paths under src/")
  return 0


if __name__ == "__main__":
  sys.exit(main())
