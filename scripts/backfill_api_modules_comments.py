#!/usr/bin/env python3
"""一次性回填 api/modules 中文注释（CMNT-03 Step 4 · 零逻辑 diff）。

作用：批量补齐文件头四标签与公开函数 doc 关键词。
业务关联：plan 1a.5 · B2 api/modules 注释债闭合。
上游：check_python_comments.py 违规清单
下游：src/server/api/modules/**

Usage:
  uv run python scripts/backfill_api_modules_comments.py
  uv run python scripts/backfill_api_modules_comments.py --dry-run
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "src" / "server" / "api" / "modules"

# 域元数据（对齐 modules/README.md · 各域 README）
DOMAIN_META: dict[str, dict[str, str]] = {
  "agent": {
    "title": "Agent",
    "paths": "/v1/agent/plan",
    "biz": "H-01 意图→DslPlan（不写 Legacy）",
    "os_core": "os_core.agent_orchestrator",
  },
  "audit": {
    "title": "Audit",
    "paths": "/v1/audit/events",
    "biz": "E-03 append-only 审计查询",
    "os_core": "os_core.audit_service",
  },
  "connectors": {
    "title": "Connectors",
    "paths": "/v1/connectors/*",
    "biz": "Connector Pack 健康检查",
    "os_core": "os_core.connector_sdk",
  },
  "dsl": {
    "title": "DSL",
    "paths": "/v1/dsl/registry",
    "biz": "CMV 动词注册表只读",
    "os_core": "os_core.shared_contracts.cmv_registry",
  },
  "execution": {
    "title": "Execution",
    "paths": "/v1/execute · /v1/executions/*",
    "biz": "E-02 L2 执行 · E-04/E-05 revert",
    "os_core": "os_core.execution_service",
  },
  "graphs": {
    "title": "Graphs",
    "paths": "/v1/graphs/*",
    "biz": "业务图谱 draft→freeze 生命周期",
    "os_core": "os_core.graph_service",
  },
  "harness": {
    "title": "Harness",
    "paths": "/v1/harness/confirm",
    "biz": "H-02 确认门 → Rule → Execute",
    "os_core": "os_core.rule_engine · execution_service",
  },
  "integration": {
    "title": "Integration",
    "paths": "/v1/integration/*",
    "biz": "Studio Connect→Prove 六步",
    "os_core": "os_core.connector_sdk",
  },
  "mcp": {
    "title": "MCP",
    "paths": "/v1/mcp/jsonrpc",
    "biz": "W7 MCP JSON-RPC 网关",
    "os_core": "os_core.mcp_gateway",
  },
  "package": {
    "title": "Package",
    "paths": "/v1/packages/*",
    "biz": "Pack 导入导出",
    "os_core": "os_core.package_service",
  },
  "probes": {
    "title": "Probes",
    "paths": "/health · /ready",
    "biz": "K8s 进程/就绪探针（非 OpenAPI 正式域）",
    "os_core": "无（进程内自检）",
  },
  "reconciliation": {
    "title": "Reconciliation",
    "paths": "/v1/reconciliation/run",
    "biz": "K-01/K-02 对账 Job",
    "os_core": "os_core.reconciliation_service",
  },
  "registry": {
    "title": "Registry",
    "paths": "/v1/registry/*",
    "biz": "Platform Registry 读 + 变更请求人审",
    "os_core": "os_core.platform_registry",
  },
  "rulesets": {
    "title": "RuleSets",
    "paths": "/v1/rulesets/*",
    "biz": "R-01～R-05 规则集 CRUD · evaluate",
    "os_core": "os_core.rule_engine",
  },
  "studio": {
    "title": "Studio",
    "paths": "/v1/studio/*",
    "biz": "Studio RBAC · 平台管理 API",
    "os_core": "os_core.platform_registry · tenant_service",
  },
  "tenant": {
    "title": "Tenant",
    "paths": "/v1/tenants/{tenantId}/settings",
    "biz": "T-01 Shadow · STU-04 write_approved",
    "os_core": "os_core.tenant_service",
  },
}

FUNC_CHAIN_MARKERS = ("上游", "下游", "参数", "返回", "异常")
FUNC_BUSINESS_MARKERS = ("功能", "业务", "业务含义")


def _domain_from_path(path: Path) -> str | None:
  rel = path.relative_to(MODULES)
  parts = rel.parts
  if not parts or parts[0] == "__init__.py":
    return None
  return parts[0] if parts[0] != "__init__.py" else None


def _file_role(path: Path) -> str:
  rel = path.relative_to(MODULES)
  parts = rel.parts
  if len(parts) == 1 and parts[0] == "__init__.py":
    return "root"
  if len(parts) == 2 and parts[1] == "__init__.py":
    return "domain_init"
  if parts[-1] == "routers.py":
    return "routers"
  if parts[-1] == "__init__.py" and "controllers" in parts:
    return "controllers_init"
  if parts[-1] == "__init__.py" and "schemas" in parts:
    return "schemas_init"
  if parts[-1] == "__init__.py" and "application" in parts:
    return "application_init"
  if "controllers" in parts and parts[-1].endswith(".py"):
    return "controller"
  return "other"


def _module_doc(path: Path) -> str:
  domain = _domain_from_path(path)
  role = _file_role(path)
  meta = DOMAIN_META.get(domain or "", {})
  title = meta.get("title", domain or "modules")
  biz = meta.get("biz", "OpenAPI 薄路由域")
  os_core = meta.get("os_core", "os_core")
  paths = meta.get("paths", "")

  if role == "root":
    return (
      '"""业务域 HTTP 模块包（api/modules）。\n\n'
      "作用：OpenAPI /v1/* 各域 HTTP 适配实现根命名空间。\n"
      "业务关联：薄路由层；业务规则在 os_core。\n"
      "上游：router/v1/registry · HTTP 客户端。\n"
      '下游：modules/*/controllers · os_core/*/service。\n"""'
    )
  if role == "domain_init":
    return (
      f'"""modules/{domain} 包根。\n\n'
      f"作用：{title} 域 HTTP 模块命名空间与 get_routers 导出。\n"
      f"业务关联：{biz}。\n"
      "上游：router/v1/registry · ROUTER_PROVIDERS。\n"
      f"下游：controllers · {os_core}。\n"
      '"""'
    )
  if role == "routers":
    return (
      f'"""{title} 域 router 聚合。\n\n'
      "作用：导出 get_routers 供 router/v1/registry 登记。\n"
      f"业务关联：{biz}。\n"
      "上游：router/v1/registry · ROUTER_PROVIDERS。\n"
      f"下游：modules/{domain}/controllers/*。\n"
      '"""'
    )
  if role == "controllers_init":
    return (
      f'"""modules/{domain}/controllers 包。\n\n'
      f"作用：{title} 域 HTTP handler（APIRouter）集合。\n"
      f"业务关联：{biz}。\n"
      f"上游：modules/{domain}/routers。\n"
      f"下游：{os_core}。\n"
      '"""'
    )
  if role == "schemas_init":
    return (
      f'"""modules/{domain}/schemas 包。\n\n'
      f"作用：{title} 域 OpenAPI DTO（Pydantic）命名空间。\n"
      f"业务关联：{biz}；与 os_core 领域模型分离。\n"
      f"上游：modules/{domain}/controllers。\n"
      "下游：OpenAPI 契约 · HTTP 序列化。\n"
      '"""'
    )
  if role == "application_init":
    return (
      f'"""modules/{domain}/application 包。\n\n'
      f"作用：{title} 域薄编排（复杂域 mandatory）。\n"
      f"业务关联：{biz}。\n"
      f"上游：modules/{domain}/controllers。\n"
      f"下游：{os_core}。\n"
      '"""'
    )
  if role == "controller" and path.name == "health.py":
    return (
      '"""Probes 域 HTTP 路由（/health · /ready）。\n\n'
      "作用：进程存活与就绪探针；无业务逻辑。\n"
      "业务关联：K8s 探针（非 OpenAPI 正式域）。\n"
      "上游：modules/probes/routers。\n"
      "下游：无（进程内返回 status ok）。\n"
      '"""'
    )
  # fallback: expand short existing
  return (
    f'"""{title} 模块（{paths}）。\n\n'
    f"作用：薄路由 HTTP 适配。\n"
    f"业务关联：{biz}。\n"
    f"上游：modules/{domain}/routers。\n"
    f"下游：{os_core}。\n"
    '"""'
  )


