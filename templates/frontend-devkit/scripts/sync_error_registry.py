#!/usr/bin/env python3
"""vendor error-registry → error-codes.ts（standalone 自给）。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT / "scripts"))

from error_registry_lib import (
  TS_CODES_PATH,
  compute_drift,
  format_drift_report,
  load_registry,
  render_typescript_module,
)


def main() -> int:
  parser = argparse.ArgumentParser(description="Sync vendor error-registry → error-codes.ts")
  parser.add_argument("--apply", action="store_true")
  args = parser.parse_args()
  report = compute_drift()
  print(format_drift_report(report))
  if not report.has_hard_fail():
    print("\nNothing to sync.")
    return 0
  _, entries = load_registry()
  mode = "APPLY" if args.apply else "DRY-RUN"
  print(f"\n── sync ({mode}) ──")
  content = render_typescript_module(entries)
  if args.apply:
    TS_CODES_PATH.write_text(content, encoding="utf-8")
    print(f"  wrote {TS_CODES_PATH.relative_to(APP_ROOT)}")
    print("\nSync complete. 运行: python scripts/check_error_registry_sync.py")
  else:
    print(f"  would update {TS_CODES_PATH.relative_to(APP_ROOT)}")
    print("\n未写盘。确认后: python scripts/sync_error_registry.py --apply")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
