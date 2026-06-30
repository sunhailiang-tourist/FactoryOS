"""os_core 内核模块注册表 — 开发者第一站。

作用：统一管理并注释 os_core 下全部内核模块。
业务关联：Core v1.0 冻结域 · import 边界 · MODULE-MAP 真源。
上游：config/lifespan · application 装配
下游：各 */service · */store · shared_contracts
关联文档：docs/文档/架构/命名约定.md
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KernelModule:
  """内核模块描述符（治理用）。"""

  name: str
  summary: str
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
    public_api=("os_core.shared_contracts.models", "os_core.shared_contracts.exceptions"),
    depends_on=(),
    forbids="业务逻辑",
    doc="src/server/os_core/shared_contracts/README.md",
  ),
  KernelModule(
    name="graph_service",
    summary="Graph 版本、freeze、checksum、Override 合并",
    public_api=("os_core.graph_service.service",),
    depends_on=("shared_contracts",),
    forbids="写 Legacy",
    doc="src/server/os_core/graph_service/README.md",
  ),
  KernelModule(
    name="rule_engine",
    summary="角色、条件、动作授权与 evaluate",
    public_api=("os_core.rule_engine.service", "os_core.rule_engine.evaluate"),
    depends_on=("shared_contracts",),
    forbids="写 Legacy",
    doc="src/server/os_core/rule_engine/README.md",
  ),
  KernelModule(
    name="execution_service",
    summary="DSL 执行、Saga、Revert、对账（唯一写 Legacy）",
    public_api=("os_core.execution_service.service",),
    depends_on=("shared_contracts", "graph_service", "rule_engine", "connector_sdk"),
    forbids="业务 UI",
    doc="src/server/os_core/execution_service/README.md",
  ),
  KernelModule(
    name="audit_service",
    summary="append-only 审计事件",
    public_api=("os_core.audit_service.store",),
    depends_on=("shared_contracts",),
    forbids="改历史",
    doc="src/server/os_core/audit_service/README.md",
  ),
  KernelModule(
    name="agent_orchestrator",
    summary="LangGraph Skill FSM → DSL 计划",
    public_api=(),
    depends_on=("shared_contracts", "execution_service"),
    forbids="写 Legacy、绕过 Rule",
    doc="src/server/os_core/agent_orchestrator/README.md",
  ),
  KernelModule(
    name="connector_sdk",
    summary="Legacy 读写、Blueprint Runtime、Pack health",
    public_api=("os_core.connector_sdk.health", "os_core.connector_sdk.runtime.execute"),
    depends_on=("shared_contracts", "platform_registry"),
    forbids="业务规则",
    doc="src/server/os_core/connector_sdk/README.md",
  ),
  KernelModule(
    name="license_service",
    summary="Pack 授权、Override 生效域",
    public_api=(),
    depends_on=("shared_contracts",),
    forbids="执行 DSL",
    doc="src/server/os_core/license_service/README.md",
  ),
  KernelModule(
    name="reconciliation_service",
    summary="对账 Job · ExecutionRecord read-back vs Legacy",
    public_api=("os_core.reconciliation_service.run_reconciliation",),
    depends_on=("shared_contracts", "connector_sdk", "execution_service"),
    forbids="写 Legacy",
    doc="src/server/os_core/reconciliation_service/README.md",
  ),
  KernelModule(
    name="mcp_gateway",
    summary="MCP tools/list、tools/call → DslPlan",
    public_api=(),
    depends_on=("shared_contracts", "agent_orchestrator"),
    forbids="直写 Legacy",
    doc="src/server/os_core/mcp_gateway/README.md",
  ),
  KernelModule(
    name="platform_registry",
    summary="配置与契约平面 DB 真源（ADR-008）",
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
