#!/usr/bin/env python3
"""Validate os_core/ import boundaries per 膨胀期架构守则 §2 (stdlib only).

作用：ALLOWED 由 IMPORT_BOUNDARY_REGISTRY 生成；新增包须补 summary/problem/usage。
业务关联：膨胀期架构 · check_registry_annotations 联动。
Usage:
  python scripts/check_import_boundaries.py

Exit 0 = pass; 1 = violations found.
"""
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OS_CORE = ROOT / "src" / "server" / "os_core"
INTEGRATION = ROOT / "src" / "integration"


@dataclass(frozen=True, slots=True)
class ImportBoundaryEntry:
  """os_core 包 import 白名单项（打开本文件即可见职责与用法）。"""

  package: str
  summary: str
  problem: str
  usage: str
  allowed: frozenset[str]


IMPORT_BOUNDARY_REGISTRY: tuple[ImportBoundaryEntry, ...] = (
  ImportBoundaryEntry(
    package="shared_contracts",
    summary="契约 DTO · 错误码 · CMV loader",
    problem="内核共享类型须最低依赖，避免业务包互引",
    usage="各 service 首选 import；仅允许读 platform_registry 契约平面",
    allowed=frozenset({"platform_registry"}),
  ),
  ImportBoundaryEntry(
    package="platform_registry",
    summary="ADR-008 配置/契约 DB 访问",
    problem="Schema/CMV/OpenAPI 真源须集中，禁止散落 SQL",
    usage="bootstrap seed · contract_store 读；shared_contracts 反查",
    allowed=frozenset({"shared_contracts"}),
  ),
  ImportBoundaryEntry(
    package="audit_service",
    summary="append-only 审计 store",
    problem="写路径审计不能由各 service 直写 SQL",
    usage="append_audit_event(session, ...)；仅 shared_contracts",
    allowed=frozenset({"shared_contracts"}),
  ),
  ImportBoundaryEntry(
    package="graph_service",
    summary="Graph freeze · checksum",
    problem="Graph 规则须与 execution 解耦但可写 audit",
    usage="graph_service.service；可 import audit_service",
    allowed=frozenset({"shared_contracts", "audit_service"}),
  ),
  ImportBoundaryEntry(
    package="rule_engine",
    summary="Rule evaluate · freeze RuleSet",
    problem="授权逻辑集中，禁止 execution 内嵌 if/role",
    usage="rule_engine.evaluate · assert_allowed_for_execute",
    allowed=frozenset({"shared_contracts", "audit_service"}),
  ),
  ImportBoundaryEntry(
    package="execution_service",
    summary="DSL 执行编排（唯一写 Legacy 链）",
    problem="L2 写依赖 Graph/Rule/Connector/License 但不得反向被依赖写规则",
    usage="execute/revert；可 import 列出的编排依赖包",
    allowed=frozenset({
      "shared_contracts",
      "audit_service",
      "connector_sdk",
      "rule_engine",
      "graph_service",
      "license_service",
    }),
  ),
  ImportBoundaryEntry(
    package="connector_sdk",
    summary="Pack runtime · mock_legacy · health",
    problem="Legacy IO 必须经 SDK，禁止 service 直 httpx ERP",
    usage="runtime.execute_op · mock_legacy.get_entity",
    allowed=frozenset({"shared_contracts", "platform_registry"}),
  ),
  ImportBoundaryEntry(
    package="agent_orchestrator",
    summary="Agent FSM → DslPlan",
    problem="Agent 禁 import execution/connector 写路径（R-01）",
    usage="create_plan 仅 shared_contracts",
    allowed=frozenset({"shared_contracts"}),
  ),
  ImportBoundaryEntry(
    package="license_service",
    summary="Pack 授权 stub/真源",
    problem="授权判断须独立，供 execution 前置调用",
    usage="assert_pack_licensed(tenant_id, pack_id)",
    allowed=frozenset({"shared_contracts"}),
  ),
  ImportBoundaryEntry(
    package="reconciliation_service",
    summary="对账 read-back",
    problem="对账只读账本+Legacy，不得 import 写路径",
    usage="run_reconciliation；可读 execution store + mock_legacy",
    allowed=frozenset({"shared_contracts", "connector_sdk", "execution_service"}),
  ),
  ImportBoundaryEntry(
    package="mcp_gateway",
    summary="MCP 网关（W7+）",
    problem="外部工具调用须经 gateway，禁止直写",
    usage="tools/list · tools/call → agent_orchestrator",
    allowed=frozenset({"shared_contracts", "agent_orchestrator"}),
  ),
)

ALLOWED: dict[str, set[str]] = {
  entry.package: set(entry.allowed) for entry in IMPORT_BOUNDARY_REGISTRY
}

INTEGRATION_ALLOWED_PACKAGES = frozenset({"shared_contracts", "connector_sdk"})


def module_name_from_path(path: Path) -> str | None:
  try:
    rel = path.relative_to(OS_CORE)
  except ValueError:
    return None
  parts = rel.parts
  if not parts or parts[0] not in ALLOWED:
    return None
  return parts[0]


def parse_imports(path: Path) -> list[tuple[int, str]]:
  try:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
  except SyntaxError as exc:
    return [(-1, f"syntax error: {exc}")]
  out: list[tuple[int, str]] = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      for alias in node.names:
        out.append((node.lineno, alias.name))
    elif isinstance(node, ast.ImportFrom) and node.module:
      out.append((node.lineno, node.module))
  return out


def imported_package(module: str) -> str | None:
  if module.startswith("os_core."):
    rest = module[len("os_core.") :]
    return rest.split(".")[0] if rest else None
  return None


def check_os_core() -> list[str]:
  errors: list[str] = []
  if not OS_CORE.is_dir():
    return errors
  for py in OS_CORE.rglob("*.py"):
    if "__pycache__" in py.parts:
      continue
    owner = module_name_from_path(py)
    if owner is None:
      continue
    allowed = ALLOWED[owner]
    for lineno, mod in parse_imports(py):
      if lineno < 0:
        errors.append(f"{py}: {mod}")
        continue
      pkg = imported_package(mod)
      if pkg is None or pkg == owner:
        continue
      if pkg not in ALLOWED:
        errors.append(f"{py}:{lineno}: unknown package import os_core.{pkg}")
      elif pkg not in allowed:
        errors.append(
          f"{py}:{lineno}: {owner} must not import os_core.{pkg} "
          f"(allowed: {sorted(allowed) or ['—']})"
        )
  return errors


def check_integration() -> list[str]:
  errors: list[str] = []
  if not INTEGRATION.is_dir():
    return errors
  for py in INTEGRATION.rglob("*.py"):
    if "__pycache__" in py.parts:
      continue
    for lineno, mod in parse_imports(py):
      if lineno < 0:
        errors.append(f"{py}: {mod}")
        continue
      pkg = imported_package(mod)
      if pkg is None:
        continue
      if pkg not in INTEGRATION_ALLOWED_PACKAGES:
        errors.append(
          f"{py}:{lineno}: integration/ must not import os_core.{pkg} "
          f"(allowed: {sorted(INTEGRATION_ALLOWED_PACKAGES)})"
        )
  return errors


def main() -> int:
  errors = check_os_core() + check_integration()
  if errors:
    print("Import boundary violations:", file=sys.stderr)
    for e in errors:
      print(f"  {e}", file=sys.stderr)
    return 1
  print("Import boundaries OK")
  return 0


if __name__ == "__main__":
  sys.exit(main())
