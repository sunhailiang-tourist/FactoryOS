#!/usr/bin/env python3
"""Validate repo-structure.yaml ↔ disk ↔ kernel registry ↔ PATH-SNAPSHOT.md.

Usage:
  uv run python scripts/check_repo_structure.py

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import sys

from repo_structure import analyze_structure_drift, format_drift_report, load_snapshot


def main() -> int:
  snap = load_snapshot()
  report = analyze_structure_drift(snap)
  if not report.ok:
    for line in format_drift_report(report).splitlines():
      print(f"FAIL: {line}", file=sys.stderr)
    return 1

  print(
    f"OK: repo-structure snapshot aligned "
    f"(v{snap.version} · {snap.kernel_module_count} kernel modules · decision {snap.decision_ref})"
  )
  return 0


if __name__ == "__main__":
  sys.exit(main())
