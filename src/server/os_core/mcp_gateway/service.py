"""MCP JSON-RPC 网关内核（W7 stub · M-01 · M-02）。

作用：tools/list 已授权 CMV · tools/call → DslPlan（不写 Legacy）。
业务关联：POST /mcp/v1/{tenantId} · MCP-Gateway 规格。
上游：server.api.modules.mcp 薄路由
下游：agent_orchestrator · platform_registry · graph_service · rule_engine
关联文档：docs/文档/规格说明/MCP-Gateway规格.md
"""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from os_core.agent_orchestrator import create_plan
from os_core.graph_service import assert_graph_executable
from os_core.platform_registry import pack_store, tenant_config_store
from os_core.rule_engine.store import find_frozen_ruleset_id
from os_core.shared_contracts.cmv_registry import require_known_verb
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.dsl import DslPlanSource


def _jsonrpc_result(*, rpc_id: int | str | None, result: Any) -> dict[str, Any]:
  """JSON-RPC 2.0 成功响应。"""
  out: dict[str, Any] = {"jsonrpc": "2.0", "result": result}
  if rpc_id is not None:
    out["id"] = rpc_id
  return out


def _jsonrpc_error(
  *,
  rpc_id: int | str | None,
  message: str,
  code: int = -32000,
) -> dict[str, Any]:
  """JSON-RPC 2.0 错误响应。"""
  out: dict[str, Any] = {
    "jsonrpc": "2.0",
    "error": {"code": code, "message": message},
  }
  if rpc_id is not None:
    out["id"] = rpc_id
  return out


def _verbs_from_licensed_packs(session: Session, *, tenant_id: str) -> list[str]:
  """已授权 Pack Blueprint ops → CMV 动词集合（M-01）。"""
  verbs: set[str] = set()
  for pack_id in tenant_config_store.list_licensed_pack_ids(session, tenant_id=tenant_id):
    blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
    if not blueprint:
      continue
    spec = blueprint.get("spec") or {}
    for op in spec.get("ops") or []:
      if isinstance(op, dict) and op.get("verb"):
        verb = str(op["verb"])
        try:
          require_known_verb(verb)
          verbs.add(verb)
        except PlatformError:
          continue
  return sorted(verbs)


def list_tools(session: Session, *, tenant_id: str) -> dict[str, Any]:
  """MCP tools/list：仅 tenant 已授权 CMV 子集。"""
  tools = [
    {"name": verb, "description": f"Licensed CMV verb {verb}"}
    for verb in _verbs_from_licensed_packs(session, tenant_id=tenant_id)
  ]
  return {"tools": tools}


def call_tool(
  session: Session,
  *,
  url_tenant_id: str,
  params: dict[str, Any],
) -> dict[str, Any]:
  """MCP tools/call → DslPlan（不写 Legacy · M-02）。"""
  tool_name = str(params.get("name") or "")
  if not tool_name:
    raise PlatformError(
      ErrorCode.DSL_UNKNOWN,
      "tools/call requires params.name",
      http_status=422,
    )

  arguments = params.get("arguments") or {}
  if not isinstance(arguments, dict):
    raise PlatformError(
      ErrorCode.DSL_UNKNOWN,
      "tools/call params.arguments must be object",
      http_status=422,
    )

  tenant_id = str(arguments.get("tenant_id") or url_tenant_id)
  if tenant_id != url_tenant_id:
    raise PlatformError(
      ErrorCode.TENANT_FORBIDDEN,
      f"URL tenant {url_tenant_id} != arguments tenant_id {tenant_id}",
      http_status=403,
    )

  graph_id = str(arguments.get("graph_id") or "")
  graph_version = str(arguments.get("graph_version") or "")
  intent = str(arguments.get("intent") or "")
  if not graph_id or not graph_version or not intent:
    raise PlatformError(
      ErrorCode.DSL_UNKNOWN,
      "tools/call arguments require graph_id, graph_version, intent",
      http_status=422,
    )

  licensed_verbs = set(_verbs_from_licensed_packs(session, tenant_id=tenant_id))
  if tool_name not in licensed_verbs:
    raise PlatformError(
      ErrorCode.MODULE_NOT_LICENSED,
      f"CMV verb {tool_name} not licensed for tenant {tenant_id}",
      http_status=403,
    )

  verb_meta = require_known_verb(tool_name)
  verb_level = str(verb_meta["level"])
  graph = assert_graph_executable(
    session,
    graph_id=graph_id,
    graph_version=graph_version,
    verb=tool_name,
    verb_level=verb_level,
  )

  ruleset_id = find_frozen_ruleset_id(
    session,
    graph_id=graph_id,
    graph_version=graph_version,
  )
  if ruleset_id is None:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "No frozen RuleSet bound to this graph version",
      http_status=403,
    )

  plan = create_plan(
    tenant_id=tenant_id,
    graph_id=graph_id,
    graph_version=graph_version,
    intent=intent,
    ruleset_id=ruleset_id,
    allowed_dsl=graph.allowed_dsl or None,
    source=DslPlanSource.MCP,
    verb=tool_name,
  )
  return plan.model_dump(mode="json")


def handle_mcp_json_rpc(
  session: Session,
  *,
  tenant_id: str,
  request: dict[str, Any],
) -> dict[str, Any]:
  """POST /mcp/v1/{tenantId} JSON-RPC 分发。

  功能：tools/list · tools/call（W7 stub）。
  业务含义：外部 Agent 工具发现与 DslPlan 产出，不经 execution 写 Legacy。
  参数 tenant_id：URL 路径租户（须与 call arguments 一致）。
  参数 request：jsonrpc 2.0 请求体。
  返回：jsonrpc 2.0 响应 dict。
  """
  rpc_id = request.get("id")
  method = str(request.get("method") or "")
  params = request.get("params") or {}
  if not isinstance(params, dict):
    params = {}

  try:
    if method == "tools/list":
      return _jsonrpc_result(rpc_id=rpc_id, result=list_tools(session, tenant_id=tenant_id))
    if method == "tools/call":
      return _jsonrpc_result(
        rpc_id=rpc_id,
        result=call_tool(session, url_tenant_id=tenant_id, params=params),
      )
    return _jsonrpc_error(rpc_id=rpc_id, message=f"Unsupported MCP method: {method}")
  except PlatformError as exc:
    return _jsonrpc_error(rpc_id=rpc_id, message=str(exc), code=exc.http_status or -32000)
