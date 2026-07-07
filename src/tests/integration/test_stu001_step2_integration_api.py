"""阶段1 Step2：integration API · STU-02 · STU-03 · STU-11。

业务：discover/prove/mappings 经 API · Registry 落库 · shadow · secrets_ref。
上游：plan Step2 · OpenAPI /v1/integration/*
下游：gate step --step 2 -k 'STU-02'
"""
from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient
from tests.integration.stu_helpers import (
  DEFAULT_TENANT,
  KINGDEE_MOCK_PACK,
  MOCK_PACK_ID,
  count_system_relations,
  studio_headers,
)


@pytest.mark.integration
@pytest.mark.parametrize("case", ["registry_via_api"], ids=["STU-02"])
def test_STU02_connect_creates_system_relation_via_api(
  case: str,
  api_client: TestClient,
  migrated_db_session,
) -> None:
  """STU-02：Studio connect API 后 system_relations 经 API 落库（非仅 bootstrap）。"""
  before = count_system_relations(migrated_db_session, tenant_id=DEFAULT_TENANT)
  resp = api_client.post(
    "/v1/integration/connect/test",
    headers=studio_headers(role="integrator"),
    json={"tenant_id": DEFAULT_TENANT, "pack_id": MOCK_PACK_ID},
  )
  assert resp.status_code == 200, resp.text
  register = api_client.post(
    "/v1/integration/connect/register",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": DEFAULT_TENANT,
      "pack_id": MOCK_PACK_ID,
      "lifecycle": "connected",
    },
  )
  assert register.status_code in (200, 201), register.text
  after = count_system_relations(migrated_db_session, tenant_id=DEFAULT_TENANT)
  assert after > before, "connect 后须新增 system_relations 记录"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["discover"], ids=["STU-02-discover"])
def test_STU02_discover_endpoint_returns_cmv_candidates(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-02/Step2：POST /v1/integration/discover 返回 CMV 候选。"""
  resp = api_client.post(
    "/v1/integration/discover",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": DEFAULT_TENANT,
      "pack_id": KINGDEE_MOCK_PACK,
      "sample_paths": ["/work_orders"],
    },
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()
  verbs = body.get("verbs") or body.get("candidates") or []
  assert len(verbs) >= 1, body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["shadow_prove"], ids=["STU-03"])
def test_STU03_prove_respects_shadow_before_write_approved(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """STU-03：Prove 后 shadow 未批准 · L2 写须 simulated 或 403。"""
  prove = api_client.post(
    "/v1/integration/prove/run",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": DEFAULT_TENANT,
      "pack_id": MOCK_PACK_ID,
      "approve_write": False,
    },
  )
  assert prove.status_code == 200, prove.text

  api_client.put(
    f"/v1/tenants/{DEFAULT_TENANT}/settings",
    headers=studio_headers(role="integrator"),
    json={"shadow_mode": True, "write_approved": False},
  )

  exec_resp = api_client.post(
    "/v1/execute",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": DEFAULT_TENANT,
      "graph_id": frozen_graph_env["graph_id"],
      "graph_version": frozen_graph_env["version"],
      "verb": "GOVERNED_WRITE",
      "params": {
        "entity_type": "work_order",
        "entity_id": "wo-stu03-shadow",
        "fields": {"status": "done"},
      },
      "dry_run": False,
      "idempotency_key": "stu03-shadow-key",
      "ruleset_id": frozen_graph_env["ruleset_id"],
      "actor": {"user_id": "stu03", "role": "integrator", "channel": "api"},
    },
  )
  assert exec_resp.status_code in (200, 403), exec_resp.text
  if exec_resp.status_code == 200:
    body = exec_resp.json()
    assert body.get("status") in ("simulated", "SIMULATED", "dry_run"), body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["secrets_ref"], ids=["STU-11"])
def test_STU11_mappings_reject_plaintext_secrets(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-11：mapping 凭证仅 secrets_ref · 响应不含明文 secret。"""
  resp = api_client.put(
    f"/v1/integration/mappings/{MOCK_PACK_ID}",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": DEFAULT_TENANT,
      "mappings": {"auth": {"password": "plaintext-secret-123"}},
      "secrets_ref": "vault://tenant/default/conn-mock",
    },
  )
  assert resp.status_code in (200, 422), resp.text
  if resp.status_code == 422:
    return
  text = json.dumps(resp.json())
  assert "plaintext-secret-123" not in text, "响应不得回显明文 secret"
  assert "secrets_ref" in text or resp.json().get("secrets_ref"), resp.text
