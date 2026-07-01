"""W7 Step1：租户 shadow_mode · T-01。

业务：tenant.shadow_mode=true 时 L2 写 simulated · Legacy 不变。
上游：plan Step1 · GET/PUT /v1/tenants/{id}/settings
下游：gate step --step 1 -k 'T-01'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy


def _l2_execute_body(env: dict[str, str], *, tenant_id: str = "default") -> dict:
  """L2 真写请求（dry_run=false · T-01 shadow 场景）。"""
  return {
    "tenant_id": tenant_id,
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "verb": "GOVERNED_WRITE",
    "params": {
      "entity_type": "work_order",
      "entity_id": f"wo-t01-{uuid.uuid4().hex[:8]}",
      "fields": {"status": "done", "completed_qty": 1},
    },
    "dry_run": False,
    "idempotency_key": f"t01-{uuid.uuid4().hex[:12]}",
    "ruleset_id": env["ruleset_id"],
    "actor": {"user_id": "t01-operator", "role": "operator", "channel": "api"},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["tenant_shadow"], ids=["T-01"])
def test_T01_tenant_shadow_mode_l2_write_simulated_no_legacy(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """T-01：shadow_mode=true · L2 write → simulated · Legacy 写计数不变。"""
  tenant_id = "default"
  settings_resp = api_client.put(
    f"/v1/tenants/{tenant_id}/settings",
    json={"shadow_mode": True, "write_approved": False},
  )
  assert settings_resp.status_code == 200, settings_resp.text

  mock_legacy.reset_write_count()
  mock_legacy.reset_entity_store()
  before_writes = mock_legacy.get_write_count()

  exec_resp = api_client.post(
    "/v1/execute",
    json=_l2_execute_body(frozen_graph_env, tenant_id=tenant_id),
  )
  assert exec_resp.status_code == 200, exec_resp.text
  body = exec_resp.json()

  assert body.get("status") == "simulated", body
  assert body.get("shadow_mode") is True, body
  assert mock_legacy.get_write_count() == before_writes, "T-01 shadow 期不得写 Legacy"
