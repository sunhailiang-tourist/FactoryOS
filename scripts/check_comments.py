#!/usr/bin/env python3
"""统一注释验收入口（CMNT-C · 双速双严）。

作用：commit 用 --staged；PR 用 --full；本地可选 --changed。
业务关联：编码绝对门禁 §3 · comment-gate-spec v2。
上游：comment_gate_lib · comment_gate_ts_lib · comment_gate_git
下游：pre-commit · check_static_quality · gate pr

Usage:
  python scripts/check_comments.py --staged
  python scripts/check_comments.py --changed
  python scripts/check_comments.py --full

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_gate_git as cgg  # noqa: E402
import comment_gate_lib as cg  # noqa: E402
from devkit.comment_gate_ts_lib import check_ts_file  # noqa: E402
from devkit.frontend_contract_lib import (  # noqa: E402
  HEADER_EXCLUDE_FILENAMES,
  REQUIRED_FILE_HEADER_LABELS,
  parse_file_header,
)


def _check_ts_paths(paths: list[Path]) -> list[str]:
  errors: list[str] = []
  for path in paths:
    if path.name in HEADER_EXCLUDE_FILENAMES:
      continue
    try:
      text = path.read_text(encoding="utf-8")
    except OSError as exc:
      errors.append(f"{path}: read error: {exc}")
      continue
    header, missing = parse_file_header(text)
    try:
      rel = path.relative_to(cgg.ROOT).as_posix()
    except ValueError:
      rel = path.as_posix()
    if header is None:
      labels = " · ".join(REQUIRED_FILE_HEADER_LABELS)
      errors.append(f"{rel}: missing file header ({labels})")
    elif missing and "FORBIDDEN_COMMENT_CLOSE" not in missing:
      errors.append(f"{rel}: file header missing: {', '.join(missing)}")
    errors.extend(check_ts_file(path, text))
  return errors


def _check_python_paths(
  paths: list[Path],
  *,
  check_fields: bool,
  check_blocks: bool,
  check_platform_error: bool,
) -> list[str]:
  if not paths:
    return []
  rel_errors: list[str] = []
  root_prefix = str(cgg.ROOT).rstrip("/") + "/"
  for err in cg.check_files(
    paths,
    check_fields=check_fields,
    check_blocks=check_blocks,
    check_platform_error=check_platform_error,
  ):
    if err.startswith(root_prefix):
      rel_errors.append(err[len(root_prefix) :])
    else:
      rel_errors.append(err)
  return rel_errors


def _collect_full_python() -> list[Path]:
  out: list[Path] = []
  skip = frozenset({"__pycache__", "migrations"})
  for base in cgg.python_full_roots():
    if not base.is_dir():
      continue
    for py in base.rglob("*.py"):
      if any(part in skip for part in py.parts):
        continue
      out.append(py)
  return sorted(out)


def _collect_full_ts_apps() -> list[Path]:
  paths: list[Path] = []
  for app in cgg.ts_full_app_roots():
    src = app / "src"
    for path in sorted(src.rglob("*")):
      if path.suffix not in (".ts", ".tsx"):
        continue
      rel = path.relative_to(ROOT).as_posix()
      if cgg._is_ts_gate_path(rel):
        paths.append(path)
  return paths


def run_check(
  mode: str,
  *,
  check_fields: bool = True,
  check_blocks: bool = True,
  check_platform_error: bool = True,
) -> tuple[list[str], int, int]:
  """返回 (errors, py_count, ts_count)。"""
  if mode == "staged":
    py, ts = cgg.filter_gate_paths(cgg.git_staged_relpaths())
  elif mode == "changed":
    py, ts = cgg.filter_gate_paths(cgg.git_changed_relpaths())
  elif mode == "full":
    py = _collect_full_python()
    ts = _collect_full_ts_apps()
  else:
    raise ValueError(mode)

  errors: list[str] = []
  errors.extend(
    _check_python_paths(
      py,
      check_fields=check_fields,
      check_blocks=check_blocks,
      check_platform_error=check_platform_error,
    )
  )
  errors.extend(_check_ts_paths(ts))
  return errors, len(py), len(ts)


def main() -> int:
  p = argparse.ArgumentParser(description="Unified comment gate (CMNT-C)")
  g = p.add_mutually_exclusive_group(required=True)
  g.add_argument("--staged", action="store_true", help="only git cached (pre-commit)")
  g.add_argument("--changed", action="store_true", help="working tree changes")
  g.add_argument("--full", action="store_true", help="full server + frontend apps")
  p.add_argument("--no-fields", action="store_true")
  p.add_argument("--no-blocks", action="store_true")
  p.add_argument("--no-platform-error", action="store_true")
  args = p.parse_args()

  mode = "staged" if args.staged else "changed" if args.changed else "full"
  errors, py_n, ts_n = run_check(
    mode,
    check_fields=not args.no_fields,
    check_blocks=not args.no_blocks,
    check_platform_error=not args.no_platform_error,
  )

  if not errors:
    print(f"Comment gate OK ({mode}: {py_n} py, {ts_n} ts)")
    return 0

  print(f"Comment gate FAILED ({mode}: {py_n} py, {ts_n} ts):", file=sys.stderr)
  for e in errors:
    print(f"  {e}", file=sys.stderr)
  print(
    f"\n{len(errors)} violation(s). See contracts/comment-gate-spec.md",
    file=sys.stderr,
  )
  return 1


if __name__ == "__main__":
  sys.exit(main())
