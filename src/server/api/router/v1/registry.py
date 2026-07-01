"""v1 HTTP 路由注册表 — 开发者第一站。

作用：集中登记 OpenAPI `/v1/*` 各 HTTP 域；新增域须补全 summary/problem/usage。
业务关联：modules/*/routers.py · check_router_registry · check_registry_annotations。
上游：router/registry.py register_routers
下游：FastAPI include_router
关联文档：src/server/api/modules/README.md · 命名约定.md
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fastapi import APIRouter, FastAPI
from server.api.modules import (
  agent,
  audit,
  connectors,
  dsl,
  execution,
  graphs,
  harness,
  integration,
  mcp,
  package,
  probes,
  reconciliation,
  registry,
  rulesets,
  tenant,
)

RouteProvider = Callable[[], list[APIRouter]]


@dataclass(frozen=True, slots=True)
class ApiRouterDomain:
  """HTTP 域注册描述符（打开本文件即可见职责与用法）。"""

  name: str
  summary: str
  problem: str
  usage: str
  provider: RouteProvider


API_ROUTER_DOMAINS: tuple[ApiRouterDomain, ...] = (
  ApiRouterDomain(
    name="probes",
    summary="进程/K8s 健康探针（非 OpenAPI 正式域）",
    problem="部署与编排需要 /health · /ready 与业务 API 解耦",
    usage="GET /health · /ready；运维探针直接打，不经业务鉴权链",
    provider=probes.get_routers,
  ),
  ApiRouterDomain(
    name="graphs",
    summary="业务图谱 draft → submit → freeze 生命周期",
    problem="Graph 版本与 checksum 须 HTTP 暴露且规则在 os_core",
    usage="POST/GET /v1/graphs/*；Studio 建图 · Harness 绑定 graph_version",
    provider=graphs.get_routers,
  ),
  ApiRouterDomain(
    name="agent",
    summary="多模态意图 → DslPlan（plan 阶段不写 Legacy）",
    problem="Agent 须产计划供 Harness 确认，禁止直写 ERP（R-01）",
    usage="POST /v1/agent/plan；intent → DslPlan UUID → harness/confirm",
    provider=agent.get_routers,
  ),
  ApiRouterDomain(
    name="harness",
    summary="Harness 确认门：confirm → Rule → Execute",
    problem="人工确认前禁止 L2 写；须 audit harness.confirmed/rejected",
    usage="POST /v1/harness/confirm；plan_id + confirmed + dry_run",
    provider=harness.get_routers,
  ),
  ApiRouterDomain(
    name="reconciliation",
    summary="对账 Job · ReconciliationReport",
    problem="Shadow 期须 read-back 比对账本与 Legacy 是否 drift",
    usage="POST /v1/reconciliation/run；body tenant_id + scope ad_hoc|daily",
    provider=reconciliation.get_routers,
  ),
  ApiRouterDomain(
    name="execution",
    summary="DSL 执行 · revert · 执行证据",
    problem="唯一 L2 写 Legacy 入口须 HTTP 薄封装 execution_service",
    usage="POST /v1/execute · POST /v1/execute/{id}/revert · GET evidence",
    provider=execution.get_routers,
  ),
  ApiRouterDomain(
    name="registry",
    summary="Platform Registry 读 + 变更请求人审",
    problem="契约/配置平面变更须可追溯且不经业务代码散落",
    usage="GET/POST /v1/registry/*；ADR-008 配置枢纽",
    provider=registry.get_routers,
  ),
  ApiRouterDomain(
    name="tenant",
    summary="租户 Shadow / 设置（REST 与 MCP 共用 tenant_service）",
    problem="shadow_mode 须租户级可配；execute 与 MCP tools/call 须同一真源",
    usage="GET/PUT /v1/tenants/{id}/settings；W7 Step5 mcp_gateway 复用内核",
    provider=tenant.get_routers,
  ),
  ApiRouterDomain(
    name="package",
    summary="Implementation Package export/import",
    problem="D1/D2 交付须可移植快照；Studio export 步与 MCP 共用内核",
    usage="POST /v1/packages/export · POST /v1/packages/import；P-01～P-03",
    provider=package.get_routers,
  ),
  ApiRouterDomain(
    name="integration",
    summary="Integration Studio Connect / Discover / Prove",
    problem="实施向导须 HTTP 暴露连通测试与映射，不经 execute 写 Legacy",
    usage="POST /v1/integration/connect/test；P-03 Override 验证",
    provider=integration.get_routers,
  ),
  ApiRouterDomain(
    name="mcp",
    summary="MCP JSON-RPC Gateway（tools/list · tools/call）",
    problem="外部 Agent 须经网关发现 CMV 并产出 DslPlan，禁止直写 Legacy",
    usage="POST /mcp/v1/{tenantId}；M-01 · M-02",
    provider=mcp.get_routers,
  ),
  ApiRouterDomain(
    name="connectors",
    summary="Connector Pack 健康与连通性",
    problem="集成前须验证 Pack 可用，避免 execute 时才失败",
    usage="GET /v1/connectors/{pack_id}/health；Integration Studio Connect 步",
    provider=connectors.get_routers,
  ),
  ApiRouterDomain(
    name="rulesets",
    summary="RuleSet CRUD · evaluate 授权",
    problem="角色/条件/动作规则须版本化并与 Graph 绑定",
    usage="POST /v1/rulesets · POST evaluate；freeze 后 execution 引用",
    provider=rulesets.get_routers,
  ),
  ApiRouterDomain(
    name="dsl",
    summary="CMV 动词注册表只读",
    problem="Execute 前须校验 verb 已知且 level 正确",
    usage="GET /v1/dsl/registry；客户端/Harness 查可用动词",
    provider=dsl.get_routers,
  ),
  ApiRouterDomain(
    name="audit",
    summary="append-only 审计事件查询",
    problem="合规与排障须按 tenant/exec/event_type 追溯写路径",
    usage="GET /v1/audit/events?tenant_id=&event_type=&exec_id=",
    provider=audit.get_routers,
  ),
)

ROUTER_PROVIDERS: tuple[RouteProvider, ...] = tuple(d.provider for d in API_ROUTER_DOMAINS)


def register_v1(app: FastAPI) -> None:
  """按 API_ROUTER_DOMAINS 顺序挂载全部 v1 路由。"""
  for provider in ROUTER_PROVIDERS:
    for router in provider():
      app.include_router(router)
