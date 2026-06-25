"""W1 Step1：FastAPI 进程存活探针。

业务：Control Plane CI 就绪前须能 GET /health；非 OpenAPI 正式域路由。
上游：apps/api/main.py create_app
下游：gate step --step 1 -k 'workflow'
"""
from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.mark.workflow
def test_health_endpoint_returns_200() -> None:
  """GET /health 返回 200（W1 Step1 交付物）。"""
  main = importlib.import_module("apps.api.main")
  create_app = getattr(main, "create_app", None)
  assert create_app is not None, "apps.api.main 缺少 create_app 工厂"

  client = TestClient(create_app())
  response = client.get("/health")

  assert response.status_code == 200, response.text
  body = response.json()
  assert body.get("status") in ("ok", "healthy"), body
