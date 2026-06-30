#!/usr/bin/env python3
"""注册表注释/元数据校验 — 供 check_registry_annotations 与 harness 复用。

规则：凡集中登记模块/路由/挂载/导入边界的注册表，每条须可读说明：
  - summary（是什么）
  - problem（解决什么问题）
  - usage（怎么用 / 入口）
dataclass 注册表用字段；dict/tuple 注册表用紧邻上一行 # 注释（≥20 字）。
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

MIN_TEXT_LEN = 8
REGISTRY_COMMENT_RE = re.compile(
    r"[\u4e00-\u9fff].{7,}|# .*(职责|解决|用法|路由|内核|导入|挂载|AC|middleware)"
)


@dataclass(frozen=True, slots=True)
class RegistrySpec:
  """单份注册表文件校验规格。"""

  rel_path: str
  assign_names: tuple[str, ...]
  kind: str  # dataclass_call | tuple_attr | dict_key | yaml_list


def registry_specs() -> tuple[RegistrySpec, ...]:
  return (
    RegistrySpec("src/server/os_core/registry.py", ("KERNEL_MODULES",), "dataclass_call"),
    RegistrySpec(
      "src/server/api/router/v1/registry.py",
      ("API_ROUTER_DOMAINS",),
      "dataclass_call",
    ),
    RegistrySpec(
      "src/integration/registry.py",
      ("INTEGRATION_MOUNTS",),
      "dataclass_call",
    ),
    RegistrySpec(
      "scripts/check_import_boundaries.py",
      ("IMPORT_BOUNDARY_REGISTRY",),
      "dataclass_call",
    ),
    RegistrySpec(
      "src/server/api/config/middleware/registry.py",
      ("MIDDLEWARE_STACK",),
      "dataclass_call",
    ),
  )


REQUIRED_KW = ("summary", "problem", "usage")


def _kw_map(call: ast.Call) -> dict[str, ast.expr]:
  out: dict[str, ast.expr] = {}
  for kw in call.keywords:
    if kw.arg:
      out[kw.arg] = kw.value
  return out


def _const_str(node: ast.expr) -> str | None:
  if isinstance(node, ast.Constant) and isinstance(node.value, str):
    return node.value
  return None


def _validate_dataclass_calls(
  path: Path,
  assign_name: str,
  *,
  required_keywords: tuple[str, ...] = REQUIRED_KW,
) -> list[str]:
  errors: list[str] = []
  try:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
  except SyntaxError as exc:
    return [f"{path}: syntax error: {exc}"]

  tuple_node: ast.Tuple | None = None
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name) and target.id == assign_name:
          if isinstance(node.value, ast.Tuple):
            tuple_node = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
      if node.target.id == assign_name and isinstance(node.value, ast.Tuple):
        tuple_node = node.value

  if tuple_node is None:
    return [f"{path}: missing assignment {assign_name}"]

  for i, elt in enumerate(tuple_node.elts):
    if not isinstance(elt, ast.Call):
      errors.append(f"{path}: {assign_name}[{i}] must be a dataclass constructor call")
      continue
    kws = _kw_map(elt)
    name = _const_str(kws.get("name", ast.Constant(value=f"#{i}"))) or f"#{i}"
    package = _const_str(kws.get("package", ast.Constant(value=""))) or name
    label = name or package
    for key in required_keywords:
      text = _const_str(kws.get(key, ast.Constant(value="")))
      if not text or len(text.strip()) < MIN_TEXT_LEN:
        errors.append(
          f"{path}: {assign_name} entry {label!r} missing or short {key!r} "
          f"(≥{MIN_TEXT_LEN} chars, 中文说明职责/问题/用法)"
        )
  return errors


def _line_comment_before(lines: list[str], idx: int) -> str | None:
  j = idx - 1
  while j >= 0 and not lines[j].strip():
    j -= 1
  if j < 0:
    return None
  stripped = lines[j].strip()
  if stripped.startswith("#"):
    return stripped
  return None


def validate_all() -> list[str]:
  errors: list[str] = []
  for spec in registry_specs():
    path = ROOT / spec.rel_path
    if not path.is_file():
      errors.append(f"missing registry file: {spec.rel_path}")
      continue
    if spec.kind == "dataclass_call":
      for name in spec.assign_names:
        errors.extend(_validate_dataclass_calls(path, name))
  errors.extend(_validate_repo_structure_kernel_comments())
  return errors


def _validate_repo_structure_kernel_comments() -> list[str]:
  path = ROOT / "contracts" / "repo-structure.yaml"
  if not path.is_file():
    return [f"missing {path.relative_to(ROOT)}"]
  errors: list[str] = []
  lines = path.read_text(encoding="utf-8").splitlines()
  in_modules = False
  for i, line in enumerate(lines):
    if re.match(r"^\s*modules:\s*$", line):
      in_modules = True
      continue
    if in_modules:
      if re.match(r"^\S", line) and not line.startswith(" "):
        break
      m = re.match(r"^\s+-\s+(\w+)\s*(#.*)?$", line)
      if not m:
        continue
      mod, comment = m.group(1), m.group(2)
      if not comment or len(comment) < MIN_TEXT_LEN + 2:
        errors.append(
          f"{path}:{i + 1}: kernel.modules {mod!r} missing inline # comment "
          f"(职责/用法，≥{MIN_TEXT_LEN} chars)"
        )
  return errors