def _get_routers_doc(domain: str | None) -> str:
  title = DOMAIN_META.get(domain or "", {}).get("title", domain or "域")
  return (
    '  """返回本域 APIRouter 列表供 v1 登记。\n\n'
    "  功能：聚合 controllers 下子 router。\n"
    f"  业务含义：{title} 域 ROUTER_PROVIDERS 调用入口。\n"
    "  上游：router/v1/registry。\n"
    f"  下游：modules/{domain}/controllers/*。\n"
    '  """'
  )


def _enhance_func_doc(existing: str | None, func_name: str, domain: str | None) -> str:
  meta = DOMAIN_META.get(domain or "", {})
  os_core = meta.get("os_core", "os_core")
  title = meta.get("title", domain or "API")
  first = (existing or f"HTTP handler {func_name}。").strip().split("\n")[0].strip()
  text = existing or ""
  has_business = any(m in text for m in FUNC_BUSINESS_MARKERS)
  has_chain = any(m in text for m in FUNC_CHAIN_MARKERS)

  lines = [first, ""]
  if not has_business:
    lines.append("  功能：薄路由 HTTP 处理；委托 os_core。")
    lines.append(f"  业务含义：{title} 域对外 API 入口。")
  else:
    for ln in text.strip().splitlines()[1:]:
      s = ln.strip()
      if s:
        lines.append(f"  {s}" if not ln.startswith("  ") else ln.rstrip())

  if not has_chain:
    if func_name == "get_routers":
      lines.extend(
        [
          "  功能：聚合本域 APIRouter 列表。",
          f"  业务含义：{title} 域路由登记入口。",
          "  上游：router/v1/registry。",
          f"  下游：modules/{domain}/controllers/*。",
        ]
      )
    elif func_name in ("health", "ready"):
      lines.extend(
        [
          "  功能：返回进程探针状态。",
          "  业务含义：K8s liveness/readiness 检查。",
          "  上游：kubelet HTTP GET。",
          "  返回：status ok 字典。",
        ]
      )
    else:
      lines.extend(
        [
          "  上游：FastAPI 请求 · Depends 注入。",
          f"  下游：{os_core}。",
        ]
      )
  lines = [ln for ln in lines if ln != ""]
  body = "\n".join(lines)
  return f'  """{body}\n  """'


