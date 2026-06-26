"""W4 Step3–4：L2 真写 · Revert · Evidence snapshot（E-02 · E-04 · E-05 · E-09+）。

业务：非 dry_run GOVERNED_WRITE 写 Legacy 并持久化 snapshot；revert 闭环。
上游：execution_service · connector_sdk runtime · POST revert HTTP
下游：gate step --step 3 -k 'E-02' · step 4 -k 'E-04'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy


def _l2_execute_body(env: dict[str, str], **overrides) -> dict:
  """W4 L2 真写 ExecuteRequest（dry_run=false）。"""
  base = {
    "tenant_id": "default",
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "verb": "GOVERNED_WRITE",
    "params": {
      "entity_type": "work_order",
      "entity_id": "wo-w4-e02",
      "fields": {"status": "in_progress", "completed_qty": 1},
    },
    "dry_run": False,
    "idempotency_key": f"w4-e02-{uuid.uuid4().hex[:12]}",
    "ruleset_id": env["ruleset_id"],
    "actor": {"user_id": "w4-operator", "role": "operator", "channel": "api"},
  }
  base.update(overrides)
  return base


@pytest.mark.integration
@pytest.mark.parametrize("case", ["l2_write"], ids=["E-02"])
def test_E02_l2_write_success_with_snapshots(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """E-02：GOVERNED_WRITE 非 dry_run → success · before/after snapshot · legacy_refs。"""
  mock_legacy.reset_write_count()
  before_writes = mock_legacy.get_write_count()

  resp = api_client.post("/v1/execute", json=_l2_execute_body(frozen_graph_env))
  assert resp.status_code == 200, resp.text
  body = resp.json()

  assert body.get("status") == "success", body
  assert body.get("dry_run") is False
  assert body.get("before_snapshot") is not None, "E-02 须持久化 before_snapshot"
  assert body.get("after_snapshot") is not None, "E-02 须持久化 after_snapshot"
  legacy_refs = body.get("legacy_refs") or []
  assert len(legacy_refs) >= 1, body
  assert mock_legacy.get_write_count() > before_writes, "L2 真写应递增 Legacy 写计数"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["revert"], ids=["E-04"])
def test_E04_revert_restores_legacy(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """E-04：revert 成功 → 原记录 reverted · Legacy 恢复。"""
  mock_legacy.reset_write_count()
  exec_resp = api_client.post("/v1/execute", json=_l2_execute_body(frozen_graph_env))
  assert exec_resp.status_code == 200, exec_resp.text
  exec_body = exec_resp.json()
  exec_id = exec_body["exec_id"]
  before_snapshot = exec_body.get("before_snapshot")

  revert_resp = api_client.post(f"/v1/execute/{exec_id}/revert")
  assert revert_resp.status_code == 200, revert_resp.text
  reverted = revert_resp.json()
  assert reverted.get("status") == "reverted", reverted

  get_resp = api_client.get(f"/v1/executions/{exec_id}")
  assert get_resp.status_code == 200, get_resp.text
  assert get_resp.json().get("status") == "reverted"

  read_entity = getattr(mock_legacy, "get_entity_snapshot", None)
  if read_entity is not None and before_snapshot:
    current = read_entity(
      entity_type=before_snapshot.get("entity_type", "work_order"),
      entity_id=before_snapshot.get("entity_id", "wo-w4-e02"),
    )
    assert current.get("fields") == before_snapshot.get("fields"), (current, before_snapshot)


@pytest.mark.integration
@pytest.mark.parametrize("case", ["dup_revert"], ids=["E-05"])
def test_E05_duplicate_revert_returns_409(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """E-05：对已 reverted 记录再次 revert → 409。"""
  exec_resp = api_client.post("/v1/execute", json=_l2_execute_body(frozen_graph_env))
  assert exec_resp.status_code == 200, exec_resp.text
  exec_id = exec_resp.json()["exec_id"]

  first = api_client.post(f"/v1/execute/{exec_id}/revert")
  assert first.status_code == 200, first.text

  second = api_client.post(f"/v1/execute/{exec_id}/revert")
  assert second.status_code == 409, second.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["evidence_snapshots"], ids=["E-09"])
def test_E09_evidence_includes_snapshots_after_l2_write(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """E-09 增强：L2 真写后 evidence.execution 含 before/after snapshot。"""
  exec_resp = api_client.post("/v1/execute", json=_l2_execute_body(frozen_graph_env))
  assert exec_resp.status_code == 200, exec_resp.text
  exec_id = exec_resp.json()["exec_id"]

  evid_resp = api_client.get(f"/v1/executions/{exec_id}/evidence")
  assert evid_resp.status_code == 200, evid_resp.text
  evidence = evid_resp.json()
  execution = evidence.get("execution") or {}
  assert execution.get("before_snapshot") is not None, evidence
  assert execution.get("after_snapshot") is not None, evidence
