"""阶段1 Step4：STU-01 · STU-04 · STU-05 onboard / 开写双签 / freeze。

业务：Studio API 六步闭环 · Audit 事件 · 无 Git/YAML 旁路。
上游：plan Step4
下游：gate step --step 4 -k 'STU-01'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from tests.integration.stu_helpers import (
  DEFAULT_TENANT,
  MOCK_PACK_ID,
  studio_headers,
)
from tests.integration.w3_helpers import bootstrap_frozen_graph, sample_graph_body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["onboard_api"], ids=["STU-01"])
def test_STU01_onboard_connect_to_export_without_git(
  case: str,
  api_client: TestClient,
  migrated_db_session,
) -> None:
  """STU-01：connect→discover→map→prove→freeze→export 全经 API（零仓库）。"""
  headers = studio_headers(role="integrator")
  suffix = uuid.uuid4().hex[:8]
  graph_id = f"graph-stu01-{suffix}"
  version = "v1.0.0"

  assert api_client.post(
    "/v1/integration/connect/test",
    headers=headers,
    json={"tenant_id": DEFAULT_TENANT, "pack_id": MOCK_PACK_ID},
  ).status_code == 200

  assert api_client.post(
    "/v1/integration/discover",
    headers=headers,
    json={"tenant_id": DEFAULT_TENANT, "pack_id": MOCK_PACK_ID},
  ).status_code == 200

  assert api_client.put(
    f"/v1/integration/mappings/{MOCK_PACK_ID}",
    headers=headers,
    json={"tenant_id": DEFAULT_TENANT, "mappings": {"entity": "work_order"}},
  ).status_code == 200

  assert api_client.post(
    "/v1/integration/prove/run",
    headers=headers,
    json={"tenant_id": DEFAULT_TENANT, "pack_id": MOCK_PACK_ID},
  ).status_code == 200

  graph_body = sample_graph_body(graph_id=graph_id, version=version)
  assert api_client.post("/v1/graphs", json=graph_body).status_code == 201
  assert api_client.post(f"/v1/graphs/{graph_id}/versions/{version}/freeze").status_code == 200

  export = api_client.post(
    "/v1/packages/export",
    headers=headers,
    json={"tenant_id": DEFAULT_TENANT, "delivery": "D1"},
  )
  assert export.status_code == 200, export.text
  pkg = export.json()
  assert pkg.get("graphs") or pkg.get("package_id"), pkg


@pytest.mark.integration
@pytest.mark.parametrize("case", ["write_approve"], ids=["STU-04"])
def test_STU04_write_approved_audit_after_g_write_approve(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-04：G-WRITE-APPROVE → write_approved + audit integration.write_approved。"""
  headers = studio_headers(role="integrator")
  approve = api_client.put(
    f"/v1/tenants/{DEFAULT_TENANT}/settings",
    headers=headers,
    json={"write_approved": True, "shadow_mode": False},
  )
  assert approve.status_code == 200, approve.text

  audit = api_client.get(
    "/v1/audit/events",
    params={"tenant_id": DEFAULT_TENANT, "event_type": "integration.write_approved"},
  )
  assert audit.status_code == 200, audit.text
  events = audit.json()
  assert len(events) >= 1, "开写双签须写 Audit integration.write_approved"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["graph_freeze"], ids=["STU-05"])
def test_STU05_graph_freeze_audit_event(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-05：Studio freeze → Audit GRAPH_FREEZE / graph.frozen。"""
  env = bootstrap_frozen_graph(
    api_client,
    graph_id=f"graph-stu05-{uuid.uuid4().hex[:6]}",
    ruleset_id=f"ruleset-stu05-{uuid.uuid4().hex[:6]}",
  )
  audit = api_client.get(
    "/v1/audit/events",
    params={
      "tenant_id": DEFAULT_TENANT,
      "event_type": "graph.frozen",
    },
  )
  assert audit.status_code == 200, audit.text
  events = audit.json()
  graph_ids = {e.get("graph_id") for e in events}
  assert env["graph_id"] in graph_ids, "freeze 须产生 graph.frozen 审计"
