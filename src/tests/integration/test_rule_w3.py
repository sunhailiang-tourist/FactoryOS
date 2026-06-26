"""W3 Rule Engine 集成测试（R-01～R-05）。"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from tests.integration.w3_helpers import (
  bootstrap_frozen_graph,
  sample_graph_body,
  sample_ruleset_body,
)


@pytest.mark.integration
@pytest.mark.parametrize("case", ["deny"], ids=["R-01"])
def test_R01_default_deny_no_matching_rule(case: str, api_client: TestClient) -> None:
  graph = sample_graph_body(graph_id="graph-r01", version="v1.0.0")
  assert api_client.post("/v1/graphs", json=graph).status_code == 201
  deny_rs = {
    **sample_ruleset_body(
      ruleset_id="ruleset-r01",
      graph_id="graph-r01",
      graph_version="v1.0.0",
    ),
    "rules": [
      {
        "id": "rule-admin-only",
        "effect": "allow",
        "subjects": ["role:admin"],
        "actions": ["GOVERNED_WRITE"],
        "priority": 1,
      }
    ],
    "default_effect": "deny",
  }
  assert api_client.post("/v1/rulesets", json=deny_rs).status_code == 201
  assert api_client.post("/v1/rulesets/ruleset-r01/freeze").status_code == 200
  assert api_client.post("/v1/graphs/graph-r01/versions/v1.0.0/submit").status_code == 200
  assert api_client.post("/v1/graphs/graph-r01/versions/v1.0.0/freeze").status_code == 200

  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": "graph-r01",
      "graph_version": "v1.0.0",
      "verb": "GOVERNED_WRITE",
      "params": {"entity_type": "x", "entity_id": "1", "payload": {}},
      "ruleset_id": "ruleset-r01",
      "dry_run": True,
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 403, resp.text
  assert resp.json()["code"] == "RULE_DENIED"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["allow"], ids=["R-02"])
def test_R02_allow_rule_passes(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(
    api_client,
    graph_id="graph-r02",
    ruleset_id="ruleset-r02",
  )
  resp = api_client.post(
    f"/v1/rulesets/{env['ruleset_id']}/evaluate",
    json={
      "graph_id": env["graph_id"],
      "graph_version": env["version"],
      "verb": "GOVERNED_WRITE",
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 200, resp.text
  assert resp.json()["effect"] == "allow"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["deny_wins"], ids=["R-03"])
def test_R03_deny_priority_over_allow(case: str, api_client: TestClient) -> None:
  graph = sample_graph_body(graph_id="graph-r03", version="v1.0.0")
  assert api_client.post("/v1/graphs", json=graph).status_code == 201
  rs = sample_ruleset_body(ruleset_id="ruleset-r03", graph_id="graph-r03", graph_version="v1.0.0")
  rs["rules"].append(
    {
      "id": "rule-deny",
      "effect": "deny",
      "subjects": ["role:operator"],
      "actions": ["GOVERNED_WRITE"],
      "priority": 100,
    }
  )
  assert api_client.post("/v1/rulesets", json=rs).status_code == 201
  resp = api_client.post(
    "/v1/rulesets/ruleset-r03/evaluate",
    json={
      "graph_id": "graph-r03",
      "graph_version": "v1.0.0",
      "verb": "GOVERNED_WRITE",
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 200
  assert resp.json()["effect"] == "deny"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["mismatch"], ids=["R-04"])
def test_R04_ruleset_graph_version_mismatch(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(api_client, graph_id="graph-r04", ruleset_id="ruleset-r04")
  resp = api_client.post(
    f"/v1/rulesets/{env['ruleset_id']}/evaluate",
    json={
      "graph_id": env["graph_id"],
      "graph_version": "v9.9.9",
      "verb": "GOVERNED_WRITE",
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 422, resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["frozen"], ids=["R-05"])
def test_R05_frozen_ruleset_not_editable(case: str, api_client: TestClient) -> None:
  env = bootstrap_frozen_graph(api_client, graph_id="graph-r05", ruleset_id="ruleset-r05")
  body = sample_ruleset_body(
    ruleset_id=env["ruleset_id"],
    graph_id=env["graph_id"],
    graph_version=env["version"],
  )
  resp = api_client.put(f"/v1/rulesets/{env['ruleset_id']}", json=body)
  assert resp.status_code == 409, resp.text
