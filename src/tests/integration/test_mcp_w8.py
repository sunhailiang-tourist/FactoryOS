"""W8 Step1：MCP SEP-414 traceparent · M-03。

业务：tools/call params._meta.traceparent → DslPlan.trace_id · audit correlation_id 一致。
上游：plan Step1 · POST /mcp/v1/{tenantId}
下游：gate step --step 1 -k 'M-03'
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

# MCP-Gateway 规格示例 traceparent → trace_id 32 hex
TRACEPARENT = "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
EXPECTED_TRACE_ID = "0af7651916cd43dd8448eb211c80319c"


def _mcp_rpc(*, method: str, params: dict | None = None, rpc_id: int = 1) -> dict:
  """MCP JSON-RPC 2.0 请求体。"""
  return {
    "jsonrpc": "2.0",
    "id": rpc_id,
    "method": method,
    "params": params or {},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["traceparent"], ids=["M-03"])
def test_M03_mcp_tools_call_propagates_traceparent_to_plan_and_audit(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """M-03：_meta.traceparent → plan.trace_id · audit mcp.tools_call correlation_id 一致。"""
  resp = api_client.post(
    "/mcp/v1/default",
    json=_mcp_rpc(
      method="tools/call",
      params={
        "name": "GOVERNED_WRITE",
        "arguments": {
          "tenant_id": "default",
          "graph_id": frozen_graph_env["graph_id"],
          "graph_version": frozen_graph_env["version"],
          "intent": "report work order wo-m03 completed qty 1",
        },
        "_meta": {
          "traceparent": TRACEPARENT,
        },
      },
      rpc_id=3,
    ),
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()
  plan = body.get("result") or {}
  assert isinstance(plan, dict), body
  plan_id = plan.get("plan_id")
  assert plan_id, plan

  assert plan.get("trace_id") == EXPECTED_TRACE_ID, (
    "M-03 DslPlan.trace_id 须等于 traceparent 解析的 32 位 trace_id"
  )

  audit_resp = api_client.get(
    "/v1/audit/events",
    params={
      "tenant_id": "default",
      "event_type": "mcp.tools_call",
    },
  )
  assert audit_resp.status_code == 200, audit_resp.text
  events = audit_resp.json()
  assert isinstance(events, list), events

  matched = [
    e
    for e in events
    if e.get("plan_id") == plan_id and e.get("correlation_id") == EXPECTED_TRACE_ID
  ]
  assert len(matched) >= 1, (
    "M-03 须 append audit mcp.tools_call · plan_id 与 correlation_id=trace_id 关联"
  )


@pytest.mark.integration
@pytest.mark.parametrize("case", ["no_meta"], ids=["M-03-no-meta"])
def test_M03_tools_call_without_meta_behaves_like_w7(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """M-03 负向补充：无 _meta 时仍产出 DslPlan · trace_id 为空或不设。"""
  resp = api_client.post(
    "/mcp/v1/default",
    json=_mcp_rpc(
      method="tools/call",
      params={
        "name": "GOVERNED_WRITE",
        "arguments": {
          "tenant_id": "default",
          "graph_id": frozen_graph_env["graph_id"],
          "graph_version": frozen_graph_env["version"],
          "intent": "report work order wo-m03-nometa completed qty 1",
        },
      },
      rpc_id=4,
    ),
  )
  assert resp.status_code == 200, resp.text
  plan = resp.json().get("result") or {}
  assert plan.get("plan_id"), plan
  trace_id = plan.get("trace_id")
  assert trace_id is None or trace_id == "", (
    "无 _meta 时 trace_id 须为空，与 W7 行为一致"
  )
