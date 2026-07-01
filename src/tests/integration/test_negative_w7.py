"""W7 Step7：负向安全 N-01～N-04。

业务：绕过 rule · checksum 篡改 · 跨 tenant · SQL injection。
上游：plan Step7 · BASE-001 §十三
下游：gate step --step 7 -k 'N-01'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from tests.integration.w3_helpers import bootstrap_frozen_graph, sample_graph_body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["no_internal_bypass"], ids=["N-01"])
def test_N01_no_internal_execute_bypass_endpoint(
  case: str,
  api_client: TestClient,
  sample_execute_request: dict,
) -> None:
  """N-01：无内部写旁路 HTTP 端点。"""
  resp = api_client.post("/v1/internal/execute", json=sample_execute_request)
  assert resp.status_code in (404, 403, 405), resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["checksum_tamper"], ids=["N-02"])
def test_N02_tampered_graph_checksum_rejected_on_freeze(
  case: str,
  api_client: TestClient,
) -> None:
  """N-02：篡改 frozen graph checksum → freeze/execute 校验失败。"""
  suffix = uuid.uuid4().hex[:8]
  env = bootstrap_frozen_graph(
    api_client,
    graph_id=f"graph-n02-{suffix}",
    ruleset_id=f"ruleset-n02-{suffix}",
  )
  body = sample_graph_body(graph_id=env["graph_id"], version=env["version"])
  body["checksum"] = "sha256:" + "f" * 64
  patch_resp = api_client.put(
    f"/v1/graphs/{env['graph_id']}/versions/{env['version']}",
    json=body,
  )
  assert patch_resp.status_code in (200, 409, 422), patch_resp.text

  freeze_resp = api_client.post(
    f"/v1/graphs/{env['graph_id']}/versions/{env['version']}/freeze",
  )
  assert freeze_resp.status_code in (409, 422, 403), freeze_resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["cross_tenant"], ids=["N-03"])
def test_N03_cross_tenant_execution_read_denied(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """N-03：tenant A 执行 · tenant B 读 execution → 403。"""
  tenant_a = "default"
  tenant_b = f"tenant-n03-{uuid.uuid4().hex[:6]}"

  exec_resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": tenant_a,
      "graph_id": frozen_graph_env["graph_id"],
      "graph_version": frozen_graph_env["version"],
      "verb": "GOVERNED_WRITE",
      "params": {
        "entity_type": "work_order",
        "entity_id": f"wo-n03-{uuid.uuid4().hex[:8]}",
        "fields": {"status": "done"},
      },
      "dry_run": True,
      "idempotency_key": f"n03-{uuid.uuid4().hex[:12]}",
      "ruleset_id": frozen_graph_env["ruleset_id"],
      "actor": {"user_id": "n03-a", "role": "operator", "channel": "api"},
    },
  )
  assert exec_resp.status_code == 200, exec_resp.text
  exec_id = exec_resp.json()["exec_id"]

  cross_resp = api_client.get(
    f"/v1/executions/{exec_id}",
    headers={"X-Tenant-Id": tenant_b},
    params={"tenant_id": tenant_b},
  )
  assert cross_resp.status_code == 403, cross_resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["sql_injection"], ids=["N-04"])
def test_N04_sql_injection_in_params_rejected(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """N-04：params 中 SQL injection 模式 → 校验拒绝。"""
  malicious = "wo-1'; DROP TABLE execution_records;--"
  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": frozen_graph_env["graph_id"],
      "graph_version": frozen_graph_env["version"],
      "verb": "GOVERNED_WRITE",
      "params": {
        "entity_type": "work_order",
        "entity_id": malicious,
        "fields": {"status": "done"},
      },
      "dry_run": True,
      "idempotency_key": f"n04-{uuid.uuid4().hex[:12]}",
      "ruleset_id": frozen_graph_env["ruleset_id"],
      "actor": {"user_id": "n04", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code in (400, 422, 403), resp.text
