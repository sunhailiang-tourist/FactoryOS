"""Python 注释门禁共享逻辑（编码绝对门禁 §3 · P0～P3）。

作用：供 check_python_comments.py 与单元测试复用。
业务关联：1a.5 闭合后 P1～P3 硬化。
上游：docs/文档/架构/编码绝对门禁.md §3.3～3.5
下游：check_python_comments.py · gate pr
"""
from __future__ import annotations

import ast
import re
import tokenize
from io import BytesIO
from pathlib import Path
from typing import Iterable

FILE_HEADER_REQUIRED = ("作用", "业务关联", "上游", "下游")
FUNC_BUSINESS_MARKERS = ("功能", "业务", "业务含义")
FUNC_CHAIN_MARKERS = ("上游", "下游", "参数", "返回", "异常")
PLATFORM_ERROR_DOC_MARKERS = ("异常", "ErrorCode", "PlatformError", "错误码")

# §3.5 复杂逻辑块：可执行语句 ≥ 此值须有块注释（# 行）
BLOCK_COMMENT_MIN_STMTS = 10
FIELD_DESC_MIN_LEN = 2

_SKIP_FIELD_NAMES = frozenset({"model_config"})


def _is_basemodel_class(node: ast.ClassDef) -> bool:
  for base in node.bases:
    if isinstance(base, ast.Name) and base.id == "BaseModel":
      return True
    if isinstance(base, ast.Attribute) and base.attr == "BaseModel":
      return True
  return False


def _field_description_ok(node: ast.AnnAssign) -> bool:
  if not isinstance(node.target, ast.Name):
    return True
  if node.target.id in _SKIP_FIELD_NAMES:
    return True
  val = node.value
  if val is None:
    return False
  if not isinstance(val, ast.Call):
    return False
  func = val.func
  is_field = (isinstance(func, ast.Name) and func.id == "Field") or (
    isinstance(func, ast.Attribute) and func.attr == "Field"
  )
  if not is_field:
    return False
  for kw in val.keywords:
    if kw.arg == "description" and isinstance(kw.value, ast.Constant):
      desc = kw.value.value
      if isinstance(desc, str) and len(desc.strip()) >= FIELD_DESC_MIN_LEN:
        return True
  return False


def _count_executable_stmts(body: list[ast.stmt]) -> int:
  """统计函数体可执行语句数（不含 docstring 与 pass-only）。"""
  count = 0
  for stmt in body:
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
      if isinstance(stmt.value.value, str):
        continue
    if isinstance(stmt, ast.Pass):
      continue
    count += 1
  return count


def _body_has_line_comment(source: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
  """函数体行范围内是否存在有意义的 # 块注释。"""
  if not node.body:
    return False
  start = node.lineno
  end = max(getattr(n, "end_lineno", n.lineno) for n in ast.walk(node) if hasattr(n, "lineno"))
  lines = source.splitlines()
  for i in range(start - 1, min(end, len(lines))):
    line = lines[i].strip()
    if line.startswith("#") and len(line) > 2:
      # 排除 shebang/encoding；要求含中文或 ≥8 字符说明
      payload = line.lstrip("#").strip()
      if len(payload) >= 8 or re.search(r"[\u4e00-\u9fff]", payload):
        return True
  return False


def _raises_platform_error(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
  for child in ast.walk(node):
    if not isinstance(child, ast.Raise):
      continue
    exc = child.exc
    if exc is None:
      continue
    if isinstance(exc, ast.Call):
      fn = exc.func
      if isinstance(fn, ast.Name) and fn.id == "PlatformError":
        return True
      if isinstance(fn, ast.Attribute) and fn.attr == "PlatformError":
        return True
  return False


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


def check_file_header(path: Path, doc: str | None) -> list[str]:
  errors: list[str] = []
  if doc is None or (isinstance(doc, str) and doc.startswith("__error__")):
    errors.append(f"{path}: missing module docstring (文件头)")
    return errors
  for tag in FILE_HEADER_REQUIRED:
    if tag not in doc:
      errors.append(f"{path}: file header missing 「{tag}」")
  if len(doc.strip()) < 40:
    errors.append(f"{path}: file header too short (<40 chars)")
  return errors


def check_file_rules(
  path: Path,
  *,
  check_fields: bool = True,
  check_blocks: bool = True,
  check_platform_error: bool = True,
) -> list[str]:
  """对单文件执行 P0～P3 注释规则。"""
  errors: list[str] = []
  try:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
  except SyntaxError as exc:
    return [f"{path}: syntax error: {exc}"]

  doc = ast.get_docstring(tree, clean=False)
  errors.extend(check_file_header(path, doc))

  class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
      self.errors: list[str] = []
      self._func_depth = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
      if check_fields and _is_basemodel_class(node):
        for item in node.body:
          if isinstance(item, ast.AnnAssign):
            if not _field_description_ok(item):
              name = item.target.id if isinstance(item.target, ast.Name) else "?"
              self.errors.append(
                f"{path}:{item.lineno}: {node.name}.{name} — "
                "Pydantic field missing Field(description=...)"
              )
      self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
      self._visit_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
      self._visit_func(node)

    def _visit_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
      if self._func_depth > 0:
        return
      if node.name == "main":
        return
      body_len = len(node.body)
      fdoc = ast.get_docstring(node, clean=False)
      for msg in _func_doc_ok(node.name, fdoc, body_len):
        self.errors.append(f"{path}:{node.lineno}: {node.name} — {msg}")

      if check_platform_error and not node.name.startswith("_"):
        if _raises_platform_error(node) and fdoc:
          if not any(m in fdoc for m in PLATFORM_ERROR_DOC_MARKERS):
            self.errors.append(
              f"{path}:{node.lineno}: {node.name} — "
              "raises PlatformError but doc missing 异常/ErrorCode/PlatformError"
            )
        elif _raises_platform_error(node) and not fdoc:
          self.errors.append(
            f"{path}:{node.lineno}: {node.name} — "
            "raises PlatformError but missing doc with 异常"
          )

      if check_blocks:
        stmt_count = _count_executable_stmts(node.body)
        if stmt_count >= BLOCK_COMMENT_MIN_STMTS and not _body_has_line_comment(text, node):
          self.errors.append(
            f"{path}:{node.lineno}: {node.name} — "
            f"complex body ({stmt_count} stmts) missing block comment (# …)"
          )

      self._func_depth += 1
      for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
          continue
        self.visit(child)
      self._func_depth -= 1

  v = _Visitor()
  v.visit(tree)
  errors.extend(v.errors)
  return errors


def check_files(
  files: Iterable[Path],
  *,
  check_fields: bool = True,
  check_blocks: bool = True,
  check_platform_error: bool = True,
) -> list[str]:
  out: list[str] = []
  for path in files:
    out.extend(
      check_file_rules(
        path,
        check_fields=check_fields,
        check_blocks=check_blocks,
        check_platform_error=check_platform_error,
      )
    )
  return out
