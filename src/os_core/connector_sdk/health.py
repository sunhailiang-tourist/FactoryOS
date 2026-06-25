"""Connector 健康检查（W1 mock · C-01）。

作用：对 Pack 实例做存活探测；W1 无真实 Legacy 调用。
业务关联：OpenAPI GET /v1/connectors/{packId}/health。
上游：apps/api/routes/connectors
下游：未来 Blueprint Runtime / httpx（W4+）
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

import time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

HealthStatus = Literal["ok", "degraded", "down"]


class ConnectorHealthResponse(BaseModel):
  """Connector healthCheck 响应体（对齐 OpenAPI Connector 域）。

  业务含义：实施与监控判断 Pack 是否可达；W1 mock 恒为 ok。
  """

  model_config = ConfigDict(extra="forbid")

  status: HealthStatus = Field(description="ok · degraded · down")
  pack_id: str = Field(description="Connector Pack ID")
  latency_ms: int | None = Field(default=None, description="探测耗时毫秒")


def check_connector_health(pack_id: str, tenant_id: str) -> ConnectorHealthResponse:
  """执行 Connector 健康检查（W1 mock）。

  功能：返回 pack 存活状态；mock 不访问外网。
  业务含义：C-01 验收；tenant_id 预留多租户过滤（W1 仅校验非空）。
  上游调用方：apps/api connector 路由
  下游被调方：未来 catalog Blueprint、httpx
  参数 pack_id：Pack 标识，如 conn-mock
  参数 tenant_id：租户 ID，如 default
  返回：ConnectorHealthResponse
  """
  _ = tenant_id  # W1：预留 tenant 作用域，不做复杂鉴权
  started = time.perf_counter()
  # W1 mock：无业务规则；所有 pack_id 视为本地 mock 可达
  latency_ms = int((time.perf_counter() - started) * 1000)
  return ConnectorHealthResponse(
    status="ok",
    pack_id=pack_id,
    latency_ms=latency_ms,
  )
