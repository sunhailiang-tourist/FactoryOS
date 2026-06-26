"""Registry API 集成测试（ADR-008 · R-01 只读）。"""
from __future__ import annotations

import pytest


@pytest.mark.integration
def test_registry_health_after_bootstrap(migrated_db_session) -> None:
  """Registry bootstrap 后 health 探针为 seeded。"""
  from fastapi.testclient import TestClient
  from server.api.main import create_app

  client = TestClient(create_app())
  r = client.get("/v1/registry/health")
  assert r.status_code == 200
  body = r.json()
  assert body["registry_seeded"] is True
  assert body["active_contract_set"] == "factoryos-v1"


@pytest.mark.integration
def test_registry_list_packs_includes_conn_mock(migrated_db_session) -> None:
  """bootstrap 后 pack_registry 含 conn-mock。"""
  from fastapi.testclient import TestClient
  from server.api.main import create_app

  client = TestClient(create_app())
  r = client.get("/v1/registry/packs")
  assert r.status_code == 200
  pack_ids = {p["pack_id"] for p in r.json()}
  assert "conn-mock" in pack_ids


@pytest.mark.integration
def test_registry_get_pack_blueprint(migrated_db_session) -> None:
  """GET pack blueprint 返回 ConnectorBlueprint。"""
  from fastapi.testclient import TestClient
  from server.api.main import create_app

  client = TestClient(create_app())
  r = client.get("/v1/registry/packs/conn-mock")
  assert r.status_code == 200
  assert r.json()["kind"] == "ConnectorBlueprint"
