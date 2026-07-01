"""os_core 内核模块注册表 — 开发者第一站。

作用：统一管理并注释 os_core 下全部内核模块；每条须 summary/problem/usage。
业务关联：Core v1.0 冻结域 · import 边界 · MODULE-MAP 真源。
上游：config/lifespan · application 装配
下游：各 */service · */store · shared_contracts
关联文档：docs/文档/架构/命名约定.md · check_registry_annotations
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KernelModule:
  """内核模块描述符（治理用；打开本文件即可见职责与用法）。"""

  name: str
  summary: str
  problem: str
  usage: str
  public_api: tuple[str, ...]
  depends_on: tuple[str, ...]
  forbids: str
  doc: str
  init_hook: Callable[[], None] | None = None


def _noop_init() -> None:
  """空 startup hook。"""


KERNEL_MODULES: tuple[KernelModule, ...] = (
  KernelModule(
    name="shared_contracts",
    summary="Pydantic 模型、JSON Schema、错误码、DomainEvent",
    problem="多内核模块共享类型须单一真源，避免循环依赖与重复 DTO",
    usage="import os_core.shared_contracts.models · exceptions；契约测试对齐 schemas/",
    public_api=("os_core.shared_contracts.models", "os_core.shared_contracts.exceptions"),
    depends_on=(),
    forbids="业务逻辑",
    doc="src/server/os_core/shared_contracts/README.md",
  ),
  KernelModule(
    name="graph_service",
    summary="Graph 版本、freeze、checksum、Override 合并",
    problem="业务图谱变更须版本化、可 freeze，execute 前校验 graph 可执行",
    usage="graph_service.service freeze/submit；execution 调 assert_graph_executable",
    public_api=("os_core.graph_service.service",),
    depends_on=("shared_contracts",),
    forbids="写 Legacy",
    doc="src/server/os_core/graph_service/README.md",
  ),
  KernelModule(
    name="rule_engine",
    summary="角色、条件、动作授权与 evaluate",
    problem="L2 写前须 Rule 授权，deny 时 audit rule.denied",
    usage="rule_engine.evaluate · assert_allowed_for_execute(session, ruleset_id, ...)",
    public_api=("os_core.rule_engine.service", "os_core.rule_engine.evaluate"),
    depends_on=("shared_contracts",),
    forbids="写 Legacy",
    doc="src/server/os_core/rule_engine/README.md",
  ),
  KernelModule(
    name="execution_service",
    summary="DSL 执行、Saga、Revert（编排唯一写 Legacy 路径）",
    problem="L2 写须集中编排：Graph→Rule→License→connector_sdk→audit→账本",
    usage="execution_service.execute(session, ExecuteRequest)；HTTP POST /v1/execute",
    public_api=("os_core.execution_service.service",),
    depends_on=("shared_contracts", "graph_service", "rule_engine", "connector_sdk"),
    forbids="业务 UI",
    doc="src/server/os_core/execution_service/README.md",
  ),
  KernelModule(
    name="audit_service",
    summary="append-only 审计事件",
    problem="每次写路径须可追溯；禁止改历史",
    usage="audit_service.store.append_audit_event · list_audit_events",
    public_api=("os_core.audit_service.store",),
    depends_on=("shared_contracts",),
    forbids="改历史",
    doc="src/server/os_core/audit_service/README.md",
  ),
  KernelModule(
    name="agent_orchestrator",
    summary="LangGraph Skill FSM → DSL 计划（不执行写）",
    problem="Agent 只能产 DslPlan，禁止 Connector.write（R-01）",
    usage="agent_orchestrator.create_plan；API POST /v1/agent/plan",
    public_api=(),
    depends_on=("shared_contracts", "execution_service"),
    forbids="写 Legacy、绕过 Rule",
    doc="src/server/os_core/agent_orchestrator/README.md",
  ),
  KernelModule(
    name="connector_sdk",
    summary="Legacy 读写、Blueprint Runtime、Pack health",
    problem="ADR-002 唯一写 Legacy 须经 Pack runtime，mock 与真 ERP 可切换",
    usage="connector_sdk.runtime.execute_op · mock_legacy；Pack health HTTP",
    public_api=("os_core.connector_sdk.health", "os_core.connector_sdk.runtime.execute"),
    depends_on=("shared_contracts", "platform_registry"),
    forbids="业务规则",
    doc="src/server/os_core/connector_sdk/README.md",
  ),
  KernelModule(
    name="tenant_service",
    summary="租户 shadow_mode / settings 真源（REST · MCP 共用）",
    problem="Shadow 开关须租户级；MCP 与 REST execute 不得各读一套配置",
    usage=(
      "tenant_service.resolve_shadow_mode(session, tenant_id=...); "
      "GET/PUT /v1/tenants/{id}/settings"
    ),
    public_api=(
      "os_core.tenant_service.get_tenant_settings",
      "os_core.tenant_service.resolve_shadow_mode",
    ),
    depends_on=("shared_contracts", "platform_registry"),
    forbids="写 Legacy",
    doc="src/server/os_core/tenant_service/README.md",
  ),
  KernelModule(
    name="license_service",
    summary="Pack 授权、租户 Override 生效域",
    problem="未订阅 Pack 禁止 L2 写，须 MODULE_NOT_LICENSED + audit",
    usage="license_service.assert_pack_licensed(tenant_id, pack_id)；execution 前调用",
    public_api=(),
    depends_on=("shared_contracts",),
    forbids="执行 DSL",
    doc="src/server/os_core/license_service/README.md",
  ),
  KernelModule(
    name="package_service",
    summary="Implementation Package export/import 快照",
    problem="D1/D2 交付须可移植 Graph+Rule+Connector 包，Studio 与 MCP 共用",
    usage=(
      "package_service.export_implementation_package(session, tenant_id=...); "
      "POST /v1/packages/export"
    ),
    public_api=(
      "os_core.package_service.export_implementation_package",
      "os_core.package_service.import_implementation_package",
    ),
    depends_on=("shared_contracts", "graph_service", "rule_engine", "platform_registry"),
    forbids="写 Legacy",
    doc="src/server/os_core/package_service/README.md",
  ),
  KernelModule(
    name="reconciliation_service",
    summary="对账 Job · ExecutionRecord read-back vs Legacy",
    problem="Shadow 期每日对账，drift 须可解释、可告警",
    usage=(
      "reconciliation_service.run_reconciliation(session, tenant_id=...); "
      "HTTP POST /v1/reconciliation/run"
    ),
    public_api=("os_core.reconciliation_service.run_reconciliation",),
    depends_on=("shared_contracts", "connector_sdk", "execution_service"),
    forbids="写 Legacy",
    doc="src/server/os_core/reconciliation_service/README.md",
  ),
  KernelModule(
    name="mcp_gateway",
    summary="MCP tools/list、tools/call → DslPlan · SEP-414 trace",
    problem="外部 MCP 工具须网关化，禁止直写 Legacy",
    usage="mcp_gateway.handle_mcp_json_rpc；tools/list · tools/call · _meta.traceparent（M-03）",
    public_api=("os_core.mcp_gateway.handle_mcp_json_rpc",),
    depends_on=(
      "shared_contracts",
      "agent_orchestrator",
      "platform_registry",
      "graph_service",
      "rule_engine",
      "audit_service",
    ),
    forbids="直写 Legacy",
    doc="src/server/os_core/mcp_gateway/README.md",
  ),
  KernelModule(
    name="platform_registry",
    summary="配置与契约平面 DB 真源（ADR-008）",
    problem="CMV/Schema/OpenAPI/Catalog 须 DB 可审计，非散落文件",
    usage="platform_registry.bootstrap 启动 seed · session 读契约；GET /v1/registry",
    public_api=("os_core.platform_registry.bootstrap", "os_core.platform_registry.session"),
    depends_on=("shared_contracts",),
    forbids="业务规则",
    doc="src/server/os_core/platform_registry/README.md · ADR-008",
    init_hook=_noop_init,
  ),
)


def kernel_module_names() -> tuple[str, ...]:
  """已登记内核包名（harness / 文档生成）。"""
  return tuple(m.name for m in KERNEL_MODULES)


def init_kernel() -> None:
  """按注册表执行各模块 startup hook（S0 多为 no-op）。"""
  for mod in KERNEL_MODULES:
    if mod.init_hook is not None:
      mod.init_hook()
