#!/usr/bin/env python3
"""增量注释自动补齐（CMNT-C · 前端 App · 与 check_comments 同范围）。

Usage:
  python scripts/comment_fix.py --staged --dry-run
  python scripts/comment_fix.py --staged --apply
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = APP_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_fix_lib as cfl  # noqa: E402
import comment_gate_git as cgg  # noqa: E402
from check_comments import run_check  # noqa: E402


def main() -> int:
  p = argparse.ArgumentParser(description="Frontend comment autofix (CMNT-C)")
  g = p.add_mutually_exclusive_group(required=True)
  g.add_argument("--staged", action="store_true")
  g.add_argument("--changed", action="store_true")
  p.add_argument("--apply", action="store_true")
  args = p.parse_args()
  mode = "staged" if args.staged else "changed"
  rels = cgg.git_staged_relpaths() if mode == "staged" else cgg.git_changed_relpaths()
  ts = cgg.filter_gate_paths(rels)
  if not ts:
    print(f"comment_fix: no gate paths ({mode})")
    return 0
  if not args.apply:
    errors, _ = run_check(mode)
    print(f"comment_fix dry-run ({mode}: {len(ts)} ts)")
    print(f"  violations: {len(errors)} — run with --apply to patch")
    for e in errors[:15]:
      print(f"  {e}")
    return 0
  changed: list[str] = []
  for path in ts:
    if cfl.fix_ts_file(path):
      changed.append(path.relative_to(APP_ROOT).as_posix())
  for rel in changed:
    print("patched", rel)
  errors, ts_n = run_check(mode)
  print(f"\nafter fix ({mode}: {ts_n} ts), violations: {len(errors)}")
  for e in errors[:15]:
    print(f"  {e}")
  return 0 if not errors else 1


if __name__ == "__main__":
  sys.exit(main())
