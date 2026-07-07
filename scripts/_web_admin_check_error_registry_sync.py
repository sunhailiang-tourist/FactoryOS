#!/usr/bin/env python3
"""校验 vendor error-registry 与 error-codes.ts 一致（App 内硬门禁）。"""
from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT / "scripts"))

from error_registry_lib import compute_drift, format_drift_report


def main() -> int:
  report = compute_drift()
  print(format_drift_report(report))
  if report.has_hard_fail():
    print("\nError registry mirror FAILED", file=sys.stderr)
    return 1
  print("\nError registry mirror OK")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
