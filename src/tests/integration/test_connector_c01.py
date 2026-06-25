"""W1 Step4：Connector mock healthCheck（C-01）。

业务：GET /v1/connectors/{packId}/health 返回 status=ok；mock 不含业务规则。
上游：connector_sdk · apps/api routes
下游：gate step --step 4 -k 'C-01'
"""
from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient

MOCK_PACK_ID = "conn-mock"
DEFAULT_TENANT_ID = "default"


@pytest.fixture
def api_client() -> TestClient:
  """FastAPI 同步测试客户端（W1 Step4 路由挂载后可用）。"""
  main = importlib.import_module("apps.api.main")
  create_app = getattr(main, "create_app", None)
  assert create_app is not None, "apps.api.main 缺少 create_app"
  return TestClient(create_app())


@pytest.mark.integration
@pytest.mark.parametrize("case", ["health"], ids=["C-01"])
def test_C01_connector_health_returns_ok(case: str, api_client: TestClient) -> None:
  """C-01：GET connector health 返回 200 且 status=ok。"""
  response = api_client.get(
    f"/v1/connectors/{MOCK_PACK_ID}/health",
    params={"tenant_id": DEFAULT_TENANT_ID},
  )
  assert response.status_code == 200, response.text
  body = response.json()
  assert body.get("status") == "ok", body
  assert body.get("pack_id") == MOCK_PACK_ID
