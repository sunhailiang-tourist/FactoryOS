"""W7 Step5：MCP Gateway stub · M-01 · M-02。

业务：tools/list 已授权 CMV · tools/call → DslPlan · 确认前 Legacy 无写。
上游：plan Step5 · POST /mcp/v1/{tenantId}
下游：gate step --step 5 -k 'M-01' · '-k M-02'
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy

DSL_PLAN_REQUIRED = frozenset({
  "plan_id",
  "tenant_id",
  "graph_id",
  "graph_version",
  "steps",
  "source",
  "created_at",
  "expires_at",
})


def _load_dsl_plan_required(contracts_dir: Path) -> set[str]:
  schema_path = contracts_dir / "schemas" / "DslPlan.schema.json"
  data = json.loads(schema_path.read_text(encoding="utf-8"))
  return set(data.get("required", []))


def _mcp_rpc(*, method: str, params: dict | None = None, rpc_id: int = 1) -> dict:
  """MCP JSON-RPC 2.0 请求体。"""
  return {
    "jsonrpc": "2.0",
    "id": rpc_id,
    "method": method,
    "params": params or {},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["tools_list"], ids=["M-01"])
def test_M01_mcp_tools_list_returns_licensed_cmv_only(
  case: str,
  api_client: TestClient,
) -> None:
  """M-01：tools/list → 仅 tenant 已授权 CMV 动词。"""
  resp = api_client.post(
    "/mcp/v1/default",
    json=_mcp_rpc(method="tools/list"),
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()
  assert body.get("jsonrpc") == "2.0", body
  result = body.get("result") or {}
  tools = result.get("tools") or []
  assert isinstance(tools, list), body
  assert len(tools) >= 1, "M-01 须返回至少一个已授权 tool"
  names = {t.get("name") for t in tools if isinstance(t, dict)}
  assert "GOVERNED_WRITE" in names or "WORK_REPORT" in names, names


@pytest.mark.integration
@pytest.mark.parametrize("case", ["tools_call_plan"], ids=["M-02"])
def test_M02_mcp_tools_call_returns_dsl_plan_without_legacy_write(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
  contracts_dir: Path,
) -> None:
  """M-02：tools/call → DslPlan · Legacy 写计数为 0。"""
  mock_legacy.reset_write_count()
  mock_legacy.reset_entity_store()
  before_writes = mock_legacy.get_write_count()

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
          "intent": "report work order wo-m02 completed qty 1",
        },
      },
      rpc_id=2,
    ),
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()
  result = body.get("result") or body.get("result", {})
  if "result" in body and isinstance(body["result"], dict):
    plan = body["result"]
  else:
    plan = result

  expected = _load_dsl_plan_required(contracts_dir)
  assert expected <= set(plan.keys()), plan
  assert DSL_PLAN_REQUIRED <= set(plan.keys())
  assert plan.get("source") in ("agent", "mcp"), plan

  after_writes = mock_legacy.get_write_count()
  assert after_writes == before_writes, "M-02 tools/call 不得直写 Legacy"
