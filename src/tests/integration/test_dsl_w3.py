"""W3 DSL registry 与 execute 动词门禁（D-01～D-03）。"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.integration.w3_helpers import bootstrap_frozen_graph, sample_graph_body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["list"], ids=["D-01"])
def test_D01_list_dsl_registry(case: str, api_client: TestClient) -> None:
  resp = api_client.get("/v1/dsl/registry")
  assert resp.status_code == 200, resp.text
  verbs = {item["verb"] for item in resp.json()}
  assert "QUERY_ENTITY" in verbs
  assert "GOVERNED_WRITE" in verbs


@pytest.mark.integration
@pytest.mark.parametrize("case", ["unknown"], ids=["D-02"])
def test_D02_unknown_verb_rejected(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict,
) -> None:
  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": frozen_graph_env["graph_id"],
      "graph_version": frozen_graph_env["version"],
      "verb": "UNKNOWN_VERB",
      "params": {},
      "ruleset_id": frozen_graph_env["ruleset_id"],
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 400, resp.text
  assert resp.json()["code"] == "DSL_UNKNOWN"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["whitelist"], ids=["D-03"])
def test_D03_verb_not_in_graph_allowed_dsl(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-d03",
    ruleset_id="ruleset-d03",
  )
  body = sample_graph_body(
    graph_id=env["graph_id"],
    version="v1.0.2",
    allowed_dsl=["QUERY_ENTITY"],
  )
  assert api_client.post("/v1/graphs", json=body).status_code == 201
  from tests.integration.w3_helpers import sample_ruleset_body

  rs = sample_ruleset_body(
    ruleset_id="ruleset-d03b",
    graph_id=env["graph_id"],
    graph_version="v1.0.2",
    allow_verbs=["GOVERNED_WRITE", "QUERY_ENTITY"],
  )
  assert api_client.post("/v1/rulesets", json=rs).status_code == 201
  assert api_client.post("/v1/rulesets/ruleset-d03b/freeze").status_code == 200
  assert api_client.post(f"/v1/graphs/{env['graph_id']}/versions/v1.0.2/submit").status_code == 200
  assert api_client.post(f"/v1/graphs/{env['graph_id']}/versions/v1.0.2/freeze").status_code == 200

  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": env["graph_id"],
      "graph_version": "v1.0.2",
      "verb": "GOVERNED_WRITE",
      "params": {"entity_type": "x", "entity_id": "1", "payload": {}},
      "ruleset_id": "ruleset-d03b",
      "dry_run": True,
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 403, resp.text
  assert resp.json()["code"] == "DSL_NOT_IN_GRAPH"
