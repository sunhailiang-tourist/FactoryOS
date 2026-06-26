"""W3 测试辅助：frozen graph + allow ruleset 环境。"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from os_core.connector_sdk import mock_legacy
from os_core.graph_service import (
  create_graph,
  freeze_graph_version,
  get_graph_version,
  submit_graph_version,
)
from os_core.graph_service.store import get_graph
from os_core.rule_engine import create_ruleset, freeze_ruleset
from os_core.rule_engine.store import get_ruleset
from os_core.shared_contracts.cmv_registry import draft_graph_checksum
from os_core.shared_contracts.models.graph import BusinessGraph, GraphStatus
from os_core.shared_contracts.models.rule import RuleSet

_NOW = datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sample_graph_body(
  *,
  graph_id: str = "graph-d1-generic-template",
  version: str = "v1.0.0",
  tenant_id: str = "default",
  allowed_dsl: list[str] | None = None,
) -> dict[str, Any]:
  """最小 BusinessGraph 请求体（draft）。"""
  if allowed_dsl is None:
    allowed_dsl = ["QUERY_ENTITY", "GOVERNED_WRITE"]
  return {
    "id": graph_id,
    "version": version,
    "status": "draft",
    "checksum": draft_graph_checksum(),
    "tenant_id": tenant_id,
    "nodes": [{"id": "node-start", "type": "start", "label": "Start"}],
    "edges": [],
    "allowed_dsl": allowed_dsl,
    "metadata": {"created_at": _NOW, "updated_at": _NOW},
  }


def sample_ruleset_body(
  *,
  ruleset_id: str = "ruleset-w3-default",
  graph_id: str = "graph-d1-generic-template",
  graph_version: str = "v1.0.0",
  allow_verbs: list[str] | None = None,
) -> dict[str, Any]:
  """默认 allow operator 的 RuleSet（draft）。"""
  if allow_verbs is None:
    allow_verbs = ["QUERY_ENTITY", "GOVERNED_WRITE"]
  return {
    "id": ruleset_id,
    "graph_id": graph_id,
    "graph_version": graph_version,
    "status": "draft",
    "default_effect": "deny",
    "rules": [
      {
        "id": "rule-allow-operator",
        "effect": "allow",
        "subjects": ["role:operator"],
        "actions": allow_verbs,
        "priority": 10,
      }
    ],
    "metadata": {"created_at": _NOW, "updated_at": _NOW},
  }


def bootstrap_frozen_graph(
  api_client: TestClient,
  *,
  graph_id: str = "graph-d1-generic-template",
  version: str = "v1.0.0",
  ruleset_id: str = "ruleset-w3-default",
  tenant_id: str = "default",
) -> dict[str, str]:
  """创建并 freeze graph + ruleset（W3 execute 前置）。

  返回 graph_id · version · ruleset_id 供 execute 使用。
  """
  mock_legacy.reset_write_count()
  existing = api_client.get(f"/v1/graphs/{graph_id}", params={"version": version})
  if existing.status_code == 200 and existing.json().get("status") == "frozen":
    return {"graph_id": graph_id, "version": version, "ruleset_id": ruleset_id}

  graph = sample_graph_body(graph_id=graph_id, version=version, tenant_id=tenant_id)
  created = api_client.post("/v1/graphs", json=graph)
  assert created.status_code in (201, 409), created.text

  ruleset = sample_ruleset_body(
    ruleset_id=ruleset_id,
    graph_id=graph_id,
    graph_version=version,
  )
  rs_created = api_client.post("/v1/rulesets", json=ruleset)
  assert rs_created.status_code in (201, 409), rs_created.text

  rs = api_client.get(f"/v1/rulesets/{ruleset_id}")
  if rs.status_code == 200 and rs.json().get("status") != "frozen":
    assert api_client.post(f"/v1/rulesets/{ruleset_id}/freeze").status_code == 200

  current = api_client.get(f"/v1/graphs/{graph_id}", params={"version": version})
  assert current.status_code == 200, current.text
  status = current.json()["status"]
  if status == "draft":
    assert api_client.post(f"/v1/graphs/{graph_id}/versions/{version}/submit").status_code == 200
  if status in ("draft", "in_review"):
    freeze_resp = api_client.post(f"/v1/graphs/{graph_id}/versions/{version}/freeze")
    assert freeze_resp.status_code == 200, freeze_resp.text

  final = api_client.get(f"/v1/graphs/{graph_id}", params={"version": version})
  assert final.json()["status"] == "frozen"
  return {"graph_id": graph_id, "version": version, "ruleset_id": ruleset_id}


def seed_frozen_env_kernel(
  session: Session,
  *,
  graph_id: str = "graph-kernel-w3",
  version: str = "v1.0.0",
  ruleset_id: str = "ruleset-kernel-w3",
  tenant_id: str = "default",
) -> dict[str, str]:
  """内核测试用：在同一 Session 种子 frozen graph + ruleset。"""
  if get_graph(session, graph_id=graph_id, version=version) is None:
    graph = BusinessGraph.model_validate(
      sample_graph_body(graph_id=graph_id, version=version, tenant_id=tenant_id)
    )
    create_graph(session, graph)
  if get_ruleset(session, ruleset_id) is None:
    ruleset = RuleSet.model_validate(
      sample_ruleset_body(
        ruleset_id=ruleset_id,
        graph_id=graph_id,
        graph_version=version,
      )
    )
    create_ruleset(session, ruleset)
  rs = get_ruleset(session, ruleset_id)
  if rs is not None and rs.status.value != "frozen":
    freeze_ruleset(session, ruleset_id=ruleset_id)
  graph = get_graph_version(session, graph_id=graph_id, version=version)
  assert graph is not None
  if graph.status == GraphStatus.DRAFT:
    submit_graph_version(session, graph_id=graph_id, version=version)
  graph = get_graph_version(session, graph_id=graph_id, version=version)
  assert graph is not None
  if graph.status == GraphStatus.IN_REVIEW:
    freeze_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return {"graph_id": graph_id, "version": version, "ruleset_id": ruleset_id}
