#!/usr/bin/env python3
"""统一注释验收入口（CMNT-C · 前端 App · TypeScript）。

作用：commit 用 --staged；迁出仓 push 用 --full；本地可选 --changed。
业务关联：编码绝对门禁 §3 · contracts/comment-gate-spec.md。
上游：comment_gate_git · comment_gate_ts_lib · frontend_contract_lib
下游：pre-commit · check_harness.py（P0+ 子集）

Usage:
  python scripts/check_comments.py --staged
  python scripts/check_comments.py --changed
  python scripts/check_comments.py --full
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = APP_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_gate_git as cgg  # noqa: E402
from devkit.comment_gate_ts_lib import check_ts_file  # noqa: E402
from devkit.frontend_contract_lib import (  # noqa: E402
  HEADER_EXCLUDE_FILENAMES,
  REQUIRED_FILE_HEADER_LABELS,
  parse_file_header,
)


def _rel(path: Path) -> str:
  try:
    return path.relative_to(APP_ROOT).as_posix()
  except ValueError:
    return path.as_posix()



def _is_ts_app_rel(rel: str) -> bool:
  """App 内相对路径（--full 扫描用）。"""
  if not rel.endswith((".ts", ".tsx")) or not rel.startswith("src/"):
    return False
  posix = rel.replace("\\", "/")
  return not any(part in posix for part in cgg.TS_SKIP_PARTS)


def _check_ts_paths(paths: list[Path]) -> list[str]:
  errors: list[str] = []
  for path in paths:
    if path.name in HEADER_EXCLUDE_FILENAMES:
      continue
    try:
      text = path.read_text(encoding="utf-8")
    except OSError as exc:
      errors.append(f"{_rel(path)}: read error: {exc}")
      continue
    header, missing = parse_file_header(text)
    rel = _rel(path)
    if header is None:
      labels = " · ".join(REQUIRED_FILE_HEADER_LABELS)
      errors.append(f"{rel}: missing file header ({labels})")
    elif missing and "FORBIDDEN_COMMENT_CLOSE" not in missing:
      errors.append(f"{rel}: file header missing: {', '.join(missing)}")
    errors.extend(check_ts_file(path, text))
  return errors


def _collect_full_ts() -> list[Path]:
  root = cgg.ts_full_src_root()
  if not root.is_dir():
    return []
  paths: list[Path] = []
  for path in sorted(root.rglob("*")):
    if path.suffix not in (".ts", ".tsx"):
      continue
    rel = path.relative_to(APP_ROOT).as_posix()
    if _is_ts_app_rel(rel):
      paths.append(path)
  return paths


def run_check(mode: str) -> tuple[list[str], int]:
  """返回 (errors, ts_count)。"""
  if mode == "staged":
    ts = cgg.filter_gate_paths(cgg.git_staged_relpaths())
  elif mode == "changed":
    ts = cgg.filter_gate_paths(cgg.git_changed_relpaths())
  elif mode == "full":
    ts = _collect_full_ts()
  else:
    raise ValueError(mode)
  errors = _check_ts_paths(ts)
  return errors, len(ts)


def main() -> int:
  p = argparse.ArgumentParser(description="Frontend comment gate (CMNT-C)")
  g = p.add_mutually_exclusive_group(required=True)
  g.add_argument("--staged", action="store_true")
  g.add_argument("--changed", action="store_true")
  g.add_argument("--full", action="store_true")
  args = p.parse_args()
  mode = "staged" if args.staged else "changed" if args.changed else "full"
  errors, ts_n = run_check(mode)
  if not errors:
    print(f"Comment gate OK ({mode}: {ts_n} ts)")
    return 0
  print(f"Comment gate FAILED ({mode}: {ts_n} ts):", file=sys.stderr)
  for e in errors:
    print(f"  {e}", file=sys.stderr)
  print(
    f"\n{len(errors)} violation(s). See contracts/comment-gate-spec.md",
    file=sys.stderr,
  )
  return 1


if __name__ == "__main__":
  sys.exit(main())
