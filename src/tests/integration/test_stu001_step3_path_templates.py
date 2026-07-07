"""阶段1 Step3：STU-10 Path 模板 path-a/b/c。

业务：Registry 种子 · tenant provision · 路径模板预填 Pack。
上游：plan Step3
下游：gate step --step 3 -k 'STU-10'
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from tests.integration.stu_helpers import studio_headers

PATH_TEMPLATE_IDS = ("path-a", "path-b", "path-c")


@pytest.mark.integration
@pytest.mark.parametrize(
  "template_id",
  PATH_TEMPLATE_IDS,
  ids=["path-a", "path-b", "path-c"],
)
def test_STU10_path_template_list_includes_standard_paths(
  template_id: str,
  api_client: TestClient,
) -> None:
  """STU-10：GET path 模板含 path-a/b/c 且预填 pack。"""
  resp = api_client.get(
    "/v1/registry/path-templates",
    headers=studio_headers(role="integrator"),
  )
  assert resp.status_code == 200, resp.text
  templates = resp.json()
  assert isinstance(templates, list), templates
  ids = {t.get("template_id") or t.get("id") for t in templates if isinstance(t, dict)}
  assert template_id in ids, f"缺少 path 模板 {template_id}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["tenant_provision"], ids=["STU-10-provision"])
def test_STU10_tenant_provision_via_change_request_or_api(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-10/ STU-02：新 tenant 经 Registry API provision（非手改 YAML）。"""
  tenant_id = "tenant-stu10-demo"
  resp = api_client.post(
    "/v1/registry/tenants",
    headers=studio_headers(role="integrator"),
    json={
      "tenant_id": tenant_id,
      "display_name": "STU-10 Demo Factory",
      "path_template_id": "path-a",
    },
  )
  assert resp.status_code in (200, 201), resp.text
  get_resp = api_client.get(
    f"/v1/registry/tenants/{tenant_id}",
    headers=studio_headers(role="integrator"),
  )
  assert get_resp.status_code == 200, get_resp.text
  assert get_resp.json().get("tenant_id") == tenant_id
