"""W6 Step3–4：对账 Job stub · K-01/K-02。

业务：run_reconciliation 内核 · POST /v1/reconciliation/run HTTP。
上游：reconciliation_service · mock_legacy read-back
下游：gate step --step 3 -k 'K-01' · step 4 -k 'K-02'
"""
from __future__ import annotations

import importlib
import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from os_core.connector_sdk import mock_legacy

RECON_REPORT_REQUIRED = frozenset({
  "run_id",
  "tenant_id",
  "started_at",
  "finished_at",
  "status",
  "drifts",
})


def _load_reconciliation_required(contracts_dir: Path) -> set[str]:
  schema_path = contracts_dir / "schemas" / "ReconciliationReport.schema.json"
  data = json.loads(schema_path.read_text(encoding="utf-8"))
  return set(data.get("required", []))


def _get_run_reconciliation():
  """导入 W6 Step3 内核 run_reconciliation（未实现时红测）。"""
  module = importlib.import_module("os_core.reconciliation_service")
  fn = getattr(module, "run_reconciliation", None)
  assert fn is not None, "缺少 os_core.reconciliation_service.run_reconciliation"
  return fn


def _l2_execute_for_reconcile(api_client: TestClient, env: dict[str, str]) -> str:
  """先写一笔 L2 成功记录供对账（dry_run=false · conn-mock）。"""
  mock_legacy.reset_write_count()
  mock_legacy.reset_entity_store()
  entity_id = f"wo-k01-{uuid.uuid4().hex[:8]}"
  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": env["graph_id"],
      "graph_version": env["version"],
      "verb": "GOVERNED_WRITE",
      "params": {
        "entity_type": "work_order",
        "entity_id": entity_id,
        "fields": {"status": "done", "completed_qty": 2},
      },
      "dry_run": False,
      "idempotency_key": f"k01-{uuid.uuid4().hex[:12]}",
      "ruleset_id": env["ruleset_id"],
      "actor": {"user_id": "k01-operator", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 200, resp.text
  return entity_id


@pytest.mark.integration
@pytest.mark.parametrize("case", ["no_drift"], ids=["K-01"])
def test_K01_reconciliation_run_returns_ok(
  case: str,
  api_client: TestClient,
  migrated_db_session: Session,
  frozen_graph_env: dict[str, str],
  contracts_dir: Path,
) -> None:
  """K-01：run_reconciliation → ReconciliationReport status=ok · 无 drift。"""
  _l2_execute_for_reconcile(api_client, frozen_graph_env)
  run_reconciliation = _get_run_reconciliation()
  report = run_reconciliation(
    migrated_db_session,
    tenant_id="default",
    scope="ad_hoc",
  )
  migrated_db_session.commit()

  if hasattr(report, "model_dump"):
    body = report.model_dump(mode="json")
  elif isinstance(report, dict):
    body = report
  else:
    pytest.fail(f"run_reconciliation 应返回 ReconciliationReport: {type(report)!r}")

  expected = _load_reconciliation_required(contracts_dir)
  assert expected <= set(body.keys()), body
  assert RECON_REPORT_REQUIRED <= set(body.keys())
  assert body.get("status") == "ok", body
  assert body.get("drifts") == [], body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["mock_drift"], ids=["K-02"])
def test_K02_reconciliation_http_detects_drift_after_tamper(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
  contracts_dir: Path,
) -> None:
  """K-02：篡改 mock Legacy 后 POST /v1/reconciliation/run → drift_detected。"""
  entity_id = _l2_execute_for_reconcile(api_client, frozen_graph_env)
  stored = mock_legacy.get_entity(entity_type="work_order", entity_id=entity_id)
  fields = dict(stored.get("fields") or {})
  fields["completed_qty"] = 999
  mock_legacy.update_entity(
    entity_type="work_order",
    entity_id=entity_id,
    fields=fields,
    pack_id="conn-mock",
    verb="TAMPER_FOR_K02",
  )

  resp = api_client.post(
    "/v1/reconciliation/run",
    json={"tenant_id": "default", "scope": "ad_hoc"},
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()

  expected = _load_reconciliation_required(contracts_dir)
  assert expected <= set(body.keys()), body
  assert body.get("status") == "drift_detected", body
  drifts = body.get("drifts") or []
  assert len(drifts) >= 1, body
