#!/usr/bin/env python3
"""Fail if legacy duplicate paths still exist under src/ (reads contracts/repo-structure.yaml).

Usage:
  uv run python scripts/check_legacy_paths.py

Exit 0 = clean; 1 = legacy paths found.
"""
from __future__ import annotations

import sys

from repo_structure import load_snapshot, repo_root


def main() -> int:
  root = repo_root()
  snap = load_snapshot()
  found: list[str] = []
  for rel in snap.forbidden_dirs:
    if (root / rel).exists():
      found.append(rel)
  for rel in snap.forbidden_files:
    if (root / rel).exists():
      found.append(rel)
  if found:
    for rel in found:
      print(f"FAIL: legacy path still exists: {rel}", file=sys.stderr)
    return 1
  print("OK: no legacy paths (snapshot forbidden list clean)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
