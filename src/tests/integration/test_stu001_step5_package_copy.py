"""阶段1 Step5：STU-06 · STU-07 · STU-08 Package 复制与 Git 禁止项。

业务：export/import 第二家 · 交付 Runbook 无 YAML 手改路径。
上游：plan Step5 · P-01～P-03
下游：gate step --step 5 -k 'STU-06'
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from tests.integration.stu_helpers import DEFAULT_TENANT, studio_headers


@pytest.mark.integration
@pytest.mark.parametrize("case", ["export"], ids=["STU-06"])
def test_STU06_package_export_matches_p01_contract(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-06：Studio export · graphs/rulesets/connectors（P-01）。"""
  resp = api_client.post(
    "/v1/packages/export",
    headers=studio_headers(role="integrator"),
    json={"tenant_id": DEFAULT_TENANT, "delivery": "D1"},
  )
  assert resp.status_code == 200, resp.text
  pkg = resp.json()
  for key in ("graphs", "rulesets", "connector_configs"):
    assert key in pkg, f"ImplementationPackage 须含 {key}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["second_tenant"], ids=["STU-07"])
def test_STU07_second_tenant_import_via_studio_api(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-07：第二家 tenant import Package + override 经 API。"""
  tenant_b = f"tenant-stu07-{uuid.uuid4().hex[:6]}"
  export = api_client.post(
    "/v1/packages/export",
    headers=studio_headers(role="integrator"),
    json={"tenant_id": DEFAULT_TENANT, "delivery": "D1"},
  )
  assert export.status_code == 200, export.text
  package = export.json()

  import_resp = api_client.post(
    "/v1/packages/import",
    headers=studio_headers(role="integrator"),
    json={**package, "tenant_id": tenant_b},
  )
  assert import_resp.status_code == 200, import_resp.text

  configs = package.get("connector_configs", [{}])
  pack_id = configs[0].get("pack_id", "conn-mock") if configs else "conn-mock"
  health = api_client.get(
    f"/v1/connectors/{pack_id}/health",
    params={"tenant_id": tenant_b},
  )
  assert health.status_code == 200, health.text


@pytest.mark.workflow
def test_STU08_delivery_runbook_forbids_yaml_hand_edit(repo_root) -> None:
  """STU-08：交付 Runbook 不得含「手改 YAML 上线」步骤。"""
  runbook = repo_root / "docs" / "准备" / "2026-06-16" / "04-工厂实施手册.md"
  assert runbook.is_file(), "缺少工厂实施手册"
  text = runbook.read_text(encoding="utf-8")
  forbidden = ("手改 YAML 上线", "vim integration/tenants", "直接改 tenants/*.yaml")
  hits = [phrase for phrase in forbidden if phrase in text]
  assert not hits, f"Runbook 含禁止的生产配置路径描述: {hits}"
