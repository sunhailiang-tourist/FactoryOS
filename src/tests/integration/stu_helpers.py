"""STU-001 集成测试辅助（阶段 1 · Studio RBAC · API 头）。

业务：统一 actor 角色头 · 租户 · mock pack。
上游：test_stu001_*.py
下游：gate step --step N -k 'STU-09'
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

MOCK_PACK_ID = "conn-mock"
KINGDEE_MOCK_PACK = "kingdee-mock"
DEFAULT_TENANT = "default"


def studio_headers(*, role: str, user_id: str | None = None) -> dict[str, str]:
  """Studio RBAC 测试头（Dev Step1 须在 AuthMiddleware 解析）。"""
  return {
    "X-Actor-Role": role,
    "X-Actor-User-Id": user_id or f"stu-test-{role}",
    "X-Tenant-Id": DEFAULT_TENANT,
  }


def get_studio_flows(client: TestClient, *, role: str) -> Any:
  """GET /v1/studio/flows — Studio 六步导航真源（studio_flows.json）。"""
  return client.get("/v1/studio/flows", headers=studio_headers(role=role))


def count_system_relations(session, *, tenant_id: str) -> int:
  """system_relations 行数（STU-02 Registry API 落库断言）。"""
  from os_core.platform_registry import tenant_config_store

  return len(tenant_config_store.list_system_relations(session, tenant_id=tenant_id))
