"""W2 Step1–2：audit migration + E-03 append-only 查询。

业务：执行产生审计；GET /v1/audit/events 按 tenant/exec_id 可查。
上游：audit_service · server.api.modules.audit.controllers
下游：gate step --step 2 -k 'E-03'
"""
from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect

W2_AUDIT_TABLES = ("audit_events", "execution_records")


def _require_w2_migration_tables(migrated_db_session) -> None:
  """W2 Step1：002 migration 后 audit/execution 表须存在。"""
  bind = migrated_db_session.get_bind()
  inspector = inspect(bind)
  for table in W2_AUDIT_TABLES:
    assert inspector.has_table(table), f"W2 Step1: 缺少表 {table}（alembic 002_*）"


@pytest.mark.integration
def test_w2_audit_execution_migration_tables(migrated_db_session) -> None:
  """W2 migration 002：audit_events · execution_records 表存在。"""
  _require_w2_migration_tables(migrated_db_session)


@pytest.mark.integration
@pytest.mark.parametrize("case", ["audit"], ids=["E-03"])
def test_E03_audit_events_after_execute(
  case: str,
  api_client: TestClient,
  migrated_db_session,
  sample_execute_request: dict,
) -> None:
  """E-03：dry_run 执行后 GET /v1/audit/events 有 append-only 记录。"""
  _require_w2_migration_tables(migrated_db_session)

  exec_resp = api_client.post("/v1/execute", json=sample_execute_request)
  assert exec_resp.status_code == 200, exec_resp.text
  exec_body = exec_resp.json()
  exec_id = exec_body["exec_id"]
  tenant_id = sample_execute_request["tenant_id"]

  audit_resp = api_client.get(
    "/v1/audit/events",
    params={"tenant_id": tenant_id, "exec_id": exec_id},
  )
  assert audit_resp.status_code == 200, audit_resp.text
  events = audit_resp.json()
  assert isinstance(events, list), events
  assert len(events) >= 1, "执行后应有 append-only audit 记录"
  assert all(e.get("tenant_id") == tenant_id for e in events)


@pytest.mark.integration
def test_audit_service_append_only_kernel(migrated_db_session) -> None:
  """W2 Step1：audit_service 内核 append + 按 exec_id 查询（无 HTTP）。"""
  _require_w2_migration_tables(migrated_db_session)

  audit_module = importlib.import_module("os_core.audit_service.store")
  append_fn = getattr(audit_module, "append_audit_event", None)
  query_fn = getattr(audit_module, "list_audit_events", None)
  assert append_fn is not None, "缺少 os_core.audit_service.store.append_audit_event"
  assert query_fn is not None, "缺少 os_core.audit_service.store.list_audit_events"

  event = append_fn(
    session=migrated_db_session,
    tenant_id="default",
    event_type="execute.completed",
    exec_id="00000000-0000-4000-8000-000000000001",
    actor={"user_id": "test", "role": "operator"},
    payload={"probe": True},
  )
  migrated_db_session.commit()
  assert event is not None

  rows = query_fn(
    session=migrated_db_session,
    tenant_id="default",
    exec_id="00000000-0000-4000-8000-000000000001",
  )
  assert len(rows) >= 1
