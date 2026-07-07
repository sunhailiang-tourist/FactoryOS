#!/usr/bin/env python3
"""校验 server 侧 Python 中文注释（编码绝对门禁 §3 · stdlib only）。

作用：机械拦截「无文件头 / 公开函数无业务注释」导致的文档债。
业务关联：SH-步步流 gate step · gate pr · check_static_quality。
上游：docs/文档/架构/编码绝对门禁.md §3
下游：check_static_quality.py · check_harness.py（step/full tier）

Usage:
  python scripts/check_python_comments.py
  python scripts/check_python_comments.py --paths src/server/os_core/connector_sdk

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENFORCED_MANIFEST = ROOT / "contracts" / "python_comment_enforced_paths.txt"
DEFAULT_ROOTS = (
  ROOT / "src" / "server" / "os_core",
  ROOT / "src" / "server" / "api",
)
SERVER_PREFIXES = ("src/server/os_core/", "src/server/api/")

FILE_HEADER_REQUIRED = ("作用", "业务关联", "上游", "下游")
FUNC_BUSINESS_MARKERS = ("功能", "业务", "业务含义")
FUNC_CHAIN_MARKERS = ("上游", "下游", "参数", "返回", "异常")

SKIP_PARTS = frozenset({"__pycache__", "migrations"})


def _read_module_doc(path: Path) -> str | None:
  try:
    text = path.read_text(encoding="utf-8")
  except OSError as exc:
    return f"__error__:{exc}"
  tree = ast.parse(text, filename=str(path))
  doc = ast.get_docstring(tree, clean=False)
  return doc


def _check_file_header(path: Path, doc: str | None) -> list[str]:
  errors: list[str] = []
  if doc is None or doc.startswith("__error__"):
    errors.append(f"{path}: missing module docstring (文件头)")
    return errors
  for tag in FILE_HEADER_REQUIRED:
    if tag not in doc:
      errors.append(f"{path}: file header missing 「{tag}」")
  if len(doc.strip()) < 40:
    errors.append(f"{path}: file header too short (<40 chars)")
  return errors


def _func_doc_ok(name: str, doc: str | None, body_len: int) -> list[str]:
  if doc is None or not doc.strip():
    if name.startswith("_") and body_len <= 3:
      return []
    return ["missing docstring"]
  text = doc.strip()
  if name.startswith("_"):
    if len(text) < 8:
      return ["private docstring too short (<8 chars)"]
    return []
  has_business = any(m in text for m in FUNC_BUSINESS_MARKERS)
  has_chain = any(m in text for m in FUNC_CHAIN_MARKERS)
  if not has_business:
    return ["public function doc missing 功能/业务/业务含义"]
  if not has_chain:
    return ["public function doc missing 上游/下游/参数/返回/异常"]
  if len(text) < 24:
    return ["public docstring too short (<24 chars)"]
  return []


def _check_functions(path: Path) -> list[str]:
  errors: list[str] = []
  try:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
  except SyntaxError as exc:
    return [f"{path}: syntax error: {exc}"]

  class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
      self.errors: list[str] = []
      self._depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
      self._visit_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
      self._visit_func(node)

    def _visit_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
      if self._depth > 0:
        return
      if node.name in ("main",):
        return
      body_len = len(node.body)
      doc = ast.get_docstring(node, clean=False)
      for msg in _func_doc_ok(node.name, doc, body_len):
        self.errors.append(f"{path}:{node.lineno}: {node.name} — {msg}")
      self._depth += 1
      for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
          continue
        self.visit(child)
      self._depth -= 1

  visitor = _Visitor()
  visitor.visit(tree)
  return visitor.errors


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


def check_files(files: list[Path]) -> list[str]:
  errors: list[str] = []
  for path in files:
    doc = _read_module_doc(path)
    if isinstance(doc, str) and doc.startswith("__error__"):
      errors.append(f"{path}: {doc}")
      continue
    errors.extend(_check_file_header(path, doc))
    errors.extend(_check_functions(path))
  return errors


def check_paths(roots: list[Path]) -> list[str]:
  return check_files(iter_py_files(roots))


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
  p = argparse.ArgumentParser(description="Python Chinese comment gate (server)")
  p.add_argument(
    "--paths",
    nargs="*",
    help="optional subpaths under repo root (default: os_core + api)",
  )
  p.add_argument(
    "--gate",
    action="store_true",
    help="enforced manifest + changed server .py (gate step / static quality)",
  )
  p.add_argument(
    "--changed-only",
    action="store_true",
    help="only git-changed server .py files",
  )
  args = p.parse_args()
  if args.gate:
    files = resolve_gate_files()
    if not files:
      print("Python comment gate OK (no enforced/changed server files)")
      return 0
    errors = check_files(files)
  elif args.changed_only:
    files = git_changed_server_py()
    if not files:
      print("Python comment gate OK (no changed server .py)")
      return 0
    errors = check_files(files)
  elif args.paths:
    roots = [(ROOT / rel).resolve() for rel in args.paths]
    errors = check_paths(roots)
  else:
    errors = check_paths(list(DEFAULT_ROOTS))
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
