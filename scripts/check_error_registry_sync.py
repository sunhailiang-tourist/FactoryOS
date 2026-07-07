#!/usr/bin/env python3
"""校验 error-registry SSOT 与 Python/TS mirror 一致（gate 硬门禁）。

Usage:
  python scripts/check_error_registry_sync.py

Exit 0 = pass; 1 = code 或 message_zh 漂移（须 sync --apply）。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from error_registry_lib import compute_drift, format_drift_report  # noqa: E402


def main() -> int:
  report = compute_drift()
  print(format_drift_report(report))
  if report.has_hard_fail():
    print("\nError registry mirror FAILED", file=sys.stderr)
    return 1
  if report.change_metadata:
    print("\nError registry mirror OK (metadata hints only)")
  else:
    print("\nError registry mirror OK")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
