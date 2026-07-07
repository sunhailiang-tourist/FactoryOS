#!/usr/bin/env python3
"""将 SSOT mirror 标记同步到 errors.py · error-codes.ts（须人工确认后 --apply）。

Usage:
  python scripts/sync_error_registry.py          # dry-run（默认）
  python scripts/sync_error_registry.py --apply  # 写盘（负责人确认后）

同步内容：ErrorCode / ERROR_CODES + ERROR_MESSAGE_ZH / ERROR_MESSAGES_ZH + helpers。
禁止 Agent 在未获明确确认时执行 --apply。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from error_registry_lib import (  # noqa: E402
  PYTHON_ENUM_PATH,
  TS_CODES_PATH,
  compute_drift,
  format_drift_report,
  load_registry,
  render_python_module,
  render_typescript_module,
)


def main() -> int:
  parser = argparse.ArgumentParser(description="Sync error registry mirrors from SSOT")
  parser.add_argument(
    "--apply",
    action="store_true",
    help="写盘（须负责人确认；默认 dry-run）",
  )
  args = parser.parse_args()

  report = compute_drift()
  print(format_drift_report(report))
  if not report.has_hard_fail():
    if report.change_metadata:
      print("\nNothing to sync (metadata hints only).")
    else:
      print("\nNothing to sync.")
    return 0

  _, entries = load_registry()
  mode = "APPLY" if args.apply else "DRY-RUN"
  print(f"\n── sync ({mode}) ──")

  py_content = render_python_module(entries)
  ts_content = render_typescript_module(entries)

  if args.apply:
    PYTHON_ENUM_PATH.parent.mkdir(parents=True, exist_ok=True)
    PYTHON_ENUM_PATH.write_text(py_content, encoding="utf-8")
    print(f"  wrote {PYTHON_ENUM_PATH.relative_to(ROOT)}")
    TS_CODES_PATH.parent.mkdir(parents=True, exist_ok=True)
    TS_CODES_PATH.write_text(ts_content, encoding="utf-8")
    print(f"  wrote {TS_CODES_PATH.relative_to(ROOT)}")
    print("\nSync complete. 请运行: python scripts/check_error_registry_sync.py")
  else:
    print(f"  would update {PYTHON_ENUM_PATH.relative_to(ROOT)}")
    print(f"  would update {TS_CODES_PATH.relative_to(ROOT)}")
    print("\n未写盘。确认后执行: python scripts/sync_error_registry.py --apply")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
