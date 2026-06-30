#!/usr/bin/env python3
"""Validate registry entries carry human-readable annotations (stdlib only).

Usage:
  python scripts/check_registry_annotations.py

Exit 0 = pass; 1 = missing summary/problem/usage on registry entries.
"""
from __future__ import annotations

import sys

from registry_annotation_lib import validate_all


def main() -> int:
  errors = validate_all()
  if errors:
    print("Registry annotation violations:", file=sys.stderr)
    for err in errors:
      print(f"  {err}", file=sys.stderr)
    return 1
  print("Registry annotations OK")
  return 0


if __name__ == "__main__":
  sys.exit(main())
