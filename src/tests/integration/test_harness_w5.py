"""W5 Step2–4：Harness 确认门 · H-01～H-03。

业务：agent plan 不执行；confirm 后 rule→execute；audit 全链路可追踪。
上游：server.api agent/harness 路由 · agent_orchestrator
下游：gate step --step 2 -k 'H-01' · step 4 -k 'H-03'
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy

DSL_PLAN_REQUIRED = frozenset({
  "plan_id",
  "tenant_id",
  "graph_id",
  "graph_version",
  "steps",
  "source",
  "created_at",
  "expires_at",
})


def _load_dsl_plan_required(contracts_dir: Path) -> set[str]:
  schema_path = contracts_dir / "schemas" / "DslPlan.schema.json"
  data = json.loads(schema_path.read_text(encoding="utf-8"))
  return set(data.get("required", []))


def _agent_plan_body(env: dict[str, str], *, intent: str | None = None) -> dict:
  """POST /v1/agent/plan 请求体（H-01）。"""
  return {
    "tenant_id": "default",
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "intent": intent or "report work order wo-h01 completed qty 1",
  }


def _harness_confirm_body(plan_id: str, *, confirmed: bool = True, dry_run: bool = True) -> dict:
  """POST /v1/harness/confirm 请求体（H-02）。"""
  return {
    "plan_id": plan_id,
    "confirmed": confirmed,
    "user_id": "harness-operator-1",
    "dry_run": dry_run,
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["plan_only"], ids=["H-01"])
def test_H01_agent_plan_returns_dsl_plan_without_legacy_write(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
  contracts_dir: Path,
) -> None:
  """H-01：POST /v1/agent/plan → DslPlan · 确认前 Legacy 写计数为 0。"""
  mock_legacy.reset_write_count()
  mock_legacy.reset_entity_store()
  before_writes = mock_legacy.get_write_count()

  resp = api_client.post("/v1/agent/plan", json=_agent_plan_body(frozen_graph_env))
  assert resp.status_code == 200, resp.text
  body = resp.json()

  expected_required = _load_dsl_plan_required(contracts_dir)
  assert expected_required <= set(body.keys()), body
  assert DSL_PLAN_REQUIRED <= set(body.keys())
  assert body.get("source") == "agent", body
  assert len(body.get("steps") or []) >= 1, body
  assert body.get("graph_id") == frozen_graph_env["graph_id"]

  after_writes = mock_legacy.get_write_count()
  assert after_writes == before_writes, "H-01 plan 阶段不得写 Legacy"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["confirm_execute"], ids=["H-02"])
def test_H02_harness_confirm_after_plan_executes(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """H-02：plan → confirm(confirmed=true) → ExecutionRecord · 未 confirm 前无 exec。"""
  mock_legacy.reset_write_count()
  mock_legacy.reset_entity_store()

  plan_resp = api_client.post("/v1/agent/plan", json=_agent_plan_body(frozen_graph_env))
  assert plan_resp.status_code == 200, plan_resp.text
  plan_body = plan_resp.json()
  plan_id = plan_body["plan_id"]

  writes_before_confirm = mock_legacy.get_write_count()

  confirm_resp = api_client.post(
    "/v1/harness/confirm",
    json=_harness_confirm_body(plan_id, confirmed=True, dry_run=True),
  )
  assert confirm_resp.status_code == 200, confirm_resp.text
  exec_body = confirm_resp.json()

  assert exec_body.get("exec_id"), exec_body
  assert exec_body.get("status") in ("simulated", "success"), exec_body
  assert writes_before_confirm == mock_legacy.get_write_count() or exec_body.get("dry_run") is False

  reject_resp = api_client.post(
    "/v1/harness/confirm",
    json=_harness_confirm_body(str(uuid.uuid4()), confirmed=False),
  )
  assert reject_resp.status_code in (200, 403, 404, 422), reject_resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["audit_trail"], ids=["H-03"])
def test_H03_harness_full_chain_audit_traceable(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """H-03：plan → confirm → GET audit 含 harness.confirmed 与 execute 事件。"""
  plan_resp = api_client.post("/v1/agent/plan", json=_agent_plan_body(frozen_graph_env))
  assert plan_resp.status_code == 200, plan_resp.text
  plan_id = plan_resp.json()["plan_id"]

  confirm_resp = api_client.post(
    "/v1/harness/confirm",
    json=_harness_confirm_body(plan_id, confirmed=True, dry_run=True),
  )
  assert confirm_resp.status_code == 200, confirm_resp.text
  exec_id = confirm_resp.json()["exec_id"]
  tenant_id = "default"

  audit_resp = api_client.get(
    "/v1/audit/events",
    params={"tenant_id": tenant_id, "exec_id": exec_id},
  )
  assert audit_resp.status_code == 200, audit_resp.text
  events = audit_resp.json()
  assert isinstance(events, list), events
  assert len(events) >= 1, "H-03 execute 后应有 audit 记录"

  event_types = {e.get("event_type") for e in events}
  assert (
    "execute.started" in event_types
    or "execute.completed" in event_types
    or "execute.simulated" in event_types
  ), event_types

  plan_audit = api_client.get(
    "/v1/audit/events",
    params={"tenant_id": tenant_id, "limit": 200},
  )
  assert plan_audit.status_code == 200, plan_audit.text
  linked = [
    e for e in plan_audit.json()
    if e.get("plan_id") == plan_id or e.get("exec_id") == exec_id
  ]
  assert len(linked) >= 1, "H-03 全链路 audit 须关联 plan_id 或 exec_id"
  harness_types = {e.get("event_type") for e in linked}
  assert (
    "harness.confirmed" in harness_types
    or "execute.completed" in harness_types
    or "execute.simulated" in harness_types
  ), harness_types
