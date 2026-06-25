"""Connector 域 HTTP 路由（OpenAPI /v1/connectors）。

作用：薄路由层，委托 connector_sdk 公开面。
业务关联：C-01 healthCheck。
上游：FastAPI app
下游：os_core.connector_sdk.health
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

from fastapi import APIRouter, Query

from os_core.connector_sdk.health import check_connector_health

router = APIRouter(tags=["Connector"])


@router.get("/v1/connectors/{pack_id}/health")
def connector_health(
  pack_id: str,
  tenant_id: str = Query(..., description="租户 ID"),
) -> dict[str, str | int | None]:
  """GET /v1/connectors/{packId}/health（C-01）。

  功能：返回 Connector 健康状态 JSON。
  业务含义：集成实施验证 Pack 连通性；W1 为 mock。
  上游调用方：Studio、监控、集成测试
  下游被调方：connector_sdk.check_connector_health
  参数 pack_id：路径 Pack ID
  参数 tenant_id：查询参数租户
  返回：status · pack_id · latency_ms
  """
  result = check_connector_health(pack_id=pack_id, tenant_id=tenant_id)
  return result.model_dump()
