#!/usr/bin/env python3
"""校验 server 侧 Python 中文注释（编码绝对门禁 §3 · P0～P3 · stdlib only）。

作用：机械拦截文件头/函数/字段/块注释/PlatformError doc 债。
业务关联：SH-步步流 gate step · gate pr · check_static_quality。
上游：docs/文档/架构/编码绝对门禁.md §3
下游：check_static_quality.py · check_harness.py（step/full tier）

Usage:
  python scripts/check_python_comments.py
  python scripts/check_python_comments.py --paths src/server/os_core/connector_sdk
  python scripts/check_python_comments.py --no-fields   # 仅 P0～P2 子集调试

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import comment_gate_lib as cg  # noqa: E402

ENFORCED_MANIFEST = ROOT / "contracts" / "python_comment_enforced_paths.txt"
DEFAULT_ROOTS = (
  ROOT / "src" / "server" / "os_core",
  ROOT / "src" / "server" / "api",
)
SERVER_PREFIXES = ("src/server/os_core/", "src/server/api/")

SKIP_PARTS = frozenset({"__pycache__", "migrations"})


def _read_module_doc(path: Path) -> str | None:
  try:
    text = path.read_text(encoding="utf-8")
  except OSError as exc:
    return f"__error__:{exc}"
  tree = ast.parse(text, filename=str(path))
  return ast.get_docstring(tree, clean=False)


def load_enforced_paths() -> list[Path]:
  """读取 contracts/python_comment_enforced_paths.txt。"""
  if not ENFORCED_MANIFEST.is_file():
    return []
  paths: list[Path] = []
  for line in ENFORCED_MANIFEST.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
      continue
    paths.append((ROOT / line).resolve())
  return paths


def git_changed_server_py() -> list[Path]:
  """Staged + unstaged + untracked 下 server 侧 .py。"""
  import subprocess

  rels: set[str] = set()
  for cmd in (
    ["git", "diff", "--name-only", "HEAD"],
    ["git", "diff", "--name-only", "--cached"],
    ["git", "ls-files", "--others", "--exclude-standard"],
  ):
    try:
      r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    except OSError:
      continue
    if r.returncode != 0:
      continue
    for line in r.stdout.splitlines():
      norm = line.strip().replace("\\", "/")
      if norm.endswith(".py") and any(norm.startswith(p) for p in SERVER_PREFIXES):
        rels.add(norm)
  return sorted((ROOT / rel).resolve() for rel in rels)


def iter_py_files(roots: list[Path]) -> list[Path]:
  out: list[Path] = []
  for base in roots:
    if not base.is_dir():
      continue
    for py in base.rglob("*.py"):
      if any(part in SKIP_PARTS for part in py.parts):
        continue
      out.append(py)
  return sorted(out)


def check_files_list(
  files: list[Path],
  *,
  check_fields: bool,
  check_blocks: bool,
  check_platform_error: bool,
) -> list[str]:
  errors: list[str] = []
  for path in files:
    doc = _read_module_doc(path)
    if isinstance(doc, str) and doc.startswith("__error__"):
      errors.append(f"{path}: {doc}")
      continue
    errors.extend(
      cg.check_file_rules(
        path,
        check_fields=check_fields,
        check_blocks=check_blocks,
        check_platform_error=check_platform_error,
      )
    )
  return errors


def check_paths(
  roots: list[Path],
  *,
  check_fields: bool,
  check_blocks: bool,
  check_platform_error: bool,
) -> list[str]:
  return check_files_list(
    iter_py_files(roots),
    check_fields=check_fields,
    check_blocks=check_blocks,
    check_platform_error=check_platform_error,
  )


def resolve_gate_files() -> list[Path]:
  """强制路径 + git 改动 server .py（去重）。"""
  seen: set[Path] = set()
  out: list[Path] = []
  for path in [*load_enforced_paths(), *git_changed_server_py()]:
    if path.is_file() and path not in seen:
      seen.add(path)
      out.append(path)
  return sorted(out)


def main() -> int:
  p = argparse.ArgumentParser(description="Python Chinese comment gate (server P0～P3)")
  p.add_argument("--paths", nargs="*", help="optional subpaths under repo root")
  p.add_argument("--gate", action="store_true", help="enforced + changed server .py")
  p.add_argument("--changed-only", action="store_true")
  p.add_argument("--no-fields", action="store_true", help="skip P1 field description")
  p.add_argument("--no-blocks", action="store_true", help="skip P2 block comments")
  p.add_argument("--no-platform-error", action="store_true", help="skip P3 PlatformError doc")
  args = p.parse_args()

  opts = dict(
    check_fields=not args.no_fields,
    check_blocks=not args.no_blocks,
    check_platform_error=not args.no_platform_error,
  )

  if args.gate:
    files = resolve_gate_files()
    if not files:
      print("Python comment gate OK (no enforced/changed server files)")
      return 0
    errors = check_files_list(files, **opts)
  elif args.changed_only:
    files = git_changed_server_py()
    if not files:
      print("Python comment gate OK (no changed server .py)")
      return 0
    errors = check_files_list(files, **opts)
  elif args.paths:
    roots = [(ROOT / rel).resolve() for rel in args.paths]
    errors = check_paths(roots, **opts)
  else:
    errors = check_paths(list(DEFAULT_ROOTS), **opts)

  if errors:
    print("Python comment gate FAILED:", file=sys.stderr)
    for e in errors:
      print(f"  {e}", file=sys.stderr)
    print(
      f"\n{len(errors)} violation(s). See docs/文档/架构/编码绝对门禁.md §3",
      file=sys.stderr,
    )
    return 1
  print("Python comment gate OK")
  return 0


if __name__ == "__main__":
  sys.exit(main())
