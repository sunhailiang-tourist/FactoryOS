"""W2 Step4：ExecutionEvidence 可重建（E-09）。

业务：GET /v1/executions/{execId}/evidence 返回 F1 审计包。
上游：execution_service · audit_service
下游：gate step --step 4 -k 'E-09'
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

EVIDENCE_REQUIRED = frozenset({
  "exec_id",
  "tenant_id",
  "execution",
  "audit_events",
  "assembled_at",
})


def _load_evidence_schema_required(contracts_dir: Path) -> set[str]:
  schema_path = contracts_dir / "schemas" / "ExecutionEvidence.schema.json"
  data = json.loads(schema_path.read_text(encoding="utf-8"))
  return set(data.get("required", []))


@pytest.mark.integration
@pytest.mark.parametrize("case", ["evidence"], ids=["E-09"])
def test_E09_execution_evidence_rebuildable(
  case: str,
  api_client: TestClient,
  sample_execute_request: dict,
  contracts_dir: Path,
) -> None:
  """E-09：execute 后 GET evidence 200，body 满足 ExecutionEvidence required。"""
  exec_resp = api_client.post("/v1/execute", json=sample_execute_request)
  assert exec_resp.status_code == 200, exec_resp.text
  exec_id = exec_resp.json()["exec_id"]

  evid_resp = api_client.get(f"/v1/executions/{exec_id}/evidence")
  assert evid_resp.status_code == 200, evid_resp.text
  body = evid_resp.json()

  expected_required = _load_evidence_schema_required(contracts_dir)
  assert set(body.keys()) >= expected_required
  assert body["exec_id"] == exec_id
  assert body["tenant_id"] == sample_execute_request["tenant_id"]
  assert isinstance(body["audit_events"], list)
  assert len(body["audit_events"]) >= 1
  assert body["execution"]["exec_id"] == exec_id
  assert EVIDENCE_REQUIRED <= set(body.keys())
