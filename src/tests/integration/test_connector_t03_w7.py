"""W7 Step2：Connector 未配置 · T-03。

业务：未注册 pack_id execute → 403 CONNECTOR_NOT_CONFIGURED。
上游：plan Step2 · license 真源 + connector registry
下游：gate step --step 2 -k 'T-03'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient


def _execute_body(env: dict[str, str], *, tenant_id: str) -> dict:
  """未配置 Connector 的 tenant execute 请求（T-03）。"""
  return {
    "tenant_id": tenant_id,
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "verb": "GOVERNED_WRITE",
    "params": {
      "entity_type": "work_order",
      "entity_id": f"wo-t03-{uuid.uuid4().hex[:8]}",
      "fields": {"status": "done", "completed_qty": 1},
    },
    "dry_run": True,
    "idempotency_key": f"t03-{uuid.uuid4().hex[:12]}",
    "ruleset_id": env["ruleset_id"],
    "actor": {"user_id": "t03-operator", "role": "operator", "channel": "api"},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["connector_missing"], ids=["T-03"])
def test_T03_execute_unconfigured_connector_returns_403(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """T-03：tenant 无已注册 pack → 403 CONNECTOR_NOT_CONFIGURED。"""
  tenant_id = "tenant-connector-missing-w7"
  resp = api_client.post(
    "/v1/execute",
    json=_execute_body(frozen_graph_env, tenant_id=tenant_id),
  )
  assert resp.status_code == 403, resp.text
  body = resp.json()
  assert body.get("code") == "CONNECTOR_NOT_CONFIGURED", body
