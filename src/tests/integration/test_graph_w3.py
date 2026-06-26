"""W3 Graph freeze 集成测试（G-01～G-08）。"""
from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy
from tests.integration.w3_helpers import bootstrap_frozen_graph, sample_graph_body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["create"], ids=["G-01"])
def test_G01_create_draft_graph(case: str, api_client: TestClient) -> None:
  body = sample_graph_body(graph_id="graph-g01", version="v1.0.0")
  resp = api_client.post("/v1/graphs", json=body)
  assert resp.status_code == 201, resp.text
  assert resp.json()["status"] == "draft"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["update"], ids=["G-02"])
def test_G02_update_draft_graph(case: str, api_client: TestClient) -> None:
  body = sample_graph_body(graph_id="graph-g02", version="v1.0.0")
  assert api_client.post("/v1/graphs", json=body).status_code == 201
  body["nodes"][0]["label"] = "Updated"
  resp = api_client.put("/v1/graphs/graph-g02/versions/v1.0.0", json=body)
  assert resp.status_code == 200, resp.text
  assert resp.json()["nodes"][0]["label"] == "Updated"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["not_frozen"], ids=["G-03"])
def test_G03_execute_l2_on_draft_graph_rejected(case: str, api_client: TestClient) -> None:
  graph = sample_graph_body(graph_id="graph-g03", version="v1.0.0")
  assert api_client.post("/v1/graphs", json=graph).status_code == 201
  from tests.integration.w3_helpers import sample_ruleset_body

  rs = sample_ruleset_body(
    ruleset_id="ruleset-g03",
    graph_id="graph-g03",
    graph_version="v1.0.0",
  )
  assert api_client.post("/v1/rulesets", json=rs).status_code == 201
  assert api_client.post("/v1/rulesets/ruleset-g03/freeze").status_code == 200

  exec_body = {
    "tenant_id": "default",
    "graph_id": "graph-g03",
    "graph_version": "v1.0.0",
    "verb": "GOVERNED_WRITE",
    "params": {"entity_type": "x", "entity_id": "1", "payload": {}},
    "ruleset_id": "ruleset-g03",
    "dry_run": True,
    "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
  }
  resp = api_client.post("/v1/execute", json=exec_body)
  assert resp.status_code == 409, resp.text
  assert resp.json()["code"] == "GRAPH_NOT_FROZEN"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["submit"], ids=["G-04"])
def test_G04_submit_to_in_review(case: str, api_client: TestClient) -> None:
  body = sample_graph_body(graph_id="graph-g04", version="v1.0.0")
  assert api_client.post("/v1/graphs", json=body).status_code == 201
  resp = api_client.post("/v1/graphs/graph-g04/versions/v1.0.0/submit")
  assert resp.status_code == 200, resp.text
  assert resp.json()["status"] == "in_review"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["freeze"], ids=["G-05"])
def test_G05_freeze_graph_with_frozen_ruleset(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-g05",
    version="v1.0.0",
    ruleset_id="ruleset-g05",
  )
  resp = api_client.get(
    f"/v1/graphs/{env['graph_id']}",
    params={"version": env["version"]},
  )
  assert resp.status_code == 200
  data = resp.json()
  assert data["status"] == "frozen"
  assert data["checksum"].startswith("sha256:")
  assert data["checksum"] != sample_graph_body()["checksum"]


@pytest.mark.integration
@pytest.mark.parametrize("case", ["immutable"], ids=["G-06"])
def test_G06_frozen_graph_not_editable(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-g06",
    version="v1.0.0",
    ruleset_id="ruleset-g06",
  )
  body = sample_graph_body(graph_id=env["graph_id"], version=env["version"])
  body["nodes"][0]["label"] = "Nope"
  resp = api_client.put(
    f"/v1/graphs/{env['graph_id']}/versions/{env['version']}",
    json=body,
  )
  assert resp.status_code == 409, resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["clone"], ids=["G-07"])
def test_G07_clone_new_draft_version(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-g07",
    version="v1.0.0",
    ruleset_id="ruleset-g07",
  )
  resp = api_client.post(f"/v1/graphs/{env['graph_id']}/versions/{env['version']}/clone")
  assert resp.status_code == 201, resp.text
  cloned = resp.json()
  assert cloned["version"] == "v1.0.1"
  assert cloned["status"] == "draft"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["deprecated"], ids=["G-08"])
def test_G08_execute_on_deprecated_graph_rejected(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-g08",
    version="v1.0.0",
    ruleset_id="ruleset-g08",
  )
  graph_mod = importlib.import_module("os_core.graph_service")
  deprecate = getattr(graph_mod, "deprecate_graph_version")
  from apps.api.deps import get_db_session

  session = next(get_db_session())
  try:
    deprecate(session, graph_id=env["graph_id"], version=env["version"])
    session.commit()
  finally:
    session.close()

  mock_legacy.reset_write_count()
  exec_body = {
    "tenant_id": "default",
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "verb": "GOVERNED_WRITE",
    "params": {"entity_type": "x", "entity_id": "1", "payload": {}},
    "ruleset_id": env["ruleset_id"],
    "dry_run": False,
    "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
  }
  resp = api_client.post("/v1/execute", json=exec_body)
  assert resp.status_code == 409, resp.text
