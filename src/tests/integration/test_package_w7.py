"""W7 Step3–4：Package export/import · P-01～P-03。

业务：Implementation Package 导出/导入 · Override 差量生效。
上游：plan Step3–4 · OpenAPI packages/*
下游：gate step --step 3 -k 'P-01' · step 4 -k 'P-02'/'P-03'
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PACKAGE_REQUIRED = frozenset({
  "package_id",
  "tenant_id",
  "version",
  "exported_at",
  "graphs",
  "rulesets",
})


def _load_package_required(contracts_dir: Path) -> set[str]:
  schema_path = contracts_dir / "schemas" / "ImplementationPackage.schema.json"
  data = json.loads(schema_path.read_text(encoding="utf-8"))
  return set(data.get("required", []))


@pytest.mark.integration
@pytest.mark.parametrize("case", ["export"], ids=["P-01"])
def test_P01_package_export_contains_graphs_rulesets_connectors(
  case: str,
  api_client: TestClient,
  contracts_dir: Path,
) -> None:
  """P-01：POST /v1/packages/export → graphs · rulesets · connector_configs。"""
  resp = api_client.post(
    "/v1/packages/export",
    json={"tenant_id": "default", "delivery": "D1"},
  )
  assert resp.status_code == 200, resp.text
  body = resp.json()

  expected = _load_package_required(contracts_dir)
  assert expected <= set(body.keys()), body
  assert PACKAGE_REQUIRED <= set(body.keys())
  assert len(body.get("graphs") or []) >= 1, body
  assert len(body.get("rulesets") or []) >= 1, body
  assert "connector_configs" in body, body


@pytest.mark.integration
@pytest.mark.parametrize("case", ["import"], ids=["P-02"])
def test_P02_package_import_enables_tenant_b_pack_resolve(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict[str, str],
) -> None:
  """P-02：export tenant A → import tenant B → resolve Pack。"""
  export_resp = api_client.post(
    "/v1/packages/export",
    json={"tenant_id": "default", "delivery": "D1"},
  )
  assert export_resp.status_code == 200, export_resp.text
  package = export_resp.json()
  tenant_b = f"tenant-b-w7-{uuid.uuid4().hex[:6]}"
  package["tenant_id"] = tenant_b
  package["source_tenant_id"] = "default"

  import_resp = api_client.post("/v1/packages/import", json=package)
  assert import_resp.status_code == 200, import_resp.text
  imported = import_resp.json()
  assert imported.get("tenant_id") == tenant_b, imported

  health_resp = api_client.get(
    "/v1/connectors/conn-mock/health",
    params={"tenant_id": tenant_b},
  )
  assert health_resp.status_code == 200, health_resp.text
  assert health_resp.json().get("status") in ("ok", "degraded"), health_resp.json()


@pytest.mark.integration
@pytest.mark.parametrize("case", ["override"], ids=["P-03"])
def test_P03_tenant_override_base_url_applied_at_runtime(
  case: str,
  api_client: TestClient,
) -> None:
  """P-03：tenant B overrides.yaml 改 base_url → runtime 使用新 URL。"""
  tenant_b = f"tenant-override-w7-{uuid.uuid4().hex[:6]}"
  override_url = "https://override-mes.example.local/v1"

  settings_resp = api_client.put(
    f"/v1/tenants/{tenant_b}/settings",
    json={
      "shadow_mode": True,
      "connector_overrides": {
        "conn-mock": {"base_url": override_url},
      },
    },
  )
  assert settings_resp.status_code == 200, settings_resp.text

  test_resp = api_client.post(
    "/v1/integration/connect/test",
    json={"tenant_id": tenant_b, "pack_id": "conn-mock"},
  )
  assert test_resp.status_code == 200, test_resp.text
  body = test_resp.json()
  assert body.get("base_url") == override_url or body.get("resolved_base_url") == override_url, body