def _replace_module_docstring(text: str, new_doc: str) -> str:
  """替换文件首个模块级 docstring。"""
  try:
    tree = ast.parse(text)
  except SyntaxError:
    return text
  doc = ast.get_docstring(tree, clean=False)
  if doc is None:
    # 无 docstring：在首行或 future import 前插入
    insert_at = 0
    lines = text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
      if ln.startswith("from __future__"):
        insert_at = i + 1
        break
    return "".join(lines[:insert_at]) + new_doc + "\n" + "".join(lines[insert_at:])

  # 定位模块 docstring 的引号范围
  pattern = re.compile(r'^("""|\'\'\')(.*?)\1', re.DOTALL | re.MULTILINE)
  m = pattern.search(text)
  if m:
    return text[: m.start()] + new_doc + text[m.end() :]
  return text


def _patch_get_routers(text: str, domain: str | None) -> str:
  if "def get_routers" not in text:
    return text
  if re.search(r"def get_routers\([^)]*\)[^:]*:\n\s+\"\"\"", text):
    return text
  doc = _get_routers_doc(domain)
  return re.sub(
    r"(def get_routers\([^)]*\)[^:]*:)\n(\s+return )",
    rf"\1\n{doc}\n\2",
    text,
    count=1,
  )


def _patch_function_docs(text: str, path: Path) -> str:
  domain = _domain_from_path(path)
  try:
    tree = ast.parse(text)
  except SyntaxError:
    return text

  lines = text.splitlines()
  patches: list[tuple[int, int, str]] = []

  class V(ast.NodeVisitor):
    def __init__(self) -> None:
      self.depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
      if self.depth > 0 or node.name == "main":
        return
      doc = ast.get_docstring(node, clean=False)
      body_len = len(node.body)
      need = False
      if doc is None or not doc.strip():
        if not (node.name.startswith("_") and body_len <= 3):
          need = True
      else:
        if not node.name.startswith("_"):
          has_b = any(m in doc for m in FUNC_BUSINESS_MARKERS)
          has_c = any(m in doc for m in FUNC_CHAIN_MARKERS)
          if not has_b or not has_c or len(doc.strip()) < 24:
            need = True
      if need and node.body:
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
          start = first.lineno - 1
          end = first.end_lineno or first.lineno
          new_doc = _enhance_func_doc(doc, node.name, domain)
          patches.append((start, end, new_doc))
        elif doc is None:
          # insert after def line
          def_line = node.lineno - 1
          new_doc = _enhance_func_doc(None, node.name, domain)
          indent = "  "
          lines_insert = new_doc.splitlines()
          block = "\n".join(lines_insert) + "\n"
          # mark for insert at lineno
          patches.append((def_line, def_line, block))

  v = V()
  v.visit(tree)

  if not patches:
    return text

  # apply bottom-up
  result_lines = lines[:]
  for start, end, new in sorted(patches, key=lambda x: -x[0]):
    if start == end:
      result_lines.insert(start, new.rstrip("\n"))
    else:
      new_lines = new.splitlines()
      result_lines[start:end] = new_lines

  return "\n".join(result_lines) + ("\n" if text.endswith("\n") else "")


