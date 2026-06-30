"""W6 Step2：License 门禁 · T-02（execute 未授权 Pack）。

业务：execution 前 license_service 拦截 · 403 + audit license.denied。
上游：plan Step2 · execution_service 钩子
下游：gate step --step 2 -k 'T-02'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient


def _execute_body(env: dict[str, str], *, tenant_id: str = "tenant-unlicensed-w6") -> dict:
  """未授权 tenant 的 ExecuteRequest（T-02）。"""
  return {
    "tenant_id": tenant_id,
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "verb": "GOVERNED_WRITE",
    "params": {
      "entity_type": "work_order",
      "entity_id": "wo-t02",
      "fields": {"status": "done", "completed_qty": 1},
    },
    "dry_run": True,
    "idempotency_key": f"t02-{uuid.uuid4().hex[:12]}",
    "ruleset_id": env["ruleset_id"],
    "actor": {"user_id": "t02-operator", "role": "operator", "channel": "api"},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["unlicensed_pack"], ids=["T-02"])
def test_T02_execute_unlicensed_pack_returns_403_and_audit(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """T-02：未授权 Pack execute → 403 MODULE_NOT_LICENSED · audit license.denied。"""
  tenant_id = "tenant-unlicensed-w6"
  resp = api_client.post("/v1/execute", json=_execute_body(frozen_graph_env, tenant_id=tenant_id))
  assert resp.status_code == 403, resp.text
  body = resp.json()
  assert body.get("code") == "MODULE_NOT_LICENSED", body

  audit_resp = api_client.get(
    "/v1/audit/events",
    params={"tenant_id": tenant_id, "event_type": "license.denied", "limit": 20},
  )
  assert audit_resp.status_code == 200, audit_resp.text
  events = audit_resp.json()
  assert isinstance(events, list), events
  assert len(events) >= 1, "T-02 须写 license.denied audit"
