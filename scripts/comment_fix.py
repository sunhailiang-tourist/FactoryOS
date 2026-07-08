#!/usr/bin/env python3
"""增量注释自动补齐（CMNT-C · 与 check_comments 同范围）。

作用：提交前为 staged 文件补注释骨架（不覆盖合格注释）。
业务关联：双速双严策略 · comment_fix → check_comments --staged。
上游：comment_gate_git · comment_fix_lib
下游：开发者 commit 前 · Agent 落盘后

Usage:
  uv run python scripts/comment_fix.py --staged --dry-run
  uv run python scripts/comment_fix.py --staged --apply
  uv run python scripts/comment_fix.py --changed --apply

Exit 0 = OK; 1 = 无 staged 文件或 apply 后仍有违规。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_fix_lib as cfl  # noqa: E402
import comment_gate_git as cgg  # noqa: E402
from check_comments import run_check  # noqa: E402


def _resolve_paths(mode: str) -> tuple[list[Path], list[Path]]:
  rels = cgg.git_staged_relpaths() if mode == "staged" else cgg.git_changed_relpaths()
  return cgg.filter_gate_paths(rels)


def _fix_paths(py: list[Path], ts: list[Path], *, apply: bool) -> list[str]:
  changed: list[str] = []
  for path in [*py, *ts]:
    would = (
      cfl.fix_python_file(path) if path.suffix == ".py" else cfl.fix_ts_file(path)
    )
    if not would:
      continue
    rel = path.relative_to(ROOT).as_posix()
    if apply:
      changed.append(rel)
    else:
      changed.append(f"{rel} (dry-run)")
  return changed


def main() -> int:
  p = argparse.ArgumentParser(description="Comment autofix (CMNT-C)")
  g = p.add_mutually_exclusive_group(required=True)
  g.add_argument("--staged", action="store_true")
  g.add_argument("--changed", action="store_true")
  p.add_argument("--apply", action="store_true", help="write files (default dry-run)")
  p.add_argument("--dry-run", action="store_true", help="only report (default)")
  args = p.parse_args()

  apply = args.apply
  mode = "staged" if args.staged else "changed"
  py, ts = _resolve_paths(mode)
  if not py and not ts:
    print(f"comment_fix: no gate paths ({mode})")
    return 0

  if not apply:
    errors, _, _ = run_check(mode)
    print(f"comment_fix dry-run ({mode}: {len(py)} py, {len(ts)} ts)")
    print(f"  violations: {len(errors)} — run with --apply to patch")
    for e in errors[:15]:
      print(f"  {e}")
    return 0

  changed = _fix_paths(py, ts, apply=True)
  for rel in changed:
    print("patched", rel)

  check_mode = "staged" if mode == "staged" else "changed"
  errors, py_n, ts_n = run_check(check_mode)
  print(f"\nafter fix ({check_mode}: {py_n} py, {ts_n} ts), violations: {len(errors)}")
  for e in errors[:15]:
    print(f"  {e}")
  return 0 if not errors else 1


if __name__ == "__main__":
  sys.exit(main())
