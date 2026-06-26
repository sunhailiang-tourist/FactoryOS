"""Registry 变更请求集成测试（人审写路径 · ADR-008）。"""
from __future__ import annotations

import pytest


@pytest.mark.integration
def test_change_request_pack_upsert_approve_flow() -> None:
  """提案 pack → pending → approve → pack_registry 可读。"""
  from fastapi.testclient import TestClient
  from server.api.main import create_app

  client = TestClient(create_app())
  create = client.post(
    "/v1/registry/change-requests",
    json={
      "tenant_id": "default",
      "kind": "pack_upsert",
      "proposed_by": "integrator-test",
      "proposal_body": {
        "pack_id": "conn-test-change",
        "body_yaml": (
          "apiVersion: factoryos.io/v1\n"
          "kind: ConnectorBlueprint\n"
          "metadata:\n  pack_id: conn-test-change\n"
          "spec:\n  ops:\n    - verb: GOVERNED_WRITE\n"
        ),
      },
    },
  )
  assert create.status_code == 201, create.text
  request_id = create.json()["request_id"]
  assert create.json()["status"] == "pending"

  approve = client.post(
    f"/v1/registry/change-requests/{request_id}/approve",
    json={"actor_id": "admin-test"},
  )
  assert approve.status_code == 200, approve.text
  assert approve.json()["status"] == "approved"

  pack = client.get("/v1/registry/packs/conn-test-change")
  assert pack.status_code == 200
  assert pack.json()["metadata"]["pack_id"] == "conn-test-change"


@pytest.mark.integration
def test_change_request_reject() -> None:
  """reject 后 status=rejected，不写入 pack。"""
  from fastapi.testclient import TestClient
  from server.api.main import create_app

  client = TestClient(create_app())
  create = client.post(
    "/v1/registry/change-requests",
    json={
      "kind": "pack_upsert",
      "proposed_by": "ai-agent",
      "ai_model_id": "test-model",
      "proposal_body": {"pack_id": "conn-reject-me", "body_yaml": "invalid: true\n"},
    },
  )
  assert create.status_code == 201
  request_id = create.json()["request_id"]

  reject = client.post(
    f"/v1/registry/change-requests/{request_id}/reject",
    json={"actor_id": "admin-test", "reason": "invalid blueprint"},
  )
  assert reject.status_code == 200
  assert reject.json()["status"] == "rejected"
  assert client.get("/v1/registry/packs/conn-reject-me").status_code == 404
