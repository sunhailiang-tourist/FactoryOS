#!/usr/bin/env python3
"""Validate integration/registry.py ↔ on-disk mounts.

Usage:
  python scripts/check_integration_registry.py

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from integration.registry import validate_integration_mounts  # noqa: E402


def main() -> int:
  errors = validate_integration_mounts()
  if errors:
    for err in errors:
      print(f"FAIL: {err}", file=sys.stderr)
    return 1
  print("OK: integration registry aligned")
  return 0


if __name__ == "__main__":
  sys.exit(main())