def _needs_module_doc(path: Path, text: str) -> bool:
  try:
    tree = ast.parse(text)
  except SyntaxError:
    return True
  doc = ast.get_docstring(tree, clean=False)
  if doc is None:
    return True
  required = ("作用", "业务关联", "上游", "下游")
  if not all(t in doc for t in required):
    return True
  if len(doc.strip()) < 40:
    return True
  return False


def patch_file(path: Path, *, dry_run: bool) -> bool:
  text = path.read_text(encoding="utf-8")
  original = text
  role = _file_role(path)

  if _needs_module_doc(path, text):
    # 已有完整四标签的 controller 不动（如 tenant.py）
    try:
      tree = ast.parse(text)
      doc = ast.get_docstring(tree, clean=False) or ""
      if all(t in doc for t in ("作用", "业务关联", "上游", "下游")) and len(doc) >= 40:
        pass
      else:
        text = _replace_module_docstring(text, _module_doc(path))
    except SyntaxError:
      text = _replace_module_docstring(text, _module_doc(path))

  if role in ("routers", "domain_init", "root", "controllers_init", "schemas_init", "application_init", "controller"):
    text = _patch_get_routers(text, _domain_from_path(path))
    text = _patch_function_docs(text, path)

  if text != original:
    if not dry_run:
      path.write_text(text, encoding="utf-8")
    return True
  return False


def main() -> int:
  p = argparse.ArgumentParser(description="Backfill api/modules Chinese comments")
  p.add_argument("--dry-run", action="store_true")
  args = p.parse_args()

  changed = 0
  for py in sorted(MODULES.rglob("*.py")):
    if patch_file(py, dry_run=args.dry_run):
      changed += 1
      print(f"{'[dry] ' if args.dry_run else ''}patched: {py.relative_to(ROOT)}")

  print(f"\n{'Would patch' if args.dry_run else 'Patched'} {changed} file(s)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
